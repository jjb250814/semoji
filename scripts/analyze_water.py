"""
비상급수시설.csv 에서 제29호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py civil_defense_water_facilities 비상급수시설

사용법:
    python scripts/analyze_water.py

※ 조심할 것

1. **분류는 이름으로 하는 것이라 어림값이다.** 「청수탕」을 목욕탕으로 세지만
   이름만 보고 판단한 것이다. 분류가 서로 겹칠 수 있어 합계가 100%를 넘는다.
   **본문에 「이름으로 나눈 어림값」이라고 반드시 밝힌다.**

2. **개별 시설을 지목하지 않는다.** 「청수탕」은 8곳이 함께 쓰는 이름이라
   옮겨도 한 곳을 가리키지 않는다. 한 곳만 쓰는 이름은 옮기지 않는다.
   비상급수시설의 위치를 콕 집어 알리는 것은 이 사이트가 할 일이 아니다.

3. **「비상시설위치」는 대부분 주소다.** 자유 입력처럼 보이지만 광맥이 아니다.
   주소는 옮기지 않는다.

4. **사용중지 비율을 「목욕탕이 없어져서」로 단정하지 않는다.**
   지정을 푼 이유는 데이터에 없다. 제17호 목욕장업과 나란히 두되 단정하지 않는다.
"""
import io
import sys
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "비상급수시설.csv"
OUT = ROOT / "data" / "분석결과_비상급수시설.txt"

# 이름으로 나눈 어림 분류. 서로 겹칠 수 있다.
CATS = [
    ("목욕탕 · 사우나", r"탕$|목욕|사우나|온천|찜질"),
    ("아파트 · 주택", r"아파트|빌라|연립|맨션|APT|주공|타운"),
    ("학교", r"학교|중학|고등|초등|대학"),
    ("공원 · 체육시설", r"공원|운동장|체육|수영장"),
    ("관공서", r"청$|시청|구청|군청|주민센터|행정복지|사무소|센터"),
    ("관정 · 우물", r"관정|우물|정호|지하수|약수"),
    ("병원 · 보건소", r"병원|의원|보건"),
    ("교회 · 사찰", r"교회|성당|절$|사찰|암자|종교"),
    ("공장 · 회사", r"공장|산업|㈜|주식회사"),
    ("농업시설", r"농업|농협|축사|축산|영농"),
    ("군 · 경찰 · 소방", r"부대|군부대|경찰|소방"),
]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py civil_defense_water_facilities 비상급수시설` "
                         f"를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False, low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    name = df["사업장명"]
    stop = df["상세영업상태명"] == "사용중지"
    yr = pd.to_numeric(df["인허가일자"].str[:4], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳 (민방위 비상급수시설)")
    p(f"사용 중 {(~stop).sum():,} ({100 * (~stop).mean():.1f}%) · "
      f"사용중지 {stop.sum():,} ({100 * stop.mean():.1f}%)")
    p(f"시설 이름 고유 {name.nunique():,}가지")
    p(f"지정 연도 {int(yr.min())}~{int(yr.max())} · 중앙값 {int(yr.median())}년")

    p("")
    p("=== 무엇이 비상급수시설인가 ===")
    p("이름으로 나눈 어림 분류다. 서로 겹칠 수 있어 합계가 100%를 넘는다.")
    p("")
    p(f"{'분류':16s} {'곳':>6s} {'비율':>7s} {'사용중지':>8s}")
    for lab, pat in CATS:
        m = name.str.contains(pat, regex=True)
        if not m.sum():
            continue
        p(f"{lab:16s} {m.sum():6,} {100 * m.mean():6.1f}% "
          f"{100 * stop[m].mean():7.1f}%")

    p("")
    p("=== 「탕」으로 끝나는 이름 ===")
    t = name[name.str.contains(r"탕$", regex=True)]
    p(f"{len(t):,}곳 · {t.nunique():,}가지")
    p("여러 곳이 함께 쓰는 이름만 옮긴다 — 상위 14")
    for v, c in t.value_counts().head(14).items():
        p(f"  {c:3,}  {v}")
    p(f"  (한 곳만 쓰는 이름 {(t.value_counts() == 1).sum():,}가지는 옮기지 않는다)")

    p("")
    p("=== 목욕탕이 가장 많이 사라졌다 ===")
    p("제17호 목욕장업과 나란히 두되, 지정을 푼 이유는 데이터에 없다.")
    p("")
    for lab, pat in CATS[:4]:
        m = name.str.contains(pat, regex=True)
        p(f"  {lab:16s} {m.sum():5,}곳 중 사용중지 {stop[m].sum():5,} "
          f"({100 * stop[m].mean():.1f}%)")
    p(f"  {'전체':16s} {n:5,}곳 중 사용중지 {stop.sum():5,} ({100 * stop.mean():.1f}%)")

    p("")
    p("=== 누가 만들었나 ===")
    for v, c in df["시설구분명"].value_counts().items():
        lab = v if v else "(빈칸)"
        p(f"  {c:6,} ({100 * c / n:4.1f}%)  {lab}")

    p("")
    p("=== 언제 지정했나 ===")
    for y, c in (yr // 10 * 10).value_counts().sort_index().items():
        if pd.notna(y):
            p(f"  {int(y)}년대  {c:5,}")

    p("")
    p("=== 「비상시설위치」 칸 ===")
    loc = df["비상시설위치"]
    lz = loc[loc != ""]
    p(f"채움 {100 * len(lz) / n:.1f}% · 고유 {lz.nunique():,}가지 · "
      f"평균 {lz.str.len().mean():.1f}자 · 최장 {lz.str.len().max()}자")
    p("※ 대부분 주소다. 자유 입력처럼 보이지만 광맥이 아니라 주소 칸이다.")
    p("※ 비상급수시설의 정확한 위치는 옮기지 않는다.")
    p(f"5자 이하로 적은 곳 {(lz.str.len() <= 5).sum():,}건")

    p("")
    p("=== 데이터에 남은 흠 ===")
    jamo = lz.str.fullmatch(r"[ㄱ-ㅎㅏ-ㅣ]+")
    p(f"비상시설위치에 자모만 적힌 것 {jamo.sum():,}건 (「ㅏㅏㅏ」)")
    p(f"시설구분명이 빈 줄 {(df['시설구분명'] == '').sum():,}건")
    p(f"지정 연도 1960년 이전 {(yr < 1960).sum():,}건 · 가장 이른 값 {int(yr.min())}년")
    p(f"이름이 「급수시설」 「비상급수시설」처럼 종류만 적힌 곳 "
      f"{name.isin(['급수시설', '비상급수시설', '민방위비상급수시설', '민간지정비상급수시설']).sum():,}곳")

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
