# Causal inference notes

The causal inference collection extends the existing Norlin Jekyll site.

- Public entry: `/causal-inference/` (`_pages/causal-inference.md`).
- Articles: `_causal_inference/<stable-slug>.md`.
- Reading order: front-matter `order`, `previous_note`, and `next_note`. Companion notes may use `reading_label` to share a step in the guide without renumbering the main learning route.
- Navigation: `_data/settings.yml`; search and tag archives include the collection.
- Layouts: `_layouts/causal-note.html` and `_layouts/causal-guide.html`.
- Rendering: `assets/css/causal-notes.css`, `js/causal-notes.js`, and the conditional MathJax loader in `_includes/head.html`.
- Figures and the reproducible synthetic example: `assets/causal-inference/`.
- Source correspondence and SHA-256 fingerprints: `_data/causal_sources.json`.
- Source heading to stable section-anchor mapping: `_data/causal_source_headings.json`. Keep these mappings current when adding or translating sections.

## Updating a note

Translate the full updated source, retaining examples, formulas, references, caveats, and self-checks. Keep stable article URLs and existing section anchors where possible, then update the guide, reading sequence, and section table of contents together. Use site-relative links and standard Markdown/HTML; Obsidian wiki links and callout markers must be converted before publishing. Do not publish local filesystem links.

Kramdown uses double-dollar delimiters for inline mathematics and separate double-dollar blocks for display mathematics. It emits MathJax delimiters. Mermaid diagrams use `<pre class="mermaid">`. Callouts use an aside with `markdown="1"`; optional details use a summary and `markdown="1"`.

## Publication copy

Public-facing copy should describe the subject directly. Keep redundant language labels, conversational context, drafting reminders, and authoring instructions out of titles, descriptions, navigation, and article text. Identify verbatim quotations as source excerpts and rewritten passages as summaries or paraphrases. Retain citations, scientific qualifications, and the distinction between reported findings and illustrative examples. Keep source filenames, heading mappings, and provenance in internal data and maintenance files.

## Maintaining the study guide

**Keep one continuous reading route when adding material**

1. Identify the question answered and prerequisite concepts, then place the material appropriately in §1 rather than merely appending a link.
2. Revise the preceding step’s transition, the new step’s reading range and self-check objective, and the following step’s connection to maintain continuity.
3. Keep one numbering sequence for the first pass. When order changes, update the map, step references, and topic count together.
4. Place detailed derivations, narrow topics, and close source interpretations on the second pass or as supplements to relevant steps. Do not create a competing main route. G-estimation currently belongs on the second pass.
5. Add common questions to §3 and case-spanning additions to §4. These support reference and consolidation; §1 remains the first-pass entry point.
6. Explain every variable, parameter, subscript, superscript, operator, value, and unit alongside a new formula. Identify whether it is a definition, assumption, model, or estimation formula. Pair important formulas with a plain-language reading and checkable example, including inside expandable sections.
7. Develop technical sections as: concrete question → why the preceding step is insufficient → why the next step helps → calculation with the same example → corresponding formula → interpretation and conditions. Explain the purpose of every operation and symbol, link missing prerequisites, and reserve advanced derivations for the second pass. A glossary alone does not repair missing logical steps in the main text.
8. Update dates and check scientific accuracy, numbers, sources, links, and anchors. Mark unfinished topics explicitly; do not use empty links as though the notes already exist.

The former public maintenance section is retained only as the empty `section-53` anchor for existing links; its instructions belong here.

## Verification and publishing

Use a compatible Ruby with the existing Gemfile, then run `bundle exec jekyll build`. Check article and guide links, fragment anchors, search/tag results, formula rendering, diagrams, images, and narrow-screen tables. Source notes are study material; reported research findings and invented teaching examples must remain distinguishable.

The existing GitHub Pages site publishes the `main` branch from its root. Publish only the intended site changes and confirm the Pages build and public URLs afterward.
