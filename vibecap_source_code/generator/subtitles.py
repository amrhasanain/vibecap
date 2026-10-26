from pathlib import Path

def make_captions(words, p):
    caps, cur = [], []

    def flush():
        if cur:
            caps.append({"start": cur[0]["start"], "end": cur[-1]["end"], "words": list(cur)})
            cur.clear()

    for w in words:
        if cur:
            joined = " ".join(x["word"] for x in cur) + " " + w["word"]
            if (len(joined) > p["max_chars"] * p["max_lines"]
                    or (p["max_words"] and len(cur) >= p["max_words"])
                    or w["end"] - cur[0]["start"] > p["max_dur"]
                    or w["start"] - cur[-1]["end"] > 0.8):
                flush()
        cur.append(w)
        if w["word"][-1] in ".!?؟…" and len(cur) >= 2:
            flush()
    flush()

    for i, c in enumerate(caps):
        nxt = caps[i + 1]["start"] if i + 1 < len(caps) else c["end"] + 0.3
        end = c["end"] + 0.25
        c["end"] = end if end <= nxt else max(nxt, c["end"])
    return caps

def wrap_words(ws, max_chars):
    total = len(" ".join(ws))
    n = max(1, -(-total // max_chars))
    target = total / n
    lines, cur = [], []
    for x in ws:
        if cur and len(" ".join(cur + [x])) > target and len(lines) < n - 1:
            lines.append(cur)
            cur = [x]
        else:
            cur.append(x)
    lines.append(cur)
    return lines

def srt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"

def ass_time(t):
    cs = round(t * 100)
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"

def ass_color(rgb, alpha=0):
    r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()

def write_srt(caps, path, p):
    with open(path, "w", encoding="utf-8") as f:
        for i, c in enumerate(caps, 1):
            lines = wrap_words([w["word"] for w in c["words"]], p["max_chars"])
            f.write(f"{i}\n{srt_time(c['start'])} --> {srt_time(c['end'])}\n")
            f.write("\n".join(" ".join(l) for l in lines) + "\n\n")

def is_rtl(text):
    for ch in text:
        if ch.isalpha():
            o = ord(ch)
            return 0x0590 <= o <= 0x08FF or 0xFB1D <= o <= 0xFEFF
    return False

def visual_order(items):
    runs = []
    for it in items:
        tok = it[1]
        if any(c.isalpha() for c in tok):
            rtl = is_rtl(tok)
        else:
            rtl = runs[-1][0] if runs else True
        if runs and runs[-1][0] == rtl:
            runs[-1][1].append(it)
        else:
            runs.append((rtl, [it]))
    out = []
    for rtl, run in reversed(runs):
        out += run[::-1] if rtl else run
    return out

def fit_chars(p, size):
    W, H = size
    k = min(W, H) / 1080
    cpl = int((W - 120 * k) / (0.6 * p["size"] * k))
    return max(8, min(p["max_chars"], cpl))

def write_ass(caps, path, p, size, font=None, position=None):
    W, H = size
    k = min(W, H) / 1080
    align, mv = p["align"], round(p["margin"] * H)
    if position == "top":
        align, mv = 8, round(0.06 * H)
    elif position == "middle":
        align, mv = 5, 0
    elif position == "bottom":
        align, mv = 2, round(0.06 * H)

    fnt = font or p["font"]
    kara = bool(p["highlight"])
    primary = p["highlight"] if kara else p["color"]
    mx = round(60 * k)

    def style(name, prim, sec, outc, outa, outline, shadow, border):
        return (
            f"Style: {name},{fnt},{round(p['size'] * k)},"
            f"{ass_color(prim)},{ass_color(sec)},{ass_color(outc, outa)},"
            f"{ass_color('000000', 0x80)},{-1 if p['bold'] else 0},0,0,0,100,100,0,0,"
            f"{border},{outline * k:.1f},{shadow * k:.1f},{align},{mx},{mx},{mv},1"
        )

    styles = [style("Default", primary, p["color"], p["outline_c"], p["outline_a"], p["outline"], p["shadow"], p["border"])]
    if p["glow"]:
        styles.append(style("Glow", p["glow"], p["glow"], p["glow"], 0x30, p["outline"] + p["glow_blur"], 0, 1))

    out = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}",
        "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,"
        "BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,"
        "BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding",
        *styles, "",
        "[Events]",
        "Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text",
    ]

    ktag = "\\kf" if p["sweep"] else "\\k"
    for c in caps:
        ws = c["words"]
        texts = []
        for w in ws:
            t = w["word"].replace("{", "").replace("}", "").replace("\\", "")
            texts.append(t.upper() if p["upper"] else t)
        lines = wrap_words(texts, p["max_chars"])

        indexed, i = [], 0
        for line in lines:
            indexed.append([(i + n, tok) for n, tok in enumerate(line)])
            i += len(line)

        plain = []
        for li, items in enumerate(indexed):
            rtl_line = is_rtl(items[0][1])
            if li > 0:
                plain.append("\\N")
            if rtl_line:
                plain.append("\u202b")
            plain.append(" ".join(tok for _, tok in items))
            if rtl_line:
                plain.append("\u202c")

        parts, t0 = [], ws[0]["start"]
        for li, items in enumerate(indexed):
            order = visual_order(items) if (kara and is_rtl(items[0][1])) else items
            for wi, (n, tok) in enumerate(order):
                sep = "" if (li == 0 and wi == 0) else ("\\N" if wi == 0 else " ")
                if kara:
                    nxt = ws[n + 1]["start"] if n + 1 < len(ws) else ws[n]["end"]
                    cs = max(1, round((nxt - ws[n]["start"]) * 100))
                    kt = max(0, round((ws[n]["start"] - t0) * 100))
                    parts.append(sep + "{\\kt" + str(kt) + ktag + str(cs) + "}" + tok)
                else:
                    parts.append(sep + tok)
        if not kara:
            parts = plain

        fx = p["fx"]
        start, end = ass_time(c["start"]), ass_time(c["end"])
        if p["glow"]:
            gfx = fx + "\\blur" + f"{p['glow_blur'] * k:.1f}"
            out.append(f"Dialogue: 0,{start},{end},Glow,,0,0,0,,{{{gfx}}}" + "".join(plain))
        out.append(f"Dialogue: 1,{start},{end},Default,,0,0,0,," + ("{" + fx + "}" if fx else "") + "".join(parts))

    Path(path).write_text("\n".join(out) + "\n", encoding="utf-8-sig")