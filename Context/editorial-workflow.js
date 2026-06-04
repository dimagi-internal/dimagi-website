export const meta = {
  name: 'hig-podcast-editorial',
  description: 'Produce ep-83-style editorial JSON (deck, pull-quote, bullets, honest stats, guests) for High Impact Growth back-catalog episodes',
  phases: [
    { title: 'Editorial', detail: 'one agent per episode: read extraction JSON, write editorial JSON' },
  ],
}

const BASE = '/Users/gillianjavetski/Documents/Gillian Coding/Pre-Login Websites/Dimagi Pre-Login/Context'

const EXAMPLE = JSON.stringify({
  deck: "Inside HEP Assist: a generative-AI call center built by Last Mile Health and IDinsight, in partnership with Ethiopia's Ministry of Health, to support the country's 40,000 health extension workers in their own languages.",
  seo_description: "How Last Mile Health and IDinsight built HEP Assist, a generative-AI call center supporting Ethiopia's 40,000 health extension workers.",
  og_description: "Inside HEP Assist: a generative-AI call center supporting Ethiopia's 40,000 health extension workers in local languages.",
  pull_quote: { text: "There's a lot of skepticism that AI is not an appropriate solution. And I feel like we have disproved that.", cite: "On the impact of HEP Assist" },
  bullets: [
    "<strong>The RAG architecture</strong> behind HEP Assist, grounded in Ethiopia's national clinical guidelines",
    "<strong>Meet Hawa</strong>, the virtual assistant built to respond in Amharic, Oromo, and other local languages",
    "<strong>Costing AI at scale</strong>: modeling what it really takes to run this for 40,000 workers",
    "<strong>Earning government trust</strong> on data security, privacy, and ministry buy-in",
    "<strong>Augmentation, not replacement</strong>: keeping the human health worker at the center"
  ],
  stats: [
    { num: "40,000", label: "health extension workers HEP Assist is designed to reach" },
    { num: "6,500+", label: "AI-supported consultations completed so far" },
    { num: "53%", label: "of cases resolved at the community level" }
  ],
  guests: [
    { name: "Abraham Zerihun", role: "Ethiopia Country Director, leading delivery of HEP Assist on the ground with the Ministry of Health.", org: "Last Mile Health", initials: "AZ" },
    { name: "Sid Ravinutala", role: "Chief Data Scientist, architect of the RAG system and evaluation approach behind the AI assistant.", org: "IDinsight", initials: "SR" }
  ]
}, null, 1)

const STATUS = {
  type: 'object',
  additionalProperties: false,
  required: ['slug', 'wrote', 'bullets', 'stats', 'guests', 'has_quote'],
  properties: {
    slug: { type: 'string' },
    num: { type: 'integer' },
    wrote: { type: 'boolean', description: 'true if the editorial JSON file was written' },
    bullets: { type: 'integer' },
    stats: { type: 'integer', description: 'number of real stats found (0 if none)' },
    guests: { type: 'integer', description: 'number of non-host guests' },
    has_quote: { type: 'boolean' },
    note: { type: 'string', description: 'optional: anything unusual (no transcript, no guests, etc.)' },
  },
}

function prompt(e) {
  const noTx = !!e.noTranscript
  const txLine = noTx
    ? 'IMPORTANT: the transcript on the source page is WRONG or unavailable for this episode. IGNORE the extraction file\'s "transcript" field completely. Base EVERYTHING only on the title and the show_notes.'
    : 'transcript (array of {speaker, text} = the full verbatim transcript), and listen links.'
  const aboutLine = noTx
    ? '- about: OPTIONAL array of 2-3 paragraph strings; include if it helps, grounded STRICTLY in the show_notes and title (invent nothing). Otherwise omit.'
    : '- about: OPTIONAL array of 2-3 paragraph strings. Include ONLY if show_notes has fewer than 2 substantial paragraphs; write a faithful summary grounded strictly in show_notes + transcript (invent nothing). Otherwise OMIT this key.'
  const quoteLine = noTx
    ? '- pull_quote: OMIT this key entirely (there is no reliable transcript to quote), UNLESS a compelling quote appears verbatim in the show_notes.'
    : '- pull_quote: { text, cite }. text = the single most compelling VERBATIM quote from the transcript (copy exactly, trim to one or two strong sentences, do NOT paraphrase). cite = the speaker\'s name or a short context phrase like "On earning government trust". Prefer a guest quote.'
  return [
    'You are writing the editorial layer for ONE episode of Dimagi\'s "High Impact Growth" podcast,',
    'to match the house style of the flagship episode (ep 83).',
    '',
    'STEP 1 - Read this extraction file:',
    BASE + '/episodes/' + e.slug + '.json',
    'It has: title, num, date, duration, show_notes (array of paragraphs = Dimagi\'s own episode description),',
    txLine,
    '',
    'STEP 2 - Produce an editorial JSON object with EXACTLY these keys:',
    '- deck: ONE 1-2 sentence hero subtitle capturing the episode, in Dimagi\'s calm credible voice. Faithful. <= ~240 chars.',
    '- seo_description: meta description, <= 160 chars.',
    '- og_description: social description, <= 120 chars.',
    aboutLine,
    quoteLine,
    '- bullets: 5-7 "In this episode" highlights. Each MAY start with a bolded lead-in using <strong>...</strong>',
    '  (see example). Grounded in the actual content.',
    '- stats: 0-3 objects { num, label }. num = a real figure ACTUALLY stated in THIS episode (e.g. "40,000", "53%", "20 years").',
    '  label = what it refers to. CRITICAL: only figures genuinely present in show_notes or transcript. If the episode has no',
    '  meaningful numbers, return []. NEVER invent, estimate, or borrow numbers from the example.',
    '- guests: array of { name, role, org, initials } for the NON-HOST people in the conversation.',
    '  The hosts are Amie Vaccaro and Jonathan (John) Jackson of Dimagi - NEVER list them as guests (they are added automatically).',
    '  Identify guests from the title, show_notes, and transcript speaker labels. role = their title/description (1 sentence),',
    '  org = their organization, initials = 2 letters. If there are no outside guests, return [].',
    '',
    'HARD RULES:',
    '- NEVER use em dashes. Use commas, periods, or "to"/"and". (Applies to every string you write.)',
    '- Everything must be faithful to the source. Do not fabricate facts, names, orgs, numbers, or quotes.',
    '- Match the example\'s shape and tone, but NEVER reuse its content.',
    '',
    'EXAMPLE (ep 83, for shape/style only):',
    EXAMPLE,
    '',
    'STEP 3 - Write ONLY the raw JSON object (no markdown, no code fences, no commentary) to:',
    BASE + '/editorial/' + e.slug + '.json',
    '',
    'Then return the status object (slug="' + e.slug + '", num=' + e.num + ').',
  ].join('\n')
}

let parsed = args
if (typeof parsed === 'string') { try { parsed = JSON.parse(parsed) } catch (_) {} }
const EP = Array.isArray(parsed) ? parsed
  : (parsed && Array.isArray(parsed.episodes) ? parsed.episodes : [])
if (!EP.length) { log('no episodes passed in args'); return { error: 'no args', argsType: typeof args } }

phase('Editorial')
const results = await parallel(EP.map((e) => () =>
  agent(prompt(e), { label: 'ep' + e.num, phase: 'Editorial', schema: STATUS })
    .then((r) => r ? { ...r, num: e.num, slug: e.slug } : { slug: e.slug, num: e.num, wrote: false })
))

const ok = results.filter((r) => r && r.wrote).length
log('editorial written: ' + ok + '/' + EP.length)
return results
