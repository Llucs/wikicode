---
title: Agent State
description: Current state and context of the WikiCode agent.
created: 2026-06-15
---
# Agent State

Last execution state. Updated by the agent after each run.

```yaml
last_run: null
last_task: null
last_result: null
current_focus: tools
queue_empty: true
```

This file is read by the agent at startup and updated after each
execution to maintain continuity across runs.
