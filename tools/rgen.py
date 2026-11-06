import json,sys
from playwright.sync_api import sync_playwright
FONT="<link href='https://fonts.googleapis.com/css2?family=Inter:wght@500;800;900&family=Fraunces:opsz,wght@9..144,600&display=swap' rel='stylesheet'>"
T={"ink":("#0b0b0b","#f6f1e7","#c6f432"),"lime":("#c6f432","#0b0b0b","#0b0b0b"),"cream":("#f6f1e7","#0b0b0b","#0e3b2c"),"green":("#0e3b2c","#f6f1e7","#c6f432")}
def trendy(n,tot,s):
    bg,fg,acc=T[s.get("theme","cream")]
    emoji=f"<div style='font-size:170px;line-height:1;margin-bottom:34px'>{s['emoji']}</div>" if s.get("emoji") else ""
    return f"""<div style="width:1080px;height:1920px;background:{bg};color:{fg};font-family:Inter,sans-serif;box-sizing:border-box;padding:260px 84px 420px;display:flex;flex-direction:column;justify-content:center">{emoji}
<div style="align-self:flex-start;background:{acc};color:{bg};font-weight:900;font-size:34px;padding:12px 22px;border-radius:14px;margin-bottom:38px;text-transform:uppercase">{s['tag']}</div>
<div style="font-weight:900;font-size:{s.get('size',124)}px;line-height:.95;letter-spacing:-5px">{s['title']}</div>
<div style="font-weight:500;font-size:46px;line-height:1.35;margin-top:44px;opacity:.85">{s['body']}</div></div>"""
def sober(n,tot,s):
    bg,fg,acc=("#f6f1e7","#15140f","#0e3b2c") if n%2 else ("#0e3b2c","#f6f1e7","#d4b26a")
    return f"""<div style="width:1080px;height:1920px;background:{bg};color:{fg};font-family:Inter,sans-serif;box-sizing:border-box;padding:300px 96px 440px;display:flex;flex-direction:column;justify-content:center">
<div style="font-size:34px;letter-spacing:8px;text-transform:uppercase;color:{acc};margin-bottom:44px">{s['tag']}</div>
<div style="font-family:Fraunces,Georgia,serif;font-weight:600;font-size:{s.get('size',104)}px;line-height:1.04;letter-spacing:-2px">{s['title']}</div>
<div style="font-size:46px;line-height:1.45;margin-top:48px;opacity:.85">{s['body']}</div>
<div style="margin-top:70px;font-size:30px;opacity:.55">storescore. · {n}/{tot}</div></div>"""
d=json.load(open(sys.argv[1]))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":1080,"height":1920})
    for name,r in d.items():
        f=trendy if r["style"]=="trendy" else sober
        for i,s in enumerate(r["slides"],1):
            pg.set_content(f"<html><head>{FONT}</head><body style='margin:0'>"+f(i,len(r["slides"]),s)+"</body></html>");pg.wait_for_timeout(500)
            pg.screenshot(path=f"{name}-{i}.png")
    b.close()
