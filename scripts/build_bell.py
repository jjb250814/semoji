"""
제9호 「약자보호」(bell.html) 조립기.

공용 CSS는 bike.html의 첫 <style> 블록을 그대로 물려받는다.
열람실 스타일을 한 벌로 유지하기 위해서다. 숫자는 전부
scripts/analyze_bell.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_bell.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

HEAD = """<title>약자보호</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="안전비상벨 88,634개는 설치목적 칸에서 방범용·약자보호·기타 중 하나를 골라야 했다. 약자가 누구인지는 서식이 말하지 않는다.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@400;600;800&family=IBM+Plex+Sans+KR:wght@300;400;500;600&family=Nanum+Gothic+Coding:wght@400;700&display=swap">
"""

EXTRA_STYLE = """<style>
/* 제9호 전용 */
.player-grid.three{grid-template-columns:1fr 1fr 1fr}
@media (max-width:640px){.player-grid.three{grid-template-columns:1fr}
  .player-grid.three .player-cell{border-right:0;border-bottom:1px solid var(--rule-2)}
  .player-grid.three .player-cell:last-child{border-bottom:0}}
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
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
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="./index.html">← 세모지</a> · 제9호 열람실</span>
    <span>원자료 <b>안전비상벨</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제9호 열람실 · 안전비상벨 등록 기록</p>
    <h1>약자보호</h1>
    <p class="lede">
      전국에 등록된 안전비상벨은 <b>88,634개</b>입니다. 등록할 때 「설치목적」 칸에서
      셋 중 하나를 골라야 합니다. <b>방범용, 약자보호, 기타.</b>
      4,625개가 &lsquo;약자보호&rsquo;로 등록됐습니다.
      약자가 누구인지는 서식이 말하지 않습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">88,634</span><span class="l">전체 등록</span><span class="s">2004년 이후 기록</span></div>
      <div class="fig"><span class="n">82,447</span><span class="l">방범용</span><span class="s">전체의 93.0%</span></div>
      <div class="fig hot"><span class="n">4,625</span><span class="l">약자보호</span><span class="s">전체의 5.2%</span></div>
      <div class="fig"><span class="n">1,562</span><span class="l">기타</span><span class="s">전체의 1.8%</span></div>
    </div>
  </div>

  <article class="form player">
    <span class="form-label">안전비상벨 등록 · 설치목적</span>
    <p class="player-q">Q. 이 비상벨은 무엇을 위해 설치했습니까</p>
    <div class="player-grid three">
      <div class="player-cell on">
        <span class="box"><span class="tick">&#10003;</span><span class="lab">방범용</span></span>
        <span class="n">82,447</span>
        <span class="s">93.0%. 거의 전부가 이쪽입니다.</span>
      </div>
      <div class="player-cell">
        <span class="box"><span class="tick">&nbsp;</span><span class="lab">약자보호</span></span>
        <span class="n">4,625</span>
        <span class="s">5.2%. 누가 약자인지 적는 칸은 없습니다.</span>
      </div>
      <div class="player-cell">
        <span class="box"><span class="tick">&nbsp;</span><span class="lab">기타</span></span>
        <span class="n">1,562</span>
        <span class="s">1.8%. 둘 다 아니라고 답한 경우입니다.</span>
      </div>
    </div>
    <p class="say">
      셋 중 하나를 반드시 골라야 합니다. 그런데 <b>&lsquo;약자&rsquo;의 정의도,
      &lsquo;방범&rsquo;과의 경계도 원본 어디에도 적혀 있지 않습니다.</b>
      88,634번의 판단이 있었지만 그 기준은 데이터에 남지 않았습니다.
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>약자보호 벨은 어디에 있나</h2><span>4,625개</span></div>
    <p class="blk-note">
      가장 많은 곳은 가로변입니다. 그런데 <b>다섯 중 하나는 화장실에 있습니다.</b>
      전체 비상벨 중 화장실 비중이 8.2%인 것과 견주면 두 배가 넘습니다.
    </p>
    <div class="hbars" id="weak"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>같은 화장실, 다른 목적</h2><span>화장실 벨 7,286개</span></div>
    <p class="blk-note">
      화장실에 달린 비상벨 7,286개 중 <b>6,247개는 &lsquo;방범용&rsquo;</b>으로,
      1,010개는 &lsquo;약자보호&rsquo;로 등록됐습니다. 29개는 &lsquo;기타&rsquo;입니다.
      같은 화장실에 달린 같은 장치인데 목적이 갈립니다.
    </p>
    <div class="two">
      <div>
        <span class="n">85.7%</span>
        <span class="s">화장실 벨 중 &lsquo;방범용&rsquo;으로 등록된 비율.
          나머지 13.9%가 &lsquo;약자보호&rsquo;입니다.</span>
      </div>
      <div>
        <span class="n hot">13곳</span>
        <span class="s">화장실 벨을 등록한 476개 기관 중,
          <b>자기가 관리하는 화장실 벨에 서로 다른 목적을 적은</b> 기관 수입니다.
          한 기관 안에서도 기준이 갈렸습니다.</span>
      </div>
    </div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>넷 중 하나는 「기타」</h2><span>설치장소유형</span></div>
    <p class="blk-note">
      장소도 고르게 되어 있습니다. 가로변·공원·화장실·건물·주차장, 그리고 기타.
      선택지를 다섯 개나 줬는데 <b>21,754개가 &lsquo;기타&rsquo;를 골랐습니다.</b> 전체의 24.5%입니다.
    </p>
    <div class="hbars" id="place"></div>
    <p class="blk-note" style="margin-top:26px">
      그 21,754개가 「설치위치」 칸에는 뭐라고 적었는지 보면, 왜 &lsquo;기타&rsquo;를 골랐는지 짐작됩니다.
    </p>
    <div class="mono-li" id="othersite"></div>
  </section>

  <article class="form reader">
    <span class="form-label">설치위치 열람</span>
    <div class="seal" id="seal" aria-hidden="true"><b>非常</b><i>안전비상벨</i></div>
    <p class="q-cat" id="q-cat">&mdash;</p>
    <p class="q-text" id="q-text">불러오는 중</p>
    <p class="q-meta" id="q-meta">&nbsp;</p>
    <div class="reader-act">
      <button class="btn" id="draw" type="button">다음 위치</button>
      <button class="btn ghost" id="copy" type="button">복사</button>
      <span class="tally" id="tally"></span>
    </div>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>비상벨이 늘어난 속도</h2><span>연도별 설치</span></div>
    <p class="blk-note">
      2006년 336개에서 시작해 <b>2019년 8,069개</b>로 정점을 찍습니다.
      2004년 이전 기록은 아홉 개뿐이라 그래프에서 뺐고, 전체 연도는 표에 남겼습니다.
    </p>
    <div class="cols" id="years"></div>
    <div class="axis" id="yaxis"></div>
    <details class="tbl">
      <summary>표로 보기</summary>
      <div class="scroll"><table id="ytbl"><thead><tr><th>연도</th><th>설치</th></tr></thead><tbody></tbody></table></div>
    </details>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">설치연도 1900</span>
        <p class="b">1900년에 설치된 것으로 기록된 안전비상벨이 한 개 있습니다.</p>
        <p class="c">서울 강북구청이 관리하는 가로변 비상벨입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">설치연도 빈칸</span>
        <p class="b">언제 설치했는지 적히지 않은 벨이 34개 있습니다.</p>
        <p class="c">대부분 화장실 벨이고, 한 군(郡)의 면 행정복지센터들에 몰려 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">부가기능 86가지</span>
        <p class="b">「경보등 + 경보음」과 「경보등+경보음」이 서로 다른 값으로 세어집니다.</p>
        <p class="c">공백만 지우면 86가지가 78가지로 줄어듭니다. 여덟 가지가 띄어쓰기 차이였습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">CCTV 관제센터 연계</span>
        <p class="b">이 한 가지 기능을 적는 방법이 네 가지입니다.</p>
        <p class="c">「CCTV 관제센터 연계」 「CCTV 관제센터연계」 「CCTV관제센터 연계」 「CCTV관제센터연계」.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="./index.html">세모지로 돌아가기 &rarr;</a> · 제9호 열람실 · <a href="./about.html">소개</a> · <a href="./contact.html">연락처</a> · <a href="./privacy.html">개인정보처리방침</a></span>
    <span>출처 <b>안전비상벨</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 88,634행 기준<br>개별 비상벨의 위치와 작동 상태는 다루지 않았습니다. 집계값만 실었습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 88,634행에서 계산했습니다. scripts/analyze_bell.py 로 재현됩니다. */

const WEAK = [
 ["가로변", 1643, 35.5], ["기타", 1023, 22.1], ["화장실", 1010, 21.8],
 ["공원", 776, 16.8], ["건물", 169, 3.7], ["주차장", 4, 0.1]
];

const PLACE = [
 ["가로변", 48684, 54.9], ["기타", 21754, 24.5], ["공원", 9430, 10.6],
 ["화장실", 7286, 8.2], ["건물", 1116, 1.3], ["주차장", 364, 0.4]
];

const OTHERSITE = [
 ["경기도 파주시", 1725],
 ["주택가·도로·골목길·공원·어린이보호구역 등", 1231],
 ["CCTV폴대", 976],
 ["주택가", 47],
 ["인천광역시 연수구 연수동 636", 37],
 ["일반주택가", 37],
 ["삼거리", 32],
 ["어린이공원", 30]
];

const SITES = [
 ["CCTV폴대", 2385, "위치를 물었는데 무엇에 붙어 있는지를 답했습니다. 가장 흔한 답입니다."],
 ["CCTV", 2112, "더 줄인 형태. 앞의 것과 합치면 4,497개입니다."],
 ["경기도 파주시", 1725, "시 전체가 위치로 적혔습니다. 파주시 어딘가에 있습니다."],
 ["가로변", 1295, "「설치장소유형」 칸에 이미 있는 답을 위치 칸에 옮겨 적었습니다."],
 ["주택가·도로·골목길·공원·어린이보호구역 등", 1231, "다섯 곳을 나열하고 ‘등’으로 닫았습니다."],
 ["-", 578, "적지 않겠다는 뜻으로 보입니다."],
 ["쌍용동", 156, "동 이름만 적힌 것들. 천안시 관내에 몰려 있습니다."],
 ["공중화장실 내부", 122, "여기까지가 구체적인 편입니다."],
 ["여자화장실 내", 119, "‘내’로 끝나는 표현이 여럿 있습니다."],
 ["삼거리", 32, "어느 삼거리인지는 적히지 않았습니다."],
 ["어린이공원", 30, "이름 없는 어린이공원 서른 곳."],
 ["서울시 종로구 보건소  화장실", 16, "공백이 두 칸 들어가 있어 다른 표기와 따로 세어집니다."]
];

const YEARS = [
 [2004,29],[2005,36],[2006,336],[2007,430],[2008,697],[2009,1611],[2010,2702],
 [2011,2278],[2012,2021],[2013,4109],[2014,2835],[2015,4615],[2016,7354],
 [2017,7628],[2018,7594],[2019,8069],[2020,6951],[2021,5862],[2022,5608],
 [2023,7088],[2024,6685],[2025,3109],[2026,944]
];
const YEARS_ALL = [[1900,1],[1995,1],[1996,1],[2001,2],[2002,1],[2003,3]].concat(YEARS);

const $ = s => document.querySelector(s);
const nf = n => n.toLocaleString("ko-KR");

/* 열람기 */
const seal = $("#seal");
let seen = new Set(), cur = 0;
function pick(){
  if (seen.size >= SITES.length) seen.clear();
  let i; do { i = Math.floor(Math.random()*SITES.length); } while (seen.has(i));
  seen.add(i); cur = i;
  const [name, cnt, note] = SITES[i];
  $("#q-cat").textContent = "같은 표현 " + nf(cnt) + "곳";
  $("#q-text").textContent = name;
  $("#q-meta").textContent = note;
  ["#q-cat","#q-text","#q-meta"].forEach(s => {
    const n = $(s); n.classList.remove("fade"); void n.offsetWidth; n.classList.add("fade");
  });
  seal.classList.remove("go"); void seal.offsetWidth; seal.classList.add("go");
  $("#tally").textContent = "열람 " + seen.size + " / " + SITES.length;
}
$("#draw").addEventListener("click", pick);
$("#copy").addEventListener("click", async e => {
  const [name, , note] = SITES[cur], b = e.currentTarget;
  try {
    await navigator.clipboard.writeText(
      "「" + name + "」\n\n" + note + "\n출처: 안전비상벨 · LOCALDATA\n— 세모지");
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

function bars(target, rows, unit){
  const max = Math.max(...rows.map(r => r[1]));
  $(target).innerHTML = rows.map(([k, n, pct]) =>
    '<div class="hrow" data-t="' + k + ' — ' + nf(n) + unit + ' (' + pct + '%)">' +
    '<span class="cat">' + k + '</span>' +
    '<span class="track"><span class="bar" data-w="' + (n / max * 100).toFixed(1) + '"></span></span>' +
    '<span class="val">' + pct + '% · ' + nf(n) + '</span></div>').join("");
}
bars("#weak", WEAK, "개");
bars("#place", PLACE, "개");

$("#othersite").innerHTML = OTHERSITE.map(([t, n]) =>
  '<div><b>' + t + '</b><span>' + nf(n) + '개</span></div>').join("");

/* 연도 막대 */
const maxY = Math.max(...YEARS.map(r => r[1]));
$("#years").innerHTML = YEARS.map(([y, n]) => {
  const peak = y === 2019;
  const tag = peak ? '<span class="tag">2019년 ' + nf(n) + '개</span>' : "";
  return '<span class="col' + (peak ? " peak" : "") + '" data-t="' + y + '년 — ' + nf(n) + '개 설치"' +
    ' style="height:' + Math.max(n / maxY * 100, 1.2) + '%">' + tag + '</span>';
}).join("");
const AXIS = [2004, 2010, 2015, 2019, 2026];
$("#yaxis").innerHTML = AXIS.map((y, k) => {
  const i = YEARS.findIndex(r => r[0] === y);
  const pct = (i + 0.5) / YEARS.length * 100;
  const cls = k === 0 ? ' class="first"' : k === AXIS.length - 1 ? ' class="last"' : "";
  return '<span' + cls + ' style="left:' + pct.toFixed(2) + '%">' + y + '</span>';
}).join("");
$("#ytbl").querySelector("tbody").innerHTML =
  YEARS_ALL.map(([y, n]) => '<tr><td>' + y + '</td><td>' + nf(n) + '</td></tr>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
pick();
</script>
"""

out = ROOT / "bell.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY, encoding="utf-8")
print(f"bell.html 작성 완료 — {out.stat().st_size:,} bytes")
