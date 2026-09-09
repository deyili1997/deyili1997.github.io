# Causal inference notes

The English causal inference collection extends the existing Norlin Jekyll site.

- Public entry: `/causal-inference/` (`_pages/causal-inference.md`).
- Articles: `_causal_inference/<stable-slug>.md`.
- Reading order: front-matter `order`, `previous_note`, and `next_note`.
- Navigation: `_data/settings.yml`; search and tag archives include the collection.
- Layouts: `_layouts/causal-note.html` and `_layouts/causal-guide.html`.
- Rendering: `assets/css/causal-notes.css`, `js/causal-notes.js`, and the conditional MathJax loader in `_includes/head.html`.
- Figures and the reproducible synthetic example: `assets/causal-inference/`.
- Source correspondence and SHA-256 fingerprints: `_data/causal_sources.json`.

## Updating a note

Translate the full updated source, retaining examples, formulas, references, caveats, and self-checks. Keep stable article URLs and existing section anchors where possible, then update the guide, reading sequence, and section table of contents together. Use English links and standard Markdown/HTML; Obsidian wiki links and callout markers must be converted before publishing. Do not publish local filesystem links.

Kramdown uses double-dollar delimiters for inline mathematics and separate double-dollar blocks for display mathematics. It emits MathJax delimiters. Mermaid diagrams use `<pre class="mermaid">`. Callouts use an aside with `markdown="1"`; optional details use a summary and `markdown="1"`.

## Verification and publishing

Use a compatible Ruby with the existing Gemfile, then run `bundle exec jekyll build`. Check article and guide links, fragment anchors, search/tag results, formula rendering, diagrams, images, and narrow-screen tables. Source notes are study material; reported research findings and invented teaching examples must remain distinguishable.

The existing GitHub Pages site publishes the `main` branch from its root. Publish only the intended site changes and confirm the Pages build and public URLs afterward.
