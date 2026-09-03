"""
청소년게임장.csv 에서 game.html(제10호)에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py youth_game_providers 청소년게임장

사용법:
    python scripts/analyze_game.py
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "청소년게임장.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_청소년게임장.txt"

# 취급품목 칸에 나오는 낱말. 앞쪽이 인형뽑기 계열, 뒤쪽이 옛 오락실 계열.
WORDS = ["토이", "크레인", "아케이드", "곰", "뽑기", "인형", "펀치", "농구"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py youth_game_providers 청소년게임장` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    alive = df["영업상태명"] == "영업/정상"

    p("=== 페이지 상단 지표 ===")
    p(f"누적 등록  {n:,}")
    p(f"사라짐     {(~alive).sum():,}  ({(~alive).sum()/n*100:.1f}%)")
    p(f"영업 중    {alive.sum():,}  ({alive.sum()/n*100:.1f}%)")

    items = df["제작취급품목내용"]
    items = items[items != ""]
    vc = items.value_counts()
    p("\n=== 제작취급품목내용 — 이 페이지의 광맥 ===")
    p(f"채운 곳 {len(items):,} ({len(items)/n*100:.1f}%) · 서로 다른 표현 {items.nunique():,}가지")
    p(f"그중 한 번만 쓰인 표현 {(vc == 1).sum():,}가지")
    p("상위 24:")
    for k, v in vc.head(24).items():
        p(f"  {v:>5}  {k[:60]}")

    p("\n=== 낱말 빈도 ===")
    for w in WORDS:
        p(f"  {w:<5} {items.str.contains(w).sum():>6,}")

    p("\n=== 가장 긴 취급품목 기재 ===")
    longest = sorted(set(items), key=len, reverse=True)[:3]
    for v in longest:
        p(f"  ({len(v)}자) {v}")

    p("\n=== 제공게임물명 ===")
    p(df["제공게임물명"].value_counts().to_string())

    p("\n=== 총게임기수 ===")
    g = df["총게임기수"]
    g = g[g != ""]
    gn = pd.to_numeric(g, errors="coerce").dropna()
    p(f"기재 {len(gn):,}곳")
    p(f"정확히 40대  {(gn == 40).sum():,}  ({(gn == 40).sum()/len(gn)*100:.1f}%)")
    p(f"41대 이상    {(gn > 40).sum():,} · 최대 {int(gn.max())}대")
    p(f"중앙값 {int(gn.median())}대")
    p("상위 10:")
    p(gn.astype(int).value_counts().head(10).to_string())
    p("※ 왜 40에 몰렸는지는 데이터에 적혀 있지 않다. 그대로 둔다.")

    p("\n=== 연도별 신규 등록 ===")
    opened = pd.to_datetime(df["인허가일자"], errors="coerce")
    closed = pd.to_datetime(df["폐업일자"], errors="coerce")
    yrs = opened.dt.year.value_counts().sort_index()
    p(yrs[yrs.index >= 2005].to_string())
    top = yrs[yrs.index >= 2005]
    p(f"최다 {top.idxmax()}년 {top.max():,}곳")

    p("\n=== 수명 ===")
    days = (closed - opened).dt.days
    ok = days.notna() & (days >= 0)
    years = days[ok] / 365.25
    p(f"대상 {ok.sum():,}곳 · 평균 {years.mean():.1f}년 · 중앙값 {years.median():.1f}년")
    p(f"1년 미만 {(years < 1).sum():,} ({(years < 1).sum()/len(years)*100:.1f}%)")

    p("\n=== 데이터의 흠 ===")
    name = df["사업장명"]
    p(f"가장 긴 사업장명 {max(len(v) for v in name)}자 · {max(name, key=len)}")
    blank = (df["제작취급품목내용"] == "").sum()
    p(f"취급품목 칸이 빈 곳 {blank:,} ({blank/n*100:.1f}%)")
    # 취급품목 칸에 업종명이나 등급을 그대로 옮겨 적은 경우
    for wrong in ["청소년게임제공업", "전체이용가"]:
        p(f"취급품목 칸에 '{wrong}'라고만 적은 곳 {(items == wrong).sum():,}")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
