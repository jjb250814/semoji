"""
제19호 「점 하나」(gas/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_gas.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_gas.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("특정고압가스 사용신고서는 「사용목적」과 「사용방법」을 따로 묻는다. "
        "11,263건 중 3,579건이 두 칸에 같은 말을 적었고, 205곳은 점 하나만 찍었다.")

HEAD = """<title>점 하나</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/gas/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="점 하나 — 세모지 제19호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/gas/">
<meta property="og:image" content="https://semoji.net/og/gas.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="점 하나 — 세모지 제19호 열람실">
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
/* 제19호 전용 */
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
.qpair{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--rule);margin-top:22px}
.qpair > div{padding:24px 20px 22px 0;border-right:1px solid var(--rule-2)}
.qpair > div:last-child{border-right:0}
.qpair .lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.13em;color:var(--muted)}
.qpair .q{display:block;font-family:var(--f-display);font-weight:700;font-size:17px;
  margin-top:12px;line-height:1.45}
.qpair .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(24px,4vw,34px);line-height:1;margin-top:16px;
  font-variant-numeric:tabular-nums}
.qpair .s{display:block;font-size:13px;color:var(--ink-2);font-weight:300;margin-top:10px}
@media (max-width:560px){.qpair{grid-template-columns:1fr}
  .qpair > div{border-right:0;border-bottom:1px solid var(--rule-2)}
  .qpair > div:last-child{border-bottom:0}}
.echo{border-top:1px solid var(--rule);margin-top:22px}
.echo div{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(74px,auto);
  gap:14px;padding:12px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.echo .a,.echo .b{font-size:15px}
.echo .b{color:var(--seal-ink)}
.echo .c{font-family:var(--f-mono);font-size:12.5px;color:var(--muted);
  text-align:right;font-variant-numeric:tabular-nums}
.echo .hd{border-bottom:1px solid var(--rule)}
.echo .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;
  color:var(--muted)}
.echo .hd .b{color:var(--muted)}
.marks{display:flex;flex-wrap:wrap;gap:12px;margin-top:6px}
.marks span{display:grid;place-items:center;gap:5px;border:1px solid var(--rule);
  background:var(--card);padding:14px 8px 11px;min-width:76px}
.marks b{font-family:var(--f-display);font-weight:800;font-size:26px;line-height:1}
.marks i{font-style:normal;font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.marks span.on{border-color:var(--seal);background:var(--seal-soft)}
.marks span.on b{color:var(--seal-ink)}
.who{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
  border-top:1px solid var(--rule);margin-top:6px}
.who > div{padding:22px 16px 20px 0;border-right:1px solid var(--rule-2)}
.who > div:last-child{border-right:0}
.who .l{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--muted)}
.who .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(26px,4.2vw,36px);line-height:1;margin-top:12px;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.who > div.on .n{color:var(--seal-ink)}
.who .s{display:block;font-size:12.5px;color:var(--muted);font-weight:300;margin-top:10px}
.top-li{border-top:1px solid var(--rule);margin-top:6px}
.top-li div{display:grid;grid-template-columns:26px minmax(0,1fr) minmax(70px,auto);
  gap:12px;padding:10px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.top-li .r{font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.top-li .nm{font-size:14.5px;word-break:keep-all}
.top-li div.on .nm{color:var(--seal-ink);font-weight:600}
.top-li .c{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);
  text-align:right;font-variant-numeric:tabular-nums}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제19호 열람실</span>
    <span>원자료 <b>특정고압가스 사용신고</b> · LOCALDATA · 2026-09-04 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제19호 열람실 · 특정고압가스 사용신고</p>
    <h1>점 하나</h1>
    <p class="lede">
      산소나 수소 같은 특정고압가스를 쓰려면 관청에 신고해야 합니다.
      그 서식에는 칸이 둘 있습니다 — <b>「사용목적」</b>과 <b>「사용방법」</b>.
      무엇에 쓰는지, 그리고 어떻게 쓰는지. 11,263건 가운데
      <b>3,579건이 두 칸에 똑같은 말을 적었고</b>, 205곳은
      방법 칸에 <b>점 하나</b>만 찍었습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">11,263</span><span class="l">사용신고</span><span class="s">영업 중 8,671곳</span></div>
      <div class="fig hot"><span class="n">31.8%</span><span class="l">두 칸에 같은 답</span><span class="s">3,579건</span></div>
      <div class="fig"><span class="n">4,358</span><span class="l">「사용목적」 답의 종류</span><span class="s">「사용방법」은 5,375가지</span></div>
      <div class="fig"><span class="n">405</span><span class="l">한 글자로 채운 방법 칸</span><span class="s">그중 점 하나가 205</span></div>
    </div>
  </div>

  <article class="form">
    <span class="form-label">특정고압가스 사용신고서</span>
    <div class="qpair">
      <div>
        <span class="lab">칸 하나</span>
        <span class="q">Q. 무엇에 쓰십니까<br>(사용목적)</span>
        <span class="n">4,358가지</span>
        <span class="s">10,742곳이 채웠습니다. 「의료용」이 1,121건으로 가장 많습니다.</span>
      </div>
      <div>
        <span class="lab">칸 둘</span>
        <span class="q">Q. 어떻게 쓰십니까<br>(사용방법)</span>
        <span class="n">5,375가지</span>
        <span class="s">10,236곳이 채웠습니다. 목적보다 답이 더 갈립니다.</span>
      </div>
    </div>
    <p class="say">
      두 질문은 다릅니다. <b>무엇에</b> 쓰는지와 <b>어떻게</b> 쓰는지는 다른 것이니까요.
      그런데 답을 받아 보면 그 구분이 잘 지켜지지 않습니다.
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>같은 말을 두 번 적는다</h2><span>3,579건 · 31.8%</span></div>
    <p class="blk-note">
      왼쪽이 목적 칸, 오른쪽이 방법 칸입니다. <b>셋 중 한 곳</b>은 두 칸에 글자 하나 다르지 않게
      같은 말을 적었습니다. 「의료용」이라고 두 번 쓴 곳만 364곳입니다.
    </p>
    <div class="echo" id="echo"></div>
    <p class="say">
      묻는 쪽은 두 가지를 알고 싶었을 텐데, 적는 쪽에게는 <b>한 가지였습니다.</b>
      병원에서 산소를 쓰는 목적도 「의료용」이고 방법도 「의료용」입니다.
      더 쪼갤 말이 없습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>답을 할 수 없을 때</h2><span>한 글자로 채운 칸</span></div>
    <p class="blk-note">
      방법 칸을 <b>한 글자</b>로 채운 곳이 405군데 있습니다. 열 가지 글자가 나옵니다.
      점, 하이픈, 0, 1 — 그리고 <b>「ㅂ」이 아홉 곳</b>, 「ㅇ」이 네 곳입니다.
      자음 하나입니다.
    </p>
    <div class="marks" id="marks"></div>
    <p class="say">
      목적 칸에도 123곳이 한 글자만 적었습니다. <b>두 칸 모두 「0」인 곳이 47군데</b>,
      두 칸 모두 비어 있는 곳이 516군데입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      <b>왜 점 하나를 찍었는지는 데이터에 없습니다.</b> 답을 몰랐을 수도 있고,
      목적 칸과 같은 말이라 굳이 다시 쓰지 않은 것일 수도 있고,
      빈칸으로는 다음 화면으로 넘어가지 않아 아무 글자나 넣어야 했을 수도 있습니다.
      <b>「ㅂ」은 자판에서 「.」 근처도 아닙니다.</b> 무엇을 누른 것인지는 알 수 없습니다.
      확실한 것은 하나입니다 — <b>서식이 답을 요구했고, 405곳이 글자 하나로 응했습니다.</b>
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>그래도 4,358가지 답이 나왔다</h2><span>사용목적에 적힌 말</span></div>
    <p class="blk-note">
      대부분은 성실하게 적었습니다. 가장 흔한 답은 <b>「의료용」 1,121건</b>이고,
      낱말로 세면 <b>「절단」이 15.9%</b>로 가장 많습니다. 고압가스는 무엇보다
      <b>무언가를 자르는 데</b> 쓰입니다.
    </p>
    <div class="top-li" id="tops"></div>
    <div class="hbars" id="words"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>누가 쓰나</h2><span>그리고 물고기</span></div>
    <p class="blk-note">
      이름에 「병원」이 들어간 곳이 <b>15.4%</b>로 가장 큰 무리입니다.
      대학과 연구소가 6.1%, 군대가 101곳입니다. 가장 자주 나오는 이름은
      성균관대학교(49건), 한국과학기술원(48건), 한국에너지기술연구원(47건) 순입니다.
    </p>
    <div class="who">
      <div class="on"><span class="l">병원</span><span class="n">1,732</span><span class="s">15.4% · 대부분 「의료용」</span></div>
      <div><span class="l">대학 · 연구소</span><span class="n">689</span><span class="s">6.1% · 「연구용」 「실험용」</span></div>
      <div><span class="l">양식장</span><span class="n">1,026</span><span class="s">9.1% · 물에 산소를 넣는다</span></div>
      <div><span class="l">군</span><span class="n">101</span><span class="s">0.9%</span></div>
    </div>
    <p class="say">
      <b>뜻밖의 무리는 양식장입니다.</b> 1,026곳(9.1%)이 목적이나 방법 칸에
      양식·축양을 적었습니다. 「어류양식」 124건, 「양식장 산소공급」 107건,
      「광어양식」 35건, 「뱀장어 양식」 27건. <b>고압산소를 사람이 아니라
      물고기에게 씁니다.</b> 물에 녹여 넣는 것입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">
      원본 파일에 실제로 들어 있는 값입니다. 어느 사업장의 기록인지는 적지 않습니다.
    </p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">수용정원수 3,000,024</span>
        <p class="b">삼백만 명이 들어간다고 적힌 곳이 있습니다.</p>
        <p class="c">1만이 넘는 곳이 20군데, 반대로 「0」이라고 적은 곳이 1,104군데입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">월사용량 1억 6천만</span>
        <p class="b">한 달에 160,000,000을 쓴다고 적힌 곳이 한 곳 있습니다.</p>
        <p class="c">단위가 무엇인지는 데이터에 없습니다. 「0」이라고 적은 곳은 629군데입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">인허가일자 1900년</span>
        <p class="b">1900년에 신고한 것으로 적힌 기록이 있습니다.</p>
        <p class="c">1990년 이전 기록이 366건입니다. 고압가스 안전관리법은 1983년에 만들어졌습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">방법 칸에 남은 메모</span>
        <p class="b">담당자가 적은 것으로 보이는 문장이 177건 있습니다.</p>
        <p class="c">그중 8건에는 사업자등록번호나 전화번호가 들어 있습니다. 이 페이지에는 옮기지 않았습니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제19호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>특정고압가스 사용신고</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-04 내려받은 11,263행 기준<br>개별 사업장의 안전 관리 상태는 다루지 않았습니다. 신고서에 적힌 값만 옮겼습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 11,263행에서 계산했습니다. scripts/analyze_gas.py 로 재현됩니다. */

/* 두 칸에 같은 말을 적은 값 [말, 건수] */
const ECHO = [
 ["의료용", 364], ["연구용", 120], ["열처리용", 89], ["절단용", 71],
 ["어류양식", 65], ["열처리", 55], ["0", 47], ["축양장 산소공급", 46]
];

/* 방법 칸을 한 글자로 채운 것 [글자, 건수] */
const MARKS = [
 [".", 205], ["-", 75], ["0", 73], ["1", 30], ["ㅂ", 9],
 ["`", 5], ["ㅇ", 4], ["반", 2], ["ㄴ", 1], ["9", 1]
];

/* 사용목적 상위 [말, 건수] */
const TOPS = [
 ["의료용", 1121], ["절단용", 262], ["열처리용", 195], ["연구용", 173],
 ["산업용", 167], ["열처리", 148], ["공업용", 140], ["어류양식", 124],
 ["양식장 산소공급", 107], ["용접용", 90]
];

/* 사용목적 낱말 [낱말, 건수, 비율] */
const WORDS = [
 ["절단", 1787, 15.9], ["의료", 1485, 13.2], ["용접", 923, 8.2],
 ["열처리", 705, 6.3], ["연구", 633, 5.6], ["실험", 417, 3.7],
 ["제조", 333, 3.0], ["소독", 202, 1.8], ["분석", 148, 1.3],
 ["시험", 135, 1.2], ["냉각", 77, 0.7], ["교육", 49, 0.4]
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

$("#echo").innerHTML =
  '<div class="hd"><span class="a">사용목적</span><span class="b">사용방법</span>' +
  '<span class="c">곳</span></div>' +
  ECHO.map(([w, c]) =>
    '<div data-t="목적도 방법도 「' + w + '」 — ' + nf(c) + '곳">' +
    '<span class="a">' + w + '</span>' +
    '<span class="b">' + w + '</span>' +
    '<span class="c">' + nf(c) + '</span></div>').join("");

$("#marks").innerHTML = MARKS.map(([m, c]) =>
  '<span' + (m === "." ? ' class="on"' : "") +
  ' data-t="방법 칸에 「' + m + '」 한 글자 — ' + nf(c) + '곳">' +
  '<b>' + m + '</b><i>' + nf(c) + '</i></span>').join("");

$("#tops").innerHTML = TOPS.map(([nm, c], i) =>
  '<div' + (i === 0 ? ' class="on"' : "") + ' data-t="' + nm + ' — ' + nf(c) + '곳">' +
  '<span class="r">' + (i + 1) + '</span>' +
  '<span class="nm">' + nm + '</span>' +
  '<span class="c">' + nf(c) + '</span></div>').join("");

const maxW = WORDS[0][1];
$("#words").innerHTML = WORDS.map(([w, c, p]) =>
  '<div class="hrow" data-t="‘' + w + '’ — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxW * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p + '% · ' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "gas"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("gas/index.html 작성 완료 — %s bytes" % f"{out.stat().st_size:,}")
