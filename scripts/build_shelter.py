"""
제11호 「사백십만 명」(shelter/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_shelter.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_shelter.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

HEAD = """<title>사백십만 명</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="민방위대피소 18,833곳 가운데 가장 큰 곳의 수용인원은 410만 명으로 등록돼 있다. 그 시설의 면적도 같은 숫자다.">
<meta name="naver-site-verification" content="e1aa1ef1b15b68297398065f83c4c5a96d1f3d0d" />
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5277473094749097"
     crossorigin="anonymous"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@400;600;800&family=IBM+Plex+Sans+KR:wght@300;400;500;600&family=Nanum+Gothic+Coding:wght@400;700&display=swap">
"""

EXTRA_STYLE = """<style>
/* 제11호 전용 */
.pair-box{padding:36px var(--pad) 32px;margin:66px 0 0}
.pair-q{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;color:var(--muted);margin:0 0 22px}
.pair-grid{display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--rule)}
.pair-cell{padding:24px 20px 22px 0;border-right:1px solid var(--rule-2)}
.pair-cell:last-child{border-right:0}
.pair-cell .lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.13em;color:var(--muted)}
.pair-cell .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(26px,4.6vw,40px);line-height:1.05;margin-top:12px;
  font-variant-numeric:tabular-nums;word-break:break-all}
.pair-cell.on .n{color:var(--seal-ink)}
.pair-cell .s{display:block;font-size:13.5px;color:var(--ink-2);font-weight:300;margin-top:10px}
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
.big-li{border-top:1px solid var(--rule);margin-top:6px}
.big-li div{display:grid;grid-template-columns:minmax(0,1fr) minmax(96px,auto) minmax(96px,auto);
  gap:14px;padding:11px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.big-li .nm{font-size:14px;word-break:keep-all}
.big-li .c{font-family:var(--f-mono);font-size:12.5px;color:var(--seal-ink);
  text-align:right;font-variant-numeric:tabular-nums}
.big-li .a{font-family:var(--f-mono);font-size:12.5px;color:var(--muted);
  text-align:right;font-variant-numeric:tabular-nums}
@media (max-width:600px){.big-li div{grid-template-columns:1fr auto}.big-li .a{display:none}}
.tunnels{display:flex;flex-wrap:wrap;gap:10px;margin-top:6px}
.tunnels span{font-family:var(--f-display);font-weight:600;font-size:16px;
  border:1px solid var(--rule);background:var(--card);padding:9px 15px}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제11호 열람실</span>
    <span>원자료 <b>전국민방위대피시설표준데이터</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제11호 열람실 · 민방위대피소 지정 기록</p>
    <h1>사백십만 명</h1>
    <p class="lede">
      전국에 지정된 민방위대피소는 <b>18,833곳</b>입니다.
      그중 수용인원이 가장 많은 곳은 서울의 한 아파트 지하주차장으로,
      <b>4,105,106명</b>이 들어간다고 등록돼 있습니다. 대한민국 인구의 8%입니다.
      같은 줄의 시설면적 칸에는 <b>4,105,106㎡</b>라고 적혀 있습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">18,833</span><span class="l">지정된 대피소</span><span class="s">사용 중 17,238곳</span></div>
      <div class="fig hot"><span class="n">98.7%</span><span class="l">인원 = 면적</span><span class="s">두 칸의 숫자가 같음</span></div>
      <div class="fig"><span class="n">2,970</span><span class="l">수용인원 중앙값</span><span class="s">최소 21명</span></div>
      <div class="fig"><span class="n">64.5%</span><span class="l">이름에 ‘주차장’</span><span class="s">‘아파트’는 50.4%</span></div>
    </div>
  </div>

  <article class="form pair-box">
    <span class="form-label">민방위대피시설 등록 · 같은 줄의 두 칸</span>
    <p class="pair-q">서울 강북구의 한 아파트 지하주차장</p>
    <div class="pair-grid">
      <div class="pair-cell on">
        <span class="lab">최대수용인원</span>
        <span class="n">4,105,106명</span>
        <span class="s">대한민국 인구의 8%가 이 주차장 한 곳에 들어갑니다.</span>
      </div>
      <div class="pair-cell">
        <span class="lab">시설면적</span>
        <span class="n">4,105,106㎡</span>
        <span class="s">4.1㎢. 여의도 면적의 절반에 가깝습니다.</span>
      </div>
    </div>
    <p class="say">
      <b>두 칸의 숫자가 완전히 같습니다.</b> 우연이 아닙니다.
      전체 18,833곳 가운데 <b>18,584곳(98.7%)</b>에서 이 두 값이 같거나 소수점만 다릅니다.
      1인당 1㎡로 계산하는 규칙일 수도 있고, 칸을 그대로 옮겨 적은 것일 수도 있습니다.
      <b>어느 쪽인지는 원본 어디에도 적혀 있지 않습니다.</b>
      확실한 건 하나뿐입니다 — 면적이 틀리면 인원도 같이 틀립니다.
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>수용인원 상위 여덟 곳</h2><span>인원과 면적을 나란히</span></div>
    <p class="blk-note">
      왼쪽이 등록된 수용인원, 오른쪽이 같은 줄의 면적입니다.
      <b>10만 명이 넘는 곳이 69곳</b>, 1만 명이 넘는 곳이 3,928곳입니다.
      전부 아파트 지하주차장이거나 학교 체육관입니다.
    </p>
    <div class="big-li" id="tops"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>민방위대피소의 실체</h2><span>시설명 낱말 빈도</span></div>
    <p class="blk-note">
      시설명에 <b>‘주차장’이 들어간 곳이 64.5%</b>, ‘아파트’가 50.4%입니다.
      전국 민방위대피소의 실체는 <b>아파트 지하주차장</b>입니다.
      가장 흔한 이름은 「현대아파트 지하주차장 1층」으로 18곳이 같은 이름을 씁니다.
    </p>
    <div class="hbars" id="words"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>지상에 있는 대피소 143곳</h2><span>지하 18,690곳</span></div>
    <p class="blk-note">
      「시설위치(지상/지하)」 칸은 답이 둘뿐입니다. 18,690곳이 지하이고
      <b>143곳이 지상</b>입니다. 그 143곳에는 학교 강당과 교회 교육실이 있고,
      <b>터널이 여섯 개</b> 있습니다. 터널은 산을 뚫은 것이니 머리 위에 흙이 있지만,
      서식은 지상이라고 적게 했습니다.
    </p>
    <div class="tunnels" id="tunnels"></div>
    <p class="say">143곳 중 <b>52곳은 이미 사용중지</b> 상태입니다. 91곳만 살아 있습니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>언제 지정했나</h2><span>연도별 신규 지정</span></div>
    <p class="blk-note">
      1970년대에는 한 해 한 자릿수였다가 1990년대부터 늘어납니다.
      <b>2010년 1,379곳</b>으로 정점을 찍고 2011년 1,173곳이 뒤를 잇습니다.
      그 뒤로는 연 300~600곳 수준입니다. 데이터는 언제 몇 곳을 지정했는지만 알려줍니다.
    </p>
    <div class="cols" id="years"></div>
    <div class="axis" id="yaxis"></div>
    <details class="tbl">
      <summary>표로 보기</summary>
      <div class="scroll"><table id="ytbl"><thead><tr><th>연도</th><th>지정</th></tr></thead><tbody></tbody></table></div>
    </details>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">지정일자 2206-06-17</span>
        <p class="b">180년 뒤에 지정될 예정인 대피소가 한 곳 있습니다.</p>
        <p class="c">그런데 운영상태는 「사용중」입니다. 아직 지정되지 않았는데 쓰이는 중입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">지정일자 1967-12-04</span>
        <p class="b">민방위대가 창설되기 8년 전에 지정된 대피소가 있습니다.</p>
        <p class="c">한 초등학교의 지하주차장입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">시설구분 빈칸</span>
        <p class="b">「공공용시설」도 「정부지원시설」도 아닌 곳이 13곳 있습니다.</p>
        <p class="c">둘 중 하나를 고르는 칸인데 비어 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">이름 18,461가지</span>
        <p class="b">18,833곳의 이름이 18,461가지입니다. 거의 전부 다릅니다.</p>
        <p class="c">「○○아파트 지하주차장 1층」이라는 틀은 같은데 앞의 이름만 바뀝니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제11호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>전국민방위대피시설표준데이터</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 18,833행 기준<br>개별 대피소의 실제 수용 능력이나 안전 여부는 다루지 않았습니다. 등록된 값만 옮겼습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 18,833행에서 계산했습니다. scripts/analyze_shelter.py 로 재현됩니다. */

const TOPS = [
 ["삼각산아이원아파트 주차장(104,105,106-지하3)", 4105106, "4,105,106"],
 ["아영초다목적체육관", 1308885, "1,308,885"],
 ["파크리오아파트 지하주차장(전체 동의 지하 1~2층)", 361211, "361,211"],
 ["올림픽파크포레온 1~3단지 지하주차장(지하2층,3층)", 335600, "335,600.91"],
 ["헬리오시티 전체 동의 지하주차장 2층 ~ 3층", 327436, "327,436.86"],
 ["리센츠아파트 전체 동의 지하주차장 지하 1,2층", 308775, "308,775"],
 ["한마을아파트(지하주차장1~2층)", 279901, "279,901"],
 ["래미안힐스테이트 고덕(지하1~3층 주차장)", 261492, "261,492"]
];

const WORDS = [
 ["주차장", 12140, 64.5], ["아파트", 9499, 50.4], ["센터", 718, 3.8],
 ["빌딩", 412, 2.2], ["학교", 337, 1.8], ["교회", 206, 1.1],
 ["회관", 176, 0.9], ["상가", 168, 0.9], ["터널", 11, 0.1]
];

const TUNNELS = ["북악터널", "자하문터널", "구기터널", "구덕터널", "대티터널", "영동와인터널"];

const YEARS = [[1970,3],[1971,1],[1972,2],[1973,2],[1974,2],[1975,9],[1976,6],[1977,7],[1978,10],[1979,26],[1980,38],[1981,26],[1982,26],[1983,31],[1984,49],[1985,53],[1986,51],[1987,68],[1988,115],[1989,119],[1990,214],[1991,285],[1992,337],[1993,428],[1994,498],[1995,567],[1996,579],[1997,535],[1998,657],[1999,508],[2000,470],[2001,553],[2002,612],[2003,966],[2004,412],[2005,556],[2006,416],[2007,395],[2008,541],[2009,505],[2010,1379],[2011,1173],[2012,419],[2013,587],[2014,269],[2015,298],[2016,580],[2017,561],[2018,405],[2019,345],[2020,324],[2021,332],[2022,294],[2023,475],[2024,260],[2025,335],[2026,116]];

const $ = s => document.querySelector(s);
const nf = n => n.toLocaleString("ko-KR");

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

/* 상위 목록 */
$("#tops").innerHTML = TOPS.map(([nm, cap, area]) =>
  '<div data-t="' + nm + ' — ' + nf(cap) + '명 / ' + area + '㎡">' +
  '<span class="nm">' + nm + '</span>' +
  '<span class="c">' + nf(cap) + '명</span>' +
  '<span class="a">' + area + '㎡</span></div>').join("");

/* 낱말 막대 */
const maxW = WORDS[0][1];
$("#words").innerHTML = WORDS.map(([w, n, pct]) =>
  '<div class="hrow" data-t="‘' + w + '’ — ' + nf(n) + '곳 (' + pct + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (n / maxW * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + pct + '% · ' + nf(n) + '</span></div>').join("");

$("#tunnels").innerHTML = TUNNELS.map(t => '<span>' + t + '</span>').join("");

/* 연도 막대 */
const maxY = Math.max(...YEARS.map(r => r[1]));
$("#years").innerHTML = YEARS.map(([y, n]) => {
  const peak = y === 2010;
  const tag = peak ? '<span class="tag">2010년 ' + nf(n) + '곳</span>' : "";
  return '<span class="col' + (peak ? " peak" : "") + '" data-t="' + y + '년 — ' + nf(n) + '곳 지정"' +
    ' style="height:' + Math.max(n / maxY * 100, 0.8) + '%">' + tag + '</span>';
}).join("");
const AXIS = [1970, 1985, 1998, 2010, 2026];
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
"""

out_dir = ROOT / "shelter"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n", encoding="utf-8")
print(f"shelter/index.html 작성 완료 — {out.stat().st_size:,} bytes")
