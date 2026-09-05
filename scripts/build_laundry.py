"""
제27호 「운동화전문세탁업」(laundry/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_laundry.py 의 출력(data/분석결과_세탁소.txt)과
대조한 값이다.

사용법:
    python scripts/build_laundry.py

※ 이 페이지에서 지킨 선

1. **「세탁기 1,326대」를 사실로 쓰지 않는다.** 면적이 29.25제곱미터다.
   흠으로 다루고 상호는 옮기지 않는다.

2. **가게 상호를 개별로 지목하지 않는다.** 흔한 이름만 세어서 옮긴다.

3. **상호의 시대 구분은 제12호 「바버샵」과 같은 모양이라 곁가지로만 둔다.**
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("세탁소 67,398곳의 업종 칸에는 「운동화전문세탁업」이라는 항목이 따로 있다. "
        "1990년대에는 한 곳도 없다가 2002년에 처음 생겨, 2010~2014년에는 새 허가의 "
        "11.17%를 차지했다. 업종이 태어나는 순간이 데이터에 찍혀 있다.")

HEAD = """<title>운동화전문세탁업</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/laundry/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="운동화전문세탁업 — 세모지 제27호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/laundry/">
<meta property="og:image" content="https://semoji.net/og/laundry.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="운동화전문세탁업 — 세모지 제27호 열람실">
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
/* 제27호 전용 */
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
/* 연도 기둥 그래프 */
.years{display:flex;align-items:flex-end;gap:3px;height:170px;margin-top:18px;
  border-bottom:1px solid var(--ink);padding-bottom:0}
.years div{flex:1;position:relative;background:var(--rule-2);min-height:2px;
  transition:height .7s cubic-bezier(.2,.9,.3,1);height:0}
.years div.on{background:var(--seal)}
.ylab{display:flex;gap:3px;margin-top:8px}
.ylab span{flex:1;font-family:var(--f-mono);font-size:9.5px;color:var(--muted);
  text-align:center;overflow:hidden}
/* 표 */
.tb{width:100%;border-collapse:collapse;margin-top:6px;font-variant-numeric:tabular-nums}
.tb th,.tb td{padding:11px 8px;border-bottom:1px solid var(--rule-2);text-align:right;
  font-family:var(--f-mono);font-size:12.5px}
.tb th{color:var(--muted);font-size:10.5px;letter-spacing:.1em;font-weight:400;
  border-bottom:1px solid var(--rule)}
.tb th:first-child,.tb td:first-child{text-align:left;color:var(--ink-2)}
.tb td.hi{color:var(--seal-ink);font-weight:700}
.tb tbody tr:last-child td{border-bottom:0}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제27호 열람실</span>
    <span>원자료 <b>세탁업</b> · LOCALDATA · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제27호 열람실 · 세탁업 「업태구분명」</p>
    <h1>운동화전문세탁업</h1>
    <p class="lede">
      세탁소 <b>67,398곳</b>의 업종 칸에는 <b>운동화만 빠는 가게</b>를 위한
      항목이 따로 있습니다. 1990년대에는 <b>한 곳도 없었습니다.</b>
      2002년에 세 곳으로 시작해, 2010년대 초에는 <b>새 허가의 아홉 중 하나</b>가 됐습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">67,398</span><span class="l">세탁업</span><span class="s">폐업 48,758곳 · 72.3%</span></div>
      <div class="fig hot"><span class="n">2002</span><span class="l">첫 허가</span><span class="s">그해 세 곳</span></div>
      <div class="fig hot"><span class="n">11.17%</span><span class="l">새 허가 중 비중</span><span class="s">2010~2014년</span></div>
      <div class="fig"><span class="n">1,553</span><span class="l">운동화 전문 세탁소</span><span class="s">지금까지 전부</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>업종이 태어난 해</h2><span>업태구분명 · 첫 허가</span></div>
    <p class="blk-note">
      「요즘 늘었다」고 말하기 전에 <b>첫 허가 연도</b>를 봤습니다.
      운동화전문세탁업의 첫 허가는 <b>2002년</b> 입니다. 그 이전에는 없습니다.
      분류가 나중에 붙은 것이 아니라 <b>업종이 그때 생긴 것</b>입니다.
    </p>
    <table class="tb" id="birth"></table>
    <p class="say">
      표의 일반세탁업 첫 허가가 <b>1900년</b>으로 찍힌 것은 날짜 오류입니다 — 그런 값이 3건 있습니다.
      일반세탁업의 중앙값은 <b>1999년</b>, 운동화전문세탁업은 <b>2013년</b> 입니다.
      열네 해 차이입니다. 빨래방업은 첫 허가가 1987년으로 더 이르지만,
      중앙값은 2012년이라 <b>실제로 퍼진 것은 최근</b>입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>2002년 세 곳에서</h2><span>연도별 새 허가</span></div>
    <p class="blk-note">
      2002년 3곳, 2003년 7곳으로 시작해 <b>2010년 142곳</b>으로 정점을 찍고
      내려옵니다. 2025년에는 11곳입니다. <b>한 업종의 처음과 끝이
      한 화면에 들어옵니다.</b>
    </p>
    <div class="years" id="years"></div>
    <div class="ylab" id="ylab"></div>
    <p class="say">
      2000년대 중반에 운동화를 신고 빨래를 맡기는 일이 <b>따로 이름을 가질 만큼</b>
      많아졌다는 뜻입니다. <b>왜 그랬는지는 데이터에 없습니다.</b>
      확실한 것은 <b>행정이 그 변화를 인정해 칸을 하나 만들었다</b>는 사실뿐입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>새로 여는 세탁소의 다섯 중 하나</h2><span>인허가 연도별 구성</span></div>
    <p class="blk-note">
      1990년대에는 새 허가의 <b>99.59%가 일반세탁업</b> 이었습니다.
      2010~2014년에는 <b>76.36%</b> 로 내려가고, 그 자리를
      운동화전문(11.17%)과 빨래방(9.24%)이 채웁니다.
    </p>
    <table class="tb" id="mix"></table>
    <p class="say">
      <b>세탁소가 쪼개진 것입니다.</b> 옷을 다 받던 한 가지 업종이
      운동화 전문과 무인 빨래방으로 갈라졌습니다.
      2020년대에 빨래방 비중이 2.10%로 떨어진 것은
      <b>이미 자리를 잡아 새로 여는 곳이 줄었기 때문일 수도 있고,
      다른 이유일 수도 있습니다.</b> 데이터는 새 허가만 셀 뿐입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>기계 몇 대로 하나</h2><span>세탁기수 · 회수건조기수</span></div>
    <p class="blk-note">
      세탁기 대수를 적는 칸이 있습니다. 채움률은 업종마다 크게 다릅니다 —
      <b>일반세탁업은 37.0%</b> 만 적었는데 <b>운동화전문은 94.2%</b> 가 적었습니다.
      새로 생긴 업종일수록 서식을 꼼꼼히 채웁니다.
    </p>
    <table class="tb" id="mach"></table>
    <p class="say">
      중앙값은 일반세탁업과 운동화전문이 <b>둘 다 1대</b>, 빨래방업이 <b>3대</b> 입니다.
      <b>세탁기가 0대라고 적은 곳이 7,444곳</b> 있습니다.
      받아서 공장에 보내는 가게일 수도 있고, 그냥 안 적은 것일 수도 있습니다.
      <b>0과 빈칸을 구분해 적었다는 것만 확실합니다.</b>
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      <b>세탁기 1,326대짜리 가게는 사실로 쓰지 않았습니다.</b> 그 가게의
      소재지면적이 <b>29.25제곱미터</b>이기 때문입니다. 여덟 평 남짓한 곳에
      세탁기 1,326대는 들어가지 않습니다. <b>흠으로 다루고 상호는 옮기지 않았습니다.</b>
      그리고 <b>세탁기수는 40.0%만 채워져 있어</b>, 중앙값은 적힌 것만 놓고 낸 값입니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>세탁소 · 크리닝 · 런드리</h2><span>상호 25,537가지</span></div>
    <p class="blk-note">
      상호의 <b>40.8%(27,508곳)</b> 가 「세탁소」로 끝납니다.
      「크리닝」이나 「클리닝」이 든 곳이 4,395곳(6.5%),
      「런드리」나 「laundry」가 든 곳은 <b>67곳(0.1%)</b> 뿐입니다.
    </p>
    <div class="hbars" id="names"></div>
    <p class="say">
      <b>「사(社)」로 끝나는 상호가 10,099곳(15.0%)</b> 있습니다.
      「백양사」 430곳, 「현대사」 279곳처럼 <b>가게를 「사」라고 부르던 시절</b>의 이름입니다.
      제12호 이용원에서 본 <b>「서류의 이름과 간판의 이름」</b> 과 같은 자리인데,
      여기서는 <b>같은 간판 안에서 시대가 갈립니다.</b>
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다. 상호와 전화번호는 옮기지 않습니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">여덟 평에 세탁기 1,326대</span>
        <p class="b">세탁기수 최대값은 1,326대입니다. 2006년 허가, 지금은 폐업한 일반세탁업입니다.</p>
        <p class="c">그 가게의 소재지면적은 29.25제곱미터입니다. 세탁기가 10대 넘는 곳은
          전국에 34곳뿐이고, 100대 넘는 곳은 이 한 곳입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">지하 104층</span>
        <p class="b">건물지하층수에 「104」라고 적힌 곳이 한 곳 있습니다.</p>
        <p class="c">「13」이라고 적은 곳도 한 곳 있습니다. 대부분은 0 아니면 1입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">사용시작지하층 · 사용끝지하층</span>
        <p class="b">지하 몇 층부터 몇 층까지 쓰는지 따로 묻는 칸이 있습니다.</p>
        <p class="c">채움률은 42.5%와 24.7%인데, 채워진 값의 96.4%와 94.1%가 「0」입니다.
          지하를 안 쓴다는 뜻을 네 칸에 걸쳐 적고 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">조건부허가신고사유 36건</span>
        <p class="b">전체의 0.1%만 채워진 칸에 32가지 값이 들어 있습니다.</p>
        <p class="c">담당자가 손으로 적은 메모라 원문은 옮기지 않았습니다.
          날짜가 지난 조건이 그대로 남아 있는 것도 있습니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제27호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>세탁업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 내려받은 67,398행 기준<br>가게 상호와 전화번호는 옮기지 않았습니다. 세탁기수는 적힌 40.0%만으로 중앙값을 냈습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 67,398행에서 계산했습니다. scripts/analyze_laundry.py 로 재현됩니다. */

/* 업종 [이름, 곳수, 첫 허가, 중앙값] */
const BIRTH = [
 ["일반세탁업", 63752, 1900, 1999],
 ["운동화전문세탁업", 1553, 2002, 2013],
 ["빨래방업", 1330, 1987, 2012],
 ["세탁업 기타", 757, 1987, 2016]
];

/* 운동화전문 연도별 [연도, 곳수] */
const YEARS = [
 [2002,3],[2003,7],[2004,14],[2005,11],[2006,17],[2007,44],[2008,93],[2009,137],
 [2010,142],[2011,113],[2012,123],[2013,124],[2014,113],[2015,94],[2016,115],
 [2017,79],[2018,68],[2019,47],[2020,34],[2021,49],[2022,43],[2023,31],[2024,30],
 [2025,11],[2026,11]
];

/* 인허가 연도별 구성 [구간, 새 허가, 운동화%, 빨래방%, 일반%] */
const MIX = [
 ["1990-1999", 21052, 0.00, 0.32, 99.59],
 ["2000-2009", 22497, 1.45, 1.36, 96.69],
 ["2010-2014", 5508, 11.17, 9.24, 76.36],
 ["2015-2019", 4090, 9.85, 9.17, 75.92],
 ["2020-2026", 2522, 8.29, 2.10, 80.29]
];

/* 기계 [업종, 채움%, 중앙값, 최대] */
const MACH = [
 ["일반세탁업", 37.0, 1.0, 1326],
 ["운동화전문세탁업", 94.2, 1.0, 9],
 ["빨래방업", 88.2, 3.0, 60],
 ["세탁업 기타", 93.0, 2.0, 15]
];

/* 상호 [분류, 곳수, 비율] */
const NAMES = [
 ["「세탁소」로 끝", 27508, 40.8], ["「사」로 끝", 10099, 15.0],
 ["「크리닝·클리닝」", 4395, 6.5], ["「빨래방」", 2802, 4.2],
 ["「런드리·laundry」", 67, 0.1]
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

$("#birth").innerHTML =
  '<thead><tr><th>업종</th><th>곳</th><th>첫 허가</th><th>중앙값</th></tr></thead><tbody>' +
  BIRTH.map(([w, c, f, m]) =>
    '<tr><td>' + w + '</td><td>' + nf(c) + '</td>' +
    '<td' + (w === "운동화전문세탁업" ? ' class="hi"' : "") + '>' +
      (f === 1900 ? "1900*" : f) + '</td><td>' + m + '</td></tr>').join("") +
  '</tbody>';

$("#mix").innerHTML =
  '<thead><tr><th>인허가 연도</th><th>새 허가</th><th>운동화 전문</th><th>빨래방</th><th>일반세탁</th></tr></thead><tbody>' +
  MIX.map(([y, n, a, b, c]) =>
    '<tr><td>' + y + '</td><td>' + nf(n) + '</td>' +
    '<td class="hi">' + a.toFixed(2) + '%</td><td>' + b.toFixed(2) + '%</td>' +
    '<td>' + c.toFixed(2) + '%</td></tr>').join("") +
  '</tbody>';

$("#mach").innerHTML =
  '<thead><tr><th>업종</th><th>세탁기수 채움</th><th>중앙값</th><th>최대</th></tr></thead><tbody>' +
  MACH.map(([w, f, m, mx]) =>
    '<tr><td>' + w + '</td><td>' + f.toFixed(1) + '%</td><td>' + m.toFixed(1) + '대</td>' +
    '<td' + (mx === 1326 ? ' class="hi"' : "") + '>' + nf(mx) + '대</td></tr>').join("") +
  '</tbody>';

const maxY = Math.max(...YEARS.map(y => y[1]));
$("#years").innerHTML = YEARS.map(([y, c]) =>
  '<div' + (c === maxY ? ' class="on"' : "") +
  ' data-h="' + (c / maxY * 100).toFixed(1) + '" data-t="' + y + '년 — ' + nf(c) + '곳"></div>').join("");
$("#ylab").innerHTML = YEARS.map(([y]) =>
  '<span>' + (y % 5 === 0 || y === 2002 ? String(y).slice(2) : "") + '</span>').join("");

const maxN = NAMES[0][1];
$("#names").innerHTML = NAMES.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxN * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
  document.querySelectorAll("#years div").forEach(b => b.style.height = b.dataset.h + "%");
});
"""

out_dir = ROOT / "laundry"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("laundry/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
