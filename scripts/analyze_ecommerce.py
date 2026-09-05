"""
통신판매업.csv 에서 제26호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py ecommerce_businesses 통신판매업

사용법:
    python scripts/analyze_ecommerce.py

※ 조심할 것

1. **3,096,399행 · 919MB 다. 세모지가 다룬 것 중 가장 크다.**
   전체 칸을 다 읽으면 메모리가 모자란다. usecols 로 필요한 칸만 읽는다.

2. **「카다로그가 늘었다」를 「카탈로그 판매가 늘었다」로 읽지 않는다.**
   고른 비율은 1999-2004년 1.35%에서 2015-2019년 3.91%로 올랐다가 떨어진다.
   체크박스를 여러 개 고르는 습관이 늘어난 것일 수도 있고 실제 판매일 수도 있다.
   **원본에 이유가 없다. 두 읽기를 나란히 둔다.**

3. **판매방식명은 여러 개를 고를 수 있다.** 수단별 숫자는 겹쳐서 센 값이라
   합계가 100%를 넘는다. 본문에 반드시 밝힌다.

4. **상호 2,173,792가지를 옮기지 않는다.** 옮기면 잡학이 아니라 명부다.
   전화번호 칸도 있다. 출력에 원문을 찍는 자리는 mask() 를 거친다.

5. **판매방식명은 4.4%가 비어 있다.** 비율의 분모는 채워진 2,960,322곳이다.
"""
import io
import sys
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "통신판매업.csv"
OUT = ROOT / "data" / "분석결과_통신판매업.txt"

COLS = ["판매방식명", "업태구분명", "사업장명", "인허가일자",
        "영업상태명", "상세영업상태명", "상세영업상태코드"]

CHANNELS = ["인터넷", "TV홈쇼핑", "카다로그", "신문잡지", "기타"]

YEAR_BANDS = [(1999, 2004), (2005, 2009), (2010, 2014), (2015, 2019), (2020, 2026)]

_MASK = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "(이메일)"),
    (re.compile(r"\d{2,3}-\d{2}-\d{5}"), "(사업자번호)"),
    (re.compile(r"\b0\d{1,2}-\d{3,4}-\d{4}\b"), "(전화번호)"),
]

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
                         f"`python scripts/fetch.py ecommerce_businesses 통신판매업` "
                         f"를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     low_memory=False, usecols=COLS)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    way = df["판매방식명"]
    got = way[way != ""]
    yr = pd.to_numeric(df["인허가일자"].str[:4], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳 (세모지가 다룬 것 중 가장 큰 데이터셋)")
    p(f"「판매방식명」 적힌 곳 {len(got):,} ({100 * len(got) / n:.1f}%) · "
      f"빈칸 {n - len(got):,} ({100 * (n - len(got)) / n:.1f}%)")
    p(f"고른 조합 {got.nunique()}가지")

    p("")
    p("=== 서식이 아직 묻는 판매 수단 ===")
    p("여러 개를 고를 수 있다. 아래 숫자는 겹쳐서 센 값이라 합계가 100%를 넘는다.")
    p("분모는 채워진 %s곳이다." % f"{len(got):,}")
    p("")
    for c in CHANNELS:
        m = got.str.contains(c, regex=False)
        p(f"  {c:8s} {m.sum():9,} ({100 * m.mean():5.2f}%)")
    p("")
    p("한 가지만 고른 곳")
    for c in CHANNELS:
        p(f"  「{c}」만 {(got == c).sum():,}")

    p("")
    p("=== 인터넷을 안 고른 곳 ===")
    noi = got[~got.str.contains("인터넷", regex=False)]
    p(f"{len(noi):,}건 ({100 * len(noi) / len(got):.2f}%) · 조합 {noi.nunique()}가지")
    for v, c in noi.value_counts().head(10).items():
        p(f"  {c:6,}  {v}")

    p("")
    p("=== 검증 — 낡은 선택지는 옛날에 더 많이 골랐나 ===")
    p("「카다로그」가 옛 수단이라면 오래된 신고일수록 많아야 한다. 그런데 반대다.")
    p("")
    p(f"{'인허가 연도':11s} {'건수':>9s} {'카다로그':>8s} {'신문잡지':>8s} {'TV홈쇼핑':>8s} {'인터넷':>8s}")
    for lo, hi in YEAR_BANDS:
        m = yr.between(lo, hi) & (way != "")
        sub = way[m]
        if len(sub) < 100:
            continue
        p(f"{lo}-{hi}  {len(sub):9,} "
          f"{100 * sub.str.contains('카다로그', regex=False).mean():7.2f}% "
          f"{100 * sub.str.contains('신문잡지', regex=False).mean():7.2f}% "
          f"{100 * sub.str.contains('TV홈쇼핑', regex=False).mean():7.2f}% "
          f"{100 * sub.str.contains('인터넷', regex=False).mean():7.2f}%")
    p("")
    p("→ 카다로그를 고른 비율이 1999-2004년 1.35%에서 2015-2019년 3.91%로 올랐다.")
    p("→ 읽기 두 가지: (가) 체크박스를 여러 개 고르는 습관이 늘었다,")
    p("   (나) 실제로 카탈로그를 같이 쓰는 곳이 늘었다. 원본에 답이 없다.")

    p("")
    p("=== 무엇을 파는가 — 업태구분명 ===")
    biz = df["업태구분명"]
    bz = biz[biz != ""]
    p(f"채움 {100 * len(bz) / n:.1f}% · 고유값 {bz.nunique():,}가지 · "
      f"최장 {bz.str.len().max()}자")
    p("※ 정해진 분류인데 고유값이 만 개가 넘는다. 여러 분류를 띄어쓰기로 붙여 적기 때문이다.")
    p("")
    for v, c in bz.value_counts().head(12).items():
        p(f"  {c:7,} ({100 * c / n:4.1f}%)  {v}")
    p("")
    p(f"「-」 라고만 적은 곳 {(biz == '-').sum():,} ({100 * (biz == '-').mean():.1f}%)")

    p("")
    p("=== 어떻게 끝났나 ===")
    for v, c in df["영업상태명"].value_counts().items():
        p(f"  {c:9,} ({100 * c / n:4.1f}%)  {v}")
    p("")
    p("상세 상태")
    for v, c in df["상세영업상태명"].value_counts().items():
        p(f"  {c:9,} ({100 * c / n:4.1f}%)  {v}")

    p("")
    p("=== 이름 ===")
    name = df["사업장명"]
    p(f"사업장명 고유 {name.nunique():,}가지 · 최장 {name.str.len().max()}자")
    p("가장 많이 쓰인 상호 — 상위 8")
    for v, c in name.value_counts().head(8).items():
        p(f"  {c:5,}  {mask(v)}")
    p("※ 흔한 상호만 옮긴다. 2,173,792가지를 옮기면 잡학이 아니라 명부다.")

    p("")
    p("=== 데이터에 남은 흠 ===")
    bb = (df["상세영업상태코드"] == "BBBB").sum()
    p(f"상세영업상태코드가 「BBBB」 인 것 {bb:,}건 "
      f"(제25호 담배소매업에서도 나온 값이다)")
    p(f"상세영업상태코드 종류 {df['상세영업상태코드'].nunique()}가지 — "
      f"{', '.join(sorted(df['상세영업상태코드'].unique()))}")
    p(f"인허가일자 2000년 이전 {(yr < 2000).sum():,}건 · "
      f"가장 이른 값 {int(yr.min())}년")

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
