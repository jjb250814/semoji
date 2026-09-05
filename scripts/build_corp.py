"""
제24호 「허가증 이면 기재」(corporation/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_corp.py 의 출력(data/분석결과_문화예술법인.txt)과
대조한 값이다.

사용법:
    python scripts/build_corp.py

※ 이 페이지에서 지킨 선

1. **법인 이름을 하나도 옮기지 않는다.** 종교 법인이 927곳이라 이름을
   그대로 띄우면 특정 단체를 가리키게 된다.

2. **「이면 기재」를 게으름으로 쓰지 않는다.** 종이 허가증이 원본이고
   전산이 사본이던 시절의 자국이다. 원본에 이유는 적혀 있지 않다.

3. **허가조건 원문을 길게 옮기지 않는다.** 담당자가 타이핑한 행정 문구다.
   짧은 값만, 그것도 사람을 특정하지 않는 것만 옮긴다.
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("문화예술 비영리법인 3,951곳의 「허가조건」 칸을 세어 봤다. 채워진 1,370곳 중 "
        "11.8%가 조건 대신 「허가증 이면 기재」처럼 종이 뒷면을 가리킨다. "
        "공개된 전산 자료가 종이 문서를 참조하라고 적혀 있다.")

HEAD = """<title>허가증 이면 기재</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/corporation/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="허가증 이면 기재 — 세모지 제24호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/corporation/">
<meta property="og:image" content="https://semoji.net/og/corporation.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="허가증 이면 기재 — 세모지 제24호 열람실">
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
/* 제24호 전용 */
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
/* 적은 그대로 목록 */
.said{border-top:1px solid var(--rule);margin-top:6px}
.said div{display:grid;grid-template-columns:minmax(0,1fr) minmax(56px,auto);
  gap:12px;padding:12px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.said .w{font-family:var(--f-mono);font-size:14px;word-break:break-word}
.said div.on .w{color:var(--seal-ink);font-weight:700}
.said .c{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);text-align:right;
  font-variant-numeric:tabular-nums}
.said .hd{border-bottom:1px solid var(--rule)}
.said .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;color:var(--muted)}
.said .rest{border-bottom:0}
.said .rest .w{color:var(--muted);font-family:var(--f-body);font-size:13px}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제24호 열람실</span>
    <span>원자료 <b>문화예술 비영리법인</b> · LOCALDATA · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제24호 열람실 · 비영리법인 「허가조건」</p>
    <h1>허가증 이면 기재</h1>
    <p class="lede">
      법인 허가에는 조건이 붙습니다. 그 조건을 적는 칸에 <b>조건 대신
      「허가증 이면 기재」</b> 라고 적힌 곳이 있습니다.
      <b>공개된 전산 자료가 종이 뒷면을 보라고 말합니다.</b>
    </p>

    <div class="figs">
      <div class="fig"><span class="n">3,951</span><span class="l">문화예술 비영리법인</span><span class="s">1934년 이후 · 98.5% 살아 있음</span></div>
      <div class="fig"><span class="n">34.7%</span><span class="l">허가조건이 적힌 곳</span><span class="s">1,370곳</span></div>
      <div class="fig hot"><span class="n">11.8%</span><span class="l">「딴 데 있다」</span><span class="s">162곳 · 72가지</span></div>
      <div class="fig hot"><span class="n">627자</span><span class="l">가장 길게 적은 조건</span><span class="s">절반은 줄바꿈까지 넣었다</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>조건은 여기 없다</h2><span>채워진 1,370곳</span></div>
    <p class="blk-note">
      허가조건 칸이 채워진 1,370곳 중 <b>162곳(11.8%)</b> 은 조건을 적는 대신
      <b>다른 데를 가리킵니다.</b> 이면·뒷면·별지·별첨·참조·붙임 중 하나가
      들어간 값을 셌습니다. 그렇게 적는 방식만 <b>72가지</b> 입니다.
    </p>
    <div class="said" id="ref"></div>
    <p class="say">
      「이면」은 종이의 <b>뒷면</b>입니다. 허가증을 발급할 때 조건을 종이 뒤에 적고,
      전산에는 <b>「뒤에 적어 뒀다」는 사실만</b> 남긴 것입니다.
      <b>종이가 원본이고 데이터가 사본이던 시절의 자국입니다.</b>
      게으름이라고 단정할 수 없습니다 — 원본에 이유는 적혀 있지 않습니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>같은 칸, 세 글자와 627자</h2><span>허가조건의 길이</span></div>
    <p class="blk-note">
      같은 칸인데 <b>「붙임」 두 글자</b>로 끝낸 곳이 있고
      <b>627자를 타이핑한 곳</b>이 있습니다. 채워진 값의 <b>50.5%(692곳)</b> 는
      값 안에 줄바꿈까지 넣어 조항을 번호로 나눠 적었습니다.
    </p>
    <div class="split">
      <div><span class="l">15자 이하로 끝냄</span><span class="n">218</span><span class="s">15.9%</span></div>
      <div><span class="l">줄바꿈까지 넣음</span><span class="n">692</span><span class="s">50.5%</span></div>
      <div class="on"><span class="l">가장 긴 값</span><span class="n">627자</span><span class="s">평균은 131.6자</span></div>
    </div>
    <div class="said" id="short"></div>
    <p class="say">
      <b>「없음」이라고 적은 곳이 17곳</b> 있습니다. 조건이 없다는 뜻입니다.
      그런데 나머지 2,581곳은 <b>칸을 아예 비워 뒀습니다.</b>
      <b>빈칸이 「조건 없음」인지 「적지 않음」인지 데이터는 구분해 주지 않습니다.</b>
      「없음」을 적은 17곳이 있다는 사실이 오히려 그 구분이 필요했다는 증거입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      이 페이지는 <b>법인 이름을 하나도 옮기지 않았습니다.</b> 3,951곳 중
      <b>927곳이 종교 법인</b>이라, 이름을 그대로 띄우면 특정 단체를 가리키게 됩니다.
      허가조건의 <b>긴 원문도 옮기지 않았습니다</b> — 담당자가 타이핑한 행정 문구이고,
      옮겨 봐야 잡학이 아니라 남의 서류입니다. 짧고 사람을 가리키지 않는 값만 실었습니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>왜 만들었나</h2><span>법인설립목적 3,842가지</span></div>
    <p class="blk-note">
      「법인설립목적」은 <b>100% 채워져 있고</b>, 3,951곳에 <b>3,842가지</b> 가 적혀 있습니다.
      거의 전부 다릅니다. 평균 <b>74자</b>, 가장 긴 것은 310자입니다.
      설립 이유를 한 문장으로 적어야 하는 칸입니다.
    </p>
    <div class="said" id="aim"></div>
    <p class="say">
      그런데 <b>한 글자로 끝낸 곳이 17곳</b> 있습니다. 「-」 12곳과 「.」 5곳입니다.
      <b>「문화」 두 글자만 적은 곳이 6곳</b>, 「미기재」라고 적은 곳이 2곳,
      그리고 <b>「111」이라고 적은 곳이 한 곳</b> 있습니다.
      제1호 모범음식점의 메뉴 칸에서 본 것과 같은 모양입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>문화예술인데 넷 중 하나가 종교</h2><span>문화체육업종명 14가지</span></div>
    <p class="blk-note">
      이 데이터는 문화·예술 비영리법인 자료입니다. 그런데 업종을 갈라 보면
      <b>종교가 927곳(23.5%)</b> 입니다. 문화(사단) 1,264곳 다음으로 큰 덩어리가
      예술(사단) 835곳, 그다음이 <b>종교(사단) 646곳</b> 입니다.
    </p>
    <div class="hbars" id="kinds"></div>
    <p class="say">
      법인 형태로는 <b>사단법인이 76.4%(3,019곳)</b>, 재단법인이 23.6%(932곳)입니다.
      업종 칸이 <b>「분야(법인형태)」를 한 칸에 붙여</b> 적게 되어 있어서
      14가지가 됐습니다. 분야 7가지 × 형태 2가지입니다.
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>거의 죽지 않는다</h2><span>1934년부터</span></div>
    <p class="blk-note">
      3,951곳 중 폐업은 <b>58곳(1.5%)</b> 뿐입니다. <b>98.5%가 아직 살아 있습니다.</b>
      제23호 유원시설이 65.9% 폐업이었던 것과 정반대입니다.
    </p>
    <div class="hbars" id="dec"></div>
    <p class="say">
      가장 이른 허가는 <b>1934년</b> 입니다. 2000년대에 1,220곳, 2010년대에 1,807곳이
      생겼습니다. <b>영리 업종과 달리 비영리법인은 해산 절차를 밟지 않으면 기록이 남습니다.</b>
      98.5%가 지금도 활동 중이라는 뜻은 아닙니다 — <b>데이터가 말해 주는 것은
      「해산 신고가 안 됐다」는 것뿐입니다.</b>
    </p>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제24호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>문화예술 비영리법인</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 내려받은 3,951행 기준<br>법인 이름과 전화번호는 옮기지 않았습니다. 허가조건은 짧고 사람을 가리키지 않는 값만 실었습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 3,951행에서 계산했습니다. scripts/analyze_corp.py 로 재현됩니다. */

/* 「딴 데 있다」고 적은 방식 [적은 그대로, 곳수] */
const REF = [
 ["허가증 이면 기재", 33], ["비영리법인 설립허가증 뒷면에 기재", 11],
 ["허가서 이면 참조", 8], ["허가증 이면 참조", 6],
 ["설립허가증 뒷면에 기재", 5], ["법인 설립허가증 뒷면에 기재", 5],
 ["붙임", 4], ["별첨", 3], ["법인설립허가증 이면 참조", 3], ["이면기재", 3]
];

/* 짧게 끝낸 값 [값, 곳수] */
const SHORT = [
 ["허가증 이면 기재", 33], ["없음", 17], ["허가서 이면 참조", 8],
 ["허가증 이면 참조", 6], ["관계 법규와 제 규정 준수", 6],
 ["설립허가증 뒷면에 기재", 5], ["법인 설립허가증 뒷면에 기재", 5],
 ["관계 법규와 규정 준수", 4], ["붙임", 4], ["법인설립허가증 이면 참조", 3],
 ["이면기재", 3], ["관련 법령 준수", 3]
];

/* 설립목적을 5자 이하로 적은 값 [값, 곳수] */
const AIM = [
 ["문화원", 12], ["-", 12], ["문화", 6], [".", 5], ["미기재", 2],
 ["참선연구", 1], ["교리 전파", 1], ["콘텐츠개발", 1], ["111", 1],
 ["자양영당", 1], ["포교사업", 1], ["종교", 1]
];

/* 업종 [이름, 곳수, 비율] */
const KINDS = [
 ["문화(사단)", 1264, 32.0], ["예술(사단)", 835, 21.1], ["종교(사단)", 646, 16.4],
 ["행정(재단)", 351, 8.9], ["종교(재단)", 281, 7.1], ["문화(재단)", 196, 5.0],
 ["문화재(사단)", 161, 4.1], ["컨텐츠(사단)", 72, 1.8], ["예술(재단)", 50, 1.3],
 ["문화재(재단)", 43, 1.1], ["행정(사단)", 38, 1.0], ["컨텐츠(재단)", 10, 0.3],
 ["교육(사단)", 3, 0.1], ["교육(재단)", 1, 0.0]
];

/* 연도대별 허가 [연도대, 곳수] */
const DEC = [
 ["1930년대", 5], ["1940년대", 6], ["1950년대", 11], ["1960년대", 40],
 ["1970년대", 20], ["1980년대", 34], ["1990년대", 147], ["2000년대", 1220],
 ["2010년대", 1807], ["2020년대", 661]
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

function list(el, rows, hot, head, rest){
  $(el).innerHTML =
    '<div class="hd"><span class="w">' + head + '</span><span class="c">곳</span></div>' +
    rows.map(([w, c]) =>
      '<div' + (w === hot ? ' class="on"' : "") +
      ' data-t="' + esc(w) + ' — ' + nf(c) + '곳">' +
      '<span class="w">' + esc(w) + '</span>' +
      '<span class="c">' + nf(c) + '</span></div>').join("") +
    (rest ? '<div class="rest"><span class="w">' + rest + '</span><span class="c"></span></div>' : "");
}

list("#ref", REF, "허가증 이면 기재", "허가조건 칸에 적은 그대로", "그 밖에 62가지 · 모두 81곳");
list("#short", SHORT, "없음", "15자 이하로 끝낸 값", "그 밖에 121곳");
list("#aim", AIM, "111", "설립 목적을 5자 이하로", "5자 이하는 모두 54곳");

const maxK = KINDS[0][1];
$("#kinds").innerHTML = KINDS.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxK * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(c) + '</span></div>').join("");

const maxD = Math.max(...DEC.map(d => d[1]));
$("#dec").innerHTML = DEC.map(([w, c]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxD * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "corporation"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("corporation/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
