# Podcast tagging + filter

Adds topic tags to every High-Impact Growth episode and a filter bar to the
`/podcast/` listing.

## Tag families
- **Product** (chip, teal): CommCare · SureAdhere · Connect · Open Chat Studio
- **Solutions** (chip, neutral) — from the CommCare pre-login IA:
  - Sector: Community Health, Mental Health, Infectious Disease, MNCH, Nutrition,
    Child Health, Livelihoods, Humanitarian Response
  - Use Case: Monitoring & Evaluation, Service Delivery, Cash & Voucher Assistance,
    Workforce Management, Sponsorship
  - Org Type (Who We Serve): Governments, International NGOs, US Community Health,
    Research & Academic
- **Theme** (chip, outline): AI · Global Development · Company & Culture · Leadership
- **Dimagi Staff** — filter facet only (`data-staff`), not a visible hero chip.

## Source of truth
`../podcast_tags.py` — the `TAGS` dict (keyed by episode number) plus the chip/filter/CSS/JS
emitters. **Edit tags there.** Both the generators and the post-process scripts import it,
so there is one place to change.

## Two ways the tags get onto the pages

### A. Generators (preferred, now tag-aware and reconciled)
`../build_episode.py` and `../build_listing.py` import `podcast_tags` and emit the chips,
card `data-*` attributes, filter bar, CSS, and combined reveal+filter JS directly.

**Regen recipe:**
```
# one or more episode pages:
python build_episode.py <slug> [<slug> ...]
python seo/inject_meta.py          # adds canonical/robots/og/twitter + absolute og:image

# the listing:
python build_listing.py            # clean no-op that preserves blurbs/guest lines/hosts + tags
```

`build_episode.py` emits the page minus the SEO `<head>` block; `seo/inject_meta.py` adds that
block (it always has — it is a required post-step, not new). Verified: `build_episode` output
differs from the live page ONLY by that SEO block (+ two cosmetic CSS comments on ep-83).
`build_listing.py` reproduces the live listing byte-for-byte.

Earlier drift that has been fixed: build_episode used stale `?v=11`/`?v=4` (now v=15/v=6);
build_listing dropped the "Featuring …" guest line and duplicated the "Meet the hosts" section
(now preserved / single).

### B. Post-process scripts (safe to run on the live pages today)
- `01_tag_episode_pages_and_cards.py` — inserts the `.ep-tags` chip row + CSS into each
  episode hero and `data-*` attributes onto each listing card. Idempotent.
- `02_listing_filter_bar.py` — injects the filter bar + CSS + empty state and swaps the
  reveal `<script>` for the combined filter+reveal controller. Idempotent.

These only add the tag layer; they do not touch blurbs, guest lines, versions, or the hosts
section, so they are non-destructive. Run them after anything that strips the tags.

## Filter behavior
6 rows (Product / Sector / Use Case / Org Type / Theme / Voices), single-select per row,
AND across rows. Lazy reveal stays for the unfiltered view; any active filter shows all
matches across both grids. Episode chips deep-link to `index.html?<facet>=<slug>`.
