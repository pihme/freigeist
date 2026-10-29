# Freigeist

A blog bringing together my open-source projects: notes, devlogs and making-ofs.

Design notes: [docs/design.md](docs/design.md)  

## Layout

```
posts/        one Markdown file per post
pages/        static pages (about.md)
theme/        HTML shell, hero SVGs, CSS, fonts, background tiles
assets/       logo mark, reference images, post images (assets/posts/<slug>/)
build.py      static site builder (Python 3.8+, no dependencies)
site/         build output (git-ignored)
```

## Writing a post

1. Create `posts/YYYY-MM-DD-short-slug.md`. The slug in the URL is the file name without the date.
2. Start the file with front matter:

   ```yaml
   ---
   title: "Introducing hermetarium"
   date: 2026-11-02
   type: essay          # essay | devlog | note  (notes also appear on notes.html)
   project: hermetarium # groups the post on projects.html
   tags: [launch, hermetarium]
   summary: "One or two sentences shown on the cards and in the list."
   draft: true          # drafts are skipped unless you build with --drafts
   ai_generated: true   # optional: marks the post as AI-generated (helper bot + tooltip)
   ---
   ```

3. Write Markdown. Supported: headings, paragraphs, **bold**, *italic*, `code`, fenced code blocks, links, images, lists, blockquotes and `---` rules.
4. Put images in `assets/posts/<slug>/` and link them as `../assets/posts/<slug>/file.png`.
5. When a post is ready, remove `draft: true`.

The files in `posts/` called `*template*` are **examples only**. Their content is placeholder text, not real project facts. Copy one, rewrite it, and delete the templates before going live.

## Build and test locally

```bash
python3 build.py --drafts --serve   # build including drafts, open http://localhost:8000
python3 build.py                    # build published posts only into ./site
```

`site/index.html` also opens directly from disk. The accent pair is random on each load; force one with `?accent=cobalt` (or acid-green, signal-orange, hot-magenta, warning-red, safety-yellow).

## Licences

Everything in this repository is licensed under [Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0)](https://creativecommons.org/licenses/by-nd/4.0/); see `LICENSE`. That covers the written content (`posts/`, `pages/` and the images published with them) and the site generator (`build.py`, `theme/`).

The fonts in `theme/fonts/` (Cormorant Garamond, IBM Plex Mono and Unbounded) are under the SIL Open Font License 1.1.
