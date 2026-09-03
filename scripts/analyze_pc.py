"""
PC방.csv (인터넷컴퓨터게임시설제공업)에서 pcbang.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py pc_bangs PC방

사용법:
    python scripts/analyze_pc.py
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "PC방.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_PC방.txt"

# 상호명에 가장 많이 쓰인 낱말. 앞쪽은 시대 어휘, 뒤쪽은 도박장 어휘.
WORDS = ["넷", "존", "인터넷", "대박", "스타", "사이버", "월드",
         "골드", "킹", "에이스", "세븐", "황금", "행운", "로얄", "럭키", "잭팟"]
GAMBLING = "대박|행운|황금|골드|로얄|세븐|킹|에이스|잭팟|럭키"

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py pc_bangs PC방` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()

    alive = df["영업상태명"] == "영업/정상"
    name = df["사업장명"]

    p("=== 페이지 상단 지표 ===")
    p(f"누적 등록  {len(df):,}")
    p(f"사라짐     {(~alive).sum():,}  ({(~alive).sum()/len(df)*100:.1f}%)")
    p(f"현재 영업  {alive.sum():,}  ({alive.sum()/len(df)*100:.1f}%)")

    # 등록일과 폐업일이 모두 있는 곳만 수명을 잰다.
    opened = pd.to_datetime(df["인허가일자"], errors="coerce")
    closed = pd.to_datetime(df["폐업일자"], errors="coerce")
    days = (closed - opened).dt.days
    ok = days.notna() & (days >= 0) & (opened.dt.year >= 1996)
    years = days[ok] / 365.25

    p("\n=== 얼마나 버티나 ===")
    p(f"대상 {ok.sum():,}곳 · 평균 {years.mean():.1f}년 · 중앙값 {years.median():.1f}년")
    p(f"최장 {years.max():.1f}년 · 하루 만에 접은 곳 {(days[ok] <= 1).sum():,}")
    bins = [0, 1, 2, 3, 5, 10, 100]
    labels = ["1년 미만", "1~2년", "2~3년", "3~5년", "5~10년", "10년 이상"]
    dist = pd.cut(years, bins=bins, labels=labels, right=False).value_counts().reindex(labels)
    for k, v in dist.items():
        p(f"  {k:<8} {v:>6,}  {v/len(years)*100:>5.1f}%")

    p("\n=== 최단 영업 8곳 ===")
    short = df[ok & (days > 1)].assign(일수=days).nsmallest(8, "일수")
    p(short[["사업장명", "인허가일자", "폐업일자", "일수"]].to_string(index=False))

    p("\n=== 최장 영업 (폐업한 곳) ===")
    long = df[ok].assign(일수=days).nlargest(3, "일수")
    p(long[["사업장명", "인허가일자", "폐업일자", "일수"]].to_string(index=False))

    p("\n=== 작명 사전 ===")
    for w in WORDS:
        p(f"  {w:<5} {name.str.contains(w, case=False).sum():>6,}")
    gam = name.str.contains(GAMBLING)
    p(f"  도박장 어휘 합계 {gam.sum():,}곳 ({gam.sum()/len(name)*100:.1f}%)")

    p("\n=== 최다 상호 ===")
    p(name.value_counts().head(12).to_string())

    p("\n=== 상호명 칸에 적힌 업무 메모 ===")
    memo = name.str.contains("무단폐업|현장조사|통보|안내|폐업")
    p(f"메모형 상호명 {memo.sum():,}곳")
    for v in sorted(set(name[memo]), key=len, reverse=True)[:6]:
        p(f"  ({len(v)}자) {v}")

    p("\n=== 연도별 신규 등록 · 폐업 ===")
    table = pd.DataFrame({"신규": opened.dt.year.value_counts(),
                          "폐업": closed.dt.year.value_counts()}).fillna(0).astype(int)
    p(table.loc[1996:2026].to_string())
    p("\n※ 2008년 신규 15,393건은 실제 개업이 아니라 제도 변경에 따른 일괄 재등록으로 보인다.")
    p("   페이지의 그래프가 2009년부터 시작하는 이유.")

    p("\n=== 1999년 등록 후 아직 영업 중 ===")
    live = df[alive & df["인허가일자"].str.match(r"(19|20)\d\d-")]
    p(live.sort_values("인허가일자")[["사업장명", "인허가일자", "도로명주소"]]
        .head(6).to_string(index=False))

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
