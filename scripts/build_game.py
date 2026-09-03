"""
제10호 「곰탱이」(game.html) 조립기.

공용 CSS는 bike.html의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_game.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_game.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

HEAD = """<title>곰탱이</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="오락실 30,771곳이 「제작취급품목내용」 칸에 적은 기계 이름 13,267가지. 그중 52곳이 적은 이름이 곰탱이다.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@400;600;800&family=IBM+Plex+Sans+KR:wght@300;400;500;600&family=Nanum+Gothic+Coding:wght@400;700&display=swap">
"""

EXTRA_STYLE = """<style>
/* 제10호 전용 */
.two{display:grid;gap:0;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));
  border-top:1px solid var(--rule);margin-top:6px}
.two > div{padding:24px 20px 22px 0;border-right:1px solid var(--rule-2)}
.two > div:last-child{border-right:0}
.two .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(30px,5vw,44px);line-height:1;font-variant-numeric:tabular-nums}
.two .n.hot{color:var(--seal-ink)}
.two .s{display:block;font-size:14px;color:var(--ink-2);font-weight:300;margin-top:12px}
.mono-li{border-top:1px solid var(--rule);font-family:var(--f-mono);font-size:13px;margin-top:6px}
.mono-li div{display:flex;justify-content:space-between;gap:14px;padding:9px 0;
  border-bottom:1px solid var(--rule-2);font-variant-numeric:tabular-nums;align-items:baseline}
.mono-li b{font-weight:400;color:var(--ink);word-break:keep-all}
.mono-li span{color:var(--muted);white-space:nowrap}
.slip{font-family:var(--f-mono);font-size:12.5px;background:var(--card);
  border:1px solid var(--rule);border-left:3px solid var(--seal);
  padding:15px 17px;margin:16px 0 0;color:var(--ink-2);line-height:1.9;
  overflow-x:auto;white-space:pre-wrap;word-break:break-all}
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="./index.html">← 세모지</a> · 제10호 열람실</span>
    <span>원자료 <b>청소년게임제공업</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제10호 열람실 · 청소년게임제공업 등록 기록</p>
    <h1>곰탱이</h1>
    <p class="lede">
      오락실을 등록할 때는 「제작취급품목내용」 칸에 무슨 기계를 갖다 놓았는지 적습니다.
      19,445곳이 이 칸을 채웠고, 적힌 표현이 <b>13,267가지</b>입니다.
      그중 52곳이 적은 이름이 <b>곰탱이</b>입니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">30,771</span><span class="l">누적 등록</span><span class="s">2005년 이후 기록</span></div>
      <div class="fig hot"><span class="n">23,954</span><span class="l">사라짐</span><span class="s">전체의 77.8%</span></div>
      <div class="fig"><span class="n">6,817</span><span class="l">영업 중</span><span class="s">전체의 22.2%</span></div>
      <div class="fig"><span class="n">13,267</span><span class="l">취급품목 표현</span><span class="s">11,596가지는 단 한 번</span></div>
    </div>
  </div>

  <article class="form reader">
    <span class="form-label">제작취급품목 열람</span>
    <div class="seal" id="seal" aria-hidden="true"><b>取扱</b><i>제작취급품목</i></div>
    <p class="q-cat" id="q-cat">&mdash;</p>
    <p class="q-text" id="q-text">불러오는 중</p>
    <p class="q-meta" id="q-meta">&nbsp;</p>
    <div class="reader-act">
      <button class="btn" id="draw" type="button">다음 품목</button>
      <button class="btn ghost" id="copy" type="button">복사</button>
      <span class="tally" id="tally"></span>
    </div>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>오락실이 아니라 인형뽑기방</h2><span>취급품목 낱말 빈도</span></div>
    <p class="blk-note">
      취급품목 칸에 가장 많이 나오는 낱말은 <b>‘토이’로 2,687곳</b>입니다.
      크레인·뽑기·인형까지 더하면 옛날 오락실의 낱말인 아케이드·펀치·농구를 크게 웃돕니다.
      법은 이 업종을 ‘청소년게임제공업’이라 부르지만, 기계 이름이 말하는 실체는 인형뽑기방입니다.
    </p>
    <div class="hbars" id="words"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>1년을 못 넘긴다</h2><span>폐업 18,970곳</span></div>
    <p class="blk-note">
      등록일과 폐업일이 모두 남은 18,970곳의 영업 기간입니다.
      <b>중앙값이 1.3년</b>입니다. 제2호에서 본 PC방의 3.1년에 견주면 절반도 안 됩니다.
    </p>
    <div class="two">
      <div>
        <span class="n hot">44.1%</span>
        <span class="s">문을 연 지 <b>1년을 못 넘기고</b> 닫은 비율입니다.
          8,371곳이 여기 해당합니다.</span>
      </div>
      <div>
        <span class="n">1.3년</span>
        <span class="s">버틴 기간의 중앙값. 평균은 2.3년입니다.
          기계는 빌려 놓고 자리만 얻으면 열 수 있는 업종의 속도입니다.</span>
      </div>
    </div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>두 번의 봉우리</h2><span>연도별 신규 등록</span></div>
    <p class="blk-note">
      2009년 3,395곳으로 한 번 솟고, 잦아들었다가 <b>2017년 3,851곳</b>으로 다시 솟습니다.
      그리고 2020년 860곳, 2023년 369곳까지 주저앉았다가 2025년 1,823곳으로 되돌아옵니다.
      데이터는 언제 몇 곳이 등록했는지만 알려줍니다.
    </p>
    <div class="cols" id="years"></div>
    <div class="axis" id="yaxis"></div>
    <details class="tbl">
      <summary>표로 보기</summary>
      <div class="scroll"><table id="ytbl"><thead><tr><th>연도</th><th>신규 등록</th></tr></thead><tbody></tbody></table></div>
    </details>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>넷에 하나는 정확히 마흔 대</h2><span>총게임기수</span></div>
    <p class="blk-note">
      게임기가 몇 대인지 적는 칸입니다. 20,318곳이 답했는데
      <b>5,097곳이 정확히 40이라고 적었습니다.</b> 기재한 곳의 25.1%입니다.
      41대 이상은 3,236곳이고 가장 많은 곳은 470대입니다. 중앙값은 27대입니다.
    </p>
    <div class="two">
      <div>
        <span class="n hot">5,097</span>
        <span class="s">‘40’이라고 적은 곳. 그다음으로 많은 숫자는 50으로 1,310곳입니다.</span>
      </div>
      <div>
        <span class="n">27대</span>
        <span class="s">기재한 20,318곳의 중앙값.
          <b>왜 40에 몰렸는지는 데이터에 적혀 있지 않습니다.</b></span>
      </div>
    </div>
    <div class="mono-li" id="counts"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>기계 목록을 통째로 적은 칸</h2><span>가장 긴 기재 167자</span></div>
    <p class="blk-note">
      칸이 작지 않았던 모양입니다. 어떤 곳은 가진 기계를 심의번호까지 붙여 전부 적었습니다.
      아래는 원본에 실제로 들어 있는 한 칸의 내용입니다.
    </p>
    <div class="slip">밀땅(CC-NA-170726-003)2대, 뉴미니미니(CC-NA-230824-003)4대, 럭키7((CC-NA-241017-005)1대, CACTI GOTCHA(CC-NA-241212-005)8대, 토이즈팝미니(CC-NA-231005-003)8대, 드래곤펀치2(CC-NA-140226-001)1대,</div>
    <p class="say">
      괄호가 하나 더 열린 채 닫히지 않은 곳(<b>럭키7((</b>)과, 마지막이 쉼표로 끝난 것까지
      그대로 남아 있습니다. 이 칸을 채운 사람은 목록을 옮겨 적다가 멈췄습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">빈칸 11,326</span>
        <p class="b">무슨 기계를 두었는지 적지 않은 곳이 36.8%입니다.</p>
        <p class="c">셋 중 하나 이상이 이 칸을 비웠습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">취급품목 · 청소년게임제공업</span>
        <p class="b">취급품목 칸에 업종 이름을 그대로 옮겨 적은 곳이 23곳 있습니다.</p>
        <p class="c">무엇을 취급하느냐는 물음에 ‘청소년게임제공업’이라고 답한 셈입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">취급품목 · 전체이용가</span>
        <p class="b">40곳은 취급품목 칸에 등급을 적었습니다.</p>
        <p class="c">‘전체이용가’는 바로 옆 「제공게임물명」 칸의 답입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">사업장명 49자</span>
        <p class="b">가장 긴 상호명은 담당자의 업무 메모였습니다.</p>
        <p class="c">「오성게임랜드 (유선통보 2009.03.13. 21:00, 2009.07.07 17:40)」.
           제2호 PC방에서 본 것과 같은 일이 여기서도 일어났습니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="./index.html">세모지로 돌아가기 &rarr;</a> · 제10호 열람실 · <a href="./about.html">소개</a> · <a href="./contact.html">연락처</a> · <a href="./privacy.html">개인정보처리방침</a></span>
    <span>출처 <b>청소년게임제공업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 30,771행 기준<br>취급품목은 기계 이름이므로 그대로 실었고, 상호는 폐업·행정 기록과 엮지 않았습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 30,771행에서 계산했습니다. scripts/analyze_game.py 로 재현됩니다. */

const WORDS = [
 ["토이", 2687], ["크레인", 1261], ["아케이드", 950], ["곰", 522],
 ["뽑기", 363], ["인형", 334], ["펀치", 265], ["농구", 42]
];

const COUNTS = [
 ["40대", 5097], ["50대", 1310], ["10대", 1117], ["8대", 793],
 ["12대", 742], ["9대", 642], ["11대", 622], ["15대", 567]
];

const ITEMS = [
 ["곰탱이", 52, "52곳이 이 이름을 적었습니다. 이 페이지의 제목이 된 기계입니다."],
 ["용팔아", 23, "23곳. 무엇을 뽑는 기계인지는 이름만으로 알기 어렵습니다."],
 ["코코짱", 32, "32곳. ‘짱’으로 끝나는 이름이 여럿 있습니다."],
 ["뽀끼뽀끼2", 22, "2편입니다. 1편도 데이터 어딘가에 있습니다."],
 ["씨로켓", 27, "27곳. 바다와 로켓이 붙었습니다."],
 ["손오공연대기", 26, "26곳. 서유기가 인형뽑기 기계가 되었습니다."],
 ["신 사대천왕", 24, "24곳. ‘신(新)’이 붙었다는 건 앞 세대가 있었다는 뜻입니다."],
 ["씨앤드래곤3알파", 23, "23곳. 3편의 알파 버전입니다."],
 ["마켓크레프트3", 22, "22곳. 이것도 3편입니다."],
 ["오바센스", 21, "21곳. 소리 내어 읽으면 뜻이 짐작됩니다."],
 ["놀러와", 21, "21곳. 기계 이름이 권유형입니다."],
 ["민속윷놀이", 21, "21곳. 오락실 기계 목록에 민속놀이가 있습니다."],
 ["레전드 오브 히어로", 21, "21곳. 영어를 한글로 옮겨 적었습니다."],
 ["골든오션플러스", 21, "21곳. ‘플러스’가 붙은 판본입니다."],
 ["토이즈팝", 189, "가장 흔한 기계 이름. 189곳이 적었습니다."],
 ["스마일토이", 34, "34곳. 띄어 쓴 ‘스마일 토이’도 31곳 따로 있습니다."],
 ["우미", 34, "34곳. 두 글자짜리 이름입니다."],
 ["청소년게임제공업", 23, "취급품목 칸에 업종 이름을 그대로 옮겨 적은 경우입니다."],
 ["전체이용가", 40, "취급품목 칸에 등급을 적었습니다. 옆 칸의 답입니다."]
];

const YEARS = [
 [2005,9],[2006,5],[2007,830],[2008,2932],[2009,3395],[2010,1762],[2011,1754],
 [2012,1394],[2013,1055],[2014,798],[2015,948],[2016,2484],[2017,3851],[2018,1870],
 [2019,1662],[2020,860],[2021,499],[2022,381],[2023,369],[2024,885],[2025,1823],[2026,1114]
];

const $ = s => document.querySelector(s);
const nf = n => n.toLocaleString("ko-KR");

/* 열람기 */
const seal = $("#seal");
let seen = new Set(), cur = 0;
function pick(){
  if (seen.size >= ITEMS.length) seen.clear();
  let i; do { i = Math.floor(Math.random()*ITEMS.length); } while (seen.has(i));
  seen.add(i); cur = i;
  const [name, cnt, note] = ITEMS[i];
  $("#q-cat").textContent = "전국 " + nf(cnt) + "곳이 적음";
  $("#q-text").textContent = name;
  $("#q-meta").textContent = note;
  ["#q-cat","#q-text","#q-meta"].forEach(s => {
    const n = $(s); n.classList.remove("fade"); void n.offsetWidth; n.classList.add("fade");
  });
  seal.classList.remove("go"); void seal.offsetWidth; seal.classList.add("go");
  $("#tally").textContent = "열람 " + seen.size + " / " + ITEMS.length;
}
$("#draw").addEventListener("click", pick);
$("#copy").addEventListener("click", async e => {
  const [name, , note] = ITEMS[cur], b = e.currentTarget;
  try {
    await navigator.clipboard.writeText(
      "「" + name + "」\n\n" + note + "\n출처: 청소년게임제공업 · LOCALDATA\n— 세모지");
    b.textContent = "복사됨";
  } catch { b.textContent = "복사 실패"; }
  setTimeout(() => { b.textContent = "복사"; }, 1500);
});

/* 툴팁 */
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

/* 낱말 막대 */
const maxW = Math.max(...WORDS.map(r => r[1]));
$("#words").innerHTML = WORDS.map(([w, n]) =>
  '<div class="hrow" data-t="‘' + w + '’ — ' + nf(n) + '곳">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (n / maxW * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + nf(n) + '곳</span></div>').join("");

$("#counts").innerHTML = COUNTS.map(([t, n]) =>
  '<div><b>' + t + '</b><span>' + nf(n) + '곳</span></div>').join("");

/* 연도 막대 */
const maxY = Math.max(...YEARS.map(r => r[1]));
$("#years").innerHTML = YEARS.map(([y, n]) => {
  const peak = y === 2017;
  const tag = peak ? '<span class="tag">2017년 ' + nf(n) + '곳</span>' : "";
  return '<span class="col' + (peak ? " peak" : "") + '" data-t="' + y + '년 — 신규 ' + nf(n) + '곳"' +
    ' style="height:' + Math.max(n / maxY * 100, 1.2) + '%">' + tag + '</span>';
}).join("");
const AXIS = [2005, 2009, 2013, 2017, 2021, 2026];
$("#yaxis").innerHTML = AXIS.map((y, k) => {
  const i = YEARS.findIndex(r => r[0] === y);
  const pct = (i + 0.5) / YEARS.length * 100;
  const cls = k === 0 ? ' class="first"' : k === AXIS.length - 1 ? ' class="last"' : "";
  return '<span' + cls + ' style="left:' + pct.toFixed(2) + '%">' + y + '</span>';
}).join("");
$("#ytbl").querySelector("tbody").innerHTML =
  YEARS.map(([y, n]) => '<tr><td>' + y + '</td><td>' + nf(n) + '</td></tr>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
pick();
</script>
"""

out = ROOT / "game.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY, encoding="utf-8")
print(f"game.html 작성 완료 — {out.stat().st_size:,} bytes")
