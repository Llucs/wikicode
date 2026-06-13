#!/usr/bin/env python3
"""WikiCode autonomous agent — runs entirely on GitHub Actions via Ollama.

No external API keys required. The agent:
  1. Reads memory/ for mission context.
  2. Picks the first pending task from tasks/queue.md.
  3. Researches the topic on the web (DuckDuckGo/Wikipedia).
  4. Generates high-quality developer content using a local LLM.
  5. Writes files, validates with mkdocs, and commits.
"""

import os
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

import httpx

OLLAMA_BASE = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
WORKSPACE = Path(os.environ.get("GITHUB_WORKSPACE", os.getcwd()))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "")
TODAY = date.today().isoformat()


def log(msg: str) -> None:
    print(f"[agent] {msg}", flush=True)


def git(*args: str) -> str:
    return subprocess.check_output(["git"] + list(args), cwd=WORKSPACE, text=True).strip()


def ollama_ensure_running() -> bool:
    for i in range(10):
        try:
            r = httpx.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
            return True
        except Exception:
            log(f"Ollama not reachable, restarting... ({i+1})")
            subprocess.Popen(
                ["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            time.sleep(3)
    return False


def ollama(prompt: str, system: str = "", max_retries: int = 3) -> str:
    for attempt in range(1, max_retries + 1):
        try:
            if not ollama_ensure_running():
                raise RuntimeError("Ollama not running")
            resp = httpx.post(
                f"{OLLAMA_BASE}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "system": system,
                    "stream": False,
                    "options": {"temperature": 0.4, "num_predict": 8192},
                },
                timeout=600,
            )
            if resp.status_code == 500:
                detail = resp.text[:500]
                log(f"Ollama 500: {detail}")
                if "not found" in detail.lower():
                    log("Model not found, pulling...")
                    subprocess.run(["ollama", "pull", MODEL], timeout=300)
                time.sleep(5)
                continue
            resp.raise_for_status()
            return resp.json()["response"].strip()
        except Exception as e:
            log(f"Ollama attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                time.sleep(10)
    raise RuntimeError(f"Ollama query failed after {max_retries} attempts")


def web_search(query: str) -> str:
    results = []
    try:
        resp = httpx.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("AbstractText"):
                results.append(f"- {data['AbstractSource']}: {data['AbstractText'][:1000]}")
            for topic in data.get("RelatedTopics", [])[:5]:
                if "Text" in topic:
                    results.append(f"- {topic['Text'][:500]}")
    except Exception as e:
        log(f"DuckDuckGo error: {e}")

    if not results:
        try:
            resp = httpx.get(
                "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_"),
                timeout=15,
            )
            if resp.status_code == 200:
                wd = resp.json()
                results.append(f"- Wikipedia: {wd.get('extract', '')[:1500]}")
        except Exception as e:
            log(f"Wikipedia error: {e}")

    return "\n".join(results)


def slugify(text: str) -> str:
    s = text.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\u00e0-\u00ff-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "untitled"


def read_memory() -> dict[str, str]:
    files = {}
    path = WORKSPACE / "memory"
    if path.exists():
        for f in sorted(path.glob("*.md")):
            files[f.stem] = f.read_text(encoding="utf-8")
    return files


def parse_queue() -> tuple[list[dict[str, str]], str]:
    path = WORKSPACE / "tasks" / "queue.md"
    if not path.exists():
        return [], ""
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    tasks: list[dict[str, str]] = []
    in_task = False
    current: dict | None = None
    task_block_start = 0
    for i, line in enumerate(lines):
        m = re.match(r"(-\s+\[\s*\]\s+\*\*(.+?)\*\*\s*(.*))", line)
        if m:
            if current:
                current["block"] = "\n".join(lines[task_block_start:i])
                tasks.append(current)
            current = {
                "title": m.group(2).strip(),
                "desc": m.group(3).strip(),
                "block": "",
                "start": task_block_start,
            }
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


def anti_duplicate(task: dict) -> bool:
    slug = slugify(task["title"])
    for section in [WORKSPACE / "docs", WORKSPACE / "projects", WORKSPACE / "snippets"]:
        if not section.exists():
            continue
        result = subprocess.run(
            ["git", "grep", "-l", "-i", slug, "--", str(section)],
            capture_output=True, text=True, timeout=30, cwd=WORKSPACE,
        )
        if result.stdout.strip():
            log(f"Duplicate found in {result.stdout.strip().split(chr(10))[0]}")
            return False
    return True


def classify_task(task: dict) -> str:
    """Determine the type of content to generate."""
    title = task["title"].lower()
    desc = task["desc"].lower()
    combined = title + " " + desc
    if "project" in combined:
        return "project"
    if "snippet" in combined:
        return "snippet"
    if "tool" in combined or "technology" in combined or "framework" in combined:
        return "tool"
    if "guide" in combined or "article" in combined or "tutorial" in combined:
        return "article"
    return "article"


def generate_content(task: dict, research: str, memory: dict) -> str:
    kind = classify_task(task)

    system = (
        "You are WikiCode Agent. You produce a high-quality developer wiki. "
        "You write REAL, USEFUL, SUBSTANTIVE content for professional developers.\n\n"
        "RULES:\n"
        "1. Output ONLY one complete Markdown file per message.\n"
        "2. Start with YAML frontmatter:\n"
        "   ---\n"
        "   title: <Exact descriptive title>\n"
        "   description: <One sentence summary>\n"
        "   created: <YYYY-MM-DD>\n"
        "   tags:\n"
        "     - <tag1>\n"
        "     - <tag2>\n"
        "   status: draft\n"
        "   ---\n"
        "3. After frontmatter, write the content with Markdown headings.\n"
        "4. Include REAL code blocks with proper syntax highlighting.\n"
        "5. Do NOT include mission/rules/knowledge text in the output.\n"
        "6. Do NOT include chat, commentary, or explanation outside the file.\n"
        "7. Do NOT wrap the output in code fences (```).\n"
    )

    if kind == "project":
        system += (
            "\nPROJECT GENERATION:\n"
            "Generate an index.md for a runnable developer project.\n"
            "- Pick a real technology (Go Gin API, Rust CLI, Python FastAPI, etc.)\n"
            "- Include actual code blocks (handlers, models, tests)\n"
            "- Document architecture, endpoints, setup, and usage\n"
            "- The project folder already exists; write ONLY index.md\n"
            "- index.md must be a complete MkDocs page for the wiki\n"
            "- Do NOT reference memory/, tasks/, or internal repo paths\n"
        )
    elif kind == "snippet":
        system += (
            "\nSNIPPET GENERATION:\n"
            "Generate an index.md for a practical code snippet.\n"
            "- Pick a real problem (JSON parsing, HTTP requests, file I/O)\n"
            "- Include the code with explanation\n"
            "- Make it copy-paste-ready with example usage\n"
        )
    elif kind == "tool":
        system += (
            "\nTOOL DOCUMENTATION:\n"
            "Generate an index.md documenting a real developer tool.\n"
            "- Use the web research for factual info\n"
            "- Cover: what, why, install, basic usage, key features\n"
            "- Include realistic command examples\n"
        )
    else:
        system += (
            "\nARTICLE GENERATION:\n"
            "Generate a Markdown article for a developer audience.\n"
            "- Pick a specific, non-trivial topic\n"
            "- Include code examples, trade-offs, best practices\n"
        )

    user = (
        f"Task: {task['title']}\n"
        f"Description: {task['desc']}\n"
        f"Today: {TODAY}\n\n"
        f"WikiCode is a developer wiki. The project goes under projects/<slug>/.\n"
    )
    if research:
        user += f"\nWeb research:\n{research}\n"
    user += "\nGenerate the complete Markdown file now."

    log(f"Generating {kind}: {task['title']}")
    return ollama(user, system)


def write_files(task: dict, content: str) -> list[Path]:
    kind = classify_task(task)
    slug = slugify(task["title"])
    created: list[Path] = []

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
        f = WORKSPACE / "docs" / f"{slug}.md"
        f.write_text(content, encoding="utf-8")
        created.append(f)

    return created


def write_report(task: dict, files: list[Path]) -> Path:
    slug = slugify(task["title"])
    path = WORKSPACE / "docs" / "reports" / f"{TODAY}-{slug}.md"
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
        "**Agent:** WikiCode autonomous (local Ollama)",
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


def update_task_lists(task: dict, report: Path) -> None:
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
        content = content.rstrip() + "\n" + row
        cpath.write_text(content, encoding="utf-8")


def validate() -> bool:
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


def commit_and_push(files: list[Path], task: dict) -> None:
    git("add", "-A")
    status = git("status", "--porcelain")
    if not status:
        log("No changes to commit.")
        return
    msg = f"wikicode: {slugify(task['title'])}"
    git("commit", "-m", msg)
    log(f"Committed: {msg}")
    if GITHUB_TOKEN and GITHUB_REPO:
        git("remote", "set-url", "origin",
            f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git")
    git("push", "origin", "HEAD")
    log("Pushed.")


def main() -> int:
    log(f"Starting — model={MODEL}")

    memory = read_memory()
    log(f"Read {len(memory)} memory files")

    tasks, _ = parse_queue()
    log(f"Pending: {len(tasks)}")

    if not tasks:
        log("Queue empty.")
        return 0

    task = tasks[0]
    log(f"Task: {task['title']}")

    if not anti_duplicate(task):
        log("Duplicate — skipping.")
        report = write_report(task, [])
        update_task_lists(task, report)
        commit_and_push([], task)
        return 0

    research = web_search(task["title"])
    log(f"Research: {len(research)} chars")

    content = generate_content(task, research, memory)
    if not content:
        log("No content — abort.")
        return 1
    log(f"Content: {len(content)} chars")

    files = write_files(task, content)
    log(f"Files: {len(files)}")

    report = write_report(task, files)
    update_task_lists(task, report)
    log("Task lists updated.")

    if not validate():
        log("Reverting.")
        git("checkout", ".")
        return 1

    commit_and_push(files, task)
    log("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
