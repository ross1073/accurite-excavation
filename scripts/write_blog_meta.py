#!/usr/bin/env python3
"""Write an AccuRite blog post's title, metaTitle and meta description with the OpenAI writer.

WHY (Ross, same rule as write_blog_post.py / write_gbp_post.py): public copy on the AccuRite
site must not be written by Claude. That includes the frontmatter fields Google shows in
search results. This script hands the finished post body to the same model, on the same
OpenRouter / OpenAI-pinned setup as write_blog_post.py (it imports that script's MODEL, key
lookup and request function), and Claude Code pastes its output into the frontmatter
WORD FOR WORD. Never hand-edit the result — rerun with --note naming the problem instead.

Length limits (from this repo, checked 2026-11-27):
- The page <title> is metaTitle + " | AccuRite Excavation" (22 chars, src/pages/blog/[...slug].astro).
  The site keeps titles under ~60 chars (docs/memory/2026-08-11.md), so metaTitle <= 38.
- Meta descriptions: 150-160 chars per the site spec (docs/superpowers/specs/2026-03-18-
  accurite-phase2-design.md); allowed 140-160 here. No phone number (blog rule).
- title is the on-page H1 and schema headline: 40-80 chars.

Usage:
  python3 scripts/write_blog_meta.py \
      --body research/blog/el-nino-winter-2026-27/writer-output.md \
      --target "El Niño winter" \
      --out research/blog/el-nino-winter-2026-27/meta-output.json

Prints the JSON {title, metaTitle, description} to stdout and --out, plus a run log at
<out>.log.json (model, provider, cost, rejected attempts). Exit 1 if no attempt passes.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from write_blog_post import (  # noqa: E402
    CERTAIN, MODEL, NEGATION, OTHER_REGION, REPO, WEATHER, ask, load_key,
)

SUFFIX = " | AccuRite Excavation"
TITLE_MAX = 60
META_TITLE_MAX = TITLE_MAX - len(SUFFIX)  # 38
TITLE_MIN_H1, TITLE_MAX_H1 = 40, 80
DESC_MIN, DESC_MAX = 140, 160

RULES = f"""\
You write the search-result metadata for one AccuRite Excavation blog post. AccuRite
Excavation & Hauling is an excavation contractor based in Ogden, Utah, serving Weber, Davis,
Box Elder and Morgan counties in Northern Utah.

Return ONLY a JSON object with exactly these three string keys, nothing else:
{{"title": "...", "metaTitle": "...", "description": "..."}}

- "title": the on-page headline shown above the post. {TITLE_MIN_H1}-{TITLE_MAX_H1} characters.
- "metaTitle": the search-result title. At most {META_TITLE_MAX} characters, because the site
  appends "{SUFFIX}" to it. Do not include "AccuRite" in it.
- "description": the meta description shown under the search result. {DESC_MIN}-{DESC_MAX}
  characters. Plain sentence(s) that tell the reader what the post gives them.

All three must contain the target keyword phrase given below, spelled exactly as given
(including any accent). Base every claim only on the post body you are given; add no facts.
Never state Utah weather as certain or expected: the post says NOAA gives Northern Utah
equal chances of a wet or dry winter. Never mention Salt Lake. No phone numbers, no
exclamation marks, no emojis, no hashtags, no clickbait, no fear-mongering.
"""


def check(meta, target):
    problems = []
    for k in ("title", "metaTitle", "description"):
        if not isinstance(meta.get(k), str) or not meta[k].strip():
            problems.append(f"missing or empty '{k}'")
    if problems:
        return problems
    t, mt, d = meta["title"], meta["metaTitle"], meta["description"]
    if not TITLE_MIN_H1 <= len(t) <= TITLE_MAX_H1:
        problems.append(f"title is {len(t)} characters (must be {TITLE_MIN_H1}-{TITLE_MAX_H1})")
    if len(mt) > META_TITLE_MAX:
        problems.append(f"metaTitle is {len(mt)} characters (max {META_TITLE_MAX})")
    if not DESC_MIN <= len(d) <= DESC_MAX:
        problems.append(f"description is {len(d)} characters (must be {DESC_MIN}-{DESC_MAX})")
    for k in ("title", "metaTitle", "description"):
        v = meta[k]
        if unicodedata.normalize("NFC", target).lower() not in unicodedata.normalize("NFC", v).lower():
            problems.append(f"{k} does not contain the target phrase '{target}' exactly")
        if re.search(r"salt lake|\bapex\b", v, re.I):
            problems.append(f"{k} mentions Salt Lake or Apex")
        if "!" in v or "#" in v:
            problems.append(f"{k} contains '!' or '#'")
        if re.search(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", v):
            problems.append(f"{k} contains a phone number")
        if (re.search(WEATHER, v, re.I) and re.search(CERTAIN, v, re.I)
                and not re.search(NEGATION, v, re.I) and not re.search(OTHER_REGION, v, re.I)):
            problems.append(f"{k} states weather as certain — use can/could/may")
    if "accurite" in mt.lower():
        problems.append("metaTitle includes AccuRite (the site adds the brand suffix)")
    return problems


def parse(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--body", required=True, help="Path to the post body (the writer's output)")
    p.add_argument("--target", required=True, help="Target keyword phrase")
    p.add_argument("--note", action="append", default=[], help="Problem from a previous run to avoid")
    p.add_argument("--tries", type=int, default=3)
    p.add_argument("--out", required=True)
    a = p.parse_args()

    body_path = Path(a.body) if Path(a.body).is_absolute() else REPO / a.body
    body = body_path.read_text()
    user = f'Target keyword phrase: "{a.target}"\n\nPOST BODY:\n\n{body}'
    if a.note:
        user += "\n\nA previous answer was rejected. Avoid these problems:\n" + "\n".join(f"- {n}" for n in a.note)
    messages = [{"role": "system", "content": RULES}, {"role": "user", "content": user}]

    out = Path(a.out) if Path(a.out).is_absolute() else REPO / a.out
    out.parent.mkdir(parents=True, exist_ok=True)
    log = {"model_requested": MODEL, "provider_pin": {"order": ["openai"], "allow_fallbacks": False},
           "target": a.target, "body": str(body_path.relative_to(REPO)) if body_path.is_relative_to(REPO) else str(body_path),
           "notes": a.note, "attempts": []}
    log_path = out.with_suffix(".log.json")
    key = load_key()
    for attempt in range(a.tries):
        text, meta_info = ask(key, messages)
        meta = parse(text)
        problems = check(meta, a.target)
        log["attempts"].append({**meta_info, "raw": text, "problems": problems})
        print(f"attempt {attempt + 1}: provider={meta_info['provider']} model={meta_info['model']} "
              f"cost=${meta_info['cost_usd']}", file=sys.stderr)
        if not problems:
            result = {k: meta[k] for k in ("title", "metaTitle", "description")}
            out.write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n")
            log["total_cost_usd"] = sum(x["cost_usd"] or 0 for x in log["attempts"])
            log_path.write_text(json.dumps(log, indent=1, ensure_ascii=False))
            print(json.dumps(result, indent=1, ensure_ascii=False))
            return
        print(f"attempt {attempt + 1} rejected: {'; '.join(problems)}", file=sys.stderr)
        messages += [
            {"role": "assistant", "content": text},
            {"role": "user", "content": "Return the whole JSON object again, fixing: " + "; ".join(problems)},
        ]
    log["total_cost_usd"] = sum(x["cost_usd"] or 0 for x in log["attempts"])
    log_path.write_text(json.dumps(log, indent=1, ensure_ascii=False))
    sys.exit("write_blog_meta: no attempt passed the checks")


if __name__ == "__main__":
    main()
