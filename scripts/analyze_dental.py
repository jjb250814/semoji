"""
치과기공소.csv 에서 dental-lab/index.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py dental_labs 치과기공소

사용법:
    python scripts/analyze_dental.py
"""
import io
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "치과기공소.csv"
OUT = ROOT / "data" / "분석결과_치과기공소.txt"

# 서식이 하나하나 세라고 시키는 기계들. 칸 이름 순서는 서식에 적힌 대로가 아니라
# 데이터의 칸 순서를 따른다.
MACHINES = ["기공용레스수", "기공용모터수", "기공용컴프레서수", "샌드기수", "서베이어수",
            "아세틸렌수", "원심주조기수", "전기로수", "진공매몰기수", "진동기수",
            "초음파청소기수", "치과용프레스수", "트리머수", "포셀린로수", "핀덱스수"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py dental_labs 치과기공소` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    name = df["사업장명"]
    num = df[MACHINES].apply(pd.to_numeric, errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"등록된 치과기공소  {n:,}곳")
    p(f"기계를 세는 칸    {len(MACHINES)}개")
    p(f"기계 총합        {num.sum().sum():,.0f}대")
    alive = (df["영업상태명"] == "영업/정상").sum()
    p(f"영업 중          {alive:,} ({alive/n*100:.1f}%)")

    # --- 이 페이지의 제목 ---
    p("\n=== 열다섯 가지 기계 ===")
    p(f"{'칸':<14}{'적은 곳':>8}{'채움':>7}{'합계':>9}{'1대':>8}{'1대 비율':>9}{'최대':>6}")
    for c in MACHINES:
        v = num[c]
        fill = (df[c] != "").sum()
        one = (v == 1).sum()
        p(f"{c:<14}{fill:>8,}{fill/n*100:>6.1f}%{v.sum():>9,.0f}{one:>8,}"
          f"{one/max(fill,1)*100:>8.1f}%{v.max():>6.0f}")
    p(f"\n전국 합계 {num.sum().sum():,.0f}대")

    # --- 몇 가지를 갖췄나 ---
    p("\n=== 한 곳이 갖춘 기계 종류 수 ===")
    filled = num.fillna(0)
    kinds = (filled > 0).sum(axis=1)
    p(kinds.value_counts().sort_index().to_string())
    p(f"중앙값 {kinds.median():.0f}종 · 열다섯 가지를 다 갖춘 곳 "
      f"{(kinds==15).sum():,} ({(kinds==15).sum()/n*100:.1f}%)")
    tot = filled.sum(axis=1)
    p(f"한 곳의 기계 총합 중앙값 {tot.median():.0f}대 · 최대 {tot.max():.0f}대")

    # --- 채움률이 갈리는 칸 ---
    p("\n=== 채움률이 갈린다 ===")
    fills = {c: (df[c] != "").sum() for c in MACHINES}
    for lvl in sorted({round(v / n * 100, 1) for v in fills.values()}, reverse=True):
        cols = [c for c in MACHINES if round(fills[c] / n * 100, 1) == lvl]
        p(f"  채움 {lvl:>5.1f}% : " + ", ".join(cols))
    low = [c for c in MACHINES if fills[c] / n < 0.95]
    op = pd.to_datetime(df["인허가일자"], errors="coerce")
    if low:
        blank = df[low[0]] == ""
        same = all((df[c] == "").equals(blank) for c in low)
        p(f"\n채움률이 낮은 칸 {len(low)}개가 비어 있는 줄이 서로 같은가: {same}")
        p(f"  그 줄 수 {blank.sum():,}")
        # 비운 줄의 인허가일자가 한 날짜에서 끊긴다. 그날 무언가 바뀌었다.
        cut = op[blank].max()
        before, after = op <= cut, op > cut
        p(f"  비운 줄의 인허가일자 최대 {cut.date()}")
        p(f"  그날까지 등록한 {before.sum():,}곳 중 비운 곳 {(blank & before).sum():,} "
          f"({(blank & before).sum()/before.sum()*100:.1f}%)")
        p(f"  그날 뒤에 등록한 {after.sum():,}곳 중 비운 곳 {(blank & after).sum():,}")
        p("  (무엇이 바뀌었는지는 데이터에 없다)")
    ace = df["아세틸렌수"] == ""
    p(f"\n아세틸렌 빈칸 {ace.sum():,} · 인허가일자 최대 {op[ace].max().date()}"
      f" · 위 네 칸과 겹치지 않는 것 {(ace & ~blank).sum():,}")

    # --- 이름 ---
    p("\n=== 이름 ===")
    vc = name.value_counts()
    p(f"고유 {name.nunique():,} · 1회성 {(vc==1).sum():,}")
    p(vc.head(12).to_string())
    p(f"\n'기공소'가 든 상호 {name.str.contains('기공소', regex=False).sum():,} "
      f"({name.str.contains('기공소', regex=False).sum()/n*100:.1f}%)")
    p(f"'덴탈' 또는 '덴털'이 든 상호 {name.str.contains('덴탈|덴털').sum():,}")
    p(f"영문 'Dental'이 든 상호 {name.str.contains('Dental', case=False, regex=False).sum():,}")
    p(f"가장 긴 이름 {name.str.len().max()}자")
    for s in name[name.str.len() == name.str.len().max()].unique()[:2]:
        p(f"   {s}")

    # --- 생존 ---
    p("\n=== 생존 ===")
    p(df["영업상태명"].value_counts().to_string())
    op = pd.to_datetime(df["인허가일자"], errors="coerce")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")
    life = (cl - op).dt.days
    life = life[life >= 0]
    p(f"\n수명 중앙값 {life.median()/365:.2f}년 ({life.median():.0f}일) · "
      f"최단 {life.min():.0f}일 · 최장 {life.max()/365:.1f}년")
    yrs = op.dt.year.value_counts().sort_index()
    p(f"최다 {yrs.idxmax():.0f}년 {yrs.max():,}곳 · 가장 이른 {yrs.index.min():.0f}년")
    p("\n연도별 신규 (1988~):")
    p(yrs[yrs.index >= 1988].to_string())

    p("\n=== 시도 ===")
    addr = df["도로명주소"].where(df["도로명주소"] != "", df["지번주소"])
    sido = addr.str.split().str[0]
    p(sido.value_counts().head(10).to_string())
    p(f"서울 비중 {sido.eq('서울특별시').sum()/n*100:.1f}%")

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print("-> " + str(OUT))


if __name__ == "__main__":
    main()
