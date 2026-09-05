"""
제18호 「개인」(dust/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_dust.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_dust.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("비산먼지 발생사업 신고 922,057건. 사업자명 칸에 가장 많이 적힌 이름은 "
        "회사가 아니라 「개인」으로, 161,461건이다.")

HEAD = """<title>개인</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/dust/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="개인 — 세모지 제18호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/dust/">
<meta property="og:image" content="https://semoji.net/og/dust.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="개인 — 세모지 제18호 열람실">
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
/* 제18호 전용 */
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
.noname{border-top:1px solid var(--rule);margin-top:22px}
.noname div{display:grid;grid-template-columns:minmax(0,1fr) minmax(90px,auto) minmax(74px,auto);
  gap:14px;padding:11px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.noname .w{font-family:var(--f-display);font-weight:600;font-size:16px}
.noname div.on .w{color:var(--seal-ink)}
.noname .c,.noname .p{font-family:var(--f-mono);font-size:12.5px;text-align:right;
  font-variant-numeric:tabular-nums}
.noname .c{color:var(--ink-2)}
.noname .p{color:var(--muted)}
.noname .sum{border-bottom:0;border-top:1.5px solid var(--ink);margin-top:4px}
.noname .sum .w{font-weight:800}
.noname .sum .c{color:var(--seal-ink);font-weight:700}
.two-read{display:grid;gap:0;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  border-top:1px solid var(--rule);margin-top:22px}
.two-read > div{padding:24px 22px 22px 0;border-right:1px solid var(--rule-2)}
.two-read > div:last-child{border-right:0}
.two-read .k{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.two-read .t{display:block;font-family:var(--f-display);font-weight:700;font-size:18px;
  margin-top:12px;line-height:1.4}
.two-read .b{display:block;font-size:13.5px;color:var(--ink-2);font-weight:300;margin-top:11px}
.big3{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));
  border-top:1px solid var(--rule);margin-top:6px}
.big3 > div{padding:22px 16px 20px 0;border-right:1px solid var(--rule-2)}
.big3 > div:last-child{border-right:0}
.big3 .l{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--muted)}
.big3 .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(26px,4.4vw,38px);line-height:1;margin-top:12px;
  font-variant-numeric:tabular-nums}
.big3 > div.on .n{color:var(--seal-ink)}
.big3 .s{display:block;font-size:12.5px;color:var(--muted);font-weight:300;margin-top:10px}
.sites{border-top:1px solid var(--rule);margin-top:6px}
.sites div{display:grid;grid-template-columns:28px minmax(0,1fr) minmax(80px,auto);
  gap:12px;padding:10px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.sites .r{font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.sites .nm{font-size:14.5px;word-break:keep-all}
.sites div.on .nm{color:var(--seal-ink);font-weight:600}
.sites .c{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);
  text-align:right;font-variant-numeric:tabular-nums}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제18호 열람실</span>
    <span>원자료 <b>비산먼지 발생사업</b> · LOCALDATA · 2026-09-04 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제18호 열람실 · 비산먼지 발생사업 신고</p>
    <h1>개인</h1>
    <p class="lede">
      땅을 파거나 건물을 올리면 먼지가 납니다. 그래서 관청에 신고를 해야 하고,
      그 신고서가 <b>922,057건</b> 쌓여 있습니다. 서식에는 「사업자명(상호)」 칸이 있는데,
      거기에 가장 많이 적힌 이름은 대우건설도 현대건설도 아닙니다.
      <b>「개인」, 161,461건</b>입니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">922,057</span><span class="l">신고 건수</span><span class="s">1990년 이후 · 관리기관 230곳</span></div>
      <div class="fig hot"><span class="n">17.5%</span><span class="l">상호가 「개인」</span><span class="s">161,461건</span></div>
      <div class="fig"><span class="n">663,652</span><span class="l">공사장 이름 가짓수</span><span class="s">이 서고에서 가장 큰 자유 입력</span></div>
      <div class="fig"><span class="n">183일</span><span class="l">공사 기간 중앙값</span><span class="s">1년 넘는 것 201,484건</span></div>
    </div>
  </div>

  <article class="form">
    <span class="form-label">비산먼지 발생사업 신고서 · 사업자명(상호)</span>
    <p class="q-text" style="margin-top:20px">Q. 사업자명(상호)을 적으십시오</p>
    <div class="noname" id="noname"></div>
    <p class="say">
      회사 이름이 들어가야 할 칸입니다. 그런데 <b>다섯 건 중 한 건</b>에는
      회사가 아니라 <b>회사가 없다는 말</b>이 적혀 있습니다.
      「개인」이 압도적이고, 「-」 「없음」 「상호없음」 「자가시공」 같은 답도 뒤를 잇습니다.
      실제 회사 이름 중 1위는 <b>(주)대우건설 1,605건</b>으로, 「개인」의 1%에 못 미칩니다.
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>2015년에 무슨 일이 있었나</h2><span>연도별 「개인」 비중</span></div>
    <p class="blk-note">
      막대 하나가 그해 신고 중 상호가 「개인」인 비율입니다.
      2013년까지 <b>6~7%</b>를 오가다가 2014년 13.5%, <b>2015년 30.7%</b>로 뜁니다.
      그 뒤로는 계속 <b>30% 언저리</b>에 머뭅니다.
    </p>
    <div class="cols" id="years"></div>
    <div class="axis" id="yaxis"></div>
    <details class="tbl">
      <summary>표로 보기</summary>
      <div class="scroll"><table id="ytbl"><thead><tr><th>연도</th><th>「개인」</th><th>그해 신고</th><th>비중</th></tr></thead><tbody></tbody></table></div>
    </details>
    <p class="say">
      <b>서서히 늘어난 게 아니라 한 해 만에 계단을 올랐습니다.</b>
      사람들의 행동이 1년 만에 이렇게 바뀌는 일은 드뭅니다.
      보통 이런 모양은 <b>서식이나 규칙이 바뀌었을 때</b> 나옵니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      <b>왜 뛰었는지는 데이터 어디에도 적혀 있지 않습니다.</b>
      읽을 수 있는 방법이 둘입니다. 하나는 개인이 직접 신고하는 일이 실제로 늘었다는 것,
      다른 하나는 개인의 이름을 「개인」으로 바꿔 내보내기 시작했다는 것입니다.
      두 번째가 더 그럴듯해 보이지만 <b>원본에 근거가 없으므로 단정하지 않습니다.</b>
      확실한 것은 하나뿐입니다 — <b>2014년과 2015년 사이에 이 칸의 답이 바뀌었습니다.</b>
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>공사장 이름 663,652가지</h2><span>전국에서 가장 흔한 이름은</span></div>
    <p class="blk-note">
      「공사장명」 칸은 규격이 없습니다. 92만 건에 <b>66만 가지</b> 이름이 적혔습니다.
      이 사이트가 지금까지 판 자유 입력 중 가장 큽니다.
      그런데 1위는 아파트도 빌딩도 아닌 <b>「농지성토」</b>, 밭에 흙을 붓는 일입니다.
    </p>
    <div class="sites" id="sites"></div>
    <div class="big3">
      <div class="on"><span class="l">농지성토</span><span class="n">13,488</span><span class="s">전국 1위 공사장 이름</span></div>
      <div><span class="l">그중 상호가 「개인」</span><span class="n">71%</span><span class="s">9,610건</span></div>
      <div><span class="l">공사 기간 중앙값</span><span class="n">91일</span><span class="s">전체 중앙값의 절반</span></div>
    </div>
    <p class="say">
      <b>가장 흔한 공사는 건물을 짓는 일이 아니라 땅을 고르는 일입니다.</b>
      그리고 그 열에 일곱은 회사가 아니라 「개인」이 냈습니다.
      석 달쯤 걸려 밭에 흙을 붓고 끝납니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>이름에 무슨 말이 들어가나</h2><span>공사장명 낱말 빈도</span></div>
    <p class="blk-note">
      66만 가지 이름이지만 들어가는 낱말은 정해져 있습니다.
      <b>넷 중 셋에 「공사」</b>가 들어가고, <b>셋 중 하나에 「신축」</b>이 들어갑니다.
      「태양광」이 「아파트」보다 많다는 점은 눈여겨볼 만합니다.
    </p>
    <div class="hbars" id="words"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">
      원본 파일에 실제로 들어 있는 값입니다.
      <b>어느 업체의 기록인지는 적지 않습니다.</b> 칸을 잘못 채운 것이지
      그 업체의 잘못이 아닙니다.
    </p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">2999년 12월 31일</span>
        <p class="b">공사가 서기 2999년에 끝난다고 적힌 신고가 161건 있습니다.</p>
        <p class="c">그중에는 1985년에 시작한 것도 있습니다. 1,015년짜리 공사입니다. 1,000년이 넘는 공사가 26건입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">발생사업명 빈칸 16.8%</span>
        <p class="b">무슨 사업인지 적는 칸이 155,061건에서 비어 있습니다.</p>
        <p class="c">채워진 것 중 739,630건은 「건설업」입니다. 나머지 열세 가지가 나눠 갖습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">신고일자 2043년</span>
        <p class="b">17년 뒤에 접수될 예정인 신고가 한 건 있습니다.</p>
        <p class="c">반대쪽에는 2000년 이전 신고가 7,221건 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">공사장 이름 84자</span>
        <p class="b">가장 긴 이름은 84자입니다. 지번을 스무 개 넘게 나열했습니다.</p>
        <p class="c">반대로 한 글자짜리 이름이 3,304건, 「-」 한 글자가 2,941건입니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제18호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>비산먼지 발생사업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-04 내려받은 922,057행 기준<br>특정 사업장의 먼지 배출량이나 위법 여부는 다루지 않았습니다. 신고서에 적힌 값만 옮겼습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 922,057행에서 계산했습니다. scripts/analyze_dust.py 로 재현됩니다. */

/* [적힌 말, 건수, 비율] */
const NONAME = [
 ["개인", 161461, 17.51], ["-", 6521, 0.71], ["빈칸", 14896, 1.62],
 ["없음", 749, 0.08], ["상호없음", 269, 0.03], ["개인직영", 99, 0.01],
 ["무", 87, 0.01], ["자가시공", 84, 0.01], ["개인사업자", 74, 0.01]
];
const NONAME_SUM = [184240, 19.98];

/* [연도, 「개인」, 그해 신고] */
const YEARS = [
 [2005,441,23338],[2006,382,24914],[2007,817,31236],[2008,1427,34964],
 [2009,1643,34614],[2010,2537,33731],[2011,2565,33687],[2012,2332,33429],
 [2013,2122,34051],[2014,4739,35000],[2015,12392,40359],[2016,12985,41154],
 [2017,12542,41043],[2018,12838,41686],[2019,12150,42763],[2020,13543,46302],
 [2021,14754,49482],[2022,13461,45650],[2023,10286,38790],[2024,9947,38143],
 [2025,9315,36394],[2026,6548,25065]
];

/* [공사장 이름, 건수] */
const SITES = [
 ["농지성토", 13488], ["근린생활시설 신축공사", 8294], ["토목공사", 4589],
 ["건축물축조공사", 3691], ["단독주택 신축공사", 3371], ["공장 신축공사", 3265],
 ["공장신축공사", 3033], ["토공사및정지공사", 3033], ["토공사 및 정지공사", 2872],
 ["건축물 축조공사", 2469], ["다세대주택 신축공사", 1930]
];

/* [낱말, 건수, 비율] */
const WORDS = [
 ["공사", 686974, 74.5], ["신축", 269969, 29.3], ["공장", 68843, 7.5],
 ["주택", 68557, 7.4], ["도로", 58099, 6.3], ["성토", 36256, 3.9],
 ["증축", 31545, 3.4], ["태양광", 22746, 2.5], ["아파트", 21367, 2.3],
 ["창고", 21226, 2.3], ["축사", 13348, 1.4], ["철거", 9460, 1.0]
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

$("#noname").innerHTML =
  NONAME.map(([w, c, p]) =>
    '<div' + (w === "개인" ? ' class="on"' : "") +
    ' data-t="' + w + ' — ' + nf(c) + '건 (' + p + '%)">' +
    '<span class="w">' + (w === "빈칸" ? "(빈칸)" : "「" + w + "」") + '</span>' +
    '<span class="c">' + nf(c) + '</span>' +
    '<span class="p">' + p.toFixed(2) + '%</span></div>').join("") +
  '<div class="sum"><span class="w">이름이 없는 신고</span>' +
  '<span class="c">' + nf(NONAME_SUM[0]) + '</span>' +
  '<span class="p">' + NONAME_SUM[1] + '%</span></div>';

const PCT = YEARS.map(([y, g, t]) => [y, g / t * 100, g, t]);
const maxP = Math.max(...PCT.map(r => r[1]));
$("#years").innerHTML = PCT.map(([y, p, g, t]) => {
  const peak = y === 2015;
  const tag = peak ? '<span class="tag">2015년 ' + p.toFixed(1) + '%</span>' : "";
  return '<span class="col' + (peak ? " peak" : "") + '" data-t="' + y + '년 — ' +
    nf(g) + '건 / 신고 ' + nf(t) + '건 = ' + p.toFixed(1) + '%"' +
    ' style="height:' + Math.max(p / maxP * 100, 0.8) + '%">' + tag + '</span>';
}).join("");

const AXIS = [2005, 2010, 2015, 2020, 2026];
$("#yaxis").innerHTML = AXIS.map((y, k) => {
  const i = PCT.findIndex(r => r[0] === y);
  const pct = (i + 0.5) / PCT.length * 100;
  const cls = k === 0 ? ' class="first"' : k === AXIS.length - 1 ? ' class="last"' : "";
  return '<span' + cls + ' style="left:' + pct.toFixed(2) + '%">' + y + '</span>';
}).join("");

$("#ytbl").querySelector("tbody").innerHTML = PCT.map(([y, p, g, t]) =>
  '<tr><td>' + y + '</td><td>' + nf(g) + '</td><td>' + nf(t) + '</td><td>' +
  p.toFixed(1) + '%</td></tr>').join("");

$("#sites").innerHTML = SITES.map(([nm, c], i) =>
  '<div' + (i === 0 ? ' class="on"' : "") + ' data-t="' + nm + ' — ' + nf(c) + '건">' +
  '<span class="r">' + (i + 1) + '</span>' +
  '<span class="nm">' + nm + '</span>' +
  '<span class="c">' + nf(c) + '</span></div>').join("");

const maxW = WORDS[0][1];
$("#words").innerHTML = WORDS.map(([w, c, p]) =>
  '<div class="hrow" data-t="‘' + w + '’ — ' + nf(c) + '건 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxW * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p + '% · ' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "dust"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("dust/index.html 작성 완료 — %s bytes" % f"{out.stat().st_size:,}")
