#!/usr/bin/env python3
"""Extract a High Impact Growth episode from its live dimagi.com page into JSON.

Usage: python3 extract_episode.py <slug-or-url>
Emits JSON on stdout: title, num, duration, spotify_id, listen links,
show_notes paragraphs, transcript paragraphs (speaker-tagged), headshot URLs.
Deterministic parsing of the Divi markup; no network beyond a single curl.
"""
import sys, re, json, html, subprocess

def fetch(url):
    return subprocess.run(["curl", "-sL", url], capture_output=True, text=True).stdout

def strip_tags(t):
    t = re.sub(r"(?is)<br\s*/?>", " ", t)
    t = re.sub(r"(?is)<[^>]+>", "", t)
    return html.unescape(t).strip()

def extract(arg):
    slug = arg.rstrip("/").split("/")[-1] if arg.startswith("http") else arg
    url = arg if arg.startswith("http") else f"https://dimagi.com/podcast/{slug}/"
    h = fetch(url)
    h = re.sub(r"(?is)<script.*?</script>", "", h)
    h = re.sub(r"(?is)<style.*?</style>", "", h)

    out = {"slug": slug, "url": url}

    # Title
    m = re.search(r"(?is)<title>(.*?)</title>", h)
    title = html.unescape(m.group(1)).strip() if m else ""
    title = re.sub(r"\s*[-|]\s*Dimagi\s*$", "", title)
    numm = re.match(r"(?i)\s*Episode\s*(\d+)\s*[:\-]\s*", title)
    if numm:
        out["num"] = int(numm.group(1))
    title = re.sub(r"(?i)^\s*Episode\s*\d+\s*[:\-]\s*", "", title).strip()
    out["title"] = title

    # Spotify episode id (ignore /video variant)
    sm = re.search(r"open\.spotify\.com/embed/episode/([A-Za-z0-9]+)", h)
    out["spotify_id"] = sm.group(1) if sm else None

    def first(pat):
        mm = re.search(pat, h)
        return mm.group(0) if mm else None
    out["apple"] = first(r"https://podcasts\.apple\.com/[^\"' ]+")
    yt = first(r"https://youtu\.be/[^\"' ]+") or first(r"https://www\.youtube\.com/watch[^\"' ]+")
    out["youtube"] = yt
    out["amazon"] = first(r"https://music\.amazon\.com/podcasts/[^\"' ]+")

    # Episode N | NN Minutes  -> duration
    dm = re.search(r"(?i)Episode\s*(\d+)\s*\|\s*(\d+)\s*Minutes?", h)
    sn_start = 0
    if dm:
        out.setdefault("num", int(dm.group(1)))
        out["duration"] = f"{dm.group(2)} min"
        sn_start = dm.start()

    # All <p> in document order with offsets
    ptags = [(mm.start(), strip_tags(mm.group(1))) for mm in re.finditer(r"(?is)<p[^>]*>(.*?)</p>", h)]

    tidx = h.find('id="toggleTranscript"')
    if tidx == -1:
        tidx = h.find("toggleTranscript")

    # Transcript = <p> between the transcript module and the first host/guest card.
    # Host & guest bios live in Divi-Plus `df_person` modules, which is a stable end marker
    # (more robust than div-balancing, which breaks on malformed pasted transcript HTML).
    transcript = []
    tc_start = tidx if tidx != -1 else len(h)
    if tidx != -1:
        tc_end = len(h)
        for mk in ("Meet The Hosts", "df_person", "Subscribe To Our Newsletter",
                   "Copyright &copy;", "Copyright ©", "<footer"):
            p = h.find(mk, tidx)
            if p != -1:
                tc_end = min(tc_end, p)
        region = h[tidx:tc_end]
        for mm in re.finditer(r"(?is)<p[^>]*>(.*?)</p>", region):
            txt = strip_tags(mm.group(1))
            if not txt or re.match(r"(?i)this transcript was generated", txt):
                continue
            transcript.append(txt)

    # Show notes = <p> between the "Episode N | Minutes" marker and the transcript heading
    show_notes = []
    tpos = h.rfind(">Transcript<", 0, tc_start)
    sn_end = tpos if tpos != -1 else tc_start
    for off, txt in ptags:
        if not txt or off < sn_start or off >= sn_end:
            continue
        if re.match(r"(?i)^(x|listen|on this episode|transcript$|episode\s*\d+\s*\|)", txt):
            continue
        show_notes.append(txt)
    out["show_notes"] = show_notes
    # Format transcript paragraphs: bold "Name:" -> span.spk
    fmt = []
    for p in transcript:
        sm2 = re.match(r"^([A-Z][A-Za-z.\-' ]{1,40}?):\s+(.*)$", p)
        if sm2 and len(sm2.group(1).split()) <= 4:
            fmt.append({"speaker": sm2.group(1).strip(), "text": sm2.group(2).strip()})
        else:
            fmt.append({"speaker": None, "text": p})
    out["transcript"] = fmt
    out["transcript_para_count"] = len(fmt)

    # Host detection (Amie / Jonathan reuse shared local headshots; guests use monograms)
    htxt = h.lower()
    out["host_amie"] = ("vaccaro" in htxt) or ("vacarro" in htxt)
    out["host_jonathan"] = "jonathan jackson" in htxt or "jonathanljackson" in htxt
    return out

if __name__ == "__main__":
    print(json.dumps(extract(sys.argv[1]), ensure_ascii=False))
