# Research structure

The website has three main research directions, defined in `_data/research_areas.json`:

- RWE Generation: `/rwe-generation/`
- Predictive Modeling: `/predictive-modeling/`
- Clinical Pharmacology: `/clinical-pharmacology/`

The homepage, navigation, About page, research hubs and Publications page use this structure. Publications follow the user's `Publications/RWE`, `Publications/PM` and `Publications/CPP` folders. See `PUBLICATIONS.md` for metadata and PDF rules.

Causal Inference is a study collection within RWE Generation. The guide remains at `/causal-inference/` and all existing note URLs are retained. The causal-note layout shows the RWE breadcrumb; collection defaults also set `research_area: rwe-generation`.

Existing blog posts are Predictive Modeling learning notes. They retain their URLs, search entries and homepage pagination. The post default is `research_area: predictive-modeling`; explicitly override that field when a future post belongs to another direction. Learning notes are separate from authored publications.

Clinical Pharmacology learning content is TBD. Existing PDF publications are available independently; do not hide them because the learning collection is still forthcoming.

Research hubs use `_layouts/research-area.html`. The homepage overview uses `_includes/research-home.html`. Shared styling is in `assets/css/research-areas.css`; the existing mobile menu is used at widths up to 1240px to accommodate longer navigation labels.

This file is excluded from the generated website.
