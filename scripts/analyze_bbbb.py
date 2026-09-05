"""
data/ 에 받아둔 데이터셋 전부를 가로질러 「BBBB」를 센다. 제30호 열람실용.

이 열람실은 데이터셋 하나를 파는 것이 아니라, **세모지가 지금까지 받아둔
파일 전부**를 훑는다. 22개를 모았기 때문에 비로소 보이는 흠이다.

먼저 데이터가 data/ 에 있어야 한다. 없으면 README 「실행」 절의
fetch 명령을 먼저 돌린다.

사용법:
    python scripts/analyze_bbbb.py

※ 조심할 것

1. **「BBBB가 오류다」라고 단정하지 않는다.**
   확인해 보면 BBBB 인 줄은 언제나 상세영업상태명이 비어 있고
   영업상태는 「영업/정상」(코드 01)이다. **세부 상태를 모른다는 뜻의
   자리표시자**로 보이지만, 원본에 그 정의는 없다.

2. **불변 관계를 매번 다시 확인한다.** 「언제나 그렇다」고 쓰려면
   파일마다 검사해야 한다. 어긋나는 파일이 하나라도 있으면 표에 적는다.

3. **행 수를 사이트 총계에 더하지 않는다.** 이미 다른 열람실에서 센
   데이터를 다시 보는 것이라 중복이 된다.

4. **파일을 통째로 읽지 않는다.** 통신판매업이 919MB 다.
   usecols 로 상태 칸 세 개만 읽는다.
"""
import io
import sys
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "분석결과_BBBB.txt"

NEED = ["상세영업상태코드", "상세영업상태명", "영업상태명", "영업상태코드"]

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def main():
    files = sorted(DATA.glob("*.csv"))
    if not files:
        raise SystemExit(f"{DATA} 에 CSV 가 없습니다. README 「실행」 절을 보세요.")

    rows = []
    total_rows = 0
    total_bbbb = 0
    broken = []

    for f in files:
        try:
            head = pd.read_csv(f, dtype=str, nrows=0)
        except Exception:
            continue
        cols = [c for c in NEED if c in head.columns]
        if "상세영업상태코드" not in cols:
            continue
        d = pd.read_csv(f, dtype=str, keep_default_na=False,
                        low_memory=False, usecols=cols)
        for c in d.columns:
            d[c] = d[c].str.strip()
        n = len(d)
        total_rows += n
        code = d["상세영업상태코드"]
        b = code == "BBBB"
        total_bbbb += b.sum()

        # 불변 관계 검사: BBBB 면 상세영업상태명이 비고 영업상태코드가 01 인가
        ok = "—"
        if b.sum():
            blank = (d.loc[b, "상세영업상태명"] == "").all() \
                if "상세영업상태명" in d.columns else False
            act = (d.loc[b, "영업상태코드"] == "01").all() \
                if "영업상태코드" in d.columns else False
            ok = "예" if (blank and act) else "아니오"
            if ok == "아니오":
                broken.append(f.stem)
        rows.append((f.stem, n, int(b.sum()), code.nunique(), ok))

    rows.sort(key=lambda r: -r[2])
    hit = [r for r in rows if r[2]]

    p("=== 페이지 상단 지표 ===")
    p(f"훑은 데이터셋 {len(rows)}개 · {total_rows:,}행")
    p(f"「BBBB」가 나온 데이터셋 {len(hit)}개 · 모두 {total_bbbb:,}건")
    p(f"가장 많은 곳 {hit[0][0]} {hit[0][2]:,}건 "
      f"({100 * hit[0][2] / hit[0][1]:.1f}%)")

    p("")
    p("=== 데이터셋별 ===")
    p(f"{'데이터셋':16s} {'행':>10s} {'BBBB':>7s} {'비율':>7s} {'코드종류':>7s} {'불변':>5s}")
    for nm, n, b, k, ok in rows:
        p(f"{nm:16s} {n:10,} {b:7,} {100 * b / n:6.2f}% {k:7,} {ok:>5s}")

    p("")
    p("=== 검증 — BBBB 인 줄은 언제나 같은 모양인가 ===")
    p("BBBB 이면 (가) 상세영업상태명이 비어 있고 (나) 영업상태코드가 01(영업/정상)인가?")
    p("")
    if broken:
        p(f"!! 어긋나는 파일 {len(broken)}개: {', '.join(broken)}")
    else:
        p(f"→ BBBB 가 나온 {len(hit)}개 파일 전부에서 참이다. 예외가 없다.")
    p("")
    p("즉 「BBBB」는 영업 중인데 세부 상태를 모른다는 뜻의 자리표시자로 보인다.")
    p("※ 다만 원본에 그 정의는 적혀 있지 않다. 단정하지 않는다.")

    p("")
    p("=== 코드 칸에 어떤 값들이 있나 ===")
    p("같은 이름의 칸인데 데이터셋마다 코드 체계가 다르다.")
    p("")
    for f in files:
        try:
            head = pd.read_csv(f, dtype=str, nrows=0)
        except Exception:
            continue
        if "상세영업상태코드" not in head.columns:
            continue
        d = pd.read_csv(f, dtype=str, keep_default_na=False,
                        low_memory=False, usecols=["상세영업상태코드"])
        s = d["상세영업상태코드"].str.strip()
        vals = sorted(s.unique())
        p(f"  {f.stem:16s} {'/'.join(vals)}")

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
