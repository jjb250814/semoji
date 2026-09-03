"""
보호수.csv 에서 tree/index.html 에 쓴 숫자를 다시 계산한다.

먼저 데이터를 받아둘 것:
    python scripts/fetch.py protected_tree_info 보호수

사용법:
    python scripts/analyze_tree.py
"""
import io
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "보호수.csv"
OUT = ROOT / "data" / "분석결과_보호수.txt"

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    if not CSV.exists():
        raise SystemExit(f"{CSV} 가 없습니다. 먼저 "
                         f"`python scripts/fetch.py protected_tree_info 보호수` 을 실행하세요.")

    df = pd.read_csv(CSV, dtype=str, keep_default_na=False,
                     on_bad_lines="skip", low_memory=False)
    df.columns = [c.strip() for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()

    n = len(df)
    # 주소 칸이 시도명 없이 「북지리 151」처럼 적힌 줄이 있다.
    # 그럴 때는 시도명·시군구명 칸을 앞에 붙여 어디인지 알아볼 수 있게 한다.
    addr = df["소재지도로명주소"].where(df["소재지도로명주소"] != "", df["소재지지번주소"])
    need = ~addr.str.startswith(tuple(df["시도명"].unique()))
    addr = addr.mask(need, (df["시도명"] + " " + df["시군구명"] + " " + addr).str.strip())
    age = pd.to_numeric(df["나무나이"], errors="coerce")
    hgt = pd.to_numeric(df["나무높이"], errors="coerce")
    grth = pd.to_numeric(df["가슴높이둘레"], errors="coerce")
    cnt = pd.to_numeric(df["그루수"], errors="coerce")

    p("=== 페이지 상단 지표 ===")
    p(f"등록된 보호수   {n:,}건")
    p(f"그루수 합계     {cnt.sum():,.0f}그루 (한 건이 여러 그루일 수 있다)")
    p(f"나무 나이 중앙값 {age.median():.0f}년")

    # --- 이 페이지의 제목 ---
    p("\n=== 「품격명」 — 서류가 나무에 매기는 등급 ===")
    v = df["품격명"]
    for k, c in v.value_counts().items():
        p(f"  {k or '(빈 칸)':<10}{c:>7,}  {c/n*100:>5.1f}%")
    p(f"적은 곳 {(v!='').sum():,} / {n:,}")

    p("\n=== 「보호수유형명」 ===")
    t = df["보호수유형명"]
    for k, c in t.value_counts().items():
        p(f"  {k or '(빈 칸)':<16}{c:>7,}")
    p("\n같은 뜻인데 순서만 다르게 적은 것:")
    p(f"  「노목+거목」 {(t=='노목+거목').sum():,} · 「거목+노목」 {(t=='거목+노목').sum():,}")

    # --- 나이 ---
    p("\n=== 나무나이 ===")
    p(f"적은 곳 {age.notna().sum():,} ({age.notna().sum()/n*100:.1f}%) · "
      f"중앙값 {age.median():.0f}년 · 최소 {age.min():.0f} · 최대 {age.max():.0f}")
    p("가장 많이 적힌 나이:")
    for k, c in df["나무나이"][df["나무나이"] != ""].value_counts().head(12).items():
        p(f"  {k:>5}년 {c:>5,}그루")
    round100 = age.isin([100, 200, 300, 400, 500, 600, 700, 800]).sum()
    round50 = age.isin([50, 150, 250, 350, 450, 550, 650, 750]).sum()
    p(f"\n100으로 나누어떨어지는 나이 {round100:,} ({round100/n*100:.1f}%)")
    p(f"50으로 끝나는 나이 {round50:,} ({round50/n*100:.1f}%)")
    p(f"둘을 합치면 {round100+round50:,} ({(round100+round50)/n*100:.1f}%)")
    p(f"\n1,000년 이상 {(age>=1000).sum():,} · 500년 이상 {(age>=500).sum():,} · "
      f"100년 미만 {(age<100).sum():,}")
    p("\n가장 나이 많은 10건:")
    for i in age.sort_values(ascending=False).head(10).index:
        p(f"  {df['나무나이'][i]:>5}년  {df['나무종류'][i][:10]:<12}"
          f"{df['품격명'][i]:<8}{addr[i][:38]}")

    # --- 크기 ---
    p("\n=== 나무높이 · 가슴높이둘레 ===")
    p(f"높이 중앙값 {hgt.median():.0f} · 최소 {hgt.min():.0f} · 최대 {hgt.max():.0f}")
    p(f"  20 이상 {(hgt>=20).sum():,} · 100 넘는 값 {(hgt>100).sum():,}")
    p(f"둘레 중앙값 {grth.median():.1f} · 최대 {grth.max():.0f}")
    p(f"  10 미만 {(grth<10).sum():,} · 100 넘는 값 {(grth>100).sum():,}")
    p("  (단위가 섞여 있다. 미터로 적은 곳과 센티미터로 적은 곳이 함께 있다)")

    # --- 종류 ---
    p("\n=== 나무종류 ===")
    kind = df["나무종류"]
    p(f"고유 {kind.nunique():,}가지")
    p(kind.value_counts().head(12).to_string())
    p(f"\n같은 나무를 다르게 적은 것:")
    for a, b in [("느티나무", "느티"), ("왕버들", "왕버들나무"), ("곰솔", "해송")]:
        p(f"  「{a}」 {(kind==a).sum():,} · 「{b}」 {(kind==b).sum():,}")
    latin = kind[kind.str.match(r"^[A-Za-z]")]
    p(f"\n종류 칸에 학명을 적은 곳 {len(latin):,} — "
      + ", ".join(f"{k}({c})" for k, c in latin.value_counts().head(4).items()))
    listed = kind[kind.str.contains(r"[,/]", regex=True)]
    p(f"종류 칸에 여러 나무를 늘어놓은 곳 {len(listed):,}")
    for s in listed.value_counts().index[:6]:
        p(f"   {s}")

    # --- 주인 ---
    p("\n=== 소유자구분 ===")
    o = df["소유자구분"]
    p(f"적은 곳 {(o!='').sum():,} ({(o!='').sum()/n*100:.1f}%) · "
      f"비워 둔 곳 {(o=='').sum():,}")
    for k, c in o[o != ""].value_counts().items():
        p(f"  {k:<6}{c:>7,}  {c/(o!='').sum()*100:>5.1f}%")

    # --- 지정 ---
    p("\n=== 보호수지정일자 ===")
    d = pd.to_datetime(df["보호수지정일자"], errors="coerce")
    yrs = d.dt.year.value_counts().sort_index()
    p(f"가장 이른 {d.min().date()} · 가장 늦은 {d.max().date()}")
    p(f"최다 {yrs.idxmax():.0f}년 {yrs.max():,}건 ({yrs.max()/n*100:.1f}%)")
    p(yrs[yrs.index >= 1968].to_string())
    p(f"1968년 이전 {yrs[yrs.index < 1968].sum():,}건")
    p(f"해지일자가 적힌 곳 {(df['보호수해지일자']!='').sum():,}")

    # --- 그루수 ---
    p("\n=== 그루수 ===")
    p(f"합계 {cnt.sum():,.0f} · 중앙값 {cnt.median():.0f} · 최대 {cnt.max():.0f}")
    p(f"1그루짜리 {(cnt==1).sum():,} ({(cnt==1).sum()/n*100:.1f}%)")

    # --- 중복 ---
    # 종류·나이·주소 세 칸만 보면 3,724건이 걸리는데, 같은 마을의 여러 그루가
    # 따로 등록된 정상 사례가 섞인다. 관리용 칸을 뺀 나머지가 전부 같은 줄만 센다.
    p("\n=== 같은 줄이 두 번 ===")
    admin = ("관리번호", "지정번호", "데이터갱신구분", "데이터갱신시점", "최종수정시점")
    cols = [c for c in df.columns if c not in admin]
    dup = df.duplicated(subset=cols, keep=False)
    p(f"관리용 칸을 뺀 모든 칸이 같은 줄 {dup.sum():,}건 ({dup.sum()/n*100:.1f}%)")
    p("예시:")
    for i in df[dup].sort_values(cols[:6]).head(4).index:
        p(f"  {df['나무종류'][i][:10]:<12}{df['나무나이'][i]:>5}년  {addr[i][:40]}")
    loose = (df["나무종류"] + "|" + df["나무나이"] + "|" + addr).duplicated(keep=False)
    p(f"참고 - 종류·나이·주소 세 칸만 보면 {loose.sum():,}건이 걸린다. "
      f"한 마을의 여러 그루가 따로 등록된 정상 사례가 섞여서 쓰지 않았다.")
    p(f"\n도로명주소가 비어 있는 줄 {(df['소재지도로명주소']=='').sum():,}"
      f" (지번주소로 대신 셌다)")

    p("\n=== 시도 ===")
    p(df["시도명"].value_counts().head(8).to_string())

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print("-> " + str(OUT))


if __name__ == "__main__":
    main()
