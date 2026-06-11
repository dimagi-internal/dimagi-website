# dimagi.com migration — old → new disposition / redirect map

_Last updated: 2026-06-11. Source of truth for what happened to each legacy
dimagi.com URL that did **not** carry its slug straight over. Decisions made
with Gillian. Implement the cross-domain 301s at the apex once the final
dimagi.com / commcarehq.org routing is wired (the domain split is still parked)._

## Legend
- **Dimagi** = new static dimagi.com site (this repo, GitHub Pages today).
- **CommCare** = commcarehq.org Astro site (`Pre-Login Websites/CommCare Pre-Login`).
- **SureAdhere** = SureAdhere static site.

## Rebuilt / has a home

| Old URL | New home | Status |
|---|---|---|
| `/careers/faqs/` | Dimagi `/company/careers/faqs/` | ✅ Rebuilt 2026-06-11 (questions recovered from live page; answers from WP export). Careers-page link repointed internally. |
| `/person/<slug>/` (×11 leadership) | Dimagi `/company/about/<slug>/` | ✅ Rebuilt 2026-06-11 via `Context/build_bios.py` (slugs preserved). About-page names link internally; old `/person/<slug>/` URLs are meta-refresh 301 stubs → the new pages. |
| `/commcare-powering-resilience/` | CommCare `/resources/powering-resilience/` | ✅ Rebuilt 2026-06-11 as an **unlinked** campaign landing page (`src/pages/resources/powering-resilience/index.astro`, noindex; not in nav/footer/Resources index/sitemap). 301 in CommCare `public/_redirects`. (Briefly built as a Dimagi blog post first, then moved here per Gillian.) |
| `/gdhf-22/` | Dimagi `/blog/global-digital-health-forum-2022/` | ✅ Redirect stub at Dimagi `/gdhf-22/` (meta-refresh; GitHub Pages has no server 301). |
| `/resource-hub/` | Dimagi `/blog/` | ✅ 2026-06-11 meta-refresh stub at Dimagi `/resource-hub/` → `/blog/`. It was a content-discovery hub linking to blog/podcast/guides — folded into the blog. |
| `/sectors/gender-based-violence/` | CommCare `/solutions/sectors/maternal-newborn-health/` | ✅ 301 in CommCare `public/_redirects`. GBV content folded into maternal/newborn health. (The MNCH sector page was later split into separate Child Health + Maternal & Newborn Health pages; GBV points to the latter.) |
| `/commcare-onboarding/` | CommCare `/support/customer-success/` | ✅ 301 in CommCare `public/_redirects`. |
| `/survey-tool-alternative/` (Competitor Comparison) | CommCare transition guides: `/transition-guide/` + `/transition-guide/{surveycto,kobotoolbox,ona,opensrp,taroworks}/` | Note only (Gillian: "those now go to the new links"). No general comparison landing; per-tool guides replace it. Add a 301 from `/survey-tool-alternative/` → `/transition-guide/` at apex. |

## Earlier consolidations (already live, still need apex 301s)

| Old URL | New home |
|---|---|
| `/commcare/` | CommCare `/platform/` (301 already in CommCare `_redirects` for `/product/*`) |
| `/services/` | Dimagi `/professional-services/` |
| `/us-health/` | Dimagi `/professional-services/united-states/` |
| `/india/` | Dimagi `/professional-services/india/` |
| `/impact-delivery/` | Folded into Dimagi `/company/our-approach/` + `/professional-services/global-services/` |
| `/resources/mobile-data-collection/` | CommCare `/resources/data-collection-guide/` |
| `/terms-privacy/` + `/terms-privacy-dimagi/` | Dimagi `/legal/privacy-policy/` (consolidated) |
| `/sectors/financial-inclusion/`, `/sectors/small-business/` | CommCare `/solutions/sectors/livelihoods/` |
| `/sectors/programmatic-research/` | CommCare `/solutions/use-cases/research/` |
| `/sectors/vaccine-delivery/` | CommCare `/solutions/sectors/immunizations/` |
| `/commcare-providers/` + `/commcare-provider/<slug>/` (×27) + `/cc-premier-provider-*/` | CommCare `/support/implementers/` (directory; all 27 orgs preserved in `providers.js`) |
| Case studies `/case-study/<slug>/` (×21 of 23) | Dimagi `/blog/<slug>/` (rebuilt as dated blog posts) |

## Intentionally dropped (no migration)

| Old URL | Reason |
|---|---|
| `/proposals/` ("Dimagi for Your Consortium") | Gillian 2026-06-11: drop it. No redirect. |
| `/case-study/deploying-motech-suite-for-mnch-nutrition-programs-in-10-countries/` | MOTECH is legacy; Gillian: OK to drop. |
| `/case-study/motech-suite-for-continuum-of-care-services-in-india/` | MOTECH is legacy; Gillian: OK to drop. |
| `/case-study/malaria-consortium-upscale-program/` | Consolidated into `/blog/malaria-consortium-upscale-iccm-child-health/` (DHIS2 angle covered there). |
| `/sample-page/` | WordPress default stub. |

## Open / pending decision

| Old URL | What it is | Status |
|---|---|---|
| `/webinar/data-democracy/` | "Data Democracy" webinar (single). | DECIDED target = `/webinars/`, but BLOCKED: `/webinars/` itself has no new home yet (build a page / redirect to `/blog/` / leave as-is). Stub NOT built (would 404). Gillian coming back to it. |
| `/webinars/` | Webinars listing (was a dynamic list; empty in the static export). | OPEN — its destination drives the data-democracy redirect above. |
