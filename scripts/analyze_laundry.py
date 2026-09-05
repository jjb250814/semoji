"""
세탁소.csv 에서 제27호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py laundries 세탁소

사용법:
    python scripts/analyze_laundry.py

※ 조심할 것

1. **업종이 「생겼다」고 말하려면 첫 해를 확인한다.**
   운동화전문세탁업은 1990년대에 0곳이고 첫 허가가 2002년이다.
   이 확인 없이 「요즘 늘었다」고만 쓰면 분류가 나중에 붙었을 뿐인
   경우와 구분되지 않는다.

2. **「세탁기 1,326대」를 사실로 쓰지 않는다.** 그 가게의 소재지면적은
   29.25제곱미터다. 흠으로 다루고, 상호는 옮기지 않는다.

3. **상호의 시대 구분(세탁소·크리닝·런드리)은 제12호 「바버샵」과 같은 모양이다.**
   반복하지 않도록 곁가지로만 두고 제12호를 가리킨다.

4. **전화번호 칸이 있다.** 출력에 원문을 찍는 자리는 mask() 를 거친다.
   상호는 흔한 것만, 개별 가게를 특정하지 않는 선에서 옮긴다.
"""
import io
import sys
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "세탁소.csv"
OUT = ROOT / "data" / "분석결과_세탁소.txt"

_MASK = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "(이메일)"),
    (re.compile(r"\d{2,3}-\d{2}-\d{5}"), "(사업자번호)"),
    (re.compile(r"\b0\d{1,2}-\d{3,4}-\d{4}\b"), "(전화번호)"),
]

KINDS = ["일반세탁업", "운동화전문세탁업", "빨래방업", "세탁업 기타", "기타"]
YEAR_BANDS = [(1990, 1999), (2000, 2009), (2010, 2014), (2015, 2019), (2020, 2026)]

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
                         f"`python scripts/fetch.py laundries 세탁소` 를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False, low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    kind = df["업태구분명"]
    yr = pd.to_numeric(df["인허가일자"].str[:4], errors="coerce")
    wash = pd.to_numeric(df["세탁기수"], errors="coerce")
    dry = pd.to_numeric(df["회수건조기수"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳")
    for v, c in kind.value_counts().items():
        p(f"  {c:6,} ({100 * c / n:4.1f}%)  {v}")
    p(f"영업 중 {(df['영업상태명'] == '영업/정상').sum():,} · "
      f"폐업 {(df['영업상태명'] == '폐업').sum():,} "
      f"({100 * (df['영업상태명'] == '폐업').mean():.1f}%)")

    p("")
    p("=== 업종이 태어난 해 ===")
    p("「요즘 늘었다」고 말하기 전에 첫 허가 연도를 본다.")
    p("")
    p(f"{'업종':14s} {'곳':>7s} {'첫 허가':>7s} {'중앙값':>7s}")
    for k in KINDS:
        s = yr[kind == k].dropna()
        if not len(s):
            continue
        p(f"{k:14s} {len(s):7,} {int(s.min()):7d} {int(s.median()):7d}")
    p("")
    p("→ 운동화전문세탁업의 첫 허가는 2002년이다. 1990년대에는 한 곳도 없다.")

    p("")
    p("=== 운동화전문세탁업 — 연도별 새 허가 ===")
    s = yr[kind == "운동화전문세탁업"].dropna().astype(int)
    for y, c in s.value_counts().sort_index().items():
        p(f"  {y}  {c:4,}")

    p("")
    p("=== 새 허가 중 차지하는 비율 ===")
    p(f"{'인허가 연도':11s} {'새 허가':>8s} {'운동화전문':>9s} {'빨래방':>8s} {'일반세탁':>8s}")
    for lo, hi in YEAR_BANDS:
        m = yr.between(lo, hi)
        if m.sum() < 50:
            continue
        p(f"{lo}-{hi}  {m.sum():8,} "
          f"{100 * (kind[m] == '운동화전문세탁업').mean():8.2f}% "
          f"{100 * (kind[m] == '빨래방업').mean():7.2f}% "
          f"{100 * (kind[m] == '일반세탁업').mean():7.2f}%")
    p("")
    p("→ 2010-2014년에는 새 허가의 11.17%가 운동화 전문이었다.")

    p("")
    p("=== 기계 몇 대로 하나 ===")
    p(f"세탁기수 채움 {100 * (df['세탁기수'] != '').mean():.1f}% · "
      f"회수건조기수 채움 {100 * (df['회수건조기수'] != '').mean():.1f}%")
    p("")
    p(f"{'업종':14s} {'채움':>6s} {'중앙값':>7s} {'최대':>7s}")
    for k in KINDS[:4]:
        m = kind == k
        w = wash[m].dropna()
        if not len(w):
            continue
        p(f"{k:14s} {100 * len(w) / m.sum():5.1f}% {w.median():7.1f} {w.max():7.0f}")
    p("")
    p(f"세탁기 0대라고 적은 곳 {(wash == 0).sum():,} · 1대 {(wash == 1).sum():,}")
    p(f"세탁기 10대 넘는 곳 {(wash > 10).sum():,} · 100대 넘는 곳 {(wash > 100).sum():,}")
    p(f"회수건조기 0대 {(dry == 0).sum():,} · 최대 {dry.max():.0f}대")

    p("")
    p("=== 이름 (제12호 「바버샵」과 같은 모양이라 곁가지) ===")
    name = df["사업장명"]
    p(f"상호 고유 {name.nunique():,}가지")
    for lab, pat in [("「세탁소」로 끝", r"세탁소$"), ("「사」로 끝", r"사$"),
                     ("「크리닝·클리닝」", r"크리닝|클리닝"),
                     ("「빨래방」", r"빨래방"), ("「런드리·laundry」", r"런드리|laundry")]:
        c = name.str.contains(pat, case=False, regex=True).sum()
        p(f"  {lab:16s} {c:6,} ({100 * c / n:4.1f}%)")
    p("")
    p("자주 쓰인 상호 — 상위 8")
    for v, c in name.value_counts().head(8).items():
        p(f"  {c:5,}  {mask(v)}")

    p("")
    p("=== 데이터에 남은 흠 ===")
    i = wash.idxmax()
    r = df.loc[i]
    p(f"세탁기수 최대 {wash.max():.0f}대 — 업종 {r['업태구분명']} · "
      f"인허가 {r['인허가일자']} · {r['영업상태명']}")
    p(f"  그 가게의 소재지면적은 {r['소재지면적']}제곱미터다.")
    p("  ※ 상호는 옮기지 않는다. 흠이지 자랑이 아니다.")
    p("")
    bf = df["건물지하층수"]
    p(f"건물지하층수에 「104」라고 적힌 곳 {(bf == '104').sum():,}건 · "
      f"「13」 {(bf == '13').sum():,}건")
    p(f"인허가일자 1900년 {(yr == 1900).sum():,}건")
    p("")
    p("사라진 칸 — 지하 몇 층부터 몇 층까지 쓰는지 묻는다")
    for c in ["사용시작지하층", "사용끝지하층", "사용시작지상층", "사용끝지상층"]:
        s2 = df[c]
        nz = s2[s2 != ""]
        p(f"  {c:10s} 채움 {100 * len(nz) / n:5.1f}% · "
          f"「0」 {(nz == '0').sum():,} ({100 * (nz == '0').mean():.1f}%)")
    p("")
    p(f"조건부허가신고사유 채움 {100 * (df['조건부허가신고사유'] != '').mean():.1f}% "
      f"({(df['조건부허가신고사유'] != '').sum():,}건) · "
      f"{df['조건부허가신고사유'][df['조건부허가신고사유'] != ''].nunique()}가지")
    p("  ※ 담당자 메모라 원문은 옮기지 않는다.")

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
