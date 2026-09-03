"""
제17호 「발한실」(bathhouse/index.html) 조립기.

공용 CSS는 waste/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_bath.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_bath.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "waste" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("목욕장업 서류에는 「발한실여부」라는 칸이 있다. 땀 내는 방이 있느냐는 뜻이다. "
        "1960년대 허가받은 곳은 18.6%, 2010년대는 52.0%가 있다고 적었다.")

HEAD = """<title>발한실</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/bathhouse/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="발한실 — 세모지 제17호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/bathhouse/">
<meta property="og:image" content="https://semoji.net/og/bathhouse.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="발한실 — 세모지 제17호 열람실">
<meta name="twitter:card" content="summary_large_image">
<meta name="naver-site-verification" content="e1aa1ef1b15b68297398065f83c4c5a96d1f3d0d" />
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5277473094749097"
     crossorigin="anonymous"></script>
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@400;600;800&family=IBM+Plex+Sans+KR:wght@300;400;500;600&family=Nanum+Gothic+Coding:wght@400;700&display=swap">
""" % {"d": DESC}

EXTRA_STYLE = """<style>
/* 제17호 전용 */
.yn-box{padding:36px var(--pad) 32px;margin:66px 0 0}
.yn-lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;color:var(--muted);margin:0 0 22px}
.yn-grid{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--rule)}
.yn-cell{padding:24px 20px 22px 0;border-right:1px solid var(--rule-2)}
.yn-cell:last-child{border-right:0}
.yn-cell .lab{font-family:var(--f-display);font-weight:800;font-size:20px}
.yn-cell .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(30px,5vw,44px);line-height:1;margin-top:12px;font-variant-numeric:tabular-nums}
.yn-cell.on .n{color:var(--seal-ink)}
.yn-cell .s{display:block;font-size:13.5px;color:var(--ink-2);font-weight:300;margin-top:10px}
.yn-say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.yn-say b{font-weight:500;color:var(--ink)}
.two{display:grid;gap:30px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-top:8px}
.hbars.wide .hrow{grid-template-columns:minmax(108px,150px) 1fr minmax(70px,auto)}
@media (max-width:560px){.hbars.wide .hrow{grid-template-columns:1fr auto}}
/* 두 낱말이 자리를 바꾸는 그림 */
.swap{border-top:1px solid var(--rule);margin-top:8px}
.swap .row{display:grid;grid-template-columns:minmax(84px,110px) 1fr;gap:14px;
  align-items:center;padding:11px 0;border-bottom:1px solid var(--rule-2)}
.swap .era{font-family:var(--f-mono);font-size:12px;color:var(--muted)}
.swap .track{display:flex;height:24px;background:var(--bar-track)}
.swap .a{background:var(--bar-neutral);height:100%;width:0;transition:width .8s cubic-bezier(.2,.8,.2,1)}
.swap .b{background:var(--seal);height:100%;width:0;transition:width .8s cubic-bezier(.2,.8,.2,1)}
.swap .row:first-child .track{position:relative}
.legend{display:flex;gap:18px;font-family:var(--f-mono);font-size:11.5px;
  color:var(--muted);margin-top:12px;flex-wrap:wrap}
.legend i{display:inline-block;width:11px;height:11px;margin-right:6px;vertical-align:-1px}
.legend .k1{background:var(--bar-neutral)}
.legend .k2{background:var(--seal)}
.longq{font-family:var(--f-mono);font-size:12.5px;background:var(--card);
  border:1px solid var(--rule);border-left:3px solid var(--seal);padding:14px 16px;
  margin:14px 0 0;color:var(--ink-2);line-height:1.8}
</style>"""

# --- 숫자 (analyze_bath.py 출력과 대조) ---
SWEAT = [("1960~79", 18.6), ("1980년대", 22.7), ("1990년대", 27.4),
         ("2000년대", 43.3), ("2010년대", 52.0), ("2020년대", 39.3)]
# (연대, 곳수, '탕' %, '사우나' %)
NAMES = [("1960~79", 1511, 80.5, 2.7), ("1980년대", 3608, 78.0, 6.2),
         ("1990년대", 4154, 70.8, 13.2), ("2000년대", 5787, 32.9, 35.5),
         ("2010년대", 1886, 14.5, 34.1), ("2020년대", 828, 13.9, 24.8)]
TRADE = [("한증막업", 79.0), ("공동탕업", 71.5), ("찜질시설서비스영업", 64.2),
         ("목욕장업 기타", 49.1), ("공동탕업+찜질시설", 46.1)]
WORDS = [("탕", 9275), ("목욕", 4309), ("사우나", 3717), ("스파", 615),
         ("한증", 579), ("찜질", 557), ("온천", 548), ("불가마", 231)]
COMMON = [("청수탕", 93), ("수정탕", 63), ("약수탕", 53), ("현대탕", 50),
          ("장수탕", 47), ("현대목욕탕", 46), ("중앙목욕탕", 44), ("옥천탕", 42)]
NEW = [(1970, 171), (1971, 159), (1972, 139), (1973, 173), (1974, 85), (1975, 46),
       (1976, 71), (1977, 70), (1978, 94), (1979, 123), (1980, 166), (1981, 281),
       (1982, 304), (1983, 424), (1984, 398), (1985, 346), (1986, 391), (1987, 452),
       (1988, 459), (1989, 387), (1990, 413), (1991, 372), (1992, 310), (1993, 355),
       (1994, 414), (1995, 454), (1996, 428), (1997, 576), (1998, 449), (1999, 383),
       (2000, 676), (2001, 635), (2002, 570), (2003, 1442), (2004, 639), (2005, 427),
       (2006, 527), (2007, 324), (2008, 299), (2009, 248), (2010, 225), (2011, 215),
       (2012, 202), (2013, 169), (2014, 190), (2015, 188), (2016, 174), (2017, 194),
       (2018, 178), (2019, 151), (2020, 131), (2021, 103), (2022, 105), (2023, 146),
       (2024, 104), (2025, 125), (2026, 114)]


def hbars(rows, unit="곳", cls=""):
    top = max(v for _, v in rows)
    out = ['<div class="hbars%s">' % ((" " + cls) if cls else "")]
    for k, v in rows:
        val = f"{v:,}{unit}" if isinstance(v, int) else f"{v}{unit}"
        out.append('<div class="hrow"><span class="cat">%s</span>'
                   '<span class="track"><span class="bar" data-w="%.2f"></span></span>'
                   '<span class="val">%s</span></div>' % (k, v / top * 100, val))
    out.append("</div>")
    return "\n    ".join(out)


swap = '<div class="swap">' + "".join(
    '<div class="row"><span class="era">%s</span>'
    '<span class="track"><span class="a" data-w="%.1f"></span>'
    '<span class="b" data-w="%.1f"></span></span></div>'
    % (era, tang, sauna) for era, _, tang, sauna in NAMES) + "</div>"

nmax = max(v for _, v in NEW)
ncols = "".join(
    '<div class="col%s" style="height:%.1f%%" data-t="%d년 %s곳"></div>'
    % (" peak" if y == 2003 else "", v / nmax * 100, y, f"{v:,}")
    for y, v in NEW)

BODY = """
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제17호 열람실</span>
    <span>원자료 <b>목욕장업</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제17호 열람실 · 전국 목욕장업 기록</p>
    <h1>발한<span class="or">실</span></h1>
    <p class="lede">
      목욕탕 영업신고서에는 <b>「발한실여부」</b>라는 칸이 있습니다.
      <b>땀을 내는 방이 있느냐</b>는 뜻입니다. 한증막이나 찜질방을 서류에서는 그렇게 부릅니다.
      17,789곳 가운데 <b>6,032곳이 「있음」</b>이라고 적었는데,
      언제 허가받았느냐에 따라 그 비율이 크게 다릅니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">17,789</span><span class="l">등록된 목욕장</span><span class="s">1954년 이후 전체 기록</span></div>
      <div class="fig hot"><span class="n">68.2%</span><span class="l">이미 사라짐</span><span class="s">12,124곳</span></div>
      <div class="fig"><span class="n">6,032</span><span class="l">발한실이 있다</span><span class="s">답한 곳의 34.1%</span></div>
      <div class="fig hot"><span class="n">13.68년</span><span class="l">버틴 기간 중앙값</span><span class="s">가장 오래 산 곳은 101.7년</span></div>
    </div>
  </div>

  <article class="form yn-box">
    <span class="form-label">발한실여부</span>
    <p class="yn-lab">땀을 내는 방이 있는가. 17,712곳(99.6%)이 답했다.</p>
    <div class="yn-grid">
      <div class="yn-cell on"><span class="lab">있음</span>
        <span class="n">6,032</span><span class="s">34.1%</span></div>
      <div class="yn-cell"><span class="lab">없음</span>
        <span class="n">11,680</span><span class="s">65.9%</span></div>
    </div>
    <p class="yn-say">지금 <b>영업 중인 곳만 보면 44.8%</b>가 있다고 답했고,
      <b>이미 문 닫은 곳은 29.0%</b>였습니다. 발한실이 있는 목욕탕이 더 오래 남았습니다.</p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>땀 내는 방이 늘어난다</h2><span>허가 연도대별 「있음」 비율</span></div>
    <p class="blk-note">1960~70년대에 허가받은 목욕탕은 <b>18.6%</b>만 발한실이 있었습니다.
      2010년대에는 <b>52.0%</b>가 됩니다. 반세기 만에 세 배 가까이 올랐습니다.
      <b>목욕탕이 씻는 곳에서 땀 빼는 곳으로 옮겨 간 흐름</b>이 칸 하나에 남아 있습니다.</p>
    {{sweat}}
    <p class="blk-note" style="margin-top:26px">2020년대에 39.3%로 떨어진 것은
      표본이 828곳으로 적고 아직 채워지는 중이기 때문일 수 있습니다.
      <b>그 이유까지는 데이터에 없습니다.</b></p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>이름도 같이 바뀐다</h2><span>상호에 든 낱말</span></div>
    <p class="blk-note">같은 흐름이 <b>간판에도</b> 있습니다.
      1960~70년대 허가받은 곳은 <b>80.5%</b>가 상호에 「탕」을 넣었고
      「사우나」는 2.7%였습니다. 2010년대에는 「탕」이 <b>14.5%</b>로 내려가고
      「사우나」가 <b>34.1%</b>로 올라갑니다. <b>2000년대에 두 낱말이 자리를 바꿉니다.</b></p>
    {{swap}}
    <div class="legend"><span><i class="k1"></i>상호에 「탕」</span>
      <span><i class="k2"></i>상호에 「사우나」</span></div>
    <p class="blk-note" style="margin-top:26px">전체로 세면 「탕」이 9,275곳으로 여전히 가장 많습니다.
      오래된 이름이 그만큼 많이 쌓여 있기 때문입니다.</p>
    <div class="two" style="margin-top:30px">
      <div>
        <p class="yn-lab">상호에 든 낱말</p>
        {{words}}
      </div>
      <div>
        <p class="yn-lab">가장 흔한 상호</p>
        {{common}}
        <p class="blk-note" style="margin-top:16px">앞에 붙는 말이 <b>물 이름</b>입니다 —
          청수, 수정, 약수, 옥천. 물이 좋다는 뜻으로 지은 이름들입니다.</p>
      </div>
    </div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>둘 다 가진 곳이 가장 오래 버텼다</h2><span>업태별 폐업률</span></div>
    <p class="blk-note">서류는 목욕장을 여섯 갈래로 나눕니다.
      탕만 있는 <b>공동탕업</b>이 13,834곳으로 대부분인데 <b>71.5%가 문을 닫았습니다.</b>
      땀 내는 곳만 있는 <b>한증막업</b>은 더 심해서 79.0%입니다.
      가장 덜 사라진 것은 <b>둘 다 가진 「공동탕업+찜질시설」로 46.1%</b>입니다.</p>
    {{trade}}
    <p class="blk-note" style="margin-top:26px">업태 칸에 <b>「관광호텔」</b>이라 적힌 곳도 14곳 있습니다.
      호텔 안의 목욕탕을 따로 신고한 것으로 보이는데,
      <b>14곳이 모두 폐업</b>했습니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>2003년에 1,442곳</h2><span>연도별 신규 허가</span></div>
    <p class="blk-note">2003년 한 해에 <b>1,442곳</b>이 새로 허가받았습니다.
      바로 앞뒤 해의 두 배가 넘습니다. 그 뒤로는 계속 줄어
      2021년에는 103곳까지 내려갔습니다.
      문 닫은 해로 보면 <b>2003년이 880곳으로 가장 많습니다</b> —
      같은 해에 가장 많이 생기고 가장 많이 사라졌습니다.</p>
    <div class="cols">{{ncols}}</div>
    <div class="axis"><span class="first">1970</span><span style="left:50%">1998</span><span class="last" style="left:100%">2026</span></div>

    <div class="flaws" style="margin-top:48px">
      <div class="flaw"><span class="h">5,764</span>
        <p class="b">욕실이 0개라고 적힌 목욕탕.</p>
        <p class="c">욕실수를 적은 13,170곳 중 43.8%입니다. 가운뎃값은 2개이고
          가장 많은 곳은 119개입니다. 안 센 것인지 없는 것인지는 알 수 없습니다.</p></div>
      <div class="flaw"><span class="h">1900</span>
        <p class="b">1900년에 허가받은 것으로 적힌 곳이 7곳.</p>
        <p class="c">가장 긴 수명이 101.7년으로 계산되는 것도 이 때문입니다.</p></div>
      <div class="flaw"><span class="h">47자</span>
        <p class="b">가장 긴 상호는 한글과 영문을 함께 적었다.</p>
        <p class="c">「켄싱턴리조트 서귀포목욕탕(Kensington Resort Seogwipo Sauna)」입니다.
          한글로는 목욕탕, 영문으로는 Sauna 입니다. <b>한 이름 안에서 두 낱말이 갈립니다.</b></p></div>
      <div class="flaw"><span class="h">31</span>
        <p class="b">「조건부허가신고사유」를 적은 곳.</p>
        <p class="c">건물이 아직 준공되지 않아 임시로 낸 신고입니다.
          「소송진행건으로 폐업 및 지위승계불가」처럼 사정이 그대로 적힌 것도 있습니다.</p></div>
    </div>

    <div class="longq">이 영업신고의 효력은 건축물 임시사용승인기간 2012.4.30까지이며 건축물 사용승인 연장 또는 준공 완료시 재신청 해야 함</div>
  </section>
</main>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제17호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>목욕장업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 17,789행 기준<br>상호는 지금 등록된 이름이고 날짜는 최초 허가일입니다. 그 사이의 개명은 데이터에 없습니다.</span>
  </div>
</footer>

<div class="tip" id="tip"></div>
<script>
/* 모든 값은 원본 CSV 17,789행에서 계산했습니다. scripts/analyze_bath.py 로 재현됩니다. */

const io = new IntersectionObserver(function (es) {
  es.forEach(function (e) {
    if (!e.isIntersecting) return;
    e.target.querySelectorAll('.bar, .a, .b').forEach(function (b, n) {
      setTimeout(function () { b.style.width = b.dataset.w + '%'; }, n * 45);
    });
    io.unobserve(e.target);
  });
}, { threshold: .25 });
document.querySelectorAll('.hbars, .swap').forEach(function (el) { io.observe(el); });

const tip = document.getElementById('tip');
document.querySelectorAll('.col').forEach(function (c) {
  c.addEventListener('mouseenter', function () {
    tip.textContent = c.dataset.t;
    tip.classList.add('on');
    const r = c.getBoundingClientRect();
    tip.style.left = (r.left + r.width / 2) + 'px';
    tip.style.top = r.top + 'px';
  });
  c.addEventListener('mouseleave', function () { tip.classList.remove('on'); });
});
"""

values = {
    "sweat": hbars(SWEAT, unit="%", cls="wide"),
    "swap": swap,
    "words": hbars(WORDS, cls="wide"),
    "common": hbars(COMMON, cls="wide"),
    "trade": hbars(TRADE, unit="%", cls="wide"),
    "ncols": ncols,
}
body = BODY
for k, v in values.items():
    body = body.replace("{{" + k + "}}", v)
assert "{{" not in body

out_dir = ROOT / "bathhouse"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + body + "</script>\n",
               encoding="utf-8")
print("bathhouse/index.html written:", f"{out.stat().st_size:,}", "bytes")
