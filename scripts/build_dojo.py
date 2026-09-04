"""
제20호 「용인대」(dojo/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_dojo.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_dojo.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("전국 체육도장 32,838곳 중 4,588곳의 이름에 대학 이름이 들어 있다. "
        "「용인대」만 2,322곳이고, 태권도장은 넷 중 하나가 자격을 간판에 적는다.")

HEAD = """<title>용인대</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/dojo/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="용인대 — 세모지 제20호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/dojo/">
<meta property="og:image" content="https://semoji.net/og/dojo.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="용인대 — 세모지 제20호 열람실">
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
/* 제20호 전용 */
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
.creds{border-top:1px solid var(--rule);margin-top:22px}
.creds div{display:grid;grid-template-columns:minmax(0,1fr) minmax(84px,auto) minmax(74px,auto);
  gap:14px;padding:12px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.creds .w{font-family:var(--f-display);font-weight:600;font-size:16px}
.creds div.on .w{color:var(--seal-ink)}
.creds .c,.creds .p{font-family:var(--f-mono);font-size:12.5px;text-align:right;
  font-variant-numeric:tabular-nums}
.creds .c{color:var(--ink-2)}
.creds .p{color:var(--muted)}
.creds .hd{border-bottom:1px solid var(--rule)}
.creds .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;color:var(--muted)}
.creds .sum{border-bottom:0;border-top:1.5px solid var(--ink);margin-top:4px}
.creds .sum .w{font-weight:800}
.creds .sum .c{color:var(--seal-ink);font-weight:700}
.proof{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
  border-top:1px solid var(--rule);margin-top:22px}
.proof > div{padding:22px 16px 20px 0;border-right:1px solid var(--rule-2)}
.proof > div:last-child{border-right:0}
.proof .l{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--muted)}
.proof .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(24px,4vw,34px);line-height:1;margin-top:12px;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.proof > div.on .n{color:var(--seal-ink)}
.proof .s{display:block;font-size:12.5px;color:var(--muted);font-weight:300;margin-top:10px}
.sports{border-top:1px solid var(--rule);margin-top:6px}
.sports div{display:grid;grid-template-columns:64px minmax(0,1fr) minmax(96px,auto);
  gap:14px;padding:12px 0;border-bottom:1px solid var(--rule-2);align-items:center}
.sports .nm{font-family:var(--f-display);font-weight:600;font-size:16px}
.sports div.on .nm{color:var(--seal-ink)}
.sports .track{display:block;height:16px;background:var(--rule-2);position:relative}
.sports .bar{display:block;height:100%;background:var(--ink-2);width:0;
  transition:width .7s cubic-bezier(.2,.9,.3,1)}
.sports div.on .bar{background:var(--seal)}
.sports .val{font-family:var(--f-mono);font-size:12.5px;color:var(--muted);
  text-align:right;font-variant-numeric:tabular-nums}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제20호 열람실</span>
    <span>원자료 <b>체육도장업</b> · LOCALDATA · 2026-09-04 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제20호 열람실 · 체육도장업 인허가</p>
    <h1>용인대</h1>
    <p class="lede">
      전국 체육도장 <b>32,838곳</b>의 이름을 세어 봤습니다. 가장 많이 등장하는
      고유명사는 지역도 사람 이름도 아니었습니다. <b>대학 이름</b>입니다.
      「용인대」가 <b>2,322곳</b>, 「경희대」가 1,491곳.
      간판이 곧 <b>관장의 이력서</b>입니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">32,838</span><span class="l">체육도장</span><span class="s">1971년 이후 · 영업 중 16,653곳</span></div>
      <div class="fig hot"><span class="n">2,322</span><span class="l">이름에 「용인대」</span><span class="s">7.07% · 열넷 중 하나</span></div>
      <div class="fig"><span class="n">16.7%</span><span class="l">자격을 적은 도장</span><span class="s">5,470곳</span></div>
      <div class="fig hot"><span class="n">25.7%</span><span class="l">태권도장만 보면</span><span class="s">검도는 0.8%</span></div>
    </div>
  </div>

  <article class="form">
    <span class="form-label">먼저 확인한 것 · 「용인대」는 학교인가 지명인가</span>
    <p class="q-text" style="margin-top:20px">용인시에 몰려 있다면 이 이야기는 통째로 틀린다</p>
    <div class="proof">
      <div class="on"><span class="l">용인대 도장</span><span class="n">2,322</span><span class="s">전국</span></div>
      <div><span class="l">주소에 ‘용인’</span><span class="n">136</span><span class="s">5.9%뿐</span></div>
      <div><span class="l">경기</span><span class="n">1,064</span><span class="s">서울 327 · 인천 200</span></div>
      <div><span class="l">대전 · 충남 · 경북</span><span class="n">274</span><span class="s">전국에 흩어져 있다</span></div>
    </div>
    <p class="say">
      용인대가 붙은 도장 2,322곳 가운데 <b>주소에 ‘용인’이 들어간 곳은 136곳(5.9%)뿐</b>입니다.
      나머지는 경기·서울·인천·대전·충남·경북에 흩어져 있습니다.
      <b>지명이 아니라 학교 이름입니다.</b>
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>간판에 적는 자격</h2><span>겹치지 않게 센 값</span></div>
    <p class="blk-note">
      앞에서 잡힌 도장은 뒤에서 다시 세지 않았습니다.
      대학 이름이 가장 많고, 그다음이 「국가대표」, 「석사·박사」, 「올림픽·금메달」입니다.
      <b>여섯 곳 중 한 곳</b>이 이름 안에 무언가를 증명해 두었습니다.
    </p>
    <div class="creds" id="creds"></div>
    <p class="say">
      낱말 하나씩 겹쳐 세면 「용인대」 2,322 · 「경희대」 1,491 · 「석사」 727 ·
      「국가대표」 594 · 「한국체대」 351 · 「올림픽」 132 · 「금메달」 72 입니다.
      <b>「석사」가 727곳입니다.</b> 태권도장 간판에 대학원 학위가 적혀 있습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>태권도만 그런다</h2><span>종목별 자격 표기 비율</span></div>
    <p class="blk-note">
      종목이 적힌 19,741곳을 갈라 보면 차이가 뚜렷합니다.
      <b>태권도장은 넷 중 하나(25.7%)</b>가 이름에 자격을 적는데,
      <b>검도장은 901곳 중 일곱 곳(0.8%)</b>뿐입니다. 레슬링은 한 곳도 없습니다.
    </p>
    <div class="sports" id="sports"></div>
    <p class="say">
      같은 「체육도장업」이라는 한 칸에 묶여 있지만 이름 짓는 방식은 종목마다 다릅니다.
      <b>왜 태권도만 그런지는 데이터가 말해 주지 않습니다.</b>
      확실한 것은 비율이 서른 배 넘게 벌어진다는 사실뿐입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      이 페이지는 <b>도장 이름을 하나도 옮기지 않았습니다.</b> 상호가 공개 데이터라 해도
      「○○대 석사 태권도」 같은 이름은 특정 관장의 학력을 그대로 가리킵니다.
      <b>세는 것과 지목하는 것은 다릅니다.</b>
      그리고 자격을 내거는 것은 흠이 아니라 정상적인 영업입니다.
      세모지가 센 것은 <b>그런 관행이 있다</b>는 사실이지, 그래서 어떻다는 이야기가 아닙니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>무슨 도장이 있나</h2><span>업태구분명</span></div>
    <p class="blk-note">
      종목 칸은 <b>39.9%가 비어 있습니다</b>(13,097곳). 채워진 19,741곳만 놓고 보면
      <b>태권도가 65.5%</b>로 셋 중 둘이고, 권투 14.9%, 합기도 7.6%,
      유도 5.5%, 검도 4.6%가 뒤를 잇습니다.
    </p>
    <div class="hbars" id="kinds"></div>
    <p class="say">
      전국 32,838곳 중 <b>공립은 35곳</b>뿐이고 나머지 32,803곳이 사립입니다.
      「지도자수」 칸은 절반 넘게 비어 있는데, 적힌 것 중 <b>14,023곳이 「1」</b>입니다.
      대부분 관장 혼자 하는 곳입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다. 상호는 옮기지 않습니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">업태구분명 「야구종목」</span>
        <p class="b">체육도장업으로 등록된 곳 가운데 종목이 「야구종목」인 데가 한 곳 있습니다.</p>
        <p class="c">1989년에 신고했고 아직 영업 중입니다. 태권도·권투·합기도·유도·검도·레슬링·우슈 사이에 야구가 하나 끼어 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">종목 칸 빈칸 39.9%</span>
        <p class="b">13,097곳은 무슨 도장인지 적혀 있지 않습니다.</p>
        <p class="c">그래서 이 페이지의 종목 비율은 전체가 아니라 채워진 19,741곳만 놓고 낸 값입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">지도자수 「0」</span>
        <p class="b">가르치는 사람이 0명이라고 적은 도장이 523곳 있습니다.</p>
        <p class="c">칸 자체가 17,944곳에서 비어 있습니다. 한 곳은 「11」이라고 적었습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">51년째 영업</span>
        <p class="b">폐업한 15,872곳의 영업 기간 중앙값은 7.9년, 가장 긴 곳은 51.3년입니다.</p>
        <p class="c">가장 이른 신고는 1971년입니다. 가장 긴 도장 이름은 51자입니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제20호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>체육도장업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-04 내려받은 32,838행 기준<br>개별 도장의 지도 자격이나 실제 경력은 확인하지 않았습니다. 등록된 상호에 적힌 낱말만 셌습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 32,838행에서 계산했습니다. scripts/analyze_dojo.py 로 재현됩니다. */

/* 겹치지 않게 센 자격 [분류, 곳수, 비율] */
const CREDS = [
 ["대학 이름", 4588, 13.97], ["국가대표", 448, 1.36],
 ["석사 · 박사", 284, 0.86], ["올림픽 · 금메달", 150, 0.46]
];
const CREDS_SUM = [5470, 16.66];

/* 종목별 자격 표기 [종목, 전체, 자격표기, 비율] */
const SPORTS = [
 ["태권도", 12931, 3322, 25.7], ["유도", 1084, 176, 16.2],
 ["합기도", 1501, 86, 5.7], ["권투", 2935, 95, 3.2],
 ["우슈", 188, 5, 2.7], ["검도", 901, 7, 0.8], ["레슬링", 200, 0, 0.0]
];

/* 종목 구성 [종목, 곳수, 비율] */
const KINDS = [
 ["태권도", 12931, 65.5], ["권투", 2935, 14.9], ["합기도", 1501, 7.6],
 ["유도", 1084, 5.5], ["검도", 901, 4.6], ["레슬링", 200, 1.0],
 ["우슈", 188, 1.0], ["야구종목", 1, 0.0]
];

const $ = s => document.querySelector(s);
const nf = n => n.toLocaleString("ko-KR");

const tip = $("#tip");
function bindTips(){
  document.querySelectorAll("[data-t]").forEach(el => {
    el.addEventListener("mousemove", e => {
      tip.textContent = el.dataset.t; tip.classList.add("on");
      tip.style.left = e.clientX + "px"; tip.style.top = e.clientY + "px";
    });
    el.addEventListener("mouseleave", () => tip.classList.remove("on"));
  });
}

$("#creds").innerHTML =
  '<div class="hd"><span class="w">간판에 적힌 것</span><span class="c">곳</span>' +
  '<span class="p">비율</span></div>' +
  CREDS.map(([w, c, p]) =>
    '<div' + (w === "대학 이름" ? ' class="on"' : "") +
    ' data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
    '<span class="w">' + w + '</span>' +
    '<span class="c">' + nf(c) + '</span>' +
    '<span class="p">' + p.toFixed(2) + '%</span></div>').join("") +
  '<div class="sum"><span class="w">자격을 적은 도장</span>' +
  '<span class="c">' + nf(CREDS_SUM[0]) + '</span>' +
  '<span class="p">' + CREDS_SUM[1] + '%</span></div>';

const maxS = SPORTS[0][3];
$("#sports").innerHTML = SPORTS.map(([nm, tot, c, p]) =>
  '<div' + (nm === "태권도" ? ' class="on"' : "") +
  ' data-t="' + nm + ' — ' + nf(tot) + '곳 중 ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="nm">' + nm + '</span>' +
  '<span class="track"><span class="bar" data-w="' +
    (p / maxS * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(c) + '</span></div>').join("");

const maxK = KINDS[0][1];
$("#kinds").innerHTML = KINDS.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxK * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p + '% · ' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "dojo"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("dojo/index.html 작성 완료 — %s bytes" % f"{out.stat().st_size:,}")
