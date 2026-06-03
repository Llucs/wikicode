#!/usr/bin/env python3
"""Drive an OpenHands Cloud conversation directly via the REST API.

Bypasses the openhands CLI's interactive OAuth login by using the
OPENHANDS_API_KEY against the cloud REST API directly.
"""
import asyncio
import json
import os
import subprocess
import sys
import time
from urllib.parse import urlparse

import httpx


SERVER_URL = os.environ.get("OPENHANDS_CLOUD_URL", "https://app.all-hands.dev")
API_KEY = os.environ["OPENHANDS_API_KEY"]
TASK_FILE = os.environ.get("OPENHANDS_TASK_FILE", "/tmp/task.md")
REPO = os.environ.get("WIKICODE_REPO", "Llucs/wikicode")
BRANCH = os.environ.get("WIKICODE_BRANCH", "main")
POLL_INTERVAL = float(os.environ.get("OPENHANDS_POLL_INTERVAL", "10"))
POLL_TIMEOUT = int(os.environ.get("OPENHANDS_POLL_TIMEOUT", "1500"))  # 25 min


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


async def create_conversation(client: httpx.AsyncClient, payload: dict) -> dict:
    resp = await client.post(
        "/api/v1/app-conversations",
        json=payload,
        timeout=30,
    )
    if resp.status_code >= 400:
        print(f"create_conversation failed: {resp.status_code} {resp.text}",
              file=sys.stderr)
        resp.raise_for_status()
    return resp.json()


async def get_start_task(client: httpx.AsyncClient, task_id: str) -> dict:
    resp = await client.get(
        f"/api/v1/app-conversations/start-task/{task_id}",
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


async def get_conversation_status(client: httpx.AsyncClient, conv_id: str) -> dict:
    resp = await client.get(
        f"/api/v1/app-conversations/{conv_id}",
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


async def main() -> int:
    with open(TASK_FILE) as f:
        task_text = f.read()

    # If a push token is provided, append explicit push instructions
    # so the cloud agent can bypass its own read-only GITHUB_TOKEN.
    push_token = os.environ.get("OPENHANDS_PUSH_TOKEN", "").strip()
    if push_token:
        push_block = (
            "\n\n---\n\n"
            "IMPORTANT — How to push your changes:\n\n"
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
            "Do NOT echo or log the token. Do NOT commit it. Use it only "
            "for the single push above, then forget it. The token is "
            "ephemeral and dies with this workflow run.\n"
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
        # Verify auth first
        me = await client.get("/api/v1/users/me", timeout=30)
        if me.status_code == 401:
            print("ERROR: API key rejected (401). The key is invalid or expired.",
                  file=sys.stderr)
            return 2
        me.raise_for_status()
        me_data = me.json()
        print(f"Authenticated as: {me_data.get('email') or me_data.get('login') or me_data}")

        # Create the conversation
        conv = await create_conversation(client, payload)
        task_id = conv.get("id")
        app_conv_id = conv.get("app_conversation_id")
        print(f"Created conversation. task_id={task_id} app_conversation_id={app_conv_id}")
        print(f"View: {SERVER_URL}/conversations/{app_conv_id or task_id}")

        # Poll the start-task until app_conversation_id is available
        deadline = time.time() + POLL_TIMEOUT
        while not app_conv_id and task_id and time.time() < deadline:
            await asyncio.sleep(POLL_INTERVAL)
            try:
                task_info = await get_start_task(client, task_id)
            except Exception as e:
                print(f"poll start-task error: {e}")
                continue
            status = task_info.get("status")
            app_conv_id = task_info.get("app_conversation_id")
            print(f"  start-task status={status} app_conversation_id={app_conv_id}")
            if status == "ERROR":
                print(f"Conversation failed: {task_info.get('detail')}",
                      file=sys.stderr)
                return 3

        conv_id = app_conv_id or task_id
        if not conv_id:
            print("ERROR: no conversation id returned", file=sys.stderr)
            return 4

        # Poll the conversation itself until it stops
        print("Waiting for agent to finish...")
        last_status = None
        while time.time() < deadline:
            await asyncio.sleep(POLL_INTERVAL)
            try:
                info = await get_conversation_status(client, conv_id)
            except Exception as e:
                print(f"poll conversation error: {e}")
                continue
            status = info.get("status") or info.get("state")
            if status != last_status:
                print(f"  conversation status={status}")
                last_status = status
            if status in ("STOPPED", "COMPLETED", "FINISHED", "ERROR", "FAILED"):
                print(f"Agent finished with status={status}")
                print(f"Full response: {json.dumps(info, indent=2)[:2000]}")
                return 0 if status not in ("ERROR", "FAILED") else 5

        print("ERROR: timed out waiting for agent", file=sys.stderr)
        return 6


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
