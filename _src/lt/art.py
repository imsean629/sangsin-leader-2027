# -*- coding: utf-8 -*-
"""캐릭터 삽화 5종 (오리지널 SVG, 4:5). 글자·로고·테두리 없음.
생성 이미지(PNG/JPG)로 바꾸려면 lt/img/<유형코드>.png 를 두면 빌드 시 자동 교체된다."""

W, H = 400, 500
INKC = "#1E1A17"


def defs(uid):
    return f'''<defs>
<filter id="brush{uid}" x="-5%" y="-5%" width="110%" height="110%">
  <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="{len(uid) * 7}" result="n"/>
  <feDisplacementMap in="SourceGraphic" in2="n" scale="5" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="grain{uid}"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" result="g"/>
  <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.10 0"/>
  <feComposite in2="SourceGraphic" operator="in"/></filter>
</defs>'''


def strokes(color, rows, opacity=0.18, w=10):
    out = ""
    for (x1, y1, x2, y2) in rows:
        out += f'<path d="M{x1} {y1} Q{(x1 + x2) / 2} {y1 - 8} {x2} {y2}" stroke="{color}" stroke-width="{w}" stroke-linecap="round" opacity="{opacity}" fill="none"/>'
    return out


def eyes(lx, rx, y, dx=0, dy=0, size=6, lid=False):
    s = ""
    for x in (lx, rx):
        s += f'<ellipse cx="{x}" cy="{y}" rx="{size + 3}" ry="{size}" fill="#FBF7F0"/>'
        s += f'<circle cx="{x + dx}" cy="{y + dy}" r="{size - 1}" fill="{INKC}"/>'
        s += f'<circle cx="{x + dx + 2}" cy="{y + dy - 2}" r="1.6" fill="#FFFFFF"/>'
        if lid:
            s += f'<path d="M{x - size - 4} {y - 1} Q{x} {y - size - 5} {x + size + 4} {y - 1}" stroke="{INKC}" stroke-width="3" fill="none"/>'
    return s


def wrap(uid, body):
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice" '
            f'role="img" aria-hidden="true" style="display:block;width:100%;height:100%;">{defs(uid)}'
            f'<g filter="url(#brush{uid})"><g transform="translate(-8 -10) scale(1.04)">{body}</g></g>'
            f'<rect width="{W}" height="{H}" fill="#000" filter="url(#grain{uid})" opacity="0.6"/></svg>')


# ------------------------------------------------------------------ 항해장
def art_N():
    u = "N"
    sk, sk2 = "#E8B992", "#C98F68"
    b = f'''
<linearGradient id="skyN" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22325E"/><stop offset="0.55" stop-color="#C77A55"/><stop offset="0.72" stop-color="#F7CF6E"/></linearGradient>
<rect width="400" height="320" fill="url(#skyN)"/>
<circle cx="322" cy="300" r="44" fill="#FFE39A"/><circle cx="322" cy="300" r="70" fill="#FFE39A" opacity="0.25"/>
{strokes("#FFF1C2", [(200, 250, 390, 248), (230, 270, 400, 268), (40, 120, 220, 112)], 0.35, 6)}
<rect y="300" width="400" height="200" fill="#2C4A6B"/>
{strokes("#F7CF6E", [(250, 318, 390, 320), (270, 336, 380, 338), (290, 352, 370, 354)], 0.7, 5)}
<path d="M0 430 L400 410 L400 500 L0 500 Z" fill="#6B4A2E"/>
<path d="M30 438 L250 426 L262 470 L36 486 Z" fill="#E9D7AE"/>
<path d="M60 450 Q110 440 150 456 T230 446 M70 468 L120 464 M160 470 L210 462" stroke="#8C6A3E" stroke-width="3" fill="none"/>
<circle cx="200" cy="452" r="7" fill="none" stroke="#B8860B" stroke-width="3"/>
<path d="M78 500 L84 352 Q100 316 150 306 L250 306 Q300 316 316 352 L322 500 Z" fill="#1E2B45"/>
<path d="M150 306 L200 360 L250 306 L236 300 L200 334 L164 300 Z" fill="#D4A62A"/>
<path d="M250 330 Q300 322 352 296" stroke="#1E2B45" stroke-width="36" stroke-linecap="round" fill="none"/>
<path d="M348 300 L378 286 Q386 284 384 292 L360 304 Z" fill="{sk}"/>
<circle cx="360" cy="298" r="13" fill="{sk}"/>
<rect x="182" y="262" width="36" height="50" fill="{sk2}"/>
<path d="M146 168 L152 252 L178 286 L222 286 L248 252 L254 168 L234 132 L166 132 Z" fill="{sk}"/>
<path d="M140 176 Q136 118 200 108 Q262 112 260 176 Q252 148 228 140 Q198 152 168 142 Q148 150 140 176 Z" fill="#D8DDE3"/>
<path d="M150 150 Q170 130 210 128" stroke="#FFFFFF" stroke-width="5" opacity="0.7" fill="none"/>
<path d="M163 196 L190 192 M210 192 L238 196" stroke="#8E949C" stroke-width="5" stroke-linecap="round"/>
{eyes(178, 222, 210, dx=4, size=6)}
<path d="M200 214 L196 240 L206 242" stroke="{sk2}" stroke-width="3" fill="none"/>
<path d="M186 260 Q200 266 216 258" stroke="#8C3F2E" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M162 226 L168 236 M238 226 L232 236" stroke="{sk2}" stroke-width="2"/>'''
    return wrap(u, b)


# ------------------------------------------------------------------ 갑판장
def art_B():
    u = "B"
    sk, sk2 = "#D8A47A", "#B57F57"
    b = f'''
<linearGradient id="bgB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9ED6CF"/><stop offset="0.5" stop-color="#2D9A90"/><stop offset="1" stop-color="#0E5C57"/></linearGradient>
<rect width="400" height="500" fill="url(#bgB)"/>
{strokes("#E6FFFB", [(10, 60, 180, 50), (220, 90, 390, 80)], 0.3, 8)}
<path d="M0 360 L400 340 L400 500 L0 500 Z" fill="#137A71"/>
<path d="M0 392 L400 374 M0 430 L400 414 M0 468 L400 454" stroke="#0B514C" stroke-width="4"/>
<g opacity="0.85"><circle cx="58" cy="292" r="18" fill="#0B4440"/><path d="M30 360 Q36 318 58 314 Q80 318 86 360 Z" fill="#0B4440"/>
<circle cx="108" cy="300" r="16" fill="#0B4440"/><path d="M84 362 Q90 324 108 320 Q126 324 132 362 Z" fill="#0B4440"/></g>
<path d="M-10 250 Q120 300 170 420" stroke="#C9A46A" stroke-width="16" fill="none"/>
<path d="M-10 250 Q120 300 170 420" stroke="#8C6A3E" stroke-width="16" stroke-dasharray="6 10" fill="none"/>
<ellipse cx="330" cy="470" rx="62" ry="22" fill="none" stroke="#C9A46A" stroke-width="14"/>
<ellipse cx="330" cy="462" rx="40" ry="14" fill="none" stroke="#B08A50" stroke-width="12"/>
<path d="M90 500 L98 368 Q120 330 176 320 L240 320 Q296 330 314 368 L320 500 Z" fill="#F2EFE6"/>
<path d="M104 410 L312 410 M100 446 L316 446 M98 482 L318 482" stroke="#2D6FA3" stroke-width="10"/>
<path d="M260 352 Q300 320 316 250" stroke="#F2EFE6" stroke-width="40" stroke-linecap="round" fill="none"/>
<path d="M298 236 Q300 206 314 204 L318 228 L322 196 Q330 192 334 198 L332 228 L340 200 Q348 198 350 206 L344 236 L354 216 Q362 216 360 226 L346 262 Q330 278 306 268 Z" fill="{sk}"/>
<rect x="186" y="278" width="40" height="46" fill="{sk2}"/>
<circle cx="206" cy="210" r="76" fill="{sk}"/>
<path d="M160 160 Q190 140 236 150" stroke="#FFFFFF" stroke-width="7" opacity="0.4" fill="none"/>
<path d="M136 226 Q140 296 206 300 Q272 296 276 226 Q262 262 206 268 Q150 262 136 226 Z" fill="#4A3A30"/>
<path d="M186 254 Q206 264 228 254" stroke="#F2E2D2" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M170 188 L194 184 M220 184 L244 188" stroke="#4A3A30" stroke-width="6" stroke-linecap="round"/>
{eyes(182, 230, 206, dx=-2, size=6)}
<path d="M206 214 Q200 230 210 236" stroke="{sk2}" stroke-width="3" fill="none"/>
<circle cx="164" cy="232" r="9" fill="#E07A5F" opacity="0.35"/><circle cx="248" cy="232" r="9" fill="#E07A5F" opacity="0.35"/>
<ellipse cx="130" cy="214" rx="10" ry="16" fill="{sk}"/><ellipse cx="282" cy="214" rx="10" ry="16" fill="{sk}"/>'''
    return wrap(u, b)


# ------------------------------------------------------------------ 선발대장
def art_S():
    u = "S"
    sk, sk2 = "#F1C7A6", "#D99E7C"
    fr = "".join(f'<circle cx="{x}" cy="{y}" r="2.4" fill="#B5643E" opacity="0.8"/>'
                 for x, y in ((174, 238), (182, 244), (168, 246), (190, 238), (230, 238), (238, 244), (224, 246), (246, 238)))
    b = f'''
<linearGradient id="bgS" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD7C2"/><stop offset="0.55" stop-color="#F48C6D"/><stop offset="0.56" stop-color="#3D7FA6"/><stop offset="1" stop-color="#1F5778"/></linearGradient>
<rect width="400" height="500" fill="url(#bgS)"/>
{strokes("#FFF0E6", [(20, 80, 200, 70), (180, 130, 380, 120)], 0.4, 8)}
{strokes("#BFE3F5", [(250, 310, 390, 312), (220, 350, 380, 352), (260, 400, 390, 402)], 0.55, 5)}
<path d="M0 330 L210 330 L210 500 L0 500 Z" fill="#E37356"/>
<path d="M0 362 L210 362 M0 398 L210 398 M0 436 L210 436 M0 474 L210 474" stroke="#B9543A" stroke-width="4"/>
<rect x="196" y="330" width="16" height="170" fill="#9C4430"/>
<g transform="translate(18 0)">
<path d="M60 500 L72 360 Q96 316 160 300 L232 300 Q262 306 280 330 L290 380 L230 500 Z" fill="#F5F0E3"/>
<path d="M150 300 L196 300 L188 340 Z" fill="#E37356"/>
<path d="M250 340 Q300 380 300 410" stroke="#F5F0E3" stroke-width="36" stroke-linecap="round" fill="none"/>
<path d="M120 380 Q190 420 260 418" stroke="#F5F0E3" stroke-width="34" stroke-linecap="round" fill="none"/>
<g transform="rotate(-14 210 220)">
<rect x="190" y="268" width="34" height="40" fill="{sk2}"/>
<path d="M150 180 Q150 280 207 296 Q264 280 264 180 Q264 130 207 126 Q150 130 150 180 Z" fill="{sk}"/>
<path d="M146 186 Q140 112 208 108 Q276 112 268 188 Q258 150 232 140 Q206 158 176 144 Q156 158 146 186 Z" fill="#A2472A"/>
<path d="M166 132 Q192 118 230 122" stroke="#D07A50" stroke-width="5" fill="none" opacity="0.8"/>
<path d="M172 196 L196 194 M218 194 L242 196" stroke="#7A3520" stroke-width="5" stroke-linecap="round"/>
{eyes(184, 230, 214, dx=2, dy=4, size=6)}
{fr}
<path d="M207 220 L202 244 L212 246" stroke="{sk2}" stroke-width="3" fill="none"/>
<path d="M190 264 Q208 274 226 262" stroke="#9C3B2A" stroke-width="4" fill="none" stroke-linecap="round"/>
</g>
<circle cx="300" cy="420" r="15" fill="{sk}"/><circle cx="262" cy="424" r="15" fill="{sk}"/>
</g>
<g transform="translate(318 438)">
<path d="M-40 0 L40 0 L28 18 L-28 18 Z" fill="#FFFFFF" stroke="#7A3520" stroke-width="3"/>
<path d="M0 0 L0 -46" stroke="#7A3520" stroke-width="3"/>
<path d="M2 -44 L30 -14 L2 -10 Z" fill="#F48C6D"/>
<path d="M-56 26 Q0 34 56 26" stroke="#BFE3F5" stroke-width="4" fill="none"/>
</g>'''
    return wrap(u, b)


# ------------------------------------------------------------------ 수리장
def art_R():
    u = "R"
    sk, sk2 = "#D9AE8A", "#A77A58"
    wr = '<path d="M176 160 Q198 154 222 160 M172 176 Q198 170 226 176" stroke="#A77A58" stroke-width="2.5" fill="none"/>'
    b = f'''
<radialGradient id="lampR" cx="0.22" cy="0.2" r="0.75"><stop offset="0" stop-color="#E8C5FF"/><stop offset="0.25" stop-color="#9B6BD6"/><stop offset="1" stop-color="#1F1533"/></radialGradient>
<rect width="400" height="500" fill="url(#lampR)"/>
{"".join(f'<rect x="{x}" y="0" width="58" height="500" fill="#3A2A44" opacity="0.55"/><path d="M{x} 0 L{x} 500" stroke="#1A1226" stroke-width="3"/>' for x in range(0, 400, 60))}
<path d="M86 40 L86 70" stroke="#2A1E1A" stroke-width="4"/>
<path d="M66 70 L106 70 L100 128 L72 128 Z" fill="#2A1E1A"/>
<rect x="74" y="78" width="24" height="44" fill="#F3D9FF"/>
<circle cx="86" cy="100" r="44" fill="#E8C5FF" opacity="0.35"/>
<path d="M330 200 L336 236 L326 270" stroke="#14101C" stroke-width="6" fill="none"/>
<path d="M332 270 Q326 284 332 290 Q338 284 332 270 Z M330 306 Q324 320 330 326 Q336 320 330 306 Z" fill="#9FD3F2"/>
<path d="M300 236 L364 236 L360 262 L304 262 Z" fill="#8C6A4A" stroke="#14101C" stroke-width="3"/>
<path d="M80 500 L92 372 Q118 330 170 318 L238 318 Q290 330 312 372 L322 500 Z" fill="#4E5D4A"/>
<path d="M140 340 L150 500 M264 340 L254 500" stroke="#3A4636" stroke-width="8"/>
<path d="M276 370 Q316 320 318 266" stroke="#4E5D4A" stroke-width="36" stroke-linecap="round" fill="none"/>
<circle cx="318" cy="256" r="16" fill="{sk}"/>
<path d="M316 252 L284 200" stroke="#7A5A3C" stroke-width="9" stroke-linecap="round"/>
<rect x="262" y="180" width="40" height="22" rx="3" fill="#6C6F78" transform="rotate(-32 282 191)"/>
<path d="M120 400 Q150 340 120 300" stroke="#4E5D4A" stroke-width="34" stroke-linecap="round" fill="none"/>
<circle cx="120" cy="292" r="14" fill="{sk}"/>
<rect x="186" y="288" width="34" height="36" fill="{sk2}"/>
<ellipse cx="203" cy="206" rx="58" ry="92" fill="{sk}"/>
{wr}
<path d="M146 186 Q140 156 152 130 L160 186 Z M260 186 Q266 156 254 130 L246 186 Z" fill="#C9C7C2"/>
<path d="M156 120 Q203 100 250 120" stroke="#C9C7C2" stroke-width="6" fill="none" opacity="0.8"/>
<path d="M170 192 L194 190 M212 190 L236 192" stroke="#C9C7C2" stroke-width="6" stroke-linecap="round"/>
{eyes(183, 223, 210, dx=0, dy=2, size=5, lid=True)}
<circle cx="183" cy="210" r="17" fill="none" stroke="#2A1E1A" stroke-width="3.5"/>
<circle cx="223" cy="210" r="17" fill="none" stroke="#2A1E1A" stroke-width="3.5"/>
<path d="M200 210 L206 210" stroke="#2A1E1A" stroke-width="3.5"/>
<path d="M203 222 L198 248 L208 250" stroke="{sk2}" stroke-width="3" fill="none"/>
<path d="M203 258 Q176 252 160 262 Q150 290 140 308 Q166 286 182 272 Q194 266 203 268 Q212 266 224 272 Q240 286 266 308 Q256 290 246 262 Q230 252 203 258 Z" fill="#D8D6D0"/>
<path d="M188 286 Q203 292 218 286" stroke="#7A4A3A" stroke-width="3" fill="none"/>
<path d="M164 230 L170 244 M242 230 L236 244 M180 268 L176 280" stroke="#A77A58" stroke-width="2"/>'''
    return wrap(u, b)


# ------------------------------------------------------------------ 파수장
def art_W():
    u = "W"
    sk, sk2 = "#F2CDB2", "#D9A587"
    b = f'''
<linearGradient id="skyW" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#DDF0FB"/><stop offset="0.55" stop-color="#86BFE6"/><stop offset="1" stop-color="#4C88BD"/></linearGradient>
<rect width="400" height="500" fill="url(#skyW)"/>
<path d="M250 90 Q280 60 320 74 Q350 50 384 72 Q410 76 400 110 L240 120 Q230 100 250 90 Z" fill="#45566E" opacity="0.85"/>
<path d="M300 120 Q330 104 370 112 Q404 116 400 140 L290 144 Z" fill="#33445C" opacity="0.8"/>
<path d="M352 124 L340 150 L352 150 L342 176" stroke="#FFF6B0" stroke-width="3" fill="none"/>
{strokes("#FFFFFF", [(20, 70, 180, 60), (40, 150, 200, 144), (10, 230, 140, 226)], 0.5, 8)}
<path d="M0 400 L400 380 L400 500 L0 500 Z" fill="#7A5638"/>
<path d="M0 392 L400 372" stroke="#5A3E28" stroke-width="10"/>
{"".join(f'<rect x="{x}" y="{392 - x * 0.05:.0f}" width="12" height="120" fill="#5A3E28"/>' for x in range(20, 400, 70))}
<path d="M90 500 L100 368 Q126 328 176 318 L236 318 Q286 328 306 368 L314 500 Z" fill="#2F5E86"/>
<path d="M176 318 L206 352 L236 318" stroke="#DDF0FB" stroke-width="6" fill="none"/>
<rect x="188" y="286" width="34" height="38" fill="{sk2}"/>
<path d="M150 182 Q150 248 205 296 Q260 248 260 182 Q260 132 205 126 Q150 132 150 182 Z" fill="{sk}"/>
<path d="M144 196 Q134 112 206 104 Q278 112 266 196 Q262 166 250 154 L238 172 L226 150 L210 170 L196 150 L182 170 L170 154 Q156 168 144 196 Z" fill="#2B2422"/>
<path d="M258 180 Q290 220 280 280 Q272 320 290 360 Q296 400 282 430" stroke="#2B2422" stroke-width="22" fill="none" stroke-linecap="round"/>
<path d="M270 250 L292 262 M272 290 L294 300 M276 330 L298 338 M282 370 L302 376" stroke="#4A3E3A" stroke-width="4"/>
<circle cx="284" cy="436" r="9" fill="#86BFE6"/>
<path d="M172 200 L194 198" stroke="#2B2422" stroke-width="4" stroke-linecap="round"/>
{eyes(184, 230, 216, dx=3, size=6)}
<path d="M206 222 L202 246 L212 248" stroke="{sk2}" stroke-width="3" fill="none"/>
<path d="M192 266 Q206 272 220 264" stroke="#B4534A" stroke-width="4" fill="none" stroke-linecap="round"/>
<circle cx="172" cy="240" r="8" fill="#F09A8A" opacity="0.35"/>
<g transform="rotate(-8 230 214)">
<rect x="222" y="196" width="150" height="34" rx="6" fill="#B08A50" stroke="#5A3E28" stroke-width="3"/>
<rect x="222" y="194" width="30" height="38" rx="5" fill="#8C6A3E"/>
<rect x="300" y="192" width="14" height="42" fill="#D4A62A"/>
<ellipse cx="372" cy="213" rx="8" ry="19" fill="#CFE8F7" stroke="#5A3E28" stroke-width="3"/>
</g>
<path d="M290 350 Q290 290 250 240" stroke="#2F5E86" stroke-width="34" stroke-linecap="round" fill="none"/>
<circle cx="258" cy="236" r="15" fill="{sk}"/>
<path d="M300 400 Q340 330 336 244" stroke="#2F5E86" stroke-width="30" stroke-linecap="round" fill="none"/>
<circle cx="338" cy="230" r="14" fill="{sk}"/>'''
    return wrap(u, b)


ARTS = {"N": art_N, "B": art_B, "S": art_S, "R": art_R, "W": art_W}
