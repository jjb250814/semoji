"""
제29호 「청수탕」(water/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_water.py 의 출력(data/분석결과_비상급수시설.txt)과
대조한 값이다.

사용법:
    python scripts/build_water.py

※ 이 페이지에서 지킨 선

1. **개별 시설의 위치를 옮기지 않는다.** 비상급수시설이 어디 있는지 콕 집어
   알리는 것은 이 사이트가 할 일이 아니다. 이름도 여러 곳이 함께 쓰는 것만 싣는다.

2. **분류는 이름으로 나눈 어림값이라고 밝힌다.** 서로 겹칠 수 있고 합계가
   100%를 넘는다.

3. **「목욕탕이 없어져서 지정이 풀렸다」고 단정하지 않는다.**
   지정을 푼 이유는 데이터에 없다. 제17호와 나란히 두기만 한다.
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("전쟁이나 재난 때 물을 얻을 민방위 비상급수시설 11,039곳을 세어 봤다. "
        "그중 1,137곳(10.3%)이 목욕탕이고, 그 목욕탕의 59.7%는 이미 사용중지다. "
        "전체 평균 47.6%보다 훨씬 높다.")

HEAD = """<title>청수탕</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/water/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="청수탕 — 세모지 제29호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/water/">
<meta property="og:image" content="https://semoji.net/og/water.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="청수탕 — 세모지 제29호 열람실">
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
/* 제29호 전용 */
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
/* 분류 표 */
.cats{border-top:1px solid var(--rule);margin-top:6px}
.cats div{display:grid;grid-template-columns:minmax(108px,auto) minmax(0,1fr) minmax(126px,auto);
  gap:14px;padding:13px 0;border-bottom:1px solid var(--rule-2);align-items:center}
.cats .nm{font-family:var(--f-display);font-weight:600;font-size:14.5px}
.cats div.on .nm{color:var(--seal-ink)}
.cats .track{display:block;height:15px;background:var(--rule-2);position:relative}
.cats .bar{display:block;height:100%;background:var(--ink-2);width:0;
  transition:width .7s cubic-bezier(.2,.9,.3,1)}
.cats div.on .bar{background:var(--seal)}
.cats .val{font-family:var(--f-mono);font-size:12px;color:var(--muted);
  text-align:right;font-variant-numeric:tabular-nums}
/* 이름 격자 */
.baths{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));
  border-top:1px solid var(--rule);margin-top:6px}
.baths div{padding:14px 12px 14px 0;border-bottom:1px solid var(--rule-2)}
.baths .w{font-family:var(--f-display);font-weight:600;font-size:15.5px;display:block}
.baths div.on .w{color:var(--seal-ink);font-weight:800}
.baths .c{font-family:var(--f-mono);font-size:11.5px;color:var(--muted);display:block;
  margin-top:5px;font-variant-numeric:tabular-nums}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제29호 열람실</span>
    <span>원자료 <b>민방위 비상급수시설</b> · LOCALDATA · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제29호 열람실 · 민방위 비상급수시설</p>
    <h1>청수탕</h1>
    <p class="lede">
      전쟁이나 재난이 나면 어디서 물을 얻을까요. 국가가 지정해 둔
      비상급수시설이 <b>11,039곳</b> 있습니다. 그 목록에
      <b>목욕탕이 1,137곳</b> 들어 있습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">11,039</span><span class="l">비상급수시설</span><span class="s">1955년부터 지정</span></div>
      <div class="fig hot"><span class="n">1,137</span><span class="l">목욕탕 · 사우나</span><span class="s">10.3%</span></div>
      <div class="fig hot"><span class="n">59.7%</span><span class="l">그중 사용중지</span><span class="s">전체 평균은 47.6%</span></div>
      <div class="fig"><span class="n">622</span><span class="l">「탕」으로 끝나는 이름</span><span class="s">488가지</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>무엇이 비상급수시설인가</h2><span>이름으로 나눈 어림 분류</span></div>
    <p class="blk-note">
      가장 많은 것은 <b>아파트·주택 1,395곳(12.6%)</b> 이고,
      그다음이 <b>학교 1,210곳</b>, <b>목욕탕·사우나 1,137곳</b> 입니다.
      공원과 운동장도 843곳 있습니다.
    </p>
    <div class="cats" id="cats"></div>
    <p class="say">
      <b>이 분류는 이름으로 나눈 어림값입니다.</b> 「청수탕」을 목욕탕으로 셌지만
      이름만 보고 판단한 것이고, 분류끼리 겹칠 수도 있어 <b>합계가 100%를 넘습니다.</b>
      그래도 큰 그림은 분명합니다 — <b>비상급수시설은 따로 지은 시설이 아니라
      이미 물이 나오는 곳을 지정한 것</b>입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>「탕」으로 끝나는 622곳</h2><span>488가지 이름</span></div>
    <p class="blk-note">
      이름이 「탕」으로 끝나는 시설이 <b>622곳</b>, 이름은 <b>488가지</b> 입니다.
      가장 많은 이름은 <b>「청수탕」 8곳</b>, 그다음이 「장수탕」 7곳입니다.
      맑은 물, 오래 사는 물 — <b>목욕탕 이름이 그대로 물 이름</b>입니다.
    </p>
    <div class="baths" id="baths"></div>
    <p class="say">
      <b>여러 곳이 함께 쓰는 이름만 옮겼습니다.</b> 488가지 중 400가지는
      한 곳만 쓰는 이름이라 그대로 특정 목욕탕을 가리킵니다.
      <b>비상급수시설이 어디 있는지 콕 집어 알리는 것은 이 사이트가 할 일이 아닙니다.</b>
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>목욕탕이 가장 많이 사라졌다</h2><span>분류별 사용중지 비율</span></div>
    <p class="blk-note">
      전체 11,039곳 중 <b>47.6%(5,252곳)가 이미 사용중지</b> 입니다.
      그런데 목욕탕은 <b>59.7%</b> 로 평균보다 훨씬 높고,
      공원·체육시설은 <b>16.1%</b> 로 훨씬 낮습니다.
    </p>
    <div class="split">
      <div class="on"><span class="l">목욕탕 · 사우나</span><span class="n">59.7%</span><span class="s">1,137곳 중 679곳</span></div>
      <div><span class="l">아파트 · 주택</span><span class="n">47.1%</span><span class="s">1,395곳 중 657곳</span></div>
      <div><span class="l">학교</span><span class="n">41.2%</span><span class="s">1,210곳 중 498곳</span></div>
      <div><span class="l">공원 · 체육시설</span><span class="n">16.1%</span><span class="s">843곳 중 136곳</span></div>
    </div>
    <p class="say">
      <b>제17호 「발한실」에서 센 목욕장업이 여기서 다시 나옵니다.</b>
      목욕탕이 문을 닫으면 그 물도 목록에서 빠집니다.
      <b>다만 지정을 푼 이유는 데이터에 적혀 있지 않습니다.</b>
      폐업 때문일 수도 있고, 수질 기준이나 관리 방침이 바뀐 것일 수도 있습니다.
      확실한 것은 <b>비상급수 목록에서 목욕탕이 가장 빠르게 줄었다</b>는 사실뿐입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      이 페이지는 <b>어느 시설이 어디 있는지 옮기지 않았습니다.</b>
      원본에는 「비상시설위치」 칸에 주소가 적혀 있지만, 재난 대비 시설의 위치를
      정리해 퍼뜨리는 것은 잡학이 아닙니다. <b>이름도 여러 곳이 함께 쓰는 것만</b>
      실었습니다. 그리고 분류는 <b>이름으로 나눈 어림값</b>이라 합계가 100%를 넘습니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>1955년부터</h2><span>지정 연도</span></div>
    <p class="blk-note">
      가장 이른 지정은 <b>1955년</b> 입니다. 1990년대에 3,126곳,
      2000년대에 3,693곳이 지정되며 정점을 찍고 줄어듭니다.
      지정 연도의 중앙값은 <b>2003년</b> 입니다.
    </p>
    <div class="hbars" id="dec"></div>
    <p class="say">
      만든 주체로 보면 <b>공공용시설이 8,590곳(77.8%)</b> 으로 대부분이고,
      정부지원시설 1,503곳, 지자체시설 945곳입니다.
      <b>새로 파는 것보다 있는 것을 지정하는 제도</b>라는 뜻입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다. 시설의 위치는 옮기지 않습니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">위치 칸에 「ㅏㅏㅏ」</span>
        <p class="b">비상시설위치 칸에 한글 자모만 적힌 것이 2건 있습니다.</p>
        <p class="c">나머지는 평균 22.7자짜리 주소입니다. 자판을 누른 자국이
          그대로 공개 데이터에 남았습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">이름이 「급수시설」</span>
        <p class="b">시설 이름 칸에 종류만 적은 곳이 있습니다.</p>
        <p class="c">「급수시설」 37곳, 「비상급수시설」 23곳, 「민방위비상급수시설」 23곳,
          「민간지정비상급수시설」 21곳. 이름 칸에 이름이 아니라 분류가 들어 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">1955년 지정</span>
        <p class="b">가장 이른 지정이 1955년입니다. 1950~60년대 지정이 모두 4건입니다.</p>
        <p class="c">1970년대가 110건, 1980년대가 765건인 것과 비교하면 외따로 떨어져 있습니다.
          이 네 건이 무엇인지는 데이터에 설명이 없습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">시설구분명 빈칸 1건</span>
        <p class="b">누가 만든 시설인지 적히지 않은 줄이 한 건 있습니다.</p>
        <p class="c">나머지 11,038곳은 공공용·정부지원·지자체 셋 중 하나입니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제29호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>민방위 비상급수시설</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 내려받은 11,039행 기준<br>시설의 위치는 옮기지 않았습니다. 분류는 이름으로 나눈 어림값이라 합계가 100%를 넘습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 11,039행에서 계산했습니다. scripts/analyze_water.py 로 재현됩니다. */

/* 분류 [이름, 곳수, 비율, 사용중지%] */
const CATS = [
 ["아파트 · 주택", 1395, 12.6, 47.1], ["학교", 1210, 11.0, 41.2],
 ["목욕탕 · 사우나", 1137, 10.3, 59.7], ["공원 · 체육시설", 843, 7.6, 16.1],
 ["관공서", 403, 3.7, 28.8], ["관정 · 우물", 302, 2.7, 49.0],
 ["병원 · 보건소", 160, 1.4, 46.2], ["교회 · 사찰", 142, 1.3, 47.9],
 ["공장 · 회사", 129, 1.2, 55.8], ["농업시설", 91, 0.8, 52.7],
 ["군 · 경찰 · 소방", 43, 0.4, 30.2]
];

/* 「탕」 이름 [이름, 곳수] */
const BATHS = [
 ["청수탕", 8], ["장수탕", 7], ["수정목욕탕", 6], ["수정탕", 6],
 ["은하탕", 5], ["약수탕", 5], ["제일목욕탕", 4], ["대호탕", 4],
 ["녹천탕", 4], ["천일탕", 3], ["아주탕", 3], ["옥천탕", 3],
 ["목화탕", 3], ["억수탕", 3]
];

/* 연도대 [연도대, 곳수] */
const DEC = [
 ["1950년대", 2], ["1960년대", 2], ["1970년대", 110], ["1980년대", 765],
 ["1990년대", 3126], ["2000년대", 3693], ["2010년대", 2118], ["2020년대", 1223]
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

const maxC = CATS[0][1];
$("#cats").innerHTML = CATS.map(([nm, c, p, stop]) =>
  '<div' + (nm === "목욕탕 · 사우나" ? ' class="on"' : "") +
  ' data-t="' + nm + ' — ' + nf(c) + '곳 (' + p + '%) · 사용중지 ' + stop + '%">' +
  '<span class="nm">' + nm + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxC * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + nf(c) + '곳 · 중지 ' + stop.toFixed(1) + '%</span></div>').join("");

$("#baths").innerHTML = BATHS.map(([w, c]) =>
  '<div' + (w === "청수탕" ? ' class="on"' : "") +
  ' data-t="' + w + ' — ' + nf(c) + '곳이 같은 이름">' +
  '<span class="w">' + w + '</span>' +
  '<span class="c">' + nf(c) + '곳</span></div>').join("");

const maxD = Math.max(...DEC.map(d => d[1]));
$("#dec").innerHTML = DEC.map(([w, c]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 지정">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxD * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "water"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("water/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
