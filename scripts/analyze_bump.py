"""
과속방지턱.csv 에서 bump.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py speed_bump_info 과속방지턱

사용법:
    python scripts/analyze_bump.py
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "과속방지턱.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_과속방지턱.txt"

# 표준 규격. 도로안전시설 설치·관리 지침이 정한 원호형 과속방지턱의 값이다.
STD_H, STD_W = 10, 360     # 높이 10cm · 폭 3.6m(=360cm)

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py speed_bump_info 과속방지턱` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    place = df["설치장소"]
    mat = df["과속방지턱재료"]
    form = df["과속방지턱형태구분"]
    h = pd.to_numeric(df["과속방지턱높이"], errors="coerce")
    w = pd.to_numeric(df["과속방지턱폭"], errors="coerce")
    L = pd.to_numeric(df["과속방지턱연장"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"과속방지턱      {n:,}개")
    p(f"설치장소 표기    {place.nunique():,}가지 "
      f"(1회만 등장 {(place.value_counts()==1).sum():,})")
    p(f"높이가 표준(10cm)인 것 {(h==STD_H).sum():,} ({(h==STD_H).sum()/n*100:.1f}%)")
    p(f"규격여부 N     {(df['규격여부']=='N').sum():,}")

    # --- 이 페이지의 제목 ---
    p("\n=== 「설치장소」 칸 — 이 페이지의 제목 ===")
    vc = place.value_counts()
    p(f"고유 표기 {place.nunique():,} · 딱 한 번만 쓰인 표기 {(vc==1).sum():,}")
    p(f"그냥 「도로」라고만 적은 곳 {vc.get('도로', 0):,} "
      f"({vc.get('도로', 0)/n*100:.1f}%)")
    p("가장 흔한 표기 15:")
    p(vc.head(15).to_string())
    p(f"\n서식 예시를 지우지 않고 낸 것 「ooo」 {vc.get('ooo', 0):,}곳")
    p("\n한 번뿐인 표기 예시:")
    for s in place[place.map(vc) == 1].head(20):
        p(f"   {s}")
    p(f"\n가장 긴 설치장소 {place.str.len().max()}자")
    for s in place[place.str.len() == place.str.len().max()].unique()[:2]:
        p(f"   {s}")

    # --- 재료 칸에 모양이 적혀 있다 ---
    p("\n=== 「재료」 칸에 적힌 답 ===")
    p(mat.value_counts().to_string())
    p("\n=== 「형태구분」 칸에 적힌 답 ===")
    p(form.value_counts().to_string())
    same = (mat == form).sum()
    p(f"\n두 칸이 같은 값인 행 {same:,} / {n:,} ({same/n*100:.1f}%)")
    p("엇갈린 조합:")
    p(pd.crosstab(mat, form).to_string())

    # --- 단위가 섞여 있다 ---
    p("\n=== 같은 칸에 센티미터와 미터가 섞여 있다 ===")
    for name, v, std in (("폭", w, STD_W), ("연장", L, None)):
        cm = ((v >= 100) & v.notna()).sum()
        m = ((v > 0) & (v < 30)).sum()
        p(f"{name}: 100 이상(센티미터로 보임) {cm:,} · 30 미만(미터로 보임) {m:,} "
          f"· 0 {int((v == 0).sum()):,} · 최대 {v.max():,.0f}")
        if std:
            p(f"   표준 {std}(=3.6m)으로 적은 곳 {(v == std).sum():,} · "
              f"4(=4m)로 적은 곳 {(v == 4).sum():,}")

    p("\n=== 높이 ===")
    p(f"최소 {h.min():.0f} · 최대 {h.max():.0f} · 중앙값 {h.median():.0f}")
    p(f"표준 10 {(h==STD_H).sum():,} ({(h==STD_H).sum()/n*100:.1f}%) · "
      f"0 {(h==0).sum():,} ({(h==0).sum()/n*100:.1f}%)")
    p(h.value_counts().sort_index().head(22).to_string())
    p(f"\n높이가 0인 것 중 형태가 '가상형' {(((h==0)) & (form=='가상형')).sum():,} / "
      f"가상형 전체 {(form=='가상형').sum():,}")

    # --- 그 밖의 흠 ---
    p("\n=== 「도로명」 칸에 도로 이름이 아닌 것 ===")
    rn = df["도로명"]
    p(f"고유값 {rn.nunique():,} · 1회성 {(rn.value_counts()==1).sum():,}")
    p(rn.value_counts().head(12).to_string())

    p("\n=== 설치연도 ===")
    y = df["과속방지턱설치연도"]
    p(f"적은 곳 {(y!='').sum():,} / {n:,} ({(y!='').sum()/n*100:.1f}%)")
    p(y[y != ""].value_counts().sort_index().to_string())

    p("\n=== 시도 ===")
    p(df["시도명"].value_counts().to_string())

    p("\n=== 관리기관 상위 ===")
    p(df["관리기관명"].value_counts().head(10).to_string())

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
