"""
링크 공유용 썸네일(OG 이미지)을 만든다.

카톡·슬랙·트위터에 semoji.net 주소를 붙이면 뜨는 그림이다.
없으면 밋밋한 글자 링크만 나간다.

생김새는 사이트를 그대로 축소한 것이다. 종이색 바탕, 위에 세모지 표제와
열람실 번호, 가운데 큰 제목, 아래 한 줄 설명, 오른쪽 아래에 붉은 직인.

글은 각 페이지의 <title> 과 <meta name="description"> 에서 읽는다.
그러니 여기 따로 적을 것이 없다. 페이지를 고치면 그림도 따라 바뀐다.

만드는 것
    og/<슬러그>.png   1200x630   페이지마다 한 장
    og-preview.png    확인용, 배포에는 안 씀

사용법:
    python scripts/build_og.py
"""
import io
import pathlib
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "og"

W, H = 1200, 630
M = 76                      # 바깥 여백

PAPER = (235, 237, 230)     # --paper
INK = (27, 29, 25)          # --ink
INK2 = (69, 74, 63)         # --ink-2
MUTED = (120, 126, 111)     # --muted
RULE = (196, 201, 185)      # --rule
SEAL = (190, 59, 46)        # --seal

# 바탕(TTC)은 사이트의 Hahmlet 과 같은 명조 계열이다.
SERIF = ("C:/Windows/Fonts/batang.ttc", 0)
SANS = ("C:/Windows/Fonts/malgun.ttf", 0)
SANS_B = ("C:/Windows/Fonts/malgunbd.ttf", 0)

SKIP = {"data", "scripts", "og"}

# 열람실이 아닌 쪽. 본문에 「제N호」가 나와도 번호로 읽지 않는다.
NOT_A_ROOM = {"about", "contact", "privacy"}


def font(spec, size):
    path, idx = spec
    return ImageFont.truetype(path, size, index=idx)


def wrap(d, text, f, width, limit):
    """폭에 맞춰 줄을 나눈다. 한글은 띄어쓰기가 없을 수 있어 글자 단위까지 내려간다."""
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if d.textlength(trial, font=f) <= width or not cur:
            cur = trial
            continue
        # 되도록 띄어쓰기에서 끊는다
        cut = cur.rfind(" ")
        if cut > len(cur) * 0.5:
            lines.append(cur[:cut])
            cur = cur[cut + 1:] + ch
        else:
            lines.append(cur)
            cur = ch
        if len(lines) == limit:
            return lines, True
    if cur:
        lines.append(cur)
    return lines[:limit], len(lines) > limit


def seal(size):
    """파비콘과 같은 붉은 직인. 큰 캔버스에 그려 줄인다."""
    ss, s = 6, size * 6
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, s, s], fill=SEAL)
    d.ellipse([s * .11, s * .11, s * .89, s * .89], outline=PAPER, width=int(s * .028))
    f = font(SANS_B, int(s * .46))
    l, t, r, b = d.textbbox((0, 0), "세", font=f)
    d.text(((s - r - l) / 2, (s - b - t) / 2), "세", font=f, fill=PAPER)
    return img.resize((size, size), Image.LANCZOS)


def card(title, kicker, desc):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # 머리 — 세모지 표제와 열람실 번호
    f_mark = font(SERIF, 42)
    d.text((M, M - 8), "세모지", font=f_mark, fill=INK)
    f_sub = font(SANS, 19)
    d.text((M + d.textlength("세모지", font=f_mark) + 16, M + 12),
           "세상에 모든 쓸데없는 지식", font=f_sub, fill=MUTED)
    f_kick = font(SANS, 21)
    d.text((W - M - d.textlength(kicker, font=f_kick), M + 8),
           kicker, font=f_kick, fill=SEAL if kicker.startswith("제") else MUTED)

    top = M + 62          # 머리 아래 가로줄
    bot = H - M - 40      # 발 위 가로줄
    d.line([(M, top), (W - M, top)], fill=RULE, width=2)
    d.line([(M, bot), (W - M, bot)], fill=RULE, width=2)

    # 제목 — 오른쪽 직인 자리를 비우고 폭에 맞을 때까지 줄인다.
    # 두 줄이 되면 설명이 들어갈 자리가 없어지므로 그때는 더 작게 시작한다.
    box = W - M * 2 - 160
    for start in (96, 76):
        for size in range(start, 47, -4):
            f = font(SERIF, size)
            lines, over = wrap(d, title, f, box, 2)
            if not over:
                break
        if len(lines) == 1 or not desc or start == 76:
            break
    lh = int(size * 1.30)
    t_h = lh * len(lines)

    # 설명 — 남는 자리만큼만 넣는다. 넘치면 줄을 줄인다.
    f_d = font(SANS, 25)
    d_lh, gap = 41, 30
    room = (bot - 34) - (top + 34) - t_h - gap
    n = max(0, min(3, room // d_lh))
    d_lines = wrap(d, desc, f_d, W - M * 2 - 190, n)[0] if (desc and n) else []
    d_h = d_lh * len(d_lines)

    # 제목과 설명을 통째로 두 가로줄 사이에 앉힌다
    y = top + ((bot - top) - (t_h + (gap + d_h if d_lines else 0))) // 2
    for ln in lines:
        d.text((M, y), ln, font=f, fill=INK)
        y += lh
    y += gap
    for ln in d_lines:
        d.text((M, y), ln, font=f_d, fill=INK2)
        y += d_lh

    # 발 — 출처와 직인
    f_f = font(SANS, 20)
    d.text((M, H - M - 22), "semoji.net · 공공데이터포털 원본에서 직접 계산",
           font=f_f, fill=MUTED)
    sz = 112
    s = seal(sz)
    img.paste(s, (W - M - sz, bot - sz - 22), s)
    return img


def read(f):
    s = io.open(f, encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    de = re.search(r'name="description" content="(.*?)"', s, re.S)
    no = re.search(r"제\s*(\d+)\s*호", s)
    title = (t.group(1) if t else "세모지").strip()
    title = re.sub(r"\s*[—-]\s*세모지$", "", title)
    return title, (de.group(1).strip() if de else ""), (no.group(1) if no else None)


def main():
    OUT.mkdir(exist_ok=True)
    targets = [("", ROOT / "index.html")]
    for p in sorted(ROOT.iterdir()):
        if p.is_dir() and p.name not in SKIP and not p.name.startswith(".") \
                and (p / "index.html").exists():
            targets.append((p.name, p / "index.html"))

    made = []
    for slug, f in targets:
        title, desc, no = read(f)
        if slug == "":
            title, kicker = "세상에 모든 쓸데없는 지식", "열람실 %d곳 개관" % (len(targets) - 4)
        elif no and slug not in NOT_A_ROOM:
            kicker = f"제{no}호 열람실"
        else:
            kicker = "세모지"
        card(title, kicker, desc).save(OUT / f"{slug or 'index'}.png")
        made.append((slug or "index", title))
        print(f"  og/{slug or 'index'}.png   {kicker}  {title}")

    # 확인용 — 앞 네 장을 줄여서 한 장에
    cols, tw = 2, 560
    th = int(tw * H / W)
    sheet = Image.new("RGB", (cols * tw + 30, 2 * th + 30), (255, 255, 255))
    for i, (name, _) in enumerate(made[:4]):
        im = Image.open(OUT / f"{name}.png").resize((tw, th), Image.LANCZOS)
        sheet.paste(im, ((i % cols) * (tw + 10) + 10, (i // cols) * (th + 10) + 10))
    sheet.save(ROOT / "og-preview.png")
    print(f"\n{len(made)}장 만들었습니다. 확인용 og-preview.png (배포에는 쓰지 않음)")


if __name__ == "__main__":
    main()
