"""
세모지 파비콘을 만든다.

마크는 사이트의 정체성인 **붉은 직인**이다. 열람실마다 찍히는 도장(取消·閉業·非常)의
축소판으로, 붉은 원 안에 「세」 한 글자를 넣었다.

16px 에서도 읽혀야 하므로 원은 채우고 글자는 종이색으로 뺐다.
직인의 이중 테두리는 32px 이상에서만 보이도록 아주 얇게 넣는다.

만드는 것
    favicon.ico          16 / 32 / 48  — 구형 브라우저와 즐겨찾기
    favicon.svg          벡터          — 최신 브라우저가 우선 사용
    apple-touch-icon.png 180x180       — iOS 홈 화면
    favicon-preview.png  미리보기       — 눈으로 확인용, 배포에는 안 씀

사용법:
    python scripts/build_favicon.py
"""
import pathlib

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent

SEAL = (190, 59, 46)      # --seal  #BE3B2E
PAPER = (235, 237, 230)   # --paper #EBEDE6
FONT = "C:/Windows/Fonts/malgunbd.ttf"
CHAR = "세"

SS = 8  # 수퍼샘플링 배수


def draw_icon(size: int, ring: bool = True) -> Image.Image:
    """size 픽셀짜리 아이콘 한 장. 큰 캔버스에 그린 뒤 줄여 계단을 없앤다."""
    S = size * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    pad = S * 0.015
    d.ellipse([pad, pad, S - pad, S - pad], fill=SEAL)

    # 직인의 이중 테두리. 작은 크기에서는 뭉개지므로 생략한다.
    if ring:
        w = max(1, int(S * 0.035))
        inset = S * 0.11
        d.ellipse([inset, inset, S - inset, S - inset], outline=PAPER, width=w)

    # 글자를 원 안에 맞춘다
    target = S * (0.52 if ring else 0.76)
    fs = int(target)
    for _ in range(40):
        f = ImageFont.truetype(FONT, fs)
        l, t, r, b = d.textbbox((0, 0), CHAR, font=f)
        if max(r - l, b - t) <= target:
            break
        fs -= max(1, fs // 20)
    f = ImageFont.truetype(FONT, fs)
    l, t, r, b = d.textbbox((0, 0), CHAR, font=f)
    d.text(((S - (r + l)) / 2, (S - (b + t)) / 2), CHAR, font=f, fill=PAPER)

    return img.resize((size, size), Image.LANCZOS)


SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="31" fill="#BE3B2E"/>
  <circle cx="32" cy="32" r="24.5" fill="none" stroke="#EBEDE6" stroke-width="1.6"/>
  <text x="32" y="33" fill="#EBEDE6" font-size="30" font-weight="700"
        text-anchor="middle" dominant-baseline="central"
        font-family="'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif">{CHAR}</text>
</svg>
"""


def main():
    # 16px 은 테두리를 빼야 글자가 산다
    ico_sizes = [(16, False), (32, True), (48, True)]
    imgs = [draw_icon(s, ring) for s, ring in ico_sizes]
    # PIL 은 「기준 이미지」보다 큰 크기를 ico 에 넣지 않는다.
    # 16px 를 기준으로 저장하면 16x16 한 장만 들어가고 32·48 은 조용히 사라진다.
    # 2026-09-05에 favicon.ico 안에 16x16 하나뿐인 것을 발견해 고쳤다 —
    # 구글은 파비콘을 48의 배수 정사각형으로 요구해서, 16만 있으면
    # 검색 결과에 지구본이 뜬다. **가장 큰 것을 기준으로 저장한다.**
    imgs[-1].save(ROOT / "favicon.ico", format="ICO",
                  sizes=[(s, s) for s, _ in ico_sizes],
                  append_images=imgs[:-1])
    print("favicon.ico       16 / 32 / 48")

    (ROOT / "favicon.svg").write_text(SVG, encoding="utf-8")
    print("favicon.svg       벡터")

    draw_icon(180).save(ROOT / "apple-touch-icon.png")
    print("apple-touch-icon.png  180x180")

    # 미리보기 — 실제 크기 그대로 늘어놓고, 아래에 확대본
    sheet = Image.new("RGBA", (420, 150), PAPER + (255,))
    x = 16
    for s in (16, 32, 48, 64):
        ic = draw_icon(s, ring=(s > 16))
        sheet.paste(ic, (x, 16), ic)
        big = ic.resize((64, 64), Image.NEAREST)
        sheet.paste(big, (x, 76), big)
        x += s + 24
    sheet.save(ROOT / "favicon-preview.png")
    print("favicon-preview.png   확인용 (배포에는 쓰지 않음)")


if __name__ == "__main__":
    main()
