# Publications page

The English research portfolio lives at `/publication/` and uses the existing Jekyll / GitHub Pages setup. Only articles represented by PDFs in the author-provided `Tech_Blog/Publications/` folder belong on this page.

## Categories follow the source folders

| Source folder | Website section | Current PDFs |
| --- | --- | --- |
| `RWE/` | RWE Generation | 1 |
| `PM/` | Healthcare AI | 7 |
| `CPP/` | Clinical Pharmacology | 2 |

The `PM/` source folder maps to Healthcare AI (`research_area: healthcare-ai`). Preserve formal paper titles, even when they contain the phrase “predictive modeling.”

`_data/research_areas.json` defines the topic names, route URLs, folder mapping and descriptions. Only topics without `show_publications: false` appear as publication sections; Investment Notes is excluded. Omics is also excluded until the user supplies classified Omics PDF articles. `_data/publications.json` stores the publication records. Every record requires `research_area`, a folder-relative `source_file` such as `PM/2608.21712v2.pdf`, and a `source_sha256` matching the supplied PDF. Category membership must follow the user-assigned folder, without inferring a different category from the article title.

- `_layouts/publications.html`: groups articles into the three research areas.
- `_includes/publication-feature.html`, `publication-row.html`, and the other `publication-*.html` includes: reusable paper displays.
- `assets/css/publications.css` and `assets/css/research-areas.css`: page design and shared research-area styles.
- `assets/publications/papers/`: the ten supplied PDFs, unchanged.
- `assets/publications/figures/`: complete figures extracted from supplied PDFs. Preserve plotted content, attribution and license links.

The page distinguishes journal articles, conference papers and arXiv preprints. SMART uses the formal 2026 issue year (online August 2025). DeepJ uses the officially confirmed AMIA 2025 conference year; index providers disagree about its exact proceedings publication date, so the public page omits the day. The tacrolimus article lists De-Yi Li third; equal-contribution credit belongs to Ling Li and Min Zhu.

Clinical Pharmacology learning material is marked TBD on its topic page. Its two existing publications remain visible under Clinical Pharmacology.

For new work, first require its PDF in one of the three source folders, then add verified title, author order, year, publication type, venue and stable publisher/arXiv link. Preserve existing article IDs and public PDF URLs when recategorizing. Never reintroduce historical publication-list entries without a corresponding source PDF.

This maintenance file is excluded from the generated website.
