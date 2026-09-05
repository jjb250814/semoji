"""
제12호 「일반이용업」(barbershop/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_barber.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_barber.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("이발관, 이용원, 바버샵. 간판은 세 번 바뀌었지만 서류의 업태 칸은 "
        "65,845곳 중 65,396곳이 60년째 「일반이용업」이다.")

HEAD = """<title>일반이용업</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/barbershop/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="일반이용업 — 세모지 제12호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/barbershop/">
<meta property="og:image" content="https://semoji.net/og/barbershop.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="일반이용업 — 세모지 제12호 열람실">
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
/* 제12호 전용 */
.trio{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
  border-top:1px solid var(--rule);margin-top:22px}
.trio > div{padding:22px 18px 20px 0;border-right:1px solid var(--rule-2)}
.trio > div:last-child{border-right:0}
.trio .lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.13em;color:var(--muted)}
.trio .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(24px,4vw,34px);line-height:1.05;margin-top:11px;
  font-variant-numeric:tabular-nums}
.trio > div.on .n{color:var(--seal-ink)}
.trio .s{display:block;font-size:13px;color:var(--ink-2);font-weight:300;margin-top:9px}
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
.signs{border-top:1px solid var(--rule);margin-top:6px}
.signs div{display:grid;
  grid-template-columns:minmax(0,1fr) minmax(84px,auto) minmax(92px,auto) minmax(86px,auto);
  gap:12px;padding:12px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.signs .nm{font-family:var(--f-display);font-weight:600;font-size:16px}
.signs div.on .nm{color:var(--seal-ink)}
.signs .c,.signs .y,.signs .a{font-family:var(--f-mono);font-size:12.5px;
  text-align:right;font-variant-numeric:tabular-nums}
.signs .c{color:var(--ink-2)}
.signs .y{color:var(--seal-ink)}
.signs .a{color:var(--muted)}
.signs .hd{border-bottom:1px solid var(--rule)}
.signs .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;
  color:var(--muted);font-weight:400}
@media (max-width:620px){
  .signs div{grid-template-columns:1fr auto auto}
  .signs .a{display:none}
}
.era{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  border-top:1px solid var(--rule);margin-top:6px}
.era > div{padding:22px 16px 20px 0;border-right:1px solid var(--rule-2)}
.era > div:last-child{border-right:0}
.era .p{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--muted)}
.era .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(28px,4.6vw,40px);line-height:1;margin-top:12px;
  font-variant-numeric:tabular-nums}
.era > div.on .n{color:var(--seal-ink)}
.era .s{display:block;font-size:12.5px;color:var(--muted);font-weight:300;margin-top:10px}
.pair-grid{display:grid;grid-template-columns:1fr 1fr;
  border-top:1px solid var(--rule);margin-top:22px}
.pair-cell{padding:24px 20px 22px 0;border-right:1px solid var(--rule-2)}
.pair-cell:last-child{border-right:0}
.pair-cell .lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.13em;color:var(--muted)}
.pair-cell .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(24px,4.2vw,34px);line-height:1.05;margin-top:12px;
  font-variant-numeric:tabular-nums}
.pair-cell.on .n{color:var(--seal-ink)}
.pair-cell .s{display:block;font-size:13.5px;color:var(--ink-2);font-weight:300;margin-top:10px}
.pair-cell .s b{font-weight:500;color:var(--ink)}
@media (max-width:560px){.pair-grid{grid-template-columns:1fr}
  .pair-cell{border-right:0;border-bottom:1px solid var(--rule-2)}
  .pair-cell:last-child{border-bottom:0}}
.caveat{border:1px solid var(--rule);background:var(--card);
  padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제12호 열람실</span>
    <span>원자료 <b>이용원</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제12호 열람실 · 이용원 인허가 기록</p>
    <h1>일반이용업</h1>
    <p class="lede">
      간판은 <b>이발관</b>에서 <b>이용원</b>으로, 다시 <b>바버샵</b>으로 바뀌었습니다.
      그런데 허가 서류의 업태 칸은 65,845곳 가운데 <b>65,396곳(99.3%)</b>이
      똑같이 「일반이용업」입니다. 1953년에 낸 서류에도, 2026년에 낸 서류에도
      같은 다섯 글자가 적혀 있습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">65,845</span><span class="l">누적 등록</span><span class="s">영업 중 14,931곳</span></div>
      <div class="fig"><span class="n">99.3%</span><span class="l">「일반이용업」</span><span class="s">서류가 부르는 이름은 하나</span></div>
      <div class="fig hot"><span class="n">27.4%</span><span class="l">최근 신규 중 ‘바버샵’</span><span class="s">1990년대엔 0.1%</span></div>
      <div class="fig"><span class="n">6.7년</span><span class="l">버틴 기간 중앙값</span><span class="s">10년 넘긴 곳 39.2%</span></div>
    </div>
  </div>

  <article class="form">
    <span class="form-label">이용업 영업신고서 · 업태구분명</span>
    <p class="q-text" style="margin-top:20px">Q. 귀 업소의 업태는 무엇입니까</p>
    <div class="trio">
      <div class="on">
        <span class="lab">일반이용업</span>
        <span class="n">65,396</span>
        <span class="s">전체의 99.3%. 사실상 답이 하나뿐인 질문입니다.</span>
      </div>
      <div>
        <span class="lab">이용업 기타</span>
        <span class="n">425</span>
        <span class="s">0.6%. 무엇이 ‘기타’인지는 적혀 있지 않습니다.</span>
      </div>
      <div>
        <span class="lab">일반미용업</span>
        <span class="n">23</span>
        <span class="s">이용원 파일에 섞여 들어온 미용업 23곳입니다.</span>
      </div>
    </div>
    <p class="say">
      「위생업태명」이라는 칸이 하나 더 있는데 값이 <b>똑같습니다</b>
      (일반이용업 65,394 · 이용업 기타 425 · 일반미용업 23).
      같은 것을 두 번 묻고 두 번 같은 답을 받습니다.
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>간판이 부르는 이름은 여섯 가지</h2><span>상호에 들어간 낱말</span></div>
    <p class="blk-note">
      서류는 전부 「일반이용업」이지만 가게가 스스로 붙인 이름은 갈립니다.
      가장 많은 것은 <b>이용원</b>(23,972곳)이고, 가장 늦게 나타난 것이
      <b>바버샵</b>(1,642곳)입니다. 가운데 붉은 숫자는 그 이름을 쓰는 가게들이
      허가받은 해의 중앙값입니다.
    </p>
    <div class="signs" id="signs"></div>
    <p class="say">
      <b>이발관은 1997년, 바버샵은 2022년.</b> 스물다섯 해 차이입니다.
      아직 영업 중인 비율도 갈립니다 — 이발관은 넷 중 하나(23.4%)만 살아 있고,
      바버샵은 넷 중 셋(74.7%)이 살아 있습니다. 최근에 생겼으니 당연한 일입니다.
      <b>이상한 건 「이발소」입니다.</b> 가장 오래된 낱말인데 중앙값이 2009년으로
      이발관보다 열두 해 뒤입니다. 한 번 밀려났던 옛말을 새로 여는 가게가 다시 꺼내 씁니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>「바버샵」이 나타난 해</h2><span>그해 신규 등록 중 비중</span></div>
    <p class="blk-note">
      막대 하나가 그해 새로 허가받은 이용원 중 상호에 ‘바버’가 들어간 비율입니다.
      2016년까지 2%를 넘지 않다가 <b>2019년 12.5%</b>, <b>2021년 25.2%</b>로 뜁니다.
      <b>2023년 30.8%</b>가 가장 높습니다.
    </p>
    <div class="cols" id="years"></div>
    <div class="axis" id="yaxis"></div>
    <details class="tbl">
      <summary>표로 보기</summary>
      <div class="scroll"><table id="ytbl"><thead><tr><th>연도</th><th>바버샵</th><th>그해 신규</th><th>비중</th></tr></thead><tbody></tbody></table></div>
    </details>
    <p class="say">
      2026년은 여덟 달치입니다(원본을 2026-09-03에 받았습니다).
      비율이라 다른 해와 견줄 수는 있지만, 곳수는 아직 한 해가 안 끝난 숫자입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>시기별로 갈라 보면</h2><span>신규 등록 중 ‘바버샵’ 비중</span></div>
    <p class="blk-note">
      네 시기로 잘라 보면 변화가 한눈에 들어옵니다.
      1990년대에는 <b>천 곳에 한 곳도 되지 않았고</b>(14,906곳 중 11곳),
      지금은 <b>넷 중 하나</b>입니다.
    </p>
    <div class="era">
      <div><span class="p">1990~1999</span><span class="n">0.1%</span><span class="s">신규 14,906곳 중 11곳</span></div>
      <div><span class="p">2000~2009</span><span class="n">0.1%</span><span class="s">신규 21,559곳 중 27곳</span></div>
      <div><span class="p">2010~2019</span><span class="n">2.9%</span><span class="s">신규 9,181곳 중 264곳</span></div>
      <div class="on"><span class="p">2021~2026</span><span class="n">27.4%</span><span class="s">신규 4,346곳 중 1,191곳</span></div>
    </div>
    <p class="say">
      같은 기간 <b>이발관은 20.2%에서 4.7%</b>로 줄었습니다 (3,014곳 → 205곳).
      전체 신규 등록 자체도 줄었습니다 — 1998년 2,135곳에서 2025년 730곳입니다.
      가게 수는 줄고, 새로 여는 가게가 부르는 이름은 바뀌었습니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">이 데이터로 말할 수 없는 것</span>
    <p>
      데이터에 적힌 상호는 <b>지금의 이름</b>이고, 날짜는 <b>처음 허가받은 날</b>입니다.
      그 사이에 간판을 몇 번 바꿔 달았는지는 <b>어디에도 적혀 있지 않습니다.</b>
      그래서 위 숫자는 “그해에 바버샵이라는 이름으로 문을 열었다”가 아니라
      “그해에 허가받은 가게 중 지금(또는 문 닫을 때) 이름이 바버샵인 곳”이라는 뜻입니다.
      가장 이른 바버샵으로 기록된 곳은 <b>1973년에 허가</b>받아 아직 영업 중인데,
      그 가게가 1973년에도 바버샵이었는지는 알 수 없습니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>서식이 묻는 두 가지</h2><span>의자수 · 침대수</span></div>
    <p class="blk-note">
      영업신고서에는 설비를 적는 칸이 둘 있습니다. <b>의자 수</b>와 <b>침대 수</b>입니다.
      이발소에 의자가 몇 개인지 묻는 건 자연스럽습니다. 그 옆 칸이 문제입니다.
    </p>
    <div class="pair-grid">
      <div class="pair-cell">
        <span class="lab">의자수</span>
        <span class="n">57,375곳 응답</span>
        <span class="s">전체의 87.1%가 채웠습니다. 중앙값 3개, 가장 흔한 답은 2개(16,606곳)입니다.
          이발소는 대개 의자 두세 개짜리 가게입니다.</span>
      </div>
      <div class="pair-cell on">
        <span class="lab">침대수</span>
        <span class="n">20,096곳이 「0」</span>
        <span class="s">채운 곳은 20,269곳뿐이고, 그중 <b>99.1%가 0이라고 적었습니다.</b>
          하나라도 있다고 답한 곳은 173곳입니다.</span>
      </div>
    </div>
    <p class="say">
      <b>왜 이발소에 침대 수를 묻는지는 데이터 어디에도 적혀 있지 않습니다.</b>
      서식이 만들어진 사정을 짐작해 볼 수는 있지만 원본에 근거가 없으므로 적지 않습니다.
      확실한 것은 둘뿐입니다 — 칸이 있었고, 답은 거의 전부 0이었습니다.
      2만 곳이 「없음」이라고 답하기 위해 이 칸을 채웠습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">인허가일자 1900-01-01</span>
        <p class="b">스물한 곳이 1900년 1월 1일에 허가받은 것으로 적혀 있습니다.</p>
        <p class="c">날짜를 모르는 칸에 들어간 기본값으로 보입니다. 스물한 곳 모두 이미 폐업했습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">인허가일자 1901-11-07</span>
        <p class="b">대한제국 시기에 허가받은 이용원이 한 곳 있습니다.</p>
        <p class="c">1904년, 1928년, 1930년, 1942년 자도 각각 있습니다. 범위 밖 날짜가 모두 51건입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">의자수 433</span>
        <p class="b">의자가 433개라고 적은 이용원이 있습니다.</p>
        <p class="c">같은 줄의 소재지면적은 0.28㎡입니다. 둘 중 하나가, 혹은 둘 다 틀렸습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">104년 영업</span>
        <p class="b">1904년에 열어 2008년에 닫은 것으로 적힌 가게가 있습니다.</p>
        <p class="c">104.2년입니다. 시작 날짜가 틀리면 영업 기간도 같이 틀립니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제12호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>이용원</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 65,845행 기준<br>개별 업소의 영업 내용은 다루지 않았습니다. 등록된 값만 옮겼습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 65,845행에서 계산했습니다. scripts/analyze_barber.py 로 재현됩니다. */

/* [이름, 곳수, 중앙연도, 영업중] — 앞에서부터 겹치지 않게 가른 값 */
const SIGNS = [
 ["이용원", 23972, 2001, 4965],
 ["이발관",  9398, 1997, 2195],
 ["이용소",  5044, 2000, 1330],
 ["바버샵",  1642, 2022, 1226],
 ["이발소",   966, 2009,  266],
 ["이용실",   375, 2005,   57]
];

/* [연도, 바버샵, 그해 신규] */
const YEARS = [
 [2013,5,963],[2014,9,885],[2015,19,887],[2016,13,912],[2017,32,874],
 [2018,57,877],[2019,119,953],[2020,141,871],[2021,211,836],[2022,235,822],
 [2023,218,707],[2024,200,732],[2025,190,730],[2026,137,519]
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

$("#signs").innerHTML =
  '<div class="hd"><span>이름</span><span class="c">곳수</span>' +
  '<span class="y">중앙연도</span><span class="a">영업 중</span></div>' +
  SIGNS.map(([nm, c, y, a]) =>
    '<div' + (nm === "바버샵" ? ' class="on"' : "") +
    ' data-t="' + nm + ' — ' + nf(c) + '곳 · 중앙 ' + y + '년 · 영업 중 ' + nf(a) + '곳">' +
    '<span class="nm">' + nm + '</span>' +
    '<span class="c">' + nf(c) + '</span>' +
    '<span class="y">' + y + '</span>' +
    '<span class="a">' + (a / c * 100).toFixed(0) + '%</span></div>').join("");

const PCT = YEARS.map(([y, b, t]) => [y, b / t * 100, b, t]);
const maxP = Math.max(...PCT.map(r => r[1]));
$("#years").innerHTML = PCT.map(([y, p, b, t]) => {
  const peak = y === 2023;
  const tag = peak ? '<span class="tag">2023년 ' + p.toFixed(1) + '%</span>' : "";
  return '<span class="col' + (peak ? " peak" : "") + '" data-t="' + y + '년 — ' +
    nf(b) + '곳 / 신규 ' + nf(t) + '곳 = ' + p.toFixed(1) + '%"' +
    ' style="height:' + Math.max(p / maxP * 100, 0.8) + '%">' + tag + '</span>';
}).join("");

const AXIS = [2013, 2017, 2021, 2026];
$("#yaxis").innerHTML = AXIS.map((y, k) => {
  const i = PCT.findIndex(r => r[0] === y);
  const pct = (i + 0.5) / PCT.length * 100;
  const cls = k === 0 ? ' class="first"' : k === AXIS.length - 1 ? ' class="last"' : "";
  return '<span' + cls + ' style="left:' + pct.toFixed(2) + '%">' + y + '</span>';
}).join("");

$("#ytbl").querySelector("tbody").innerHTML = PCT.map(([y, p, b, t]) =>
  '<tr><td>' + y + '</td><td>' + nf(b) + '</td><td>' + nf(t) + '</td><td>' +
  p.toFixed(1) + '%</td></tr>').join("");

bindTips();
"""

out_dir = ROOT / "barbershop"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("barbershop/index.html 작성 완료 — %s bytes" % f"{out.stat().st_size:,}")
