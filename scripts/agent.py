#!/usr/bin/env python3
"""Wikicode autonomous agent — runs entirely on GitHub Actions via Ollama.

No external API keys required. The agent:
  1. Reads memory/ for mission context.
  2. Picks the first pending task from tasks/queue.md.
  3. Researches the topic (web search via DuckDuckGo).
  4. Generates content using a local LLM (Ollama).
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
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:3b")
WORKSPACE = Path(os.environ.get("GITHUB_WORKSPACE", os.getcwd()))
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPOSITORY", "")


def log(msg: str) -> None:
    print(f"[agent] {msg}", flush=True)


def git(*args: str) -> str:
    return subprocess.check_output(["git"] + list(args), cwd=WORKSPACE, text=True).strip()


def ollama_generate(prompt: str, system: str = "", max_retries: int = 3) -> str:
    for attempt in range(1, max_retries + 1):
        try:
            resp = httpx.post(
                f"{OLLAMA_BASE}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "system": system,
                    "stream": False,
                    "options": {"temperature": 0.3, "num_predict": 4096},
                },
                timeout=600,
            )
            resp.raise_for_status()
            return resp.json()["response"].strip()
        except Exception as e:
            log(f"Ollama attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                time.sleep(5)
    raise RuntimeError(f"Ollama query failed after {max_retries} attempts")


def web_search(query: str, max_results: int = 5) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    try:
        resp = httpx.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=15,
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Abstract", "") or query,
                    "body": data.get("AbstractText", ""),
                    "source": data.get("AbstractSource", ""),
                    "url": data.get("AbstractURL", ""),
                })
            for topic in data.get("RelatedTopics", [])[:max_results]:
                if "Text" in topic:
                    results.append({
                        "title": topic.get("Text", "").split(" - ")[0],
                        "body": topic.get("Text", ""),
                        "source": "",
                        "url": topic.get("FirstURL", ""),
                    })
        if not results:
            log("DuckDuckGo returned no results, trying Wikipedia...")
            wiki_resp = httpx.get(
                "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_"),
                timeout=15,
            )
            if wiki_resp.status_code == 200:
                wd = wiki_resp.json()
                results.append({
                    "title": wd.get("title", query),
                    "body": wd.get("extract", ""),
                    "source": "Wikipedia",
                    "url": wd.get("content_urls", {}).get("desktop", {}).get("page", ""),
                })
    except Exception as e:
        log(f"Web search error: {e}")
    return results


def read_dir(path: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    if path.exists():
        for f in sorted(path.glob("*.md")):
            files[f.stem] = f.read_text(encoding="utf-8")
    return files


def slugify(text: str) -> str:
    s = text.lower().replace(" ", "-")
    s = re.sub(r"[^a-z0-9\u00e0-\u00ff-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "untitled"


def anti_duplicate_check(task: dict) -> bool:
    slug = slugify(task["title"])
    sections = [
        WORKSPACE / "docs",
        WORKSPACE / "projects",
        WORKSPACE / "snippets",
    ]
    for section in sections:
        if not section.exists():
            continue
        result = subprocess.run(
            ["git", "grep", "-l", "-i", slug, "--", str(section)],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.stdout.strip():
            idx = result.stdout.strip().split("\n")[0]
            log(f"Duplicate detected: {slug} found in {idx}")
            return False
    return True


def parse_queue() -> tuple[list[dict[str, str]], str]:
    path = WORKSPACE / "tasks" / "queue.md"
    if not path.exists():
        return [], ""
    content = path.read_text(encoding="utf-8")
    tasks: list[dict[str, str]] = []
    for line in content.split("\n"):
        m = re.match(r"-\s+\[\s*\]\s+\*\*(.+?)\*\*\s*(.*)", line)
        if m:
            tasks.append({"title": m.group(1).strip(), "desc": m.group(2).strip(), "line": line})
    return tasks, content


def generate_content(task: dict, research: list[dict], memory: dict) -> str:
    mission = memory.get("mission", "")
    rules = memory.get("rules", "")

    research_blob = ""
    if research:
        research_blob = "\n\n## Web research\n" + "\n".join(
            f"- {r['title']}: {r['body'][:800]}" for r in research[:3]
        )

    system = (
        "You are WikiCode Agent. You produce clean, well-structured Markdown "
        "for a developer wiki. Every file MUST start with YAML frontmatter:\n"
        "---\ntitle: <Title>\ndescription: <Short description>\n"
        "created: <YYYY-MM-DD>\ntags:\n  - <tag>\nstatus: draft\n---\n\n"
        "After the frontmatter, write the content using standard Markdown. "
        "Output ONLY the file content — no chat, no explanation, no code fences."
    )

    user = (
        f"Task: {task['title']}\n"
        f"Description: {task['desc']}\n"
        f"{research_blob}\n\n"
        f"Mission:\n{mission[:1500]}\n\n"
        f"Rules:\n{rules[:1500]}\n\n"
        f"Write the complete Markdown file with frontmatter. "
        f"Today is {date.today().isoformat()}. Be specific, useful, and real."
    )

    log(f"Generating content for: {task['title']}")
    return ollama_generate(user, system)


def write_files(task: dict, content: str) -> list[Path]:
    created: list[Path] = []
    title = task["title"].lower()
    slug = slugify(task["title"])

    if "project" in title:
        base = WORKSPACE / "projects" / slug
        base.mkdir(parents=True, exist_ok=True)
        f = base / "index.md"
        f.write_text(content, encoding="utf-8")
        created.append(f)
        readme = base / "README.md"
        if not readme.exists():
            readme.write_text(f"# {task['title']}\n\n{task['desc']}\n", encoding="utf-8")
            created.append(readme)
    elif "snippet" in title:
        base = WORKSPACE / "snippets" / slug
        base.mkdir(parents=True, exist_ok=True)
        f = base / "index.md"
        f.write_text(content, encoding="utf-8")
        created.append(f)
    elif "tool" in title:
        base = WORKSPACE / "docs" / "tools" / slug
        base.mkdir(parents=True, exist_ok=True)
        f = base / "index.md"
        f.write_text(content, encoding="utf-8")
        created.append(f)
    else:
        f = WORKSPACE / "docs" / f"{slug}.md"
        f.write_text(content, encoding="utf-8")
        created.append(f)

    return created


def write_report(task: dict, files: list[Path]) -> Path:
    today = date.today().isoformat()
    slug = slugify(task["title"])
    path = WORKSPACE / "docs" / "reports" / f"{today}-{slug}.md"

    lines = [
        "---",
        f'title: "{task["title"]}"',
        'description: "Agent execution report"',
        f"created: {today}",
        "tags:",
        "  - agent",
        "status: completed",
        "---",
        "",
        f"# Report: {task['title']}",
        "",
        f"**Date:** {today}",
        "**Agent:** WikiCode autonomous (local Ollama)",
        "",
        "## Summary",
        "",
        f"Executed task: **{task['title']}**",
        "",
        "### Files created / modified",
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
        lines = qpath.read_text(encoding="utf-8").split("\n")
        filtered = [l for l in lines if task["line"] not in l]
        qpath.write_text("\n".join(filtered), encoding="utf-8")

    today = date.today().isoformat()
    row = f"| {today} | {task['title']} | [{task['title']}]({report.relative_to(WORKSPACE)}) |\n"

    if cpath.exists():
        content = cpath.read_text(encoding="utf-8")
        if "| ---" in content:
            content = content.rstrip() + "\n" + row
        else:
            content += "\n" + row
        cpath.write_text(content, encoding="utf-8")


def validate() -> bool:
    log("Validating with mkdocs build...")
    result = subprocess.run(
        ["mkdocs", "build", "--clean"],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        log(f"MkDocs build FAILED:\n{result.stderr[:2000]}")
        return False
    log("MkDocs build passed.")
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
        push_url = f"https://x-access-token:{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"
        git("remote", "set-url", "origin", push_url)

    git("push", "origin", "HEAD")
    log("Pushed to origin.")


def main() -> int:
    log(f"Starting — model={MODEL}, workspace={WORKSPACE}")

    memory = read_dir(WORKSPACE / "memory")
    log(f"Read {len(memory)} memory files")

    tasks, _ = parse_queue()
    log(f"Pending tasks: {len(tasks)}")

    if not tasks:
        log("Queue empty — nothing to do.")
        return 0

    task = tasks[0]
    log(f"Selected task [{task['title']}]")

    if not anti_duplicate_check(task):
        log("Topic appears to already exist — skipping and marking done.")
        report = write_report(task, [])
        update_task_lists(task, report)
        commit_and_push([], task)
        return 0

    research = web_search(task["title"])
    log(f"Web results: {len(research)}")

    content = generate_content(task, research, memory)
    log(f"Generated {len(content)} chars")

    if not content:
        log("No content generated — aborting.")
        return 1

    files = write_files(task, content)
    log(f"Wrote {len(files)} file(s)")

    report = write_report(task, files)
    log(f"Report: {report.relative_to(WORKSPACE)}")

    update_task_lists(task, report)
    log("Task lists updated")

    if not validate():
        log("Validation failed — reverting changes.")
        git("checkout", ".")
        return 1

    commit_and_push(files, task)
    log("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
