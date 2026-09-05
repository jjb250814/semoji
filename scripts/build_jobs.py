"""
제28호 「개미인력」(jobs/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_jobs.py 의 출력(data/분석결과_직업소개소.txt)과
대조한 값이다.

사용법:
    python scripts/build_jobs.py

※ 이 페이지에서 지킨 선

1. **프랜차이즈 검사를 본문에 싣는다.** 독자가 같은 의심을 하기 때문이다.

2. **개별 업소를 지목하지 않는다.** 「개미인력」처럼 71곳이 함께 쓰는
   이름만 옮긴다. 한 곳만 쓰는 이름은 옮기지 않는다.

3. **「파출부」를 비웃지 않는다.** 지금은 잘 쓰지 않는 말이지만,
   그 이름으로 오래 일해 온 가게의 상호다.
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("유료직업소개소 60,010곳의 상호에서 가장 많이 나오는 동물은 개미(452곳)다. "
        "그다음이 황소(173곳). 둘 다 부지런하고 힘센 동물이다. "
        "프랜차이즈인지 확인해 보니 19개 시도에 흩어진 247가지 이름이었다.")

HEAD = """<title>개미인력</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/jobs/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="개미인력 — 세모지 제28호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/jobs/">
<meta property="og:image" content="https://semoji.net/og/jobs.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="개미인력 — 세모지 제28호 열람실">
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
/* 제28호 전용 */
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
.proof{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
  border-top:1px solid var(--rule);margin-top:22px}
.proof > div{padding:22px 16px 20px 0;border-right:1px solid var(--rule-2)}
.proof > div:last-child{border-right:0}
.proof .l{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--muted)}
.proof .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(24px,4vw,34px);line-height:1;margin-top:12px;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.proof > div.on .n{color:var(--seal-ink)}
.proof .s{display:block;font-size:12.5px;color:var(--muted);font-weight:300;margin-top:10px}
/* 동물 격자 */
.zoo{display:grid;grid-template-columns:repeat(auto-fill,minmax(128px,1fr));
  border-top:1px solid var(--rule);margin-top:6px}
.zoo div{padding:15px 12px 15px 0;border-bottom:1px solid var(--rule-2)}
.zoo .w{font-family:var(--f-display);font-weight:600;font-size:16px;display:block}
.zoo div.on .w{color:var(--seal-ink);font-weight:800}
.zoo .c{font-family:var(--f-mono);font-size:12px;color:var(--muted);display:block;
  margin-top:5px;font-variant-numeric:tabular-nums}
/* 상호 목록 */
.said{border-top:1px solid var(--rule);margin-top:6px}
.said div{display:grid;grid-template-columns:minmax(0,1fr) minmax(56px,auto);
  gap:12px;padding:12px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.said .w{font-family:var(--f-mono);font-size:14px;word-break:break-word}
.said div.on .w{color:var(--seal-ink);font-weight:700}
.said .c{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);text-align:right;
  font-variant-numeric:tabular-nums}
.said .hd{border-bottom:1px solid var(--rule)}
.said .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;color:var(--muted)}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제28호 열람실</span>
    <span>원자료 <b>유료직업소개소</b> · LOCALDATA · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제28호 열람실 · 유료직업소개소 상호</p>
    <h1>개미인력</h1>
    <p class="lede">
      인력사무소 <b>60,010곳</b>의 이름을 세어 봤습니다. 가장 많이 나오는
      동물은 <b>개미(452곳)</b> 이고, 그다음이 <b>황소(173곳)</b> 입니다.
      <b>부지런한 것과 힘센 것</b> 입니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">60,010</span><span class="l">유료직업소개소</span><span class="s">폐업 39,356곳 · 65.6%</span></div>
      <div class="fig hot"><span class="n">452</span><span class="l">이름에 「개미」</span><span class="s">247가지 이름</span></div>
      <div class="fig"><span class="n">173</span><span class="l">이름에 「황소」</span><span class="s">그다음이 코끼리 38</span></div>
      <div class="fig hot"><span class="n">660</span><span class="l">이름에 「파출부」</span><span class="s">지금은 잘 안 쓰는 말</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>상호에 든 동물</h2><span>60,010곳 · 상호 37,433가지</span></div>
    <p class="blk-note">
      인력사무소가 스스로에게 붙인 동물 이름입니다. <b>개미가 452곳</b> 으로 압도적이고,
      <b>황소가 173곳</b> 입니다. 코끼리 38곳, 까치 30곳, 백마 25곳이 뒤를 잇습니다.
    </p>
    <div class="zoo" id="zoo"></div>
    <p class="say">
      낱말이 겹치는 동물은 세지 않았습니다. <b>「소」로 세면 「직업소개소」가 다 걸려
      21,406곳</b>이 되고, 「용」은 「고용」과 「용역」에, 「말」은 「말소」에 걸립니다.
      <b>글자가 다른 낱말에 섞이지 않는 이름만</b> 셌습니다.
    </p>
  </section>

  <article class="form">
    <span class="form-label">먼저 확인한 것 · 개미가 프랜차이즈인가</span>
    <p class="q-text" style="margin-top:20px">한 회사의 지점 452곳이라면 「작명 습관」이라는 이야기는 통째로 틀린다</p>
    <div class="proof">
      <div class="on"><span class="l">「개미」가 든 상호</span><span class="n">452</span><span class="s">전국</span></div>
      <div><span class="l">흩어진 시도</span><span class="n">19</span><span class="s">전체 24곳 중</span></div>
      <div><span class="l">상호 종류</span><span class="n">247</span><span class="s">가지</span></div>
      <div><span class="l">법인</span><span class="n">13</span><span class="s">나머지는 개인</span></div>
    </div>
    <p class="say">
      452곳이 <b>19개 시도에 흩어져</b> 있고, 이름이 <b>247가지</b> 이며,
      <b>법인은 13곳뿐</b>입니다. 인허가는 1996년부터 2026년까지 걸쳐 있습니다.
      <b>프랜차이즈가 아니라 작명 습관입니다.</b>
      황소도 마찬가지로 17개 시도에 40가지 이름으로 흩어져 있습니다.
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>개미와 황소가 든 이름</h2><span>여러 곳이 함께 쓰는 상호</span></div>
    <p class="blk-note">
      <b>「개미인력」이 71곳</b>, 「개미인력개발」 52곳, 「개미직업소개소」 26곳입니다.
      황소는 <b>「황소인력」 89곳</b>이 가장 많습니다.
      <b>같은 이름을 서로 모르는 71곳이 따로 지었습니다.</b>
    </p>
    <div class="said" id="ant"></div>
    <p class="say">
      개미는 부지런함, 황소는 힘입니다. <b>일을 소개하는 곳이 스스로를
      「일하는 동물」로 부릅니다.</b> 손님에게 파는 것이 사람의 노동이기 때문일 텐데,
      <b>왜 그 동물을 골랐는지는 데이터에 없습니다.</b>
      확실한 것은 <b>같은 선택을 수백 곳이 따로 했다</b>는 사실뿐입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      이 페이지는 <b>한 곳만 쓰는 상호를 옮기지 않았습니다.</b> 37,433가지 이름 중
      <b>29,548가지가 딱 한 번</b>만 쓰였는데, 그런 이름은 그대로 특정 업소를 가리킵니다.
      여러 곳이 함께 쓰는 이름만 실었습니다. 그리고 <b>「파출부」를 비웃지 않습니다</b> —
      지금은 잘 쓰지 않는 말이지만 그 이름으로 오래 일해 온 가게의 상호입니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>인력 · 직업소개소 · 파출부</h2><span>상호에 쓰인 말</span></div>
    <p class="blk-note">
      상호의 <b>40.26%(24,160곳)</b> 에 「인력」이 들어갑니다.
      「직업소개소」가 28.92%, 「인력개발」이 6.71%입니다.
      그리고 <b>「파출부」가 660곳(1.10%)</b> 남아 있습니다.
    </p>
    <div class="hbars" id="words"></div>
    <p class="say">
      「잡(JOB)」이 든 상호가 928곳, 「컨설팅」이 888곳입니다.
      <b>같은 일을 부르는 말이 시대별로 겹쳐 있습니다</b> —
      파출부, 인력, 직업소개소, 컨설팅, 잡. 간판만 보면 어느 시대에
      문을 열었는지 짐작할 수 있습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>열에 아홉은 개인</h2><span>법인구분명 · 영업상태</span></div>
    <p class="blk-note">
      60,010곳 중 <b>개인이 53,253곳(88.7%)</b>, 법인은 6,751곳(11.2%)뿐입니다.
      그리고 <b>65.6%가 이미 폐업</b>했습니다.
    </p>
    <div class="hbars" id="alive"></div>
    <p class="say">
      2000년대에 22,808곳, 2010년대에 20,341곳이 새로 생겼습니다.
      1990년대는 2,103곳뿐입니다. <b>이 업종은 2000년 이후에 폭발했고
      동시에 대부분 사라졌습니다.</b> 개인 사업자가 열에 아홉인 것이
      그 짧은 수명과 무관하지 않을 것입니다 —
      <b>다만 그 연결은 데이터가 보여 주지 않습니다.</b>
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다. 한 곳만 쓰는 상호와 전화번호는 옮기지 않습니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">세 번째 「BBBB」</span>
        <p class="b">상세영업상태코드에 「BBBB」라고 적힌 것이 1건 있습니다.</p>
        <p class="c">제25호 담배소매업 400건, 제26호 통신판매업 115건에 이어 세 번째입니다.
          서로 다른 세 업종의 데이터에 같은 가짜 코드가 들어 있습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">답이 하나뿐인 칸</span>
        <p class="b">「구분명」 칸의 값은 60,004곳이 전부 「유료」입니다.</p>
        <p class="c">이 파일이 유료직업소개소만 담고 있어서입니다. 무료직업소개소는
          다른 데이터셋입니다. 쓸모없는 칸이라는 뜻은 아닙니다.</p>
      </div>
      <div class="flaw">
        <span class="h">인허가일자 1900년</span>
        <p class="b">인허가일자가 1900년으로 적힌 곳이 3건 있습니다.</p>
        <p class="c">1960년대 기록이 16건, 1970년대가 36건 있는 것과는 다른 종류의 값입니다.
          날짜 칸의 기본값으로 보입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">빈 줄 6건</span>
        <p class="b">구분명과 법인구분명이 동시에 빈 줄이 6건 있습니다.</p>
        <p class="c">같은 줄입니다. 두 칸이 함께 비어 있어 입력이 누락된 것으로 보입니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제28호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>유료직업소개소</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 내려받은 60,010행 기준<br>한 곳만 쓰는 상호와 전화번호는 옮기지 않았습니다. 동물 이름은 다른 낱말에 겹치지 않는 것만 셌습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 60,010행에서 계산했습니다. scripts/analyze_jobs.py 로 재현됩니다. */

/* 상호에 든 동물 [이름, 곳수] */
const ZOO = [
 ["개미", 452], ["황소", 173], ["코끼리", 38], ["까치", 30], ["백마", 25],
 ["천마", 20], ["꿀벌", 14], ["기린", 13], ["두꺼비", 13], ["청마", 8],
 ["백조", 7], ["다람쥐", 2], ["독수리", 1], ["제비", 1]
];

/* 개미·황소가 든 상호 [상호, 곳수] */
const ANT = [
 ["개미인력", 71], ["개미인력개발", 52], ["개미직업소개소", 26],
 ["개미인력소개소", 8], ["개미인력직업소개소", 6], ["개미인력개발(주)", 6],
 ["개미인력공사", 6], ["개미파출부", 4],
 ["황소인력", 89], ["황소직업소개소", 18], ["황소인력개발", 8],
 ["황소인력소개소", 6], ["황소인력공사", 4], ["황소종합인력", 3]
];

/* 상호에 쓰인 말 [말, 곳수, 비율] */
const WORDS = [
 ["인력", 24160, 40.26], ["직업소개소", 17352, 28.92], ["인력개발", 4026, 6.71],
 ["사무소", 1403, 2.34], ["잡 · JOB", 928, 1.55], ["컨설팅", 888, 1.48],
 ["파출부", 660, 1.10]
];

/* 영업상태 [상태, 곳수, 비율] */
const ALIVE = [
 ["폐업", 39356, 65.6], ["영업중", 14822, 24.7],
 ["타시군구이관", 4047, 6.7], ["등록취소", 1756, 2.9],
 ["경고조치", 9, 0.0], ["사업정지", 2, 0.0]
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

$("#zoo").innerHTML = ZOO.map(([w, c]) =>
  '<div' + (w === "개미" ? ' class="on"' : "") +
  ' data-t="' + w + ' — ' + nf(c) + '곳">' +
  '<span class="w">' + w + '</span>' +
  '<span class="c">' + nf(c) + '곳</span></div>').join("");

$("#ant").innerHTML =
  '<div class="hd"><span class="w">여러 곳이 함께 쓰는 상호</span><span class="c">곳</span></div>' +
  ANT.map(([w, c]) =>
    '<div' + (w === "개미인력" ? ' class="on"' : "") +
    ' data-t="' + esc(w) + ' — ' + nf(c) + '곳">' +
    '<span class="w">' + esc(w) + '</span>' +
    '<span class="c">' + nf(c) + '</span></div>').join("");

const maxW = WORDS[0][1];
$("#words").innerHTML = WORDS.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxW * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(2) + '% · ' + nf(c) + '</span></div>').join("");

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

out_dir = ROOT / "jobs"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("jobs/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
