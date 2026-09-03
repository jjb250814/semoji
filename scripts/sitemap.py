"""
robots.txt 와 sitemap.xml 을 다시 만든다.

열람실을 새로 추가할 때마다 손으로 고치면 언젠가 빠뜨린다.
폴더를 훑어서 매번 새로 쓴다.

주소는 폴더 구조다. `about/index.html` 이 `https://semoji.net/about/` 으로 나간다.
(2026-09-03에 `about.html` 방식에서 옮겼다. 색인 전이라 비용이 없었다.)

사용법:
    python scripts/sitemap.py
"""
import datetime
import pathlib

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


def main():
    if not (ROOT / "index.html").exists():
        raise SystemExit("index.html 이 없습니다. 프로젝트 루트에서 실행하세요.")

    found = pages()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, f in found:
        loc = f"{DOMAIN}/" if slug == "" else f"{DOMAIN}/{slug}/"
        mtime = datetime.date.fromtimestamp(f.stat().st_mtime)
        lines.append(f"  <url><loc>{loc}</loc>"
                     f"<lastmod>{mtime}</lastmod>"
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


if __name__ == "__main__":
    main()
