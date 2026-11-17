import base64, json, os, segno
from data import WORDS, LEVELS
H = os.path.dirname(os.path.abspath(__file__))
URL = "https://imsean629.github.io/sangsin-leader-2027/mz/"
q = segno.make(URL, error='q'); q.save(f"{H}/out/qr_mz.png", scale=20, border=2, dark="#0B1B36"); q.save(f"{H}/out/qr_mz.svg", scale=10, border=2, dark="#0B1B36")
b64 = lambda p, m: f"data:{m};base64," + base64.b64encode(open(p, "rb").read()).decode()
h2c = open(f"{H}/../lt/vendor/node_modules/html2canvas/dist/html2canvas.min.js").read().replace("</script", "<\\/script")
s = open(f"{H}/template.html").read()
s = (s.replace("/*__H2C__*/", h2c).replace("/*__WORDS__*/null", json.dumps(WORDS, ensure_ascii=False))
      .replace("/*__LEVELS__*/null", json.dumps(LEVELS, ensure_ascii=False)).replace("__LOGO__", b64(f"{H}/../assets/logo_en.png", "image/png")))
open(f"{H}/out/index.html", "w").write(s); print(len(WORDS), "words", os.path.getsize(f"{H}/out/index.html")//1024, "KB")
