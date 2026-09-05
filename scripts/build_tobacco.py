"""
제25호 「2009년11월법개정전자료」(tobacco/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_tobacco.py 의 출력(data/분석결과_담배소매업.txt)과
대조한 값이다.

사용법:
    python scripts/build_tobacco.py

※ 이 페이지에서 지킨 선

1. **상호는 「무」 「없음」처럼 사람을 특정하지 않는 값만 옮긴다.**
   657,136곳의 담배 가게 이름을 옮기는 것은 잡학이 아니라 명부다.

2. **「없음」 상호는 제18호와 같은 모양이라 곁가지로만 다룬다.**
   반복하지 않고 제18호를 가리킨다.

3. **분류 이름을 날짜로 검증한 결과를 본문에 싣는다.**
   검증 없이 「이름이 이상하다」로만 끝내면 이야기가 서지 않는다.
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("담배소매업 657,136곳의 「민원종류명」 칸에는 답이 셋뿐인데, 그중 하나가 "
        "「2009년11월법개정전자료」다. 분류가 아니라 법이 바뀐 시점이다. "
        "빈칸까지 합치면 57.3%가 옛 기록으로 표시되어 있다.")

HEAD = """<title>2009년11월법개정전자료</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/tobacco/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="2009년11월법개정전자료 — 세모지 제25호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/tobacco/">
<meta property="og:image" content="https://semoji.net/og/tobacco.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="2009년11월법개정전자료 — 세모지 제25호 열람실">
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
/* 제25호 전용 */
h1{word-break:break-all}
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
/* 검증 표 */
.chk{width:100%;border-collapse:collapse;margin-top:6px;font-variant-numeric:tabular-nums}
.chk th,.chk td{padding:11px 8px;border-bottom:1px solid var(--rule-2);text-align:right;
  font-family:var(--f-mono);font-size:12.5px}
.chk th{color:var(--muted);font-size:10.5px;letter-spacing:.1em;font-weight:400;
  border-bottom:1px solid var(--rule)}
.chk th:first-child,.chk td:first-child{text-align:left;color:var(--ink-2);
  word-break:break-all}
.chk tr.on td{color:var(--seal-ink);font-weight:700}
.chk tbody tr:last-child td{border-bottom:0}
/* 분류 목록 */
.kinds{border-top:1px solid var(--rule);margin-top:6px}
.kinds div{display:grid;grid-template-columns:minmax(0,1fr) minmax(112px,auto);
  gap:12px;padding:13px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.kinds .w{font-family:var(--f-mono);font-size:14px;word-break:break-all}
.kinds div.on .w{color:var(--seal-ink);font-weight:700}
.kinds .c{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);text-align:right;
  font-variant-numeric:tabular-nums}
.kinds .hd{border-bottom:1px solid var(--rule)}
.kinds .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;color:var(--muted)}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제25호 열람실</span>
    <span>원자료 <b>담배소매업</b> · LOCALDATA · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제25호 열람실 · 담배소매업 「민원종류명」</p>
    <h1>2009년11월법개정전자료</h1>
    <p class="lede">
      담배 가게 <b>657,136곳</b>의 서식에는 「민원종류명」 칸이 있고
      답이 <b>셋뿐</b>입니다. 그런데 그중 하나가 분류가 아니라
      <b>법이 바뀐 시점</b>입니다. 218,118건이 이 답을 달고 있습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">657,136</span><span class="l">담배소매업</span><span class="s">영업 중 135,579곳</span></div>
      <div class="fig hot"><span class="n">218,118</span><span class="l">「법개정전자료」</span><span class="s">33.2%</span></div>
      <div class="fig"><span class="n">3</span><span class="l">민원종류명의 답</span><span class="s">빈칸까지 넣으면 넷</span></div>
      <div class="fig hot"><span class="n">57.3%</span><span class="l">옛 기록으로 표시됨</span><span class="s">376,457곳</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>답이 셋뿐인 칸</h2><span>민원종류명</span></div>
    <p class="blk-note">
      「민원종류명」은 어떤 근거로 지정된 소매인인지 적는 칸입니다.
      답은 <b>세 가지</b>뿐이고, 24.1%는 아예 비어 있습니다.
      셋 중 둘은 <b>법조문 번호</b>이고, 나머지 하나는 <b>날짜</b>입니다.
    </p>
    <div class="kinds" id="kinds"></div>
    <p class="say">
      「제7조의3제2항에따른경우」에는 <b>띄어쓰기가 없습니다.</b>
      조문 번호가 그대로 분류 이름이 되어 있습니다.
      담배사업법의 조문을 모르면 이 값이 무엇을 뜻하는지 알 수 없습니다.
      <b>서식이 시민의 말이 아니라 법의 말로 적혀 있습니다.</b>
    </p>
  </section>

  <article class="form">
    <span class="form-label">먼저 확인한 것 · 그 이름이 정말 그 시기를 가리키나</span>
    <p class="q-text" style="margin-top:20px">「2009년11월법개정전자료」라고 적혀 있다고 정말 옛 기록이라는 보장은 없다</p>
    <table class="chk" id="chk"></table>
    <p class="say">
      인허가일자와 대조해 보니 <b>이름이 정직합니다.</b>
      「법개정전자료」로 표시된 218,118건은 <b>91.3%가 2009년 이전</b>이고
      등록 중앙값이 <b>2004년</b> 입니다. 2010년 이후 인허가인데 이 분류인 것은
      <b>1,329건(0.61%)</b> 뿐입니다.
    </p>
    <p class="say">
      더 중요한 것은 <b>빈칸</b> 입니다. 민원종류명이 빈 158,339건은
      인허가일자가 <b>전부 2007년 이전</b> 입니다. 가장 늦은 것이 2007년입니다.
      <b>빈칸은 「누락」이 아니라 「옛 기록」입니다.</b>
      둘을 합치면 <b>376,457곳(57.3%)</b> 이 옛 기록으로 표시되어 있습니다.
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>분류가 아니라 자국이다</h2><span>서식이 바뀐 흔적</span></div>
    <p class="blk-note">
      정상적인 분류라면 「어떤 경우인가」에 답해야 합니다. 그런데 이 칸의 세 답 중
      하나는 <b>「그 질문을 하기 전에 들어온 자료」</b> 라는 뜻입니다.
      질문에 대한 답이 아니라, <b>질문이 없던 시절에 대한 표시</b>입니다.
    </p>
    <div class="split">
      <div><span class="l">지금 쓰는 분류 (조문 번호)</span><span class="n">280,679</span><span class="s">42.7% · 두 가지</span></div>
      <div class="on"><span class="l">옛 기록 표시</span><span class="n">376,457</span><span class="s">57.3% · 빈칸 + 법개정전자료</span></div>
    </div>
    <p class="say">
      <b>지금 분류로 답한 것보다 「옛 자료」로 표시된 것이 더 많습니다.</b>
      2009년 11월에 담배사업법이 바뀌면서 지정 근거를 조문별로 적게 됐고,
      그 이전 기록은 소급해서 나눌 수 없으니 통째로 한 칸에 몰아넣은 것으로 보입니다.
      <b>다만 원본에 그 이유는 적혀 있지 않습니다.</b>
      확실한 것은 <b>칸의 값 하나가 날짜라는 사실</b>뿐입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      이 페이지는 <b>담배 가게 이름을 옮기지 않았습니다</b> — 「무」 「없음」처럼
      사람을 가리키지 않는 값만 예외로 실었습니다. 657,136곳의 상호를 옮기는 것은
      잡학이 아니라 <b>명부</b>입니다. 그리고 「법개정전자료」가 왜 생겼는지는
      <b>추측입니다.</b> 데이터에는 값만 있고 이유가 없습니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>이름 없는 가게</h2><span>사업장명</span></div>
    <p class="blk-note">
      상호 칸에서 가장 많이 적힌 값은 가게 이름이 아니라
      <b>「무」 2,888곳</b> 입니다. 「없음」 2,650곳, 「-」 2,349곳, 「.」 2,038곳,
      「상호없음」 1,290곳. 다 합치면 <b>11,468곳(1.75%)</b> 이 이름이 없다고 적었습니다.
    </p>
    <div class="hbars" id="names"></div>
    <p class="say">
      <b>제18호 「개인」에서 본 것과 같은 모양입니다.</b> 상호를 적는 칸에
      상호가 아닌 것이 1위로 올라옵니다. 담배소매인 지정은 구멍가게와
      좌판에도 붙기 때문에, <b>이름이 없는 가게가 실제로 많습니다.</b>
      전체 상호는 365,369가지이고 <b>294,441가지는 딱 한 번</b>만 쓰였습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>셋 중 둘은 문을 닫았다</h2><span>영업상태</span></div>
    <p class="blk-note">
      657,136곳 중 <b>폐업이 445,591곳(67.8%)</b>, 영업 중은 135,579곳(20.6%)입니다.
      그리고 <b>직권취소 37,504곳</b>, 지정취소 34,691곳이 따로 있습니다.
    </p>
    <div class="hbars" id="alive"></div>
    <p class="say">
      제13호 방문판매업에서 본 <b>「직권말소」</b> 와 같은 자리입니다.
      담배소매업에서는 <b>「직권취소」</b> 라고 부르고 37,504곳이 여기에 해당합니다.
      「임시소매기간만료」라는 끝맺음도 3,585곳 있습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다. 상호와 전화번호는 옮기지 않습니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">상세영업상태코드 「BBBB」</span>
        <p class="b">코드 칸에 「BBBB」라고 적힌 것이 400건 있습니다.</p>
        <p class="c">다른 코드는 0부터 6까지 한 자리 숫자입니다. 「BBBB」만 글자이고,
          그 400건은 상세영업상태명이 전부 비어 있습니다. 인허가는 1986~2006년입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">인허가일자 1900년</span>
        <p class="b">인허가일자가 1900년으로 적힌 곳이 있습니다.</p>
        <p class="c">담배소매인 지정 제도가 있기 전입니다. 날짜 칸의 기본값으로 보입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">지정일자 1990년 이전 14,524건</span>
        <p class="b">지정일자는 75.9%만 채워져 있고, 그중 14,524건이 1990년보다 이릅니다.</p>
        <p class="c">가장 이른 값은 1900년입니다. 인허가일자와 지정일자가 서로 다른 칸인데
          무엇이 다른지는 데이터에 설명이 없습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">상호가 「.」인 곳 2,038</span>
        <p class="b">가게 이름 칸에 마침표 하나만 적은 곳이 2,038곳입니다.</p>
        <p class="c">제19호 고압가스에서 찾은 「한 글자 답」 신호가 여기서도 나옵니다.
          채움률로는 안 보입니다 — 채워져 있으니까요.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제25호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>담배소매업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 내려받은 657,136행 기준<br>가게 상호와 전화번호는 옮기지 않았습니다. 「무」 「없음」처럼 사람을 가리키지 않는 값만 실었습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 657,136행에서 계산했습니다. scripts/analyze_tobacco.py 로 재현됩니다. */

/* 민원종류명 [값, 건수, 비율] */
const KINDS = [
 ["제7조의3제2항에따른경우", 250543, 38.1],
 ["2009년11월법개정전자료", 218118, 33.2],
 ["(빈칸)", 158339, 24.1],
 ["제7조의3제3항에따른경우", 30136, 4.6]
];

/* 검증표 [분류, 건수, 중앙값, 2009년 이전%, 최대연도] */
const CHK = [
 ["2009년11월법개정전자료", 218118, 2004, 91.3, 2026],
 ["제7조의3제2항에따른경우", 250543, 2016, 1.6, 2026],
 ["제7조의3제3항에따른경우", 30136, 2015, 2.7, 2026],
 ["(빈칸)", 158339, 2000, 100.0, 2007]
];

/* 이름 없다고 적은 상호 [값, 곳수] */
const NAMES = [
 ["무", 2888], ["없음", 2650], ["-", 2349], ["."  , 2038],
 ["상호없음", 1290], ["미상", 196], ["무명", 54], ["없슴", 2], ["무상호", 1]
];

/* 영업상태 [상태, 곳수, 비율] */
const ALIVE = [
 ["폐업처리", 445591, 67.8], ["정상영업", 135179, 20.6],
 ["직권취소", 37504, 5.7], ["지정취소", 34691, 5.3],
 ["임시소매기간만료", 3585, 0.5], ["휴업처리", 124, 0.0], ["영업정지", 62, 0.0]
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

$("#kinds").innerHTML =
  '<div class="hd"><span class="w">민원종류명에 적힌 값</span><span class="c">건 · 비율</span></div>' +
  KINDS.map(([w, c, p]) =>
    '<div' + (w === "2009년11월법개정전자료" ? ' class="on"' : "") +
    ' data-t="' + esc(w) + ' — ' + nf(c) + '건 (' + p + '%)">' +
    '<span class="w">' + esc(w) + '</span>' +
    '<span class="c">' + nf(c) + ' · ' + p.toFixed(1) + '%</span></div>').join("");

$("#chk").innerHTML =
  '<thead><tr><th>민원종류명</th><th>건수</th><th>등록 중앙값</th><th>2009년 이전</th><th>최대</th></tr></thead><tbody>' +
  CHK.map(([w, c, med, pre, mx]) =>
    '<tr' + (w === "2009년11월법개정전자료" || w === "(빈칸)" ? ' class="on"' : "") + '>' +
    '<td>' + esc(w) + '</td><td>' + nf(c) + '</td><td>' + med + '</td>' +
    '<td>' + pre.toFixed(1) + '%</td><td>' + mx + '</td></tr>').join("") +
  '</tbody>';

const maxN = NAMES[0][1];
$("#names").innerHTML = NAMES.map(([w, c]) =>
  '<div class="hrow" data-t="「' + esc(w) + '」 — ' + nf(c) + '곳">' +
  '<span class="cat">' + esc(w) + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxN * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + nf(c) + '곳</span></div>').join("");

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

out_dir = ROOT / "tobacco"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("tobacco/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
