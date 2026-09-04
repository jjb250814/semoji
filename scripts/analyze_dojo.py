"""
체육도장.csv 에서 제20호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py martial_arts_dojo 체육도장

사용법:
    python scripts/analyze_dojo.py

※ 조심할 것

1. **「용인대」가 학교인지 지명인지 먼저 확인했다.**
   용인대가 들어간 도장 2,322곳 중 주소에 '용인'이 있는 곳은 136곳(5.9%)뿐이고
   경기 1,064 · 서울 327 · 인천 200 처럼 전국에 흩어져 있다. 지명이 아니라
   학교 이름이다. **이 검사를 빼먹으면 통째로 틀린 이야기가 된다.**

2. **도장 이름을 낱개로 옮기지 않는다.**
   상호는 공개 데이터지만, 「○○대 석사 태권도」 같은 이름은 특정 관장의
   학력을 그대로 가리킨다. 세는 것과 지목하는 것은 다르다.
   페이지에는 **낱말의 개수만** 쓰고 실제 상호는 쓰지 않는다.

3. **학벌을 적은 것을 흠으로 쓰지 않는다.**
   자격을 내거는 것은 정상적인 영업이다. 세모지가 셀 것은 '그런 관행이 있다'는
   사실이지 '그래서 어떻다'가 아니다.

4. 「업태구분명」이 39.9% 비어 있다. 종목별 비율을 낼 때는 채워진 것만
   분모로 삼되, 빈칸이 얼마인지 반드시 같이 밝힌다.
"""
import io
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "체육도장.csv"
OUT = ROOT / "data" / "분석결과_체육도장.txt"

UNIV = r"용인대|경희대|한국체대|한체대|단국대|계명대|동아대|우석대|조선대"
# 앞에서 잡힌 것은 뒤에서 다시 세지 않는다
GROUPS = [("대학 이름", UNIV), ("국가대표", r"국가대표"),
          ("석사 · 박사", r"석사|박사"), ("올림픽 · 금메달", r"올림픽|금메달")]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py martial_arts_dojo 체육도장` 를 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    nm = df["사업장명"]
    addr = df["지번주소"].where(df["지번주소"] != "", df["도로명주소"])
    sido = addr.str.split().str[0]
    lic = pd.to_datetime(df["인허가일자"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳")
    for k, v in df["영업상태명"].value_counts().items():
        p(f"  {k:<22} {v:>6,}  {v/n*100:>5.1f}%")

    p("\n=== 먼저 확인: 「용인대」는 학교인가 지명인가 ===")
    u = nm.str.contains("용인대", regex=False)
    inyongin = addr[u].str.contains("용인").sum()
    p(f"용인대가 들어간 도장 {u.sum():,}곳")
    p(f"  그중 주소에 '용인'이 있는 곳 {inyongin:,}곳 ({inyongin/u.sum()*100:.1f}%)")
    p("  시도 분포: " + " · ".join(f"{k} {v:,}" for k, v in sido[u].value_counts().head(6).items()))
    p("→ 전국에 흩어져 있다. 지명이 아니라 학교 이름이다.")

    p("\n=== 간판에 적힌 자격 ===")
    taken = pd.Series(False, index=df.index)
    for lab, pat in GROUPS:
        m = nm.str.contains(pat, regex=True) & ~taken
        taken |= m
        p(f"  {lab:<14} {m.sum():>6,}  {m.sum()/n*100:>5.2f}%")
    p(f"  {'합계':<14} {taken.sum():>6,}  {taken.sum()/n*100:>5.2f}%")
    p("\n낱말 하나씩 (겹쳐 세는 값):")
    for w in ["용인대", "경희대", "한국체대", "한체대", "국가대표", "석사",
              "박사", "올림픽", "금메달"]:
        c = nm.str.contains(w, regex=False).sum()
        p(f"  {w:<8} {c:>6,}  {c/n*100:>5.2f}%")

    p("\n=== 종목 ===")
    vc = df["업태구분명"].value_counts()
    blank = (df["업태구분명"] == "").sum()
    p(f"빈칸 {blank:,} ({blank/n*100:.1f}%) — 종목 비율은 채워진 {n-blank:,}곳만 놓고 본다")
    for k, v in vc.items():
        if k == "":
            continue
        p(f"  {k:<8} {v:>6,}  {v/(n-blank)*100:>5.1f}%")

    p("\n=== 종목별 자격 표기 비율 ===")
    for s in ["태권도", "유도", "합기도", "권투", "검도", "레슬링", "우슈"]:
        m = df["업태구분명"] == s
        if m.sum():
            p(f"  {s:<6} {m.sum():>6,}곳 중 {(m & taken).sum():>5,}"
              f"  ({(m & taken).sum()/m.sum()*100:>4.1f}%)")

    p("\n=== 그 밖 ===")
    p(f"공립 {(df['공사립구분명'] == '공립').sum():,} / "
      f"사립 {(df['공사립구분명'] == '사립').sum():,}")
    ld = df["지도자수"]
    p(f"지도자수: 빈칸 {(ld == '').sum():,} · "
      + " · ".join(f"{k}명 {v:,}" for k, v in ld[ld != ""].value_counts().head(5).items()))
    p("상세영업상태명: " + " · ".join(f"{k} {v:,}" for k, v in
                                df["상세영업상태명"].value_counts().head(6).items()))

    p("\n=== 수명 ===")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")
    life = ((cl - lic).dt.days / 365.25).dropna()
    life = life[life >= 0]
    p(f"폐업 {len(life):,}곳 · 중앙 {life.median():.1f}년 · 최장 {life.max():.1f}년")
    y = lic.dt.year
    p(f"인허가 연도 {int(y.min())} ~ {int(y.max())}")

    p("\n=== 데이터의 흠 ===")
    p(f"업태구분명이 「야구종목」인 체육도장 {(df['업태구분명'] == '야구종목').sum()}곳")
    p(f"업태구분명 빈칸 {blank:,} ({blank/n*100:.1f}%)")
    p(f"지도자수가 「0」 {(ld == '0').sum():,}곳")
    p(f"가장 긴 이름 {nm.str.len().max()}자")
    p("※ 상호는 옮기지 않는다. 특정 관장의 학력을 지목하게 된다.")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
