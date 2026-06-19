#!/usr/bin/env python3
"""WikiCode Agent — entry point.

FOCUS=tools   → discover/document developer tools
FOCUS=content → discover/document concepts, articles, projects, snippets
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib import (
    WORKSPACE, GITHUB_TOKEN, GITHUB_REPO, TODAY,
    log, git, read_memory, parse_queue, enrich_task,
    discover_one_tool, discover_one_project, discover_one_concept,
    add_task_to_queue, research_topic, generate_content,
    write_files, write_report, update_task_lists, write_state,
    validate, commit_and_push, post_comment, add_label, classify_request,
)

FOCUS = os.environ.get("FOCUS", "tools").lower()

def get_next_task():
    tasks, _ = parse_queue()
    if not tasks:
        log(f"Queue empty. Discovering from focus={FOCUS}...")
        if FOCUS == "content":
            item = discover_one_concept()
            if not item:
                item = discover_one_project()
            if not item:
                item = discover_one_tool()
        else:
            item = discover_one_tool()
            if not item:
                item = discover_one_project()
            if not item:
                item = discover_one_concept()
        if item:
            add_task_to_queue(item["title"], item["desc"])
            tasks, _ = parse_queue()
    return tasks[0] if tasks else None

def execute_pipeline(task):
    log(f"Processing: {task['title']}")
    memory = read_memory()
    research = research_topic(task["title"], FOCUS)
    content = generate_content(task, research, memory)
    if not content:
        log("No content generated.")
        return False

    files = write_files(task, content)
    report = write_report(task, files)
    update_task_lists(task, report)

    if not validate():
        git("checkout", "--", ".")
        git("clean", "-fd")
        log("Build failed - reverted all changes.")
        return False

    commit_and_push(files, task)
    write_state(task, report)
    return True

def handle_issue_event():
    issue_number = os.environ.get("ISSUE_NUMBER", "").strip()
    issue_title = os.environ.get("ISSUE_TITLE", "").strip()
    issue_body = os.environ.get("ISSUE_BODY", "").strip()
    comment_body = os.environ.get("COMMENT_BODY", "").strip()

    if not issue_number:
        log("No issue number found in event payload.")
        return

    log(f"Processing issue #{issue_number}: {issue_title}")
    post_comment(issue_number, f"Thanks! I'll process this request: **{issue_title}**")
    add_label(issue_number, "agent")

    task_title = issue_title or "Untitled request"
    task_desc = issue_body if issue_body else comment_body if comment_body else ""
    kind = classify_request(task_title + " " + task_desc)
    task = {"title": task_title, "desc": task_desc[:500], "kind": kind}

    git("pull", "--rebase", "origin", "main")

    task = enrich_task(task)
    ok = execute_pipeline(task)

    if ok:
        post_comment(issue_number, f"Done! I've documented **{task['title']}** and pushed it to the wiki.")
        log(f"Issue #{issue_number} completed successfully.")
    else:
        post_comment(issue_number, f"Sorry, I couldn't complete the request for **{task['title']}**. Check the workflow logs for details.")
        log(f"Issue #{issue_number} failed.")

def run():
    log(f"Starting (focus={FOCUS})")

    event_name = os.environ.get("EVENT_NAME", "")
    if event_name in ("issue_comment", "issues"):
        handle_issue_event()
        return

    git("pull", "--rebase", "origin", "main")

    task = get_next_task()
    if not task:
        log("No new tasks discovered. Done.")
        return

    task = enrich_task(task)
    execute_pipeline(task)
    log("Done.")

if __name__ == "__main__":
    run()
