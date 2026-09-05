"""
문화예술법인.csv 에서 제24호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py cultural_art_corporations 문화예술법인

사용법:
    python scripts/analyze_corp.py

※ 조심할 것

1. **법인명·사업장명의 개별 값을 옮기지 않는다.** 종교 법인이 많아서
   이름을 그대로 옮기면 특정 단체를 가리키게 된다. 세는 것으로 충분하다.

2. **전화번호 칸이 있다.** 출력에 원문을 찍는 자리는 전부 mask() 를 거친다.

3. **「허가증 이면 기재」를 잘못이라고 쓰지 않는다.** 종이 허가증에 조건을
   적어 두고 전산에는 그 사실만 남긴 것이다. 담당자가 게으른 것이 아니라
   **종이가 원본이고 데이터가 사본이던 시절의 자국**이다. 원본에 이유는 없다.

4. **「딴 데 있다」 판정은 낱말로 한다.** 이면·뒷면·별지·별첨·참조·참고·
   붙임·첨부·기재 중 하나가 들어간 값을 센다. 「관계 법규와 제 규정 준수」처럼
   실제 조건을 적은 짧은 값도 있으므로 짧다는 것만으로 세지 않는다.

5. **허가조건은 65.3%가 비어 있다.** 비율의 분모는 채워진 1,370곳이다.
"""
import io
import sys
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "문화예술법인.csv"
OUT = ROOT / "data" / "분석결과_문화예술법인.txt"

_MASK = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "(이메일)"),
    (re.compile(r"\d{2,3}-\d{2}-\d{5}"), "(사업자번호)"),
    (re.compile(r"\b0\d{1,2}-\d{3,4}-\d{4}\b"), "(전화번호)"),
]

ELSEWHERE = re.compile(r"이면|뒷면|뒤면|별지|별첨|참조|참고|붙임|첨부|기재")

# corporation/index.html 의 REF 배열과 같은 목록이어야 한다.
# 기계로 상위 10을 자르면 긴 법령 문구 두 개가 들어오는데, 페이지는 그것을
# 빼고 짧은 것만 싣는다(원문을 길게 옮기지 않는다는 규칙). 여기서 나머지를
# 계산하므로 한쪽만 고치면 페이지의 「그 밖에 N곳」이 틀어진다.
PAGE_REF = ["허가증 이면 기재", "비영리법인 설립허가증 뒷면에 기재", "허가서 이면 참조",
            "허가증 이면 참조", "설립허가증 뒷면에 기재", "법인 설립허가증 뒷면에 기재",
            "붙임", "별첨", "법인설립허가증 이면 참조", "이면기재"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def mask(t):
    t = str(t)
    for pat, rep in _MASK:
        t = pat.sub(rep, t)
    return t


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py cultural_art_corporations 문화예술법인` "
                         f"를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False, low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)

    cond = df["허가조건"]
    got = cond[cond != ""]

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳 (문화·예술·종교·문화재 비영리법인)")
    p(f"「허가조건」 적힌 곳 {len(got):,} ({100 * len(got) / n:.1f}%) · "
      f"빈칸 {n - len(got):,} ({100 * (n - len(got)) / n:.1f}%)")
    p(f"고유값 {got.nunique():,}가지 · 평균 {got.str.len().mean():.1f}자 · "
      f"최장 {got.str.len().max():,}자")

    p("")
    p("=== 조건이 여기 없다고 적은 칸 ===")
    p("판정: 이면·뒷면·별지·별첨·참조·참고·붙임·첨부·기재 중 하나가 든 값.")
    p("분모는 채워진 %s곳이다." % f"{len(got):,}")
    ref = got.str.contains(ELSEWHERE)
    p(f"「딴 데 있다」 {ref.sum():,} ({100 * ref.mean():.1f}%) · {got[ref].nunique():,}가지")
    p("")
    p("어떻게 적었나 — 상위 12")
    rv = got[ref].value_counts()
    for v, c in rv.head(12).items():
        p(f"  {c:4,}  {mask(v)[:70]}")
    shown = sum(rv.get(t, 0) for t in PAGE_REF)
    p(f"  (페이지에 실은 {len(PAGE_REF)}가지 합계 {shown:,} · "
      f"나머지 {got[ref].nunique() - len(PAGE_REF):,}가지 {ref.sum() - shown:,})")
    miss = [t for t in PAGE_REF if t not in rv.index]
    if miss:
        p(f"  !! 페이지에 있는데 데이터에 없는 값: {miss}")

    p("")
    p("=== 짧게 끝낸 칸 ===")
    short = got[got.str.len() <= 15]
    p(f"15자 이하 {len(short):,}건 ({100 * len(short) / len(got):.1f}%)")
    sv = short.value_counts()
    for v, c in sv.head(12).items():
        p(f"  {c:4,}  {mask(v)}")
    p(f"  (페이지에 실은 상위 12 합계 {sv.head(12).sum():,} · "
      f"나머지 {len(short) - sv.head(12).sum():,})")

    p("")
    p("=== 길게 적은 칸 ===")
    nl = got.str.contains(r"\r|\n")
    p(f"값 안에 줄바꿈이 든 것 {nl.sum():,}건 ({100 * nl.mean():.1f}%)")
    p(f"가장 긴 값 {got.str.len().max():,}자")
    p("※ 조건 원문은 옮기지 않는다. 담당자가 타이핑한 행정 문구이고 길다.")

    p("")
    p("=== 왜 만들었나 — 「법인설립목적」 ===")
    aim = df["법인설립목적"]
    p(f"채움 {100 * (aim != '').mean():.1f}% · 고유값 {aim.nunique():,}가지 "
      f"(전체 {n:,}곳) · 평균 {aim.str.len().mean():.1f}자 · 최장 {aim.str.len().max():,}자")
    one = aim[aim.str.len() == 1]
    p(f"한 글자로 적은 곳 {len(one):,}건 · "
      f"{', '.join('「' + x + '」' for x in sorted(one.unique()))}")
    p(f"5자 이하 {(aim.str.len() <= 5).sum():,}건")
    p("")
    p("5자 이하로 적은 값 — 상위 12")
    for v, c in aim[aim.str.len() <= 5].value_counts().head(12).items():
        p(f"  {c:4,}  {mask(v)}")
    p("※ 「111」이라고 적은 곳이 하나 있다. 제1호 모범음식점의 메뉴 칸과 같은 모양이다.")

    p("")
    p("=== 문화예술 법인인데 넷 중 하나가 종교다 ===")
    vc = df["문화체육업종명"].value_counts()
    for v, c in vc.items():
        p(f"  {c:5,} ({100 * c / n:4.1f}%)  {v}")
    rel = df["문화체육업종명"].str.startswith("종교").sum()
    p("")
    p(f"종교(사단)+종교(재단) = {rel:,} ({100 * rel / n:.1f}%)")
    sadan = df["문화체육업종명"].str.contains(r"\(사단\)").sum()
    p(f"사단법인 {sadan:,} ({100 * sadan / n:.1f}%) · "
      f"재단법인 {n - sadan:,} ({100 * (n - sadan) / n:.1f}%)")

    p("")
    p("=== 거의 죽지 않는다 ===")
    for v, c in df["영업상태명"].value_counts().items():
        p(f"  {c:5,} ({100 * c / n:4.1f}%)  {v}")
    lic = pd.to_numeric(df["인허가일자"].str[:4], errors="coerce")
    p("")
    p(f"가장 이른 허가 {int(lic.min())}년 · 가장 늦은 허가 {int(lic.max())}년")
    p("연도대별 허가")
    dec = (lic // 10 * 10).value_counts().sort_index()
    for y, c in dec.items():
        if pd.notna(y):
            p(f"  {int(y)}년대  {c:5,}")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
