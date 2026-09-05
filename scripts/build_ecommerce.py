"""
제26호 「카다로그」(ecommerce/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_ecommerce.py 의 출력(data/분석결과_통신판매업.txt)과
대조한 값이다.

사용법:
    python scripts/build_ecommerce.py

※ 이 페이지에서 지킨 선

1. **「카다로그가 늘었다」를 「카탈로그 판매가 늘었다」로 단정하지 않는다.**
   읽기 두 가지를 나란히 둔다. 원본에 이유가 없다.

2. **판매 수단은 여러 개를 고를 수 있다.** 합계가 100%를 넘는다는 사실을
   본문에 밝힌다.

3. **상호 2,173,792가지를 옮기지 않는다.** 흔한 상호 몇 개만, 그것도
   가게를 특정하지 못하는 짧은 이름만 예로 든다.
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("통신판매업 3,096,399곳의 「판매방식명」 칸에는 아직 「카다로그」와 「신문잡지」가 "
        "선택지로 남아 있다. 81,567곳이 카다로그를 골랐고, 1,415곳은 인터넷을 빼고 "
        "카다로그만 골랐다. 그 비율은 1999년보다 2010년대에 더 높다.")

HEAD = """<title>카다로그</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/ecommerce/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="카다로그 — 세모지 제26호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/ecommerce/">
<meta property="og:image" content="https://semoji.net/og/ecommerce.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="카다로그 — 세모지 제26호 열람실">
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
/* 제26호 전용 */
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
.split{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
  border-top:1px solid var(--rule);margin-top:22px}
.split > div{padding:22px 16px 20px 0;border-right:1px solid var(--rule-2)}
.split > div:last-child{border-right:0}
.split .l{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--muted)}
.split .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(24px,4vw,34px);line-height:1;margin-top:12px;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.split > div.on .n{color:var(--seal-ink)}
.split .s{display:block;font-size:12.5px;color:var(--muted);font-weight:300;margin-top:10px}
/* 체크박스 */
.boxes{border-top:1px solid var(--rule);margin-top:6px}
.boxes div{display:grid;grid-template-columns:minmax(84px,auto) minmax(0,1fr) minmax(128px,auto);
  gap:14px;padding:14px 0;border-bottom:1px solid var(--rule-2);align-items:center}
.boxes .nm{font-family:var(--f-display);font-weight:600;font-size:16px}
.boxes div.on .nm{color:var(--seal-ink)}
.boxes .track{display:block;height:16px;background:var(--rule-2);position:relative}
.boxes .bar{display:block;height:100%;background:var(--ink-2);width:0;
  transition:width .7s cubic-bezier(.2,.9,.3,1)}
.boxes div.on .bar{background:var(--seal)}
.boxes .val{font-family:var(--f-mono);font-size:12.5px;color:var(--muted);
  text-align:right;font-variant-numeric:tabular-nums}
/* 연도 교차표 */
.yrs{width:100%;border-collapse:collapse;margin-top:6px;font-variant-numeric:tabular-nums}
.yrs th,.yrs td{padding:11px 8px;border-bottom:1px solid var(--rule-2);text-align:right;
  font-family:var(--f-mono);font-size:12.5px}
.yrs th{color:var(--muted);font-size:10.5px;letter-spacing:.1em;font-weight:400;
  border-bottom:1px solid var(--rule)}
.yrs th:first-child,.yrs td:first-child{text-align:left;color:var(--ink-2)}
.yrs td.hi{color:var(--seal-ink);font-weight:700}
.yrs tbody tr:last-child td{border-bottom:0}
.yrs .sub{color:var(--muted);font-size:10.5px}
/* 조합 목록 */
.combo{border-top:1px solid var(--rule);margin-top:6px}
.combo div{display:grid;grid-template-columns:minmax(0,1fr) minmax(72px,auto);
  gap:12px;padding:11px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.combo .w{font-family:var(--f-mono);font-size:13.5px;word-break:break-word}
.combo div.on .w{color:var(--seal-ink);font-weight:700}
.combo .c{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);text-align:right;
  font-variant-numeric:tabular-nums}
.combo .hd{border-bottom:1px solid var(--rule)}
.combo .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;color:var(--muted)}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제26호 열람실</span>
    <span>원자료 <b>통신판매업</b> · LOCALDATA · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제26호 열람실 · 통신판매업 「판매방식명」</p>
    <h1>카다로그</h1>
    <p class="lede">
      온라인 쇼핑몰을 열려면 통신판매업 신고를 합니다. 그 서식이 묻는
      「어떻게 파느냐」의 선택지에는 아직 <b>「카다로그」와 「신문잡지」</b> 가
      남아 있습니다. <b>81,567곳이 카다로그를 골랐습니다.</b>
    </p>

    <div class="figs">
      <div class="fig"><span class="n">3,096,399</span><span class="l">통신판매업</span><span class="s">세모지가 판 것 중 가장 큼</span></div>
      <div class="fig hot"><span class="n">81,567</span><span class="l">「카다로그」를 고름</span><span class="s">2.76%</span></div>
      <div class="fig hot"><span class="n">1,415</span><span class="l">카다로그만 고름</span><span class="s">인터넷을 안 골랐다</span></div>
      <div class="fig"><span class="n">31</span><span class="l">고른 조합</span><span class="s">수단은 다섯 가지</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>서식이 아직 묻는 것</h2><span>판매방식명 · 채워진 2,960,322곳</span></div>
    <p class="blk-note">
      선택지는 <b>인터넷 · TV홈쇼핑 · 카다로그 · 신문잡지 · 기타</b> 다섯 가지이고
      여러 개를 고를 수 있습니다. 아래 숫자는 <b>겹쳐서 센 값</b>이라
      합계가 100%를 넘습니다.
    </p>
    <div class="boxes" id="boxes"></div>
    <p class="say">
      <b>「카다로그」</b> 는 지금 표기법으로는 「카탈로그」입니다.
      서식에 적힌 철자가 바뀌지 않은 채로 남아 있습니다.
      <b>「신문잡지」</b> 는 신문·잡지 광고를 보고 주문하는 방식입니다.
      둘 다 인터넷 이전의 통신판매 수단인데, <b>지금도 선택지에 있습니다.</b>
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>인터넷을 안 고른 70,978곳</h2><span>조합 15가지</span></div>
    <p class="blk-note">
      통신판매업의 <b>97.60%가 인터넷</b>을 골랐습니다. 그런데 인터넷을
      고르지 않은 곳이 <b>70,978곳(2.40%)</b> 있습니다.
      그중 <b>1,415곳은 「카다로그」 하나만</b>, <b>591곳은 「신문잡지」 하나만</b> 골랐습니다.
    </p>
    <div class="combo" id="combo"></div>
    <p class="say">
      「기타」만 고른 곳이 57,057곳으로 가장 많습니다. 무엇이 기타인지는
      <b>데이터에 없습니다.</b> 그다음이 TV홈쇼핑 9,243곳입니다.
      <b>인터넷 없이 카탈로그로만 파는 곳이 천 곳 넘게 등록되어 있다</b>는 사실이
      이 칸이 아직 살아 있다는 증거입니다.
    </p>
  </section>

  <article class="form">
    <span class="form-label">먼저 확인한 것 · 낡은 선택지는 옛날에 더 많이 골랐나</span>
    <p class="q-text" style="margin-top:20px">카다로그가 옛 수단이라면 오래된 신고일수록 많아야 한다</p>
    <table class="yrs" id="yrs"></table>
    <p class="say">
      <b>반대였습니다.</b> 카다로그를 고른 비율은 1999-2004년 <b>1.35%</b> 에서
      2015-2019년 <b>3.91%</b> 로 <b>세 배 가까이 올랐다가</b>
      2020년대에 2.10%로 떨어집니다. 신문잡지도 같은 모양입니다.
    </p>
    <p class="say">
      <b>읽기가 두 가지입니다.</b> 하나는 <b>체크박스를 여러 개 고르는 습관</b>이
      늘었다는 것 — 온라인 신고가 보편화되면서 해당할 것 같으면 다 고르는
      쪽으로 바뀌었을 수 있습니다. 다른 하나는 <b>실제로 카탈로그를 같이 쓰는
      곳이 늘었다</b>는 것입니다. <b>원본에 답이 없습니다.</b>
      확실한 것은 <b>낡은 선택지가 시간이 갈수록 덜 골라지지는 않았다</b>는 사실뿐입니다.
    </p>
  </article>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      판매 수단은 <b>여러 개를 고를 수 있어</b> 위 비율의 합계는 100%를 넘습니다.
      그리고 <b>판매방식명은 4.4%(136,077곳)가 비어 있어</b>, 비율은 전부 채워진
      2,960,322곳만 놓고 낸 값입니다. 상호 <b>2,173,792가지는 옮기지 않았습니다</b> —
      옮기면 잡학이 아니라 명부입니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>정해진 분류인데 15,354가지</h2><span>업태구분명</span></div>
    <p class="blk-note">
      「업태구분명」은 무엇을 파는지 고르는 칸입니다. 분류가 정해져 있는데
      고유값이 <b>15,354가지</b> 이고 가장 긴 값이 <b>87자</b> 입니다.
      여러 분류를 <b>띄어쓰기로 붙여</b> 적기 때문입니다.
    </p>
    <div class="hbars" id="biz"></div>
    <p class="say">
      가장 많은 것은 <b>「종합몰」 796,630곳(25.7%)</b> 입니다.
      「종합몰 의류/패션/잡화/뷰티」처럼 두 분류를 붙인 값이 60,099곳,
      「종합몰 기타」가 28,144곳 있습니다.
      그리고 <b>「-」 라고만 적은 곳이 136,031곳(4.4%)</b> 입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>넷 중 하나는 문을 닫았다</h2><span>영업상태</span></div>
    <p class="blk-note">
      3,096,399곳 중 영업 중이 <b>1,638,663곳(52.9%)</b>, 폐업이 761,321곳(24.6%)입니다.
      그리고 <b>직권말소가 368,648곳(11.9%)</b> 입니다.
    </p>
    <div class="hbars" id="alive"></div>
    <p class="say">
      <b>제13호 방문판매업의 「직권말소」</b> 가 여기서도 큰 덩어리입니다.
      스스로 폐업 신고를 하지 않아 관청이 지운 것이 <b>열에 하나가 넘습니다.</b>
      「타시군구이관」이 297,556곳(9.6%)인 것도 눈에 띕니다 —
      사업장을 옮기면 기록이 따라 이동합니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다. 상호와 전화번호는 옮기지 않습니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">또 「BBBB」</span>
        <p class="b">상세영업상태코드에 「BBBB」라고 적힌 것이 115건 있습니다.</p>
        <p class="c">제25호 담배소매업에서도 같은 값이 400건 나왔습니다.
          서로 다른 업종의 데이터에 같은 가짜 코드가 들어 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">업태구분명 「-」 136,031</span>
        <p class="b">무엇을 파는지 고르는 칸에 붙임표 하나만 적은 곳이 136,031곳입니다.</p>
        <p class="c">전체의 4.4%입니다. 제19호에서 찾은 「한 글자 답」 신호가
          백만 단위 데이터에서도 그대로 나옵니다.</p>
      </div>
      <div class="flaw">
        <span class="h">코드가 열한 가지</span>
        <p class="b">상세영업상태코드는 01~08 두 자리인데, 「1」 「0」처럼 한 자리인 것도 섞여 있습니다.</p>
        <p class="c">「BBBB」까지 합쳐 열한 가지가 됩니다. 상태 이름은 여덟 가지뿐입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">상호가 65자</span>
        <p class="b">가장 긴 상호는 65자입니다. 고유한 상호는 2,173,792가지입니다.</p>
        <p class="c">가장 많이 쓰인 상호는 「다온」 906곳입니다. 「라온」 523곳,
          「가온」 367곳 — 순우리말 짧은 이름이 몰려 있습니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제26호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>통신판매업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 내려받은 3,096,399행 기준<br>판매 수단은 여러 개를 고를 수 있어 비율의 합계가 100%를 넘습니다. 상호와 전화번호는 옮기지 않았습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 3,096,399행에서 계산했습니다. scripts/analyze_ecommerce.py 로 재현됩니다. */

/* 판매 수단 [수단, 곳수, 비율, 한 가지만 고른 곳] */
const BOXES = [
 ["인터넷", 2889344, 97.60, 2667381],
 ["기타", 214056, 7.23, 57057],
 ["TV홈쇼핑", 92745, 3.13, 9243],
 ["카다로그", 81567, 2.76, 1415],
 ["신문잡지", 52376, 1.77, 591]
];

/* 인터넷을 안 고른 조합 [조합, 건수] */
const COMBO = [
 ["기타", 57057], ["TV홈쇼핑", 9243], ["카다로그", 1415],
 ["카다로그, 기타", 739], ["TV홈쇼핑, 기타", 603], ["신문잡지", 591],
 ["카다로그, 신문잡지, 기타", 325], ["TV홈쇼핑, 카다로그, 신문잡지, 기타", 228],
 ["카다로그, 신문잡지", 224], ["신문잡지, 기타", 220]
];

/* 연도별 [구간, 건수, 카다로그%, 신문잡지%, TV홈쇼핑%, 인터넷%] */
const YRS = [
 ["1999-2004", 23207, 1.35, 0.75, 1.48, 92.69],
 ["2005-2009", 211243, 2.64, 1.76, 2.40, 97.57],
 ["2010-2014", 400400, 3.70, 2.48, 3.27, 98.36],
 ["2015-2019", 663104, 3.91, 2.59, 4.00, 98.19],
 ["2020-2026", 1661961, 2.10, 1.28, 2.87, 97.27]
];

/* 업태구분명 [값, 곳수, 비율] */
const BIZ = [
 ["종합몰", 796630, 25.7], ["의류/패션/잡화/뷰티", 666542, 21.5],
 ["기타", 501802, 16.2], ["건강/식품", 229778, 7.4], ["-", 136031, 4.4],
 ["교육/도서/완구/오락", 65546, 2.1], ["종합몰 의류/패션/잡화/뷰티", 60099, 1.9],
 ["레져/여행/공연", 48287, 1.6], ["가구/수납용품", 35233, 1.1],
 ["컴퓨터/사무용품", 33120, 1.1], ["종합몰 기타", 28144, 0.9]
];

/* 영업상태 [상태, 곳수, 비율] */
const ALIVE = [
 ["정상영업", 1637845, 52.9], ["폐업처리", 761321, 24.6],
 ["직권말소", 368648, 11.9], ["타시군구이관", 297556, 9.6],
 ["직권취소", 21573, 0.7], ["휴업처리", 8638, 0.3]
];

const $ = s => document.querySelector(s);
const nf = n => n.toLocaleString("ko-KR");
const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");

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

const maxB = BOXES[0][1];
$("#boxes").innerHTML = BOXES.map(([nm, c, p, only]) =>
  '<div' + (nm === "카다로그" || nm === "신문잡지" ? ' class="on"' : "") +
  ' data-t="' + nm + ' — ' + nf(c) + '곳 (' + p + '%) · 이것만 고른 곳 ' + nf(only) + '">' +
  '<span class="nm">' + nm + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxB * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(2) + '% · ' + nf(c) + '</span></div>').join("");

$("#combo").innerHTML =
  '<div class="hd"><span class="w">인터넷 없이 고른 조합</span><span class="c">건</span></div>' +
  COMBO.map(([w, c]) =>
    '<div' + (w === "카다로그" || w === "신문잡지" ? ' class="on"' : "") +
    ' data-t="' + esc(w) + ' — ' + nf(c) + '건">' +
    '<span class="w">' + esc(w) + '</span>' +
    '<span class="c">' + nf(c) + '</span></div>').join("");

$("#yrs").innerHTML =
  '<thead><tr><th>인허가 연도</th><th>건수</th><th>카다로그</th><th>신문잡지</th><th>TV홈쇼핑</th><th>인터넷</th></tr></thead><tbody>' +
  YRS.map(([y, n, cat, np, tv, net]) =>
    '<tr><td>' + y + '</td><td><span class="sub">' + nf(n) + '</span></td>' +
    '<td class="hi">' + cat.toFixed(2) + '%</td>' +
    '<td>' + np.toFixed(2) + '%</td><td>' + tv.toFixed(2) + '%</td>' +
    '<td>' + net.toFixed(2) + '%</td></tr>').join("") +
  '</tbody>';

const maxZ = BIZ[0][1];
$("#biz").innerHTML = BIZ.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + esc(w) + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + esc(w) + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxZ * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(c) + '</span></div>').join("");

const maxA = ALIVE[0][1];
$("#alive").innerHTML = ALIVE.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxA * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "ecommerce"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("ecommerce/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
