"""
비디오감상실.csv 에서 videoroom.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py video_viewing_rooms 비디오감상실

사용법:
    python scripts/analyze_video.py
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "비디오감상실.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_비디오감상실.txt"

WORDS = ["비디오", "DVD", "방", "영화", "시네마", "무비", "스크린", "천국", "마을", "극장"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py video_viewing_rooms 비디오감상실` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()

    alive = df["영업상태명"] == "영업/정상"
    name = df["사업장명"]
    opened = pd.to_datetime(df["인허가일자"], errors="coerce")
    closed = pd.to_datetime(df["폐업일자"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"누적 등록  {len(df):,}")
    p(f"사라짐     {(~alive).sum():,}  ({(~alive).sum()/len(df)*100:.1f}%)")
    p(f"영업 중    {alive.sum():,}")
    p("영업 중인 곳의 시도 분포:")
    p(df.loc[alive, "도로명주소"].str.split().str[0].value_counts().to_string())

    p("\n=== 비디오재생기명 — 이 페이지의 제목 ===")
    player = df["비디오재생기명"][df["비디오재생기명"] != ""]
    p(f"기재한 곳 {len(player):,}")
    p(player.value_counts().to_string())
    top = player.value_counts()
    if len(top):
        p(f"'{top.index[0]}' 비율 {top.iloc[0]/len(player)*100:.1f}%")

    p("\n=== 소멸 곡선 (연도별 신규 등록) ===")
    years = opened.dt.year.value_counts().sort_index()
    p(years[years.index >= 1994].to_string())
    p(f"최다 연도 {years.idxmax()}년 {years.max():,}곳 · 마지막 등록 {opened.max().date()}")

    p("\n=== 수명 ===")
    days = (closed - opened).dt.days
    ok = days.notna() & (days >= 0) & (opened.dt.year >= 1995)
    yrs = days[ok] / 365.25
    p(f"대상 {ok.sum():,}곳 · 평균 {yrs.mean():.1f}년 · 중앙값 {yrs.median():.1f}년 · 최장 {yrs.max():.1f}년")
    p(f"1년 미만 {(yrs < 1).sum()} ({(yrs < 1).sum()/len(yrs)*100:.1f}%)")

    p("\n=== 상호에 박제된 매체 ===")
    for w in WORDS:
        p(f"  {w:<5} {name.str.contains(w, case=False).sum():>5}")
    p("\n최다 상호:")
    p(name.value_counts().head(10).to_string())

    p("\n=== 마지막으로 문을 연 곳 ===")
    p(df.assign(d=opened).nlargest(6, "d")[["사업장명", "인허가일자", "영업상태명", "도로명주소"]]
        .to_string(index=False))

    p("\n=== 1996년 개업 중 아직 영업 ===")
    n96 = (opened.dt.year == 1996)
    p(f"{(n96 & alive).sum()}곳 / 1996년 개업 {n96.sum()}곳")
    live = df[alive & df["인허가일자"].str.match(r"(19|20)\d\d-")]
    p(live.sort_values("인허가일자")[["사업장명", "인허가일자", "도로명주소"]].head(6).to_string(index=False))

    p("\n=== 가장 최근 폐업 ===")
    p(df.assign(d=closed).nlargest(3, "d")[["사업장명", "인허가일자", "폐업일자"]].to_string(index=False))

    p("\n=== 데이터의 흠 ===")
    odd = df[~df["인허가일자"].str.match(r"(199[4-9]|20[0-2]\d)-")]
    p(odd[["사업장명", "인허가일자", "영업상태명"]].to_string(index=False))

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
