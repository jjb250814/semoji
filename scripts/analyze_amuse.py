"""
기타유원시설.csv 에서 제23호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py general_amusement_facilities 기타유원시설

사용법:
    python scripts/analyze_amuse.py

※ 조심할 것

1. **「신고테마파크업」 한 곳의 상호를 옮기지 않는다.** 전국에 하나뿐이라
   업종만 적어도 사실상 특정된다. 인허가 연도와 상태까지만 쓴다.
   (이미 등록취소된 곳이라 더더욱 실명으로 부를 이유가 없다.)

2. **낱말을 셀 때 서식 낱말을 기구 이름으로 세지 않는다.**
   「안전성검사」 「대상」 「유기기구」 「비대상」은 담당자가 붙인 분류어이지
   놀이기구 이름이 아니다. STOP 에 넣어 뺀다. 이걸 안 빼면 「대상」이
   1위가 되어 이야기가 통째로 틀어진다.

3. **비율의 분모는 채워진 1,309곳이다.** 놀이기구수내역은 25.3%가 비어 있다.

4. **1,752행짜리 작은 데이터셋이다.** 낱말 빈도의 절대수가 작으니
   「가장 많다」를 세게 쓰지 않는다.
"""
import io
import sys
import pathlib
import re
from collections import Counter

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "기타유원시설.csv"
OUT = ROOT / "data" / "분석결과_유원시설.txt"

# 담당자가 붙인 분류어. 놀이기구 이름이 아니다.
STOP = {"안전성검사", "안전성", "안전검사", "확인검사", "확인검사대상", "안전성검사대상",
        "대상", "비대상", "유기기구", "기구", "이동식", "고정식", "추가", "설치",
        "검사", "비검사", "검사대상", "비검사대상", "종류", "이상", "없음", "해당",
        "기타", "외", "및", "등", "대상유기기구", "비대상유기기구",
        "아닌", "대상이", "유기시설", "안전검사대상", "인승", "시설", "포함",
        "이용", "운영", "구분", "총계", "합계", "또는", "그리고"}

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py general_amusement_facilities 기타유원시설` "
                         f"를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False, low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    col = df["놀이기구수내역"]
    got = col[col != ""]

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳")
    p(f"「놀이기구수내역」 적힌 곳 {len(got):,} ({100 * len(got) / n:.1f}%) · "
      f"빈칸 {n - len(got):,} ({100 * (n - len(got)) / n:.1f}%)")
    p(f"고유값 {got.nunique():,}가지")

    p("")
    p("=== 개수를 묻는 칸에 무엇을 적었나 ===")
    p("분모는 채워진 %s곳이다." % f"{len(got):,}")
    num = got.str.fullmatch(r"[\d\s,.]+")
    kind = got.str.fullmatch(r"\d+\s*종")
    name = got.str.contains(r"[가-힣]") & ~kind
    p(f"숫자만 적은 곳        {num.sum():5,} ({100 * num.mean():5.1f}%)")
    p(f"「N종」이라고만 적은 곳 {kind.sum():5,} ({100 * kind.mean():5.1f}%)")
    p(f"기구 이름을 적은 곳    {name.sum():5,} ({100 * name.mean():5.1f}%)")
    p("")
    L = got.str.len()
    p(f"길이 평균 {L.mean():.1f}자 · 중앙값 {int(L.median())}자 · 최장 {L.max()}자")
    p(f"가장 긴 것 {L.max()}자 — {got.loc[L.idxmax()]}")

    p("")
    p("=== 손으로 적은 놀이기구 이름 ===")
    p("서식 낱말(안전성검사·대상·유기기구…)은 STOP 으로 뺐다. 기구 이름만 센다.")
    cnt = Counter()
    for v in got[name]:
        for w in re.findall(r"[가-힣A-Za-z]{2,}", v):
            if w not in STOP:
                cnt[w] += 1
    p("")
    for w, c in cnt.most_common(24):
        p(f"  {c:4,}  {w}")
    p("")
    p(f"이름 낱말 종류 {len(cnt):,}가지")

    p("")
    p("=== 전국에 한 곳뿐인 업종 ===")
    vc = df["문화체육업종명"].value_counts()
    for v, c in vc.items():
        p(f"  {c:5,}  {v}")
    only = df[df["문화체육업종명"] == "신고테마파크업"]
    if len(only) == 1:
        r = only.iloc[0]
        p("")
        p(f"「신고테마파크업」 한 곳 — 인허가 {r['인허가일자']} · "
          f"{r['영업상태명']} ({r['상세영업상태명']})")
        p(f"  놀이기구수내역: {r['놀이기구수내역']}")
        p("  ※ 상호는 옮기지 않는다. 전국에 하나뿐이라 이름을 적으면 특정된다.")

    p("")
    p("=== 살아 있나 ===")
    for v, c in df["영업상태명"].value_counts().items():
        p(f"  {c:5,} ({100 * c / n:4.1f}%)  {v}")
    lic = pd.to_numeric(df["인허가일자"].str[:4], errors="coerce")
    p("")
    p(f"가장 이른 인허가 {int(lic.min())}년 · 가장 늦은 인허가 {int(lic.max())}년")

    p("")
    p("=== 있는지 없는지만 묻는 칸들 ===")
    p("채움률이 낮은데, 채워진 것은 거의 다 Y다.")
    for c in ["안내소유무", "의무실유무", "발전시설유무", "방송시설유무"]:
        s = df[c]
        f = s[s != ""]
        if len(f):
            y = (f == "Y").sum()
            p(f"  {c:8s} 채움 {100 * len(f) / n:5.1f}% ({len(f):,}) · "
              f"그중 Y {100 * y / len(f):5.1f}% ({y:,}) · N {len(f) - y:,}")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
