#!/usr/bin/env python3
"""
Static site generator for minghaozhou.com

Edit _build/projects.json, then run:   python3 _build/build.py
Outputs index.html and work/<slug>.html at the site root.

Nothing here needs installing — standard library only.
"""

import json
import html
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "_build" / "projects.json"
WORK = ROOT / "work"

# Pages that appear in the header nav: (href from root, label, key)
NAV = [("index.html", "Work", "work"),
       ("teaching.html", "Teaching", "teaching"),
       ("about.html", "About", "about")]

CV_PATH = "MinghaoZhou_CV.pdf"


def esc(s):
    return html.escape(s, quote=True)


def nav_html(active, depth=0):
    """depth=0 for root pages, 1 for pages inside work/."""
    up = "../" * depth
    out = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ""
        out.append(f'<a href="{up}{href}"{cur}>{esc(label)}</a>')
    out.append(f'<a class="cv" href="{up}{CV_PATH}">CV (PDF)</a>')
    return "\n        ".join(out)


def head(title, desc, depth=0):
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}css/style.css">
</head>
<body>"""


def header(active, depth=0):
    up = "../" * depth
    return f"""
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{up}index.html">Minghao Zhou<span>.</span></a>
    <nav class="nav">
        {nav_html(active, depth)}
    </nav>
  </div>
</header>"""


def footer(depth=0):
    return """
<footer class="site-foot">
  <div class="wrap">
    <div class="foot-links">
      <a href="mailto:zhoumh.ariza@gmail.com">zhoumh.ariza@gmail.com</a>
      <a href="https://www.linkedin.com/in/minghaoz">LinkedIn</a>
      <a href="https://vimeo.com/user105794618">Vimeo</a>
      <a href="https://assetstore.unity.com/packages/templates/systems/penguin-arpg-toolkit-302387">Unity Asset Store</a>
    </div>
    <div class="copyright">&copy; 2026 Minghao Zhou</div>
  </div>
</footer>
</body>
</html>"""


PLAY_ICON = ('<svg viewBox="0 0 10 12" fill="currentColor" aria-hidden="true">'
             '<path d="M0 0l10 6-10 6z"/></svg>')


def video_block(url, title, hint):
    """Render an embed if a URL is set, otherwise a labelled empty slot."""
    if url:
        return (f'<div class="embed"><iframe src="{esc(url)}" title="{esc(title)}" '
                f'allowfullscreen loading="lazy" '
                f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
                f'gyroscope; picture-in-picture"></iframe></div>')
    return f"""<div class="video-ph">
        <span class="icon">{PLAY_ICON}</span>
        <strong>{esc(hint)}</strong>
        <code>{esc(title)}</code>
      </div>"""


def thumb(p, depth=0):
    up = "../" * depth
    figs = p.get("figures") or []
    if figs:
        src = figs[0]["src"]
        return (f'<div class="thumb">'
                f'<img src="{up}{esc(src)}" alt="{esc(p["title"])}" loading="lazy" '
                f'onerror="this.remove()">'
                f'<div class="ph">{esc(src)}</div></div>')
    return f'<div class="thumb"><div class="ph">add image</div></div>'


def card(p):
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in p.get("tags", []))
    return f"""      <a class="card" href="work/{esc(p['slug'])}.html">
        {thumb(p)}
        <div class="card-body">
          <h3>{esc(p['title'])}</h3>
          <p class="role">{esc(p.get('role',''))} &middot; {esc(p.get('year',''))}</p>
          <div class="tags">{tags}</div>
        </div>
      </a>"""


def build_index(data):
    by_group = {}
    for p in data["projects"]:
        by_group.setdefault(p["group"], []).append(p)

    sections = []
    for g in data["groups"]:
        items = by_group.get(g["id"], [])
        if not items:
            continue
        note = f'<p class="section-note">{esc(g["note"])}</p>' if g.get("note") else ""
        cards = "\n".join(card(p) for p in items)
        sections.append(f"""  <section class="section" id="{esc(g['id'])}">
    <div class="wrap">
      <div class="section-head">
        <h2>{esc(g['title'])}</h2>
        <span class="count">{len(items):02d}</span>
      </div>
      {note}
      <div class="grid">
{cards}
      </div>
    </div>
  </section>""")

    reel = data.get("reel", {})
    reel_note = reel.get("note", "")
    reel_html = f"""
  <section class="reel" id="reel">
    <div class="wrap">
      <div class="section-head">
        <h2>{esc(reel.get('title', 'Demo Reel'))}</h2>
        <span class="count">{esc(reel.get('year', ''))}</span>
      </div>
      {video_block(reel.get('embed', ''), 'reel.embed in _build/projects.json',
                   'Demo reel goes here')}
      {f'<p class="reel-note">{esc(reel_note)}</p>' if reel_note and not reel.get('embed') else ''}
    </div>
  </section>
"""

    body = f"""
  <section class="hero">
    <div class="wrap">
      <p class="label">Technical Artist &middot; Game Developer &middot; Educator</p>
      <h1>Rigging, animation systems and pipeline tools.</h1>
      <p class="lede">I build the tools that sit between artists and engines — rigging systems,
      editor tooling and animation architecture in Maya, Unreal Engine and Unity.
      I'm currently <strong>Assistant Professor of Game Development at SUNY Morrisville</strong>,
      and I run <strong>Erosoft Studio</strong>, where I'm making a character-driven puzzle game in UE5.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="#reel">Watch the reel</a>
        <a class="btn" href="{CV_PATH}">Download CV</a>
        <a class="btn" href="mailto:zhoumh.ariza@gmail.com">Get in touch</a>
      </div>
    </div>
  </section>
{reel_html}
{chr(10).join(sections)}
"""
    page = (head("Minghao Zhou — Technical Artist & Game Developer",
                 "Technical artist and game developer specialising in character rigging and "
                 "pipeline tool development for Maya, Unreal Engine and Unity. Assistant Professor "
                 "of Game Development at SUNY Morrisville.")
            + header("work") + body + footer())
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def render_sections(secs):
    out = []
    for s in secs:
        if s.get("heading"):
            out.append(f"<h2>{esc(s['heading'])}</h2>")
        for para in s.get("body", []):
            out.append(f"<p>{para}</p>")
        if s.get("list"):
            items = "".join(f"<li>{i}</li>" for i in s["list"])
            out.append(f"<ul>{items}</ul>")
    return "\n      ".join(out)


def render_figures(figs, depth=1):
    up = "../" * depth
    out = []
    for f in figs:
        cap = f'<figcaption>{esc(f["caption"])}</figcaption>' if f.get("caption") else ""
        out.append(f"""<figure>
        <img src="{up}{esc(f['src'])}" alt="{esc(f.get('caption',''))}" loading="lazy"
             onerror="this.outerHTML='&lt;div class=\\'ph\\'&gt;{esc(f['src'])}&lt;/div&gt;'">
        {cap}
      </figure>""")
    return "\n      ".join(out)


def build_project(p, prev_p, next_p):
    meta_rows = "".join(
        f"<div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in p.get("meta", {}).items())

    embed = video_block(p.get("embed", ""),
                        f'"embed" on {p["slug"]} in projects.json',
                        f'Video slot — {p["title"]}')

    pager = []
    if prev_p:
        pager.append(f'<a href="{esc(prev_p["slug"])}.html">'
                     f'<span class="label">Previous</span>{esc(prev_p["title"])}</a>')
    else:
        pager.append("<span></span>")
    if next_p:
        pager.append(f'<a href="{esc(next_p["slug"])}.html" style="text-align:right">'
                     f'<span class="label">Next</span>{esc(next_p["title"])}</a>')

    body = f"""
  <section class="proj-head">
    <div class="wrap">
      <a class="backlink" href="../index.html">&larr; All work</a>
      <h1>{esc(p['title'])}</h1>
      <p class="summary">{esc(p['summary'])}</p>
      <dl class="meta">{meta_rows}</dl>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      {embed}
      {render_figures(p.get('figures', []))}
      <div class="prose">
      {render_sections(p.get('sections', []))}
      </div>
      <div class="pager">{''.join(pager)}</div>
    </div>
  </section>
"""
    page = (head(f"{p['title']} — Minghao Zhou", p["summary"], depth=1)
            + header("work", depth=1) + body + footer(depth=1))
    (WORK / f"{p['slug']}.html").write_text(page, encoding="utf-8")


COURSES = [
    ("CITA 113", "Introduction to Game Design and Development", "GameMaker &middot; two sections",
     "The entry point to the game programming degree. I rebuilt the syllabus, lecture material "
     "and project briefs so that students ship several small complete games rather than one "
     "unfinished large one."),
    ("CITA 255", "Application Development", "C# and .NET MAUI",
     "Built from scratch. I replaced the previous platform with C# on .NET MAUI so students work "
     "in a front-end framework that is actually used in industry — and so that the language "
     "reinforces the Unity sequence most of them are already taking, rather than sitting apart "
     "from it."),
    ("CITA 386", "Game Interface Design", "Figma and Unity",
     "Redesigned from a Figma-only design exercise into a full pipeline, carrying students from "
     "interface design through to implementation inside a game engine. Designing a HUD and "
     "building it are different skills, and the gap between them is where student work usually "
     "falls down."),
]


def build_teaching():
    courses = "\n      ".join(
        f"""<div class="course">
        <div class="code">{code}</div>
        <h3>{esc(title)}</h3>
        <p class="tools">{tools}</p>
        <p>{body}</p>
      </div>""" for code, title, tools, body in COURSES)

    body = f"""
  <section class="proj-head">
    <div class="wrap">
      <p class="label">Teaching</p>
      <h1>Teaching</h1>
      <p class="summary">I am Assistant Professor of Game Development at SUNY Morrisville, in the
      Computer Information Technology department, teaching four sections across the game
      programming degree and to students from other computing majors.</p>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="two-col">
        <div>
          <div class="section-head"><h2>Courses</h2><span class="count">Fall 2026</span></div>
          {courses}

          <div class="prose" style="margin-top:46px">
            <h2>Approach</h2>
            <p>PLACEHOLDER — two or three paragraphs of teaching philosophy. Search committees
            read this page, and a specific account of how you run a studio course is worth more
            than general statements about student-centred learning. Draw on the curriculum
            reasoning above: you make decisions about what students learn based on how the
            pieces of a program fit together.</p>
          </div>
        </div>

        <aside class="sidecard">
          <h3>Previously</h3>
          <dl>
            <dt>Teaching Assistant</dt>
            <dd>Technical Character Animation; Advanced 3D Pipeline &mdash; Carnegie Mellon
            Entertainment Technology Center, 2024&ndash;2025.</dd>
            <dt>Guest lecture</dt>
            <dd>Authoring production tools in Maya with Python and MEL, Advanced 3D Pipeline.</dd>
            <dt>Workshop</dt>
            <dd>Penguin Action Toolkit workshop and game jam, Carnegie Mellon ETC, 2024.</dd>
          </dl>
          <p style="margin-top:20px"><a href="{CV_PATH}">Download full CV (PDF) &rarr;</a></p>
        </aside>
      </div>
    </div>
  </section>
"""
    page = (head("Teaching — Minghao Zhou",
                 "Courses taught in game development, interface design and application "
                 "development at SUNY Morrisville.")
            + header("teaching") + body + footer())
    (ROOT / "teaching.html").write_text(page, encoding="utf-8")


def build_about():
    body = f"""
  <section class="proj-head">
    <div class="wrap">
      <p class="label">About</p>
      <h1>About</h1>
    </div>
  </section>

  <section class="section" style="padding-top:0">
    <div class="wrap">
      <div class="two-col">
        <div class="prose">
          <p>I'm a technical artist and game developer working between character rigging,
          animation systems and pipeline tooling. Most of what I make is infrastructure: the
          rig an animator poses, the editor a designer authors behaviour in, the script that
          turns an hour of setup into one dialog.</p>

          <p>I'm currently Assistant Professor of Game Development at SUNY Morrisville, where I
          teach across the game programming degree. I also run Erosoft Studio, an independent
          studio where I'm building a character-driven puzzle game in Unreal Engine 5, and I
          consult for other studios on UE5 animation systems, Maya rigging, AI workflow
          integration and tool development.</p>

          <p>Before teaching I worked as a technical artist at Tencent, where I contributed to
          an in-house modular rigging system in Maya, and as a technical designer intern at
          Lilith Games on <em>Farlight 84</em>. I hold a Master of Entertainment Technology from
          Carnegie Mellon University and a BFA from the School of the Art Institute of Chicago,
          where I worked in art and technology and new media.</p>

          <p>PLACEHOLDER — add a closing paragraph in your own voice. What draws you to tool
          work specifically, or what you want students to take away. The three paragraphs above
          are factual; this one should sound like a person.</p>
        </div>

        <aside class="sidecard">
          <h3>Details</h3>
          <dl>
            <dt>Currently</dt>
            <dd>Assistant Professor of Game Development, SUNY Morrisville</dd>
            <dt>Studio</dt>
            <dd>Erosoft Studio &mdash; founder</dd>
            <dt>Education</dt>
            <dd>MET, Carnegie Mellon University, 2025<br>BFA, School of the Art Institute of
            Chicago, 2023</dd>
            <dt>Email</dt>
            <dd><a href="mailto:zhoumh.ariza@gmail.com">zhoumh.ariza@gmail.com</a></dd>
            <dt>Elsewhere</dt>
            <dd><a href="https://www.linkedin.com/in/minghaoz">LinkedIn</a><br>
                <a href="https://vimeo.com/user105794618">Vimeo</a><br>
                <a href="https://assetstore.unity.com/packages/templates/systems/penguin-arpg-toolkit-302387">Unity Asset Store</a></dd>
          </dl>
          <p style="margin-top:20px"><a href="{CV_PATH}">Download CV (PDF) &rarr;</a></p>
        </aside>
      </div>
    </div>
  </section>
"""
    page = (head("About — Minghao Zhou",
                 "Technical artist and game developer. Assistant Professor of Game Development "
                 "at SUNY Morrisville and founder of Erosoft Studio.")
            + header("about") + body + footer())
    (ROOT / "about.html").write_text(page, encoding="utf-8")


def main():
    if not DATA.exists():
        sys.exit(f"Missing {DATA}")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    WORK.mkdir(exist_ok=True)

    build_index(data)
    build_teaching()
    build_about()

    ps = data["projects"]
    for i, p in enumerate(ps):
        build_project(p, ps[i - 1] if i > 0 else None,
                      ps[i + 1] if i + 1 < len(ps) else None)

    print(f"Built index.html and {len(ps)} project pages in work/")


if __name__ == "__main__":
    main()
