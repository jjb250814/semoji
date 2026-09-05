"""
제23호 「타가다디스코」(amusement/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_amuse.py 의 출력(data/분석결과_유원시설.txt)과
대조한 값이다.

사용법:
    python scripts/build_amuse.py

※ 이 페이지에서 지킨 선

1. **「신고테마파크업」 한 곳의 상호를 옮기지 않는다.** 전국에 하나뿐이라
   이름을 적으면 그대로 특정된다. 연도와 상태까지만 쓴다.

2. **놀이기구 이름은 옮긴다.** 기구 이름은 업체를 가리키지 않는다.
   가장 긴 값 하나도 그대로 싣는다 — 상호가 들어 있지 않은 것을 확인했다.

3. **「이름을 적은 것」을 잘못으로 쓰지 않는다.** 칸 이름이 「놀이기구수내역」
   이라 개수와 내역을 같이 묻는 것으로 읽을 수도 있다. 본문에 그 가능성을 밝힌다.
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("유원시설 1,752곳의 「놀이기구수내역」 칸을 세어 봤다. 개수를 묻는 칸인데 "
        "92.4%가 숫자 대신 기구 이름을 적었다. 타가다디스코 69곳, 무궤도열차 56곳, "
        "붕붕뜀틀 16곳 — 손으로 적은 놀이기구 목록이 남았다.")

HEAD = """<title>타가다디스코</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/amusement/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="타가다디스코 — 세모지 제23호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/amusement/">
<meta property="og:image" content="https://semoji.net/og/amusement.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="타가다디스코 — 세모지 제23호 열람실">
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
/* 제23호 전용 */
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
/* 놀이기구 이름 격자 */
.rides{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
  gap:0;border-top:1px solid var(--rule);margin-top:6px}
.rides div{padding:13px 12px 13px 0;border-bottom:1px solid var(--rule-2)}
.rides .w{font-family:var(--f-display);font-weight:600;font-size:15px;display:block}
.rides div.on .w{color:var(--seal-ink);font-weight:800}
.rides .c{font-family:var(--f-mono);font-size:12px;color:var(--muted);display:block;
  margin-top:5px;font-variant-numeric:tabular-nums}
/* 원문 한 줄 */
.quote{font-family:var(--f-mono);font-size:13px;line-height:1.8;word-break:break-word;
  background:var(--card);border:1px solid var(--rule);padding:16px;margin-top:14px}
.quote .cap{display:block;font-size:10.5px;letter-spacing:.12em;color:var(--muted);
  margin-bottom:10px}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제23호 열람실</span>
    <span>원자료 <b>기타유원시설업</b> · LOCALDATA · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제23호 열람실 · 기타유원시설업 「놀이기구수내역」</p>
    <h1>타가다디스코</h1>
    <p class="lede">
      유원시설 신고서에는 <b>「놀이기구수내역」</b> 이라는 칸이 있습니다.
      개수를 묻는 칸인데, 적힌 1,309곳 중 <b>92.4%가 숫자 대신 기구 이름</b>을
      적었습니다. 그래서 <b>전국 놀이기구 목록</b>이 손글씨로 남았습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">1,752</span><span class="l">기타유원시설</span><span class="s">1965년 이후 · 영업 중 426곳</span></div>
      <div class="fig hot"><span class="n">92.4%</span><span class="l">이름을 적음</span><span class="s">1,209곳</span></div>
      <div class="fig"><span class="n">5.0%</span><span class="l">숫자만 적음</span><span class="s">66곳</span></div>
      <div class="fig hot"><span class="n">647</span><span class="l">기구 이름 종류</span><span class="s">손으로 적은 낱말</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>개수를 묻는데 이름을 적었다</h2><span>채워진 1,309곳</span></div>
    <p class="blk-note">
      칸 이름은 「놀이기구<b>수</b>내역」 입니다. 그런데 숫자만 적은 곳은
      <b>66곳(5.0%)</b> 뿐이고, 「N종」이라고만 적은 곳이 32곳,
      나머지 <b>1,209곳(92.4%)</b> 은 기구 이름을 늘어놓았습니다.
    </p>
    <div class="split">
      <div class="on"><span class="l">기구 이름을 적음</span><span class="n">92.4%</span><span class="s">1,209곳</span></div>
      <div><span class="l">숫자만</span><span class="n">5.0%</span><span class="s">66곳</span></div>
      <div><span class="l">「N종」만</span><span class="n">2.4%</span><span class="s">32곳</span></div>
    </div>
    <p class="say">
      <b>이것을 잘못 적은 것이라고 단정하지는 않습니다.</b> 칸 이름을
      「놀이기구 수 + 내역」으로 읽으면 이름을 적는 것이 맞습니다.
      다만 <b>같은 칸에 어떤 사람은 「1」을, 어떤 사람은 76자를 적었습니다.</b>
      정해진 답의 모양이 없다는 뜻입니다.
    </p>
    <div class="quote">
      <span class="cap">가장 길게 적은 칸 · 76자</span>
      미니바이킹 1대, 회전목마 1대, 매직스윙 1대, 무궤도열차 1대, 우주전투기 1대, 배터리카 1대, 회전형라이더 1대, 미니라이더 3대
    </div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>무엇이 있었나</h2><span>손으로 적은 기구 이름</span></div>
    <p class="blk-note">
      담당자가 붙인 분류어(「안전성검사」 「대상」 「유기기구」)는 빼고
      기구 이름만 셌습니다. <b>647가지</b>가 나옵니다.
      가장 많이 적힌 것은 <b>미니바이킹 153곳</b> 입니다.
    </p>
    <div class="rides" id="rides"></div>
    <p class="say">
      <b>「타가다디스코」</b> 69곳, <b>「무궤도열차」</b> 56곳, <b>「붕붕뜀틀」</b> 16곳.
      놀이공원의 큰 기구가 아니라 <b>동네 유원지와 워터파크의 기구</b>들입니다.
      「타가디스코」 22곳, 「타가다」 21곳처럼 <b>같은 기구를 다르게 적은 것</b>도 있어,
      실제로는 이보다 몇 곳 더 많습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>전국에 한 곳뿐인 업종</h2><span>문화체육업종명</span></div>
    <p class="blk-note">
      이 데이터의 업종 칸에는 답이 둘뿐입니다.
      <b>허가테마파크업 1,751곳, 신고테마파크업 1곳.</b>
    </p>
    <div class="split">
      <div><span class="l">허가테마파크업</span><span class="n">1,751</span><span class="s">99.94%</span></div>
      <div class="on"><span class="l">신고테마파크업</span><span class="n">1</span><span class="s">전국에 하나</span></div>
    </div>
    <p class="say">
      그 한 곳은 <b>1996년 9월 12일에 인허가를 받았고, 지금은 등록취소</b> 상태입니다.
      놀이기구수내역 칸에는 <b>「22종(검사대상7,비검사15)」</b> 이라고 적혀 있습니다.
      <b>상호는 옮기지 않았습니다</b> — 전국에 하나뿐이라 이름을 적으면 그대로 특정됩니다.
      제도상 이 분류가 왜 하나뿐인지는 <b>데이터에 적혀 있지 않습니다.</b>
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      이 데이터는 <b>1,752행뿐</b>입니다. 세모지가 지금까지 판 것 중 가장 작습니다.
      낱말 하나가 몇 곳 차이로 순위가 바뀌므로 <b>「가장 많은 기구」를 세게 말하지 않습니다.</b>
      그리고 <b>「놀이기구수내역」은 25.3%가 비어 있습니다</b>(443곳).
      위 비율은 전부 적힌 1,309곳만 놓고 낸 값입니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>셋 중 둘은 이미 없다</h2><span>영업상태</span></div>
    <p class="blk-note">
      1,752곳 중 <b>폐업이 1,155곳(65.9%)</b> 입니다. 영업 중인 곳은 426곳(24.3%)뿐입니다.
      가장 이른 인허가는 <b>1965년</b> 입니다.
    </p>
    <div class="hbars" id="alive"></div>
    <p class="say">
      위에서 센 기구 이름의 상당수는 <b>이미 사라진 유원지의 목록</b>입니다.
      「우주전투기」 「무궤도열차」 같은 이름이 데이터에 남은 이유가 그것입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>있는지만 묻는 칸들</h2><span>채움률과 쏠림</span></div>
    <p class="blk-note">
      「안내소유무」 「의무실유무」 「발전시설유무」 「방송시설유무」는 Y/N 만 받는 칸입니다.
      절반 안팎이 비어 있는데, <b>채워진 것은 거의 다 Y</b> 입니다.
    </p>
    <div class="hbars" id="yn"></div>
    <p class="say">
      <b>없으면 적지 않는 쪽에 가깝습니다.</b> 「발전시설유무」는 33.9%만 채워져 있고
      그중 77.1%가 Y입니다. N을 적은 곳은 136곳뿐입니다.
      <b>빈칸이 N을 뜻하는지 「모름」을 뜻하는지는 데이터가 말해 주지 않습니다.</b>
    </p>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제23호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>기타유원시설업</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 내려받은 1,752행 기준<br>업체 상호는 옮기지 않았습니다. 놀이기구 이름은 원본에 적힌 그대로입니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 1,752행에서 계산했습니다. scripts/analyze_amuse.py 로 재현됩니다. */

/* 손으로 적은 기구 이름 [이름, 곳수] */
const RIDES = [
 ["미니바이킹", 153], ["미니기차", 91], ["타가다디스코", 69], ["바이킹", 67],
 ["에어바운스", 62], ["바디슬라이드", 57], ["무궤도열차", 56], ["회전목마", 55],
 ["디스코팡팡", 53], ["미니에어바운스", 50], ["미니워터에어바운스", 50], ["유수풀", 48],
 ["워터에어바운스", 46], ["워터슬라이드", 38], ["회전그네", 37], ["범퍼카", 28],
 ["타가디스코", 22], ["슬라이딩카", 22], ["타가다", 21], ["배터리카", 18],
 ["페달보트", 17], ["붕붕뜀틀", 16], ["레일바이크", 16]
];

/* 영업상태 [상태, 곳수, 비율] */
const ALIVE = [
 ["폐업", 1155, 65.9], ["영업/정상", 426, 24.3], ["휴업", 65, 3.7],
 ["취소·말소·정지", 59, 3.4], ["기타", 47, 2.7]
];

/* Y/N 칸 [칸, 채움%, 채워진 곳, Y비율, Y곳] */
const YN = [
 ["방송시설유무", 61.9, 1084, 90.4, 980],
 ["안내소유무", 61.5, 1078, 89.9, 969],
 ["의무실유무", 47.8, 838, 84.5, 708],
 ["발전시설유무", 33.9, 594, 77.1, 458]
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

$("#rides").innerHTML = RIDES.map(([w, c]) =>
  '<div' + (w === "타가다디스코" ? ' class="on"' : "") +
  ' data-t="' + w + ' — ' + nf(c) + '곳이 적었다">' +
  '<span class="w">' + w + '</span>' +
  '<span class="c">' + nf(c) + '곳</span></div>').join("");

const maxA = ALIVE[0][1];
$("#alive").innerHTML = ALIVE.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxA * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(c) + '</span></div>').join("");

$("#yn").innerHTML = YN.map(([w, f, fc, y, yc]) =>
  '<div class="hrow" data-t="' + w + ' — 채움 ' + f + '% (' + nf(fc) + '곳) 중 Y ' + y + '% (' + nf(yc) + '곳)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + f.toFixed(1) + '"></span></span>' +
  '<span class="val">채움 ' + f.toFixed(1) + '% · Y ' + y.toFixed(1) + '%</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "amusement"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("amusement/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
