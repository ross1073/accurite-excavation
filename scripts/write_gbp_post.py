#!/usr/bin/env python3
"""Write the AccuRite GBP post text with an OpenAI model via OpenRouter.

WHY (2026-10-27, Ross): Claude now embeds an invisible text watermark in everything it
writes. Ross wants the post that goes on AccuRite's Google Business Profile written by a
non-Claude model. Claude Code still runs the routine (rotation, Teamwork, logging) but must
paste this script's output VERBATIM — any Claude rewrite, even a light polish, can put the
watermark back.

Model: openai/gpt-6.1-sol, pinned to OpenAI's own servers (no Azure/Bedrock fallback).
OpenAI's published policy: API text watermarking is OFF by default and opt-in per customer.
Through OpenRouter, OpenRouter is the OpenAI customer; their setting is not publicly
documented (checked 2026-10-27).

Usage:
  python3 scripts/write_gbp_post.py --type "Service Highlight" \
      --brief "Service: Demolition. Avoid repeating: Ogden, drainage." --out /tmp/post.txt

Prints the post text to stdout (and --out if given). Exit 1 if no attempt passes the
mechanical checks after 3 tries. Never hand-edit the result; rerun instead.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / ".claude/skills/gbp-post/SKILL.md"
MODEL = "openai/gpt-6.1-sol"
KEY_FILES = [
    Path.home() / ".config/secrets/secrets.env",
    Path.home() / ".hermes/profiles/rk/.env",
]


def load_key():
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"]
    for f in KEY_FILES:
        if f.is_file():
            for line in f.read_text().splitlines():
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                if line.startswith("OPENROUTER_API_KEY="):
                    v = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if v:
                        return v
    sys.exit("write_gbp_post: OPENROUTER_API_KEY not found")


def writing_rules():
    """The content parts of SKILL.md: business info through the templates."""
    text = SKILL.read_text()
    start = text.index("## Business info")
    end = text.index("## Photo selection")
    return text[start:end]


def check(post):
    problems = []
    words = len(post.split())
    if len(post) >= 1500:
        problems.append(f"{len(post)} characters (must be under 1,500)")
    if not 150 <= words <= 300:
        problems.append(f"{words} words (must be 150-300)")
    if re.search(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", post):
        problems.append("contains a phone number")
    if "#" in post:
        problems.append("contains a hashtag")
    if re.search(r"salt lake", post, re.I):
        problems.append("mentions Salt Lake")
    if re.search(r"\b(call us|free estimate|contact us|visit our|book now|get started)\b", post, re.I):
        problems.append("contains a call to action")
    return problems


def ask(key, messages):
    body = {
        "model": MODEL,
        "messages": messages,
        "provider": {"order": ["openai"], "allow_fallbacks": False},
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)["choices"][0]["message"]["content"].strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--type", required=True, help="Educational / Seasonal Tip / Service Highlight / Review-Trust")
    p.add_argument("--brief", default="", help="Topic, service, date context, things to avoid repeating")
    p.add_argument("--out")
    a = p.parse_args()

    system = (
        "You write Google Business Profile posts for AccuRite Excavation & Hauling. "
        "Follow every rule below exactly. Output ONLY the post text: no title, no quotes, "
        "no preamble, no notes, no markdown.\n\n" + writing_rules()
    )
    user = f"Write this week's post. Post type: {a.type}.\n{a.brief}".strip()
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

    key = load_key()
    for attempt in range(3):
        post = ask(key, messages)
        problems = check(post)
        if not problems:
            if a.out:
                Path(a.out).write_text(post + "\n")
            print(post)
            return
        print(f"attempt {attempt + 1} rejected: {'; '.join(problems)}", file=sys.stderr)
        messages += [
            {"role": "assistant", "content": post},
            {"role": "user", "content": "Rewrite it to fix: " + "; ".join(problems)},
        ]
    sys.exit("write_gbp_post: no attempt passed the checks")


if __name__ == "__main__":
    main()
