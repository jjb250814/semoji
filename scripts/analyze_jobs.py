"""
직업소개소.csv 에서 제28호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py paid_job_centers 직업소개소

사용법:
    python scripts/analyze_jobs.py

※ 조심할 것

1. **동물 이름을 세기 전에 프랜차이즈인지 확인한다.**
   「개미」가 든 상호 452곳이 한 회사의 지점이라면 이야기가 통째로 틀린다.
   19개 시도에 흩어져 있고 상호가 247가지이며 법인은 13곳뿐이라
   **프랜차이즈가 아니라 작명 습관**이다. 이 검사를 본문에도 싣는다.

2. **낱말을 부분일치로 세면 오탐이 난다.**
   「소」로 세면 「직업소개소」가 다 걸려 21,406곳이 된다.
   **글자가 겹치지 않는 동물 이름만** 센다 (개미·황소·코끼리·기린·까치…).
   「용」은 「고용」 「용역」에, 「매」는 다른 낱말에 걸리므로 뺀다.

3. **전화번호 칸이 있다.** 출력에 원문을 찍는 자리는 mask() 를 거친다.
   상호는 여러 곳이 함께 쓰는 흔한 이름만 옮긴다.

4. **「구분명」의 답이 하나뿐인 것을 크게 쓰지 않는다.**
   이 파일이 유료직업소개소만 담고 있어서 그렇다. 무료직업소개소는
   다른 데이터셋이다. 칸이 쓸모없다는 뜻이 아니다.
"""
import io
import sys
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "직업소개소.csv"
OUT = ROOT / "data" / "분석결과_직업소개소.txt"

_MASK = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "(이메일)"),
    (re.compile(r"\d{2,3}-\d{2}-\d{5}"), "(사업자번호)"),
    (re.compile(r"\b0\d{1,2}-\d{3,4}-\d{4}\b"), "(전화번호)"),
]

# 다른 낱말에 겹치지 않는 동물 이름만 센다.
# 「소」(직업소개소) 「용」(고용·용역) 「말」(말소) 「매」는 오탐이라 뺀다.
ANIMALS = ["개미", "황소", "코끼리", "기린", "까치", "꿀벌", "두꺼비",
           "백조", "백마", "천마", "청마", "다람쥐", "부엉이", "독수리",
           "호랑이", "제비", "비둘기"]

WORDS = ["인력", "직업소개소", "파출부", "컨설팅", "잡", "인력개발", "사무소"]

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
                         f"`python scripts/fetch.py paid_job_centers 직업소개소` "
                         f"를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False, low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    name = df["사업장명"]
    df["addr"] = df["도로명주소"].where(df["도로명주소"] != "", df["지번주소"])
    df["sido"] = df["addr"].str.split().str[0]
    yr = pd.to_numeric(df["인허가일자"].str[:4], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳 (유료직업소개소)")
    p(f"상호 고유 {name.nunique():,}가지 · 한 번만 쓰인 이름 "
      f"{(name.value_counts() == 1).sum():,} · 최장 {name.str.len().max()}자")
    p(f"영업 중 {(df['영업상태명'] == '영업/정상').sum():,} · "
      f"폐업 {(df['영업상태명'] == '폐업').sum():,} "
      f"({100 * (df['영업상태명'] == '폐업').mean():.1f}%)")

    p("")
    p("=== 상호에 든 동물 ===")
    p("겹치는 낱말은 세지 않는다. 「소」로 세면 「직업소개소」가 다 걸려 오탐이 된다.")
    p(f"  (오탐 예: 「소」로 세면 {name.str.contains('소', regex=False).sum():,}곳, "
      f"「용」은 {name.str.contains('용', regex=False).sum():,}곳이 걸린다)")
    p("")
    for a in ANIMALS:
        c = name.str.contains(a, regex=False).sum()
        if c:
            p(f"  {a:5s} {c:5,} ({100 * c / n:5.2f}%)")

    p("")
    p("=== 검증 — 개미가 프랜차이즈인가 ===")
    p("한 회사의 지점이라면 「작명 습관」이라는 이야기가 통째로 틀린다.")
    p("")
    for a in ["개미", "황소"]:
        m = name.str.contains(a, regex=False)
        y = yr[m].dropna()
        p(f"「{a}」 {m.sum():,}곳")
        p(f"  시도 {df.loc[m, 'sido'].nunique()}곳에 분포 (전체 시도 {df['sido'].nunique()}곳)")
        p(f"  상호 종류 {name[m].nunique()}가지")
        p(f"  법인은 {(df.loc[m, '법인구분명'] == '법인').sum()}곳뿐 "
          f"(나머지는 개인)")
        p(f"  인허가 {int(y.min())}~{int(y.max())}년 · 중앙값 {int(y.median())}년")
        p("  가장 많은 시도: " +
          " · ".join(f"{k} {v}" for k, v in
                     df.loc[m, "sido"].value_counts().head(4).items()))
        p("")
    p("→ 흩어져 있고 이름도 제각각이다. 프랜차이즈가 아니라 작명 습관이다.")

    p("")
    p("=== 「개미」가 든 상호 — 상위 8 ===")
    for v, c in name[name.str.contains("개미", regex=False)].value_counts().head(8).items():
        p(f"  {c:4,}  {mask(v)}")
    p("")
    p("=== 「황소」가 든 상호 — 상위 6 ===")
    for v, c in name[name.str.contains("황소", regex=False)].value_counts().head(6).items():
        p(f"  {c:4,}  {mask(v)}")

    p("")
    p("=== 상호에 쓰인 말 ===")
    for w in WORDS:
        c = name.str.contains(w, regex=False).sum()
        p(f"  {w:10s} {c:6,} ({100 * c / n:5.2f}%)")
    p("")
    p("※ 「파출부」는 지금은 잘 쓰지 않는 말인데 상호에 남아 있다.")

    p("")
    p("=== 자주 쓰인 상호 — 상위 10 ===")
    for v, c in name.value_counts().head(10).items():
        p(f"  {c:4,}  {mask(v)}")

    p("")
    p("=== 개인이 열에 아홉 ===")
    for v, c in df["법인구분명"].value_counts().items():
        lab = v if v else "(빈칸)"
        p(f"  {c:6,} ({100 * c / n:4.1f}%)  {lab}")

    p("")
    p("=== 답이 하나뿐인 칸 ===")
    for v, c in df["구분명"].value_counts().items():
        lab = v if v else "(빈칸)"
        p(f"  {c:6,}  {lab}")
    p("※ 이 파일이 유료직업소개소만 담고 있어서 그렇다. 무료직업소개소는 다른 데이터셋이다.")

    p("")
    p("=== 어떻게 끝났나 ===")
    for v, c in df["상세영업상태명"].value_counts().items():
        p(f"  {c:6,} ({100 * c / n:4.1f}%)  {v}")

    p("")
    p("=== 언제 생겼나 ===")
    for y, c in (yr // 10 * 10).value_counts().sort_index().items():
        if pd.notna(y):
            p(f"  {int(y)}년대  {c:6,}")

    p("")
    p("=== 데이터에 남은 흠 ===")
    bb = (df["상세영업상태코드"] == "BBBB").sum()
    p(f"상세영업상태코드가 「BBBB」 인 것 {bb:,}건")
    p("  ※ 제25호 담배소매업 400건, 제26호 통신판매업 115건에 이어 세 번째다.")
    p(f"인허가일자 1900년 {(yr == 1900).sum():,}건")
    p(f"구분명·법인구분명이 빈 줄 {(df['구분명'] == '').sum():,}건 (같은 줄이다)")

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
