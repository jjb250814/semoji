"""
공중화장실.csv 에서 restroom.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py public_restroom_info 공중화장실

사용법:
    python scripts/analyze_toilet.py
"""
import io
import re
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "공중화장실.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_공중화장실.txt"

# 변기 칸. 남성용은 6가지를 묻고 여성용은 3가지를 묻는다 (소변기 항목이 없다).
FIXTURES = [
    "남성용-대변기수", "남성용-소변기수",
    "남성용-장애인용대변기수", "남성용-장애인용소변기수",
    "남성용-어린이용대변기수", "남성용-어린이용소변기수",
    "여성용-대변기수", "여성용-장애인용대변기수", "여성용-어린이용대변기수",
]

# 「아홉 시부터 여섯 시까지」 하나만 뜻하는 표기를 골라내는 자.
# 요일·휴무 조건이 붙은 것은 뜻이 달라지므로 제외한다.
NINE_TO_SIX = re.compile(r"^\(?(평일)?\)?\s*0?9\s*[:시]?\s*0?0?\s*[~\-–]\s*18\s*[:시]?\s*0?0?\s*$")
ALL_DAY = re.compile(r"^(24시간|0?0:00\s*[~\-]\s*24:00|상시|연중무휴)$")

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py public_restroom_info 공중화장실` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    name = df["화장실명"]
    addr = df["소재지도로명주소"].where(df["소재지도로명주소"] != "", df["소재지지번주소"])
    sido = addr.str.split().str[0]
    for c in FIXTURES:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    total = df[FIXTURES].sum(axis=1)

    p("=== 페이지 상단 지표 ===")
    p(f"화장실        {len(df):,}곳")
    p(f"변기 총합      {total.sum():,.0f}개")
    p(f"이름          {name.nunique():,}가지 (1회만 등장 {(name.value_counts()==1).sum():,})")

    # --- 이 페이지의 제목 ---
    od = df["개방시간상세"]
    od = od[od != ""]
    nine = od[od.str.match(NINE_TO_SIX)]
    p("\n=== 「09시부터 18시까지」를 적는 방법 — 이 페이지의 제목 ===")
    p(f"표기 {nine.nunique()}가지 · {len(nine):,}건")
    p(nine.value_counts().to_string())

    allday = od[od.str.match(ALL_DAY)]
    p(f"\n=== 「24시간」을 적는 방법 — {allday.nunique()}가지 · {len(allday):,}건 ===")
    p(allday.value_counts().to_string())

    p(f"\n개방시간상세를 적은 곳 {len(od):,} / 고유 표기 {od.nunique():,} / "
      f"딱 한 번만 쓰인 표기 {(od.value_counts()==1).sum():,}")
    p("한 번뿐인 표기 예시:")
    once = od[od.map(od.value_counts()) == 1]
    for s in once.head(8):
        p(f"   {s}")

    # --- 이름 ---
    p("\n=== 화장실의 이름 ===")
    vc = name.value_counts()
    p(f"고유 이름 {name.nunique():,} · 딱 한 번만 쓰인 이름 {(vc==1).sum():,}")
    p("가장 흔한 이름:")
    p(vc.head(12).to_string())
    p(f"\n가장 긴 이름 {name.str.len().max()}자")
    for s in name[name.str.len() == name.str.len().max()].unique()[:3]:
        p(f"   {s}")
    p(f"가장 짧은 이름 {name.str.len().min()}자: "
      + ", ".join(name[name.str.len() == name.str.len().min()].unique()))
    p(f"이름을 '기타'라고 적은 곳 {(name=='기타').sum()}곳")
    tok = name.str.replace(r"[()\[\]]", " ", regex=True).str.split().explode()
    tok = tok[tok.str.len() >= 2]
    p("자주 쓰인 낱말:")
    p(tok.value_counts().head(15).to_string())

    # --- 종류와 처리방식 ---
    p("\n=== 구분 ===")
    p(df["구분명"].value_counts().to_string())
    p("\n=== 오물처리방식 ===")
    p(df["오물처리방식"].value_counts().to_string())
    t = pd.crosstab(sido, df["오물처리방식"])
    t = t[t.sum(axis=1) >= 200]
    p("수거식 비율이 높은 시도 (200곳 이상만):")
    p((t["수거식"] / t.sum(axis=1) * 100).sort_values(ascending=False).head(8).round(1).to_string())

    # --- 변기 ---
    p("\n=== 변기 ===")
    for c in FIXTURES:
        p(f"{c:<22} 합계 {df[c].sum():>9,.0f}  평균 {df[c].mean():>5.2f}  최대 {df[c].max():>5.0f}")
    has = total > 0
    p(f"\n변기가 0개로 적힌 곳 {(~has).sum():,}")
    m_all = df["남성용-대변기수"] + df["남성용-소변기수"]
    w_big = df["여성용-대변기수"]
    p(f"남성 대변기+소변기가 여성 대변기보다 많은 곳 "
      f"{((w_big < m_all) & has).sum():,} ({((w_big < m_all) & has).sum()/has.sum()*100:.1f}%)")
    p(f"평균 남성 {m_all[has].mean():.2f} / 여성 {w_big[has].mean():.2f}")
    dis = (df["남성용-장애인용대변기수"] + df["남성용-장애인용소변기수"]
           + df["여성용-장애인용대변기수"])
    p(f"장애인용이 하나도 없는 곳 {((dis==0)&has).sum():,} "
      f"({((dis==0)&has).sum()/has.sum()*100:.1f}%)")
    i = total.idxmax()
    p(f"변기가 가장 많이 적힌 한 줄 {total.max():.0f}개 — {sido[i]} · {name[i]}")

    # --- 데이터의 흠 ---
    p("\n=== 설치연월 — 데이터의 흠 ===")
    ym = df["설치연월"]
    yr = pd.to_numeric(ym.str[:4], errors="coerce")
    p(f"적은 곳 {(ym!='').sum():,} / {len(df):,} ({(ym!='').sum()/len(df)*100:.1f}%)")
    p(f"가장 이른 값 {yr.min():.0f} · 가장 늦은 값 {yr.max():.0f}")
    p(f"1930년 이전 {((yr<1930)).sum():,}곳 · 2027년 이후 {((yr>2026)).sum():,}곳")
    p("1905년으로 적힌 곳의 시도 분포:")
    p(sido[yr == 1905].value_counts().head(5).to_string())
    p("미래로 적힌 곳 예시:")
    for _, r in df[yr > 2026].head(6).iterrows():
        p(f"   {r['설치연월']}  {r['화장실명'][:26]}  ({sido[_]})")

    p("\n=== 안전·편의 칸이 묻는 것 ===")
    for c in ["비상벨설치여부", "화장실입구CCTV설치유무", "기저귀교환대유무"]:
        v = df[c].value_counts()
        p(f"{c}: Y {v.get('Y',0):,} / N {v.get('N',0):,}")
    p("\n비상벨을 어디에 달았나 (적은 곳만):")
    bell = df["비상벨설치장소"]
    p(bell[bell != ""].value_counts().head(8).to_string())
    p("\n기저귀교환대를 어디에 두었나 (적은 곳만):")
    chg = df["기저귀교환대장소"]
    p(chg[chg != ""].value_counts().to_string())

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
