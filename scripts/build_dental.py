"""
제15호 「열다섯 가지」(dental-lab/index.html) 조립기.

공용 CSS는 tree/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_dental.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_dental.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "tree" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("치과기공소 영업신고서는 기계 열다섯 가지를 하나하나 세라고 한다. "
        "서베이어, 포셀린로, 진공매몰기, 핀덱스. 답은 거의 다 「1」이다.")

HEAD = """<title>열다섯 가지</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/dental-lab/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="열다섯 가지 — 세모지 제15호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/dental-lab/">
<meta property="og:image" content="https://semoji.net/og/dental-lab.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="열다섯 가지 — 세모지 제15호 열람실">
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
/* 제15호 전용 */
.list-box{padding:36px var(--pad) 32px;margin:66px 0 0}
.list-lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;color:var(--muted);margin:0 0 22px}
.mlist{border-top:1px solid var(--rule);
  display:grid;grid-template-columns:repeat(auto-fit,minmax(216px,1fr))}
.mlist div{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:12px;
  align-items:baseline;padding:11px 16px 11px 0;border-bottom:1px solid var(--rule-2)}
.mlist .no{font-family:var(--f-mono);font-size:10.5px;color:var(--muted)}
.mlist .nm{font-size:14.5px;word-break:keep-all}
.mlist .ct{font-family:var(--f-mono);font-size:11.5px;color:var(--ink-2);
  font-variant-numeric:tabular-nums;white-space:nowrap}
.mlist .odd .nm{color:var(--seal-ink);font-weight:600}
.list-say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.list-say b{font-weight:500;color:var(--ink)}
.two{display:grid;gap:30px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-top:8px}
.mono-li{border-top:1px solid var(--rule);font-family:var(--f-mono);font-size:13px}
.mono-li div{display:flex;justify-content:space-between;gap:14px;padding:8px 0;
  border-bottom:1px solid var(--rule-2);font-variant-numeric:tabular-nums}
.mono-li b{font-weight:400;color:var(--ink)}
.mono-li span{color:var(--muted)}
.hbars.wide .hrow{grid-template-columns:minmax(112px,164px) 1fr minmax(64px,auto)}
@media (max-width:560px){.hbars.wide .hrow{grid-template-columns:1fr auto}}
/* 2015년 경계 */
.cut{display:grid;grid-template-columns:1fr auto 1fr;gap:18px;align-items:center;
  border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
  padding:26px 0;margin-top:8px}
.cut .side{text-align:center}
.cut .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(28px,5vw,44px);line-height:1;font-variant-numeric:tabular-nums}
.cut .side.on .n{color:var(--seal-ink)}
.cut .l{display:block;font-family:var(--f-mono);font-size:11px;color:var(--muted);margin-top:10px}
.cut .s{display:block;font-size:13px;color:var(--ink-2);font-weight:300;margin-top:6px}
.cut .mid{font-family:var(--f-mono);font-size:12px;color:var(--ink-2);white-space:nowrap;
  border-left:1px solid var(--rule);border-right:1px solid var(--rule);padding:0 18px}
@media (max-width:560px){.cut{grid-template-columns:1fr}
  .cut .mid{border:0;border-block:1px solid var(--rule);padding:12px 0;text-align:center}}
</style>"""

# --- 숫자 (analyze_dental.py 출력과 대조) ---
# (이름, 합계, 「1대」 비율, 채움률)
MACH = [("기공용레스", 9375, 95.7, 100.0), ("기공용모터", 29194, 4.8, 100.0),
        ("기공용컴프레서", 9255, 86.6, 90.0), ("샌드기", 10068, 77.4, 90.0),
        ("서베이어", 9983, 88.7, 100.0), ("아세틸렌", 8216, 93.0, 96.7),
        ("원심주조기", 9870, 92.5, 100.0), ("전기로", 11434, 76.5, 100.0),
        ("진공매몰기", 8328, 93.4, 90.0), ("진동기", 9683, 91.8, 100.0),
        ("초음파청소기", 9412, 93.4, 100.0), ("치과용프레스", 9175, 95.8, 100.0),
        ("트리머", 9122, 96.3, 100.0), ("포셀린로", 12239, 73.8, 100.0),
        ("핀덱스", 7641, 92.4, 90.0)]
ONE = [("트리머", 96.3), ("치과용프레스", 95.8), ("기공용레스", 95.7), ("진공매몰기", 93.4),
       ("초음파청소기", 93.4), ("아세틸렌", 93.0), ("원심주조기", 92.5), ("핀덱스", 92.4),
       ("진동기", 91.8), ("서베이어", 88.7), ("기공용컴프레서", 86.6), ("샌드기", 77.4),
       ("전기로", 76.5), ("포셀린로", 73.8), ("기공용모터", 4.8)]
KINDS = [("15종", 6935), ("11종", 935), ("14종", 610), ("13종", 261), ("12종", 22),
         ("10종", 1), ("1종", 1), ("0종", 3)]
NAMES = [("수치과기공소", 48), ("하나치과기공소", 45), ("미소치과기공소", 43),
         ("다온치과기공소", 41), ("우리치과기공소", 36), ("미래치과기공소", 34),
         ("이사랑치과기공소", 30), ("에이스치과기공소", 29), ("원치과기공소", 27),
         ("중앙치과기공소", 27)]
YEARS = [(1988, 35), (1989, 36), (1990, 44), (1991, 51), (1992, 61), (1993, 62),
         (1994, 71), (1995, 77), (1996, 83), (1997, 101), (1998, 96), (1999, 121),
         (2000, 163), (2001, 150), (2002, 160), (2003, 225), (2004, 226), (2005, 257),
         (2006, 277), (2007, 284), (2008, 348), (2009, 347), (2010, 394), (2011, 466),
         (2012, 476), (2013, 410), (2014, 370), (2015, 416), (2016, 424), (2017, 366),
         (2018, 330), (2019, 284), (2020, 253), (2021, 256), (2022, 236), (2023, 211),
         (2024, 217), (2025, 146), (2026, 107)]
SIDO = [("서울특별시", 2532), ("경기도", 1468), ("부산광역시", 871), ("대구광역시", 662),
        ("전남광주통합특별시", 634), ("경상남도", 410), ("대전광역시", 358), ("경상북도", 341)]


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


def monoli(rows, unit="곳"):
    out = ['<div class="mono-li">']
    for k, v in rows:
        out.append("<div><b>%s</b><span>%s%s</span></div>" % (k, f"{v:,}", unit))
    out.append("</div>")
    return "\n        ".join(out)


mlist = '<div class="mlist">' + "".join(
    '<div class="%s"><span class="no">%02d</span><span class="nm">%s</span>'
    '<span class="ct">%s대</span></div>'
    # 붉게 칠하는 것은 채움률 90.0%인 네 칸뿐이다. 아세틸렌(96.7%)은 사정이 달라
    # 본문에서 따로 설명하므로 여기서 함께 칠하면 「붉은 넷」과 어긋난다.
    % ("odd" if fill == 90.0 else "", i, nm, f"{tot:,}")
    for i, (nm, tot, one, fill) in enumerate(MACH, 1)) + "</div>"

ymax = max(v for _, v in YEARS)
ycols = "".join(
    '<div class="col%s" style="height:%.1f%%" data-t="%d년 %s곳"></div>'
    % (" peak" if y == 2012 else "", v / ymax * 100, y, f"{v:,}")
    for y, v in YEARS)

BODY = """
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제15호 열람실</span>
    <span>원자료 <b>치과기공소</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제15호 열람실 · 전국 치과기공소 기록</p>
    <h1>열다섯 <span class="or">가지</span></h1>
    <p class="lede">
      치과기공소를 열려면 영업신고서를 냅니다. 그 서식에는
      <b>기계를 세는 칸이 열다섯 개</b> 있습니다. 서베이어가 몇 대인지,
      포셀린로가 몇 대인지, 진공매몰기가 몇 대인지 하나하나 적어야 합니다.
      대부분 이름조차 낯선 기계들인데, <b>8,768곳이 이 칸들을 채웠고
      전국 합계는 162,995대</b>입니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">8,768</span><span class="l">등록된 치과기공소</span><span class="s">1974년 이후 전체 기록</span></div>
      <div class="fig hot"><span class="n">15</span><span class="l">기계를 세는 칸</span><span class="s">서식이 정한 목록</span></div>
      <div class="fig"><span class="n">162,995</span><span class="l">기계 총합</span><span class="s">한 곳 중앙값 17대</span></div>
      <div class="fig hot"><span class="n">79.1%</span><span class="l">열다섯 가지를 다 갖춤</span><span class="s">6,935곳</span></div>
    </div>
  </div>

  <article class="form list-box">
    <span class="form-label">영업신고서</span>
    <p class="list-lab">몇 대인지 적어야 하는 기계들. 옆의 수는 전국 합계다.</p>
    {{mlist}}
    <p class="list-say">붉은 넷은 <b>채움률이 다른 칸</b>입니다. 아래 4항에서 다시 봅니다.
      「레스」는 깎는 기계, 「포셀린로」는 도자기를 굽는 가마,
      「진공매몰기」는 공기를 빼고 본을 굳히는 기계입니다.
      <b>이 목록이 곧 기공소를 열 수 있는 조건인 셈입니다.</b></p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>거의 다 한 대씩</h2><span>「1대」라고 답한 비율</span></div>
    <p class="blk-note">열다섯 칸 가운데 열네 칸은 <b>답이 거의 다 「1」</b>입니다.
      트리머를 한 대만 둔 곳이 96.3%, 치과용프레스가 95.8%입니다.
      기계를 여러 대 두는 곳이 드물다는 뜻이고,
      <b>목록을 채우려고 한 대씩 갖췄다</b>는 뜻이기도 합니다.</p>
    {{one}}
    <p class="blk-note" style="margin-top:26px"><b>딱 하나가 다릅니다. 기공용모터입니다.</b>
      한 대만 둔 곳이 4.8%뿐이고 가운뎃값이 3대, 전국 합계도 29,194대로 가장 많습니다.
      모터는 손에 쥐고 쓰는 기계라 사람 수만큼 필요한 것으로 보이지만,
      <b>그 이유는 데이터에 없습니다.</b></p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>열다섯 가지를 다 갖춘 곳</h2><span>6,935곳</span></div>
    <p class="blk-note">한 곳이 몇 종류를 갖췄는지 세면 <b>79.1%가 열다섯 가지를 전부</b> 갖고 있습니다.
      가운뎃값도 15종입니다. 열한 가지만 있는 935곳은 아래 4항의 네 칸이 비어 있는 곳들입니다.</p>
    {{kinds}}
    <p class="blk-note" style="margin-top:26px">한 곳이 가진 기계를 전부 더하면 가운뎃값이 <b>17대</b>,
      가장 많은 곳이 <b>126대</b>입니다. 기계가 한 대도 없다고 적힌 곳도 3곳 있습니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>2015년 3월 11일</h2><span>네 칸의 경계</span></div>
    <p class="blk-note">열다섯 칸의 채움률이 갈립니다. 열 칸은 100%, 아세틸렌은 96.7%인데
      <b>컴프레서·샌드기·진공매몰기·핀덱스 네 칸만 90.0%</b>입니다.
      그리고 <b>이 네 칸이 비어 있는 876줄은 서로 정확히 같은 줄</b>입니다.
      네 칸을 함께 비웠다는 뜻입니다.</p>
    <p class="blk-note">그 876줄의 인허가일자를 보면 <b>2015년 3월 11일에서 끊깁니다.</b></p>
    <div class="cut">
      <div class="side"><span class="n">876</span>
        <span class="l">그날까지 등록한 5,583곳 중</span>
        <span class="s">15.7%가 네 칸을 비웠다</span></div>
      <div class="mid">2015-03-11</div>
      <div class="side on"><span class="n">0</span>
        <span class="l">그날 뒤에 등록한 3,185곳 중</span>
        <span class="s">비운 곳이 하나도 없다</span></div>
    </div>
    <p class="blk-note" style="margin-top:26px">그날 뒤로는 <b>예외가 없습니다.</b>
      서식이 바뀌었는지, 채우는 규칙이 생겼는지, 시스템이 빈칸을 막았는지 —
      <b>무엇이 바뀌었는지는 데이터에 없습니다.</b> 바뀐 날짜만 보입니다.</p>
    <p class="blk-note" style="margin-top:22px">아세틸렌 칸은 사정이 다릅니다.
      빈칸 289건이 2026년까지 흩어져 있고, 그중 287건은 위 네 칸과 겹치지 않습니다.
      이쪽은 그냥 안 적은 것으로 보입니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>이름은 거의 다 「치과기공소」</h2><span>4,654가지</span></div>
    <p class="blk-note">상호는 4,654가지이고 그중 <b>3,331개가 딱 한 번만</b> 쓰였습니다.
      그런데 <b>8,097곳(92.3%)이 상호에 「기공소」를 넣었습니다.</b>
      앞에 붙는 두 글자만 다른 셈입니다 — 수, 하나, 미소, 다온, 우리, 미래.
      「덴탈」이나 「덴털」을 쓴 곳은 406곳입니다.</p>
    <div class="two">
      <div>
        <p class="list-lab">가장 흔한 상호</p>
        {{names}}
      </div>
      <div>
        <p class="list-lab">어디에 있나</p>
        {{sido}}
        <p class="blk-note" style="margin-top:16px">서울에 <b>28.9%</b>가 몰려 있습니다.</p>
      </div>
    </div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>2012년이 꼭대기였다</h2><span>연도별 신규 등록</span></div>
    <p class="blk-note">2012년 한 해에 <b>476곳</b>이 새로 등록했고, 2026년에는 107곳입니다.
      지금까지 등록된 8,768곳 중 <b>영업 중인 곳은 4,661곳(53.2%)</b>입니다.
      버틴 기간의 가운뎃값은 <b>3.90년</b>입니다.</p>
    <div class="cols">{{ycols}}</div>
    <div class="axis"><span class="first">1988</span><span style="left:50%">2007</span><span class="last" style="left:100%">2026</span></div>

    <div class="flaws" style="margin-top:48px">
      <div class="flaw"><span class="h">126</span>
        <p class="b">기계를 126대 가진 곳이 있다.</p>
        <p class="c">한 곳의 기계 총합 가운뎃값은 17대입니다.</p></div>
      <div class="flaw"><span class="h">111</span>
        <p class="b">샌드기를 111대 가졌다고 적힌 곳.</p>
        <p class="c">샌드기 칸의 가운뎃값은 1대입니다. 다른 칸의 최대값은 대개 스물 안팎입니다.</p></div>
      <div class="flaw"><span class="h">0종</span>
        <p class="b">기계가 한 대도 없다고 적힌 기공소가 3곳.</p>
        <p class="c">열다섯 칸을 모두 0으로 두었습니다.</p></div>
      <div class="flaw"><span class="h">39자</span>
        <p class="b">가장 긴 상호는 한글과 영문을 함께 적었다.</p>
        <p class="c">「워너비 디지털 덴탈랩(Wannabe digital dental lab)」입니다.
          같은 이름을 두 번 적은 셈입니다.</p></div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제15호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>치과기공소</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 8,768행 기준<br>개별 업소의 영업 내용은 다루지 않았습니다. 등록된 값만 옮겼습니다.</span>
  </div>
</footer>

<div class="tip" id="tip"></div>
<script>
/* 모든 값은 원본 CSV 8,768행에서 계산했습니다. scripts/analyze_dental.py 로 재현됩니다. */

const io = new IntersectionObserver(function (es) {
  es.forEach(function (e) {
    if (!e.isIntersecting) return;
    e.target.querySelectorAll('.bar').forEach(function (b, n) {
      setTimeout(function () { b.style.width = b.dataset.w + '%'; }, n * 45);
    });
    io.unobserve(e.target);
  });
}, { threshold: .25 });
document.querySelectorAll('.hbars').forEach(function (el) { io.observe(el); });

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
    "mlist": mlist,
    "one": hbars(ONE, unit="%", cls="wide"),
    "kinds": hbars(KINDS, cls="wide"),
    "names": monoli(NAMES),
    "sido": hbars(SIDO, cls="wide"),
    "ycols": ycols,
}
body = BODY
for k, v in values.items():
    body = body.replace("{{" + k + "}}", v)
assert "{{" not in body

out_dir = ROOT / "dental-lab"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + body + "</script>\n",
               encoding="utf-8")
print("dental-lab/index.html written:", f"{out.stat().st_size:,}", "bytes")
