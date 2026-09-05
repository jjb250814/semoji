"""
여행업 3종 CSV 에서 제21호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py comprehensive_travel_agencies 종합여행업
    python scripts/fetch.py domestic_international_travel_agencies 국내외여행업
    python scripts/fetch.py domestic_travel_agencies 국내여행업

사용법:
    python scripts/analyze_travel.py

※ 조심할 것

1. **영문상호명 원문을 찍는 자리는 전부 mask() 를 거친다.**
   이 칸에 사업자등록번호를 적어 넣은 곳이 2건 있다. 개수는 세도 되지만
   값은 남기지 않는다. (2026-09-04에 `data/광맥상세.txt` 로 사업자 이메일
   19건이 실제로 사이트에 올라간 적이 있다. 같은 일을 반복하지 않는다.)

2. **채움률 계단을 「업종 차이」로 단정하기 전에 연도를 통제한다.**
   국내여행업은 폐업이 59%라 종합여행업보다 훨씬 늙은 집단이다. 계단이
   업종이 아니라 등록 시기 차이일 수 있다. 그래서 연도 구간별 교차표를
   같이 뽑는다. 여섯 구간 전부에서 계단이 남아야 이야기가 성립한다.

3. **세 업종은 완전히 다른 집단이 아니다.**
   상호와 주소가 같은 곳이 두 업종 이상 허가를 들고 있는 경우가 있다.
   그 비율을 반드시 같이 뽑아 본문에 밝힌다.

4. **「같은 회사가 영문 이름을 여러 가지로 적었다」는 상호만으로 세지 않는다.**
   사업자등록번호는 0.5%만 채워져 있어 쓸 수 없다. 하나여행사처럼 흔한
   이름은 남남일 수 있으므로 **상호 + 주소**가 둘 다 같을 때만 같은 곳으로
   본다. 상호만으로 세면 422곳이 되지만 그 숫자는 믿을 수 없다.

5. **비워둔 것을 게으름으로 읽지 않는다.** 영문 이름이 필요 없는 업체가
   비워두는 것은 합리적이다. 원본에 이유는 없다.
"""
import io
import sys
import pathlib
import re
from collections import Counter

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "분석결과_여행업.txt"

TIERS = [
    ("종합여행업", "종합여행업.csv", "comprehensive_travel_agencies"),
    ("국내외여행업", "국내외여행업.csv", "domestic_international_travel_agencies"),
    ("국내여행업", "국내여행업.csv", "domestic_travel_agencies"),
]

YEAR_BANDS = [(1990, 1999), (2000, 2004), (2005, 2009),
              (2010, 2014), (2015, 2019), (2020, 2026)]

# 법인격 꼬리표. 「Co., Ltd.」 하나를 몇 가지로 적었는지 세는 데 쓴다.
TAIL = re.compile(
    r"(?:^|[\s,.\(])((?:CO|CORP|INC|LTD|LLC)[\s,.\)]*(?:LTD|INC)?[\s,.\)]*)$",
    re.IGNORECASE)

WORDS = ["TOUR", "TOURS", "TRAVEL", "TRIP", "TOURISM",
         "AIR", "HOLIDAY", "KOREA", "SERVICE", "AGENCY"]

# travel/index.html 의 SPELL 배열과 같은 순서·같은 목록이어야 한다.
# 여기서 「나머지 N가지 M건」을 계산하므로 한쪽만 고치면 페이지 숫자가 틀어진다.
PAGE_SPELL = ["Co., Ltd.", "Co.,Ltd.", "CO.,LTD", "Co., Ltd", "Inc.", "Co.,Ltd",
              "CO., LTD", "CO., LTD.", "CO.LTD", "CO.,LTD.", "Co. Ltd",
              "CO., Ltd.", "Co.Ltd", "CO. LTD", "CO.LTD.", "CO,.LTD"]

_MASK = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "(이메일)"),
    (re.compile(r"\d{2,3}-\d{2}-\d{5}"), "(사업자번호)"),
    (re.compile(r"\d{2,4}-\d{3,4}-\d{4}"), "(전화번호)"),
]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def mask(t):
    """원문을 찍는 자리는 전부 이걸 거친다."""
    t = str(t)
    for pat, rep in _MASK:
        t = pat.sub(rep, t)
    return t


def load():
    frames = []
    for label, fname, slug in TIERS:
        path = ROOT / "data" / fname
        if not path.exists():
            raise SystemExit(f"{path} 가 없습니다. 먼저 "
                             f"`python scripts/fetch.py {slug} {label}` "
                             f"를 실행하세요.")
        d = pd.read_csv(path, dtype=str, keep_default_na=False,
                        on_bad_lines="skip", engine="python")
        for c in d.columns:
            d[c] = d[c].str.strip()
        d["업종"] = label
        # 영문 이름 안에 줄바꿈이 든 값이 있다. 한 줄로 눌러 센다.
        d["영문"] = d["영문상호명"].str.replace(r"\s+", " ", regex=True).str.strip()
        d["연도"] = pd.to_numeric(d["인허가일자"].str[:4], errors="coerce")
        d["주소"] = d["도로명주소"].where(d["도로명주소"] != "", d["지번주소"])
        frames.append(d)
    return frames


def main():
    frames = load()
    df = pd.concat(frames, ignore_index=True)
    filled = df[df["영문"] != ""]

    p("=== 페이지 상단 지표 ===")
    p(f"데이터셋 3개 · 전체 {len(df):,}행")
    for label, _, _ in TIERS:
        d = df[df["업종"] == label]
        p(f"  {label} {len(d):,}행")
    p(f"영문상호명을 적은 곳 {len(filled):,} ({100 * len(filled) / len(df):.1f}%)")
    p(f"비워둔 곳 {len(df) - len(filled):,} "
      f"({100 * (len(df) - len(filled)) / len(df):.1f}%)")
    p(f"영문 이름 고유값 {filled['영문'].nunique():,}가지")

    p("")
    p("=== 계단 — 업종별 영문상호명 채움률 ===")
    for label, _, _ in TIERS:
        d = df[df["업종"] == label]
        f = (d["영문"] != "").sum()
        p(f"{label:8s} {f:6,} / {len(d):6,} = {100 * f / len(d):5.1f}%")

    p("")
    p("=== 계단이 나이 탓인지 검증 — 등록 연도를 통제한다 ===")
    p("국내여행업은 폐업이 많아 늙은 집단이다. 연도를 갈라도 계단이 남아야 한다.")
    p("")
    for label, _, _ in TIERS:
        d = df[df["업종"] == label]
        dead = (d["영업상태명"] == "폐업").sum()
        p(f"{label:8s} 등록 중앙값 {int(d['연도'].median())}년 · "
          f"폐업 {100 * dead / len(d):4.1f}% · "
          f"영업중 {100 * (d['영업상태명'] == '영업/정상').mean():4.1f}%")
    p("")
    p(f"{'등록 연도':10s} " + " ".join(f"{l[:4]:>14s}" for l, _, _ in TIERS))
    for lo, hi in YEAR_BANDS:
        row = f"{lo}-{hi}  "
        for label, _, _ in TIERS:
            d = df[(df["업종"] == label) & df["연도"].between(lo, hi)]
            row += (f"{100 * (d['영문'] != '').mean():8.1f}% ({len(d):5,})"
                    if len(d) > 50 else f"{'-':>14s}")
        p(row)
    p("")
    p("영업 중인 것만 (죽은 기록을 빼면)")
    for label, _, _ in TIERS:
        d = df[(df["업종"] == label) & (df["영업상태명"] == "영업/정상")]
        p(f"  {label:8s} {100 * (d['영문'] != '').mean():5.1f}%  (n={len(d):,})")

    p("")
    p("=== 세 업종은 완전히 다른 집단이 아니다 (본문에 밝힐 것) ===")
    both = df[(df["사업장명"] != "") & (df["주소"] != "")].copy()
    both["키"] = (both["사업장명"].str.replace(r"\s", "", regex=True) + "|"
                 + both["주소"].str.replace(r"\s", "", regex=True))
    tiers_per = both.groupby("키")["업종"].nunique()
    p(f"상호+주소로 묶으면 {len(tiers_per):,}곳 · "
      f"두 업종 이상 허가를 든 곳 {(tiers_per > 1).sum():,} "
      f"({100 * (tiers_per > 1).mean():.1f}%)")

    p("")
    p("=== 「Co., Ltd.」 를 몇 가지로 적었나 ===")
    tails = Counter()
    for v in filled["영문"]:
        m = TAIL.search(v)
        if m:
            tails[m.group(1).strip()] += 1
    p(f"법인격 꼬리표가 붙은 것 {sum(tails.values()):,}건 · "
      f"표기 {len(tails):,}가지")
    p("※ 이 151가지에는 Inc. · Corp. 처럼 다른 법인격도 섞여 있다.")
    # CO 와 LTD 가 둘 다 든 것만 = 같은 말을 다르게 적은 것
    coltd = {t: c for t, c in tails.items()
             if re.search(r"CO", t, re.I) and re.search(r"LTD", t, re.I)}
    p(f"그중 CO 와 LTD 가 둘 다 든 것 — 즉 똑같은 말을 다르게 적은 것 "
      f"{sum(coltd.values()):,}건 · {len(coltd):,}가지")
    p("")
    for t, c in tails.most_common(20):
        star = " ←CO+LTD" if t in coltd else ""
        p(f"  {c:5,}  「{mask(t)}」{star}")
    # 페이지(travel/index.html)가 싣는 목록. 기계로 상위 16개를 자르면 안 된다 —
    # 59건이 「INC.」와 「CO.LTD.」 둘이라 순서가 흔들리고, 「INC.」는 다른 법인격이라
    # 이 절의 요점(같은 말을 다르게 적었다)에 맞지 않아 일부러 뺐다.
    shown = sum(tails[t] for t in PAGE_SPELL)
    p("")
    p(f"페이지에 실은 {len(PAGE_SPELL)}가지 합계 {shown:,}건 · "
      f"나머지 {len(tails) - len(PAGE_SPELL):,}가지 {sum(tails.values()) - shown:,}건")
    missing = [t for t in PAGE_SPELL if t not in tails]
    if missing:
        p(f"!! 페이지에 있는데 데이터에 없는 표기: {missing}")

    p("")
    p("=== 낱말 ===")
    up = filled["영문"].str.upper()
    for w in WORDS:
        c = up.str.contains(rf"\b{w}\b", regex=True).sum()
        p(f"  {w:9s} {c:5,} ({100 * c / len(filled):4.1f}%)")

    p("")
    p("=== 표기 습관 ===")
    caps = filled[filled["영문"].str.match(r"^[^a-z]*$")
                  & filled["영문"].str.contains(r"[A-Z]")]
    lows = filled[filled["영문"].str.match(r"^[^A-Z]*$")
                  & filled["영문"].str.contains(r"[a-z]")]
    L = filled["영문"].str.len()
    p(f"대문자만 {len(caps):,} ({100 * len(caps) / len(filled):.1f}%) · "
      f"소문자만 {len(lows):,} ({100 * len(lows) / len(filled):.1f}%)")
    p(f"길이 평균 {L.mean():.1f}자 · 중앙값 {int(L.median())}자 · 최장 {L.max()}자")
    longest = filled.loc[L.idxmax(), "영문"]
    p(f"가장 긴 것 {len(longest)}자 — {mask(longest)}")

    p("")
    p("=== 영문 이름 칸에 영문이 아닌 것을 적은 곳 ===")
    num = filled[filled["영문"].str.match(r"^[\d\s.\-]+$")]
    one = filled[filled["영문"].str.len() == 1]
    han = filled[filled["영문"].str.contains(r"[가-힣]")]
    p(f"숫자만 적은 곳 {len(num):,}건 · 종류 {num['영문'].nunique()}가지")
    p(f"  값: {', '.join('「' + mask(x) + '」' for x in sorted(num['영문'].unique())[:16])}")
    p(f"  ※ 사업자등록번호꼴 열 자리가 2건 섞여 있다. 마스킹해서 찍는다.")
    p(f"한 글자만 적은 곳 {len(one):,}건 · "
      f"{', '.join('「' + x + '」' for x in sorted(one['영문'].unique()))}")
    p(f"한글이 섞인 곳 {len(han):,}건")

    p("")
    p("=== 영문 이름과 영문 주소는 짝으로 움직인다 ===")
    ea = df["영문상호주소"]
    p(f"영문상호주소 채움 {(ea != '').sum():,} "
      f"({100 * (ea != '').mean():.1f}%)")
    p(f"영문 이름을 적은 곳 중 영문 주소도 적은 비율 "
      f"{100 * (filled['영문상호주소'] != '').mean():.1f}%")
    p(f"영문 이름을 비운 곳 중 영문 주소는 적은 곳 "
      f"{(df.loc[df['영문'] == '', '영문상호주소'] != '').sum():,}건")

    p("")
    p("=== 같은 곳이 두 번 적었는데 두 번이 안 맞는다 ===")
    p("사업자등록번호는 0.5%만 채워져 못 쓴다. 상호+주소가 둘 다 같을 때만 같은 곳으로 본다.")
    key = filled[(filled["사업장명"] != "") & (filled["주소"] != "")].copy()
    key["키"] = (key["사업장명"].str.replace(r"\s", "", regex=True) + "|"
                + key["주소"].str.replace(r"\s", "", regex=True))
    g = key.groupby("키")["영문"].nunique()
    p(f"대조 가능한 {len(g):,}곳 중 영문 이름이 2가지 이상인 곳 "
      f"{(g > 1).sum():,} ({100 * (g > 1).mean():.1f}%) · 최다 {g.max()}가지")
    p("(상호만으로 세면 422곳이 되지만 남남이 섞이므로 쓰지 않는다)")
    p("")
    p("차이가 무엇인지 — 위에서 다섯 곳")
    for k in g[g > 1].sort_values(ascending=False).head(5).index:
        r = key[key["키"] == k]
        p(f"  {r['사업장명'].iloc[0]}  [{'·'.join(sorted(r['업종'].unique()))}]")
        for x in sorted(r["영문"].unique()):
            p(f"      {mask(x)}")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    # 윈도 콘솔이 cp949 라 「—」 에서 죽는다. 파일은 UTF-8 로 남기고 화면만 눌러 찍는다.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
