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
- **Dimagi Staff** — still tagged on cards (`data-staff`) but NO longer a filter facet
  (the listing dropdowns dropped the old "Voices / Dimagi Staff" row).

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

## Filter behavior (blog-style, redesigned 2026-06-09)
The listing filter mirrors the `/blog/` filter bar: a **search box** + two rounded
**dropdowns**, single-select each, AND across them (and AND with search):

- **Product** — CommCare / Connect / SureAdhere / Open Chat Studio  (`data-product`)
- **Focus** — grouped *Sectors* (`data-sector`) + *Use cases* (`data-usecase`) + a *Themes*
  group folded in from the old standalone Theme dropdown, limited to six: AI / Global
  Development / Company & Culture / Leadership (`data-theme`) + Governments / United States
  (`data-orgtype`, where `us-community-health` is now labeled "United States"). Each option
  carries `data-dim` so the one dropdown spans several card attributes. The old **Theme**
  dropdown was removed (2026-06-09); International NGOs / Research & Academic are still on
  cards but no longer offered as filter options.

Search matches episode title + number + blurb. Accent is podcast maroon `#9A2C23` (not the
blog indigo). Lazy reveal stays for the unfiltered view; when any filter/search is active the
controller relocates every "more" episode up into the single archive grid (and hides the now
-empty `.more-section`) so all matches render in one continuous 3-col grid, instead of two
separate grids meeting at a ragged half-empty row. On clear they return to `#more-grid` for
the lazy-reveal list. State is URL-synced and episode hero chips still deep-link to
`index.html?<dim>=<slug>` (`product`/`sector`/`usecase`/`theme`/`orgtype`), which the
dropdowns resolve on load. The old "Voices / Dimagi Staff" row was removed.

Markup/CSS/JS all come from `../podcast_tags.py` (`filter_bar_html` / `FILTER_CSS` /
`COMBINED_JS`); `02_listing_filter_bar.py` now imports those and *upgrades* an older
chip-row bar in place, so re-running it after a stale regen restores this design.
