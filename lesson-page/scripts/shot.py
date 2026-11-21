"""给讲解页截整页图，再切成几段，方便从头到尾当读者看一遍。
    python shot.py <url 或 html 文件> <输出目录> [宽度=1400]
输出 <输出目录>/full.png 和 part_01.jpg, part_02.jpg ...（每段高约 1400 px）。

需要 playwright 和 chromium。脚本会自动使用 ~/.local/share/lesson-page/pw 里的 playwright（不动项目环境）。换了机器、
这个目录不在了，就重新装一次（用项目的 python 即可，版本要和运行本脚本的 python 一致）：
    uv pip install --python <python> --target ~/.local/share/lesson-page/pw playwright
    PYTHONPATH=~/.local/share/lesson-page/pw <python> -m playwright install chromium
中文显示成方块说明机器上没有中文字体：把 NotoSansCJKsc-Regular.otf / -Bold.otf（github.com/notofonts/noto-cjk）放进
~/.fonts 后运行 fc-cache -f。
"""
import os
import sys

_pw = os.path.expanduser("~/.local/share/lesson-page/pw")
if os.path.isdir(_pw):
    sys.path.insert(0, _pw)

# 项目的环境脚本可能改了缓存目录，导致找不到已装好的浏览器：固定到默认位置
_default = os.path.expanduser("~/.cache/ms-playwright")
if "PLAYWRIGHT_BROWSERS_PATH" not in os.environ and os.path.isdir(_default):
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = _default

from playwright.sync_api import sync_playwright

url, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 1400
if not url.startswith(("http://", "https://", "file://")):
    url = "file://" + os.path.abspath(url)
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": width, "height": 1000})
    pg.goto(url, wait_until="networkidle")
    pg.evaluate("document.querySelectorAll('details').forEach(d => d.open = false)")
    h = pg.evaluate("document.documentElement.scrollHeight")
    pg.screenshot(path=os.path.join(out, "full.png"), full_page=True)
    n = 0
    for y in range(0, h, 1400):
        n += 1
        pg.screenshot(path=os.path.join(out, f"part_{n:02d}.jpg"), clip={"x": 0, "y": y, "width": width, "height": min(1400, h - y)}, type="jpeg", quality=80, full_page=True)
    b.close()
print(f"{n} parts, page height {h} px -> {out}")
