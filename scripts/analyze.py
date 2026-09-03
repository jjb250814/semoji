"""
모범음식점정보.csv 에서 페이지에 쓴 숫자를 다시 계산한다.

index.html 과 cancelled.html 에 하드코딩된 값이 원본과 맞는지 확인하는 용도.
데이터가 갱신되면(수시 갱신) 이 스크립트를 다시 돌려 값을 바꿔 넣으면 된다.

사용법
    python scripts/analyze.py
"""
import io
import pathlib
import re

import pandas as pd

CSV = pathlib.Path(__file__).resolve().parent.parent / "data" / "모범음식점정보.csv"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "분석결과.txt"

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def classify(reason):
    """자유 입력 사유를 낱말 기준으로 묶는다. cancelled.html 의 분류 차트와 같은 규칙."""
    if not reason:
        return "(사유 없음)"
    if re.search("승계|명의|양도|변경", reason):
        return "주인이 바뀜"
    if re.search("폐업|폐문|멸실|영업소폐쇄|휴업|대장정리|자료정비|직권", reason):
        return "가게가 사라짐"
    if re.search("행정처분|위반|적발|과태료", reason):
        return "행정처분"
    if re.search("미달|부적합|탈락|점수|등급|미흡", reason):
        return "재심사 탈락"
    if re.search("자진|반납|희망|원함|요청|포기|사퇴|의사 없음|안함|않음", reason):
        return "본인이 그만둠"
    return "기타"


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 scripts/fetch.py 를 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()

    cancelled = df["지정취소일자"] != ""
    alive = (df["영업상태명"] == "영업") & (~cancelled)
    reasons = df.loc[df["지정취소사유"] != "", "지정취소사유"]
    vc = reasons.value_counts()

    p("=== 페이지 상단 지표 ===")
    p(f"누적 지정      {len(df):,}")
    p(f"지정 취소      {cancelled.sum():,}  ({cancelled.sum()/len(df)*100:.1f}%)")
    p(f"현재 유지      {alive.sum():,}")
    p(f"서로 다른 사유 {reasons.nunique():,}  (1회만 등장 {(vc == 1).sum():,})")

    p("\n=== 취소 사유 분류 ===")
    cats = df.loc[cancelled, "지정취소사유"].map(classify).value_counts()
    for name, n in cats.items():
        p(f"{name:<12} {n:>6,}  {n/cats.sum()*100:>5.1f}%")

    p("\n=== 85점의 벽 ===")
    sc = reasons.str.extract(r"(\d{2,3})\s*점")[0].dropna().astype(int)
    sc = sc[(sc >= 1) & (sc <= 100)]
    p(f"점수가 적힌 사유 {len(sc):,}건 · 최저 {sc.min()}점 · 최고 {sc.max()}점")

    p("\n=== 연도별 신규 지정 ===")
    yr = df["지정일자"].str[:4]
    p(yr[yr.str.match(r"(19|20)\d\d")].value_counts().sort_index().to_string())

    p("\n=== 현역 최장수 10곳 ===")
    live = df[alive & df["지정일자"].str.match(r"(19|20)\d\d-")]
    p(live.sort_values("지정일자")[["업소명", "지정일자", "도로명주소", "주된음식종류"]]
        .head(10).to_string(index=False))

    p("\n=== 랜딩에 쓴 값 ===")
    nm = df["업소명"]
    sido = df["도로명주소"].str.split().str[0]
    p(f"세종 전체 {(sido == '세종특별자치시').sum()} / 세종 현역 {((sido == '세종특별자치시') & alive).sum()}")
    for kw in ["가든", "할매", "할머니", "엄마", "원조", "본가"]:
        p(f"'{kw}' 들어간 업소명 {nm.str.contains(kw).sum():,}곳")
    p(f"이름이 겹치는 가게 {len(nm) - nm.nunique():,}곳 · 최다 상호 {nm.value_counts().index[0]} ({nm.value_counts().iloc[0]}곳)")
    p(f"한 글자 업소명 {(nm.str.len() == 1).sum()}곳")
    p(f"가장 긴 업소명 {max(len(v) for v in nm)}자 · {max(nm, key=len)}")
    p(f"주된음식종류 표기 {df['주된음식종류'].nunique():,}가지")
    p(f"전화번호 빈칸 전체 {(df['전화번호'] == '').sum():,}곳 / 현역 {(df.loc[alive, '전화번호'] == '').sum():,}곳")

    p("\n=== 데이터의 흠 ===")
    odd = df[~df["지정일자"].str.match(r"(19[89]\d|20[0-2]\d)-")]
    p(f"1980~2029 밖 지정일자 {len(odd)}건")
    p(odd[["업소명", "지정일자"]].to_string(index=False))
    d0409 = df["지정일자"] == "1987-04-09"
    p(f"1987-04-09 지정 {d0409.sum()}곳 중 주된음식종류 '팔보채' "
      f"{(d0409 & (df['주된음식종류'] == '팔보채')).sum()}곳")
    p("메뉴 칸에 숫자만: " + ", ".join(df.loc[df["주된음식종류"].str.match(r"^\d+$"), "주된음식종류"]))

    p("\n=== 부활 ===")
    revived = df[cancelled & (df["영업상태명"] == "영업") & (df["재지정일자"] > df["지정취소일자"])]
    p(f"취소됐다가 재지정받고 지금도 영업 중 {len(revived):,}곳")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
