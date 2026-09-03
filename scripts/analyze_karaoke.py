"""
노래방.csv 에서 karaoke.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py karaoke_rooms 노래방

사용법:
    python scripts/analyze_karaoke.py
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "노래방.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_노래방.txt"

# 서류가 「있는가 없는가」를 물어본 칸들. 답은 Y 아니면 N 둘뿐이다.
YN = ["방음시설여부", "비상계단여부", "비상구여부",
      "자동환기여부", "특수조명여부", "청소년실여부"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py karaoke_rooms 노래방` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    name = df["사업장명"]
    alive = df["영업상태명"] == "영업/정상"

    p("=== 페이지 상단 지표 ===")
    p(f"등록된 노래방   {n:,}곳")
    p(f"영업 중        {alive.sum():,} · 폐업 {(df['영업상태명']=='폐업').sum():,}")

    # --- 이 페이지의 제목 ---
    p("\n=== 우리가 부르는 이름과 서류에 적힌 이름 ===")
    for w in ["노래연습장", "노래방", "코인", "가라오케", "노래빠"]:
        p(f"  상호에 '{w}' {name.str.contains(w, regex=False).sum():,}곳")
    p("'노래연습장'이 '노래방'의 %.1f배" % (
        name.str.contains("노래연습장", regex=False).sum()
        / max(name.str.contains("노래방", regex=False).sum(), 1)))

    # --- 서류가 물어본 여부 칸 ---
    p("\n=== 서류가 「있는가 없는가」를 물어본 칸 ===")
    p(f"{'칸':<12}{'적은 곳':>9}{'채움':>8}{'Y':>8}{'N':>8}{'N비율':>8}")
    for c in YN:
        v = df[c]
        fill = (v != "").sum()
        y, no = (v == "Y").sum(), (v == "N").sum()
        p(f"{c:<12}{fill:>9,}{fill/n*100:>7.1f}%{y:>8,}{no:>8,}{no/max(fill,1)*100:>7.1f}%")

    p("\n영업 중인 곳만:")
    for c in YN:
        v = df.loc[alive, c]
        fill = (v != "").sum()
        y, no = (v == "Y").sum(), (v == "N").sum()
        p(f"{c:<12}{fill:>9,}{y:>8,}{no:>8,}   Y비율 {y/max(fill,1)*100:>5.1f}%")

    # --- 청소년실 ---
    p("\n=== 청소년실 ===")
    ys = pd.to_numeric(df["청소년실수"], errors="coerce")
    p(f"「청소년실여부」에 Y {(df['청소년실여부']=='Y').sum():,} · "
      f"N {(df['청소년실여부']=='N').sum():,} · 빈칸 {(df['청소년실여부']=='').sum():,}")
    p(f"청소년실 합계 {ys.sum():,.0f}개 · 적은 곳 {(df['청소년실수']!='').sum():,} · "
      f"최대 {ys.max():.0f}")
    p("방 개수 분포:")
    p(ys.value_counts().sort_index().head(12).to_string())
    p(f"「있음」이라 적었는데 개수가 0이거나 빈칸 "
      f"{((df['청소년실여부']=='Y') & ((ys.isna()) | (ys==0))).sum():,}곳")

    # --- 조도 ---
    p("\n=== 「조명시설조도」 — 노래방 조명의 밝기를 적는 칸 ===")
    lux = df["조명시설조도"]
    lx = pd.to_numeric(lux, errors="coerce")
    p(f"적은 곳 {(lux!='').sum():,} ({(lux!='').sum()/n*100:.1f}%) · "
      f"고유값 {lux[lux!=''].nunique():,}")
    p(f"중앙값 {lx.median():.0f} · 최소 {lx.min():.0f} · 최대 {lx.max():,.0f}")
    p(lux[lux != ""].value_counts().head(12).to_string())

    # --- 방 --
    p("\n=== 노래방실수 ===")
    rm = pd.to_numeric(df["노래방실수"], errors="coerce")
    p(f"적은 곳 {(df['노래방실수']!='').sum():,} · 합계 {rm.sum():,.0f}개 · "
      f"중앙값 {rm.median():.0f} · 최대 {rm.max():.0f}")
    p(rm.value_counts().sort_index().head(16).to_string())

    # --- 이름 ---
    p("\n=== 이름 ===")
    vc = name.value_counts()
    p(f"고유 {name.nunique():,} · 1회성 {(vc==1).sum():,}")
    p(vc.head(15).to_string())
    p(f"\n가장 긴 이름 {name.str.len().max()}자")
    for s in name[name.str.len() == name.str.len().max()].unique()[:2]:
        p(f"   {s}")

    # --- 생존 ---
    p("\n=== 생존 ===")
    p(df["영업상태명"].value_counts().to_string())
    op = pd.to_datetime(df["인허가일자"], errors="coerce")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")
    life = (cl - op).dt.days
    life = life[life >= 0]
    p(f"수명 중앙값 {life.median()/365:.1f}년 · 최단 {life.min():.0f}일 · "
      f"최장 {life.max()/365:.1f}년")
    years = op.dt.year.value_counts().sort_index()
    p("\n연도별 신규 (1992~):")
    p(years[(years.index >= 1992) & (years.index <= 2026)].to_string())
    p(f"최다 연도 {years.idxmax():.0f}년 {years.max():,}곳")
    p(f"1992년 이전으로 적힌 곳 {years[years.index < 1992].sum():,} "
      f"(가장 이른 값 {years.index.min():.0f})")

    p("\n=== 주변환경명 ===")
    env = df["주변환경명"]
    p(f"적은 곳 {(env!='').sum():,} ({(env!='').sum()/n*100:.1f}%)")
    p(env[env != ""].value_counts().to_string())

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
