# Site generator source

`build.py` writes the whole site (pages, style.css, sitemap, share cards) into `site/`. To rebuild, run it from a folder that holds this repo checked out as `site/`, with copies of `entries.json`, `shops.json` and `tips.py` next to `build.py`:

    python3 build.py

Needs Python 3, Pillow and Playwright (Chromium) for the share cards.

- `entries.json`: the build entries. Internal file-path source fields were removed from this copy. They are not shown on the site.
- `tips.py`: the tips on tips.html, credited to the Grok Bot that learned each one.
- `shops.json`: the shops list.
- Tip images are already resized in `tips/img/`. build.py only reads the originals when a resized copy is missing.
