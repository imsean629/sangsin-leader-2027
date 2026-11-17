import base64, json, os, re, segno

H = os.path.dirname(os.path.abspath(__file__))
URL = "https://imsean629.github.io/sangsin-leader-2027/count/"
SHEET = "https://script.google.com/macros/s/AKfycbyKUOWiAiVvusrHAca13lW98N5fdfOaQ7xPv9i8O7rbmpiq3UJLeRtMizwF6-Kfy5tx/exec"
q = segno.make(URL, error='q'); q.save(f"{H}/out/qr_count.png", scale=20, border=2, dark="#0B1B36"); q.save(f"{H}/out/qr_count.svg", scale=10, border=2, dark="#0B1B36")
b64 = lambda p, m: f"data:{m};base64," + base64.b64encode(open(p, "rb").read()).decode()
bt = open(f"{H}/../brake/template.html").read()
board_css = bt[bt.index("/* 순위판 (#board)"):bt.index("</style>")]
board_css = board_css.replace("#s-board{padding:0;", "#s-board{padding:0 !important;")
h2c = open(f"{H}/../lt/vendor/node_modules/html2canvas/dist/html2canvas.min.js").read().replace("</script", "<\\/script")
J = lambda o: json.dumps(o, ensure_ascii=False)
s = open(f"{H}/template.html").read()
s = (s.replace("/*__BOARDCSS__*/", board_css).replace("/*__H2C__*/", h2c)
      .replace("__LOGOW__", b64(f"{H}/../assets/logo_en_white.png", "image/png")).replace("__LOGO__", b64(f"{H}/../assets/logo_en.png", "image/png"))
      .replace("__QR__", b64(f"{H}/out/qr_count.png", "image/png")).replace('SHEET_URL: ""', f'SHEET_URL: "{SHEET}"'))
open(f"{H}/out/index.html", "w").write(s)
F = "/home/claude/xb/fonts/node_modules/@fontsource"
loc = "".join(f'<link rel="stylesheet" href="file://{F}/{x}">' for x in ["noto-sans-kr/400.css", "noto-sans-kr/700.css", "noto-sans-kr/900.css", "jetbrains-mono/700.css"])
m = s.replace(f'SHEET_URL: "{SHEET}"', 'SHEET_URL: "https://mock.sheet.test/exec"').replace("</head>", loc + "</head>")
open(f"{H}/out/index_mock.html", "w").write(m)
print("built", os.path.getsize(f"{H}/out/index.html") // 1024, "KB")
