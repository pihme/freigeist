#!/usr/bin/env python3
"""Freigeist static site builder - no dependencies beyond Python 3.8+.

    python3 build.py                 # build published posts into ./site
    python3 build.py --drafts        # include posts with draft: true
    python3 build.py --out DIR       # other output directory
    python3 build.py --serve         # build, then serve on http://localhost:8000
"""
import argparse, datetime, html, os, re, shutil, sys, textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))
TH = os.path.join(ROOT, "theme")
E = html.escape

# ---------- front matter + tiny Markdown ----------
def parse(path):
    raw = open(path, encoding="utf-8").read()
    meta, body = {}, raw
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            if ":" not in line or line.strip().startswith("#"): continue
            k, v = line.split(":", 1); v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                v = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
            elif v.lower() in ("true", "false"): v = v.lower() == "true"
            else: v = v.strip("\"'")
            meta[k.strip()] = v
    meta.setdefault("title", os.path.splitext(os.path.basename(path))[0])
    meta["slug"] = meta.get("slug") or re.sub(r"^\d{4}-\d\d-\d\d-", "", os.path.splitext(os.path.basename(path))[0])
    meta["body"] = body
    return meta

def inline(t):
    codes = []
    t = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes)-1}\x00", t)
    t = E(t, quote=False)
    t = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(.+?)\*(?![\w*])", r"<em>\1</em>", t)
    return re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{E(codes[int(m.group(1))])}</code>", t)

def markdown(src):
    out, para, lst, lines = [], [], None, src.splitlines()
    def flush():
        nonlocal para, lst
        if para: out.append("<p>" + inline(" ".join(para)) + "</p>"); para = []
        if lst: out.append(f"<{lst[0]}>" + "".join(f"<li>{inline(i)}</li>" for i in lst[1]) + f"</{lst[0]}>"); lst = None
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            flush(); lang = l[3:].strip(); buf = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"): buf.append(lines[i]); i += 1
            out.append(f'<pre><code class="lang-{E(lang)}">' + E("\n".join(buf)) + "</code></pre>")
        elif re.match(r"^#{1,6} ", l):
            flush(); n = len(l) - len(l.lstrip("#")); out.append(f"<h{n}>{inline(l[n+1:].strip())}</h{n}>")
        elif l.startswith(">"):
            flush(); out.append(f"<blockquote><p>{inline(l.lstrip('> '))}</p></blockquote>")
        elif re.match(r"^\s*([-*]|\d+\.) ", l):
            if para: flush()
            kind = "ol" if re.match(r"^\s*\d+\.", l) else "ul"
            if not lst or lst[0] != kind: flush(); lst = (kind, [])
            lst[1].append(re.sub(r"^\s*([-*]|\d+\.) ", "", l))
        elif not l.strip(): flush()
        elif l.strip() in ("---", "***"): flush(); out.append("<hr>")
        else:
            if lst: flush()
            para.append(l.strip())
        i += 1
    flush()
    return "\n".join(out)

def minutes(body): return max(1, round(len(re.findall(r"\w+", body)) / 220))

def nice_date(d):
    try: return datetime.date.fromisoformat(str(d)).strftime("%-d %b %Y").upper()
    except ValueError: return str(d).upper()

def meta_line(p):
    return f'{p.get("type","post").upper()} · {minutes(p["body"])} MIN · {nice_date(p.get("date",""))}'

# ---------- hero cards (SVG) ----------
def tspans(text, x, width, dy, max_lines):
    lines = textwrap.wrap(text, width)[:max_lines]
    if len(textwrap.wrap(text, width)) > max_lines: lines[-1] = lines[-1].rstrip(".,;: ") + "…"
    return "".join(f'<tspan x="{x}"{"" if k == 0 else f" dy={chr(34)}{dy}{chr(34)}"}>{E(s)}</tspan>' for k, s in enumerate(lines))

def cards(a, b, root, mobile):
    G, L = 'font-family="Cormorant Garamond"', lambda p: f'{root}posts/{p["slug"]}.html'
    s = ""
    if not mobile:
        if a:
            s += (f'<text x="96" y="455" {G} font-size="15" fill="#8a8079" letter-spacing="2">{E(meta_line(a))}</text>'
                  f'<a href="{L(a)}"><text x="96" y="510" {G} font-style="italic" font-size="46" fill="#2b2724">{tspans(a["title"],96,34,0,1)}</text></a>'
                  f'<text x="96" y="570" {G} font-size="21" fill="#3a332e">{tspans(a.get("summary",""),96,62,31,3)}</text>'
                  f'<a href="{L(a)}"><text x="96" y="695" {G} font-size="19" fill="#2b2724" text-decoration="underline">Read more</text></a>')
        if b:
            s += (f'<text x="960" y="645" {G} font-size="15" fill="#8a8079" letter-spacing="2">{E(meta_line(b))}</text>'
                  f'<a href="{L(b)}"><text x="960" y="695" {G} font-style="italic" font-size="36" fill="#2b2724">{tspans(b["title"],960,22,42,2)}</text></a>')
    else:
        if a:
            s += (f'<text x="24" y="410" {G} font-size="13" fill="#8a8079" letter-spacing="2">{E(meta_line(a))}</text>'
                  f'<a href="{L(a)}"><text x="24" y="455" {G} font-style="italic" font-size="34" fill="#2b2724">{tspans(a["title"],24,19,40,2)}</text></a>'
                  f'<text x="24" y="550" {G} font-size="18" fill="#3a332e">{tspans(a.get("summary",""),24,36,28,3)}</text>'
                  f'<a href="{L(a)}"><text x="24" y="660" {G} font-size="17" fill="#2b2724" text-decoration="underline">Read more</text></a>')
        if b:
            s += f'<a href="{L(b)}"><text x="24" y="742" {G} font-style="italic" font-size="24" fill="#2b2724">{tspans(b["title"],24,30,0,1)}</text></a>'
    return s

# ---------- pages ----------
def page(title, main, root, a=None, b=None):
    base = open(os.path.join(TH, "base.html"), encoding="utf-8").read()
    hd = open(os.path.join(TH, "hero-desktop.svg"), encoding="utf-8").read().replace("{{CARDS}}", cards(a, b, root, False))
    hm = open(os.path.join(TH, "hero-mobile.svg"), encoding="utf-8").read().replace("{{CARDS}}", cards(a, b, root, True))
    if not b:  # hide empty second card background
        hd = hd.replace('<rect class="c2"', '<rect class="c2" display="none"')
        hm = hm.replace('<rect x="12" y="712"', '<rect display="none" x="12" y="712"')
    return (base.replace("{{HERO_D}}", hd).replace("{{HERO_M}}", hm).replace("{{MAIN}}", main)
                .replace("{{TITLE}}", E(title)).replace("{{ROOT}}", root))

MK = '<svg class="mk" viewBox="0 0 88 88"><use href="#fg-mark"/></svg>'
FOOT = f'<footer>{MK}FREIGEIST · FG-06 · NOTES FROM OPEN-SOURCE WORK</footer>'

def teaser(p, root):
    tags = " · ".join("#" + t for t in p.get("tags", []))
    proj = f'PROJECT: {E(p["project"]).upper()} · ' if p.get("project") else ""
    dr = '<span class="draft">DRAFT</span>' if p.get("draft") else ""
    return (f'<article><div class="meta">{E(meta_line(p))}{dr}</div><i class="st"></i>'
            f'<h2><a href="{root}posts/{p["slug"]}.html">{E(p["title"])}</a></h2><p>{E(p.get("summary",""))}</p>'
            f'<div class="tags">{proj}{E(tags)}</div><a href="{root}posts/{p["slug"]}.html" class="more">Read more</a></article>')

def listing(kick, items, root):
    n = f"{len(items):02d}"
    return (f'<main class="posts"><div class="kick"><span>{MK}{E(kick)}</span><span>{n} / {n}</span></div>'
            f'<div class="grid">{"".join(teaser(p, root) for p in items)}</div>{FOOT}</main>')

def build(out, drafts):
    posts = [parse(os.path.join(ROOT, "posts", f)) for f in sorted(os.listdir(os.path.join(ROOT, "posts"))) if f.endswith(".md")]
    posts = [p for p in posts if drafts or not p.get("draft")]
    posts.sort(key=lambda p: str(p.get("date", "")), reverse=True)
    if os.path.exists(out): shutil.rmtree(out)
    os.makedirs(os.path.join(out, "posts"))
    shutil.copytree(TH, os.path.join(out, "theme"), ignore=shutil.ignore_patterns("*.html", "hero-*.svg"))
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(out, "assets"))
    fonts = [("Cormorant Garamond", "CormorantGaramond-VariableFont_wght.ttf", "normal", "300 700"),
             ("Cormorant Garamond", "CormorantGaramond-Italic-VariableFont_wght.ttf", "italic", "300 700"),
             ("IBM Plex Mono", "IBMPlexMono-Regular.ttf", "normal", "400 500"), ("IBM Plex Mono", "IBMPlexMono-SemiBold.ttf", "normal", "600"),
             ("IBM Plex Mono", "IBMPlexMono-Bold.ttf", "normal", "700"), ("Unbounded", "Unbounded-VariableFont_wght.ttf", "normal", "200 900")]
    open(os.path.join(out, "theme", "fonts.css"), "w").write("".join(
        f"@font-face{{font-family:'{a}';src:url(fonts/{f}) format('truetype');font-style:{s};font-weight:{w};font-display:swap}}\n" for a, f, s, w in fonts))
    W = lambda path, s: open(os.path.join(out, path), "w", encoding="utf-8").write(s)
    a, b = (posts + [None, None])[:2]
    W("index.html", page("Freigeist", listing("ALL POSTS // ARCHIVE", posts, ""), "", a, b))
    notes = [p for p in posts if p.get("type") == "note"]
    W("notes.html", page("Notes – Freigeist", listing("NOTES // SHORT FORM", notes, ""), "", *(notes + [None, None])[:2]))
    projects = {}
    for p in posts: projects.setdefault(p.get("project") or "misc", []).append(p)
    pm = "".join(f'<div class="kick"><span>{MK}PROJECT // {E(k).upper()}</span><span>{len(v):02d}</span></div><div class="grid" style="margin-bottom:80px">{"".join(teaser(p, "") for p in v)}</div>' for k, v in sorted(projects.items()))
    W("projects.html", page("Projects – Freigeist", f'<main class="posts">{pm}{FOOT}</main>', "", a, b))
    about = os.path.join(ROOT, "pages", "about.md")
    if os.path.exists(about):
        ab = parse(about)
        W("about.html", page("About – Freigeist", f'<main class="posts post"><div class="prose"><h1>{E(ab["title"])}</h1>{markdown(ab["body"])}</div>{FOOT}</main>', "", a, b))
    for i, p in enumerate(posts):
        nxt = posts[i + 1] if i + 1 < len(posts) else None
        dr = '<span class="draft">DRAFT</span>' if p.get("draft") else ""
        tags = " · ".join("#" + t for t in p.get("tags", []))
        proj = f'PROJECT: {E(p["project"]).upper()} · ' if p.get("project") else ""
        main = (f'<main class="posts post"><div class="kick"><a class="back" href="../index.html">← All posts</a><span>{E(meta_line(p))}{dr}</span></div>'
                f'<div class="prose"><h1>{E(p["title"])}</h1><div class="tags">{proj}{E(tags)}</div>{markdown(p["body"])}</div>{FOOT}</main>')
        W(f'posts/{p["slug"]}.html', page(f'{p["title"]} – Freigeist', main, "../", p, nxt))
    print(f"built {len(posts)} posts into {out}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "site"))
    ap.add_argument("--drafts", action="store_true")
    ap.add_argument("--serve", action="store_true")
    a = ap.parse_args()
    build(os.path.abspath(a.out), a.drafts)
    if a.serve:
        import http.server, functools
        print("serving http://localhost:8000  (Ctrl+C to stop)")
        http.server.ThreadingHTTPServer(("", 8000), functools.partial(http.server.SimpleHTTPRequestHandler, directory=a.out)).serve_forever()
