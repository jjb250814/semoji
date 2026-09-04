"""
robots.txt 와 sitemap.xml 을 다시 만든다.

열람실을 새로 추가할 때마다 손으로 고치면 언젠가 빠뜨린다.
폴더를 훑어서 매번 새로 쓴다.

주소는 폴더 구조다. `about/index.html` 이 `https://semoji.net/about/` 으로 나간다.
(2026-09-03에 `about.html` 방식에서 옮겼다. 색인 전이라 비용이 없었다.)

새로 생긴 주소는 따로 모아서 알려준다. 색인 요청을 몰아서 넣을 때
"어느 걸 넣었더라" 를 기억하지 않아도 되게.

사용법:
    python scripts/sitemap.py
"""
import datetime
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://semoji.net"

# 색인시키지 않을 폴더
SKIP = {"data", "scripts", ".claude", ".git"}

# 중요도. 적히지 않은 페이지는 열람실로 보고 0.8 을 준다.
PRIORITY = {"": "1.0", "about": "0.5", "contact": "0.4", "privacy": "0.3"}


def pages():
    """(주소경로, 파일) 목록. 루트가 맨 앞."""
    out = [("", ROOT / "index.html")]
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir()):
        if d.name in SKIP or d.name.startswith("."):
            continue
        f = d / "index.html"
        if f.exists():
            out.append((d.name, f))
    return out


def last_changed(f):
    """그 파일을 마지막으로 고친 날. **파일 수정시각을 쓰면 안 된다.**
    git clone 이나 OneDrive 동기화가 수정시각을 '오늘'로 만들어 버려서,
    21쪽 전부가 오늘 바뀐 것처럼 검색엔진에 알리게 된다. 커밋 날짜는 어디서
    받아도 같다. 아직 커밋 안 된 새 파일만 수정시각으로 물러선다."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(f)],
                             cwd=ROOT, capture_output=True, text=True, timeout=10)
        d = out.stdout.strip()
        if d:
            return d
    except Exception:
        pass
    return str(datetime.date.fromtimestamp(f.stat().st_mtime))


def already_listed():
    """지난번 sitemap.xml 에 적혀 있던 주소들. 없으면 빈 집합."""
    f = ROOT / "sitemap.xml"
    if not f.exists():
        return set()
    return set(re.findall(r"<loc>(.*?)</loc>", f.read_text(encoding="utf-8")))


def main():
    if not (ROOT / "index.html").exists():
        raise SystemExit("index.html 이 없습니다. 프로젝트 루트에서 실행하세요.")

    before = already_listed()
    found = pages()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, f in found:
        loc = f"{DOMAIN}/" if slug == "" else f"{DOMAIN}/{slug}/"
        lines.append(f"  <url><loc>{loc}</loc>"
                     f"<lastmod>{last_changed(f)}</lastmod>"
                     f"<priority>{PRIORITY.get(slug, '0.8')}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8")

    print(f"{DOMAIN} 기준으로 {len(found)}쪽 기록했습니다.")
    for slug, _ in found:
        print("  ", f"/{slug}/" if slug else "/")

    locs = [f"{DOMAIN}/" if slug == "" else f"{DOMAIN}/{slug}/" for slug, _ in found]
    new = [loc for loc in locs if loc not in before]
    if new:
        bar = "-" * 52
        print()
        print(bar)
        print(f"새로 생긴 주소 {len(new)}개. 색인 요청에 그대로 붙여넣으세요.")
        print("  구글   서치콘솔 위쪽 검색창에 주소를 넣고 → 색인 생성 요청")
        print("  네이버 서치어드바이저 → 요청 → 웹 페이지 수집")
        print(bar)
        for loc in new:
            print(loc)
        print(bar)
        print("※ 급하지 않습니다. 몇 개 모아서 한 번에 넣어도 됩니다.")


if __name__ == "__main__":
    main()
