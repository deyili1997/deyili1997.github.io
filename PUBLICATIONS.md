# Publications page

The English research portfolio lives at `/publication/` and uses the existing Jekyll / GitHub Pages setup. Only articles represented by PDFs in the author-provided `Tech_Blog/Publications/` folder belong on this page. The current collection contains nine articles.

- `_data/publications.json`: titles, authors, years, publication type, summaries, links, and feature selection. Featured papers appear in file order. All other main papers follow in file order.
- `_layouts/publications.html` and `_includes/publication-*.html`: page and reusable paper components.
- `assets/css/publications.css`: page-scoped responsive design.
- `assets/publications/papers/`: the nine author-supplied PDF files, unchanged.
- `assets/publications/figures/`: complete figures extracted from those PDFs. Preserve plotted content, attribution, and license links.

The page distinguishes journal articles, conference papers, and arXiv preprints. SMART uses the formal 2026 issue year (online August 2025). DeepJ uses the officially confirmed AMIA 2025 conference year; index providers disagree about its exact proceedings publication date, so the public page omits the day.

For new work, first require its PDF in `Tech_Blog/Publications/`, then add a data record with a verified title, author order, year, type, venue, and stable publisher/arXiv link. Only provide a local PDF or figure when the asset is available. Keep preprints explicitly labeled, and do not infer publication from a journal-formatted manuscript.

This maintenance file is excluded from the generated website.
