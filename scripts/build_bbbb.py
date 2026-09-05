"""
제30호 「BBBB」(bbbb/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_bbbb.py 의 출력(data/분석결과_BBBB.txt)과
대조한 값이다.

사용법:
    python scripts/build_bbbb.py

※ 이 열람실이 다른 것과 다른 점

데이터셋 하나를 파는 것이 아니라 **세모지가 받아둔 22개 전부**를 가로지른다.
그래서 랜딩의 「읽은 데이터 행」에는 더하지 않는다 — 이미 센 데이터를
다시 보는 것이라 중복이 된다.

※ 지킨 선

1. **「BBBB는 오류다」라고 단정하지 않는다.** 언제나 같은 모양으로 나타나므로
   자리표시자로 보이지만, 원본에 정의가 없다.

2. **업체를 하나도 옮기지 않는다.** 이 열람실에는 상호가 나올 자리가 없다.
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("세모지가 모은 22개 데이터셋 4,679,894행을 가로질러 「BBBB」를 찾았다. "
        "12개 파일에 5,870건 있고, 고압가스는 46.25%가 이 값이다. "
        "BBBB 인 줄은 예외 없이 상세 상태가 비어 있고 영업 중이다.")

HEAD = """<title>BBBB</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/bbbb/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="BBBB — 세모지 제30호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/bbbb/">
<meta property="og:image" content="https://semoji.net/og/bbbb.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="BBBB — 세모지 제30호 열람실">
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
/* 제30호 전용 */
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
/* 데이터셋 표 */
.ds{width:100%;border-collapse:collapse;margin-top:6px;font-variant-numeric:tabular-nums}
.ds th,.ds td{padding:10px 8px;border-bottom:1px solid var(--rule-2);text-align:right;
  font-family:var(--f-mono);font-size:12.5px}
.ds th{color:var(--muted);font-size:10.5px;letter-spacing:.1em;font-weight:400;
  border-bottom:1px solid var(--rule)}
.ds th:first-child,.ds td:first-child{text-align:left;color:var(--ink-2)}
.ds tr.on td{color:var(--seal-ink);font-weight:700}
.ds tr.zero td{color:var(--muted)}
.ds tbody tr:last-child td{border-bottom:0}
/* 코드 목록 */
.codes{border-top:1px solid var(--rule);margin-top:6px}
.codes div{display:grid;grid-template-columns:minmax(96px,auto) minmax(0,1fr);
  gap:14px;padding:11px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.codes .nm{font-family:var(--f-display);font-weight:600;font-size:14px}
.codes .v{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);word-break:break-word}
.codes .v em{font-style:normal;color:var(--seal-ink);font-weight:700}
.codes .hd{border-bottom:1px solid var(--rule)}
.codes .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;color:var(--muted)}
.big{font-family:var(--f-mono);font-size:clamp(34px,9vw,72px);font-weight:700;
  letter-spacing:.14em;color:var(--seal-ink);text-align:center;padding:34px 0 30px;
  border:1px solid var(--rule);background:var(--card);margin-top:14px}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제30호 열람실</span>
    <span>원자료 <b>세모지가 모은 22개 데이터셋</b> · LOCALDATA · 2026-09-05 기준</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제30호 열람실 · 22개 데이터셋 교차 조사</p>
    <h1>BBBB</h1>
    <p class="lede">
      인허가 데이터에는 상태를 나타내는 코드 칸이 있습니다. 값은 보통
      <b>01, 02, 03</b> 같은 숫자입니다. 그런데 <b>스물두 개 데이터셋 중
      열두 개</b>에, 숫자가 아닌 값이 하나 섞여 있습니다.
    </p>

    <div class="big">BBBB</div>

    <div class="figs">
      <div class="fig"><span class="n">4,679,894</span><span class="l">훑은 행</span><span class="s">데이터셋 22개</span></div>
      <div class="fig hot"><span class="n">5,870</span><span class="l">「BBBB」</span><span class="s">12개 파일에서</span></div>
      <div class="fig hot"><span class="n">46.25%</span><span class="l">고압가스는</span><span class="s">11,263행 중 5,209건</span></div>
      <div class="fig"><span class="n">0</span><span class="l">예외</span><span class="s">모양이 늘 같다</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>스물두 개를 모았더니 보였다</h2><span>데이터셋 하나로는 안 보이는 것</span></div>
    <p class="blk-note">
      세모지는 지금까지 열람실 스물아홉 곳을 열며 <b>데이터셋 22개, 4,679,894행</b>을
      받아 뒀습니다. 그 파일들을 한 번에 훑으니 <b>같은 이상한 값이
      열두 곳에서 똑같이</b> 나왔습니다.
    </p>
    <table class="ds" id="ds"></table>
    <p class="say">
      <b>고압가스는 46.25%가 이 값입니다.</b> 11,263행 중 5,209건입니다.
      제19호 「점 하나」를 만들 때 판 파일인데, 그때는 사용목적과 사용방법 칸을
      보느라 이 칸을 지나쳤습니다. <b>한 파일만 볼 때는 「이 데이터가 좀 이상하네」로
      끝나지만, 열두 파일에서 같은 값이 나오면 이야기가 달라집니다.</b>
    </p>
  </section>

  <article class="form">
    <span class="form-label">먼저 확인한 것 · BBBB 인 줄은 언제나 같은 모양인가</span>
    <p class="q-text" style="margin-top:20px">그냥 깨진 값이라면 줄마다 제각각이어야 한다</p>
    <div class="split">
      <div class="on"><span class="l">상세영업상태명</span><span class="n">빈칸</span><span class="s">5,870건 전부</span></div>
      <div class="on"><span class="l">영업상태</span><span class="n">영업/정상</span><span class="s">코드 01 · 전부</span></div>
      <div><span class="l">검사한 파일</span><span class="n">12</span><span class="s">BBBB 가 나온 전부</span></div>
      <div><span class="l">어긋난 파일</span><span class="n">0</span><span class="s">예외 없음</span></div>
    </div>
    <p class="say">
      <b>깨진 값이 아닙니다.</b> BBBB 인 줄은 <b>예외 없이</b> 상세영업상태명이
      비어 있고, 영업상태는 「영업/정상」(코드 01)입니다.
      열두 파일 전부에서 그렇습니다.
    </p>
    <p class="say">
      즉 <b>「영업 중인데 세부 상태를 모른다」</b>는 뜻으로 보입니다.
      빈칸을 그냥 두는 대신 <b>「여기는 비어 있음」이라고 적어 넣은 자리표시자</b>입니다.
      <b>다만 원본 어디에도 그 정의는 없습니다.</b> 코드표가 함께 오지 않기 때문에,
      이 값이 무엇인지는 <b>데이터를 여러 개 겹쳐 봐야 짐작할 수 있습니다.</b>
    </p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>같은 칸, 다른 체계</h2><span>상세영업상태코드</span></div>
    <p class="blk-note">
      더 이상한 것은 <b>칸 이름이 같은데 코드 체계가 파일마다 다르다</b>는 점입니다.
      어떤 파일은 <b>01/02</b>, 어떤 파일은 <b>1/2</b>, 어떤 파일은 <b>0000/0001</b>,
      또 어떤 파일은 <b>10/20/40/50/70</b> 입니다.
    </p>
    <div class="codes" id="codes"></div>
    <p class="say">
      <b>「02」와 「2」가 같은 뜻인지 다른 뜻인지 데이터만 봐서는 알 수 없습니다.</b>
      방문판매업에는 <b>「-」</b> 라는 코드까지 있습니다.
      같은 이름의 칸이라도 <b>파일을 넘나들며 비교하면 안 된다</b>는 뜻입니다.
      세모지가 열람실마다 그 데이터셋 안에서만 비율을 낸 이유가 이것입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      <b>「BBBB는 오류다」라고 단정하지 않습니다.</b> 모양이 한결같으니
      자리표시자로 보이지만, 원본에 정의가 없어 확인할 길이 없습니다.
      그리고 이 열람실의 <b>4,679,894행은 사이트의 「읽은 데이터 행」에 더하지
      않았습니다</b> — 이미 다른 열람실에서 센 것을 다시 본 것이라 중복이 됩니다.
      <b>이 페이지에는 업체 이름이 한 곳도 나오지 않습니다.</b>
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>서른 곳을 열고 나서야</h2><span>제30호에 부치는 말</span></div>
    <p class="blk-note">
      세모지의 열람실은 하나씩 데이터셋 하나를 팠습니다.
      제30호는 <b>그렇게 쌓인 파일들 자체가 자료가 된 첫 번째 열람실</b>입니다.
    </p>
    <p class="say">
      「BBBB」는 어느 한 데이터셋의 흠이 아닙니다.
      <b>여러 기관이 각자 만든 파일에 같은 자리표시자가 들어 있다</b>는 것은,
      그 파일들이 <b>어딘가에서 같은 틀을 거쳐 나왔다</b>는 뜻입니다.
      <b>그 틀이 무엇인지는 공개된 데이터에 적혀 있지 않습니다.</b>
    </p>
    <p class="say">
      쓸데없는 것을 서른 번 캐면 <b>캔 자리들 사이에 또 쓸데없는 것이 생깁니다.</b>
      이것이 그 첫 번째입니다.
    </p>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제30호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>세모지가 모은 22개 데이터셋</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-05 기준 4,679,894행<br>이 행 수는 사이트 총계에 더하지 않았습니다. 이미 다른 열람실에서 센 데이터입니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 data/ 의 22개 CSV 에서 계산했습니다. scripts/analyze_bbbb.py 로 재현됩니다. */

/* 데이터셋 [이름, 행, BBBB, 비율, 코드종류] */
const DS = [
 ["고압가스", 11263, 5209, 46.25, 3], ["담배소매업", 657136, 400, 0.06, 8],
 ["통신판매업", 3096399, 115, 0.00, 11], ["노래방", 64396, 69, 0.11, 13],
 ["PC방", 82244, 32, 0.04, 12], ["방문판매업", 114172, 20, 0.02, 10],
 ["비디오감상실", 3627, 12, 0.33, 8], ["국내여행업", 20206, 5, 0.02, 13],
 ["국내외여행업", 29265, 4, 0.01, 13], ["기타유원시설", 1752, 2, 0.11, 10],
 ["동물병원", 10612, 1, 0.01, 6], ["직업소개소", 60010, 1, 0.00, 8],
 ["목욕장업", 17789, 0, 0.00, 2], ["문화예술법인", 3951, 0, 0.00, 2],
 ["비상급수시설", 11039, 0, 0.00, 2], ["세탁소", 67398, 0, 0.00, 2],
 ["식품자판기", 270591, 0, 0.00, 2], ["이용원", 65845, 0, 0.00, 2],
 ["종합여행업", 19822, 0, 0.00, 9], ["청소년게임장", 30771, 0, 0.00, 11],
 ["체육도장", 32838, 0, 0.00, 12], ["치과기공소", 8768, 0, 0.00, 8]
];

/* 코드 체계 [데이터셋, 코드들] */
const CODES = [
 ["고압가스", "1 / 2 / BBBB"],
 ["문화예술법인", "1 / 4"],
 ["목욕장업", "01 / 02"],
 ["담배소매업", "0 / 1 / 2 / 3 / 4 / 5 / 6 / BBBB"],
 ["동물병원", "0000 / 0001 / 0002 / 0003 / 0004 / BBBB"],
 ["직업소개소", "10 / 20 / 40 / 50 / 70 / 80 / 90 / BBBB"],
 ["비상급수시설", "18 / 19"],
 ["방문판매업", "- / 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / BBBB"],
 ["노래방", "02 / 03 / 13 / 14 / 15 / 25 / 30 / 31 / 32 / 33 / 34 / 35 / BBBB"],
 ["통신판매업", "0 / 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 1 / BBBB"]
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

$("#ds").innerHTML =
  '<thead><tr><th>데이터셋</th><th>행</th><th>BBBB</th><th>비율</th><th>코드 종류</th></tr></thead><tbody>' +
  DS.map(([nm, n, b, p, k]) =>
    '<tr class="' + (b ? (nm === "고압가스" ? "on" : "") : "zero") + '"' +
    ' data-t="' + nm + ' — ' + nf(n) + '행 중 BBBB ' + nf(b) + '건">' +
    '<td>' + nm + '</td><td>' + nf(n) + '</td><td>' + nf(b) + '</td>' +
    '<td>' + p.toFixed(2) + '%</td><td>' + k + '</td></tr>').join("") +
  '</tbody>';

$("#codes").innerHTML =
  '<div class="hd"><span class="nm">데이터셋</span><span class="v">상세영업상태코드에 있는 값</span></div>' +
  CODES.map(([nm, v]) =>
    '<div data-t="' + nm + ' — ' + v + '">' +
    '<span class="nm">' + nm + '</span>' +
    '<span class="v">' + v.replace(/BBBB/g, "<em>BBBB</em>") + '</span></div>').join("");

bindTips();
"""

out_dir = ROOT / "bbbb"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("bbbb/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
