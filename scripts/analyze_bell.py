"""
안전비상벨.csv 에서 bell.html(제9호)에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py emergency_call_box_info 안전비상벨

사용법:
    python scripts/analyze_bell.py

※ 다루지 않기로 한 칸이 있다.
   「연계방식」(양방향/단방향/미연계)과 「경찰연계유무」는 이 데이터셋에서 가장
   눈길을 끄는 숫자지만, 각 값이 정확히 무엇을 뜻하는지 원본 어디에도 적혀 있지 않다.
   뜻을 모른 채 쓰면 "비상벨이 작동하지 않는다"는 인상을 주게 되고,
   그것이 틀렸을 경우의 피해가 잡학의 재미보다 훨씬 크다.
   그래서 페이지에서 뺐다. 아래 참고 항목에서 분포만 출력한다.
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "안전비상벨.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_안전비상벨.txt"

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py emergency_call_box_info 안전비상벨` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)

    p("=== 페이지 상단 지표 ===")
    p(f"전체 등록  {n:,}")
    purpose = df["설치목적"].value_counts()
    for k, v in purpose.items():
        p(f"  {k:<6} {v:>7,}  {v/n*100:>5.1f}%")

    p("\n=== 설치장소유형 ===")
    place = df["설치장소유형"].value_counts()
    for k, v in place.items():
        p(f"  {k:<5} {v:>7,}  {v/n*100:>5.1f}%")

    p("\n=== 「약자보호」 4,625개는 어디에 ===")
    weak = df[df["설치목적"] == "약자보호"]
    wp = weak["설치장소유형"].value_counts()
    for k, v in wp.items():
        p(f"  {k:<5} {v:>6,}  {v/len(weak)*100:>5.1f}%")

    p("\n=== 같은 화장실, 다른 목적 ===")
    toilet = df[df["설치장소유형"] == "화장실"]
    p(f"화장실 비상벨 {len(toilet):,}개")
    for k, v in toilet["설치목적"].value_counts().items():
        p(f"  {k:<6} {v:>6,}  {v/len(toilet)*100:>5.1f}%")
    p("※ 같은 화장실 벨인데 무엇을 기준으로 갈렸는지는 데이터에 없다.")

    # 한 기관이 관리하는 화장실 벨끼리도 목적이 갈리는가
    by_org = toilet.groupby("관리기관명")["설치목적"].agg(["nunique", "count"])
    multi = by_org[(by_org["nunique"] > 1)]
    p(f"\n화장실 벨을 등록한 기관 {len(by_org):,}곳 중 "
      f"{len(multi):,}곳은 자기가 관리하는 화장실 벨에 서로 다른 목적을 적었다.")
    p("가장 여러 목적이 섞인 기관:")
    p(multi.sort_values("count", ascending=False).head(6).to_string())

    p("\n=== 데이터의 흠 — 설치연도 ===")
    yr_all = df["안전비상벨설치연도"]
    blank = (yr_all == "").sum()
    odd = df[(yr_all != "") & (~yr_all.str.match(r"^20(0[4-9]|1\d|2[0-6])$"))]
    p(f"연도 칸이 빈 곳 {blank}개")
    p(f"2004~2026 밖 {len(odd)}개")
    p(odd[["안전비상벨설치연도", "설치장소유형", "관리기관명"]].to_string(index=False))

    p("\n=== 「기타」를 고른 21,754개는 어디라고 적었나 ===")
    other = df[df["설치장소유형"] == "기타"]
    p(f"설치장소유형이 '기타'인 곳 {len(other):,} ({len(other)/n*100:.1f}%)")
    p(other["설치위치"].value_counts().head(10).to_string())

    p("\n=== 설치위치 자유입력 ===")
    loc = df["설치위치"]
    p(f"고유 표현 {loc.nunique():,}가지 / 전체 {n:,}")
    p(loc.value_counts().head(12).to_string())

    p("\n=== 설치연도 ===")
    yr = df["안전비상벨설치연도"]
    yr = yr[yr.str.match(r"(19|20)\d\d")]
    counts = yr.value_counts().sort_index()
    p(counts.to_string())
    p(f"최다 {counts.idxmax()}년 {counts.max():,}개")

    p("\n=== 데이터의 흠 — 부가기능 표기 ===")
    fx = df["부가기능"]
    fx = fx[fx != ""]
    normalized = fx.str.replace(r"\s+", "", regex=True)
    p(f"기재 {len(fx):,} ({len(fx)/n*100:.1f}%) · 표기 {fx.nunique()}가지")
    p(f"공백만 지우면 {normalized.nunique()}가지 — {fx.nunique()-normalized.nunique()}가지가 띄어쓰기 차이였다")
    grouped = fx.groupby(normalized).agg(lambda s: sorted(set(s)))
    for key, variants in grouped.items():
        if len(variants) > 1:
            p(f"  {key}  ←  {variants}")

    p("\n=== 관리기관 ===")
    p(f"고유 {df['관리기관명'].nunique():,}곳")
    p(df["관리기관명"].value_counts().head(6).to_string())

    p("\n=== 참고 — 페이지에 쓰지 않은 칸 ===")
    p("아래 세 칸은 뜻이 원본에 정의돼 있지 않아 페이지에서 뺐다. 위 주석 참고.")
    for c in ["연계방식", "경찰연계유무", "최종점검결과구분"]:
        p(f"[{c}] {dict(df[c].value_counts())}")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
