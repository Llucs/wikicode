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
        resp = httpx.get("https://html.duckduckgo.com/html/", params={"q": query},
            headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        if resp.status_code == 200:
            for m in re.finditer(r'class="result__snippet"[^>]*>(.*?)</(?:a|span|td)', resp.text, re.DOTALL):
                text = html_mod.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
                if text and len(text) > 30:
                    add(text[:500], "DDG")
    except Exception as e:
        log(f"DDG error: {e}")
    try:
        resp = httpx.get("https://en.wikipedia.org/w/api.php",
            params={"action": "opensearch", "search": query, "limit": 5, "format": "json"}, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            if len(data) > 2:
                for title, desc in zip(data[1][:3], data[2][:3]):
                    if desc:
                        add(f"{title}: {desc[:500]}", "Wiki")
    except Exception as e:
        log(f"Wiki error: {e}")
    try:
        resp = httpx.get("https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_"), timeout=15)
        if resp.status_code == 200:
            wd = resp.json()
            if wd.get("extract"):
                add(wd["extract"][:1500], "Wiki-summary")
    except Exception:
        pass
    if not results:
        try:
            resp = httpx.get("https://api.duckduckgo.com/", params={"q": query, "format": "json", "no_html": 1}, timeout=15)
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
        {"role": "system", "content": "You are a thorough research assistant. Provide detailed, factual information. Include what it is, key features, history, use cases, installation, and basic usage. Up to 3000 chars."},
        {"role": "user", "content": f"Research: {query}"},
    ]
    try:
        return api_chat(messages)
    except Exception as e:
        log(f"AI research failed: {e}")
        return ""

def slugify(text):
    s = text.lower().strip(" .:;,!?")
    s = s.replace(" ", "-")
    s = re.sub(r"[^a-z0-9\u00e0-\u00ff-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "untitled"

def clean_title(text):
    return text.strip().rstrip(" .:;,!?")

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
        m = re.match(r"(-\s+\[\s*\]\s+\*\*(.+?)\*\*)\s*(.*)", line)
        if m:
            if current:
                current["block"] = "\n".join(lines[task_block_start:i])
                tasks.append(current)
            current = {"title": clean_title(m.group(2)), "desc": m.group(3).strip(), "block": "", "start": task_block_start}
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
        try:
            result = subprocess.run(["git", "grep", "-l", "-i", slug.replace("-", " "), "--", str(section)],
                capture_output=True, text=True, timeout=15, cwd=WORKSPACE)
            if result.stdout.strip():
                return True
        except subprocess.TimeoutExpired:
            pass
    return False

def list_documented_tools():
    td = WORKSPACE / "docs" / "tools"
    return [d.name for d in td.iterdir() if d.is_dir() and (d / "index.md").exists()] if td.exists() else []

def list_documented_projects():
    pd = WORKSPACE / "projects"
    return [d.name for d in pd.iterdir() if d.is_dir()] if pd.exists() else []

def discover_one_tool():
    existing = list_documented_tools()
    existing_str = "\n".join(f"- {t}" for t in existing) if existing else "None yet."
    web_data = web_search_deep("best developer tools 2026")
    messages = [
        {"role": "system", "content": "You are a tool curator. Using the web research, suggest 1 real developer tool worth documenting that is NOT already documented. Output exactly:\n- **Tool Name.** One-sentence description containing the word 'tool'.\nONLY suggest well-known real tools (e.g. Kubernetes, Docker, Redis, Postman, Grafana, etc.). Do NOT invent or combine tools."},
        {"role": "user", "content": f"Already documented:\n{existing_str}\n\nWeb research:\n{web_data}\n\nSuggest 1 real tool."},
    ]
    try:
        raw = api_chat(messages)
        for line in raw.split("\n"):
            m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
            if m:
                title = clean_title(m.group(1))
                desc = m.group(2).strip() if m.group(2) else ""
                if not topic_exists(slugify(title)):
                    return {"title": title, "desc": desc}
    except Exception as e:
        log(f"Tool discovery failed: {e}")
    return None

def discover_one_project():
    existing = list_documented_projects()
    existing_str = "\n".join(f"- {p}" for p in existing) if existing else "None yet."
    web_data = web_search_deep("most popular open source projects on GitHub")
    messages = [
        {"role": "system", "content": "You are a project curator. From the web search results, pick ONE real, well-known open-source project that is NOT already documented. Output exactly:\n- **Project Name.** One-sentence description of what the project does and its primary language.\nONLY pick real projects with 10k+ GitHub stars."},
        {"role": "user", "content": f"Already documented:\n{existing_str}\n\nWeb research:\n{web_data}\n\nPick 1 real project from the search results."},
    ]
    try:
        raw = api_chat(messages)
        for line in raw.split("\n"):
            m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
            if m:
                title = clean_title(m.group(1))
                desc = m.group(2).strip() if m.group(2) else ""
                if not topic_exists(slugify(title)):
                    return {"title": f"Analyze {title} project", "desc": desc}
    except Exception as e:
        log(f"Project discovery failed: {e}")
    return None

def discover_one_article():
    existing_titles = set()
    for f in (WORKSPACE / "docs").rglob("*.md"):
        existing_titles.add(f.stem)
    web_data = web_search_deep("best software architecture and development articles 2026")
    messages = [
        {"role": "system", "content": "You are a content curator. From the web search results, pick ONE real technical article topic that would be useful for developers and is NOT already documented. Output exactly:\n- **Article Title.** One-sentence description.\nONLY pick well-established topics (design patterns, system design, performance, security, etc.)."},
        {"role": "user", "content": f"Web research:\n{web_data}\n\nPick 1 real article topic."},
    ]
    try:
        raw = api_chat(messages)
        for line in raw.split("\n"):
            m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
            if m:
                title = clean_title(m.group(1))
                desc = m.group(2).strip() if m.group(2) else ""
                if slugify(title) not in existing_titles and not topic_exists(slugify(title)):
                    return {"title": title, "desc": desc}
    except Exception as e:
        log(f"Article discovery failed: {e}")
    return None

def add_task_to_queue(title, desc):
    title = clean_title(title)
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
        {"role": "system", "content": "You are a task clarifier. Respond with ONE clear sentence describing what should be documented."},
        {"role": "user", "content": f"Describe: {task['title']}"},
    ]
    try:
        desc = api_chat(messages)
        task["desc"] = desc[:300]
    except Exception:
        task["desc"] = task.get("desc", "") or f"Document {task['title']}."
    return task

def research_topic(topic, kind):
    web_data = web_search_deep(topic)
    ai_data = ai_research(topic)
    parts = []
    if web_data:
        parts.append(f"=== Web Research ===\n{web_data}")
    if ai_data:
        parts.append(f"=== AI Knowledge ===\n{ai_data}")
    return "\n\n".join(parts)

def generate_content(task, research, memory):
    kind = "tool"  # default
    title = task["title"].lower()
    desc = task["desc"].lower()
    combined = title + " " + desc
    if "project" in combined:
        kind = "project"
    elif "snippet" in combined:
        kind = "snippet"
    tool_kw = ["tool","technology","framework","container","database","cli","library","platform","orchestrator","dashboard","monitoring","proxy","engine"]
    if any(w in combined for w in tool_kw):
        kind = "tool"
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
        parts += ["", "Document a REAL open-source project's architecture. Cover: tech stack, project structure, how it works internally, setup guide, key code insights. DO NOT invent fictional projects."]
    elif kind == "snippet":
        parts += ["", "Generate an index.md for a code snippet. Include code with explanation, copy-paste-ready."]
    elif kind == "tool":
        parts += ["", "Document a REAL developer tool. Cover: what, why, install, usage, key features with command examples. DO NOT invent fictional tools."]
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
    kind = "tool"
    combined = (task["title"] + " " + task.get("desc", "")).lower()
    if "project" in combined:
        kind = "project"
    elif "snippet" in combined:
        kind = "snippet"
    tool_kw = ["tool","technology","framework","container","database","cli","library","platform","orchestrator","dashboard","monitoring","proxy","engine"]
    if any(w in combined for w in tool_kw):
        kind = "tool"
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
    result = subprocess.run(["mkdocs", "build", "--clean"], cwd=WORKSPACE, capture_output=True, text=True, timeout=120)
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
    for attempt in range(3):
        try:
            git("pull", "--rebase", "origin", "main")
            git("push", "origin", "HEAD")
            log("Pushed.")
            return
        except subprocess.CalledProcessError as e:
            log(f"Push attempt {attempt+1}/3 failed: {e}")
            if attempt < 2:
                time.sleep(5)
    raise RuntimeError("Failed to push after 3 attempts")
