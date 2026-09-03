"""
식품자판기.csv 에서 vending.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py food_vending_machines 식품자판기

사용법:
    python scripts/analyze_vending.py
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "식품자판기.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_자판기.txt"

# 서식이 자판기에게 물어보는 '회사' 질문들.
PEOPLE = ["본사직원수", "공장사무직직원수", "공장생산직직원수", "공장판매직직원수",
          "남성종사자수", "여성종사자수"]
MONEY = ["보증액", "월세액"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def zero_line(df, col):
    v = df[col]
    fill = (v != "").sum()
    zero = (v == "0").sum()
    return fill, zero, zero / max(fill, 1) * 100


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py food_vending_machines 식품자판기` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    name = df["사업장명"]
    alive = df["영업상태명"] == "영업/정상"

    p("=== 페이지 상단 지표 ===")
    p(f"등록된 자판기   {n:,}대")
    p(f"폐업          {(~alive).sum():,} ({(~alive).sum()/n*100:.1f}%) · "
      f"영업 중 {alive.sum():,}")

    # --- 이 페이지의 제목 ---
    p("\n=== 서식이 자판기에게 묻는 '회사' 질문 ===")
    p(f"{'칸':<16}{'적은 곳':>10}{'채움':>8}{'0이라 답':>10}{'0 비율':>9}")
    for c in PEOPLE + MONEY:
        fill, zero, pct = zero_line(df, c)
        p(f"{c:<16}{fill:>10,}{fill/n*100:>7.1f}%{zero:>10,}{pct:>8.1f}%")
    p("\n0이 아닌 답도 있다 (본사직원수):")
    v = df["본사직원수"]
    p(v[(v != "") & (v != "0")].value_counts().head(6).to_string())

    p("\n=== 시설총규모 ===")
    fill, zero, pct = zero_line(df, "시설총규모")
    p(f"적은 곳 {fill:,} ({fill/n*100:.1f}%) · 0이라 답 {zero:,} ({pct:.1f}%)")
    p(df["시설총규모"][df["시설총규모"] != ""].value_counts().head(8).to_string())

    # --- 이름 ---
    p("\n=== 이름 ===")
    vc = name.value_counts()
    p(f"고유 {name.nunique():,} · 1회성 {(vc==1).sum():,}")
    p("가장 흔한 15:")
    p(vc.head(15).to_string())
    one = name[name.str.len() == 1]
    p(f"\n한 글자로 적은 곳 {len(one):,}")
    p(one.value_counts().head(12).to_string())
    p(f"\n가장 긴 이름 {name.str.len().max()}자")
    for s in name[name.str.len() == name.str.len().max()].unique()[:2]:
        p(f"   {s}")

    # 같은 브랜드를 한글로도 영문으로도 적는다.
    # 겹치는 문자열('GS'가 'GS25'를 물고 들어오는 식)은 빼고 서로 배타적인 쌍만 센다.
    p("\n=== 같은 편의점, 다른 표기 ===")
    for brand, ko, en in (("CU", "씨유", "CU"),
                          ("GS25", "지에스25", "GS25"),
                          ("이마트24", "이마트24", "emart24")):
        a = name.str.contains(ko, regex=False).sum()
        b = name.str.contains(en, regex=False).sum()
        p(f"{brand:<8} 「{ko}」 {a:,} · 「{en}」 {b:,}")

    # --- 곁가지 칸 ---
    p("\n=== 급수시설구분명 — 자판기에 수도를 묻는다 ===")
    p(df["급수시설구분명"].value_counts().to_string())
    p("\n=== 등급구분명 ===")
    p(df["등급구분명"].value_counts().to_string())
    p("\n=== 영업장주변구분명 ===")
    p(df["영업장주변구분명"].value_counts().to_string())
    p("\n=== 다중이용업소여부 ===")
    p(df["다중이용업소여부"].value_counts().to_string())

    # --- 생존 ---
    p("\n=== 생존 ===")
    op = pd.to_datetime(df["인허가일자"], errors="coerce")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")
    life = (cl - op).dt.days
    life = life[life >= 0]
    p(f"수명 중앙값 {life.median()/365:.2f}년 ({life.median():.0f}일) · "
      f"최단 {life.min():.0f}일 · 최장 {life.max()/365:.1f}년")
    p(f"1년을 못 버틴 것 {(life<365).sum():,} ({(life<365).sum()/len(life)*100:.1f}%)")
    p(f"하루 만에 사라진 것 {(life<=1).sum():,}")
    years = op.dt.year.value_counts().sort_index()
    p("\n연도별 신규 (1980~):")
    p(years[(years.index >= 1980) & (years.index <= 2026)].to_string())
    p(f"최다 {years.idxmax():.0f}년 {years.max():,}대")
    sel = years[(years.index >= 2010) & (years.index <= 2026)]
    p(f"2010년 이후 최저 {sel.idxmin():.0f}년 {sel.min():,}대")
    p(f"1980년 이전으로 적힌 것 {years[years.index < 1980].sum():,} "
      f"(가장 이른 값 {years.index.min():.0f})")

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
