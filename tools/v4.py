#!/usr/bin/env python3
"""StoreScore carrousels v4 — 1080x1350, détourage, emojis Apple, grain, style "magazine actu".
Usage: python3 tools/v4.py spec.json outdir
Slide types: cover | text | photo | split | quote | cta | min | grid
font:"serif" (citation-portrait) ; lh: interligne du titre (slides text, ex. 1.12) ; cards:[[img,x,y,w,h,rot,(css),(objpos)],...] collage ; style:"min" (par slide) = minimaliste sans grain ; min: huge/hy/hs/hc ; grid: cells[4], cols[2], rows[2] ; photo: pos, mag, huge
Champs: title (avec *mot* = surligné), sub, emoji (liste), cutout (photos/cutouts/x.png), photo (photos/lib/x.jpg), bigword, num, tag, theme(dark|light|green)
Emojis: tout emoji unicode dans un texte est rendu en emoji Apple.
"""
import json, sys, os, base64, re
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMO = os.path.join(ROOT, "tools", "emoji")

def b64(p, mime=None):
    p = p if os.path.isabs(p) else os.path.join(ROOT, p)
    mime = mime or ("image/png" if p.endswith(".png") else "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()

EMO_RE = re.compile("(?:[\U0001F1E6-\U0001F1FF]{2})|(?:[☀-➿\U0001F300-\U0001FAFF⭐⬆↔-↪⏩-⏺⤴⤵〰〽㊗㊙©®‼⁉™ℹ](?:️)?(?:‍[☀-➿\U0001F300-\U0001FAFF](?:️)?)*)")
def emo_img(ch, size="1.05em"):
    cps = [f"{ord(c):04x}" for c in ch]
    for cand in ("-".join(cps), "-".join(c for c in cps if c != "fe0f"), "-".join(cps + ["fe0f"])):
        f = os.path.join(EMO, cand + ".png")
        if os.path.exists(f):
            return f'<img class="e" style="height:{size}" src="{b64(f)}">'
    return ch
def rich(t):
    t = (t or "").replace("&", "&amp;").replace("<", "&lt;")
    t = re.sub(r"\*(.+?)\*", r'<mark>\1</mark>', t)
    t = t.replace("\n", "<br>")
    return EMO_RE.sub(lambda m: emo_img(m.group(0)), t)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;font-family:'Inter',sans-serif}
.s{position:relative;width:1080px;height:1350px;overflow:hidden}
.dark{background:radial-gradient(120% 90% at 80% 10%,#1d3b2c 0%,#0b0f0d 55%,#050605 100%);color:#fff}
.green{background:radial-gradient(110% 90% at 20% 0%,#2fe38a 0%,#12a35c 45%,#06381f 100%);color:#fff}
.light{background:#f4f1ea;color:#0d0d0d}
.grain:after{content:"";position:absolute;inset:0;pointer-events:none;opacity:.10;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
.top{position:absolute;top:56px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center;z-index:9;font:700 28px 'Inter'}
.pill{background:#fff;color:#0b0f0d;padding:12px 26px;border-radius:99px;font:800 26px 'Inter';letter-spacing:.04em;text-transform:uppercase;display:inline-flex;gap:10px;align-items:center}
.light .pill{background:#0d0d0d;color:#fff}
.handle{opacity:.85}
.big{position:absolute;left:-20px;right:-20px;text-align:center;font:900 330px/0.85 'Anton','Bebas Neue',sans-serif;letter-spacing:-4px;text-transform:uppercase;color:rgba(255,255,255,.12);z-index:1;white-space:nowrap}
.light .big{color:rgba(0,0,0,.07)}
.cut{position:absolute;bottom:0;z-index:3;filter:drop-shadow(0 30px 60px rgba(0,0,0,.55))}
.title{position:absolute;left:64px;right:64px;z-index:5;font:900 92px/1.02 'Inter';letter-spacing:-3px}
.title mark{background:#2fe38a;color:#05140b;padding:0 14px;border-radius:14px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.green .title mark{background:#fff}
.sub{position:absolute;left:64px;right:64px;z-index:5;font:600 44px/1.3 'Inter';opacity:.92}
.fade{position:absolute;left:0;right:0;bottom:0;height:62%;z-index:4;background:linear-gradient(180deg,rgba(0,0,0,0),rgba(0,0,0,.88) 60%)}
.st{position:absolute;z-index:6;filter:drop-shadow(0 12px 20px rgba(0,0,0,.35))}
.num{font:900 220px/0.9 'Anton','Inter';color:#2fe38a;letter-spacing:-6px}
.light .num{color:#12a35c}
.green .num{color:#fff}
.card{position:absolute;z-index:3;border-radius:36px;overflow:hidden;box-shadow:0 40px 80px rgba(0,0,0,.35);border:10px solid #fff}
.card img{width:100%;height:100%;object-fit:cover;display:block}
.swipe{position:absolute;right:64px;bottom:60px;z-index:9;font:800 30px 'Inter';display:flex;gap:12px;align-items:center}
.photo{position:absolute;inset:0;background-size:cover;background-position:center}
/* style minimaliste : fond uni, typo énorme, pas de grain */
.mn.light{background:#f6f5f1}.mn.dark{background:#0a0a0a}.mn.green{background:#0f7a45}
.mn .title mark{background:none;color:#12a35c;padding:0}.mn.dark .title mark{color:#2fe38a}.mn.green .title mark{color:#0a0a0a;background:none}
.mn .pill{background:none;color:inherit;border:3px solid currentColor;padding:9px 22px;font-size:22px}
.mn .swipe{font:700 26px 'Inter';opacity:.6}
.huge{position:absolute;left:56px;right:56px;z-index:5;white-space:nowrap;font:900 300px/0.9 'Anton','Inter';letter-spacing:-6px}
.grid{position:absolute;left:150px;top:470px;width:780px;height:640px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;z-index:5}
.grid div{border:4px solid currentColor;margin:-2px;display:flex;align-items:center;justify-content:center;font:800 40px/1.15 'Inter';text-align:center}
.gl{position:absolute;z-index:5;font:900 30px 'Inter';letter-spacing:.12em;text-transform:uppercase;opacity:.55}
.serif .title{font-family:Georgia,'Playfair Display',serif;font-style:italic;font-weight:800;letter-spacing:-1px;line-height:1.08}
.serif .title mark{font-style:italic}
.mag{position:absolute;left:64px;top:150px;z-index:6;font:900 34px 'Inter';letter-spacing:.3em;text-transform:uppercase}
"""
FONTS = "<link href='https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@500;700;800;900&display=swap' rel='stylesheet'>"

def stickers(s):
    out = ""
    for st in s.get("emoji", []):
        ch, x, y, sz, rot = st
        out += f'<div class="st" style="left:{x}px;top:{y}px;transform:rotate({rot}deg)">{emo_img(ch, f"{sz}px")}</div>'
    return out

def slide(s, i, n, lang):
    th = s.get("theme", "dark")
    mn = s.get("style") == "min"
    h = f'<div class="s {th} {"mn" if mn else "grain"} {"serif" if s.get("font")=="serif" else ""}">'
    tag = rich(s.get("tag", ""))
    h += f'<div class="top">{f"<span class=pill>{tag}</span>" if tag else "<span></span>"}<span class="handle">@storescore.audit</span></div>'
    t = s.get("type", "text")
    if t == "cover":
        if s.get("bg"): h += f'<div class="photo" style="background-image:url({b64(s["bg"])});opacity:.35"></div>'
        h += f'<div class="big" style="top:{s.get("bigy",170)}px;font-size:{min(330,int(1450/max(1,len(s.get("bigword","x")))))}px">{s.get("bigword","")}</div>'
        if s.get("cutout"):
            h += f'<img class="cut" src="{b64(s["cutout"])}" style="height:{s.get("cuth",980)}px;{s.get("cutpos","right:-40px")}">'
        h += '<div class="fade"></div>'
        h += f'<div class="title" style="bottom:{s.get("ty",250)}px;font-size:{s.get("fs",96)}px">{rich(s["title"])}</div>'
        if s.get("sub"): h += f'<div class="sub" style="bottom:120px">{rich(s["sub"])}</div>'
    elif t == "min":
        if s.get("huge"): h += f'<div class="huge" style="top:{s.get("hy",230)}px;font-size:{s.get("hs",300)}px;color:{s.get("hc","inherit")}">{rich(s["huge"])}</div>'
        h += f'<div class="title" style="top:{s.get("ty",640)}px;font-size:{s.get("fs",84)}px">{rich(s["title"])}</div>'
        if s.get("sub"): h += f'<div class="sub" style="top:{s.get("sy",1000)}px;font-size:{s.get("ss",40)}px;opacity:.7">{rich(s["sub"])}</div>'
    elif t == "grid":
        h += f'<div class="title" style="top:{s.get("ty",190)}px;font-size:{s.get("fs",76)}px">{rich(s["title"])}</div>'
        c = s["cells"]; cl = s.get("cols", ["", ""]); rl = s.get("rows", ["", ""])
        h += '<div class="grid">' + "".join(f"<div>{rich(x)}</div>" for x in c) + '</div>'
        h += f'<div class="gl" style="left:250px;top:425px">{cl[0]}</div><div class="gl" style="left:660px;top:425px">{cl[1]}</div>'
        h += f'<div class="gl" style="left:-60px;top:610px;transform:rotate(-90deg);width:300px;text-align:center">{rl[0]}</div><div class="gl" style="left:-60px;top:930px;transform:rotate(-90deg);width:300px;text-align:center">{rl[1]}</div>'
        if s.get("sub"): h += f'<div class="sub" style="top:{s.get("sy",1150)}px;font-size:36px;opacity:.7">{rich(s["sub"])}</div>'
    elif t == "photo":
        h += f'<div class="photo" style="background-image:url({b64(s["photo"])});background-position:{s.get("pos","center")}"></div><div class="fade" style="height:{s.get("fh",75)}%"></div>'
        if s.get("mag"): h += f'<div class="mag" style="color:#fff">{rich(s["mag"])}</div>'
        if s.get("huge"): h += f'<div class="huge" style="bottom:{s.get("hb",520)}px;font-size:{s.get("hs",230)}px;color:#2fe38a">{rich(s["huge"])}</div>'
        h += f'<div class="title" style="bottom:{s.get("ty",330)}px;font-size:{s.get("fs",80)}px">{rich(s["title"])}</div>'
        if s.get("sub"): h += f'<div class="sub" style="bottom:130px">{rich(s["sub"])}</div>'
    elif t == "split":
        if s.get("cutout"):
            h += f'<img class="cut" src="{b64(s["cutout"])}" style="height:{s.get("cuth",760)}px;{s.get("cutpos","right:-60px")};z-index:2">'
        if s.get("photo"):
            h += f'<div class="card" style="right:70px;bottom:120px;width:520px;height:600px;transform:rotate(4deg)"><img src="{b64(s["photo"])}"></div>'
        if s.get("num"): h += f'<div class="num" style="position:absolute;left:64px;top:170px;z-index:5">{s["num"]}</div>'
        h += f'<div class="title" style="top:{s.get("ty",420)}px;right:{s.get("tr",480)}px;font-size:{s.get("fs",72)}px">{rich(s["title"])}</div>'
        if s.get("sub"): h += f'<div class="sub" style="top:{s.get("sy",800)}px;right:{s.get("tr",480)}px;font-size:36px">{rich(s["sub"])}</div>'
    elif t == "text":
        if s.get("num"): h += f'<div class="num" style="position:absolute;left:64px;top:190px;z-index:5">{s["num"]}</div>'
        h += f'<div class="title" style="top:{s.get("ty",470)}px;font-size:{s.get("fs",84)}px;{("line-height:"+str(s["lh"])) if s.get("lh") else ""}">{rich(s["title"])}</div>'
        if s.get("sub"): h += f'<div class="sub" style="top:{s.get("sy",900)}px">{rich(s["sub"])}</div>'
    elif t == "quote":
        if s.get("cutout"):
            h += f'<img class="cut" src="{b64(s["cutout"])}" style="height:{s.get("cuth",820)}px;{s.get("cutpos","right:-60px")};z-index:2">'
        h += f'<div style="position:absolute;left:50px;top:120px;z-index:5;font:900 300px/1 Georgia,serif;color:{"#12a35c" if th=="light" else "#2fe38a"}">&ldquo;</div>'
        h += f'<div class="title" style="top:{s.get("ty",380)}px;right:{s.get("tr",380)}px;font:italic 800 {s.get("fs",70)}px/1.12 Georgia,serif;letter-spacing:-1px">{rich(s["title"])}</div>'
        h += f'<div class="sub" style="top:{s.get("sy",1000)}px;font:800 38px Inter;opacity:1">— {rich(s.get("author",""))}</div>'
    elif t == "cta":
        if s.get("cutout"):
            h += f'<img class="cut" src="{b64(s["cutout"])}" style="height:{s.get("cuth",700)}px;{s.get("cutpos","right:-40px")};opacity:.95">'
        h += f'<div class="title" style="top:{s.get("ty",260)}px;font-size:{s.get("fs",88)}px">{rich(s["title"])}</div>'
        if s.get("sub"): h += f'<div class="sub" style="font-size:46px;top:{s.get("sy",640)}px;right:{s.get("tr",64)}px">{rich(s["sub"])}</div>'
    for c in s.get("cards", []):
        h += f'<div class="card" style="left:{c[1]}px;top:{c[2]}px;width:{c[3]}px;height:{c[4]}px;transform:rotate({c[5]}deg);{c[6] if len(c)>6 else ""}"><img src="{b64(c[0])}" style="object-position:{c[7] if len(c)>7 else "center"}"></div>'
    if s.get("card"):
        c=s["card"]; h += f'<div class="card" style="left:{c[1]}px;top:{c[2]}px;width:{c[3]}px;height:{c[4]}px;transform:rotate({c[5]}deg)"><img src="{b64(c[0])}"></div>'
    h += stickers(s)
    if i < n - 1 and not s.get("noswipe"):
        h += f'<div class="swipe">{"Swipe" if lang=="en" else "Glisse"} {emo_img("👉","40px")}</div>'
    return h + "</div>"

def main(spec, out):
    d = json.load(open(spec)); os.makedirs(out, exist_ok=True)
    lang = d.get("lang", "fr"); n = len(d["slides"])
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(d["slides"]):
            pg.set_content(f"<html><head>{FONTS}<style>{CSS}</style></head><body>{slide(s,i,n,lang)}</body></html>")
            pg.wait_for_timeout(700)
            pg.screenshot(path=f"{out}/{i+1:02d}.jpg", type="jpeg", quality=92)
        b.close()
    print("ok", out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
