"""
LOCALDATA(지방행정인허가데이터개방) 파일 내려받기.

file.localdata.go.kr 은 인허가/생활편의 데이터셋 수백 개를 CSV로 열어두고 있다.
목록 페이지:  https://file.localdata.go.kr/file/excellent_restaurant_info/info
실제 파일:    https://file.localdata.go.kr/file/download/<slug>/info

받은 파일은 CP949 인코딩이라 UTF-8로 바꿔서 data/ 에 저장한다.

사용법
    python scripts/fetch.py excellent_restaurant_info 모범음식점정보
    python scripts/fetch.py animal_hospitals 동물병원
    python scripts/fetch.py --list            # 어떤 데이터셋이 있는지 뽑아보기
"""
import sys
import pathlib
import re
import urllib.request

BASE = "https://file.localdata.go.kr"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0 Safari/537.36")
DATA_DIR = pathlib.Path(__file__).resolve().parent.parent / "data"


def get(url):
    """WebFetch 로는 403이 난다. 브라우저 UA와 Referer를 붙여야 열린다."""
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": BASE + "/"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def list_datasets():
    html = get(f"{BASE}/file/excellent_restaurant_info/info").decode("utf-8", "replace")
    slugs = sorted(set(re.findall(r'href="/file/([a-z0-9_]+)/info"', html)))
    print(f"{len(slugs)}개 데이터셋")
    for s in slugs:
        print(" ", s)


def fetch(slug, name):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / f"{name}.csv"
    print(f"내려받는 중 … {slug}")
    raw = get(f"{BASE}/file/download/{slug}/info")
    # 공백 CSV나 에러 페이지를 그대로 덮어쓰지 않도록 확인한다.
    if len(raw) < 1024 or raw.lstrip()[:15].lower().startswith(b"<!doctype"):
        sys.exit(f"CSV가 아닌 응답을 받았습니다 ({len(raw):,} bytes). slug를 확인하세요.")
    text = raw.decode("cp949", "replace")
    out.write_text(text, encoding="utf-8", newline="")
    rows = text.count("\n")
    print(f"저장 완료 → {out}  ({len(raw):,} bytes, 약 {rows:,}행)")
    print("첫 줄:", text.split("\n", 1)[0][:200])


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        sys.exit(__doc__)
    if args[0] == "--list":
        list_datasets()
    else:
        slug = args[0]
        fetch(slug, args[1] if len(args) > 1 else slug)
