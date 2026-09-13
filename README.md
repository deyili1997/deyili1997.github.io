# Deyi Li

Personal academic website: https://deyili1997.github.io/

The site uses semantic HTML, a small shared stylesheet, and Jekyll to publish Markdown notes. Pages use system serif fonts and ordinary text links. There are no theme bundles, external fonts, decorative covers, or animation libraries. JavaScript is limited to note search, legacy tag navigation, responsive tables, mathematical typesetting, diagrams, and legacy redirects.

## Build

With a Ruby version compatible with the Gemfile:

```sh
bundle install
bundle exec jekyll build
bundle exec jekyll serve
```

GitHub Pages publishes the root of `main`. Preserve existing routes and scientific content when updating the site.

## Structure

- `index.html`: academic homepage.
- `_data/settings.yml`: identity, contact links, and navigation.
- `_layouts/` and `_includes/`: semantic document layouts.
- `assets/css/site.css`: shared typography and responsive document styles.
- `_data/publications.json`: publication metadata; see `PUBLICATIONS.md`.
- `_data/research_areas.json`: subject directories; see `RESEARCH_AREAS.md`.
- `_causal_inference/`: study notes; see `CAUSAL_NOTES.md`.
- `_posts/`: learning notes with stable article URLs.
- `assets/`: scientific figures, publication PDFs, and examples.

Before publishing, build the site and check links, figures, formulas, search, and mobile reading. Public copy should use formal names and direct descriptions, without authoring instructions or redundant language labels.
