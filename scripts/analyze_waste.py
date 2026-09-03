"""
생활폐기물.csv 에서 waste/index.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py household_waste_info 생활폐기물

사용법:
    python scripts/analyze_waste.py
"""
import io
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "생활폐기물.csv"
OUT = ROOT / "data" / "분석결과_생활폐기물.txt"

WAYS = ["생활쓰레기배출방법", "음식물쓰레기배출방법", "재활용품배출방법",
        "일시적다량폐기물배출방법"]
DAYS = ["생활쓰레기배출요일", "음식물쓰레기배출요일", "재활용품배출요일"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py household_waste_info 생활폐기물` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    place = df["배출장소"]

    p("=== 페이지 상단 지표 ===")
    p(f"관리구역        {n:,}곳")
    p(f"시군구          {df['시군구명'].nunique()}개 · 시도 {df['시도명'].nunique()}개")
    p(f"배출장소 표기    {place.nunique():,}가지 "
      f"(1회만 등장 {(place.value_counts()==1).sum():,})")

    # --- 이 페이지의 제목 ---
    p("\n=== 「배출장소」 — 어디에 내놓으라고 적었나 ===")
    vc = place.value_counts()
    p(f"고유 {place.nunique():,} · 1회성 {(vc==1).sum():,} · "
      f"가장 긴 것 {place.str.len().max()}자")
    p("가장 흔한 12가지:")
    for k, c in vc.head(12).items():
        p(f"  {c:>5,}  {k}")
    p("\n「내 집 앞」을 뜻하는 표기들 (한 번씩만 쓰인 것):")
    mine = place[place.str.contains("내집|내 집|자기집|자기 집|집앞|집 앞|점포|가게", regex=True)]
    for s in mine[mine.map(vc) == 1].head(12):
        p(f"   {s}")
    p(f"\n'집' 또는 '점포'가 든 표기 {place.str.contains('집|점포|가게', regex=True).sum():,}건 · "
      f"{place[place.str.contains('집|점포|가게', regex=True)].nunique():,}가지")

    # --- 같은 말을 몇 가지로 ---
    p("\n=== 버리는 방법을 적는 네 칸 ===")
    for c in WAYS:
        v = df[c][df[c] != ""]
        p(f"\n{c}: {v.nunique()}가지 · 1회성 {(v.value_counts()==1).sum()}")
        for k, cnt in v.value_counts().head(6).items():
            p(f"  {cnt:>5,}  {k[:64]}")

    p("\n=== '종량제'를 적는 방법 ===")
    v = df["생활쓰레기배출방법"]
    jong = v[v.str.contains("종량제|규격봉투", regex=True)]
    p(f"'종량제' 또는 '규격봉투'가 든 표기 {len(jong):,}건 "
      f"({len(jong)/n*100:.1f}%) · {jong.nunique()}가지")
    for k, c in jong.value_counts().head(10).items():
        p(f"  {c:>5,}  {k[:60]}")

    # --- 요일과 시각 ---
    p("\n=== 배출 요일 ===")
    for c in DAYS:
        v = df[c][df[c] != ""]
        p(f"{c}: {v.nunique()}가지 · " +
          ", ".join(f"{k}({cnt:,})" for k, cnt in v.value_counts().head(5).items()))

    p("\n=== 배출 시각 ===")
    for c in [x for x in df.columns if "시각" in x]:
        v = df[c][df[c] != ""]
        p(f"{c}: {v.nunique()}가지 · " +
          ", ".join(f"{k}({cnt:,})" for k, cnt in v.value_counts().head(4).items()))

    # --- 미수거일 ---
    p("\n=== 미수거일 ===")
    m = df["미수거일"]
    mvc = m.value_counts()
    p(f"고유 {m.nunique():,} · 1회성 {(mvc==1).sum():,}")
    for k, c in mvc.head(12).items():
        p(f"  {c:>5,}  {k[:56]}")
    p(f"\n'명절'이 든 표기 {m.str.contains('명절', regex=False).sum():,}건 · "
      f"{m[m.str.contains('명절', regex=False)].nunique()}가지")
    p(f"'없음'이라 적은 곳 {(m=='없음').sum():,}")
    p("가장 긴 미수거일:")
    p("   " + m.loc[m.str.len().idxmax()][:150])

    # --- 그 밖 ---
    p("\n=== 배출장소유형 ===")
    p(df["배출장소유형"].value_counts().to_string())

    p("\n=== 관리구역 ===")
    p(f"관리구역명 {df['관리구역명'].nunique():,}가지 · "
      f"대상지역명 {df['관리구역대상지역명'].nunique():,}가지")
    p(df["관리구역명"].value_counts().head(8).to_string())
    p(f"관리구역명을 '없음'이라 적은 곳 {(df['관리구역명']=='없음').sum():,}")

    p("\n=== 오타 ===")
    typo = df["일시적다량폐기물배출방법"].str.contains("일시작", regex=False)
    p(f"「일시작다량폐기물」이라 적힌 줄 {typo.sum():,}건")
    if typo.any():
        p("   " + df.loc[typo, "일시적다량폐기물배출방법"].iloc[0][:70])
        p("   시군구: " + ", ".join(df.loc[typo, "시군구명"].unique()[:5]))

    p("\n=== 시도 ===")
    p(df["시도명"].value_counts().head(8).to_string())

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print("-> " + str(OUT))


if __name__ == "__main__":
    main()
