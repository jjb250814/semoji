"""
자전거보관소.csv 에서 bike.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py bicycle_parking_info 자전거보관소

사용법:
    python scripts/analyze_bike.py
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "자전거보관소.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_자전거.txt"

# 서식이 「있는가 없는가」를 묻는 세 가지.
YN = ["차양막설치여부", "공기주입기비치여부", "수리대설치여부"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py bicycle_parking_info 자전거보관소` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    name = df["자전거보관소명"]
    org = df["관리기관명"]
    cap = pd.to_numeric(df["보관대수"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"등록된 보관소   {n:,}곳")
    p(f"보관대수 합계   {cap.sum():,.0f}대 (중앙값 {cap.median():.0f})")

    # --- 이 페이지의 제목 ---
    p("\n=== 서식이 묻는 세 가지 ===")
    p(f"{'칸':<14}{'적은 곳':>9}{'채움':>8}{'Y':>8}{'Y비율':>9}{'N':>9}")
    for c in YN:
        v = df[c]
        fill = (v != "").sum()
        y = (v == "Y").sum()
        p(f"{c:<14}{fill:>9,}{fill/n*100:>7.1f}%{y:>8,}{y/max(fill,1)*100:>8.2f}%"
          f"{(v=='N').sum():>9,}")

    p("\n=== 수리대가 있다고 답한 곳 ===")
    sel = df[df["수리대설치여부"] == "Y"]
    p(f"전국 {len(sel):,}곳")
    p("\n관리기관별:")
    p(sel["관리기관명"].value_counts().to_string())
    top = sel["관리기관명"].value_counts()
    p(f"\n상위 두 기관이 {top.iloc[:2].sum():,}곳 / {len(sel):,}곳 "
      f"({top.iloc[:2].sum()/len(sel)*100:.1f}%)")
    p("\n목록:")
    for _, r in sel.iterrows():
        p(f"   {r['자전거보관소명'][:34]:<36}{r['관리기관명'][:20]:<22}{r['보관대수']:>5}대")

    # --- 공기주입기 ---
    p("\n=== 공기주입기 ===")
    p(df["공기주입기유형명"].value_counts().to_string())
    yes = (df["공기주입기비치여부"] == "Y").sum()
    blank = ((df["공기주입기비치여부"] == "Y") & (df["공기주입기유형명"] == "")).sum()
    p(f"\n비치했다고 답한 {yes:,}곳 중 유형을 비워 둔 곳 {blank:,} ({blank/yes*100:.1f}%)")

    # --- 설치형태 ---
    p("\n=== 설치형태 ===")
    p(df["설치형태"].value_counts().to_string())

    # --- 보관대수 ---
    p("\n=== 보관대수 ===")
    p(f"합계 {cap.sum():,.0f}대 · 중앙값 {cap.median():.0f} · 최대 {cap.max():.0f} · "
      f"0대라고 적은 곳 {(cap==0).sum():,}")
    p(cap.value_counts().sort_index().head(16).to_string())
    i = cap.idxmax()
    p(f"가장 큰 값 {cap.max():.0f}대 — {name[i]}")

    # --- 이름 ---
    p("\n=== 이름 ===")
    vc = name.value_counts()
    p(f"고유 {name.nunique():,} · 1회성 {(vc==1).sum():,}")
    p(vc.head(12).to_string())
    tok = name.str.replace(r"[()\[\],]", " ", regex=True).str.split().explode()
    tok = tok[tok.str.len() >= 2]
    p("\n이름에 자주 들어간 낱말:")
    p(tok.value_counts().head(16).to_string())
    p(f"\n가장 긴 이름 {name.str.len().max()}자")
    for s in name[name.str.len() == name.str.len().max()].unique()[:2]:
        p(f"   {s}")
    one = name[name.str.len() == 1]
    p(f"이름을 한 글자로 적은 곳 {len(one):,} — " + ", ".join(sorted(one.unique())))

    # --- 데이터의 흠 ---
    p("\n=== 글자가 깨진 칸 ===")
    bn = name[name.str.contains("?", regex=False)]
    bo = org[org.str.contains("?", regex=False)]
    p(f"보관소명 {len(bn):,}곳 · 관리기관명 {len(bo):,}곳")
    for s in list(bn.unique())[:8]:
        p(f"   {s}")
    for s in list(bo.unique())[:4]:
        p(f"   {s}")

    p("\n=== 관리기관 ===")
    p(f"고유 {org.nunique():,} · 1회성 {(org.value_counts()==1).sum():,}")
    p(org.value_counts().head(10).to_string())

    p("\n=== 설치연도 ===")
    y = df["설치연도"]
    p(f"적은 곳 {(y!='').sum():,} ({(y!='').sum()/n*100:.1f}%)")
    yv = pd.to_numeric(y[y != ""], errors="coerce").value_counts().sort_index()
    p(yv.to_string())
    p(f"최다 {yv.idxmax():.0f}년 {yv.max():,}곳")

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
