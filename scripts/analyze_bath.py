"""
목욕장업.csv 에서 bathhouse/index.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py public_baths 목욕장업

사용법:
    python scripts/analyze_bath.py
"""
import io
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "목욕장업.csv"
OUT = ROOT / "data" / "분석결과_목욕장업.txt"

# 상호에서 세는 낱말. 물 이름이 앞에 붙고 뒤에 '탕'이 오는 것이 오래된 방식이다.
WORDS = ["탕", "목욕", "사우나", "스파", "한증", "찜질", "온천", "불가마"]
DECADES = [(1960, 1979), (1980, 1989), (1990, 1999),
           (2000, 2009), (2010, 2019), (2020, 2026)]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py public_baths 목욕장업` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    name = df["사업장명"]
    alive = df["영업상태명"] == "영업/정상"
    sweat = df["발한실여부"]
    op = pd.to_datetime(df["인허가일자"], errors="coerce")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"등록된 목욕장    {n:,}곳")
    p(f"폐업            {(~alive).sum():,} ({(~alive).sum()/n*100:.1f}%) · "
      f"영업 중 {alive.sum():,}")

    # --- 이 페이지의 제목 ---
    p("\n=== 「발한실여부」 — 땀 내는 방이 있는가 ===")
    p(sweat.value_counts().to_string())
    filled = (sweat != "").sum()
    y = (sweat == "Y").sum()
    no = (sweat == "N").sum()
    p(f"적은 곳 {filled:,} ({filled/n*100:.1f}%) · "
      f"Y {y:,} ({y/filled*100:.1f}%) · N {no:,} ({no/filled*100:.1f}%)")
    p(f"\n영업 중인 곳: Y {(alive & (sweat=='Y')).sum():,} / "
      f"N {(alive & (sweat=='N')).sum():,} "
      f"→ Y 비율 {(alive & (sweat=='Y')).sum()/((alive)&(sweat!='')).sum()*100:.1f}%")
    p(f"폐업한 곳:   Y {((~alive) & (sweat=='Y')).sum():,} / "
      f"N {((~alive) & (sweat=='N')).sum():,} "
      f"→ Y 비율 {((~alive)&(sweat=='Y')).sum()/((~alive)&(sweat!='')).sum()*100:.1f}%")

    p("\n=== 허가 연도대별 발한실 비율 ===")
    for lo, hi in DECADES:
        sel = (op.dt.year >= lo) & (op.dt.year <= hi) & (sweat != "")
        if sel.sum():
            yy = (sweat[sel] == "Y").sum()
            p(f"  {lo}~{hi}  {sel.sum():>6,}곳 · Y {yy:>5,} ({yy/sel.sum()*100:>5.1f}%)")

    # --- 업태 ---
    p("\n=== 업태구분명 ===")
    p(df["업태구분명"].value_counts().to_string())
    p("\n업태별 폐업률:")
    t = pd.crosstab(df["업태구분명"], alive)
    t.columns = ["폐업", "영업"] if False in t.columns else t.columns
    for k in df["업태구분명"].value_counts().index:
        sel = df["업태구분명"] == k
        dead = (sel & ~alive).sum()
        p(f"  {k:<22}{sel.sum():>6,}곳 · 폐업 {dead:>6,} ({dead/sel.sum()*100:>5.1f}%)")

    # --- 생존 ---
    p("\n=== 생존 ===")
    life = (cl - op).dt.days
    life = life[life >= 0]
    p(f"수명 중앙값 {life.median()/365:.2f}년 ({life.median():.0f}일) · "
      f"최단 {life.min():.0f}일 · 최장 {life.max()/365:.1f}년")
    yrs = op.dt.year.value_counts().sort_index()
    p(f"신규 최다 {yrs.idxmax():.0f}년 {yrs.max():,}곳 · 가장 이른 {yrs.index.min():.0f}년")
    p(f"1960년 이전으로 적힌 것 {yrs[yrs.index < 1960].sum():,}곳")
    p("\n연도별 신규 (1970~):")
    p(yrs[yrs.index >= 1970].to_string())
    cy = cl.dt.year.value_counts().sort_index()
    p(f"\n폐업 최다 {cy.idxmax():.0f}년 {cy.max():,}곳")
    p("연도별 폐업 (2000~):")
    p(cy[cy.index >= 2000].to_string())

    # --- 욕실 · 층 ---
    p("\n=== 욕실수 ===")
    bath = pd.to_numeric(df["욕실수"], errors="coerce")
    p(f"적은 곳 {(df['욕실수']!='').sum():,} · 합계 {bath.sum():,.0f} · "
      f"중앙값 {bath.median():.0f} · 최대 {bath.max():.0f}")
    p(f"0이라 적은 곳 {(bath==0).sum():,} "
      f"({(bath==0).sum()/(df['욕실수']!='').sum()*100:.1f}%)")
    p(df["욕실수"][df["욕실수"] != ""].value_counts().head(8).to_string())

    p("\n=== 층을 적는 네 칸 ===")
    for c in ["사용시작지상층", "사용끝지상층", "사용시작지하층", "사용끝지하층"]:
        v = df[c][df[c] != ""]
        p(f"{c}: 적은 곳 {len(v):,} ({len(v)/n*100:.1f}%) · " +
          ", ".join(f"{k}({cnt:,})" for k, cnt in v.value_counts().head(5).items()))

    # --- 이름 ---
    p("\n=== 이름 ===")
    vc = name.value_counts()
    p(f"고유 {name.nunique():,} · 1회성 {(vc==1).sum():,}")
    p(vc.head(12).to_string())
    p("\n상호에 든 낱말:")
    for w in WORDS:
        c = name.str.contains(w, regex=False).sum()
        p(f"  {w:<5}{c:>6,}  ({c/n*100:>4.1f}%)")
    p(f"\n가장 긴 이름 {name.str.len().max()}자")
    for s in name[name.str.len() == name.str.len().max()].unique()[:2]:
        p(f"   {s}")
    # 옛 이름과 새 이름을 연도로 갈라 본다
    p("\n허가 연도대별 상호 낱말 비율:")
    for lo, hi in DECADES:
        sel = (op.dt.year >= lo) & (op.dt.year <= hi)
        if not sel.sum():
            continue
        parts = []
        for w in ["탕", "사우나", "스파", "찜질"]:
            c = name[sel].str.contains(w, regex=False).sum()
            parts.append(f"{w} {c/sel.sum()*100:.1f}%")
        p(f"  {lo}~{hi}  {sel.sum():>6,}곳 · " + " · ".join(parts))

    p("\n=== 조건부허가신고사유 ===")
    c = df["조건부허가신고사유"]
    p(f"적은 곳 {(c!='').sum():,}")
    for s in c[c != ""].unique()[:4]:
        p(f"   {s[:90]}")

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print("-> " + str(OUT))


if __name__ == "__main__":
    main()
