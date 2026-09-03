"""
robots.txt 와 sitemap.xml 을 다시 만든다.

열람실을 새로 추가할 때마다 손으로 고치면 언젠가 빠뜨린다.
폴더에 있는 .html 을 훑어서 매번 새로 쓴다.

사용법:
    python scripts/sitemap.py
"""
import datetime
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOMAIN = "https://semoji.net"

# 색인시키지 않을 페이지
SKIP = set()

# 중요도. 적히지 않은 페이지는 열람실로 보고 0.8 을 준다.
PRIORITY = {"index.html": "1.0", "about.html": "0.5",
            "contact.html": "0.4", "privacy.html": "0.3"}


def main():
    pages = sorted(p.name for p in ROOT.glob("*.html") if p.name not in SKIP)
    if "index.html" not in pages:
        raise SystemExit("index.html 이 없습니다. 프로젝트 루트에서 실행하세요.")

    # index.html 을 맨 앞으로
    pages.remove("index.html")
    pages.insert(0, "index.html")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name in pages:
        # 루트 문서는 파일명 없이 노출하는 편이 정본 주소로 깔끔하다.
        loc = f"{DOMAIN}/" if name == "index.html" else f"{DOMAIN}/{name}"
        mtime = datetime.date.fromtimestamp((ROOT / name).stat().st_mtime)
        lines.append(f"  <url><loc>{loc}</loc>"
                     f"<lastmod>{mtime}</lastmod>"
                     f"<priority>{PRIORITY.get(name, '0.8')}</priority></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (ROOT / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {DOMAIN}/sitemap.xml\n",
        encoding="utf-8")

    print(f"{DOMAIN} 기준으로 {len(pages)}쪽 기록했습니다.")
    for name in pages:
        print("  ", name)


if __name__ == "__main__":
    main()
