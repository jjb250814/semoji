"""
아무 LOCALDATA CSV나 넣으면 '광맥 후보'를 훑어준다.

208개 데이터셋 중 어디에 이야기가 있는지 먼저 찾기 위한 정찰 도구다.
여기서 나온 숫자를 그대로 발행하지 않는다. 열람실로 쓸 데이터셋이 정해지면
전용 analyze_*.py 를 만들어 다시 계산하고 검증한 뒤에 쓴다.

사용법:
    python scripts/scan.py              # data/ 안의 모든 CSV
    python scripts/scan.py 동물병원       # 이름에 '동물병원'이 들어가는 것만
"""
import io
import re
import sys
import pathlib

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "스캔결과.txt"

# 이야기가 될 수 없는 칸. 주소는 규격이 있어서 고유값이 많아도 광맥이 아니다.
NOISE = re.compile(
    r"코드|번호|좌표|일련|갱신|우편|시점|버전|url|링크|위도|경도|주소|소재지|지번",
    re.IGNORECASE,
)
DATE_HINT = re.compile(r"일자|날짜|시점|기간")

buf = io.StringIO()


def p(*a):
    print(*a, file=buf)


def classify(s: pd.Series, col: str):
    """칸 하나를 보고 어떤 종류인지 판정한다."""
    filled = s[s != ""]
    if len(filled) == 0:
        return "빈 칸", 0.0, 0, 0, 0.0
    fill = len(filled) / len(s)
    uniq = filled.nunique()
    once = (filled.value_counts() == 1).sum()
    avglen = filled.str.len().mean()
    ratio = uniq / len(filled)
    once_n = once

    if NOISE.search(col):
        kind = "식별자"
    elif DATE_HINT.search(col):
        kind = "날짜"
    elif (ratio > 0.15 or once >= 500) and avglen > 6:
        kind = "자유입력"          # 사람이 손으로 적는 칸 — 최고의 광맥
    elif ratio > 0.3:
        kind = "이름"              # 상호처럼 거의 다 다른 짧은 값
    elif uniq <= 30:
        kind = "범주"              # 답이 몇 개뿐 — 「자동/수동」 같은 것
    else:
        kind = "기타"
    return kind, fill, uniq, once, avglen


def dig(df: pd.DataFrame, title: str):
    p("=" * 60)
    p(f"■ {title}   {len(df):,}행 × {len(df.columns)}칸")
    p("=" * 60)

    score = 0
    veins = []
    if len(df) >= 50_000:
        score += 2
    elif len(df) >= 10_000:
        score += 1

    # --- 칸 목록 ---
    p("\n[칸]")
    p(f"{'칸 이름':<22}{'종류':<8}{'채움':>7}{'고유값':>9}{'1회만':>9}{'평균길이':>8}")
    rows = {}
    for col in df.columns:
        kind, fill, uniq, once, avglen = classify(df[col], col)
        rows[col] = kind
        if kind in ("식별자", "빈 칸"):
            continue
        p(f"{col[:20]:<22}{kind:<8}{fill*100:>6.1f}%{uniq:>9,}{once:>9,}{avglen:>8.1f}")

    # --- 자유입력: 담당자의 말투가 남는 칸 ---
    free = [c for c, k in rows.items() if k == "자유입력"]
    if free:
        p("\n[자유입력 — 규격이 없어서 사람 말투가 남는 칸]")
        for c in free:
            v = df[c][df[c] != ""]
            once = (v.value_counts() == 1).sum()
            p(f"  · {c}: 고유값 {v.nunique():,} / 1회만 등장 {once:,}")
            for s in v.value_counts().index[:3]:
                p(f"      많이 쓴 말   {s[:45]}")
            for s in v[v.map(v.value_counts()) == 1].head(3):
                p(f"      한 번뿐인 말 {s[:45]}")
            pts = 0
            for thr, w in ((500, 2), (3_000, 2), (10_000, 3)):
                if once >= thr:
                    pts += w
            if pts:
                score += pts
                veins.append(f"자유입력 「{c}」 1회성 {once:,}건  (+{pts})")

    # --- 범주: 답이 몇 개뿐인 칸. 사라진 서식 항목이 여기 숨어 있다 ---
    cat = [c for c, k in rows.items() if k == "범주"]
    if cat:
        p("\n[범주 — 답이 몇 개뿐인 칸]")
        for c in cat:
            v = df[c][df[c] != ""]
            if v.nunique() <= 1:
                continue
            fill = len(v) / len(df)
            tops = ", ".join(f"{i}({n:,})" for i, n in v.value_counts().head(5).items())
            p(f"  · {c} [채움 {fill*100:.1f}%]: {tops}")

            # 옛 서식이 물어봤던 질문. 신호는 '낮은 채움률'이 아니라
            # '답이 두세 개뿐인데 한쪽으로 쏠린 것'이다. 「비디오재생기명 자동/수동」이 그랬다.
            if c in ("영업상태명", "상세영업상태명") or fill < 0.05:
                continue
            share = v.value_counts().iloc[0] / len(v)
            if v.nunique() <= 3:
                pts = 4 if share >= 0.9 else 3
                veins.append(f"사라진 칸 「{c}」 답 {v.nunique()}가지, "
                             f"쏠림 {share*100:.1f}%  (+{pts})")
            elif v.nunique() <= 8 and fill < 0.6:
                pts = 2
                veins.append(f"옛 서식 「{c}」 답 {v.nunique()}가지, "
                             f"채움 {fill*100:.1f}%  (+2)")
            else:
                continue
            score += pts

    # --- 이름 ---
    namecol = next((c for c in df.columns if "사업장명" in c or "업소명" in c), None)
    if namecol:
        n = df[namecol][df[namecol] != ""]
        longest = n.loc[n.str.len().idxmax()]
        p(f"\n[이름] {namecol}")
        p(f"  가장 긴 이름 {n.str.len().max()}자 — {longest[:60]}")
        toks = n.str.split().explode()
        toks = toks[toks.str.len() >= 2]
        p("  자주 쓰인 낱말 " + ", ".join(
            f"{w}({c:,})" for w, c in toks.value_counts().head(12).items()))
        if n.str.len().max() >= 25:
            score += 1
            veins.append(f"긴 이름 {n.str.len().max()}자  (+1)")

    # --- 수명 ---
    oc = next((c for c in df.columns if "인허가일자" in c or "지정일자" in c), None)
    cc = next((c for c in df.columns if "폐업일자" in c), None)
    if oc and cc:
        o = pd.to_datetime(df[oc], errors="coerce")
        c_ = pd.to_datetime(df[cc], errors="coerce")
        life = (c_ - o).dt.days
        life = life[life >= 0]
        if len(life):
            p(f"\n[수명] 폐업까지 {len(life):,}건")
            p(f"  중앙값 {life.median()/365:.1f}년 · 최단 {life.min():.0f}일 · "
              f"최장 {life.max()/365:.1f}년")
            if life.min() <= 7:
                score += 2
                veins.append(f"최단 수명 {life.min():.0f}일  (+2)")
        # 데이터의 흠
        bad = o[(o.dt.year < 1960) | (o.dt.year > 2026)]
        if len(bad):
            score += 1
            p(f"\n[데이터의 흠] {oc} 범위 밖 {len(bad)}건: "
              + ", ".join(str(d.date()) for d in bad.head(5)))
            veins.append(f"범위 밖 날짜 {len(bad)}건")

    # --- 생존 ---
    if "영업상태명" in df.columns:
        alive = (df["영업상태명"] == "영업/정상").sum()
        p(f"\n[생존] 영업 중 {alive:,} / 사라짐 {len(df)-alive:,} "
          f"({(len(df)-alive)/len(df)*100:.1f}%)")

    p(f"\n★ 광맥 점수 {score}")
    for v in veins:
        p(f"   - {v}")
    p("")
    return score, veins


def main():
    pat = sys.argv[1] if len(sys.argv) > 1 else ""
    files = sorted(f for f in DATA.glob("*.csv") if pat in f.stem)
    if not files:
        raise SystemExit(f"data/ 에 '{pat}' 에 맞는 CSV가 없습니다.")

    board = []
    for f in files:
        try:
            df = pd.read_csv(f, dtype=str, keep_default_na=False,
                             on_bad_lines="skip", engine="python")
        except Exception as e:
            p(f"!! {f.name} 읽기 실패: {e}\n")
            continue
        df.columns = [c.strip() for c in df.columns]
        for c in df.columns:
            df[c] = df[c].str.strip()
        board.append((dig(df, f.stem)[0], f.stem))

    p("=" * 60)
    p("■ 순위")
    p("=" * 60)
    for s, name in sorted(board, reverse=True):
        p(f"  {s:>3}  {name}")

    OUT.write_text(buf.getvalue(), encoding="utf-8")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
