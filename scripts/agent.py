#!/usr/bin/env python3
"""WikiCode Agent — entry point.

FOCUS=tools   → discover/document developer tools
FOCUS=content → discover/document articles, projects, snippets
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import (
    WORKSPACE, GITHUB_TOKEN, GITHUB_REPO, TODAY,
    log, git, read_memory, parse_queue, enrich_task,
    discover_one_tool, discover_one_project, discover_one_article,
    add_task_to_queue, research_topic, generate_content,
    write_files, write_report, update_task_lists, write_state,
    validate, commit_and_push,
)

FOCUS = os.environ.get("FOCUS", "tools").lower()

def get_next_task():
    tasks, _ = parse_queue()
    if not tasks:
        log(f"Queue empty. Discovering from focus={FOCUS}...")
        if FOCUS == "content":
            item = discover_one_project()
            if not item:
                item = discover_one_article()
            if not item:
                item = discover_one_tool()
        else:
            item = discover_one_tool()
            if not item:
                item = discover_one_project()
            if not item:
                item = discover_one_article()
        if item:
            add_task_to_queue(item["title"], item["desc"])
            tasks, _ = parse_queue()
    return tasks[0] if tasks else None

def run():
    log(f"Starting (focus={FOCUS})")
    git("pull", "--rebase", "origin", "main")

    task = get_next_task()
    if not task:
        log("No new tasks discovered. Done.")
        return

    task = enrich_task(task)
    log(f"Processing: {task['title']}")
    memory = read_memory()
    research = research_topic(task["title"], FOCUS)
    content = generate_content(task, research, memory)
    if not content:
        log("No content generated.")
        sys.exit(1)

    files = write_files(task, content)
    report = write_report(task, files)
    update_task_lists(task, report)

    if not validate():
        git("checkout", "--", ".")
        git("clean", "-fd")
        log("Build failed — reverted all changes.")
        sys.exit(1)

    commit_and_push(files, task)
    write_state(task, report)
    log("Done.")

if __name__ == "__main__":
    run()
