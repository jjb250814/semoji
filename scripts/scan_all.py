"""
LOCALDATA 데이터셋 208개를 전부 내려받아 광맥 점수를 매긴다.

scan.py 가 칸 하나하나를 보는 도구라면, 이 스크립트는 그걸 208번 돌려서
「다음 열람실을 어디서 팔지」 순위표를 만든다.

받은 원본은 data/raw/ 에 쌓인다. 정리할 때는 그 폴더만 지우면 된다.
중간에 끊겨도 다시 실행하면 이미 받은 것은 건너뛴다.

사용법:
    python scripts/scan_all.py           # 전부
    python scripts/scan_all.py 30        # 앞에서 30개만
"""
import io
import sys
import time
import pathlib
import traceback

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fetch as F      # noqa: E402
import scan as S       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RANK = ROOT / "data" / "광맥순위.txt"
FULL = ROOT / "data" / "광맥상세.txt"

# 수백만 행짜리도 있다. 정찰 단계에서는 앞부분만 봐도 어떤 칸이 있는지는 드러난다.
# 잘린 경우 반드시 표시한다 — 이 숫자를 그대로 발행하지 않기 위해서다.
ROW_CAP = 400_000


def slugs():
    html = F.get(f"{F.BASE}/file/excellent_restaurant_info/info").decode("utf-8", "replace")
    import re
    return sorted(set(re.findall(r'href="/file/([a-z0-9_]+)/info"', html)))


def download(slug):
    """이미 받아둔 것은 건너뛴다. 실패하면 None."""
    out = RAW / f"{slug}.csv"
    if out.exists() and out.stat().st_size > 1024:
        return out
    for attempt in (1, 2):
        try:
            raw = F.get(f"{F.BASE}/file/download/{slug}/info")
            if len(raw) < 1024 or raw.lstrip()[:15].lower().startswith(b"<!doctype"):
                return None
            out.write_text(raw.decode("cp949", "replace"), encoding="utf-8", newline="")
            return out
        except Exception as e:
            if attempt == 2:
                print(f"   실패: {e}")
                return None
            time.sleep(3)


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    limit = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None

    names = slugs()[:limit]
    print(f"{len(names)}개 대상")

    board, detail = [], io.StringIO()
    t0 = time.time()

    for i, slug in enumerate(names, 1):
        print(f"[{i}/{len(names)}] {slug}", flush=True)
        path = download(slug)
        if not path:
            board.append((-1, slug, "받기 실패"))
            continue
        try:
            df = pd.read_csv(path, dtype=str, keep_default_na=False,
                             on_bad_lines="skip", low_memory=False, nrows=ROW_CAP)
            capped = len(df) >= ROW_CAP
            df.columns = [str(c).strip() for c in df.columns]
            for c in df.columns:
                df[c] = df[c].astype(str).str.strip()

            S.buf = io.StringIO()          # dig() 는 모듈 전역 buf 에 쓴다
            title = slug + ("  ※ 앞 40만 행만 봄" if capped else "")
            score, veins = S.dig(df, title)
            detail.write(S.buf.getvalue())
            board.append((score, slug, " · ".join(veins) if veins else "―"))
            print(f"   {score}점  {len(df):,}행", flush=True)
        except Exception:
            board.append((-1, slug, "읽기 실패"))
            print("   읽기 실패\n" + traceback.format_exc(limit=1), flush=True)

    board.sort(key=lambda r: -r[0])
    with RANK.open("w", encoding="utf-8") as f:
        f.write(f"광맥 순위 — {len(board)}개 데이터셋 · {time.time()-t0:.0f}초 소요\n")
        f.write("점수는 정찰용 눈금이다. 실제 발행 전에는 전용 analyze 스크립트로 다시 센다.\n\n")
        for score, slug, note in board:
            f.write(f"{score:>4}  {slug:<42}{note}\n")
    FULL.write_text(detail.getvalue(), encoding="utf-8")
    print(f"\n-> {RANK}\n-> {FULL}")


if __name__ == "__main__":
    main()
