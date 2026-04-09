# CLAUDE.md

This repository uses Claude/Codex as an execution agent, not just a chat assistant.

## Project Identity

- Product:
- Users:
- Primary outcome:
- Current phase:

## Runbook

### Start

```bash
# fill in the real command
```

### Test

```bash
# fill in the real command
```

### Build / Package

```bash
# fill in the real command
```

## Architecture Boundaries

- Define the core modules and their ownership.
- State which runtime/database/message gateway choices are authoritative.
- State what is transitional compatibility only.
- State what must not be expanded further.

## Repository Workflow

Use issue-centered closed-loop delivery by default:

1. For non-trivial work, lock scope and verification before editing implementation files.
2. If the current workspace is risky or parallel work is expected, prefer an isolated worktree.
3. Read the issue and local repo rules first.
4. Create a dedicated branch.
5. Implement only the issue scope.
6. Run targeted verification before commit.
7. Push, open PR, merge, then sync local `master`.

## Definition Of Done

A task is not done when code is written. It is done only when:

- the change is implemented
- the relevant checks passed
- the affected runtime path was verified when applicable
- the branch/PR state is clean and understandable
- local `master` is synced after merge

## Rules

- Do not revert unrelated local changes.
- Do not widen scope silently.
- For non-trivial tasks, plan before implementation.
- Repeated gatekeeping checks with stable triggers should move into hooks or CI, not stay as ad hoc reminders.
- When one reusable capability spans multiple skills, hooks, MCP servers, or templates, define a capability-pack boundary instead of scattering the activation points.
- Permission policy should explicitly separate allow, ask, and deny behaviors; avoid broad interpreter allow rules.
- If the repo supports long-running or resumable sessions, persist only recovery-critical session state and explicitly model lineage, worktree state, and subagent metadata.
- If work is delegated across multiple agents, define task ownership, dependency edges, and final verification responsibility before parallel execution.
- Use worktree isolation when branch-only execution would contaminate the current workspace.
- Findings come before summaries in review work.
- Treat regression risk as a first-class concern.
- Promote only stable, repeatable rules into this file.
- Keep temporary debugging notes out of this file.

## Local Runtime Notes

- Ports:
- Required env vars:
- External services:
- Data/runtime config paths:

## Dangerous Actions

Require extra caution before:

- deleting branches
- overwriting user config
- stopping unknown processes
- changing production credentials
- force pushing
- destructive database operations

## Promotion Rules

When a new preference or workflow is discovered, classify it before storing it:

- Project-wide stable rule -> this file
- Personal preference -> personal memory, not this repo
- Temporary session note -> do not persist here
