#!/usr/bin/env python3
"""
tw — the ONE canonical way anything on this machine talks to Teamwork.

Why this exists
---------------
The claude.ai Teamwork MCP connector authenticates with interactive OAuth. Its token
expires and can only be renewed by a human clicking through claude.ai connector
settings. That is fine for a live session and FATAL for anything scheduled: when the
token dies, an unattended run has no human to click, so it fails silently. That is
exactly how the AccuRite weekly GBP post disappeared for three weeks in Jun/Jul 2026
without anyone noticing.

The Teamwork REST API uses a STATIC token that does not expire. So:

    REST is the only supported path for unattended work. MCP is never a dependency.

Token resolution order (first hit wins):
    1. $TEAMWORK_API_TOKEN                     (cloud routines / CI / GitHub Actions)
    2. ~/.config/secrets/secrets.env           (this machine — the master secrets file)

That order is what makes this portable: the same command works on Ross's Mac, in a
claude.ai cloud routine, and in GitHub Actions, with no code change.

Usage
-----
    tw whoami
    tw tasklists <project_id>
    tw tasks <project_id> [--search TEXT] [--limit N]
    tw create --tasklist ID --name "..." [--desc "..."] [--desc-file PATH]
              [--assignee ID] [--due YYYY-MM-DD] [--start YYYY-MM-DD] [--priority none]
    tw comment --task ID --body "..."
    tw complete --task ID

People: Ross 157735, Cassandra 463236.  Site: https://csfund.teamwork.com
Never print the token. Errors are loud and non-zero — never silent.
"""

import argparse
import base64
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

SITE = os.environ.get("TEAMWORK_SITE", "https://csfund.teamwork.com")
SECRETS = pathlib.Path.home() / ".config" / "secrets" / "secrets.env"

PEOPLE = {"ross": "157735", "cassandra": "463236"}


def die(msg, code=1):
    print(f"tw: error: {msg}", file=sys.stderr)
    sys.exit(code)


def get_token():
    tok = os.environ.get("TEAMWORK_API_TOKEN", "").strip()
    if tok:
        return tok
    if SECRETS.exists():
        for line in SECRETS.read_text().splitlines():
            line = line.strip()
            if line.startswith("TEAMWORK_API_TOKEN="):
                return line.split("=", 1)[1].strip().strip("'\"")
    die(
        "no Teamwork token. Set $TEAMWORK_API_TOKEN, or add TEAMWORK_API_TOKEN= to "
        f"{SECRETS}. Do NOT fall back to the Teamwork MCP — it expires and cannot "
        "self-renew in an unattended run."
    )


def call(method, path, body=None):
    """Basic auth: token as username, any password."""
    token = get_token()
    url = path if path.startswith("http") else f"{SITE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    auth = base64.b64encode(f"{token}:x".encode()).decode()
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read().decode()
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:600]
        if e.code in (401, 403):
            die(
                f"Teamwork auth failed (HTTP {e.code}). The REST token is bad or revoked. "
                "Fix the token — do not switch to the MCP connector.\n" + detail
            )
        die(f"Teamwork API {method} {url} -> HTTP {e.code}\n{detail}")
    except urllib.error.URLError as e:
        die(f"Teamwork API unreachable: {e.reason}")


def ymd(s):
    """Accept YYYY-MM-DD, emit Teamwork v1's YYYYMMDD."""
    return s.replace("-", "") if s else None


def resolve_person(v):
    if not v:
        return None
    return PEOPLE.get(str(v).lower(), str(v))


def main():
    p = argparse.ArgumentParser(prog="tw", description="Canonical Teamwork REST client (never MCP).")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("whoami")

    t = sub.add_parser("tasklists"); t.add_argument("project_id")

    k = sub.add_parser("tasks")
    k.add_argument("project_id")
    k.add_argument("--search")
    k.add_argument("--limit", type=int, default=50)

    c = sub.add_parser("create")
    c.add_argument("--tasklist", required=True)
    c.add_argument("--name", required=True)
    c.add_argument("--desc", default="")
    c.add_argument("--desc-file")
    c.add_argument("--assignee", default="ross")
    c.add_argument("--start")
    c.add_argument("--due")
    c.add_argument("--priority", default="")

    m = sub.add_parser("comment")
    m.add_argument("--task", required=True)
    m.add_argument("--body", required=True)

    d = sub.add_parser("complete"); d.add_argument("--task", required=True)

    a = p.parse_args()

    if a.cmd == "whoami":
        me = call("GET", "/me.json").get("person", {})
        print(f"{me.get('id')}  {me.get('first-name')} {me.get('last-name')}  {me.get('email-address')}")

    elif a.cmd == "tasklists":
        r = call("GET", f"/projects/api/v3/projects/{a.project_id}/tasklists.json")
        for tl in r.get("tasklists", []):
            print(f"{tl['id']}\t{tl['name']}")

    elif a.cmd == "tasks":
        q = f"/projects/api/v3/projects/{a.project_id}/tasks.json?pageSize={a.limit}&includeCompletedTasks=true"
        if a.search:
            q += f"&searchTerm={urllib.request.quote(a.search)}"
        r = call("GET", q)
        for tk in r.get("tasks", []):
            print(f"{tk['id']}\t{(tk.get('createdAt') or '')[:10]}\t{tk.get('status')}\t{tk['name']}")

    elif a.cmd == "create":
        desc = a.desc
        if a.desc_file:
            desc = pathlib.Path(a.desc_file).read_text()
        item = {"content": a.name, "description": desc}
        who = resolve_person(a.assignee)
        if who:
            item["responsible-party-id"] = who
        if a.start:
            item["start-date"] = ymd(a.start)
        if a.due:
            item["due-date"] = ymd(a.due)
        if a.priority:
            item["priority"] = a.priority
        r = call("POST", f"/tasklists/{a.tasklist}/tasks.json", {"todo-item": item})
        tid = r.get("id") or r.get("taskId")
        if not tid:
            die(f"task create returned no id: {r}")
        print(tid)
        print(f"{SITE}/app/tasks/{tid}", file=sys.stderr)

    elif a.cmd == "comment":
        call("POST", f"/tasks/{a.task}/comments.json",
             {"comment": {"body": a.body, "notify": "", "content-type": "text"}})
        print("ok")

    elif a.cmd == "complete":
        call("PUT", f"/tasks/{a.task}/complete.json")
        print("ok")


if __name__ == "__main__":
    main()
