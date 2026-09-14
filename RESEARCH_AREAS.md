# Research and learning structure

The website has four peer topics, defined in `_data/research_areas.json`:

- Real-World Evidence: `/real-world-evidence/`
- Healthcare AI: `/healthcare-ai/`
- Clinical Pharmacology: `/clinical-pharmacology/`
- Investment: `/investment/`

The homepage, navigation and About page expose all four topics. Investment is a personal learning journal on U.S. equities, rather than an academic publication category. Its `show_publications: false` flag hides publication links and excludes it from the Publications page. The three academic publication groups still follow the user's `Publications/RWE`, `Publications/PM` and `Publications/CPP` folders. See `PUBLICATIONS.md` for metadata and PDF rules.

Real-World Evidence uses `real-world-evidence` as its internal topic ID and `/real-world-evidence/` as its canonical hub. The former `/rwe-generation/` hub redirects to it, and `/publication/#rwe-generation` remains an anchor alias for `/publication/#real-world-evidence`. The source publication folder remains `Publications/RWE/` and maps to Real-World Evidence.

Healthcare AI uses `healthcare-ai` as its internal topic ID and `/healthcare-ai/` as its canonical hub. The former `/predictive-modeling/` hub redirects to it, and `/publication/#predictive-modeling` remains an anchor alias for `/publication/#healthcare-ai`. Original paper titles and post URLs are retained. The source publication folder remains `Publications/PM/` and maps to Healthcare AI.

Causal Inference is a study collection within Real-World Evidence. The RWE hub shows every foundation note directly under `#area-learning-title`, without pagination or collapsed groups. `_data/rwe_learning.json` defines five consecutive learning stages; `start` is inclusive and `end` is exclusive, with the last stage open-ended. Keep boundaries contiguous when extending the route. Notes are sorted numerically by `order`; displayed labels preserve companion steps such as 14.1 and 14.2. The guide remains at `/causal-inference/` as an additional reading aid and all existing note URLs are retained. Note breadcrumbs return to the RWE directory.

The RWE hub puts foundations and paper readings side by side on wide screens and stacks them on smaller screens. On-page links provide direct access to either section. Individual articles retain the site's narrower reading width. Homepage links and counts are generated from the two collections.

### Adding an RWE paper reading

Add a dated Markdown file in `_posts/` with `layout: post`, `title`, `description`, and `research_area: real-world-evidence`. It automatically appears under `#area-paper-notes-title`, in site search, and in the archive; no manual directory edit is needed. Use `math: true` for MathJax and an explicit permalink under `/rwe/`. Source figures belong in `assets/rwe/` with attribution and links to the original article.

For paper-note titles, prefix the title with `(publication year journal/conference)` using the source's verified publication year and venue, for example `(2026 Nature Medicine) COMPASS: ...`. Concept notes without a specific source paper need no venue prefix.

Optional metadata enriches the directory and connects the paper to foundational study notes:

```yaml
paper_year: 2026
paper_venue: Nature Communications
reading_focus: "A short explanation of the methodological question this reading answers."
rwe_topics: [Propensity scores, Survival analysis]
foundation_notes: [inverse-probability-weighting, weighted-survival-analysis]
```

- `paper_year` is the original paper's publication year; `date` is when the reading note was added. Keep them separate.
- `reading_focus` falls back to `description`. Aim for one useful sentence rather than repeating the full paper title.
- Reuse existing `rwe_topics` when appropriate. These topics appear as descriptive labels in the directory and are separate from site-wide `tags`.
- `foundation_notes` contains collection filename slugs without `.md`. Links appear in the directory and at the top of the reading. Choose the two or three foundations most useful for understanding the paper.
- A post without optional metadata still appears. Paper readings are ordered automatically by note-added `date`, newest first; `paper_year` is displayed as source metadata and does not control ordering.
- All foundation notes and paper readings remain visible on screen and in print. The RWE directory has no local search, filter, sort, or reset controls and requires no directory JavaScript. The global site Search remains available.
- Article Previous/Next links remain within the current research area.

The static directory is rendered by `_includes/rwe-learning.html`, with optional foundation links shared through `_includes/rwe-foundation-links.html`. Inclusion, counts, and note-date ordering update automatically; there is no fixed count or hardcoded paper reading sequence to maintain.

Existing blog posts are Healthcare AI learning notes. They retain their URLs, search entries and the legacy paginated archive. The post default is `research_area: healthcare-ai`; explicitly override that field when a future post belongs to another topic. Learning notes are separate from authored publications.

Investment uses `investment` as its internal topic ID and `/investment/` as its canonical hub. The former `/investment-notes/` hub redirects to it.

For an investment learning entry, add a normal `_posts/YYYY-MM-DD-slug.md` with `layout: post`, a title and description, and `research_area: investment`. It will appear in the Investment hub, the legacy paginated archive and site search, and its breadcrumb will link back to the investment hub. Do not invent investment entries or import notes until the user supplies the source. Until the first entry exists, the Investment hub shows TBD.

Clinical Pharmacology learning content remains TBD. Existing PDF publications are available independently; do not hide them because the learning collection is still forthcoming.

Topic hubs use `_layouts/research-area.html`. The homepage overview and topic hubs use plain headings, paragraphs and lists. Shared typography is in `assets/css/site.css`; there are no topic cards, decorative images or mobile menu controls. The same text navigation wraps naturally on narrow screens.

This file is excluded from the generated website.
