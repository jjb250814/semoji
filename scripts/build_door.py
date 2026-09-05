"""
제13호 「직권말소」(door-to-door/index.html) 조립기.

공용 CSS는 barbershop/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_door.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_door.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "barbershop" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("방문판매업 114,172곳 중 영업 중인 곳은 14.8%뿐이다. "
        "36,860곳은 그만둔다는 말도 없이 사라져서 관청이 대신 등록을 지웠다.")

HEAD = """<title>직권말소</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/door-to-door/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="직권말소 — 세모지 제13호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/door-to-door/">
<meta property="og:image" content="https://semoji.net/og/door-to-door.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="직권말소 — 세모지 제13호 열람실">
<meta name="twitter:card" content="summary_large_image">
<meta name="naver-site-verification" content="e1aa1ef1b15b68297398065f83c4c5a96d1f3d0d" />
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5277473094749097"
     crossorigin="anonymous"></script>
<link rel="icon" href="/favicon.ico" sizes="48x48 32x32 16x16">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@400;600;800&family=IBM+Plex+Sans+KR:wght@300;400;500;600&family=Nanum+Gothic+Coding:wght@400;700&display=swap">
""" % {"d": DESC}

EXTRA_STYLE = """<style>
/* 제13호 전용 */
.end-box{padding:36px var(--pad) 32px;margin:66px 0 0}
.end-lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;color:var(--muted);margin:0 0 22px}
.end-word{font-family:var(--f-display);font-weight:800;color:var(--seal-ink);
  font-size:clamp(40px,9vw,78px);line-height:1;letter-spacing:-.03em}
.end-say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.end-say b{font-weight:500;color:var(--ink)}
.two{display:grid;gap:30px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-top:8px}
.mono-li{border-top:1px solid var(--rule);font-family:var(--f-mono);font-size:13px}
.mono-li div{display:flex;justify-content:space-between;gap:14px;padding:8px 0;
  border-bottom:1px solid var(--rule-2);font-variant-numeric:tabular-nums}
.mono-li b{font-weight:400;color:var(--ink)}
.mono-li span{color:var(--muted)}
.hbars.wide .hrow{grid-template-columns:minmax(112px,158px) 1fr minmax(72px,auto)}
@media (max-width:560px){.hbars.wide .hrow{grid-template-columns:1fr auto}}
/* 수명 견주기 */
.lifebars{border-top:1px solid var(--rule);margin-top:6px}
.lifebars div{display:grid;grid-template-columns:minmax(78px,110px) 1fr minmax(58px,auto);
  gap:14px;align-items:center;padding:9px 0;border-bottom:1px solid var(--rule-2)}
.lifebars .cat{font-size:14px}
.lifebars .track{background:var(--bar-track);height:20px;display:block}
.lifebars .bar{display:block;height:100%;background:var(--bar-neutral);width:0;
  transition:width .8s cubic-bezier(.2,.8,.2,1)}
.lifebars .on .bar{background:var(--seal)}
.lifebars .on .cat{font-weight:600}
.lifebars .val{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);text-align:right;
  font-variant-numeric:tabular-nums}
.nine{font-family:var(--f-mono);font-size:clamp(15px,3.2vw,26px);color:var(--seal-ink);
  background:var(--card);border:1px solid var(--rule);padding:16px;margin:14px 0 0;
  overflow-x:auto;letter-spacing:.04em;font-weight:700}
</style>"""

# --- 숫자 (analyze_door.py 출력과 대조) ---
STATES = [("폐업처리", 48558), ("직권말소", 32266), ("정상영업", 16823),
          ("타시군구이관", 11500), ("직권취소", 4594), ("휴업처리", 341),
          ("타시군구전입", 44), ("영업재개", 25)]
LIFE = [("방문판매업", 1.85), ("PC방", 3.10), ("자판기", 5.31), ("노래방", 9.50)]
FILLED = [("자본금", 22.3), ("자산규모", 22.5), ("부채총액", 22.1)]
ZERO = [("부채총액", 54.3), ("자산규모", 20.5), ("자본금", 13.3)]
NAMES = [("아모레카운셀러", 259), ("르네셀", 228), ("웰빙플러스", 218), ("해피월드", 200),
         ("윤선생영어교실", 191), ("마임", 170), ("알로에마임", 127), ("인셀덤", 121),
         ("유니베라", 120), ("마더코아", 109)]
WORDS = [("주식회사", 8290), ("인셀덤", 1461), ("마임", 888), ("대리점", 612),
         ("윤선생영어교실", 498), ("유니베라", 430), ("에치와이", 399), ("코리아", 364)]
YEARS = [(1996, 1892), (1997, 1038), (1998, 1460), (1999, 1790), (2000, 1873),
         (2001, 3006), (2002, 4254), (2003, 3797), (2004, 3935), (2005, 4971),
         (2006, 4651), (2007, 6164), (2008, 5880), (2009, 6790), (2010, 6303),
         (2011, 5801), (2012, 5088), (2013, 4464), (2014, 3949), (2015, 4585),
         (2016, 4149), (2017, 4239), (2018, 3906), (2019, 4545), (2020, 3606),
         (2021, 2774), (2022, 2821), (2023, 2184), (2024, 1756), (2025, 1463),
         (2026, 878)]


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


lifetop = max(v for _, v in LIFE)
lifebars = '<div class="lifebars">' + "".join(
    '<div class="%s"><span class="cat">%s</span>'
    '<span class="track"><span class="bar" data-w="%.1f"></span></span>'
    '<span class="val">%.2f년</span></div>' % ("on" if k == "방문판매업" else "",
                                              k, v / lifetop * 100, v)
    for k, v in LIFE) + "</div>"

ymax = max(v for _, v in YEARS)
ycols = "".join(
    '<div class="col%s" style="height:%.1f%%" data-t="%d년 %s곳"></div>'
    % (" peak" if y == 2009 else "", v / ymax * 100, y, f"{v:,}")
    for y, v in YEARS)

BODY = """
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제13호 열람실</span>
    <span>원자료 <b>방문판매업</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제13호 열람실 · 전국 방문판매업 등록 기록</p>
    <h1>직권<span class="or">말소</span></h1>
    <p class="lede">
      방문판매업으로 등록한 곳이 <b>114,172곳</b>입니다. 그중 지금도 영업 중인 곳은
      <b>16,913곳(14.8%)</b>뿐입니다. 나머지는 사라졌는데,
      절반쯤은 <b>그만둔다는 말조차 하지 않았습니다.</b>
      신고 없이 없어진 곳을 관청이 대신 지우는데, 그 처리에 붙는 이름이 「직권말소」입니다.
      <b>36,860곳</b>이 그렇게 지워졌습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">114,172</span><span class="l">등록된 방문판매업체</span><span class="s">1996년 이후 전체 기록</span></div>
      <div class="fig hot"><span class="n">14.8%</span><span class="l">아직 영업 중</span><span class="s">16,913곳</span></div>
      <div class="fig hot"><span class="n">32,266</span><span class="l">직권말소</span><span class="s">관청이 대신 지운 것</span></div>
      <div class="fig"><span class="n">1.85년</span><span class="l">버틴 기간 중앙값</span><span class="s">셋에 하나는 1년을 못 넘겼다</span></div>
    </div>
  </div>

  <article class="form end-box">
    <span class="form-label">상세영업상태</span>
    <p class="end-lab">어떻게 끝났는지 적는 칸. 답은 여덟 가지다.</p>
    <div><span class="end-word">직권말소</span></div>
    <p class="end-say"><b>32,266곳.</b> 폐업 신고를 하지 않고 없어져서,
      관청이 직권으로 등록을 지웠다는 뜻입니다.
      여기에 「직권취소」 4,594곳을 더하면 <b>36,860곳</b>이 됩니다.</p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>어떻게 끝났나</h2><span>114,172곳</span></div>
    <p class="blk-note">스스로 폐업을 신고한 곳이 48,558곳,
      말없이 사라져 관청이 지운 곳이 36,860곳입니다.
      <b>끝을 스스로 말한 쪽과 말하지 않은 쪽이 거의 반반입니다.</b>
      「타시군구이관」 11,500곳은 사라진 게 아니라 관할이 옮겨간 것입니다.</p>
    {{states}}
    <p class="blk-note" style="margin-top:26px">한 번 접었다가 다시 연 곳도 있습니다.
      <b>「영업재개」 25곳</b>입니다. 재개업일자가 적힌 곳으로 넓혀 세면 1,625곳입니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>1년 10개월</h2><span>버틴 기간 중앙값</span></div>
    <p class="blk-note">문 닫은 날이 적힌 56,621곳으로 계산하면 가운뎃값이 <b>676일</b>,
      1년 10개월입니다. <b>18,844곳(33.3%)은 1년을 못 넘겼고,
      10,504곳(18.6%)은 6개월도 못 채웠습니다.</b>
      등록한 날 바로 사라진 곳도 384곳 있습니다.</p>
    {{lifebars}}
    <p class="blk-note" style="margin-top:26px">세모지가 지금까지 센 업종 가운데
      <b>가장 빨리 사라집니다.</b> 노래방의 5분의 1입니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>신고서가 재무제표를 묻는다</h2><span>자본금 · 자산규모 · 부채총액</span></div>
    <p class="blk-note">방문판매업 신고서에는 다른 업종에 없는 칸이 셋 있습니다.
      <b>자본금이 얼마인지, 자산이 얼마인지, 빚이 얼마인지</b>를 적게 합니다.
      가게를 열 때 재무 상태를 밝히라는 것입니다.
      다만 <b>채운 곳은 다섯에 하나 남짓</b>입니다.</p>
    <div class="two">
      <div>
        <p class="end-lab">칸을 채운 비율</p>
        {{filled}}
      </div>
      <div>
        <p class="end-lab">채운 곳 가운데 「0원」이라 적은 비율</p>
        {{zero}}
      </div>
    </div>
    <p class="blk-note" style="margin-top:30px"><b>빚이 0원이라고 적은 곳이 절반을 넘습니다</b>(13,717곳).
      부채총액 칸의 가운뎃값은 아예 0원입니다. 반대로 <b>자산보다 빚이 많다고 적은 곳도
      2,072곳</b> 있습니다. 자본금은 0인데 자산은 있다고 적은 곳이 211곳,
      빚을 <b>1원</b>이라 적은 곳이 253곳입니다.</p>
    <p class="blk-note" style="margin-top:22px">세 칸의 가장 큰 값은 모두 같습니다.
      <b>9를 열다섯 번 적은 것</b>입니다. 각 칸에 한 곳씩 있습니다.</p>
    <div class="nine">999,999,999,999,999원 &nbsp;&nbsp;≈ 1,000조원</div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>회사가 아니라 사람의 이름</h2><span>84,012가지</span></div>
    <p class="blk-note">상호는 84,012가지이고 그중 <b>72,253개는 딱 한 번만</b> 쓰였습니다.
      가장 흔한 이름은 <b>「아모레카운셀러」</b> 259곳입니다.
      「카운셀러」가 들어간 상호가 393곳 있습니다 —
      <b>회사가 아니라 방문판매원 한 사람 한 사람이 따로 등록한 것</b>으로 보입니다.
      「주식회사」가 들어간 상호는 8,290곳뿐입니다.</p>
    <div class="two">
      <div>
        <p class="end-lab">가장 흔한 상호</p>
        {{names}}
      </div>
      <div>
        <p class="end-lab">상호에 자주 들어간 낱말</p>
        {{words}}
      </div>
    </div>
    <p class="blk-note" style="margin-top:26px">화장품, 건강식품, 학습지.
      방문판매라는 말이 무엇을 팔았는지가 이름에 그대로 남아 있습니다.
      <b>여기 적은 이름은 전체 등록 기록에서 흔한 순으로 뽑은 것이고,
      위의 폐업·말소 숫자와는 엮지 않았습니다.</b></p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>2009년이 꼭대기였다</h2><span>연도별 신규 등록</span></div>
    <p class="blk-note">2009년 한 해에 <b>6,790곳</b>이 새로 등록했습니다.
      그 뒤로 계속 줄어 2026년에는 878곳입니다.
      초인종을 누르는 일이 그만큼 줄었습니다.</p>
    <div class="cols">{{ycols}}</div>
    <div class="axis"><span class="first">1996</span><span style="left:50%">2011</span><span class="last" style="left:100%">2026</span></div>

    <div class="flaws" style="margin-top:48px">
      <div class="flaw"><span class="h">1900</span>
        <p class="b">1900년에 등록한 것으로 적힌 곳이 154곳.</p>
        <p class="c">가장 긴 수명이 116년으로 계산되는 것도 이 때문입니다.
          방문판매업 등록 제도는 1990년대에 자리를 잡았습니다.</p></div>
      <div class="flaw"><span class="h">384</span>
        <p class="b">등록한 날에 문을 닫은 곳.</p>
        <p class="c">인허가일자와 폐업일자가 같습니다. 취소한 것인지 잘못 적은 것인지는
          데이터에 없습니다.</p></div>
      <div class="flaw"><span class="h">1원</span>
        <p class="b">빚이 1원이라고 적은 곳이 253곳.</p>
        <p class="c">0을 적기 싫어서인지, 칸을 비울 수 없어서인지는 알 수 없습니다.</p></div>
      <div class="flaw"><span class="h">22%</span>
        <p class="b">재무 칸을 채운 곳은 다섯에 하나뿐이다.</p>
        <p class="c">나머지 89,000여 곳은 비워 두었습니다.
          <b>여기 적은 비율은 모두 「답을 적은 곳」만 놓고 센 것입니다.</b></p></div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제13호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>방문판매업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 114,172행 기준<br>개별 업체의 영업 내용은 다루지 않았습니다. 상호는 폐업·말소 기록과 엮지 않았습니다.</span>
  </div>
</footer>

<div class="tip" id="tip"></div>
<script>
/* 모든 값은 원본 CSV 114,172행에서 계산했습니다. scripts/analyze_door.py 로 재현됩니다. */

const io = new IntersectionObserver(function (es) {
  es.forEach(function (e) {
    if (!e.isIntersecting) return;
    e.target.querySelectorAll('.bar').forEach(function (b, n) {
      setTimeout(function () { b.style.width = b.dataset.w + '%'; }, n * 45);
    });
    io.unobserve(e.target);
  });
}, { threshold: .25 });
document.querySelectorAll('.hbars, .lifebars').forEach(function (el) { io.observe(el); });

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
    "states": hbars(STATES, cls="wide"),
    "lifebars": lifebars,
    "filled": hbars(FILLED, unit="%", cls="wide"),
    "zero": hbars(ZERO, unit="%", cls="wide"),
    "names": monoli(NAMES),
    "words": hbars(WORDS, cls="wide"),
    "ycols": ycols,
}
body = BODY
for k, v in values.items():
    body = body.replace("{{" + k + "}}", v)
assert "{{" not in body

out_dir = ROOT / "door-to-door"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + body + "</script>\n",
               encoding="utf-8")
print("door-to-door/index.html written:", f"{out.stat().st_size:,}", "bytes")
