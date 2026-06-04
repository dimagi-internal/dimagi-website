export const meta = {
  name: 'dimagi-blog-import',
  description: 'Fetch dimagi.com blog posts, extract faithful content + cover, write per-post JSON records for central rendering',
  phases: [{ title: 'Extract', detail: 'one agent per source post: fetch, author body, download cover, write record JSON' }],
}

const ROOT = "/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login"

// args = [[slug, datehint], ...]
let _raw = args
if (typeof _raw === 'string') { try { _raw = JSON.parse(_raw) } catch (e) { _raw = [] } }
const ITEMS = Array.isArray(_raw) ? _raw : []

const SCHEMA = {
  type: "object",
  additionalProperties: false,
  properties: {
    slug: { type: "string" },
    status: { type: "string", enum: ["ok", "no_source", "error"] },
    category: { type: "string" },
    cover: { type: "string", description: "cover filename written, e.g. cover.jpg, or empty if fallback" },
    coverw: { type: "integer" },
    coverh: { type: "integer" },
    words: { type: "integer", description: "approx word count of authored body" },
    note: { type: "string", description: "one line: anything notable or problematic" },
  },
  required: ["slug", "status", "note"],
}

function prompt(slug, hint) {
  return `You are importing ONE dimagi.com blog post into a static site. Work faithfully and do not invent facts.

ROOT = "${ROOT}"
SOURCE = https://dimagi.com/${slug}/
SLUG = ${slug}
(Approx date hint from sitemap, NOT authoritative: ${hint})

## Step 1 — fetch the real source
Run: curl -sL -A "Mozilla/5.0" "https://dimagi.com/${slug}/" -o /tmp/blog_import/src/${slug}.html
Then Read that file. Pull from it: the real <title>, <meta name="description">, <meta property="og:image"> URL, <meta property="article:published_time"> (ISO date), author name, and the full article body text. If curl returns an error page / 404 / empty, return status "no_source" with a note and STOP (do not fabricate).

## Step 2 — download the cover image
mkdir -p "$ROOT/assets/images/${slug}"
Take the og:image URL and download it: curl -sL "<og:image>" -o "$ROOT/assets/images/${slug}/cover.<ext>" (choose ext jpg/png/webp from the URL or content-type).
Get dimensions: sips -g pixelWidth -g pixelHeight "<file>". If pixelWidth > 1300, downscale: sips -Z 1200 "<file>" and re-read dimensions.
Record the final filename (e.g. "cover.jpg") and final width/height.
If there is genuinely NO og:image, set "cover":"" and report it; the renderer will use a branded fallback.

## Step 3 — author the body as prose HTML (faithful to the source)
Rewrite the source article into clean prose HTML. Rules:
- First paragraph: <p class="lead">...</p>
- Section headings: <h2 id="short-kebab-id">Title</h2>  (use sentence case-ish, matching the source)
- Sub-headings: <h3>...</h3> ; paragraphs <p>...</p> ; bullet lists <ul><li>...</li></ul>
- For a standout statistic or result, optionally use ONE OR MORE callouts:
  <div class="article-callout"><div class="article-callout-label">LABEL</div><div class="article-callout-num">42%</div><p class="article-callout-text">explanation</p></div>
- At most ONE feature pull-quote, for the single strongest quote in the piece:
  <blockquote class="feature"><p>&ldquo;quote&rdquo;</p><cite>Name, Title</cite></blockquote>
  (regular inline quotes: <blockquote><p>...</p><cite>...</cite></blockquote>)
- External links: <a href="URL" target="_blank" rel="noopener">text</a>. Keep links that appear in the source (to dimagi.com pages, partners, reports). Do not invent URLs.
- Use HTML entities: &rsquo; &lsquo; &ldquo; &rdquo; &amp; and &ndash; for number ranges.
- ABSOLUTELY NO em dashes: never output the character "—" or "&mdash;". Recast with commas, colons, or "and".
- Do NOT include: the end CTA, the tags/"filed under" block, related posts, breadcrumbs, share buttons, social-follow lists, or "subscribe to our newsletter" boilerplate. Body = the article content only (lead paragraph through the final content paragraph).
- Indent each top-level body element with 8 spaces.
- Be faithful: use only facts, names, numbers, and quotes present in the source. If the source is short, write a shorter page. Aim to preserve the substance of the original.

## Step 4 — pick a category (controlled vocabulary, choose exactly ONE)
CommCare | Connect | SureAdhere | AI for Good | Global Health | Community Health | Maternal &amp; Child Health | Events | Research | Company
Guidance: Events = summits/forums/conferences/webinars. Research = research grants/studies/evaluations/academic work. Company = culture/strategy/awards/anniversaries/climate/B-Corp/hiring/"innovation at Dimagi" series. AI for Good = AI/ML/chatbots. Connect = CommCare Connect. SureAdhere = TB/adherence. Maternal &amp; Child Health = MCH/nutrition/child health (write it EXACTLY as "Maternal &amp; Child Health"). Community Health = CHW/community health systems. Global Health = general global health/COVID/partnerships. CommCare = product features or case studies primarily about the CommCare platform.

## Step 5 — write the record JSON
Write the file /tmp/blog_import/${slug}.json containing EXACTLY these keys (a single JSON object):
{
  "slug": "${slug}",
  "h1": "Article Title (entities ok, no trailing | Dimagi)",
  "titletag": "Short Title | Dimagi",
  "ogtitle": "Article Title",
  "desc": "1-2 sentence meta description from/faithful to the source.",
  "deck": "A one-sentence hero deck (can mirror desc).",
  "date": "YYYY-MM-DD",            // real publish date from article:published_time
  "datelabel": "Mon YYYY",         // e.g. "Nov 2024"
  "author": "Author Name",         // real author; if none, "Dimagi"
  "initials": "AB",                // 1-2 letters from author; "D" if Dimagi
  "category": "<one of the controlled vocab>",
  "crumb": "<same as category>",
  "readtime": "N min read",        // ~200 words/min
  "cover": "cover.jpg",            // filename you saved (or "" for fallback)
  "coverw": 1200, "coverh": 750,   // final cover dims
  "coveralt": "descriptive alt text for the cover",
  "covercaption": "one short caption shown under the cover",
  "ogimage": "https://dimagi.com/.../the-og-image.jpg",  // absolute source URL
  "ogw": 1200, "ogh": 750,         // og image dims (use source values or your cover dims)
  "ogalt": "alt text for social image",
  "keywords": "comma, separated, keywords",
  "body": "<the prose HTML from Step 3 as a single string>",
  "toc": [["section-id","Short label"], ...],   // one per h2; renderer shows it only if 3+
  "tags": ["Tag One","Tag Two"],   // 2-4 short tags
  "cta": { "h3": "CTA heading", "p": "one sentence", "btntext": "Get in touch", "btnhref": "../../contact/index.html" }
}
Defaults: CTA usually links to ../../contact/index.html with "Get in touch". For a clearly product-focused post you may link the product (https://dimagi.com/commcare/ , https://connect.dimagi.com/ , https://dimagi.com/sureadhere/) with target via absolute URL.

Before writing, double-check the body string contains NO "—" and NO "&mdash;".

Finally return the status object. Set status "ok" when the JSON file is written and the cover downloaded (or fallback noted).`
}

const results = await parallel(ITEMS.map(([slug, hint]) => () =>
  agent(prompt(slug, hint), { label: `import:${slug}`, phase: 'Extract', schema: SCHEMA })
))

const ok = results.filter(r => r && r.status === 'ok')
const bad = results.filter(r => !r || r.status !== 'ok')
log(`done: ${ok.length} ok, ${bad.length} needing attention`)
return { ok: ok.length, total: ITEMS.length, problems: bad }
