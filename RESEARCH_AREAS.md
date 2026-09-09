# Research and learning structure

The website has five peer topics, defined in `_data/research_areas.json`:

- RWE Generation: `/rwe-generation/`
- Predictive Modeling: `/predictive-modeling/`
- Clinical Pharmacology: `/clinical-pharmacology/`
- Omics: `/omics/` (TBD)
- Investment Notes: `/investment-notes/`

The homepage, navigation and About page expose all five topics. Investment Notes is a personal learning journal on U.S. equities, rather than an academic publication category. Its `show_publications: false` flag hides publication links/panels and excludes it from the Publications page. The three academic publication groups still follow the user's `Publications/RWE`, `Publications/PM` and `Publications/CPP` folders. See `PUBLICATIONS.md` for metadata and PDF rules.

Causal Inference is a study collection within RWE Generation. The guide remains at `/causal-inference/` and all existing note URLs are retained. The causal-note layout shows the RWE breadcrumb; collection defaults also set `research_area: rwe-generation`.

Existing blog posts are Predictive Modeling learning notes. They retain their URLs, search entries and homepage pagination. The post default is `research_area: predictive-modeling`; explicitly override that field when a future post belongs to another topic. Learning notes are separate from authored publications.

For an investment learning entry, add a normal `_posts/YYYY-MM-DD-slug.md` with `layout: post`, a title and description, and `research_area: investment-notes`. It will appear in the Investment Notes hub, homepage pagination and site search, and its breadcrumb will link back to the investment hub. Do not invent investment entries or import notes until the user supplies the source. Until the first entry exists, the homepage and hub show TBD automatically.

Omics is a research direction with content marked TBD. Its `show_publications: false` flag suppresses empty publication links and panels until the user supplies Omics PDF articles and their classification. Do not infer an Omics paper category from existing article titles.

Clinical Pharmacology learning content remains TBD. Existing PDF publications are available independently; do not hide them because the learning collection is still forthcoming.

Topic hubs use `_layouts/research-area.html`. The homepage overview uses `_includes/research-home.html`. Shared styling is in `assets/css/research-areas.css`; the five homepage cards use three columns with a centered second row on wide screens, two columns at widths up to 1120px, and one at widths up to 760px. The mobile menu is used at widths up to 1360px to accommodate all navigation labels.

This file is excluded from the generated website.
