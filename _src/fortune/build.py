import base64, json, os, segno
from data import FORTUNES, ITEMS, COLORS
H = os.path.dirname(os.path.abspath(__file__))
URL = "https://imsean629.github.io/sangsin-leader-2027/fortune/"
q = segno.make(URL, error='q'); q.save(f"{H}/out/qr_fortune.png", scale=20, border=2, dark="#0B1B36"); q.save(f"{H}/out/qr_fortune.svg", scale=10, border=2, dark="#0B1B36")
b64 = lambda p, m: f"data:{m};base64," + base64.b64encode(open(p, "rb").read()).decode()
h2c = open(f"{H}/../lt/vendor/node_modules/html2canvas/dist/html2canvas.min.js").read().replace("</script", "<\\/script")
J = lambda o: json.dumps(o, ensure_ascii=False)
s = open(f"{H}/template.html").read()
s = (s.replace("/*__H2C__*/", h2c).replace("/*__FORTUNES__*/null", J(FORTUNES)).replace("/*__ITEMS__*/null", J(ITEMS)).replace("/*__COLORS__*/null", J(COLORS))
      .replace("__LOGOW__", b64(f"{H}/../assets/logo_en_white.png", "image/png")).replace("__LOGO__", b64(f"{H}/../assets/logo_en.png", "image/png")))
open(f"{H}/out/index.html", "w").write(s)
F = "/home/claude/xb/fonts/node_modules/@fontsource"
loc = "".join(f'<link rel="stylesheet" href="file://{F}/{x}">' for x in ["noto-sans-kr/400.css", "noto-sans-kr/700.css", "noto-sans-kr/900.css", "gowun-batang/700.css"])
open(f"{H}/out/index_local.html", "w").write(s.replace("</head>", loc + "</head>"))
print("built", os.path.getsize(f"{H}/out/index.html") // 1024, "KB")
