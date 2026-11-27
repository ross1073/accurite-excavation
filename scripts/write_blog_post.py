#!/usr/bin/env python3
"""Write an AccuRite blog post body with an OpenAI model via OpenRouter.

WHY (Ross, same reason as write_gbp_post.py): client-facing text on the AccuRite site must
be written by a non-Claude model. Claude Code runs the research, builds the brief and the
frontmatter, but pastes this script's output VERBATIM into the post body. Never hand-edit
or polish the result — rerun with --note naming the problem instead.

Model: openai/gpt-6.1-sol (same as write_gbp_post.py), pinned to OpenAI's own servers on
OpenRouter with no fallbacks. Same key lookup as write_gbp_post.py.

Usage:
  python3 scripts/write_blog_post.py \
      --title "El Niño winter 2026–27: what it means for your Northern Utah property" \
      --target "El Niño winter" \
      --facts research/blog/el-nino-winter-2026-27/facts.md \
      --brief "Before-and-after checklist ..." \
      --link "/services/grading-land-clearing|grading and land clearing" \
      --link "/blog/avoid-flooding-new-home|How to Avoid Flooding in Your New Utah Home" \
      --out research/blog/el-nino-winter-2026-27/writer-output.md

Prints the markdown body (no frontmatter) to stdout and --out. Writes a JSON run log next
to --out (model, provider, cost, rejected attempts). Exit 1 if no attempt passes the
mechanical checks after --tries attempts.
"""
import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MODEL = "openai/gpt-6.1-sol"
KEY_FILES = [
    Path.home() / ".config/secrets/secrets.env",
    Path.home() / ".hermes/profiles/rk/.env",
]
SERVICE_COUNTIES = {"Weber", "Davis", "Box Elder", "Morgan"}
# Length band from the site's existing posts (584–1,501 words; the educational posts
# run ~900–1,330). Measured 2026-11-26 with `wc -w` on the bodies.
MIN_WORDS, MAX_WORDS = 900, 1500

BLOG_RULES = """\
## AccuRite blog content rules

Business (use exactly, nothing more): AccuRite Excavation & Hauling, based in Ogden, Utah.
In business since 1995. Utah E100 licensed. Service area: Weber, Davis, Box Elder and
Morgan counties in Northern Utah. Write "AccuRite" or "AccuRite Excavation".

Never mention Salt Lake City, Salt Lake County, or any Salt Lake County city. They are not
in the service area.

No fabrication. Do not invent or imply a specific past job, customer, quote, testimonial,
crew size, response time, price, guarantee, or "24/7" availability. Do not claim AccuRite
did work in a named city. Do not invent statistics. Every weather or climate statement
must come from the fact sheet you are given, attributed to NOAA where it is NOAA's.

Do not name, quote or paraphrase any other company's newsletter or marketing. Do not take
swipes at other contractors ("cheap bids", "cutting corners", "fly-by-night") — readers
who already hired someone hear that as an accusation.

Work AccuRite does NOT do — never suggest it: snow removal or plowing, anything inside a
house (indoor plumbing, frozen or burst indoor pipes, basement waterproofing from the
inside), septic pumping. All work described is outside, in the ground.

Voice: a working Northern Utah excavation contractor talking to a property owner. Plain,
direct, practical, friendly. Short paragraphs. No hype, no fear-mongering, no "in today's
world", no emojis, no exclamation marks.

Format: Markdown body only. Do NOT write frontmatter and do NOT write an H1 title — the
site renders the title separately. Use ## for section headings and ### for sub-sections.
Bulleted checklists are welcome. Put every internal link as a normal Markdown link with the
exact path given, e.g. [grading and land clearing](/services/grading-land-clearing). Use
each required internal link at least once, worked naturally into a sentence. You may link
to the NOAA source URLs given in the fact sheet. Do not invent any other link.

You may close with one short, low-key line inviting the reader to [contact AccuRite](/contact)
to look at their property. No phone numbers anywhere. No hashtags.
"""

WEATHER = r"(storms?|stormy|\brain\w*|snow\w*|flood\w*|\bwet\b|wetter|precipitation|runoff|moisture)"
CERTAIN = r"(\bwill\b|\bis expected\b|\bare expected\b|\bis forecast(ed)? to\b|\bare forecast(ed)? to\b|\bis likely\b|\bare likely\b|\bgoing to\b|\bis coming\b|\bare coming\b|\bon the way\b|\bheaded (for|to|our way)\b)"
NEGATION = r"(\bnot\b|n't\b|\bno one\b|\bnobody\b|\bnothing\b|\bnever\b)"
OTHER_REGION = r"(california|southwest|southern|southeast|gulf|east coast|eastern|florida|nationally|across the country|northern rockies|northern u\.?s\.?|northern tier|northern states)"


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
    sys.exit("write_blog_post: OPENROUTER_API_KEY not found")


def allowed_internal_paths():
    paths = {"/contact", "/free-estimate", "/about", "/blog"}
    for s in json.loads((REPO / "src/data/services.json").read_text()):
        paths.add(f"/services/{s['slug']}")
    for loc in json.loads((REPO / "src/data/locations.json").read_text()):
        if loc.get("county") in SERVICE_COUNTIES:
            paths.add(f"/locations/{loc['slug']}")
    for p in (REPO / "src/content/blog").glob("*.md"):
        if not p.name.startswith("_") and not re.search(r"^unlisted:\s*true\s*$", p.read_text(), re.M):
            paths.add(f"/blog/{p.stem}")
    return paths


def sentences(text):
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", plain) if s.strip()]


def check(body, required_links, target, extra_banned, allowed_external):
    problems = []
    words = len(re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body).split())
    if not MIN_WORDS <= words <= MAX_WORDS:
        problems.append(f"{words} words (must be {MIN_WORDS}-{MAX_WORDS})")
    if body.lstrip().startswith("---"):
        problems.append("starts with frontmatter (write the body only)")
    if re.search(r"^# ", body, re.M):
        problems.append("contains an H1 '# ' heading (use ## and ### only)")
    if re.search(r"salt lake", body, re.I):
        problems.append("mentions Salt Lake")
    if re.search(r"\bapex\b", body, re.I):
        problems.append("mentions Apex")
    for word in extra_banned:
        if re.search(re.escape(word), body, re.I):
            problems.append(f"contains banned wording '{word}'")
    if re.search(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", body):
        problems.append("contains a phone number")
    if re.search(r"24/7|24-7|around the clock", body, re.I):
        problems.append("promises 24/7 availability")
    if "#" in re.sub(r"^#{2,3} .*$", "", body, flags=re.M):
        problems.append("contains a stray '#' (hashtag or bad heading)")
    if target and target.lower().replace("ñ", "n") not in body.lower().replace("ñ", "n"):
        problems.append(f"target phrase '{target}' does not appear in the body")
    for path in required_links:
        if f"]({path})" not in body:
            problems.append(f"missing required internal link to {path}")
    ok_paths = allowed_internal_paths()
    for path in re.findall(r"\]\((/[^)\s#]*)", body):
        if path.rstrip("/") not in ok_paths:
            problems.append(f"internal link {path} is not a real in-area page")
    for url in re.findall(r"\]\((https?://[^)\s]+)", body):
        if not any(url.startswith(a) for a in allowed_external):
            problems.append(f"external link {url} is not an allowed source")
    for s in sentences(body):
        if (re.search(WEATHER, s, re.I) and re.search(CERTAIN, s, re.I)
                and not re.search(NEGATION, s, re.I) and not re.search(OTHER_REGION, s, re.I)):
            problems.append(
                f'sentence states weather as certain ("{s[:140]}") — use "can", "could" or "may", '
                "never will/expected/likely for Utah weather"
            )
    return problems, words


def ask(key, messages):
    body = {
        "model": MODEL,
        "messages": messages,
        "provider": {"order": ["openai"], "allow_fallbacks": False},
        "usage": {"include": True},
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.load(r)
    text = resp["choices"][0]["message"]["content"].strip()
    meta = {
        "model": resp.get("model"),
        "provider": resp.get("provider"),
        "cost_usd": (resp.get("usage") or {}).get("cost"),
        "tokens": {k: (resp.get("usage") or {}).get(k) for k in ("prompt_tokens", "completion_tokens")},
    }
    return text, meta


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--target", required=True, help="Target keyword phrase")
    p.add_argument("--facts", required=True, help="Path to the fact sheet (markdown)")
    p.add_argument("--brief", default="", help="Angle, structure, audience")
    p.add_argument("--link", action="append", default=[], help="'/path|anchor idea' — required internal link")
    p.add_argument("--ban", action="append", default=[], help="Extra banned word/phrase")
    p.add_argument("--allow-external", action="append",
                   default=["https://www.cpc.ncep.noaa.gov/", "https://www.noaa.gov/"])
    p.add_argument("--note", action="append", default=[], help="Problem from a previous run to avoid")
    p.add_argument("--tries", type=int, default=3)
    p.add_argument("--out", required=True)
    a = p.parse_args()

    facts = (REPO / a.facts).read_text() if not Path(a.facts).is_absolute() else Path(a.facts).read_text()
    links = [l.split("|", 1) for l in a.link]
    required = [l[0] for l in links]
    link_lines = "\n".join(f"- {path} — {(hint[0] if hint else '')}" for path, *hint in links)

    system = (
        "You write blog posts for AccuRite Excavation's website. Follow every rule below exactly. "
        "Output ONLY the Markdown body of the post: no frontmatter, no H1 title, no preamble, "
        "no notes to the editor.\n\n" + BLOG_RULES
    )
    user = (
        f"Post title (rendered by the site, do not repeat as a heading): {a.title}\n"
        f"Target keyword phrase: \"{a.target}\" — use it naturally in the first paragraph and "
        f"once or twice more. Do not stuff it.\n"
        f"Length: {MIN_WORDS}-{MAX_WORDS} words.\n\n"
        f"Required internal links (each at least once, exact path):\n{link_lines}\n\n"
        f"Brief:\n{a.brief}\n\n"
        f"FACT SHEET — the only source for weather/climate claims. Obey its 'do not say' list:\n\n{facts}"
    )
    if a.note:
        user += "\n\nA previous draft was rejected. Avoid these problems:\n" + "\n".join(f"- {n}" for n in a.note)
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    log = {"model_requested": MODEL, "provider_pin": {"order": ["openai"], "allow_fallbacks": False},
           "notes": a.note, "attempts": []}
    key = load_key()
    for attempt in range(a.tries):
        body, meta = ask(key, messages)
        problems, words = check(body, required, a.target, a.ban, a.allow_external)
        log["attempts"].append({**meta, "words": words, "problems": problems})
        print(f"attempt {attempt + 1}: provider={meta['provider']} model={meta['model']} "
              f"cost=${meta['cost_usd']} words={words}", file=sys.stderr)
        if not problems:
            out.write_text(body + "\n")
            log["total_cost_usd"] = sum(x["cost_usd"] or 0 for x in log["attempts"])
            out.with_suffix(".log.json").write_text(json.dumps(log, indent=1))
            print(body)
            return
        print(f"attempt {attempt + 1} rejected: {'; '.join(problems)}", file=sys.stderr)
        messages += [
            {"role": "assistant", "content": body},
            {"role": "user", "content": "Rewrite the whole post to fix: " + "; ".join(problems)},
        ]
    log["total_cost_usd"] = sum(x["cost_usd"] or 0 for x in log["attempts"])
    out.with_suffix(".log.json").write_text(json.dumps(log, indent=1))
    sys.exit("write_blog_post: no attempt passed the checks")


if __name__ == "__main__":
    main()
