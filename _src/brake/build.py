import base64, os, segno
H = os.path.dirname(os.path.abspath(__file__))
URL = "https://imsean629.github.io/sangsin-leader-2027/brake/"
q = segno.make(URL, error='q')
q.save(f"{H}/out/qr_brake.png", scale=20, border=2, dark="#0B1B36", light="#FFFFFF")
q.save(f"{H}/out/qr_brake.svg", scale=10, border=2, dark="#0B1B36", light="#FFFFFF")
b64 = lambda p, m: f"data:{m};base64," + base64.b64encode(open(p, "rb").read()).decode()
h2c = open(f"{H}/../lt/vendor/node_modules/html2canvas/dist/html2canvas.min.js").read().replace("</script", "<\\/script")
s = open(f"{H}/template.html").read()
s = (s.replace("/*__H2C__*/", h2c).replace("__LOGOW__", b64(f"{H}/../assets/logo_en_white.png", "image/png"))
      .replace("__LOGO__", b64(f"{H}/../assets/logo_en.png", "image/png")).replace("__QR__", b64(f"{H}/out/qr_brake.png", "image/png")))
open(f"{H}/out/index.html", "w").write(s)
print(f"{H}/out/index.html", os.path.getsize(f"{H}/out/index.html") // 1024, "KB")
