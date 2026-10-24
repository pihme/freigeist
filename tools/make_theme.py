#!/usr/bin/env python3
"""One-off: derive theme/ from the round-6 design sources (variant C, 'fine cut').
Usage: python3 tools/make_theme.py <round6-dir>
Not needed for normal blogging - theme/ is committed."""
import re, sys, os, shutil
R = sys.argv[1]; T = os.path.join(os.path.dirname(__file__), "..", "theme")
H = open(os.path.join(R, "demo/C-feiner-hieb.html")).read()

def card_tokens(s, mobile):
    # replace the two static German teaser cards with tokens filled by build.py
    if not mobile:
        a = s.index('<text x="96" y="455"'); b = s.index('<g class="g-bar">', a)
        s = s[:a] + '{{CARDS}}' + s[b:]
        s = s.replace('<rect x="80" y="420" width="800" height="295"', '<rect class="c1" x="80" y="420" width="800" height="295"')
        s = s.replace('<rect x="950" y="615" width="400" height="140"', '<rect class="c2" x="950" y="615" width="400" height="140"')
    else:
        a = s.index('<text x="24" y="410"'); b = s.index('<clipPath', a)
        s = s[:a] + '{{CARDS}}' + s[b:]
    return s

TR = [("BLÜTE 06 // HALB STICH", "BLOSSOM 06 // HALF ETCH"), ("HALB PIXEL · 1-BIT", "HALF PIXEL · 1-BIT"),
      ("SIGNAL: ZART", "SIGNAL: SOFT"), ("FREIGEIST · 52.52N", "FREIGEIST · 22.91S"), ("STICH→PIXEL", "ETCH→PIXEL"), ("EIN BLOG ÜBER DAS FREIE DENKEN", "STEERING AI IN UNCHARTED WATERS"),
      (">Texte<", '><a href="{{ROOT}}index.html">Posts</a><'), (">Notizen<", '><a href="{{ROOT}}notes.html">Notes</a><'),
      (">Wege<", '><a href="{{ROOT}}projects.html">Projects</a><'), (">Über<", '><a href="{{ROOT}}about.html">About</a><'),
      ("Texte   Notizen   Wege   Über", "Posts   Notes   Projects   About")]
svgs = re.findall(r'<svg class="(?:d|m)".*?</svg>', H, flags=re.S)
# the first two body-level svgs are the hero (desktop, mobile)
d, m = svgs[0], svgs[1]
for a, b in TR: d = d.replace(a, b); m = m.replace(a, b)
# English nav labels are longer: respace them
for o, n in [('x="1040" y="70"', 'x="1010" y="70"'), ('x="1136.0" y="70"', 'x="1088" y="70"'), ('x="1256.8" y="70"', 'x="1170" y="70"'), ('x="1340.3999999999999" y="70"', 'x="1280" y="70"')]:
    d = d.replace(o, n)
# plate number = two-digit year, filled by build.py
d = d.replace("FG-06", "FG-{{YY}}").replace("FG/06", "FG/{{YY}}"); m = m.replace("FG-06", "FG-{{YY}}").replace("FG/06", "FG/{{YY}}")
d = card_tokens(d, False); m = card_tokens(m, True)
open(os.path.join(T, "hero-desktop.svg"), "w").write(d)
open(os.path.join(T, "hero-mobile.svg"), "w").write(m)

# page shell: head (accent picker + css), hero slots, main slot, header bar + scripts
h = H.replace(d and svgs[0], "{{HERO_D}}", 1).replace(svgs[1], "{{HERO_M}}", 1)
h = re.sub(r"@font-face\{[^}]*\}", "", h)
h = h.replace('<html lang="de">', '<html lang="en">')
h = re.sub(r"<title>.*?</title>", "<title>{{TITLE}}</title><link rel=\"stylesheet\" href=\"{{ROOT}}theme/fonts.css\"><link rel=\"stylesheet\" href=\"{{ROOT}}theme/content.css\"><link rel=\"icon\" href=\"{{ROOT}}assets/freigeist-mark.svg\">", h)
a = h.index('<main class="posts">'); b = h.index('</main>') + 7
h = h[:a] + "{{MAIN}}" + h[b:]
h = re.sub(r'<nav class="demo">.*?</nav>', "", h)
# placeholder HUD coordinates: Rio de Janeiro
h = h.replace("52.52N 13.40E", "22.91S 43.17W").replace("FG-06", "FG-{{YY}}")
# compact mode (post pages): hero hidden, header permanently compact; title + mark link home
h = h.replace("let p=Math.min(1,Math.max(0,y/st.dist));", "let p=Math.min(1,Math.max(0,y/st.dist));if(document.body.classList.contains('compact'))p=1;")
h = h.replace("bar.style.opacity=e;", "bar.style.opacity=e;{const hh=document.getElementById('hhome');if(hh){hh.style.left=(tx+st.tb.x*k)+'px';hh.style.top=(ty+st.tb.y*k)+'px';hh.style.width=((st.tb.r-st.tb.x)*k+(st.mob?54:66))+'px';hh.style.height=Math.max(30,(st.tb.b-st.tb.y)*k)+'px';hh.style.pointerEvents=e>.6?'auto':'none'}}", 1)
h = h.replace('<div id="hbar">', '<a id="hhome" href="{{ROOT}}index.html" aria-label="Freigeist – home"></a><style>#hhome{position:fixed;z-index:6;pointer-events:none}body.compact>svg.d,body.compact>svg.m{position:absolute;top:0;left:0;visibility:hidden;pointer-events:none}body.compact main.posts{position:relative;z-index:1;margin-top:0;padding-top:130px}@media(max-width:700px){body.compact main.posts{padding-top:110px}}</style><div id="hbar">', 1)
for a_, b_ in [('aria-label="Menü"', 'aria-label="Menu"'), ('<a href="#">Texte</a>', '<a href="{{ROOT}}index.html">Posts</a>'),
               ('<a href="#">Notizen</a>', '<a href="{{ROOT}}notes.html">Notes</a>'), ('<a href="#">Wege</a>', '<a href="{{ROOT}}projects.html">Projects</a>'),
               ('<a href="#">Über</a>', '<a href="{{ROOT}}about.html">About</a>')]:
    h = h.replace(a_, b_)
import base64
names = iter(["waves-desktop.svg", "waves-mobile.svg", "waves-bar.svg"])
def _ext(m):
    n = next(names); open(os.path.join(T, n), "wb").write(base64.b64decode(m.group(1))); return "url({{ROOT}}theme/" + n + ")"
h = re.sub(r"url\(data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)\)", _ext, h)
open(os.path.join(T, "base.html"), "w").write(h)

F = "/usr/share/fonts/truetype/sand-box/google/"
for p in ["Cormorant Garamond/CormorantGaramond-VariableFont_wght.ttf", "Cormorant Garamond/CormorantGaramond-Italic-VariableFont_wght.ttf",
          "IBM Plex Mono/IBMPlexMono-Regular.ttf", "IBM Plex Mono/IBMPlexMono-SemiBold.ttf", "IBM Plex Mono/IBMPlexMono-Bold.ttf", "Unbounded/Unbounded-VariableFont_wght.ttf"]:
    shutil.copy(F + p, os.path.join(T, "fonts", os.path.basename(p)))
for x in ["OFL.txt", "LICENSE.txt"]:
    for fam in ["Cormorant Garamond", "IBM Plex Mono", "Unbounded"]:
        if os.path.exists(F + fam + "/" + x): shutil.copy(F + fam + "/" + x, os.path.join(T, "fonts", fam.replace(" ", "") + "-" + x))
print("theme written")
