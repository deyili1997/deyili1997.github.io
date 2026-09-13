# Research and learning structure

The website has four peer topics, defined in `_data/research_areas.json`:

- Real-World Evidence: `/real-world-evidence/`
- Healthcare AI: `/healthcare-ai/`
- Clinical Pharmacology: `/clinical-pharmacology/`
- Investment: `/investment/`

The homepage, navigation and About page expose all four topics. Investment is a personal learning journal on U.S. equities, rather than an academic publication category. Its `show_publications: false` flag hides publication links/panels and excludes it from the Publications page. The three academic publication groups still follow the user's `Publications/RWE`, `Publications/PM` and `Publications/CPP` folders. See `PUBLICATIONS.md` for metadata and PDF rules.

Real-World Evidence uses `real-world-evidence` as its internal topic ID and `/real-world-evidence/` as its canonical hub. The former `/rwe-generation/` hub redirects to it, and `/publication/#rwe-generation` remains an anchor alias for `/publication/#real-world-evidence`. The source publication folder remains `Publications/RWE/` and maps to Real-World Evidence.

Healthcare AI uses `healthcare-ai` as its internal topic ID and `/healthcare-ai/` as its canonical hub. The former `/predictive-modeling/` hub redirects to it, and `/publication/#predictive-modeling` remains an anchor alias for `/publication/#healthcare-ai`. Original paper titles and post URLs are retained. The source publication folder remains `Publications/PM/` and maps to Healthcare AI.

Causal Inference is a study collection within Real-World Evidence. The guide remains at `/causal-inference/` and all existing note URLs are retained. The causal-note layout shows the Real-World Evidence breadcrumb; collection defaults also set `research_area: real-world-evidence`.

Existing blog posts are Healthcare AI learning notes. They retain their URLs, search entries and homepage pagination. The post default is `research_area: healthcare-ai`; explicitly override that field when a future post belongs to another topic. Learning notes are separate from authored publications.

Investment uses `investment` as its internal topic ID and `/investment/` as its canonical hub. The former `/investment-notes/` hub redirects to it.

For an investment learning entry, add a normal `_posts/YYYY-MM-DD-slug.md` with `layout: post`, a title and description, and `research_area: investment`. It will appear in the Investment hub, homepage pagination and site search, and its breadcrumb will link back to the investment hub. Do not invent investment entries or import notes until the user supplies the source. Until the first entry exists, the homepage and hub show TBD automatically.

Clinical Pharmacology learning content remains TBD. Existing PDF publications are available independently; do not hide them because the learning collection is still forthcoming.

Topic hubs use `_layouts/research-area.html`. The homepage overview uses `_includes/research-home.html`. Shared styling is in `assets/css/research-areas.css`; the four homepage cards use two columns on wide screens and one at widths up to 760px. The mobile menu is used at widths up to 1360px to accommodate all navigation labels.

This file is excluded from the generated website.
