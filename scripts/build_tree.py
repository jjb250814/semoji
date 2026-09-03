"""
제14호 「나무의 품격」(tree/index.html) 조립기.

공용 CSS는 door-to-door/index.html 의 첫 <style> 블록을 그대로 물려받는다.
숫자는 전부 scripts/analyze_tree.py 의 출력과 대조한 값이다.

사용법:
    python scripts/build_tree.py
"""
import io
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

src = io.open(ROOT / "door-to-door" / "index.html", encoding="utf-8").read()
i = src.find("<style>")
j = src.find("</style>") + len("</style>")
BASE_STYLE = src[i:j]

DESC = ("전국 보호수 12,795건의 기록. 서류는 나무에 품격을 매긴다 "
        "— 도나무, 시·군나무, 면나무, 마을나무. 가장 나이 많은 나무는 1,345살이다.")

HEAD = """<title>나무의 품격</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="%(d)s">
<link rel="canonical" href="https://semoji.net/tree/">
<meta property="og:type" content="article">
<meta property="og:site_name" content="세모지">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="나무의 품격 — 세모지 제14호 열람실">
<meta property="og:description" content="%(d)s">
<meta property="og:url" content="https://semoji.net/tree/">
<meta property="og:image" content="https://semoji.net/og/tree.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="나무의 품격 — 세모지 제14호 열람실">
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
/* 제14호 전용 */
.rank-box{padding:36px var(--pad) 32px;margin:66px 0 0}
.rank-lab{font-family:var(--f-mono);font-size:11px;letter-spacing:.16em;color:var(--muted);margin:0 0 22px}
.rank{border-top:1px solid var(--rule)}
.rank > div{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:16px;
  align-items:baseline;padding:15px 0;border-bottom:1px solid var(--rule-2)}
.rank .step{font-family:var(--f-mono);font-size:11px;color:var(--muted);letter-spacing:.1em}
.rank .nm{font-family:var(--f-display);font-weight:800;font-size:clamp(19px,3.4vw,26px);
  letter-spacing:-.01em}
.rank .top .nm{color:var(--seal-ink)}
.rank .ct{font-family:var(--f-mono);font-size:13px;color:var(--ink-2);
  font-variant-numeric:tabular-nums;white-space:nowrap}
.rank-say{font-size:14.5px;color:var(--ink-2);font-weight:300;margin:22px 0 0;max-width:58ch}
.rank-say b{font-weight:500;color:var(--ink)}
.two{display:grid;gap:30px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-top:8px}
.mono-li{border-top:1px solid var(--rule);font-family:var(--f-mono);font-size:13px}
.mono-li div{display:flex;justify-content:space-between;gap:14px;padding:8px 0;
  border-bottom:1px solid var(--rule-2);font-variant-numeric:tabular-nums}
.mono-li b{font-weight:400;color:var(--ink)}
.mono-li span{color:var(--muted)}
.hbars.wide .hrow{grid-template-columns:minmax(104px,150px) 1fr minmax(74px,auto)}
@media (max-width:560px){.hbars.wide .hrow{grid-template-columns:1fr auto}}
/* 가장 늙은 나무 목록 */
.olds{border-top:1px solid var(--rule)}
.olds div{display:grid;grid-template-columns:minmax(62px,74px) minmax(0,1fr) minmax(0,1.4fr);
  gap:14px;align-items:baseline;padding:11px 0;border-bottom:1px solid var(--rule-2)}
.olds .yr{font-family:var(--f-display);font-weight:800;font-size:17px;
  font-variant-numeric:tabular-nums;white-space:nowrap}
.olds div:first-child .yr{color:var(--seal-ink)}
.olds .kd{font-size:14.5px}
.olds .ad{font-size:13px;color:var(--ink-2);font-weight:300}
@media (max-width:640px){.olds div{grid-template-columns:auto 1fr}
  .olds .ad{grid-column:1/-1;margin-top:2px}}
.oddlist{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.oddlist span{font-family:var(--f-mono);font-size:12.5px;color:var(--ink-2);
  border:1px solid var(--rule);background:var(--card);padding:6px 11px}
</style>"""

# --- 숫자 (analyze_tree.py 출력과 대조) ---
GRADE = [("도나무", 1181, "도가 정한 나무"), ("시·군나무", 5757, "시나 군이 정한 나무"),
         ("면나무", 2380, "면이 정한 나무"), ("마을나무", 3328, "마을이 정한 나무")]
KIND = [("노목", 7951), ("거목", 2733), ("노목+거목", 1711), ("희귀목", 357),
        ("노목+거목+희귀목", 25), ("노목+희귀목", 10), ("거목+노목", 6), ("거목+희귀목", 2)]
AGES = [("300년", 953), ("200년", 880), ("250년", 612), ("400년", 527), ("150년", 489),
        ("350년", 373), ("500년", 365), ("100년", 164), ("450년", 160), ("301년", 148)]
OLDS = [(1345, "느티나무", "부산광역시 기장군 장안읍 장안리"),
        (1344, "느티", "경기도 화성시 향남읍 증거리"),
        (1300, "골담초", "경상북도 영주시 북지리"),
        (1223, "느티나무", "경상남도 하동군 화개면 운수리"),
        (1200, "은행나무", "경기도 구리시 아차산로"),
        (1101, "느티나무", "전남광주통합특별시 해남군 삼산면 구림리"),
        (1061, "느티나무", "충청남도 예산군 대흥면 상중리"),
        (1044, "느티나무", "경상남도 거창군 웅양면 산포리"),
        (1042, "느티나무", "경기도 양주시 남면 감악산로"),
        (1041, "느티나무", "대구광역시 북구 연경동")]
SPECIES = [("느티나무", 6794), ("팽나무", 1140), ("소나무", 853), ("은행나무", 784),
           ("회화나무", 343), ("향나무", 292), ("왕버들", 225), ("곰솔", 157),
           ("푸조나무", 150), ("버드나무", 148)]
OWNER = [("공공", 2704), ("개인", 1887), ("단체", 1348)]
ODD = ["느티13,팽8,회화3,물푸레1", "팽나무1/느티나무3", "느티43,팽5", "느티5,이팝2",
       "굴참,곰솔", "느티/회화", "서어,회화,팽나무", "Zelkova serrata",
       "Ginkgo biloba", "Abies holophylla"]
YEARS = [(1968, 47), (1969, 1), (1971, 4), (1972, 196), (1974, 66), (1976, 3),
         (1978, 3), (1979, 88), (1980, 44), (1981, 225), (1982, 6711), (1983, 119),
         (1984, 1), (1985, 6), (1986, 20), (1987, 13), (1988, 65), (1989, 15),
         (1990, 105), (1991, 29), (1992, 43), (1993, 111), (1994, 75), (1995, 134),
         (1996, 85), (1997, 104), (1998, 179), (1999, 354), (2000, 234), (2001, 253),
         (2002, 98), (2003, 361), (2004, 399), (2005, 289), (2006, 239), (2007, 245),
         (2008, 224), (2009, 288), (2010, 196), (2011, 170), (2012, 86), (2013, 158),
         (2014, 46), (2015, 109), (2016, 95), (2017, 84), (2018, 31), (2019, 43),
         (2020, 57), (2021, 52), (2022, 72), (2023, 51), (2024, 39), (2025, 19),
         (2026, 2)]


def hbars(rows, unit="건", cls=""):
    top = max(v for _, v in rows)
    out = ['<div class="hbars%s">' % ((" " + cls) if cls else "")]
    for k, v in rows:
        val = f"{v:,}{unit}" if isinstance(v, int) else f"{v}{unit}"
        out.append('<div class="hrow"><span class="cat">%s</span>'
                   '<span class="track"><span class="bar" data-w="%.2f"></span></span>'
                   '<span class="val">%s</span></div>' % (k, v / top * 100, val))
    out.append("</div>")
    return "\n    ".join(out)


def monoli(rows, unit="건"):
    out = ['<div class="mono-li">']
    for k, v in rows:
        out.append("<div><b>%s</b><span>%s%s</span></div>" % (k, f"{v:,}", unit))
    out.append("</div>")
    return "\n        ".join(out)


rank = '<div class="rank">' + "".join(
    '<div class="%s"><span class="step">%s</span><span class="nm">%s</span>'
    '<span class="ct">%s건</span></div>' % ("top" if i == 0 else "", note, k, f"{v:,}")
    for i, (k, v, note) in enumerate(GRADE)) + "</div>"

olds = '<div class="olds">' + "".join(
    '<div><span class="yr">%s년</span><span class="kd">%s</span>'
    '<span class="ad">%s</span></div>' % (f"{y:,}", k, a) for y, k, a in OLDS) + "</div>"

oddlist = '<div class="oddlist">' + "".join(
    "<span>%s</span>" % s for s in ODD) + "</div>"

ymax = max(v for _, v in YEARS)
ycols = "".join(
    '<div class="col%s" style="height:%.1f%%" data-t="%d년 %s건"></div>'
    % (" peak" if y == 1982 else "", v / ymax * 100, y, f"{v:,}")
    for y, v in YEARS)

BODY = """
<div class="top">
  <div class="wrap">
    <span><a href="../">← 세모지</a> · 제14호 열람실</span>
    <span>원자료 <b>전국보호수표준데이터</b> · LOCALDATA · 2026-09-03 내려받음</span>
  </div>
</div>

<main class="wrap">
  <div class="head">
    <p class="eyebrow">제14호 열람실 · 전국 보호수 기록</p>
    <h1>나무의 <span class="or">품격</span></h1>
    <p class="lede">
      전국의 보호수 <b>12,795건</b>이 등록돼 있습니다. 그 서류에는
      <b>「품격명」</b>이라는 칸이 있습니다. 나무마다 등급이 매겨져 있고,
      등급은 <b>그 나무를 정한 행정구역의 크기</b>를 따릅니다.
      도가 정하면 도나무, 마을이 정하면 마을나무입니다.
    </p>

    <div class="figs">
      <div class="fig"><span class="n">12,795</span><span class="l">등록된 보호수</span><span class="s">합쳐서 16,282그루</span></div>
      <div class="fig hot"><span class="n">1,181</span><span class="l">도나무</span><span class="s">가장 높은 등급</span></div>
      <div class="fig hot"><span class="n">1,345년</span><span class="l">가장 나이 많은 나무</span><span class="s">부산 기장의 느티나무</span></div>
      <div class="fig"><span class="n">300년</span><span class="l">나이 중앙값</span><span class="s">가장 많이 적힌 나이이기도 하다</span></div>
    </div>
  </div>

  <article class="form rank-box">
    <span class="form-label">품격명</span>
    <p class="rank-lab">나무의 등급을 적는 칸. 답은 넷이다.</p>
    {{rank}}
    <p class="rank-say">사람이 아니라 <b>나무에 품격을 매기는 칸</b>입니다.
      높고 낮음을 가르는 게 아니라 <b>누가 이 나무를 지키기로 했는가</b>를 적는 것입니다.
      149건은 이 칸을 비워 두었습니다.</p>
  </article>

  <section class="blk">
    <div class="blk-head"><h2>노목 · 거목 · 희귀목</h2><span>보호수유형명</span></div>
    <p class="blk-note">등급과 별개로 <b>왜 지키는지</b>를 적는 칸이 또 있습니다.
      늙어서(<b>노목</b> 7,951), 커서(<b>거목</b> 2,733), 드물어서(<b>희귀목</b> 357).
      둘 다인 나무는 「노목+거목」으로 적고, 셋 다인 나무가 25그루 있습니다.</p>
    {{kinds}}
    <p class="blk-note" style="margin-top:26px">그런데 <b>「거목+노목」이 따로 6건</b> 있습니다.
      「노목+거목」과 같은 말인데 순서만 바뀌었습니다.
      기계로 세면 서로 다른 종류가 됩니다.</p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>삼백 년</h2><span>나무나이</span></div>
    <p class="blk-note">나이 칸은 <b>12,795건 전부가 채웠습니다.</b> 비워 둔 곳이 하나도 없습니다.
      그런데 적힌 값을 보면 <b>953그루가 똑같이 300년</b>이고, 그다음이 200년, 250년, 400년입니다.
      <b>100이나 50으로 딱 떨어지는 나이가 4,719건(36.9%)</b>입니다.</p>
    {{ages}}
    <p class="blk-note" style="margin-top:26px">나무의 나이는 베어서 나이테를 세지 않으면 정확히 알 수 없습니다.
      <b>그래서 어림으로 적습니다.</b> 「300년」은 「아주 오래됐다」는 뜻에 가깝습니다.
      다만 301년이라 적은 곳이 148건, 220년이 112건 있는 것을 보면
      <b>어딘가에서는 더 자세히 셌다는 뜻</b>이기도 합니다.</p>

    <p class="blk-note" style="margin-top:36px">가장 나이 많은 열 그루입니다.
      1,000년이 넘는 나무가 <b>26그루</b>, 500년이 넘는 나무가 <b>1,442그루</b> 있습니다.
      반대로 100년이 안 된 나무도 43그루 있습니다.</p>
    {{olds}}
    <p class="blk-note" style="margin-top:20px">세 번째 줄의 <b>골담초</b>는 나무라기보다 떨기나무에 가깝습니다.
      1,300년이라 적혀 있는데 <b>맞는지는 데이터로 가릴 수 없습니다.</b></p>
  </section>

  <section class="blk">
    <div class="blk-head"><h2>나무 이름을 적는 칸</h2><span>283가지</span></div>
    <p class="blk-note">무슨 나무인지 적는 칸에 283가지가 들어 있습니다.
      절반이 넘는 <b>6,794건이 느티나무</b>입니다.
      그런데 <b>「느티」라고만 적은 것도 129건</b> 있습니다.
      「왕버들」 225건과 「왕버들나무」 56건, 「곰솔」 157건과 「해송」 70건도 마찬가지입니다.
      <b>같은 나무인데 기계는 다른 나무로 셉니다.</b></p>
    <div class="two">
      <div>
        <p class="rank-lab">가장 많은 나무</p>
        {{species}}
      </div>
      <div>
        <p class="rank-lab">누가 가진 나무인가 · 적은 5,939건만</p>
        {{owner}}
        <p class="blk-note" style="margin-top:16px">보호수의 <b>3분의 1이 개인 소유</b>입니다.
          나머지 6,856건은 이 칸을 비워 두었습니다.</p>
      </div>
    </div>
    <p class="blk-note" style="margin-top:32px">종류 칸에 <b>학명을 적은 곳이 122건</b>,
      <b>여러 나무를 늘어놓은 곳이 44건</b> 있습니다.
      한 그루가 아니라 한 무리를 한 줄에 적은 것입니다.</p>
    {{oddlist}}
  </section>

  <section class="blk">
    <div class="blk-head"><h2>1982년에 6,711건</h2><span>보호수지정일자</span></div>
    <p class="blk-note">보호수로 정해진 날짜를 보면 <b>1982년 한 해가 6,711건</b>으로
      <b>전체의 52.5%</b>입니다. 나머지 44년을 다 합친 것보다 많습니다.
      그해에 전국을 한 번에 조사해 등록한 것으로 보이지만,
      <b>왜 1982년인지는 데이터에 없습니다.</b></p>
    <div class="cols">{{ycols}}</div>
    <div class="axis"><span class="first">1968</span><span style="left:50%">1997</span><span class="last" style="left:100%">2026</span></div>
    <p class="blk-note" style="margin-top:26px">가장 이른 지정일은 <b>1905년 6월 4일</b>입니다.
      1968년 이전으로 적힌 것이 9건 있습니다.
      보호수 지정을 푼 기록(해지일자)이 있는 것은 127건입니다.</p>

    <div class="flaws" style="margin-top:48px">
      <div class="flaw"><span class="h">25,000</span>
        <p class="b">키가 25,000이라고 적힌 나무.</p>
        <p class="c">단위가 미터라면 25킬로미터입니다. 높이 칸의 가운뎃값은 18입니다.</p></div>
      <div class="flaw"><span class="h">18 vs 6.8</span>
        <p class="b">키와 둘레의 단위가 섞여 있다.</p>
        <p class="c">둘레를 미터로 적은 곳(가운뎃값 6.8)과 센티미터로 적은 곳(100 넘는 값 5,013건)이
          함께 있습니다. 그래서 둘을 곧바로 견줄 수 없습니다.</p></div>
      <div class="flaw"><span class="h">1,129</span>
        <p class="b">관리용 칸을 뺀 모든 칸이 똑같은 줄.</p>
        <p class="c">전체의 8.8%입니다. 같은 나무가 두 번 올라간 것으로 보입니다.
          종류·나이·주소 세 칸만 보면 3,724건이 걸리는데, 한 마을의 여러 그루가
          따로 등록된 정상 사례가 섞여서 그건 세지 않았습니다.</p></div>
      <div class="flaw"><span class="h">6,615</span>
        <p class="b">도로명주소가 없는 줄.</p>
        <p class="c">절반이 넘습니다. 나무는 길가에만 서 있지 않아서,
          지번주소로 대신 셌습니다.</p></div>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="wrap r">
    <span><a href="../">세모지로 돌아가기 &rarr;</a> · 제14호 열람실 · <a href="../about/">소개</a> · <a href="../contact/">연락처</a> · <a href="../privacy/">개인정보처리방침</a></span>
    <span>출처 <b>전국보호수표준데이터</b> — 지방행정인허가데이터개방(LOCALDATA) · 2026-09-03 내려받은 12,795행 기준<br>나무의 위치는 등록된 주소를 그대로 옮겼습니다. 개인 소유지의 상세 지번은 싣지 않았습니다.</span>
  </div>
</footer>

<div class="tip" id="tip"></div>
<script>
/* 모든 값은 원본 CSV 12,795행에서 계산했습니다. scripts/analyze_tree.py 로 재현됩니다. */

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

const tip = document.getElementById('tip');
document.querySelectorAll('.col').forEach(function (c) {
  c.addEventListener('mouseenter', function () {
    tip.textContent = c.dataset.t;
    tip.classList.add('on');
    const r = c.getBoundingClientRect();
    tip.style.left = (r.left + r.width / 2) + 'px';
    tip.style.top = r.top + 'px';
  });
  c.addEventListener('mouseleave', function () { tip.classList.remove('on'); });
});
"""

values = {
    "rank": rank,
    "kinds": hbars(KIND, cls="wide"),
    "ages": hbars(AGES, unit="그루", cls="wide"),
    "olds": olds,
    "species": hbars(SPECIES, cls="wide"),
    "owner": monoli(OWNER),
    "oddlist": oddlist,
    "ycols": ycols,
}
body = BODY
for k, v in values.items():
    body = body.replace("{{" + k + "}}", v)
assert "{{" not in body

out_dir = ROOT / "tree"
out_dir.mkdir(exist_ok=True)
out = out_dir / "index.html"
out.write_text(HEAD + BASE_STYLE + "\n" + EXTRA_STYLE + "\n" + body + "</script>\n",
               encoding="utf-8")
print("tree/index.html written:", f"{out.stat().st_size:,}", "bytes")
