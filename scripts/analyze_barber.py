"""
이용원.csv 에서 제12호 열람실에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py barber_shops 이용원

사용법:
    python scripts/analyze_barber.py

※ 조심할 것

1. 「침대수」 칸을 다룰 때 상호를 붙이지 않는다.
   이발소에 침대가 있다는 사실을 특정 가게 이름과 함께 띄우면, 이 업종에 붙어 있는
   오래된 혐의를 그 가게에 씌우는 일이 된다. 공개 데이터라도 하지 않는다.
   **왜 서식이 침대 수를 묻는지도 데이터 어디에도 적혀 있지 않다. 추측하지 않는다.**
   확실한 것은 칸이 있었고 답이 거의 전부 0이었다는 사실뿐이다.

2. 「바바」로 이름을 잡으면 안 된다.
   「바바리안」 「바바라헤어」 처럼 관계없는 상호가 딸려온다. `바버|barber` 로만 잡는다.

3. 2026년은 여덟 달치뿐이다.
   원본을 2026-09-03에 받았다. 연도별 표에서 2026을 다른 해와 나란히 놓고
   "줄었다" 고 말하면 틀린다.
"""
import io
import pathlib
import re

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "이용원.csv"
OUT = ROOT / "data" / "분석결과_이용원.txt"

# 앞에서 잡힌 곳은 뒤에서 다시 세지 않는다. 순서가 곧 우선순위다.
GROUPS = [
    ("바버샵", r"바버|barber"),
    ("이발관", r"이발관"),
    ("이발소", r"이발소"),
    ("이용원", r"이용원"),
    ("이용소", r"이용소"),
    ("이용실", r"이용실"),
]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def split_names(name):
    """겹치지 않는 이름 무리로 가른다. 어디에도 안 걸리면 '그 외'."""
    taken = pd.Series(False, index=name.index)
    out = {}
    for label, pat in GROUPS:
        m = name.str.contains(pat, case=False, regex=True) & ~taken
        taken |= m
        out[label] = m
    out["그 외"] = ~taken
    return out


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py barber_shops 이용원` 를 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", engine="python")
    for c in df.columns:
        df[c] = df[c].str.strip()
    n = len(df)
    name = df["사업장명"]
    d = pd.to_datetime(df["인허가일자"], errors="coerce")
    yr = d.dt.year.where((d.dt.year >= 1960) & (d.dt.year <= 2026))
    groups = split_names(name)

    p("=== 페이지 상단 지표 ===")
    p(f"전체 등록   {n:,}")
    for k, v in df["영업상태명"].value_counts().items():
        p(f"  {k:<10} {v:>7,}  {v/n*100:>5.1f}%")

    p("\n=== 서류가 부르는 이름은 하나다 ===")
    for col in ["업태구분명", "위생업태명"]:
        vc = df[col].value_counts()
        top = vc.index[0] if vc.index[0] else vc.index[1]
        p(f"{col}: " + " · ".join(f"{k or '(빈칸)'} {v:,}" for k, v in vc.items()))
        p(f"  가장 많은 값 「{top}」 {vc[top]:,}곳 = {vc[top]/n*100:.1f}%")

    p("\n=== 간판이 부르는 이름은 여섯 가지다 ===")
    p(f"{'이름':<7}{'곳수':>8}{'비중':>7}{'중앙연도':>8}{'최초':>6}{'영업중':>8}")
    for label, m in groups.items():
        y = yr[m].dropna()
        med = f"{y.median():.0f}" if len(y) else "-"
        mn = f"{y.min():.0f}" if len(y) else "-"
        alive = (df.loc[m, "영업상태명"] == "영업/정상").sum()
        p(f"{label:<7}{m.sum():>8,}{m.sum()/n*100:>6.1f}%{med:>8}{mn:>6}{alive:>8,}")

    p("\n=== 새로 여는 가게가 고르는 이름 (시기별 비중) ===")
    PER = [("1990~1999", 1990, 1999), ("2000~2009", 2000, 2009),
           ("2010~2019", 2010, 2019), ("2021~2026", 2021, 2026)]
    p(f"{'시기':<12}{'신규':>8}" + "".join(f"{l:>9}" for l, _ in GROUPS) + f"{'그 외':>9}")
    for label, a, b in PER:
        w = (yr >= a) & (yr <= b)
        tot = w.sum()
        row = "".join(f"{(m & w).sum()/tot*100:>8.1f}%" for m in groups.values())
        p(f"{label:<12}{tot:>8,}{row}")
    p("같은 것을 곳수로:")
    for label, a, b in PER:
        w = (yr >= a) & (yr <= b)
        c = (groups["바버샵"] & w).sum()
        p(f"  {label}  신규 {w.sum():,}곳 중 바버샵 {c:,}곳"
          f"  ·  이발관 {(groups['이발관'] & w).sum():,}곳")
    p("※ 2026년은 여덟 달치뿐이다 (원본 2026-09-03 내려받음).")

    p("\n=== 「바버샵」이 나타난 해 ===")
    bb = groups["바버샵"]
    vc = yr[bb].value_counts().sort_index()
    p(f"가장 이른 등록 {vc.index[0]:.0f}년 (그 뒤 오래 끊긴다)")
    p("2013년부터:")
    for y, c in vc[vc.index >= 2013].items():
        tot = (yr == y).sum()
        p(f"  {y:.0f}  {c:>4,}곳   그해 신규의 {c/tot*100:>4.1f}%")

    p("\n=== 연도별 전체 신규 등록 ===")
    allv = yr.value_counts().sort_index()
    p(allv[allv.index >= 1990].to_string())

    p("\n=== 서식이 묻는 두 가지: 의자와 침대 ===")
    for col in ["의자수", "침대수"]:
        v = pd.to_numeric(df[col], errors="coerce")
        filled = (df[col] != "").sum()
        p(f"{col}: 채운 곳 {filled:,} ({filled/n*100:.1f}%)")
        p(f"  0 이라고 적음 {(v == 0).sum():,}"
          f"  ·  1 이상 {(v > 0).sum():,}"
          f"  ·  적힌 가장 큰 값 {v.max():.0f}")
        p(f"  많이 적힌 답: "
          + " · ".join(f"{k}({c:,})" for k, c in df[df[col] != ""][col]
                       .value_counts().head(6).items()))
    ch = pd.to_numeric(df["의자수"], errors="coerce")
    bd = pd.to_numeric(df["침대수"], errors="coerce")
    p(f"둘 다 채운 곳 {((df['의자수'] != '') & (df['침대수'] != '')).sum():,}")
    p(f"  의자>0 · 침대=0  {((ch > 0) & (bd == 0)).sum():,}")
    p(f"  의자>0 · 침대>0  {((ch > 0) & (bd > 0)).sum():,}")
    p(f"의자수 중앙값 {ch[ch > 0].median():.0f}개"
      f"  ·  2개 {(ch == 2).sum():,}곳  ·  3개 {(ch == 3).sum():,}곳")
    p("※ 왜 이발소에 침대 수를 묻는지는 데이터 어디에도 적혀 있지 않다.")
    p("※ 침대를 적은 곳의 상호는 쓰지 않는다.")

    p("\n=== 수명 ===")
    cl = pd.to_datetime(df["폐업일자"], errors="coerce")
    life = ((cl - d).dt.days / 365.25).dropna()
    life = life[life >= 0]
    p(f"폐업까지 {len(life):,}건 · 중앙값 {life.median():.1f}년 · 평균 {life.mean():.1f}년")
    p(f"가장 길게 적힌 영업 기간 {life.max():.1f}년")
    top = df.assign(L=life).nlargest(1, "L").iloc[0]
    p(f"  그 줄: 인허가 {top['인허가일자']} → 폐업 {top['폐업일자']}"
      f"  (시작 날짜가 틀리면 기간도 같이 틀린다)")
    p(f"  10년 넘게 버틴 곳 {(life >= 10).sum():,} ({(life >= 10).sum()/len(life)*100:.1f}%)")

    p("\n=== 데이터의 흠 ===")
    odd = df[(d.dt.year < 1960) | (d.dt.year > 2026)]
    p(f"인허가일자가 1960~2026 밖 {len(odd)}건")
    p(odd["인허가일자"].value_counts().head(8).to_string())
    p(f"의자수에 적힌 가장 큰 값 {ch.max():.0f}"
      f" (같은 줄 소재지면적 {df.loc[ch.idxmax(), '소재지면적']}㎡)")
    p(f"인허가일자가 비어 있거나 못 읽는 곳 {d.isna().sum():,}")

    text = buf.getvalue()
    OUT.write_text(text, encoding="utf-8")
    print(text)
    print(f"\n저장 → {OUT}")


if __name__ == "__main__":
    main()
