"""
제22호 「SEOUL」(wifi/index.html) 조립기.

공용 CSS는 bike-rack/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_wifi.py 의 출력(data/분석결과_와이파이.txt)과
대조한 값이다.

사용법:
    python scripts/build_wifi.py

※ 이 페이지에서 지킨 선

1. **표기 흔들림을 제목으로 삼지 않았다.** SSID 에도 Public WiFi Free /
   Public Wifi Free / public wifi free 가 섞여 있지만, 그건 제21호와 같은
   이야기다. 곁가지로 한 문단만 두고 축은 「작명」에 뒀다.

2. **지자체를 나무라지 않는다.** 자체 브랜드가 나쁜 것이 아니다. 전국 공통
   이름을 정해 두었는데 절반 넘게 다른 이름을 쓴다는 사실만 센다.

3. **설치장소명·관리기관명의 개별 값과 전화번호는 옮기지 않는다.**
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "bike-rack" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("전국 공공와이파이 94,164곳의 SSID 를 세어 봤다. 공통 이름을 정해 뒀는데 "
        "58.2%가 자기 이름을 쓴다. 서울의 이름은 그냥 「SEOUL」 이고, "
        "제주는 공통 이름을 쓰는 곳이 한 곳도 없다.")

HEAD = """<title>SEOUL</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/wifi/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="SEOUL — 세모지 제22호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/wifi/">
<meta property="og:image" content="https://semoji.net/og/wifi.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="SEOUL — 세모지 제22호 열람실">
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
/* 제22호 전용 */
.say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.say b{font-weight:500;color:var(--ink)}
.split{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
  border-top:1px solid var(--rule);margin-top:22px}
.split > div{padding:22px 16px 20px 0;border-right:1px solid var(--rule-2)}
.split > div:last-child{border-right:0}
.split .l{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;color:var(--muted)}
.split .n{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(24px,4vw,34px);line-height:1;margin-top:12px;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.split > div.on .n{color:var(--seal-ink)}
.split .s{display:block;font-size:12.5px;color:var(--muted);font-weight:300;margin-top:10px}
/* SSID 목록 */
.ssid{border-top:1px solid var(--rule);margin-top:6px}
.ssid div{display:grid;grid-template-columns:minmax(0,1fr) minmax(72px,auto);
  gap:12px;padding:11px 0;border-bottom:1px solid var(--rule-2);align-items:baseline}
.ssid .w{font-family:var(--f-mono);font-size:14px;word-break:break-word}
.ssid div.on .w{color:var(--seal-ink);font-weight:700}
.ssid .c{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);text-align:right;
  font-variant-numeric:tabular-nums}
.ssid .hd{border-bottom:1px solid var(--rule)}
.ssid .hd span{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.12em;color:var(--muted)}
.ssid .rest{border-bottom:0}
.ssid .rest .w{color:var(--muted);font-family:var(--f-body);font-size:13px}
/* 시도 막대 */
.sido{border-top:1px solid var(--rule);margin-top:6px}
.sido div{display:grid;grid-template-columns:minmax(96px,auto) minmax(0,1fr) minmax(104px,auto);
  gap:14px;padding:11px 0;border-bottom:1px solid var(--rule-2);align-items:center}
.sido .nm{font-family:var(--f-display);font-weight:600;font-size:14.5px}
.sido div.on .nm{color:var(--seal-ink)}
.sido .track{display:block;height:14px;background:var(--rule-2);position:relative}
.sido .bar{display:block;height:100%;background:var(--ink-2);width:0;
  transition:width .7s cubic-bezier(.2,.9,.3,1)}
.sido div.on .bar{background:var(--seal)}
.sido .val{font-family:var(--f-mono);font-size:12px;color:var(--muted);
  text-align:right;font-variant-numeric:tabular-nums}
.caveat{border:1px solid var(--rule);background:var(--card);padding:24px var(--pad);margin:40px 0 0}
.caveat .h{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;color:var(--seal-ink)}
.caveat p{font-size:14px;color:var(--ink-2);font-weight:300;margin:13px 0 0;max-width:60ch}
.caveat p b{font-weight:500;color:var(--ink)}
</style>"""

BODY = r"""
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제22호 열람실</span>
    <span>원자료 <b>전국무료와이파이</b> · 행정안전부 · 2026-09-05 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제22호 열람실 · 공공와이파이 「와이파이SSID」</p>
    <h1>SEOUL</h1>
    <p class="lede">
      공공와이파이 <b>94,164곳</b>의 이름을 세어 봤습니다. 전국이 함께 쓰라고
      정해 둔 이름이 있는데, <b>58.2%가 자기 이름을 씁니다.</b>
      서울이 고른 이름은 그냥 <b>「SEOUL」</b> 입니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">94,164</span><span class="l">공공와이파이</span><span class="s">SSID 적힌 곳 66,548</span></div>
      <div class="fig hot"><span class="n">58.2%</span><span class="l">자기 이름을 씀</span><span class="s">38,735곳 · 1,059가지</span></div>
      <div class="fig hot"><span class="n">7,298</span><span class="l">이름이 「SEOUL」</span><span class="s">대문자 다섯 글자</span></div>
      <div class="fig"><span class="n">0% ~ 100%</span><span class="l">시도별 편차</span><span class="s">제주 0.0 · 세종 100.0</span></div>
    </div>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>이름이 하나가 아니다</h2><span>SSID 1,092가지</span></div>
    <p class="blk-note">
      전국 공통 이름은 <b>「Public WiFi Free」</b> 입니다. 그런데 SSID 가 적힌
      66,548곳 중 이 이름을 쓰는 곳은 <b>41.8%</b> 뿐입니다.
      나머지 <b>58.2%</b> 는 각자 지은 이름 <b>1,059가지</b>를 씁니다.
    </p>
    <div class="split">
      <div><span class="l">공통 이름</span><span class="n">41.8%</span><span class="s">27,813곳 · 표기 33가지</span></div>
      <div class="on"><span class="l">자체 브랜드</span><span class="n">58.2%</span><span class="s">38,735곳 · 이름 1,059가지</span></div>
    </div>
    <p class="say">
      판정은 기계적으로 했습니다. 소문자로 바꾸고 알파벳만 남겨 <code>publicwififree</code>
      또는 <code>publicwifi</code> 인 것만 공통 이름으로 셌습니다.
      <b>「Public WiFi@Seoul」처럼 공통 이름에 지역을 붙인 것은 자체 브랜드로 셌습니다</b> —
      그것도 결국 자기 이름을 지은 것이기 때문입니다.
    </p>
    <div class="ssid" id="own"></div>
    <p class="say">
      <b>「Golden-Fi Gyeongju」</b>는 경주가 지은 이름입니다. 무엇에서 따왔는지는
      데이터에 없습니다. 춘천은 <b>「Chuncheon_Free_WiFi」</b>, 제주는 <b>「Jeju Free Wifi」</b>,
      대전은 <b>「DJ_Public_WiFi」</b> 입니다. 길에서 휴대폰을 열었을 때 뜨는 이름이
      <b>도시마다 다릅니다.</b>
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>제주는 0%, 세종은 100%</h2><span>시도별 공통 이름 사용률</span></div>
    <p class="blk-note">
      같은 사업인데 시도별로 <b>0%에서 100%까지</b> 갈립니다.
      제주는 1,748곳이 전부 <b>「Jeju Free Wifi」 하나</b>를 쓰고,
      세종은 801곳이 전부 공통 이름 하나를 씁니다.
      <b>양 끝이 똑같이 「한 가지 이름」인데 고른 답이 반대입니다.</b>
    </p>
    <div class="sido" id="sido"></div>
    <p class="say">
      서울은 16,876곳 중 공통 이름이 <b>4.2%</b> 뿐이고 이름이 59가지입니다.
      전남광주통합특별시는 6,174곳에 이름이 <b>480가지</b>로 가장 어지럽습니다.
      <b>많이 설치한 곳일수록 이름이 갈린다고는 말할 수 없습니다</b> —
      경기도는 11,968곳인데 47가지뿐입니다.
    </p>
  </section>

  <div class="caveat">
    <span class="h">여기서 멈춘다</span>
    <p>
      <b>자체 브랜드가 잘못이라는 이야기가 아닙니다.</b> 도시가 자기 이름을 붙이는 데는
      이유가 있을 것이고, 원본에 그 이유는 적혀 있지 않습니다.
      세모지가 센 것은 <b>전국이 함께 쓸 이름을 정해 두었는데 절반 넘게 다른 이름을 쓴다</b>는
      사실뿐입니다. 그리고 <b>SSID 는 29.3%가 비어 있어</b>, 위 비율은 전부
      이름이 적힌 66,548곳만 놓고 낸 값입니다.
    </p>
  </div>

  <section class="blk">
    <div class="blk-head"><h2>통신사를 묻는데 시청이 답했다</h2><span>서비스제공사명 232가지</span></div>
    <p class="blk-note">
      「서비스제공사명」은 어느 통신사가 제공하는지 묻는 칸입니다. 그런데 값이
      <b>232가지</b>이고, 그중 <b>45.3%(42,687곳)가 관공서 이름</b>입니다.
      「경상북도 경주시청」 「과학기술정보통신부」 「자체설치(구로구)」 같은 값입니다.
    </p>
    <div class="split">
      <div><span class="l">통신사 이름</span><span class="n">54.7%</span><span class="s">51,477곳 · 66가지</span></div>
      <div class="on"><span class="l">관공서 이름</span><span class="n">45.3%</span><span class="s">42,687곳 · 166가지</span></div>
    </div>
    <p class="say">
      판정은 <b>한글이 들어 있고 통신사 이름이 아닌 것</b>을 관공서로 봤습니다
      (유플러스·브로드밴드·텔레콤·케이티·엘지는 통신사로 셌습니다).
      통신사 쪽도 KT 33,307 · LGU+ 7,871 · SKT 2,704 · 「LG U+」 1,816 ·
      「LG」 1,029 처럼 <b>같은 회사를 여러 가지로</b> 적었습니다.
      <b>제21호에서 본 일이 여기서도 일어납니다.</b>
    </p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>어디에 놓였나</h2><span>설치시설구분명 8가지</span></div>
    <p class="blk-note">
      가장 많은 곳은 관광지도 번화가도 아닙니다. <b>서민·복지시설 18,708곳(19.9%)</b> 입니다.
      그다음이 관공서, 교통시설 순입니다. <b>교육시설은 734곳(0.8%)뿐</b> 입니다.
    </p>
    <div class="hbars" id="kinds"></div>
    <p class="say">
      설치장소명은 <b>51,956가지</b>로 거의 다 다릅니다. 관리기관은 738곳입니다.
      설치연월이 적힌 58,708곳을 연도로 보면 <b>2020년 11,855곳</b>이 가장 많습니다.
      아래 그래프는 2013년부터입니다 — 그 이전은 2002~2012년을 다 합쳐 480곳뿐입니다.
    </p>
    <div class="hbars" id="years"></div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>데이터에 남은 흠</h2><span>공식 자료입니다</span></div>
    <p class="blk-note">원본 파일에 실제로 들어 있는 값입니다. 장소 이름과 전화번호는 옮기지 않습니다.</p>
    <div class="flaws">
      <div class="flaw">
        <span class="h">설치연월 1905년</span>
        <p class="b">2000년보다 이른 값이 6건 있고, 가장 이른 값은 1905년입니다.</p>
        <p class="c">와이파이가 없던 때입니다. 날짜 칸의 기본값이거나 입력 실수로 보입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">SSID 빈칸 29.3%</span>
        <p class="b">27,616곳은 무슨 이름으로 잡히는지 적혀 있지 않습니다.</p>
        <p class="c">그래서 이 페이지의 비율은 전부 이름이 적힌 66,548곳만 놓고 낸 값입니다.</p>
      </div>
      <div class="flaw">
        <span class="h">SSID 한 칸에 두 개</span>
        <p class="b">「SEOUL, SEOUL_Secure」처럼 이름 두 개가 쉼표로 들어간 값이 있습니다.</p>
        <p class="c">「Public Wifi Free(Public WiFi Secure)」처럼 괄호로 묶은 것도 있습니다.
          한 칸에 하나를 적으라는 규격이 없습니다.</p>
      </div>
      <div class="flaw">
        <span class="h">설치연월 빈칸 37.7%</span>
        <p class="b">언제 놓였는지 적히지 않은 곳이 35,456곳입니다.</p>
        <p class="c">연도 그래프는 적힌 58,708곳만 놓고 그렸습니다.</p>
      </div>
    </div>
  </section>
</main>

<div class="tip" id="tip"></div>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제22호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>전국무료와이파이 표준데이터</b> — 행정안전부 공공데이터포털 · 2026-09-05 내려받은 94,164행 기준<br>SSID 가 적힌 66,548곳만으로 비율을 냈습니다. 설치 장소의 이름과 관리기관 전화번호는 옮기지 않았습니다.</span>
  </div>
</footer>

<script>
/* 모든 값은 원본 CSV 94,164행에서 계산했습니다. scripts/analyze_wifi.py 로 재현됩니다. */

/* 자체 브랜드 상위 [이름, 곳수] */
const OWN = [
 ["SEOUL", 7298], ["Golden-Fi Gyeongju", 3396], ["SEOUL, SEOUL_Secure", 2555],
 ["Chuncheon_Free_WiFi", 1802], ["Jeju Free Wifi", 1748], ["Public WiFi@Seoul", 1276],
 ["G_PublicWiFi@SeongNam", 988], ["SEOUL_Secure", 971],
 ["Public WiFi Free, Public WiFi Secure", 900], ["Seoul", 792], ["DJ_Public_WiFi", 656],
 ["Public Wifi Free(Public WiFi Secure)", 606]
];

/* 시도별 [시도, 곳수, 공통이름%, 이름 가짓수] */
const SIDO = [
 ["제주특별자치도", 1748, 0.0, 1], ["서울특별시", 16876, 4.2, 59],
 ["경상남도", 4058, 34.1, 329], ["대전광역시", 1325, 41.6, 5],
 ["경상북도", 6763, 42.3, 41], ["강원특별자치도", 5407, 50.5, 22],
 ["전남광주통합특별시", 6174, 54.5, 480], ["충청남도", 3184, 55.4, 49],
 ["경기도", 11968, 60.4, 47], ["울산광역시", 241, 62.2, 22],
 ["충청북도", 2045, 69.2, 11], ["부산광역시", 1968, 72.5, 29],
 ["대구광역시", 628, 77.2, 16], ["인천광역시", 1655, 87.1, 5],
 ["전북특별자치도", 1707, 88.5, 41], ["세종특별자치시", 801, 100.0, 1]
];

/* 시설 구분 [이름, 곳수, 비율] */
const KINDS = [
 ["서민·복지시설", 18708, 19.9], ["관공서", 16761, 17.8], ["교통시설", 16556, 17.6],
 ["기타", 16055, 17.1], ["관광", 10223, 10.9], ["지역문화시설", 9375, 10.0],
 ["편의시설", 5752, 6.1], ["교육시설", 734, 0.8]
];

/* 연도별 설치 [연도, 곳수] */
const YEARS = [
 ["2013", 1071], ["2014", 1673], ["2015", 2538], ["2016", 1008], ["2017", 1758],
 ["2018", 4011], ["2019", 4468], ["2020", 11855], ["2021", 7325], ["2022", 9037],
 ["2023", 9233], ["2024", 2249], ["2025", 1965]
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

$("#own").innerHTML =
  '<div class="hd"><span class="w">휴대폰에 뜨는 이름</span><span class="c">곳</span></div>' +
  OWN.map(([w, c]) =>
    '<div' + (w === "SEOUL" ? ' class="on"' : "") +
    ' data-t="' + esc(w) + ' — ' + nf(c) + '곳">' +
    '<span class="w">' + esc(w) + '</span>' +
    '<span class="c">' + nf(c) + '</span></div>').join("") +
  '<div class="rest"><span class="w">그 밖에 1,047가지</span><span class="c">15,747</span></div>';

$("#sido").innerHTML = SIDO.map(([nm, n, p, u]) =>
  '<div' + (p === 0 || p === 100 ? ' class="on"' : "") +
  ' data-t="' + nm + ' — ' + nf(n) + '곳 · 이름 ' + u + '가지">' +
  '<span class="nm">' + nm + '</span>' +
  '<span class="track"><span class="bar" data-w="' + p.toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(n) + '</span></div>').join("");

const maxK = KINDS[0][1];
$("#kinds").innerHTML = KINDS.map(([w, c, p]) =>
  '<div class="hrow" data-t="' + w + ' — ' + nf(c) + '곳 (' + p + '%)">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxK * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + p.toFixed(1) + '% · ' + nf(c) + '</span></div>').join("");

const maxY = Math.max(...YEARS.map(y => y[1]));
$("#years").innerHTML = YEARS.map(([w, c]) =>
  '<div class="hrow" data-t="' + w + '년 — ' + nf(c) + '곳">' +
  '<span class="cat">' + w + '</span>' +
  '<span class="track"><span class="bar" data-w="' + (c / maxY * 100).toFixed(1) + '"></span></span>' +
  '<span class="val">' + nf(c) + '</span></div>').join("");

bindTips();
requestAnimationFrame(() => {
  document.querySelectorAll(".bar").forEach(b => b.style.width = b.dataset.w + "%");
});
"""

out_dir = ROOT / "wifi"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + BODY + "</script>\n",
               encoding="utf-8")
print("wifi/index.html 작성 완료 · %s bytes" % f"{out.stat().st_size:,}")
