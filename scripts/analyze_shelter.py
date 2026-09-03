"""
민방위대피소.csv 에서 제11호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py civil_defense_shelter_info 민방위대피소

사용법:
    python scripts/analyze_shelter.py

※ 조심할 것
   「최대수용인원」이 「시설면적(㎡)」과 거의 항상 같은 숫자다.
   1인당 1㎡ 라는 산정 규칙일 수도 있고 칸을 그대로 복사한 것일 수도 있는데,
   어느 쪽인지는 원본 어디에도 적혀 있지 않다. 단정하지 않는다.
   확실한 것은 면적이 틀리면 인원도 같이 틀린다는 사실뿐이다.
"""
import io
import pathlib

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "민방위대피소.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과_민방위대피소.txt"

WORDS = ["주차장", "아파트", "학교", "센터", "교회", "빌딩", "회관", "상가", "터널"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py civil_defense_shelter_info 민방위대피소` 를 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    cap = pd.to_numeric(df["최대수용인원"], errors="coerce")
    area = pd.to_numeric(df["시설면적(㎡)"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"전체 등록   {n:,}")
    for k, v in df["운영상태"].value_counts().items():
        p(f"  {k:<6} {v:>7,}  {v/n*100:>5.1f}%")
    p(f"해제일자 있는 곳 {(df['해제일자'] != '').sum():,}")

    p("\n=== 수용인원과 면적이 같은 숫자다 ===")
    same = cap.notna() & area.notna() & (cap == area)
    close = cap.notna() & area.notna() & (abs(cap - area) < 1) & ~same
    p(f"완전히 같음   {same.sum():,}  ({same.sum()/n*100:.1f}%)")
    p(f"소수점만 다름 {close.sum():,}")
    p(f"합계          {same.sum()+close.sum():,}  ({(same.sum()+close.sum())/n*100:.1f}%)")
    rest = cap.notna() & area.notna() & (cap > 0) & ~same & ~close
    ratio = (area / cap)[rest]
    p(f"나머지 {rest.sum():,}곳도 면적÷인원 중앙값 {ratio.median():.2f}㎡/명")
    p("※ 1인당 1㎡ 규칙인지 칸을 복사한 것인지는 데이터에 적혀 있지 않다.")

    p("\n=== 그래서 수용인원이 말이 안 된다 ===")
    p(f"최대 {int(cap.max()):,}명 · 중앙 {int(cap.median()):,}명 · 최소 {int(cap.min()):,}명")
    p(f"1만명 이상 {(cap >= 10000).sum():,}곳 · 10만명 이상 {(cap >= 100000).sum():,}곳")
    p("상위 8:")
    for _, x in df.assign(c=cap).nlargest(8, "c").iterrows():
        p(f"  {x['시설명'][:44]:<44} {int(float(x['최대수용인원'])):>9,}명  {x['시설면적(㎡)']}㎡")

    p("\n=== 민방위대피소의 실체 ===")
    name = df["시설명"]
    for w in WORDS:
        c = name.str.contains(w).sum()
        p(f"  {w:<5} {c:>7,}  {c/n*100:>5.1f}%")
    p(f"고유 시설명 {name.nunique():,}가지")
    p("가장 흔한 이름:")
    p(name.value_counts().head(6).to_string())

    p("\n=== 지상에 있는 대피소 ===")
    p(df["시설위치(지상/지하)"].value_counts().to_string())
    up = df[df["시설위치(지상/지하)"] == "지상"]
    p(f"지상 {len(up)}곳의 운영상태: {dict(up['운영상태'].value_counts())}")
    tunnel = up[up["시설명"].str.contains("터널")]
    p(f"그중 터널 {len(tunnel)}곳: {', '.join(tunnel['시설명'].tolist())}")

    p("\n=== 시설구분 ===")
    p(df["시설구분"].value_counts().to_string())

    p("\n=== 지정 연도 ===")
    d = pd.to_datetime(df["지정일자"], errors="coerce")
    yrs = d.dt.year.value_counts().sort_index()
    inrange = yrs[(yrs.index >= 1970) & (yrs.index <= 2026)]
    p(inrange.to_string())
    p(f"최다 {int(inrange.idxmax())}년 {int(inrange.max()):,}곳")

    p("\n=== 데이터의 흠 ===")
    odd = df[(d.dt.year < 1970) | (d.dt.year > 2026)]
    p(f"지정일자가 1970~2026 밖 {len(odd)}건")
    p(odd[["시설명", "지정일자", "운영상태"]].to_string(index=False))

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
