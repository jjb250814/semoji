"""
무료와이파이.csv 에서 제22호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py free_wifi_info 무료와이파이

사용법:
    python scripts/analyze_wifi.py

※ 조심할 것

1. **「표기가 여러 가지」를 제목으로 삼지 않는다.** SSID 에도 대소문자만 다른
   표기가 잔뜩 있지만(Public WiFi Free / Public Wifi Free / public wifi free),
   그건 제21호 「Co., Ltd.」와 같은 이야기다. 이 열람실의 축은 **표기가 아니라
   작명** — 전국 공통 이름을 쓸 것인가, 자기 이름을 지을 것인가다.

2. **공통 이름 계열 판정은 기계적으로 한다.** 소문자로 바꾸고 알파벳만 남겨
   `publicwififree` / `publicwifi` 인 것만 공통 이름으로 센다. 「Public WiFi@Seoul」
   이나 「G_PublicWiFi@SeongNam」은 공통 이름에 지역을 붙인 것이라 자체 브랜드로 센다.
   판정 기준을 본문에 밝힌다.

3. **SSID 는 29.3%가 비어 있다.** 비율은 전부 채워진 66,548곳만 놓고 낸 값이다.

4. **관리기관전화번호 칸이 있다.** 이 저장소는 공개다. 출력에 원문을 찍는 곳은
   전부 mask() 를 거친다. 전화번호는 세지도 찍지도 않는다.

5. **설치장소명·관리기관명은 개별 값을 옮기지 않는다.** 세는 것으로 충분하다.
"""
import io
import sys
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "무료와이파이.csv"
OUT = ROOT / "data" / "분석결과_와이파이.txt"

_MASK = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "(이메일)"),
    (re.compile(r"\d{2,3}-\d{2}-\d{5}"), "(사업자번호)"),
    (re.compile(r"\b0\d{1,2}-\d{3,4}-\d{4}\b"), "(전화번호)"),
]

# 전국 공통 이름으로 볼 값. 소문자 + 알파벳만 남긴 뒤 비교한다.
STD_KEYS = {"publicwififree", "publicwifi"}

# 실제 통신사. 나머지는 관공서 이름이 들어온 것이다.
TELCO = re.compile(r"^(KT|SKT|SKB|LG\s*U\+?|LGU\+|SK브로드밴드|KT\s*텔레캅)$", re.I)

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def mask(t):
    t = str(t)
    for pat, rep in _MASK:
        t = pat.sub(rep, t)
    return t


def norm(s):
    return s.str.lower().str.replace(r"[^a-z]", "", regex=True)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py free_wifi_info 무료와이파이` "
                         f"를 실행하세요.")
    df = pd.read_csv(CSV, dtype=str, keep_default_na=False, low_memory=False)
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    ssid = df["와이파이SSID"]
    got = df[ssid != ""].copy()
    got["std"] = norm(got["와이파이SSID"]).isin(STD_KEYS)

    p("=== 페이지 상단 지표 ===")
    p(f"전체 {n:,}곳")
    p(f"SSID 적힌 곳 {len(got):,} ({100 * len(got) / n:.1f}%) · "
      f"빈칸 {n - len(got):,} ({100 * (n - len(got)) / n:.1f}%)")
    p(f"SSID 고유값 {got['와이파이SSID'].nunique():,}가지")

    p("")
    p("=== 전국 공통 이름을 쓰는가, 자기 이름을 짓는가 ===")
    p("판정: 소문자로 바꾸고 알파벳만 남겨 publicwififree / publicwifi 인 것만 공통 이름.")
    p("「Public WiFi@Seoul」처럼 지역을 붙인 것은 자체 브랜드로 센다.")
    p("")
    std, own = got[got["std"]], got[~got["std"]]
    p(f"공통 이름   {len(std):6,} ({100 * len(std) / len(got):4.1f}%) · 표기 {std['와이파이SSID'].nunique():,}가지")
    p(f"자체 브랜드 {len(own):6,} ({100 * len(own) / len(got):4.1f}%) · 이름 {own['와이파이SSID'].nunique():,}가지")
    p("")
    p("공통 이름을 적은 방식 — 상위 8")
    for v, c in std["와이파이SSID"].value_counts().head(8).items():
        p(f"  {c:6,}  {mask(v)}")
    p("※ 표기가 갈리는 것은 제21호 「Co., Ltd.」와 같은 일이다. 여기서는 곁가지로만 다룬다.")
    p("")
    p("자체 브랜드 — 상위 12")
    top12 = own["와이파이SSID"].value_counts().head(12)
    for v, c in top12.items():
        p(f"  {c:6,}  {mask(v)}")
    p(f"  (페이지에 실은 위 12가지 합계 {top12.sum():,} · "
      f"나머지 {own['와이파이SSID'].nunique() - 12:,}가지 {len(own) - top12.sum():,})")

    p("")
    p("=== 시도별 — 공통 이름을 쓰는 비율 ===")
    g = got.groupby("설치시도명").agg(n=("와이파이SSID", "size"),
                                  std=("std", "mean"),
                                  uniq=("와이파이SSID", "nunique"))
    g = g.sort_values("std")
    p(f"{'시도':14s} {'곳':>7s} {'공통이름':>8s} {'이름 가짓수':>9s}")
    for k, r in g.iterrows():
        p(f"{k:14s} {int(r['n']):7,} {100 * r['std']:7.1f}% {int(r['uniq']):9,}")
    p("")
    p(f"가장 낮은 곳 {g.index[0]} {100 * g['std'].iloc[0]:.1f}% · "
      f"가장 높은 곳 {g.index[-1]} {100 * g['std'].iloc[-1]:.1f}%")

    p("")
    p("=== 「SEOUL」 ===")
    seoul = got[got["와이파이SSID"].str.fullmatch(r"SEOUL")]
    seoul_any = got[got["와이파이SSID"].str.contains(r"SEOUL", case=False)]
    p(f"SSID 가 정확히 「SEOUL」 인 곳 {len(seoul):,}")
    p(f"SSID 에 seoul 이 든 곳 {len(seoul_any):,} · {seoul_any['와이파이SSID'].nunique()}가지")
    sd = got[got["설치시도명"] == "서울특별시"]
    p(f"서울특별시 {len(sd):,}곳 · 공통 이름 {100 * sd['std'].mean():.1f}% · "
      f"이름 {sd['와이파이SSID'].nunique()}가지")

    p("")
    p("=== 통신사를 묻는 칸에 관공서가 들어왔다 ===")
    prov = df["서비스제공사명"]
    pv = prov[prov != ""]
    # 판정 규칙: 한글이 들어 있고 통신사 이름이 아닌 것을 관공서로 본다.
    # 「LG」 「LG U+」처럼 띄어쓰기만 다른 통신사 표기를 관공서로 세지 않기 위해서다.
    has_han = pv.str.contains(r"[가-힣]")
    telco_han = pv.str.contains(r"유플러스|브로드밴드|텔레콤|케이티|엘지")
    gov = has_han & ~telco_han
    p("판정: 한글이 들어 있고 통신사 이름(유플러스·브로드밴드·텔레콤·케이티·엘지)이 아닌 것을 관공서로 본다.")
    p(f"서비스제공사명 고유 {pv.nunique():,}가지 · 채움 {100 * len(pv) / n:.1f}%")
    p(f"통신사 이름 {(~gov).sum():,} ({100 * (~gov).mean():.1f}%) · "
      f"{pv[~gov].nunique():,}가지")
    p(f"관공서 이름 {gov.sum():,} ({100 * gov.mean():.1f}%) · "
      f"{pv[gov].nunique():,}가지")
    p("관공서 이름 — 상위 10")
    for v, c in pv[gov].value_counts().head(10).items():
        p(f"  {c:6,}  {mask(v)}")
    p("통신사 이름을 적은 방식 — 상위 8")
    for v, c in pv[~gov].value_counts().head(8).items():
        p(f"  {c:6,}  {mask(v)}")

    p("")
    p("=== 어디에 놓였나 ===")
    for v, c in df["설치시설구분명"].value_counts().items():
        p(f"  {c:6,} ({100 * c / n:4.1f}%)  {v}")
    p("")
    p(f"설치장소명 고유 {df['설치장소명'].nunique():,}가지 (전체 {n:,}곳)")
    p(f"관리기관명 고유 {df['관리기관명'].nunique():,}가지")

    p("")
    p("=== 데이터에 남은 흠 ===")
    ym = df["설치연월"]
    yy = pd.to_numeric(ym.str[:4], errors="coerce")
    p(f"설치연월 채움 {100 * (ym != '').mean():.1f}% ({(ym != '').sum():,}곳)")
    bad = yy[(yy < 2000) & yy.notna()]
    p(f"2000년보다 이른 값 {len(bad):,}건 · 가장 이른 값 {int(yy.min())}년")
    p("연도별 설치 (채워진 것만)")
    vc = yy[(yy >= 2000)].value_counts().sort_index()
    for y, c in vc.items():
        p(f"  {int(y)}  {c:6,}")
    p("")
    p("※ 설치장소명·관리기관명의 개별 값과 전화번호는 옮기지 않는다.")

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
