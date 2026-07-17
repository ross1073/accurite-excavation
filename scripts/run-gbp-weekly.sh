#!/bin/zsh
# Runs the AccuRite weekly Google Business Profile post routine via Claude Code in
# non-interactive mode. Fired by launchd on Tuesdays at 12:03 local time.
# See ~/Library/LaunchAgents/com.rosswalker.accurite-gbp-weekly.plist.
#
# WHY THIS RUNS ON ROSS'S MAC AND NOT A claude.ai CLOUD ROUTINE (migrated 2026-07-17):
# claude.ai RemoteTrigger sandboxes block outbound HTTPS to almost every host, including
# csfund.teamwork.com. The Teamwork REST client (scripts/teamwork.py) therefore could not
# create the task from the cloud — the proxy rejected the connection (403 connect_rejected),
# so the post silently produced nothing week after week. This machine has normal internet
# egress, so the REST client works here. REST is correct; the cloud sandbox was the problem.

set -eu

# launchd ships a minimal PATH; restore what an interactive shell would see.
export PATH="/Users/rosswalker/.local/bin:/Users/rosswalker/.nvm/versions/node/v24.14.0/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export HOME="/Users/rosswalker"

LOG_DIR="$HOME/Library/Logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/accurite-gbp-weekly.log"

echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) — run start =====" >> "$LOG"

cd /Users/rosswalker/projects/accurite-excavation

# --allowedTools enumerates exactly what the routine may call. No --dangerously-skip-permissions:
# any tool not on this list fails closed, so in headless mode the run aborts rather than escalating.
/Users/rosswalker/.local/bin/claude \
  --allowedTools \
    "Bash" \
    "Read" \
    "Write" \
    "Edit" \
    "Glob" \
    "Grep" \
  -p "Generate and file this week's AccuRite Google Business Profile post. This is the unattended scheduled run — do NOT ask questions, ship straight to Cassandra. Read .claude/skills/gbp-post/SKILL.md and execute it exactly: follow every content and Google-policy hard rule, pick the next rotation type (Teamwork is the source of truth for history — never auto-generate a Project Spotlight), write the post, and create the Teamwork task for Cassandra to proof and approve. Use the vendored REST client for ALL Teamwork calls: python3 scripts/teamwork.py (it reads TEAMWORK_API_TOKEN from ~/.config/secrets/secrets.env). NEVER use the Teamwork MCP connector. Best-effort commit+push the post-log per the skill; if that push fails, do not fail the run. If any step genuinely fails, run ~/.local/bin/notify with a one-line summary of what broke." \
  >> "$LOG" 2>&1

echo "===== $(date -u +%Y-%m-%dT%H:%M:%SZ) — run end =====" >> "$LOG"
