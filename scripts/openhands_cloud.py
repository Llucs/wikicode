#!/usr/bin/env python3
"""Start an OpenHands Cloud conversation via the REST API and return.

This script is designed to be **fire-and-forget**. It authenticates against
the OpenHands Cloud, creates a new conversation, prints the conversation
URL, and exits. It does NOT wait for the agent to finish.

Why fire-and-forget? The OpenHands Cloud agent runs on All-Hands Dev
infrastructure (its own VM/container), not inside the GitHub Actions
runner. A single agent task can take 20-40 minutes. If we block the CI
job for the whole duration we hit the 45-min workflow timeout and
waste runner minutes on pure polling.

Instead, the workflow dispatches the agent, exits, and the agent works
asynchronously. When the agent finishes and pushes commits to `main`,
the `.github/workflows/pages.yml` workflow (triggered by `push: main`)
rebuilds and deploys the site automatically.
"""
import asyncio
import json
import os
import subprocess
import sys

import httpx


SERVER_URL = os.environ.get("OPENHANDS_CLOUD_URL", "https://app.all-hands.dev")
API_KEY = os.environ["OPENHANDS_API_KEY"]
TASK_FILE = os.environ.get("OPENHANDS_TASK_FILE", "/tmp/task.md")
REPO = os.environ.get("WIKICODE_REPO", "Llucs/wikicode")
BRANCH = os.environ.get("WIKICODE_BRANCH", "main")


def detect_repo_from_git() -> str | None:
    try:
        url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"], text=True
        ).strip()
    except Exception:
        return None
    if url.startswith("git@"):
        return url.split(":", 1)[1].removesuffix(".git") or None
    if url.startswith("https://"):
        parts = [p for p in url.split("/") if p]
        if len(parts) >= 2:
            return f"{parts[-2]}/{parts[-1].removesuffix('.git')}"
    return None


def detect_branch_from_git() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True
        ).strip()
    except Exception:
        return None


async def main() -> int:
    with open(TASK_FILE) as f:
        task_text = f.read()

    # Append push instructions if a push token is provided, so the cloud
    # agent can bypass its own read-only GITHUB_TOKEN.
    push_token = os.environ.get("OPENHANDS_PUSH_TOKEN", "").strip()
    if push_token:
        push_block = (
            "\n\n---\n\n"
            "IMPORTANT — How to push your changes AND trigger the site deploy:\n\n"
            "The OpenHands Cloud environment's default GITHUB_TOKEN is "
            "read-only and cannot push to this repository. To commit and "
            "push, use the token below (it has `contents: write`):\n\n"
            "```bash\n"
            "git remote set-url origin "
            f"https://x-access-token:{push_token}@github.com/{REPO}.git\n"
            "git config user.name 'wikicode-bot'\n"
            "git config user.email 'wikicode-bot@users.noreply.github.com'\n"
            "git add -A\n"
            "git commit -m 'OpenHands: <short description>'\n"
            f"git push origin {BRANCH}\n"
            "```\n\n"
            "AFTER the push succeeds, you MUST wake up the Pages deploy. "
            "Pushes made with a GITHUB_TOKEN do NOT trigger workflows on "
            "their own, so the site would not rebuild. Call the repository "
            "dispatch API to fire a custom `agent-pushed` event (the Pages "
            "workflow listens for it):\n\n"
            "```bash\n"
            "curl -fsS -X POST \\\n"
            "  -H 'Accept: application/vnd.github+json' \\\n"
            "  -H 'Authorization: Bearer " + push_token + "' \\\n"
            f"  https://api.github.com/repos/{REPO}/dispatches \\\n"
            "  -d '{\"event_type\":\"agent-pushed\"}'\n"
            "```\n\n"
            "Both steps are required. Do not skip the dispatch call.\n\n"
            "Do NOT echo or log the token in your output. Do NOT commit it. "
            "Use it only for the push and dispatch above, then forget it. "
            "The token is ephemeral and dies with this workflow run.\n"
        )
        task_text = task_text + push_block
        print("Push instructions appended to task (token hidden in prompt).")
    else:
        print("No OPENHANDS_PUSH_TOKEN set; agent will try its own GITHUB_TOKEN.")

    repo = detect_repo_from_git() or REPO
    branch = detect_branch_from_git() or BRANCH
    print(f"Repository: {repo}")
    print(f"Branch: {branch}")
    print(f"Task length: {len(task_text)} chars")

    payload = {
        "initial_message": {
            "content": [{"type": "text", "text": task_text}],
        },
        "selected_repository": repo,
        "selected_branch": branch,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(base_url=SERVER_URL, headers=headers) as client:
        # Verify auth
        me = await client.get("/api/v1/users/me", timeout=30)
        if me.status_code == 401:
            print("ERROR: API key rejected (401). Invalid or expired.",
                  file=sys.stderr)
            return 2
        me.raise_for_status()
        me_data = me.json()
        print(f"Authenticated as: {me_data.get('email') or me_data.get('login') or me_data}")

        # Create the conversation (fire-and-forget)
        resp = await client.post(
            "/api/v1/app-conversations",
            json=payload,
            timeout=30,
        )
        if resp.status_code >= 400:
            print(f"Create conversation failed: {resp.status_code} {resp.text}",
                  file=sys.stderr)
            return 3
        conv = resp.json()
        task_id = conv.get("id")
        app_conv_id = conv.get("app_conversation_id")
        view_id = app_conv_id or task_id
        print("Conversation created successfully.")
        print(f"  task_id           = {task_id}")
        print(f"  app_conversation_id = {app_conv_id}")
        print(f"  view              = {SERVER_URL}/conversations/{view_id}")
        print()
        print("Agent will now run asynchronously on OpenHands Cloud.")
        print("This CI job is done; the agent will push to main when finished,")
        print("and .github/workflows/pages.yml will deploy the site automatically.")
        return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
