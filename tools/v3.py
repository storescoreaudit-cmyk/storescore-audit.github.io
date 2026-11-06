import json,sys
from playwright.sync_api import sync_playwright
F="<link href='https://fonts.googleapis.com/css2?family=Inter:wght@500;700;900&display=swap' rel='stylesheet'>"
BG=["radial-gradient(circle at 70% 25%,#2d3b8f 0%,#0b0d18 65%)","radial-gradient(circle at 25% 75%,#0e5a3c 0%,#081410 65%)","radial-gradient(circle at 75% 70%,#7a2f12 0%,#120a06 65%)"]
def slide(i,n,s,bg):
    if s.get("photo"): bg=f"linear-gradient(180deg,rgba(0,0,0,.05) 0%,rgba(0,0,0,.25) 45%,rgba(0,0,0,.92) 80%),url('{s['photo']}') center top/cover"
    big=s.get("big","")
    return f"""<div style="width:1080px;height:1350px;background:{bg};color:#fff;font-family:Inter,sans-serif;box-sizing:border-box;padding:120px 90px;display:flex;flex-direction:column;justify-content:{'flex-end' if i==1 else 'center'};position:relative">
{f"<div style='position:absolute;top:110px;left:90px;right:90px;font-size:300px;font-weight:900;line-height:1;opacity:.12;letter-spacing:-10px'>{big}</div>" if big else ""}
<div style="align-self:flex-start;background:{s.get('pill','#ff3b30')};color:#fff;font-weight:900;font-size:32px;padding:10px 22px;border-radius:10px;letter-spacing:1px;margin-bottom:36px">{s['tag']}</div>
<div style="font-weight:900;font-size:{s.get('size',104 if i==1 else 84)}px;line-height:1.02;letter-spacing:-3px">{s['title']}</div>
{f"<div style='font-weight:500;font-size:42px;line-height:1.4;margin-top:40px;color:#e8e8ee'>{s['body']}</div>" if s.get('body') else ""}
{f"<div style='margin-top:56px;font-size:28px;color:#9aa0b4'>{s['src']}</div>" if s.get('src') else ""}
{"<div style='position:absolute;right:90px;bottom:70px;font-weight:900;font-size:40px'>→</div>" if i<n else ""}</div>"""
d=json.load(open(sys.argv[1]))
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":1080,"height":1350})
    for k,(name,sl) in enumerate(d.items()):
        for i,s in enumerate(sl,1):
            pg.set_content(f"<html><head>{F}</head><body style='margin:0'>"+slide(i,len(sl),s,BG[k%3])+"</body></html>");pg.wait_for_timeout(400)
            pg.screenshot(path=f"{name}-{i}.jpg",type="jpeg",quality=92)
    b.close()
