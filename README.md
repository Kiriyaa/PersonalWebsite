# minghaozhou.com

A static portfolio site. No build tools, no dependencies, no framework — plain HTML and CSS,
with a small Python script that generates the project pages so you never hand-edit them.

## Running it locally

```bash
cd site
python3 -m http.server 8000
```

Then open <http://localhost:8000>. That's it — there is nothing to install.

## Structure

```
index.html            generated — the work grid
about.html            generated
teaching.html         generated
work/*.html           generated — one page per project
css/style.css         hand-edited, the only stylesheet
images/               your images go here
MinghaoZhou_CV.pdf    linked from the nav and both content pages
_build/projects.json  ← the file you actually edit
_build/build.py       the generator
```

## Videos

There are two kinds of video slot, and both work the same way: paste an **embed** URL and the
player appears. Leave it empty and you get a labelled placeholder instead, so the layout never
looks broken while you're still editing.

- **Demo reel** — the `reel` object at the top of `projects.json`. Appears on the home page
  between the intro and the first group of work.
- **Per project** — the `embed` field on each project. Appears at the top of that project page,
  directly under the metadata.

Use the embed form of the URL, not the one from the address bar:

| Platform | Use this |
|---|---|
| YouTube | `https://www.youtube.com/embed/VIDEO_ID` |
| Vimeo | `https://player.vimeo.com/video/VIDEO_ID` |

For a YouTube link like `youtube.com/watch?v=Ch0Z9n4zCUY`, the ID is `Ch0Z9n4zCUY`. For Vimeo,
it's the number at the end of the URL. Pasting a plain watch URL will not play — the platforms
refuse to be framed that way.

The short note under the empty reel slot is a reminder to you and disappears automatically once
you fill the embed in, so it will never show on the live site.

## Adding or editing a project

Edit `_build/projects.json`, then run:

```bash
python3 _build/build.py
```

Every project is one object. The fields:

| Field | Purpose |
|---|---|
| `slug` | Filename — becomes `work/<slug>.html`. Lowercase, hyphens. |
| `group` | Which section of the home page: `tools`, `rigging`, `games`, `art`. |
| `title`, `role`, `year` | Shown on the card and the project page. |
| `tags` | Small mono labels on the card. Keep to three or four. |
| `summary` | One or two sentences under the title, and the page's meta description. |
| `meta` | The definition list under the summary. Values may contain HTML, so links work. |
| `sections` | Body content. Each has an optional `heading`, plus `body` (paragraphs) and/or `list`. |
| `figures` | Images shown on the project page. Can be empty. |
| `thumb` | Optional card thumbnail. Defaults to the first figure. |
| `embed` | Optional video embed URL (use the `/embed/` form for YouTube). |
| `no_video` | Set `true` on a project with no video, so it doesn't show the empty video slot. |
| `sections[].embeds` | Optional list of `{"url", "title"}` videos shown inside that section, for pages with several clips. |

To reorder the home page, reorder the `projects` array. To reorder or rename the sections,
edit `groups`.

## Images

Drop files into `images/` using the paths named in `projects.json`. Missing images degrade
gracefully — you get a labelled placeholder showing the expected filename rather than a broken
image icon, so you can add them one at a time.

Two things worth doing before you upload:

- Resize to about 1600px on the long edge. Full-resolution renders will make the site slow.
- Use `.jpg` for renders and photographs, `.png` for UI screenshots and anything with text.

## Still to write

Search `projects.json` and the generated pages for `PLACEHOLDER`. The ones that matter most:

1. **Project Good Boy** — the premise and the puzzle mechanic. Most visitors will open this first.
2. **Teaching → Approach** — your teaching philosophy. Search committees read this page.
3. **About** — a closing paragraph in your own voice.
4. **AI MetaHuman Pipeline** — relevant to the consulting side of Erosoft.
5. **Silt Symphony** — written as an artist statement, not a production breakdown.

The rigging pages also have placeholders where each individual rig should be introduced.

## Deploying to Cloudflare Pages

1. Sign in at <https://dash.cloudflare.com> and go to **Workers & Pages → Create → Pages**.
2. Choose **Upload assets**, name the project, and drag in the whole `site` folder.
3. It goes live at `<name>.pages.dev` within a minute or so.
4. Check that URL thoroughly before touching your domain.
5. Only then add `minghaozhou.com` under **Custom domains**, and follow the DNS instructions.
6. Cancel Wix last, once the new site is confirmed live on the real domain.

To update later, either drag in a new folder, or connect a Git repository so that pushing to
`main` redeploys automatically.

## Before it goes live

- [ ] Replace `MinghaoZhou_CV.pdf` whenever the CV changes
- [ ] Confirm every link in the footer works
- [ ] Check the site on a phone, not just a narrow browser window
- [ ] Set your title to whatever your appointment letter says — Game Development or Game Programming
- [ ] Remove the old `mzhou3@andrew.cmu.edu` address anywhere it still appears
