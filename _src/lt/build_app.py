# -*- coding: utf-8 -*-
"""모바일 리더십 테스트 — 단일 HTML 생성 (이미지·데이터·스크립트 모두 포함)"""
import base64, json, os
from data import TYPES, ORDER, STAT_LABELS, QUESTIONS, WORLD, ICONS, exposures

HERE = os.path.dirname(os.path.abspath(__file__))


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def build():
    data = {
        "order": ORDER, "statLabels": STAT_LABELS, "world": WORLD,
        "types": {k: dict(t) for k, t in TYPES.items()},
        "questions": [{"text": q, "options": [{"t": t, "label": l} for t, l in opts]} for q, opts in QUESTIONS],
        "expo": exposures(),
    }
    imgs = {}
    for k in ORDER:
        imgs[k] = b64(os.path.join(HERE, "img", f"{k}.jpg"), "image/jpeg")
        imgs[k + "_th"] = b64(os.path.join(HERE, "img", f"{k}_th.jpg"), "image/jpeg")
    h2c = open(os.path.join(HERE, "vendor/node_modules/html2canvas/dist/html2canvas.min.js"), encoding="utf-8").read()
    h2c = h2c.replace("</script", "<\\/script")
    tpl = open(os.path.join(HERE, "app_template.html"), encoding="utf-8").read()
    html = (tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
               .replace("/*__IMGS__*/null", json.dumps(imgs))
               .replace("/*__ICONS__*/null", json.dumps(ICONS))
               .replace("/*__H2C__*/", h2c)
               .replace("__LOGOW__", b64(os.path.join(HERE, "../assets/logo_en_white.png"), "image/png"))
               .replace("__LOGO__", b64(os.path.join(HERE, "../assets/logo_en.png"), "image/png")))
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    out = os.path.join(HERE, "out", "leadership_test.html")
    open(out, "w", encoding="utf-8").write(html)
    return out


if __name__ == "__main__":
    p = build(); print(p, os.path.getsize(p) // 1024, "KB")
