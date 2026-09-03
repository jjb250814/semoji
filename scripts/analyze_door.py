"""
방문판매업.csv 에서 door-to-door/index.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py door_to_door_sales 방문판매업

사용법:
    python scripts/analyze_door.py
"""
import io
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "방문판매업.csv"
OUT = ROOT / "data" / "분석결과_방문판매.txt"

# 다른 업종 신고서에는 없는 칸들. 방문판매업만 회사의 재무 상태를 적게 한다.
MONEY = ["자본금", "자산규모", "부채총액"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def won(n):
    """원 단위 숫자를 읽기 쉬운 말로."""
    if pd.isna(n):
        return "―"
    n = int(n)
    for unit, div in (("조", 10**12), ("억", 10**8), ("만", 10**4)):
        if n >= div:
            return f"{n/div:,.1f}{unit}원"
    return f"{n:,}원"


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py door_to_door_sales 방문판매업` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    name = df["사업장명"]
    state = df["상세영업상태명"]

    p("=== 페이지 상단 지표 ===")
    p(f"등록된 방문판매업체  {n:,}곳")
    alive = (df["영업상태명"] == "영업/정상").sum()
    p(f"영업 중            {alive:,} ({alive/n*100:.1f}%)")

    # --- 이 페이지의 제목 ---
    p("\n=== 어떻게 끝났나 — 상세영업상태 ===")
    vc = state.value_counts()
    for k, v in vc.items():
        p(f"  {k or '(빈 칸)':<12}{v:>8,}  {v/n*100:>5.1f}%")
    auto = vc.get("직권말소", 0) + vc.get("직권취소", 0)
    p(f"\n관청이 대신 지운 것(직권말소+직권취소) {auto:,} ({auto/n*100:.1f}%)")
    p(f"직권말소만 {vc.get('직권말소',0):,}")
    p(f"스스로 폐업 신고 {vc.get('폐업처리',0):,}")

    # --- 수명 ---
    p("\n=== 수명 ===")
    op = pd.to_datetime(df["인허가일자"], errors="coerce")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")
    life = (cl - op).dt.days
    life = life[life >= 0]
    p(f"폐업일자가 있는 곳 {len(life):,}")
    p(f"중앙값 {life.median()/365:.2f}년 ({life.median():.0f}일) · "
      f"최단 {life.min():.0f}일 · 최장 {life.max()/365:.1f}년")
    p(f"1년을 못 넘긴 곳 {(life<365).sum():,} ({(life<365).sum()/len(life)*100:.1f}%)")
    p(f"6개월을 못 넘긴 곳 {(life<182).sum():,} ({(life<182).sum()/len(life)*100:.1f}%)")
    p(f"하루 만에 사라진 곳 {(life<=1).sum():,}")
    p("다른 열람실과 견주면 — PC방 3.1년 · 노래방 9.5년 · 자판기 5.31년")

    # --- 돈을 묻는 칸 ---
    p("\n=== 신고서가 회사의 재무 상태를 묻는다 ===")
    for c in MONEY:
        v = pd.to_numeric(df[c], errors="coerce")
        fill = (df[c] != "").sum()
        zero = (v == 0).sum()
        p(f"\n{c}: 적은 곳 {fill:,} ({fill/n*100:.1f}%) · "
          f"0원 {zero:,} ({zero/max(fill,1)*100:.1f}%)")
        p(f"   중앙값 {won(v.median())} · 최대 {v.max():,.0f}")
        p("   자주 적힌 값: " + ", ".join(
            f"{won(float(k))}({v2:,})" for k, v2 in
            df[c][df[c] != ""].value_counts().head(5).items() if k.isdigit()))

    cap = pd.to_numeric(df["자본금"], errors="coerce")
    ast = pd.to_numeric(df["자산규모"], errors="coerce")
    deb = pd.to_numeric(df["부채총액"], errors="coerce")
    p(f"\n세 칸을 다 적은 곳 {(cap.notna()&ast.notna()&deb.notna()).sum():,}")
    p(f"자산보다 빚이 많은 곳 {((ast<deb)&ast.notna()&deb.notna()).sum():,}")
    p(f"자본금 0인데 자산은 있는 곳 {((cap==0)&(ast>0)).sum():,}")
    NINE = 999999999999999
    p(f"세 칸에 9를 열다섯 개 적은 곳: "
      f"자본금 {(cap==NINE).sum()} · 자산 {(ast==NINE).sum()} · 부채 {(deb==NINE).sum()}")
    p(f"  (999,999,999,999,999원 = 약 1,000조원)")

    # --- 이름 ---
    p("\n=== 이름 ===")
    nvc = name.value_counts()
    p(f"고유 {name.nunique():,} · 1회성 {(nvc==1).sum():,}")
    p(nvc.head(12).to_string())
    tok = name.str.replace(r"[()\[\]]", " ", regex=True).str.split().explode()
    tok = tok[tok.str.len() >= 2]
    p("\n자주 쓰인 낱말:")
    p(tok.value_counts().head(12).to_string())
    for w in ["주식회사", "카운셀러", "뷰티", "대리점", "교실"]:
        p(f"  '{w}' 들어간 상호 {name.str.contains(w, regex=False).sum():,}")
    p(f"\n가장 긴 이름 {name.str.len().max()}자")
    for s in name[name.str.len() == name.str.len().max()].unique()[:2]:
        p(f"   {s}")

    # --- 연도 ---
    p("\n=== 연도별 신규 등록 ===")
    years = op.dt.year.value_counts().sort_index()
    p(years[(years.index >= 1996) & (years.index <= 2026)].to_string())
    p(f"최다 {years.idxmax():.0f}년 {years.max():,}곳")
    p(f"1996년 이전으로 적힌 것 {years[years.index < 1996].sum():,} "
      f"(가장 이른 값 {years.index.min():.0f}년 {years.iloc[0]:,}곳)")
    p(f"재개업일자가 있는 곳 {(df['재개업일자']!='').sum():,}")

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
