#!/usr/bin/env bash
# SessionEnd hook: dispatches the memory-keeper agent to append today's
# session block to docs/memory/<YYYY-MM-DD>.md.
#
# Wired from .claude/settings.json as a "command" type SessionEnd hook.
# Every invocation logs to .claude/hooks/session-end-memory-keeper.log so
# we have a visible trail when the agent silently no-ops or fails.

set -uo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$repo_root"

log_file=".claude/hooks/session-end-memory-keeper.log"
ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log() { echo "[${ts}] $*" >> "$log_file"; }

# Recursion guard: `claude --agent ... --print` spawns a subprocess Claude
# session, which itself ends and re-fires SessionEnd. Without this guard,
# every real session-end cascades into N invocations until something times
# out. The env var is exported before the claude call below, so any
# subprocess-triggered invocation short-circuits here.
if [[ -n "${CLAUDE_MEMORY_KEEPER_RUNNING:-}" ]]; then
  log "skipped: re-entry from subprocess (CLAUDE_MEMORY_KEEPER_RUNNING=${CLAUDE_MEMORY_KEEPER_RUNNING})"
  exit 0
fi

log "invoked (pwd=${repo_root})"

completed=0
trap '[[ $completed -eq 0 ]] && log "TIMEOUT or KILLED: script exited before OK/FAIL line"' EXIT

if ! command -v claude >/dev/null 2>&1; then
  log "FAIL: claude CLI not found on PATH"
  exit 0
fi

prompt="Run the memory-keeper agent (.claude/agents/memory-keeper.md). Read the session transcript and append a timestamped session block to docs/memory/<today>.md (create the file if missing). Record: decisions made, work completed, items closed, items changed, items deferred, new open items. Never edit prior days' notes. Edit directly — do not stage for approval. If the session was trivial (no commits, no decisions, no state changes), exit silently with no edits."

export CLAUDE_MEMORY_KEEPER_RUNNING=1
output=$(claude --agent memory-keeper --print "$prompt" 2>&1)
rc=$?
unset CLAUDE_MEMORY_KEEPER_RUNNING

if [[ $rc -eq 0 ]]; then
  log "OK (exit=0): ${output:0:200}"
else
  log "FAIL (exit=${rc}): ${output:0:500}"
fi

completed=1
exit 0
