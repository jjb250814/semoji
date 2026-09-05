"""
담배소매업.csv 에서 제25호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py tobacco_retailers 담배소매업

사용법:
    python scripts/analyze_tobacco.py

※ 조심할 것

1. **분류 이름을 믿기 전에 날짜와 대조한다.**
   「2009년11월법개정전자료」가 정말 2009년 이전 기록인지 인허가일자로 확인한다.
   확인해 보니 91.3%가 2009년 이전이고 중앙값이 2004년이라 이름이 정직하다.
   **이 검사를 안 하면 「이름이 이상하다」로만 끝나고 이야기가 서지 않는다.**

2. **빈칸도 같이 본다.** 민원종류명이 빈 158,339건은 인허가일자가
   **전부 2007년 이전**이다. 즉 빈칸도 「옛 기록」이라는 뜻이다.
   빈칸을 「누락」으로 읽으면 틀린다.

3. **상호 칸의 「무」 「없음」은 제18호(비산먼지 「개인」)와 같은 모양이다.**
   반복하지 않도록 곁가지로만 다루고, 제18호를 가리킨다.

4. **전화번호 칸이 있다.** 출력에 원문을 찍는 자리는 mask() 를 거친다.
   상호는 「무」 「없음」처럼 사람을 특정하지 않는 값만 옮긴다.

5. **657,136행이다.** 읽는 데 시간이 걸린다.
"""
import io
import sys
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "담배소매업.csv"
OUT = ROOT / "data" / "분석결과_담배소매업.txt"

_MASK = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "(이메일)"),
    (re.compile(r"\d{2,3}-\d{2}-\d{5}"), "(사업자번호)"),
    (re.compile(r"\b0\d{1,2}-\d{3,4}-\d{4}\b"), "(전화번호)"),
]

# 「이름이 없다」는 뜻으로 적힌 상호. 제18호 「개인」과 같은 모양이다.
NONAME = ["무", "없음", "-", ".", "상호없음", "무상호", "없슴", "미상", "무명"]

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
                         f"`python scripts/fetch.py tobacco_retailers 담배소매업` "
                         f"를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False, low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    kind = df["민원종류명"]
    yr = pd.to_numeric(df["인허가일자"].str[:4], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳")
    p(f"「민원종류명」 적힌 곳 {(kind != '').sum():,} ({100 * (kind != '').mean():.1f}%) · "
      f"빈칸 {(kind == '').sum():,} ({100 * (kind == '').mean():.1f}%)")
    p(f"답의 종류 {kind[kind != ''].nunique()}가지")

    p("")
    p("=== 답이 셋뿐인데 하나가 「법이 바뀌기 전 자료」다 ===")
    for v, c in kind.value_counts().items():
        lab = v if v else "(빈칸)"
        p(f"  {c:7,} ({100 * c / n:4.1f}%)  {lab}")

    p("")
    p("=== 검증 — 그 이름이 정말 그 시기를 가리키나 ===")
    p("분류 이름을 믿기 전에 인허가일자와 대조한다. (제20호에서 배운 것)")
    p("")
    p(f"{'민원종류명':24s} {'건수':>9s} {'중앙값':>7s} {'2009년 이전':>11s} {'최대':>6s}")
    for v in ["2009년11월법개정전자료", "제7조의3제2항에따른경우",
              "제7조의3제3항에따른경우", ""]:
        m = kind == v
        y = yr[m].dropna()
        if not len(y):
            continue
        lab = v if v else "(빈칸)"
        p(f"{lab:24s} {m.sum():9,} {int(y.median()):7d} "
          f"{100 * (y < 2009).mean():10.1f}% {int(y.max()):6d}")
    p("")
    m = kind == "2009년11월법개정전자료"
    late = (m & (yr >= 2010)).sum()
    p(f"이 분류인데 2010년 이후 인허가인 것 {late:,}건 ({100 * late / m.sum():.2f}%)")
    p("→ 이름이 정직하다. 91.3%가 2009년 이전이고 중앙값이 2004년이다.")
    p("")
    blank = kind == ""
    p(f"빈칸 {blank.sum():,}건은 인허가일자가 전부 "
      f"{int(yr[blank].max())}년 이전이다 (2009년 이전 {100 * (yr[blank] < 2009).mean():.1f}%).")
    p("→ 빈칸도 「누락」이 아니라 「옛 기록」이다.")
    old = blank.sum() + m.sum()
    p("")
    p(f"옛 기록으로 표시된 것 = 빈칸 {blank.sum():,} + 법개정전자료 {m.sum():,} "
      f"= {old:,} ({100 * old / n:.1f}%)")

    p("")
    p("=== 지금 쓰는 분류는 법조문 번호다 ===")
    for v in ["제7조의3제2항에따른경우", "제7조의3제3항에따른경우"]:
        c = (kind == v).sum()
        p(f"  {c:7,} ({100 * c / n:4.1f}%)  {v}")
    now = sum((kind == v).sum() for v in ["제7조의3제2항에따른경우", "제7조의3제3항에따른경우"])
    p(f"  {now:7,} ({100 * now / n:4.1f}%)  합계 — 지금 쓰는 분류")
    p("※ 띄어쓰기가 없다. 조문 번호가 그대로 분류 이름이 되어 있다.")

    p("")
    p("=== 가게 이름이 「없음」인 곳 ===")
    p("제18호(비산먼지 「개인」)와 같은 모양이라 곁가지로만 센다.")
    name = df["사업장명"]
    p(f"사업장명 고유 {name.nunique():,}가지 · 한 번만 쓰인 이름 "
      f"{(name.value_counts() == 1).sum():,} · 최장 {name.str.len().max()}자")
    p("")
    tot = 0
    for v in NONAME:
        c = (name == v).sum()
        if c:
            tot += c
            p(f"  {c:6,}  「{v}」")
    p(f"  {tot:6,}  합계 ({100 * tot / n:.2f}%)")
    p("")
    p("자주 쓰인 상호 — 상위 10")
    for v, c in name.value_counts().head(10).items():
        p(f"  {c:6,}  {mask(v)}")

    p("")
    p("=== 어떻게 끝났나 ===")
    for v, c in df["영업상태명"].value_counts().items():
        p(f"  {c:7,} ({100 * c / n:4.1f}%)  {v}")
    p("")
    p("상세 상태")
    for v, c in df["상세영업상태명"].value_counts().items():
        lab = v if v else "(빈칸)"
        p(f"  {c:7,} ({100 * c / n:4.1f}%)  {lab}")

    p("")
    p("=== 데이터에 남은 흠 ===")
    bb = df["상세영업상태코드"] == "BBBB"
    p(f"상세영업상태코드가 「BBBB」 인 것 {bb.sum():,}건")
    p(f"  그 {bb.sum():,}건은 상세영업상태명이 전부 비어 있다.")
    p(f"  인허가 연도 {int(yr[bb].min())}~{int(yr[bb].max())}년")
    p("  ※ 다른 코드는 0~6 한 자리 숫자다. 「BBBB」만 글자다.")
    p("")
    zy = pd.to_numeric(df["지정일자"].str[:4], errors="coerce")
    p(f"지정일자 채움 {100 * (df['지정일자'] != '').mean():.1f}% · "
      f"1990년 이전 {(zy < 1990).sum():,}건")
    p(f"인허가일자 1900년인 것 {(yr == 1900).sum():,}건")

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
