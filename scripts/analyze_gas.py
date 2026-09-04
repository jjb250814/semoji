"""
고압가스.csv 에서 제19호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py specific_high_pressure_gas 고압가스

사용법:
    python scripts/analyze_gas.py

※ 조심할 것

1. **「사용방법」 칸의 원문을 그대로 찍지 않는다.**
   담당자 메모로 보이는 값이 193건 있고, 그중 8건에는 사업자등록번호나
   전화번호가 들어 있다. 이 저장소는 공개다. 개수만 세고 값은 남기지 않는다.
   (2026-09-04에 `data/광맥상세.txt` 로 이메일 19건이 실제로 사이트에
   올라간 적이 있다. 같은 일을 반복하지 않는다.)

2. **「점 하나」를 게으름으로 단정하지 않는다.**
   405곳이 사용방법 칸에 한 글자만 적었다. 답을 몰라서일 수도 있고,
   목적 칸과 같은 말이라 생략한 것일 수도 있고, 시스템이 빈칸을 막아서
   아무 글자나 넣어야 했을 수도 있다. **원본에 이유가 없다.**

3. 한 글자 답의 종류는 찍어도 된다. 사람을 특정할 수 없는 기호다.
"""
import io
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "고압가스.csv"
OUT = ROOT / "data" / "분석결과_고압가스.txt"

PURPOSE_WORDS = ["절단", "의료", "용접", "열처리", "연구", "실험",
                 "제조", "소독", "분석", "시험", "냉각", "교육"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py specific_high_pressure_gas 고압가스` "
                         f"를 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    why = df["사용목적"]
    how = df["사용방법"]
    name = df["사업장명"]
    lic = pd.to_datetime(df["인허가일자"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}건 · 칸 {len(df.columns)}개")
    for k, v in df["영업상태명"].value_counts().items():
        p(f"  {k:<10} {v:>6,}  {v/n*100:>5.1f}%")

    p("\n=== 서식이 두 번 묻는다 ===")
    for col, s in [("사용목적", why), ("사용방법", how)]:
        p(f"{col}: 채움 {(s != '').sum():,} ({(s != '').sum()/n*100:.1f}%)"
          f" · 답 {s.nunique():,}가지")
    same = (why != "") & (how != "") & (why == how)
    p(f"두 칸에 같은 말을 적은 곳 {same.sum():,}건 ({same.sum()/n*100:.1f}%)")
    p("  그 값 상위:")
    p("  " + " · ".join(f"{k}({v:,})" for k, v in why[same].value_counts().head(8).items()))
    p(f"둘 다 빈칸 {((why == '') & (how == '')).sum():,}건")

    p("\n=== 한 글자로 채운 칸 ===")
    for col, s in [("사용목적", why), ("사용방법", how)]:
        one = s[(s.str.len() == 1) & (s != "")]
        p(f"{col}: {len(one):,}건 · {one.nunique()}가지")
        p("  " + " · ".join(f"「{k}」 {v:,}" for k, v in one.value_counts().items()))
    p(f"두 칸 모두 「0」 {((why == '0') & (how == '0')).sum():,}건")

    p("\n=== 담당자 메모로 보이는 칸 (개수만) ===")
    memo = how.str.contains(r"연락|퇴사|확인|전화|폐업|함\.|삭제", regex=True)
    num = how.str.contains(r"\d{3}-\d{2}-\d{5}|\d{2,4}-\d{3,4}-\d{4}", regex=True)
    p(f"  {memo.sum():,}건 · 그중 등록번호·전화번호가 섞인 것 {num.sum():,}건")
    p("  ※ 값은 찍지 않는다. 공개 저장소다.")

    p("\n=== 무엇에 쓰나 ===")
    p(f"사용목적 답 {why.nunique():,}가지 중 상위:")
    p(why[why != ""].value_counts().head(15).to_string())
    p("\n낱말로 세면:")
    for w in PURPOSE_WORDS:
        c = why.str.contains(w, regex=False).sum()
        p(f"  {w:<5} {c:>6,}  {c/n*100:>5.1f}%")

    p("\n=== 물고기 ===")
    fish = (why.str.contains("양식|축양|어류|수산", regex=True)
            | how.str.contains("양식|축양|어류|수산", regex=True))
    p(f"양식·축양에 쓴다고 적은 곳 {fish.sum():,}건 ({fish.sum()/n*100:.1f}%)")
    p("  " + " · ".join(f"{k}({v})" for k, v in
                        why[fish & (why != "")].value_counts().head(8).items()))

    p("\n=== 누가 쓰나 ===")
    for lab, pat in [("병원", r"병원"), ("대학·연구소", r"대학|연구|과학기술원"),
                     ("군", r"육군|해군|공군"), ("(주)·주식회사", r"\(주\)|주식회사|㈜")]:
        c = name.str.contains(pat, regex=True).sum()
        p(f"  {lab:<12} {c:>6,}  {c/n*100:>5.1f}%")
    p("가장 자주 나온 이름:")
    p(name[name != ""].value_counts().head(10).to_string())

    p("\n=== 연도별 신고 ===")
    y = lic.dt.year
    vc = y[(y >= 2007) & (y <= 2026)].value_counts().sort_index()
    p(vc.to_string())
    p("※ 2026년은 여덟 달치뿐이다(원본 2026-09-04 내려받음).")

    p("\n=== 수명 ===")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")
    life = ((cl - lic).dt.days / 365.25).dropna()
    life = life[life >= 0]
    p(f"폐업 {len(life):,}건 · 중앙 {life.median():.1f}년 · 최장 {life.max():.1f}년")

    p("\n=== 데이터의 흠 ===")
    cap = pd.to_numeric(df["수용정원수"], errors="coerce")
    use = pd.to_numeric(df["월사용량"], errors="coerce")
    p(f"인허가일자 1990년 이전 {(y < 1990).sum():,}건 "
      f"(가장 이른 값 {int(y.min())}년)")
    p(f"수용정원수 최대 {cap.max():,.0f} · 1만 넘는 곳 {(cap > 10000).sum():,}"
      f" · 0인 곳 {(cap == 0).sum():,}")
    p(f"월사용량 최대 {use.max():,.0f} · 1억 넘는 곳 {(use > 100000000).sum():,}"
      f" · 0인 곳 {(use == 0).sum():,}")
    p("※ 흠이 있는 줄의 사업장 이름은 옮기지 않는다.")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
