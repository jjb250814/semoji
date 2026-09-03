"""
제16호 「내집내점포앞」(waste/index.html) 조립기.

공용 CSS는 dental-lab/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_waste.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_waste.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "dental-lab" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("전국 10,187개 관리구역이 쓰레기 버리는 법을 저마다 적었다. "
        "같은 「종량제 봉투」를 162가지로, 내놓을 자리를 5,848가지로 적었다.")

HEAD = """<title>내집내점포앞</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/waste/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="내집내점포앞 — 세모지 제16호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/waste/">
<meta property="og:image" content="https://semoji.net/og/waste.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="내집내점포앞 — 세모지 제16호 열람실">
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
/* 제16호 전용 */
.say-box{padding:36px var(--pad) 32px;margin:66px 0 0}
.say-lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;color:var(--muted);margin:0 0 20px}
.say-big{font-family:var(--f-display);font-weight:800;color:var(--seal-ink);
  font-size:clamp(32px,7vw,62px);line-height:1.05;letter-spacing:-.03em}
.say-note{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:20px 0 0;max-width:58ch}
.say-note b{font-weight:500;color:var(--ink)}
/* 같은 말, 다른 표기 */
.variants{border-top:1px solid var(--rule);margin-top:8px}
.variants div{display:grid;grid-template-columns:minmax(56px,68px) minmax(0,1fr);
  gap:14px;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--rule-2)}
.variants .c{font-family:var(--f-mono);font-size:12px;color:var(--muted);text-align:right;
  font-variant-numeric:tabular-nums}
.variants .t{font-size:14.5px;word-break:keep-all}
.variants .once .c{color:var(--seal-ink)}
.variants .once .t{color:var(--seal-ink)}
.two{display:grid;gap:30px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-top:8px}
.mono-li{border-top:1px solid var(--rule);font-family:var(--f-mono);font-size:13px}
.mono-li div{display:flex;justify-content:space-between;gap:14px;padding:8px 0;
  border-bottom:1px solid var(--rule-2);font-variant-numeric:tabular-nums}
.mono-li b{font-weight:400;color:var(--ink)}
.mono-li span{color:var(--muted)}
.hbars.wide .hrow{grid-template-columns:minmax(118px,172px) 1fr minmax(64px,auto)}
@media (max-width:560px){.hbars.wide .hrow{grid-template-columns:1fr auto}}
/* 밤 그림 */
.night{display:grid;grid-template-columns:1fr auto 1fr;gap:16px;align-items:center;
  border-block:1.5px solid var(--ink);padding:26px 0;margin-top:10px}
.night .t{text-align:center}
.night .h{display:block;font-family:var(--f-display);font-weight:800;
  font-size:clamp(30px,6vw,52px);line-height:1;font-variant-numeric:tabular-nums}
.night .l{display:block;font-family:var(--f-mono);font-size:11px;color:var(--muted);margin-top:10px}
.night .s{display:block;font-size:13px;color:var(--ink-2);font-weight:300;margin-top:6px}
.night .arr{font-family:var(--f-mono);font-size:13px;color:var(--seal-ink)}
@media (max-width:560px){.night{grid-template-columns:1fr}.night .arr{transform:rotate(90deg)}}
.longq{font-family:var(--f-mono);font-size:12.5px;background:var(--card);
  border:1px solid var(--rule);border-left:3px solid var(--seal);padding:14px 16px;
  margin:14px 0 0;color:var(--ink-2);line-height:1.8}
</style>"""

# --- 숫자 (analyze_waste.py 출력과 대조) ---
MINE = [("내 집 앞, 내 가게 앞 배출", 1), ("내집내점포앞", 1), ("내 집 혹은 내 점포 앞", 1),
        ("집앞, 점포앞", 1), ("내집 대문 앞 및 가게 앞", 1),
        ("자기집 대문앞, 자기업소 1층 출입구", 1), ("집 또는 공장 앞", 1),
        ("집 또는 공장 문 앞", 1), ("대문 앞, 1층 출입구에 배출", 1),
        ("집앞", 261), ("집 앞", 58), ("자기 집(건물) 앞", 34)]
JONG = [("규격봉투에 넣어 지정된 요일에 배출", 3893), ("종량제배출", 1311),
        ("종량제 봉투 사용", 833), ("쓰레기 종량제 봉투에 넣어 지정된 요일에 배출", 704),
        ("종량제봉투에 담아서 배출", 697), ("종량제봉투", 528), ("규격봉투", 526),
        ("종량제봉투에담아배출", 298), ("종량제봉투 사용", 218),
        ("종량제 규격 봉투에 넣어 지정요일에 배출", 118)]
WAYS = [("음식물쓰레기 배출방법", 242), ("일시적다량폐기물 배출방법", 223),
        ("재활용품 배출방법", 212), ("생활쓰레기 배출방법", 178)]
DAYS = [("재활용품 배출요일", 88), ("생활쓰레기 배출요일", 83), ("음식물쓰레기 배출요일", 70)]
DAYTOP = [("일+화+목", 2343), ("월+화+수+목+금+토", 1272), ("월+화+수+목+금", 1027),
          ("일+월+화+수+목+금", 851), ("화", 560), ("목", 466), ("수", 452),
          ("월+수+금", 445)]
NOPICK = [("토+일", 2557), ("토,일요일+공휴일", 1311), ("법정공휴일+대체공휴일+토요일", 704),
          ("일요일+명절당일+일부 공휴일", 696), ("명절 및 일요일", 516),
          ("일요일, 명절(설,추석)", 506), ("명절+임시공휴일", 468), ("공휴일", 428)]
TYPE = [("거점수거", 8987), ("문전수거", 1155), ("기타", 45)]
SIDO = [("강원특별자치도", 2252), ("경상북도", 1832), ("전남광주통합특별시", 1440),
        ("경상남도", 1352), ("경기도", 1198), ("전북특별자치도", 766), ("대구광역시", 586)]


def hbars(rows, unit="곳", cls=""):
    top = max(v for _, v in rows)
    out = ['<div class="hbars%s">' % ((" " + cls) if cls else "")]
    for k, v in rows:
        val = f"{v:,}{unit}" if isinstance(v, int) else f"{v}{unit}"
        out.append('<div class="hrow"><span class="cat">%s</span>'
                   '<span class="track"><span class="bar" data-w="%.2f"></span></span>'
                   '<span class="val">%s</span></div>' % (k, v / top * 100, val))
    out.append("</div>")
    return "\n    ".join(out)


def monoli(rows, unit="곳"):
    out = ['<div class="mono-li">']
    for k, v in rows:
        out.append("<div><b>%s</b><span>%s%s</span></div>" % (k, f"{v:,}", unit))
    out.append("</div>")
    return "\n        ".join(out)


def variants(rows):
    out = ['<div class="variants">']
    for k, v in rows:
        out.append('<div class="%s"><span class="c">%s</span><span class="t">%s</span></div>'
                   % ("once" if v == 1 else "", f"{v:,}", k))
    out.append("</div>")
    return "\n    ".join(out)


BODY = """
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제16호 열람실</span>
    <span>원자료 <b>전국생활폐기물배출정보표준데이터</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제16호 열람실 · 전국 생활폐기물 배출 기록</p>
    <h1>내집<span class="or">내점포</span>앞</h1>
    <p class="lede">
      쓰레기를 어디에 내놓아야 하는지는 <b>동네마다 따로 정합니다.</b>
      전국 10,187개 관리구역이 그 자리를 각자 적었는데,
      <b>표기가 5,848가지</b>이고 그중 <b>4,704개는 딱 한 번만</b> 쓰였습니다.
      위의 여섯 글자도 그중 하나입니다. 띄어쓰기 없이 그렇게 적혀 있습니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">10,187</span><span class="l">관리구역</span><span class="s">203개 시군구가 나눠 정했다</span></div>
      <div class="fig hot"><span class="n">5,848</span><span class="l">배출장소 표기</span><span class="s">4,704개는 한 번뿐</span></div>
      <div class="fig hot"><span class="n">162</span><span class="l">「종량제 봉투」의 표기</span><span class="s">같은 말을 이렇게 갈라 적었다</span></div>
      <div class="fig"><span class="n">229</span><span class="l">미수거일 표기</span><span class="s">안 가져가는 날</span></div>
    </div>
  </div>

  <article class="form say-box">
    <span class="form-label">배출장소</span>
    <p class="say-lab">쓰레기를 어디에 내놓으라고 적었나.</p>
    <div><span class="say-big">내집내점포앞</span></div>
    <p class="say-note">전국에서 <b>딱 한 번</b> 쓰인 표기입니다.
      같은 뜻을 이렇게도 적었습니다 — 「내 집 앞, 내 가게 앞 배출」,
      「자기집 대문앞, 자기업소 1층 출입구」, 「집 또는 공장 문 앞」.
      <b>다 같은 자리를 가리킵니다.</b></p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>같은 자리를 가리키는 말들</h2><span>붉은 줄은 한 번뿐인 표기</span></div>
    <p class="blk-note">배출장소 칸에 규격이 없어서 담당자가 손으로 적습니다.
      가장 흔한 답은 <b>「지정된 장소」 516곳</b>인데, 어디인지는 알려주지 않습니다.
      그다음이 「문앞」 348곳, 「집앞」 261곳입니다.
      <b>띄어쓰기 하나로 「집앞」과 「집 앞」이 갈립니다.</b></p>
    {{mine}}
    <p class="blk-note" style="margin-top:26px">가장 긴 표기는 57자입니다.
      한 칸에 세 가지 경우를 다 넣었습니다.</p>
    <div class="longq">본인 집(가게) 건물 앞에 배출, 공동주택 및 다가구 주택 내 거점 수거 장소가 마련된 경우 해당 장소</div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>「종량제 봉투」를 적는 162가지 방법</h2><span>10,014곳</span></div>
    <p class="blk-note">생활쓰레기를 어떻게 버리라고 적었는지 보면,
      <b>10,187곳 중 10,014곳(98.3%)이 「종량제」나 「규격봉투」를 말합니다.</b>
      전국이 같은 말을 하고 있습니다. 그런데 <b>그 말을 162가지로 적었습니다.</b></p>
    {{jong}}
    <p class="blk-note" style="margin-top:26px">「종량제봉투에담아배출」은 띄어쓰기가 하나도 없고,
      「규격봉투」와 「종량제봉투」는 같은 것을 다르게 부르는 말입니다.
      기계로 세면 전부 다른 답이 됩니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>네 칸 모두 그렇다</h2><span>배출방법 표기 가짓수</span></div>
    <p class="blk-note">버리는 방법을 적는 칸은 넷입니다. 생활쓰레기, 음식물쓰레기,
      재활용품, 일시적다량폐기물. <b>네 칸 다 표기가 178~242가지</b>입니다.</p>
    {{ways}}
    <p class="blk-note" style="margin-top:26px">요일도 마찬가지입니다.
      재활용품 배출요일이 <b>88가지</b>, 생활쓰레기가 83가지, 음식물쓰레기가 70가지입니다.
      가장 흔한 것은 「일+화+목」 2,343곳입니다.</p>
    {{daytop}}
  </section>

  <section class="blk">
    <div class="blk-head"><h2>저녁에 내놓고 새벽에 가져간다</h2><span>배출 시각</span></div>
    <p class="blk-note">언제부터 언제까지 내놓을 수 있는지는 <b>거의 통일돼 있습니다.</b>
      시작 시각은 13가지, 종료 시각은 22가지뿐입니다. 앞의 칸들과 견주면 놀랍도록 적습니다.
      <b>시각은 숫자라서 흔들릴 여지가 없기 때문입니다.</b></p>
    <div class="night">
      <div class="t"><span class="h">20:00</span><span class="l">가장 흔한 시작 시각</span>
        <span class="s">3,351곳 · 18시 3,054 · 19시 2,857</span></div>
      <div class="arr">→</div>
      <div class="t"><span class="h">06:00</span><span class="l">가장 흔한 종료 시각</span>
        <span class="s">2,971곳 · 07시 2,218 · 04시 1,420</span></div>
    </div>
    <p class="blk-note" style="margin-top:26px">해가 진 뒤에 내놓고 해가 뜨기 전에 치웁니다.
      쓰레기가 길에 나와 있는 시간을 밤으로 몰아둔 것입니다.
      전국 8,987곳이 <b>거점수거</b>, 1,155곳이 <b>문전수거</b>입니다.</p>
    {{type}}
  </section>

  <section class="blk">
    <div class="blk-head"><h2>안 가져가는 날</h2><span>미수거일 229가지</span></div>
    <p class="blk-note">쓰레기를 <b>가져가지 않는 날</b>을 적는 칸이 있습니다.
      가장 흔한 답은 「토+일」 2,557곳입니다.
      <b>「명절」이 든 표기가 3,720곳, 63가지</b>입니다 —
      설과 추석에는 전국의 수거차가 멈춥니다.</p>
    {{nopick}}
    <p class="blk-note" style="margin-top:26px">가장 긴 미수거일은 서울의 한 구입니다.
      <b>동마다 안 가져가는 요일이 달라서</b>, 그것을 한 칸에 전부 적었습니다.</p>
    <div class="longq">동별상이(일요일 배출금지 : 소공,회현,을지로동 / 토요일 배출금지 : 중림,필,장충,광희,다산,신당,약수,청구,신당5,동화,황학동 ※ 명동은 별도 배출금지 요일 없음)</div>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>어디에 몰려 있나</h2><span>시도별 관리구역</span></div>
    <p class="blk-note">관리구역을 잘게 나눈 곳일수록 줄이 많습니다.
      강원이 2,252곳으로 가장 많은데, 인구가 아니라 <b>구역을 얼마나 잘게 나눴는지</b>를
      보여주는 숫자입니다.</p>
    {{sido}}

    <div class="flaws" style="margin-top:48px">
      <div class="flaw"><span class="h">2,203</span>
        <p class="b">「일시<b>작</b>다량폐기물」이라 적힌 줄.</p>
        <p class="c">「일시적」의 오타입니다. 한 시군구가 같은 문장을 2,203줄에 그대로
          복사해 넣으면서 오타까지 함께 퍼졌습니다.</p></div>
      <div class="flaw"><span class="h">1,595</span>
        <p class="b">관리구역 이름을 「없음」이라 적은 줄.</p>
        <p class="c">관리구역명은 649가지인데 그중 가장 많은 축이 「없음」입니다.
          이름을 붙이지 않은 구역이 그만큼 많습니다.</p></div>
      <div class="flaw"><span class="h">23:59</span>
        <p class="b">종료 시각을 23시 59분으로 적은 곳이 1,129곳.</p>
        <p class="c">24:00을 적을 수 없어서 1분을 뺀 것으로 보입니다.
          하루의 끝을 적는 방법도 갈립니다.</p></div>
      <div class="flaw"><span class="h">121</span>
        <p class="b">미수거일이 「없음」인 곳.</p>
        <p class="c">쉬는 날 없이 가져간다는 뜻인지, 적지 않은 것인지는
          데이터로 가릴 수 없습니다.</p></div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제16호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>전국생활폐기물배출정보표준데이터</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 10,187행 기준<br>배출 규칙은 수시로 바뀝니다. 실제로 버릴 때는 사는 곳의 시군구 안내를 따르십시오.</span>
  </div>
</footer>

<div class="tip" id="tip"></div>
<script>
/* 모든 값은 원본 CSV 10,187행에서 계산했습니다. scripts/analyze_waste.py 로 재현됩니다. */

const io = new IntersectionObserver(function (es) {
  es.forEach(function (e) {
    if (!e.isIntersecting) return;
    e.target.querySelectorAll('.bar').forEach(function (b, n) {
      setTimeout(function () { b.style.width = b.dataset.w + '%'; }, n * 45);
    });
    io.unobserve(e.target);
  });
}, { threshold: .25 });
document.querySelectorAll('.hbars').forEach(function (el) { io.observe(el); });
"""

values = {
    "mine": variants(MINE),
    "jong": hbars(JONG, cls="wide"),
    "ways": hbars(WAYS, unit="가지", cls="wide"),
    "daytop": hbars(DAYTOP, cls="wide"),
    "type": hbars(TYPE, cls="wide"),
    "nopick": hbars(NOPICK, cls="wide"),
    "sido": hbars(SIDO, cls="wide"),
}
body = BODY
for k, v in values.items():
    body = body.replace("{{" + k + "}}", v)
assert "{{" not in body

out_dir = ROOT / "waste"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + body + "</script>\n",
               encoding="utf-8")
print("waste/index.html written:", f"{out.stat().st_size:,}", "bytes")
