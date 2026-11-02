"""Save every image a public page loads (headless, installed Chrome channel) - a client's real product shots, logos,
banners - for real-asset explainer scenes. Built for a client promo (2026-10-27, Shopee store + FB post).

usage: py -3.12 harvest-images.py <out_dir> <url> [<url> ...] [--min-kb 8] [--scrolls 12]

Per url: follows redirects (short links), scrolls to load lazy images, saves every image/* response >= --min-kb to
<out_dir>/<host-slug>/NNN-<name>.<ext>, plus a viewport + full-page screenshot and an index.json (src url, size, px).
Shopee: image urls ending in _tn / @resize are thumbnails - the full file is fetched too (same url without the suffix).
Public pages only; a login wall shows up as a screenshot of the wall and few images - report it, never log in.
"""
import asyncio, hashlib, io, json, re, sys
from pathlib import Path
from urllib.parse import urlparse
from PIL import Image
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
args = sys.argv[1:]
def opt(k, d):
    if k in args:
        i = args.index(k); v = args[i + 1]; del args[i:i + 2]; return v
    return d
MIN_KB = float(opt("--min-kb", "8")); SCROLLS = int(opt("--scrolls", "12"))
OUT = Path(args[0]); URLS = args[1:]
EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif", "image/svg+xml": "svg", "image/avif": "avif"}


def full_size(u):
    if "susercontent.com" in u or "img.shopee" in u:
        return re.sub(r"(_tn|@resize_[^/?]+)(?=$|\?)", "", u)
    return None


async def harvest(ctx, url):
    page = await ctx.new_page()
    got = {}

    async def on_resp(r):
        ct = (r.headers.get("content-type") or "").split(";")[0]
        if not ct.startswith("image/"):
            return
        try:
            body = await r.body()
        except Exception:
            return
        if len(body) >= MIN_KB * 1024:
            got[r.url] = (ct, body)

    page.on("response", on_resp)
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
        print(f"  goto: {e}")
    await page.wait_for_timeout(4000)
    for _ in range(SCROLLS):
        await page.mouse.wheel(0, 1400)
        await page.wait_for_timeout(900)
    await page.wait_for_timeout(2000)
    slug = re.sub(r"[^a-z0-9]+", "-", (urlparse(page.url).netloc + urlparse(page.url).path).lower()).strip("-")[:60]
    d = OUT / slug; d.mkdir(parents=True, exist_ok=True)
    await page.evaluate("window.scrollTo(0,0)"); await page.wait_for_timeout(800)
    await page.screenshot(path=str(d / "_viewport.png"))
    try:
        await page.screenshot(path=str(d / "_full.png"), full_page=True)
    except Exception as e:
        print(f"  full shot: {e}")
    # thumbnails -> full size
    for u in list(got):
        f = full_size(u)
        if f and f not in got:
            try:
                r = await ctx.request.get(f, timeout=30000)
                ct = (r.headers.get("content-type") or "").split(";")[0]
                if r.ok and ct.startswith("image/"):
                    got[f] = (ct, await r.body())
            except Exception:
                pass
    index, seen = [], set()
    for i, (u, (ct, body)) in enumerate(got.items()):
        h = hashlib.md5(body).hexdigest()
        if h in seen:
            continue
        seen.add(h)
        try:
            w, hgt = Image.open(io.BytesIO(body)).size
        except Exception:
            w = hgt = None
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(urlparse(u).path).name)[:40] or "img"
        fn = f"{len(index):03d}-{name}"
        if not fn.lower().endswith("." + EXT.get(ct, "bin")):
            fn += "." + EXT.get(ct, "bin")
        (d / fn).write_bytes(body)
        index.append({"file": fn, "url": u, "kb": round(len(body) / 1024), "w": w, "h": hgt})
    (d / "index.json").write_text(json.dumps({"start": url, "final": page.url, "title": await page.title(), "images": index}, indent=1), encoding="utf-8")
    print(f"{url}\n  -> {page.url}\n  title: {await page.title()}\n  {len(index)} images -> {d}")
    await page.close()


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel="chrome", headless=True)
        ctx = await b.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2, locale="en-PH")
        for u in URLS:
            await harvest(ctx, u)
        await b.close()

asyncio.run(main())
