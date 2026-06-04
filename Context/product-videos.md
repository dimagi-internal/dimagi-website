# OUR PRODUCTS — homepage video embeds

The home page "Our Products" section has a 16:9 video slot above each card
(`.product-video` in index.html). Embeds are responsive iframes.

| Product    | Video | Host | Source | Status |
|------------|-------|------|--------|--------|
| Connect    | `eyDDRv-v1Bk` "CommCare Connect Demo: Pay for Outcomes, Not Effort" | YouTube | connect.dimagi.com | ✅ embedded |
| CommCare   | `o4y7gg9ssm` "CommCare INTRO VIDEO" | Wistia | dimagi.com homepage | ✅ embedded |
| SureAdhere | _none found_ | — | — | ⏳ needs link |

## How they were found
- `Context/Full Wordpress Export - June 3 2026.xml`: 78 items with YouTube videos, all CommCare/Dimagi-general — none were product overviews for Connect/SureAdhere.
- **Live dimagi.com homepage uses Wistia, not YouTube.** 9 Wistia videos, mostly partner stories (IRC, Save the Children, FCW, "Data Security", WellMe, Research webinar) + `o4y7gg9ssm` = "CommCare INTRO VIDEO".
- **connect.dimagi.com** has 2 YouTube (youtube-nocookie) embeds: `eyDDRv-v1Bk` (Connect demo ✅) and `VRbvUj9LTUg` ("Inside the Child Health Campaign in Kenya | Connect by Dimagi", a story video).
- **dimagi.com/sureadhere/** (and sureadhere.com, which redirects to it): same global Wistia set + `htl85vr750` = "SA header video_texture" (a 22-sec background loop, NOT an explainer). No SureAdhere product video available.

## Open
- **SureAdhere video needed.** No explainer found on dimagi.com / sureadhere.com. Provide a YouTube/Wistia link.
- CommCare is embedded as Wistia (matches the live site). If a YouTube version is preferred, supply the ID and swap.
