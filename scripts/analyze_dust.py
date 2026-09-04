"""
비산먼지.csv 에서 제18호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py dust_emission_business_info 비산먼지

사용법:
    python scripts/analyze_dust.py

※ 조심할 것

1. **「개인」이 왜 16만 건인지 단정하지 않는다.**
   2013년 6.2% → 2014년 13.5% → 2015년 30.7% 로 한 해 만에 뛴다.
   서서히가 아니라 계단이라 서식이나 공개 정책이 바뀐 신호로 보이지만,
   원본 어디에도 그렇게 적혀 있지 않다. 읽을 수 있는 방법이 둘이다 —
   개인 신고가 실제로 늘었거나, 개인 이름을 「개인」으로 바꿔 내보내기
   시작했거나. **어느 쪽인지는 데이터가 말해 주지 않는다.**

2. **2015년 이전 기록에 남아 있는 개인 이름을 옮겨 적지 않는다.**
   상호 칸에 사람 이름으로 보이는 값이 실제로 들어 있다. 공개 데이터라도
   이 사이트가 그것을 다시 퍼뜨릴 이유가 없다. 이 스크립트도 개수만 세고
   값은 찍지 않는다.

3. **데이터의 흠에 업체 이름을 붙이지 않는다.**
   「2999년에 끝나는 공사」는 담당자가 칸을 잘못 채운 것이지 그 업체의
   잘못이 아니다. 이름을 붙이면 잡학이 아니라 특정 업체 망신주기가 된다.

4. 2026년은 여덟 달치뿐이다(원본 2026-09-04 내려받음). 연도별 표에서
   2026을 다른 해와 나란히 놓고 "줄었다" 고 말하면 틀린다.
"""
import io
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "비산먼지.csv"
OUT = ROOT / "data" / "분석결과_비산먼지.txt"

# 공사장명에서 세어 볼 낱말
WORDS = ["공사", "신축", "주택", "공장", "도로", "성토", "증축",
         "창고", "아파트", "태양광", "철거", "축사", "리모델링"]

# 이름 대신 들어간 값들
NONAME = ["개인", "-", "없음", "상호없음", "개인직영", "자가시공", "무", "개인사업자"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py dust_emission_business_info 비산먼지` "
                         f"를 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="c", low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    biz = df["사업자명(상호)"]
    site = df["공사장명"]
    start = pd.to_datetime(df["설치(공사)시작일"], errors="coerce")
    end = pd.to_datetime(df["설치(공사)종료일"], errors="coerce")
    days = (end - start).dt.days
    filed = pd.to_datetime(df["데이터기준일자(신고일자)"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 신고 {n:,}건 · 칸 {len(df.columns)}개")
    yr = filed.dt.year
    inr = yr[(yr >= 1990) & (yr <= 2026)]
    p(f"신고 연도 {int(inr.min())} ~ {int(inr.max())}")
    p(f"관리기관 {df['관리기관명'].nunique():,}곳")

    p("\n=== 상호 칸에 이름이 없는 신고 ===")
    tot = 0
    for w in NONAME:
        c = (biz == w).sum()
        if c:
            p(f"  「{w}」 {c:>8,}  {c/n*100:>5.2f}%")
            tot += c
    p(f"  빈칸 {(biz == '').sum():>10,}  {(biz == '').sum()/n*100:>5.2f}%")
    p(f"  합계 {tot + (biz == '').sum():>10,}  "
      f"{(tot + (biz == '').sum())/n*100:>5.2f}%")
    p(f"고유 상호 {biz.nunique():,}가지")
    p("가장 많이 적힌 상호 (「개인」 다음부터가 실제 회사다):")
    p(biz[biz != ""].value_counts().head(8).to_string())

    p("\n=== 「개인」이 뛴 해 ===")
    g = biz == "개인"
    t = pd.crosstab(yr, g)
    t.columns = ["그외", "개인"] if True in t.columns else ["그외"]
    t["합계"] = t.sum(axis=1)
    t["개인%"] = (t["개인"] / t["합계"] * 100).round(1)
    p(t[(t.index >= 2005) & (t.index <= 2026)].to_string())
    p("※ 2013년 6.2% → 2014년 13.5% → 2015년 30.7%. 계단식이다.")
    p("※ 왜 뛰었는지는 원본에 적혀 있지 않다. 단정하지 않는다.")
    p("※ 2026년은 여덟 달치뿐이다.")

    p("\n=== 사람 이름으로 보이는 값이 남아 있나 (개수만 센다) ===")
    NAMEY = re.compile(r"^[가-힣]{2,4}$")
    CORP = re.compile(r"주식회사|\(주\)|㈜|건설|산업|개발|토건|엔지|종합|공사|주\)|유한|합자")
    cand = biz[biz.str.match(NAMEY) & ~biz.str.contains(CORP, regex=True)
               & ~biz.isin(NONAME)]
    p(f"  2~4자 한글이면서 회사 표식이 없는 값 {cand.nunique():,}가지 · {len(cand):,}건")
    p("  ※ 값은 찍지 않는다. 사람 이름이 섞여 있다.")

    p("\n=== 공사장 이름 ===")
    p(f"고유 {site.nunique():,}가지 / {n:,}건")
    p("가장 흔한 이름:")
    p(site[site != ""].value_counts().head(12).to_string())
    p("\n자주 나오는 낱말:")
    for w in WORDS:
        c = site.str.contains(w, regex=False).sum()
        p(f"  {w:<6} {c:>8,}  {c/n*100:>5.1f}%")
    L = site.str.len()
    p(f"\n가장 긴 이름 {L.max()}자 · 한 글자 {(L == 1).sum():,}건 · 두 글자 {(L == 2).sum():,}건")

    p("\n=== 「농지성토」 ===")
    farm = site == "농지성토"
    p(f"{farm.sum():,}건 — 전국에서 가장 흔한 공사장 이름")
    p(f"  그중 상호가 「개인」 {(farm & g).sum():,}건 ({(farm & g).sum()/farm.sum()*100:.0f}%)")
    p(f"  공사기간 중앙값 {days[farm].median():.0f}일")

    p("\n=== 공사 기간 ===")
    ok = days.notna()
    p(f"계산 가능 {ok.sum():,}건")
    p(f"  중앙 {days.median():.0f}일 · 평균 {days.mean():.0f}일")
    p(f"  하루 {(days == 0).sum():,}건 · 1년 초과 {(days > 365).sum():,}건 "
      f"· 10년 초과 {(days > 3650).sum():,}건")
    p(f"  「개인」 중앙 {days[g].median():.0f}일 / 그 외 {days[~g].median():.0f}일")

    p("\n=== 발생사업명 ===")
    vc = df["발생사업명"].value_counts()
    p(f"빈칸 {(df['발생사업명'] == '').sum():,} "
      f"({(df['발생사업명'] == '').sum()/n*100:.1f}%)")
    p(vc.head(8).to_string())

    p("\n=== 데이터의 흠 ===")
    p(f"종료일이 2030년 이후 {(end.dt.year >= 2030).sum():,}건")
    p(f"  그중 2999년 {(end.dt.year == 2999).sum():,}건")
    p(f"1000년 넘는 공사 {(days > 365000).sum():,}건 · 가장 긴 것 {days.max():,.0f}일")
    p(f"신고일자가 2027년 이후 {(yr >= 2027).sum():,}건 "
      f"(값 {sorted(set(yr[yr >= 2027].dropna().astype(int)))})")
    p(f"신고일자가 2000년 이전 {(yr < 2000).sum():,}건")
    p(f"공사장명이 「-」 {(site == '-').sum():,}건")
    p("※ 흠이 있는 줄의 업체 이름은 옮기지 않는다.")

    p("\n=== 관리기관 상위 ===")
    p(df["관리기관명"].value_counts().head(8).to_string())

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
