import os, re, subprocess, sys, time, json, html as html_mod
from datetime import date
from pathlib import Path
import concurrent.futures
import httpx

API_BASE = "http://127.0.0.1:8080/v1"
API_KEY = ""
MODEL = "Qwen3.6-27B-IQ2_M-mtp"
WORKSPACE = Path(os.environ.get("GITHUB_WORKSPACE", os.getcwd()))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "")
TODAY = date.today().isoformat()

LANGUAGES = [
    ("pt", "Portugu\u00eas", "Portuguese"),
    ("es", "Espa\u00f1ol", "Spanish"),
    ("fr", "Fran\u00e7ais", "French"),
    ("de", "Deutsch", "German"),
    ("ja", "\u65e5\u672c\u8a9e", "Japanese"),
    ("zh", "\u4e2d\u6587", "Chinese"),
]

def log(msg):
    print(f"[agent] {msg}", flush=True)

def git(*args):
    return subprocess.check_output(["git"] + list(args), cwd=WORKSPACE, text=True).strip()

def api_chat(messages, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            headers = {"Content-Type": "application/json"}
            if API_KEY:
                headers["Authorization"] = f"Bearer {API_KEY}"
            resp = httpx.post(
                f"{API_BASE}/chat/completions",
                headers=headers,
                json={"model": MODEL, "messages": messages},
                timeout=3600,
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
            for m in re.finditer(r'[^>]*class="result__snippet"[^>]*>(.*?)</(?:a|span|td)', resp.text, re.DOTALL):
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

def translate_content(markdown_text, target_language):
    messages = [
        {"role": "system", "content": (
            "You are a professional technical translator. Translate the following Markdown document "
            f"to {target_language}. "
            "Rules:\n"
            "1. Translate the YAML frontmatter 'title' and 'description' fields only. Keep all other frontmatter fields unchanged.\n"
            "2. Preserve ALL Markdown syntax exactly: headings, lists, bold, italic, links, images, tables, code fences, admonitions.\n"
            "3. DO NOT translate content inside code blocks (```...```) or inline code (`...`).\n"
            "4. DO NOT translate URLs, file paths, command-line examples, or technical terms (API, REST, Git, Docker, HTTP, JSON, YAML, etc.).\n"
            "5. Keep proper nouns, brand names, and tool names in their original form.\n"
            "6. Output ONLY the translated Markdown file content. No explanations, no notes.\n"
            "7. Do NOT wrap the output in ```md fences."
        )},
        {"role": "user", "content": markdown_text},
    ]
    return api_chat(messages)

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
    if not td.exists():
        return []
    result = []
    for d in td.iterdir():
        if d.is_dir() and d.name != "archive":
            if (d / "index.en.md").exists() or (d / "index.md").exists():
                result.append(d.name)
    return result

def list_documented_projects():
    pd = WORKSPACE / "projects"
    return [d.name for d in pd.iterdir() if d.is_dir()] if pd.exists() else []

TOOL_SEARCHES = [
    ("monitoring and observability", "monitoring and observability tools Prometheus Grafana Loki"),
    ("container and orchestration", "container orchestration tools Docker Kubernetes Podman"),
    ("CI/CD and automation", "CI/CD automation and pipeline tools Jenkins ArgoCD Ansible"),
    ("database and storage", "database storage tools PostgreSQL Redis MongoDB SQLite"),
    ("developer productivity", "developer productivity CLI terminal tools fzf ripgrep lazygit"),
    ("networking and proxy", "networking reverse proxy tools nginx Traefik Caddy HAProxy"),
    ("security and secrets", "security secrets vulnerability tools Vault Trivy SonarQube"),
    ("frontend build tools", "frontend web build tools Vite Webpack esbuild Tailwind"),
    ("backend and API tools", "backend API framework tools FastAPI Express Gin Kafka GraphQL"),
    ("infrastructure as code", "infrastructure as code tools Terraform Pulumi Ansible Vagrant"),
]

def discover_one_tool():
    existing = list_documented_tools()
    existing_lower = [t.lower() for t in existing]

    for cat_name, search_query in TOOL_SEARCHES:
        web_data = web_search_deep(search_query)
        if not web_data:
            continue
        existing_str = "\n".join(f"- {t}" for t in existing) if existing else "None yet."
        messages = [
            {"role": "system", "content": "You are a tool curator reading web search results. Pick ONE real developer tool mentioned in the results that is NOT already documented. Output exactly:\n- **Tool Name.** One-sentence description containing the word 'tool'.\nONLY pick a tool that appears in the search results. NEVER invent or suggest article topics."},
            {"role": "user", "content": f"Already documented:\n{existing_str}\n\nWeb search results for '{cat_name}':\n{web_data}\n\nPick 1 real tool from these results."},
        ]
        try:
            raw = api_chat(messages)
            for line in raw.split("\n"):
                m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
                if m:
                    title = clean_title(m.group(1))
                    desc = m.group(2).strip() if m.group(2) else ""
                    slug = slugify(title)
                    if topic_exists(slug):
                        continue
                    return {"title": title, "desc": desc, "kind": "tool"}
        except Exception as e:
            log(f"Tool discovery '{cat_name}' failed: {e}")
    return None

PROJECT_SEARCHES = [
    ("most popular frontend framework", "most popular frontend JavaScript framework React Vue Angular Svelte"),
    ("most popular backend framework", "most popular backend framework Django Express Spring Boot FastAPI"),
    ("popular programming language", "popular programming language Rust Go TypeScript Zig adoption"),
    ("state management library", "popular state management library Redux Zustand TanStack Query Zustand"),
    ("testing library framework", "most popular testing library framework Jest Vitest Playwright Cypress"),
    ("build tool bundler", "most popular build tool bundler Webpack Vite esbuild Rollup Turborepo"),
    ("CSS framework library", "popular CSS framework library Tailwind Styled Components Sass"),
    ("mobile cross platform framework", "popular mobile cross platform framework React Native Flutter"),
    ("machine learning framework", "popular machine learning AI framework TensorFlow PyTorch LangChain"),
]

def discover_one_project():
    existing = list_documented_projects()
    existing_lower = [t.lower() for t in existing]

    for cat_name, search_query in PROJECT_SEARCHES:
        web_data = web_search_deep(search_query)
        if not web_data:
            continue
        existing_str = "\n".join(f"- {p}" for p in existing) if existing else "None yet."
        messages = [
            {"role": "system", "content": "You are a project curator reading web search results. Pick ONE real open-source project from the results that is NOT already documented. Output exactly:\n- **Project Name.** One-sentence description of what it does and its primary language.\nONLY pick a real project mentioned in the search results."},
            {"role": "user", "content": f"Already documented:\n{existing_str}\n\nWeb search results for '{cat_name}':\n{web_data}\n\nPick 1 real project from these results."},
        ]
        try:
            raw = api_chat(messages)
            for line in raw.split("\n"):
                m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
                if m:
                    title = clean_title(m.group(1))
                    desc = m.group(2).strip() if m.group(2) else ""
                    if not topic_exists(slugify(title)):
                        return {"title": f"Analyze {title} project", "desc": desc, "kind": "project"}
        except Exception as e:
            log(f"Project discovery '{cat_name}' failed: {e}")
    return None

ARTICLE_SEARCHES = [
    ("software architecture patterns", "software architecture patterns microservices event driven CQRS clean architecture"),
    ("design patterns", "software design patterns explained Singleton Factory Observer Strategy"),
    ("system design", "system design concepts load balancing caching database sharding CAP theorem"),
    ("performance optimization", "web performance optimization techniques lazy loading code splitting caching"),
    ("security best practices", "web security best practices OAuth JWT authentication SQL injection prevention"),
    ("DevOps practices", "DevOps practices GitOps immutable infrastructure CI CD blue green deployment"),
    ("testing strategies", "software testing strategies unit testing integration testing TDD"),
    ("API design", "API design best practices REST GraphQL API versioning WebSocket gRPC"),
]

def discover_one_concept():
    existing = set()
    for f in (WORKSPACE / "docs" / "concepts").rglob("*.md"):
        existing.add(f.stem)
    existing_lower = [t.lower() for t in existing]

    for cat_name, search_query in ARTICLE_SEARCHES:
        web_data = web_search_deep(search_query)
        if not web_data:
            continue
        existing_str = "\n".join(f"- {t}" for t in existing) if existing else "None yet."
        messages = [
            {"role": "system", "content": "You are a content curator reading web search results. Pick ONE technical concept topic from the results that is NOT already documented. Output exactly:\n- **Concept Title.** One-sentence description.\nONLY pick a real topic mentioned in the search results."},
            {"role": "user", "content": f"Already documented concepts:\n{existing_str}\n\nWeb search results for '{cat_name}':\n{web_data}\n\nPick 1 real concept from these results."},
        ]
        try:
            raw = api_chat(messages)
            for line in raw.split("\n"):
                m = re.match(r"-\s+\*\*(.+?)\*\*[.:]?\s*(.*)", line)
                if m:
                    title = clean_title(m.group(1))
                    desc = m.group(2).strip() if m.group(2) else ""
                    if slugify(title) not in existing_lower and not topic_exists(slugify(title)):
                        return {"title": title, "desc": desc, "kind": "concept"}
        except Exception as e:
            log(f"Concept discovery '{cat_name}' failed: {e}")
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
    kind = task.get("kind", "tool")
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
    elif kind == "concept":
        parts += ["", "Write a developer guide on this concept. Cover: what it is, why it matters, how it works with real code examples, trade-offs, and best practices. Include diagrams in ASCII if helpful."]
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
    kind = task.get("kind", "tool")
    slug = slugify(task["title"])
    created = []

    if kind == "project":
        base = WORKSPACE / "projects" / slug
        base.mkdir(parents=True, exist_ok=True)
        en_path = base / "index.en.md"
        en_path.write_text(content, encoding="utf-8")
        created.append(en_path)
        readme = base / "README.md"
        if not readme.exists():
            readme.write_text(f"# {task['title']}\n\n{task['desc']}\n", encoding="utf-8")
            created.append(readme)
    elif kind == "snippet":
        base = WORKSPACE / "snippets" / slug
        base.mkdir(parents=True, exist_ok=True)
        en_path = base / "index.en.md"
        en_path.write_text(content, encoding="utf-8")
        created.append(en_path)
    elif kind == "tool":
        base = WORKSPACE / "docs" / "tools" / slug
        base.mkdir(parents=True, exist_ok=True)
        en_path = base / "index.en.md"
        en_path.write_text(content, encoding="utf-8")
        created.append(en_path)
    else:
        en_path = WORKSPACE / "docs" / f"{slug}.en.md"
        en_path.write_text(content, encoding="utf-8")
        created.append(en_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}
        for locale, native, english_name in LANGUAGES:
            if kind in ("project", "snippet", "tool"):
                tx_path = base / f"index.{locale}.md"
            else:
                tx_path = WORKSPACE / "docs" / f"{slug}.{locale}.md"
            future = executor.submit(translate_content, content, english_name)
            futures[future] = tx_path
        for future in concurrent.futures.as_completed(futures):
            tx_path = futures[future]
            try:
                translated = future.result()
                tx_path.write_text(translated, encoding="utf-8")
                created.append(tx_path)
                log(f"Translated to {locale}")
            except Exception as e:
                log(f"Translation failed for {tx_path}: {e}")
    return created

def write_report(task, files):
    slug = slugify(task["title"])
    year, month, _ = TODAY.split("-")
    rdir = WORKSPACE / "docs" / "reports" / year / month
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
        f"**Agent:** WikiCode autonomous (Qwen3.6-27B local)",
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
    report_rel = os.path.relpath(report, cpath.parent)
    slug = slugify(task["title"])
    if cpath.exists():
        content = cpath.read_text(encoding="utf-8")
        if slug in content.lower():
            log(f"Task already in completed list: {task['title']}")
            return
        row = f"| {TODAY} | {task['title']} | [{task['title']}]({report_rel}) |\n"
        content = content.rstrip() + "\n" + row
        cpath.write_text(content, encoding="utf-8")

def post_comment(issue_number, comment):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        log("Cannot post comment: missing GITHUB_TOKEN or GITHUB_REPO")
        return
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}/comments"
    try:
        resp = httpx.post(url, headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
        }, json={"body": comment}, timeout=30)
        resp.raise_for_status()
        log(f"Posted comment on issue #{issue_number}")
    except Exception as e:
        log(f"Failed to post comment: {e}")

def add_label(issue_number, label):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        return
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}/labels"
    try:
        resp = httpx.post(url, headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
        }, json={"labels": [label]}, timeout=30)
        resp.raise_for_status()
        log(f"Added label '{label}' to issue #{issue_number}")
    except Exception as e:
        log(f"Failed to add label: {e}")

def close_issue(issue_number):
    if not GITHUB_TOKEN or not GITHUB_REPO:
        log("Cannot close issue: missing GITHUB_TOKEN or GITHUB_REPO")
        return
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues/{issue_number}"
    try:
        resp = httpx.patch(url, headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
        }, json={"state": "closed"}, timeout=30)
        resp.raise_for_status()
        log(f"Closed issue #{issue_number}")
    except Exception as e:
        log(f"Failed to close issue: {e}")

def analyze_request(title, body):
    text = f"Title: {title}\n\nDescription: {body}"[:2000]
    messages = [
        {"role": "system", "content": (
            "You are a gatekeeper for a developer wiki. Analyze the following issue request.\n"
            "Decide if this is a legitimate request to document a real developer tool, concept, or project.\n"
            "REJECT if:\n"
            "- The request is spam, gibberish, or nonsensical\n"
            "- The topic doesn't exist or is made up\n"
            "- The request is inappropriate, offensive, or malicious\n"
            "- The request is a bug report or support question, not a documentation request\n"
            "- The topic is not developer/tech related\n\n"
            "If VALID, extract:\n"
            "- The real topic name/title to document\n"
            "- A short description\n"
            "- Kind: 'tool', 'concept', or 'project'\n\n"
            "Output JSON only, no markdown:\n"
            '{"valid": true/false, "title": "...", "description": "...", "kind": "tool|concept|project", "reason": "why rejected if invalid"}'
        )},
        {"role": "user", "content": text},
    ]
    try:
        raw = api_chat(messages)
        raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        result = json.loads(raw)
        if not isinstance(result, dict):
            return {"valid": False, "reason": "Invalid analysis response format.", "title": title}
        if result.get("valid") and result.get("kind") not in ("tool", "concept", "project"):
            result["valid"] = False
            result["reason"] = "Could not classify request type."
        if result.get("valid"):
            result.setdefault("title", title)
            result.setdefault("description", "")
            result.setdefault("kind", "tool")
        return result
    except Exception as e:
        log(f"Request analysis failed: {e}")
        return {"valid": False, "reason": f"Analysis error: {e}", "title": title}

def validate():
    log("Running mkdocs build validation...")
    result = subprocess.run(["mkdocs", "build", "--clean"], cwd=WORKSPACE, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        log(f"Build FAILED:\n{result.stderr[:2000]}")
        return False
    log("Build passed.")
    return True

def write_state(task, report):
    path = WORKSPACE / "memory" / "state.md"
    content = f"""---
title: Agent State
description: Current state and context of the WikiCode agent.
created: 2026-06-15
---
# Agent State

Last execution state. Updated by the agent after each run.

```yaml
last_run: {TODAY}
last_task: {task['title']}
last_result: completed
current_focus: tools
queue_empty: true
```

This file is read by the agent at startup and updated after each
execution to maintain continuity across runs.
"""
    path.write_text(content, encoding="utf-8")

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
