#!/usr/bin/env python3
import os, re, subprocess, sys, time, html as html_mod
from datetime import date
from pathlib import Path
import httpx

API_BASE = "https://opencode.ai/zen/v1"
API_KEY = "public"
MODEL = "deepseek-v4-flash-free"
WORKSPACE = Path(os.environ.get("GITHUB_WORKSPACE", os.getcwd()))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "")
TODAY = date.today().isoformat()

def log(msg):
    print(f"[agent] {msg}", flush=True)

def git(*args):
    return subprocess.check_output(["git"] + list(args), cwd=WORKSPACE, text=True).strip()

def api_chat(messages, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            resp = httpx.post(
                f"{API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
                json={"model": MODEL, "messages": messages},
                timeout=180,
            )
            if resp.status_code == 500:
                log(f"API 500: {resp.text[:300]}")
                time.sleep(10)
                continue
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            log(f"API attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                time.sleep(10)
    raise RuntimeError(f"API call failed after {max_retries} attempts")

def web_search_deep(query):
    results = []
    seen = set()
    def add(text, source):
        key = text[:100].lower()
        if key not in seen:
            seen.add(key)
            results.append(f"- [{source}] {text[:600]}")

    try:
        resp = httpx.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query},
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Mozilla/5.0"},
            timeout=20,
        )
        if resp.status_code == 200:
            for m in re.finditer(r'class="result__snippet"[^>]*>(.*?)</(?:a|span|td)', resp.text, re.DOTALL):
                text = html_mod.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
                if text and len(text) > 30:
                    add(text[:500], "DDG")
            for m in re.finditer(r'class="result__title"[^>]*>.*?href="(.*?)".*?>(.*?)</a>', resp.text, re.DOTALL):
                title = html_mod.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
                if title and len(title) > 10:
                    add(title[:300], "DDG-title")
    except Exception as e:
        log(f"DDG html error: {e}")

    try:
        resp = httpx.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "opensearch", "search": query, "limit": 5, "format": "json"},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 2:
                for title, desc in zip(data[1][:3], data[2][:3]):
                    if desc:
                        add(f"{title}: {desc[:500]}", "Wiki")
    except Exception as e:
        log(f"Wiki search error: {e}")

    try:
        resp = httpx.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_"),
            timeout=15,
        )
        if resp.status_code == 200:
            wd = resp.json()
            extract = wd.get("extract", "")[:1500]
            if extract:
                add(extract, "Wiki-summary")
    except Exception:
        pass

    if not results:
        try:
            resp = httpx.get(
                "https://api.duckduckgo.com/",
                params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("AbstractText"):
                    add(data["AbstractText"][:1000], "DDG-IA")
                for topic in data.get("RelatedTopics", [])[:5]:
                    if "Text" in topic:
                        add(topic["Text"][:500], "DDG-rel")
        except Exception:
            pass

    return "\n".join(results)

def ai_research(query):
    messages = [
        {"role": "system", "content": "You are a thorough research assistant. Provide detailed, factual information about the given topic. Include what it is, key features, history, use cases, installation, and basic usage. Be as comprehensive as possible. Up to 3000 characters."},
        {"role": "user", "content": f"Research this topic thoroughly: {query}"},
    ]
    try:
        return api_chat(messages)
    except Exception as e:
        log(f"AI research failed: {e}")
        return ""

def slugify(text):
    s = text.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\u00e0-\u00ff-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "untitled"

def read_memory():
    files = {}
    path = WORKSPACE / "memory"
    if path.exists():
        for f in sorted(path.glob("*.md")):
            files[f.stem] = f.read_text(encoding="utf-8")
    return files

def parse_queue():
    path = WORKSPACE / "tasks" / "queue.md"
    if not path.exists():
        return [], ""
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    tasks = []
    in_task = False
    current = None
    task_block_start = 0
    for i, line in enumerate(lines):
        m = re.match(r"(-\s+\[\s*\]\s+\*\*(.+?)\*\*\s*(.*))", line)
        if m:
            if current:
                current["block"] = "\n".join(lines[task_block_start:i])
                tasks.append(current)
            current = {"title": m.group(2).strip(), "desc": m.group(3).strip(), "block": "", "start": task_block_start}
            task_block_start = i
            in_task = True
        elif in_task and line.strip() and not line.startswith("- ") and not line.startswith("#") and not line.startswith("---"):
            pass
        elif in_task and (line.startswith("- ") or line.startswith("#") or line.strip() == ""):
            if current:
                current["block"] = "\n".join(lines[task_block_start:i])
                tasks.append(current)
                current = None
            in_task = False
    if current:
        current["block"] = "\n".join(lines[task_block_start:])
        tasks.append(current)
    return tasks, content

def topic_exists(slug):
    for section in [WORKSPACE / "docs", WORKSPACE / "projects", WORKSPACE / "snippets"]:
        if not section.exists():
            continue
        for subdir in section.rglob("*"):
            if subdir.is_dir() and subdir.name == slug:
                return True
            if subdir.is_dir() and subdir.name.startswith(slug[:20]):
                return True
        try:
            result = subprocess.run(
                ["git", "grep", "-l", "-i", slug.replace("-", " "), "--", str(section)],
                capture_output=True, text=True, timeout=15, cwd=WORKSPACE,
            )
            if result.stdout.strip():
                return True
        except subprocess.TimeoutExpired:
            pass
    return False

def classify_task(task):
    title = task["title"].lower()
    desc = task["desc"].lower()
    combined = title + " " + desc
    if "project" in combined:
        return "project"
    if "snippet" in combined:
        return "snippet"
    if any(w in combined for w in ["tool", "technology", "framework", "container", "database", "cli", "library", "platform", "orchestrator", "dashboard", "monitoring", "observability", "proxy", "server", "engine", "manager", "runner", "tracker", "formatter", "linter", "compiler", "bundler", "runner"]):
        return "tool"
    return "article"

def list_documented_tools():
    tools_dir = WORKSPACE / "docs" / "tools"
    if not tools_dir.exists():
        return []
    return [d.name for d in tools_dir.iterdir() if d.is_dir() and (d / "index.md").exists()]

def list_documented_projects():
    proj_dir = WORKSPACE / "projects"
    if not proj_dir.exists():
        return []
    return [d.name for d in proj_dir.iterdir() if d.is_dir()]

def discover_deep():
    existing = list_documented_tools()
    existing_str = "\n".join(f"- {t}" for t in existing) if existing else "None yet."

    categories = [
        "monitoring and observability tools (Grafana, Prometheus, Datadog, Heimdall)",
        "container and orchestration tools (Docker, Kubernetes, Podman, containerd)",
        "CI/CD and automation tools (Jenkins, GitHub Actions, ArgoCD, Ansible)",
        "database and storage tools (PostgreSQL, Redis, SQLite, MongoDB, MinIO)",
        "developer productivity tools (tmux, zsh, fzf, ripgrep, fd, lazygit)",
        "networking and proxy tools (nginx, Traefik, Caddy, HAProxy, Cloudflare)",
        "security tools (Vault, Let's Encrypt, OWASP ZAP, Trivy, SonarQube)",
        "frontend tools (Vite, Webpack, esbuild, Tailwind, shadcn/ui)",
        "backend and API tools (FastAPI, Express, Gin, Fiber, gRPC, GraphQL)",
        "infrastructure as code (Terraform, Pulumi, Crossplane, OpenTofu)",
    ]

    all_suggestions = []
    seen_titles = set()

    for cat_text in categories:
        messages = [
            {"role": "system", "content": f"You are a deep tool researcher. From the category '{cat_text}', suggest 2 specific developer tools that are real and well-known. Output each as exactly: - **Tool Name.** One-sentence description containing the word 'tool'. Do NOT suggest anything already documented."},
            {"role": "user", "content": f"Already documented:\n{existing_str}\n\nSuggest 2 tools from this category."},
        ]
        try:
            raw = api_chat(messages)
            for line in raw.split("\n"):
                m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
                if m:
                    title = m.group(1).strip()
                    desc = m.group(2).strip() if m.group(2) else ""
                    slug = slugify(title)
                    if slug not in seen_titles and not topic_exists(slug):
                        seen_titles.add(slug)
                        all_suggestions.append({"title": title, "desc": desc})
        except Exception as e:
            log(f"Category '{cat_text}' failed: {e}")

    log(f"Deep discovery found {len(all_suggestions)} new tools")
    return all_suggestions

def discover_tools():
    existing = list_documented_tools()
    existing_str = "\n".join(f"- {t}" for t in existing) if existing else "None yet."
    web_data = web_search_deep("best developer tools 2026 most used open source")
    messages = [
        {"role": "system", "content": "You are a developer tool curator. Using the web research below, suggest 4 real developer tools worth documenting. Include BOTH very popular AND lesser-known but powerful tools. Do NOT suggest already documented tools. Output exactly: - **Tool Name.** One-sentence description containing the word 'tool'."},
        {"role": "user", "content": f"Already documented:\n{existing_str}\n\nWeb research:\n{web_data}\n\nSuggest 4 diverse tools."},
    ]
    try:
        raw = api_chat(messages)
        tasks = []
        seen = set()
        for line in raw.split("\n"):
            m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
            if m:
                title = m.group(1).strip()
                desc = m.group(2).strip() if m.group(2) else ""
                slug = slugify(title)
                if slug not in seen and not topic_exists(slug):
                    seen.add(slug)
                    tasks.append({"title": title, "desc": desc})
        return tasks
    except Exception as e:
        log(f"Tool discovery failed: {e}")
        return []

def discover_projects():
    existing = list_documented_projects()
    existing_str = "\n".join(f"- {p}" for p in existing) if existing else "None yet."
    web_data = web_search_deep("interesting developer projects to build 2026")
    messages = [
        {"role": "system", "content": "Using web research, suggest 2 real-world developer project ideas worth documenting. Each must use a real technology stack. Include diverse tech (not all web frameworks). Output exactly: - **Project Name.** One-sentence description containing the word 'project'."},
        {"role": "user", "content": f"Existing:\n{existing_str}\n\nWeb research:\n{web_data}\n\nSuggest 2 new projects."},
    ]
    try:
        raw = api_chat(messages)
        tasks = []
        seen = set()
        for line in raw.split("\n"):
            m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
            if m:
                title = m.group(1).strip()
                desc = m.group(2).strip() if m.group(2) else ""
                slug = slugify(title)
                if slug not in seen and not topic_exists(slug):
                    seen.add(slug)
                    tasks.append({"title": f"Create {title} project", "desc": desc})
        return tasks
    except Exception as e:
        log(f"Project discovery failed: {e}")
        return []

def ensure_tools_section_populated():
    tools = list_documented_tools()
    if len(tools) >= 10:
        return
    log(f"Tools section sparse ({len(tools)} tools) — deep discovering")
    for t in discover_deep():
        add_task_to_queue(t["title"], t["desc"])

def add_task_to_queue(title, desc):
    qpath = WORKSPACE / "tasks" / "queue.md"
    if not qpath.exists():
        return
    content = qpath.read_text(encoding="utf-8")
    if slugify(title) in content.lower():
        return
    content = content.rstrip() + f"\n- [ ] **{title}.** {desc}\n"
    qpath.write_text(content, encoding="utf-8")
    log(f"Added task: {title}")

def enrich_task(task):
    if task.get("desc") and len(task["desc"]) > 10:
        return task
    messages = [
        {"role": "system", "content": "You are a task clarifier. Given a task title, respond with ONE clear sentence describing what should be documented."},
        {"role": "user", "content": f"Describe this task: {task['title']}"},
    ]
    try:
        desc = api_chat(messages)
        task["desc"] = desc[:300]
    except Exception as e:
        log(f"Enrichment failed: {e}")
        task["desc"] = task.get("desc", "") or f"Document {task['title']}."
    return task

def research_topic(topic, kind):
    web_data = web_search_deep(topic)
    ai_data = ai_research(topic)
    combined = ""
    if web_data:
        combined += f"=== Web Research ===\n{web_data}\n\n"
    if ai_data:
        combined += f"=== AI Knowledge ===\n{ai_data}\n"
    return combined.strip()

def generate_content(task, research, memory):
    kind = classify_task(task)
    parts = [
        "You are WikiCode Agent. You produce a high-quality developer wiki page with REAL, USEFUL content.",
        "RULES:",
        "1. Output ONLY the Markdown file content.",
        "2. Start with YAML frontmatter:",
        "   ---",
        "   title: <Exact descriptive title>",
        "   description: <One sentence summary>",
        "   created: <YYYY-MM-DD>",
        "   tags:",
        "     - <tag1>",
        "     - <tag2>",
        "   status: draft",
        "   ---",
        "3. Include REAL code blocks with proper syntax highlighting.",
        "4. Do NOT wrap output in ``` fences.",
    ]
    if kind == "project":
        parts += ["", "Generate an index.md for a runnable project. Include architecture, setup, code examples."]
    elif kind == "snippet":
        parts += ["", "Generate an index.md for a code snippet. Include code with explanation, copy-paste-ready."]
    elif kind == "tool":
        parts += ["", "Document a REAL developer tool. Cover: what, why, install, basic usage, key features with command examples. DO NOT invent fictional tools or document this repository."]
    else:
        parts += ["", "Generate a developer article with code examples and best practices."]
    system = "\n".join(parts)
    user = f"Task: {task['title']}\nDescription: {task['desc']}\nToday: {TODAY}\n"
    if research:
        user += f"\nResearch:\n{research}\n"
    user += "\nGenerate the complete Markdown file now."
    log(f"Generating {kind}: {task['title']}")
    return api_chat([{"role": "system", "content": system}, {"role": "user", "content": user}])

def write_files(task, content):
    kind = classify_task(task)
    slug = slugify(task["title"])
    created = []
    if kind == "project":
        base = WORKSPACE / "projects" / slug
        base.mkdir(parents=True, exist_ok=True)
        idx = base / "index.md"
        idx.write_text(content, encoding="utf-8")
        created.append(idx)
        readme = base / "README.md"
        if not readme.exists():
            readme.write_text(f"# {task['title']}\n\n{task['desc']}\n", encoding="utf-8")
            created.append(readme)
    elif kind == "snippet":
        base = WORKSPACE / "snippets" / slug
        base.mkdir(parents=True, exist_ok=True)
        idx = base / "index.md"
        idx.write_text(content, encoding="utf-8")
        created.append(idx)
    elif kind == "tool":
        base = WORKSPACE / "docs" / "tools" / slug
        base.mkdir(parents=True, exist_ok=True)
        idx = base / "index.md"
        idx.write_text(content, encoding="utf-8")
        created.append(idx)
    else:
        fpath = WORKSPACE / "docs" / f"{slug}.md"
        fpath.write_text(content, encoding="utf-8")
        created.append(fpath)
    return created

def write_report(task, files):
    slug = slugify(task["title"])
    rdir = WORKSPACE / "docs" / "reports"
    rdir.mkdir(parents=True, exist_ok=True)
    path = rdir / f"{TODAY}-{slug}.md"
    lines = [
        "---",
        f'title: "{task["title"]}"',
        "description: Agent execution report",
        f"created: {TODAY}",
        "tags:",
        "  - agent",
        "status: completed",
        "---",
        "",
        f"# Report: {task['title']}",
        "",
        f"**Date:** {TODAY}",
        "**Agent:** WikiCode autonomous (OpenCode API)",
        "",
        "## Summary",
        "",
        f"Executed task: **{task['title']}**",
        "",
        "### Files",
        "",
    ]
    for f in files:
        lines.append(f"- `{f.relative_to(WORKSPACE)}`")
    lines.extend(["", "### Result", "", "Task completed successfully.", ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path

def update_task_lists(task, report):
    qpath = WORKSPACE / "tasks" / "queue.md"
    cpath = WORKSPACE / "tasks" / "completed.md"
    if qpath.exists():
        content = qpath.read_text(encoding="utf-8")
        block = task.get("block", "")
        if block:
            content = content.replace(block, "")
            content = re.sub(r"\n{3,}", "\n\n", content).strip() + "\n"
        qpath.write_text(content, encoding="utf-8")
    row = f"| {TODAY} | {task['title']} | [{task['title']}]({report.relative_to(WORKSPACE)}) |\n"
    if cpath.exists():
        content = cpath.read_text(encoding="utf-8")
        if row.strip() not in content:
            content = content.rstrip() + "\n" + row
            cpath.write_text(content, encoding="utf-8")

def validate():
    log("Running mkdocs build validation...")
    result = subprocess.run(
        ["mkdocs", "build", "--clean"],
        cwd=WORKSPACE, capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        log(f"Build FAILED:\n{result.stderr[:2000]}")
        return False
    log("Build passed.")
    return True

def commit_and_push(files, task):
    git("add", "-A")
    status = git("status", "--porcelain")
    if not status:
        log("No changes to commit.")
        return
    msg = f"wikicode: {slugify(task['title'])}"
    git("commit", "-m", msg)
    log(f"Committed: {msg}")
    if GITHUB_TOKEN and GITHUB_REPO:
        git("remote", "set-url", "origin", f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git")
    git("push", "origin", "HEAD")
    log("Pushed.")

def main():
    log(f"Starting — model={MODEL}")
    memory = read_memory()
    log(f"Read {len(memory)} memory files")

    ensure_tools_section_populated()

    tasks, _ = parse_queue()
    log(f"Pending: {len(tasks)}")

    if not tasks:
        log("Queue empty — deep discovering new content")
        for t in discover_tools():
            add_task_to_queue(t["title"], t["desc"])
        for t in discover_projects():
            add_task_to_queue(t["title"], t["desc"])
        tasks, _ = parse_queue()
        log(f"After discovery: {len(tasks)} tasks")
        if not tasks:
            log("No tasks found. Done.")
            return 0

    task = enrich_task(tasks[0])
    log(f"Task: {task['title']}")
    research = research_topic(task["title"], classify_task(task))
    log(f"Research: {len(research)} chars")
    content = generate_content(task, research, memory)
    if not content:
        log("No content generated.")
        return 1
    log(f"Generated: {len(content)} chars")
    files = write_files(task, content)
    report = write_report(task, files)
    update_task_lists(task, report)
    log("Task lists updated.")
    if not validate():
        log("Validation failed — reverting.")
        git("checkout", ".")
        return 1
    commit_and_push(files, task)
    log("Done.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
