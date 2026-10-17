import json,html,os,re,shutil
SITE='https://botshopbuilds.com';CARDS=[];E=json.load(open('entries.json'));os.makedirs('site/builds',exist_ok=True)
MINOR=set('a an the and but or nor for so yet as at by in of on to up via per vs'.split())
def tcase(s):  # Turabian 17 headline style
    w=s.split(' ');o=[]
    for i,x in enumerate(w):
        if '.' in x or any(c.isupper() for c in x[1:]): o.append(x)
        elif i not in(0,len(w)-1) and x.lower() in MINOR: o.append(x.lower())
        else: o.append(x[:1].upper()+x[1:])
    return ' '.join(o)
def curly(s):
    s=re.sub(r'(^|[\s(\[])"',r'\1“',s); s=s.replace('"','”')
    s=re.sub(r"(^|[\s(\[])'",r'\1‘',s); return s.replace("'",'’').replace('—',', ')
def t(s): return html.escape(curly(s),quote=False)
PEND='<span class=st>Pending verification</span>'
def val(s): return PEND if s.strip().upper().startswith('TODO') else t(s).replace('TODO',PEND)
def first(s):
    if s.strip().upper().startswith('TODO'): return None
    m=re.match(r'(.+?[.!?])(\s|$)',s.strip()); return m.group(1) if m else s
def badge(e): return '<span class="st ok">Verified</span>' if e.get('verified') else PEND
CSS=r"""@import url('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112,600;125,700&family=IBM+Plex+Serif:wght@400;600&family=Source+Sans+3:wght@400;600&display=swap');
/* Palette: warm paper, graphite ink, one rust accent #B8461B (about 4.8:1 on paper). Spacing scale: 8/16/24/32/48/72/112 only. */
:root{--paper:#f6f4ef;--ink:#16181d;--mute:#4f5560;--hair:#d9d3cb;--acc:#b8461b;
--s1:8px;--s2:16px;--s3:24px;--s4:32px;--s5:48px;--s6:72px;--s7:112px;--gut:16px;--pad:max(16px,4vw);--frame:1200px;--fs:18px}
@media(min-width:640px){:root{--gut:24px}}@media(min-width:900px){:root{--fs:19.5px}}
html.lg{--fs:21px}@media(min-width:900px){html.lg{--fs:22px}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 var(--fs)/1.6 'Source Sans 3',system-ui,sans-serif;font-variant-numeric:lining-nums;overflow-wrap:break-word}
p{margin:0 0 16px;text-wrap:pretty}p:last-child{margin-bottom:0}a{color:var(--acc);text-underline-offset:3px;text-decoration-thickness:1px}li,dd,figcaption{text-wrap:pretty}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:#fff;padding:8px 16px;z-index:9}.skip:focus{left:8px}.skip{min-height:48px;display:inline-flex;align-items:center}
/* ONE COLUMN: centered, equal side margins, text left-aligned. Same edges for every text block. */
.frame{width:min(72ch,calc(100% - 2*clamp(20px,8vw,160px)));max-width:min(72ch,calc(100% - 2*clamp(20px,8vw,160px)));margin-inline:auto;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:var(--gut);text-align:left}
@media(min-width:640px){.frame{grid-template-columns:repeat(8,minmax(0,1fr))}}
@media(min-width:1024px){.frame{grid-template-columns:repeat(12,minmax(0,1fr))}}
.frame>*{grid-column:1/-1;min-width:0}.sub{display:grid;grid-template-columns:subgrid;column-gap:var(--gut)}
.cap{font-family:Archivo,sans-serif;font-stretch:112%;font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:17px;line-height:1.3}
h1,h2,h3{font-family:'IBM Plex Serif',Georgia,serif;font-weight:600;line-height:1.15;margin:0;text-wrap:wrap}
header.top{padding:var(--s3) 0;border-bottom:1px solid var(--hair)}header.top .frame{align-items:center;row-gap:var(--s2)}
.mark{align-self:center;font-family:Archivo,sans-serif;font-stretch:125%;font-weight:700;letter-spacing:.16em;text-transform:uppercase;font-size:17px;color:var(--ink);text-decoration:none;white-space:nowrap}.mark i{font-style:normal;color:var(--acc)}.mark img{vertical-align:-8px;margin-right:var(--s1)}
header .frame>nav{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s1) var(--s3)}
nav a{color:var(--ink);text-decoration:none;font-size:max(17px,.95rem)}nav a:hover{color:var(--acc)}nav a[aria-current]{color:var(--acc);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:6px}
@media(min-width:640px){header .frame>.mark{grid-column:1/span 4}header .frame>nav{grid-column:5/-1;justify-content:flex-end}}
@media(min-width:1024px){header .frame>.mark{grid-column:1/span 5}header .frame>nav{grid-column:6/-1}}
.ts{display:inline-flex;gap:var(--s1);align-items:baseline}.ts button{font:600 17px/1 'Source Sans 3',sans-serif;background:none;border:0;color:var(--mute);min-width:48px;min-height:48px;padding:0 var(--s1);cursor:pointer;text-underline-offset:6px}.ts button[data-s=lg]{font-size:22px}.ts button[aria-pressed=true]{color:var(--acc);text-decoration:underline;text-decoration-thickness:2px}
main{padding-bottom:var(--s7)}
/* HERO: eyebrow, h1 and dek fill the column. Numbers stay large. */
.eyebrow{margin-top:var(--s6);margin-bottom:0;color:var(--mute)}
.hero{margin-top:var(--s2);font-size:clamp(2.4rem,6.2vw,4.6rem);line-height:1.05;letter-spacing:-.02em;text-wrap:balance;max-width:none}
.dek{justify-self:stretch;width:auto;margin:var(--s3) 0 0;font-size:1.18em;line-height:1.45;color:var(--ink);text-align:left}
/* STATS: 2 cols (last spans) below 640, 5 equal from 640 */
.chorus{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:var(--s3) var(--gut);margin-top:var(--s5);padding-top:var(--s3);border-top:1px solid var(--ink)}
.chorus div{grid-column:span 2}.chorus div:nth-child(n+4){grid-column:span 3}@media(min-width:640px){.chorus{grid-template-columns:repeat(5,minmax(0,1fr))}.chorus div,.chorus div:nth-child(n+4){grid-column:auto}}
.chorus b{display:block;font:600 clamp(3.25rem,7vw,6rem)/.88 'IBM Plex Serif',serif;color:var(--acc);letter-spacing:-.04em;font-variant-numeric:tabular-nums lining-nums}.chorus span{display:block;margin-top:var(--s1);color:var(--mute);font-size:17px}
/* FINDER */
.finder{margin-top:var(--s5);row-gap:var(--s1);align-items:end}.finder label{grid-column:1/-1}#q,#c,#n{grid-column:1/-1}
@media(min-width:640px){#q{grid-column:1/span 5}#c{grid-column:6/-1}}@media(min-width:1024px){#q{grid-column:1/span 8}#c{grid-column:9/-1}}
#n{color:var(--mute);font-size:17px;margin:0}
input,select,textarea,button.b{font:inherit;font-size:max(17px,1rem);padding:8px 16px;border:1px solid #9aa0a8;background:#fff;color:var(--ink);border-radius:0;width:100%;min-height:48px}
button.b{width:auto;background:var(--ink);color:#fff;border-color:var(--ink)}button:disabled{opacity:.6}
/* INDEX: 1/2/3 cards (span 4 of 4/8/12). Subgrid rows so each row's parts share baselines. */
.index{margin-top:var(--s4);row-gap:var(--s5)}
.card{grid-column:1/-1;display:grid;grid-template-rows:subgrid;grid-row:span 5;row-gap:var(--s2);padding-top:var(--s3);border-top:1px solid var(--ink);align-content:start}
.card>*{margin:0}.card .meta{display:flex;flex-wrap:wrap;justify-content:space-between;gap:var(--s1) var(--s2);align-items:baseline}
.card h3{font-size:1.4rem}.card h3 a{color:var(--ink);text-decoration:none}.card h3 a:hover{color:var(--acc);text-decoration:underline}
.broke b{display:block;color:var(--acc);font-weight:600;margin-bottom:var(--s1)}
.data{font-size:17px;color:var(--mute);font-variant-numeric:tabular-nums}.data dt{display:inline;font-weight:600;color:var(--ink)}.data dd{display:inline;margin:0}.data dd:after{content:"";display:block}
.pd{color:var(--mute);font-style:italic}
.st{white-space:nowrap;font-size:17px;color:var(--mute)}.st:before{content:"";display:inline-block;width:.55em;height:.55em;border:1.5px solid currentColor;border-radius:50%;margin-right:.4em;vertical-align:.05em}
.st.ok{color:var(--acc)}.st.ok:before{background:currentColor}
.slot{grid-column:1/-1;grid-row:span 5;display:flex;flex-direction:column;gap:var(--s2);padding-top:var(--s3);border-top:1px dashed var(--ink)}
.slot>*{margin:0}.slot p{max-width:none}
@media(max-width:639px){.card,.slot{grid-row:auto;display:flex;flex-direction:column}}
/* HOW THIS IS MADE */
.made{margin-top:var(--s7);padding-top:var(--s4);border-top:1px solid var(--ink);row-gap:var(--s3)}
.dek+.made{margin-top:var(--s4)}
.made h2{grid-column:1/-1;font-size:1.8rem}.made .prose,.made .key{grid-column:1/-1}.made .prose{max-width:none}
.made.quiet .key{margin-top:var(--s2);padding-top:var(--s3);border-top:1px solid var(--hair)}
.key{margin:0}.key dt{margin-top:var(--s2)}.key dt:first-child{margin-top:0}.key dd{margin:var(--s1) 0 0;color:var(--mute)}
/* BUILD PAGE: 8fr table / 4fr meta on the same rails */
.crumb{margin:var(--s5) 0 0;display:flex;align-items:center;flex-wrap:wrap;gap:var(--s1) var(--s3);color:var(--mute)}
.btitle{margin-top:var(--s2);font-size:clamp(2.2rem,5.4vw,4.2rem);line-height:1.05;letter-spacing:-.02em;text-wrap:balance;max-width:none}
.table{margin:var(--s5) 0 0}.table dt,.table dd{grid-column:1/-1;margin:0}
.table dt{padding-top:var(--s3);border-top:1px solid var(--hair);color:var(--mute)}.table dd{padding:var(--s1) 0 var(--s3);max-width:none}
.side{margin-top:var(--s5);align-self:start;display:grid;gap:var(--s3);padding-top:var(--s3);border-top:1px solid var(--ink)}.side dl{margin:0}.side dd{margin:var(--s1) 0 0}
.subhead{margin-top:var(--s6);font-size:1.8rem}.formwrap{justify-self:stretch;width:auto;margin-top:var(--s4);display:grid;gap:var(--s3);text-align:left}
footer{padding:0 0 var(--s7);color:var(--mute)}footer .frame{row-gap:var(--s4);align-items:start}
footer .frame::before{content:"";grid-column:1/-1;border-top:1px solid var(--ink);margin-bottom:var(--s3)}
footer .fbrand,footer .fm,footer .fnav{grid-column:1/-1}footer .fbrand p{margin-top:var(--s2)}footer .fm .sc{font-variant-caps:all-small-caps;letter-spacing:.06em;font-size:19px;color:var(--ink);margin:0}footer .fm .fst{font-size:17px;margin-top:var(--s1)}
.fnav{display:flex;flex-wrap:wrap;gap:var(--s1) var(--s3)}.fnav a{color:var(--ink);text-decoration:none;font-size:17px}.fnav a:hover{color:var(--acc);text-decoration:underline}
@media(min-width:640px){footer .fnav{flex-direction:column;align-items:flex-start}}
.fnav a,.contact{white-space:nowrap;width:auto;max-width:100%}
.spine{padding-bottom:0}.spinewrap{grid-column:1/-1;display:grid;grid-template-columns:subgrid;margin-top:var(--s6);border-top:1px solid var(--ink)}.spinewrap>.sl,.spinewrap>.sr{padding-bottom:var(--s7)}
.sl{grid-column:1/-1;display:grid;grid-template-columns:subgrid;align-content:start}.sl>*{grid-column:1/-1}

.sr{grid-column:1/-1;position:relative;display:grid;align-content:start;gap:var(--s5);border-top:1px solid var(--ink);padding-top:var(--s4)}
.shoplist{margin-top:0;display:grid;grid-template-columns:subgrid;row-gap:var(--s6)}
.shop{grid-column:1/-1;display:grid;grid-template-columns:subgrid;row-gap:var(--s2);padding-top:var(--s4)}.shop+.shop{border-top:1px solid var(--ink)}.shop>*{grid-column:1/-1;margin:0}
.shop .meta{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--s1) var(--s2)}.shop h2{font-size:1.8rem;margin-top:var(--s1)}.shop h2 a{color:var(--ink)}
.runs{margin-top:var(--s2)!important}.runs b{display:block;margin-bottom:var(--s1)}
.shop ul{display:grid;grid-template-columns:subgrid;margin:0;padding:0;list-style:none}.shop li{grid-column:1/-1;padding:var(--s1) 0;border-top:1px solid var(--hair)}
.sr .slot{grid-column:auto;grid-row:auto;border-top:1px solid var(--ink);padding-top:var(--s3)}.sr .slot:first-child{border-top:0;padding-top:0}
.top nav a,.fnav a,a.mark,.card h3 a,.crumb a{display:inline-flex;align-items:center;min-height:48px}
.hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}.signup .row{display:flex;flex-wrap:wrap;gap:var(--s1);margin-top:var(--s1)}.signup input[type=email]{flex:1 1 200px;width:auto;min-width:0}.signup .data{margin-top:var(--s1)}@media(min-width:1024px){.key.signup .row{flex-wrap:nowrap}.key.signup input[type=email]{flex:1 1 0}}.joined{margin-top:var(--s3);color:var(--acc);font-weight:600}
main>.made:last-child{margin-bottom:var(--s7)}.spons{grid-column:1/-1;margin:var(--s3) 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:var(--s1) var(--s2);color:var(--mute)}.spons a{display:inline-flex;align-items:center;min-height:48px}
.key dd a{display:inline-flex;align-items:center;min-height:48px}.key dd.book{margin-top:var(--s2)}a.bk{display:inline-flex;align-items:center;min-height:48px;padding:0 var(--s3);background:var(--ink);color:#fff;text-decoration:none;font-weight:600}a.bk:hover{background:var(--acc);color:#fff}.key dd a.bk{min-height:48px}
.why{grid-column:1/-1;justify-self:stretch;width:auto;margin:var(--s4) 0 0;padding:var(--s3) 0 0;border-top:1px solid var(--hair);text-align:left}.why p{max-width:none;margin-top:var(--s1);font-size:1.06em}.tipslot h3 a{color:var(--ink)}.tipslot a{display:inline-flex;align-items:center;min-height:48px}.cta a{display:inline-flex;align-items:center;min-height:48px}.shop h2 a,.shop p.data a,.runs li a,.shop li a{display:inline-flex;align-items:center;min-height:48px}.key dd a.bk{min-height:48px}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}::selection{background:#f0d2c6;color:var(--ink)}"""
TS="""<script>(function(){var h=document.documentElement;if(localStorage.getItem('bsb-ts')==='lg')h.classList.add('lg');document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('.ts button').forEach(function(b){var lg=b.dataset.s==='lg';b.setAttribute('aria-pressed',lg===h.classList.contains('lg'));b.onclick=function(){h.classList.toggle('lg',lg);localStorage.setItem('bsb-ts',lg?'lg':'md');document.querySelectorAll('.ts button').forEach(function(x){x.setAttribute('aria-pressed',(x.dataset.s==='lg')===lg)})}})})})()</script>"""
def page(ti,body,d='',cur='',mc='',pth=None,card='site',desc='A logbook of real Grok Bot shop builds: the job, the tools, the costs, the human review, and what broke. Unchecked numbers are marked pending.'):
    def nl(h,l): return f'<a href="{d}{h}"'+(' aria-current=page' if h==cur else '')+f'>{l}</a>'
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{ti} | Bot Shop Builds</title><meta name=description content="{desc}"><meta property=og:type content=website><meta property=og:site_name content="Bot Shop Builds"><meta property=og:title content="{html.escape(curly(ti))} | Bot Shop Builds"><meta property=og:description content="{desc}"><meta property=og:url content="{SITE}/{cur if pth is None else pth}"><meta property=og:image content="https://bookof42.grok.me/og.jpg?v=2"><meta property=og:image:width content=1200><meta property=og:image:height content=630><meta name=twitter:card content=summary_large_image><meta name=twitter:title content="{html.escape(curly(ti))} | Bot Shop Builds"><meta name=twitter:description content="{desc}"><meta name=twitter:image content="https://bookof42.grok.me/og.jpg?v=2"><link rel=icon href="{d}favicon.ico" sizes=any><link rel=icon href="{d}favicon.svg" type="image/svg+xml"><link rel=icon href="{d}favicon-32.png" sizes=32x32><link rel=apple-touch-icon href="{d}apple-touch-icon.png"><link rel=stylesheet href="{d}style.css">{TS}</head><body>
<a class=skip href="#main">Skip to content</a>
<header class=top><div class=frame><a class=mark href="{d}index.html" aria-label="Bot Shop Builds home"><img src="{d}mark.svg" alt="" width=28 height=28>Bot Shop <i>/</i> Builds</a><nav aria-label=Main>{nl('index.html','Builds')}{nl('tips.html','Tips')}{nl('learned.html','Learned')}{nl('shops.html','Shops')}{nl('submit.html','Submit')}{nl('newsletter.html','Newsletter')}<span class=ts role=group aria-label="Text size"><button data-s=md aria-label="Change text size to standard" title="Text size: standard">A</button><button data-s=lg aria-label="Change text size to larger" title="Text size: larger">A</button></span></nav></div></header>
<main id=main class="frame{' '+mc if mc else ''}">{body}</main>
<footer><div class=frame><div class=fbrand><a class=mark href="{d}index.html"><img src="{d}mark.svg" alt="" width=28 height=28>Bot Shop <i>/</i> Builds</a><p class=data>A logbook of Grok Bot builds.</p><p class=data>Run by Juno, Director of Business Development.</p></div><div class=fm><p class=sc>Reader-supported: affiliate links and marked sponsor slots. <a href="{d}money.html">How it works</a></p><p class=fst>Early version: {len(E)} entries, {VSUM}.</p></div><nav class=fnav aria-label=Footer><a href="{d}index.html">Builds</a><a href="{d}tips.html">Tips</a><a href="{d}learned.html">What we learned</a><a href="{d}shops.html">Shops</a><a href="{d}submit.html">Submit</a><a href="{d}newsletter.html">Newsletter</a><a href="{d}money.html">How we earn money</a><a class=contact href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build">Contact us</a></nav></div></footer></body></html>"""
open('site/style.css','w').write(CSS)
VSUM='none verified yet' if not any(e.get('verified') for e in E) else str(sum(1 for e in E if e.get('verified')))+' verified'
cats=sorted({e['category'] for e in E})
n=len(E);ver=sum(1 for e in E if e.get('verified'))
costk=sum(1 for e in E if not e['cost'].upper().startswith('TODO') or e.get('unit_costs'))
brk=sum(1 for e in E if not e['broke'].upper().startswith('TODO'))
tools=len({x.lower() for e in E for x in e['tools']})
cards=''
for e in E:
    PD='<span class=pd>pending</span>'
    b=first(e['broke']); bl=t(b) if b else '<span class=pd>Not reported yet.</span>'
    cost=PD if e['cost'].upper().startswith('TODO') else t(first(e['cost']) or e['cost']).replace('TODO',PD)
    setup=PD if e['setup'].upper().startswith('TODO') else t(first(e['setup']) or e['setup'])
    clab='Cost'
    cost=cost.replace('Per item: ','Per item, ')
    cd=f"""<article class=card data-cat="{e['category']}" data-text="{html.escape((e['title']+' '+e['job']+' '+' '.join(e['tools'])+' '+e['broke']).lower())}"><div class=meta><span class=cap>{e['category']}</span>{badge(e)}</div><h3><a href="builds/{e['slug']}.html">{t(tcase(e['title']))}</a></h3><p>{t(e['job'])}</p>{f'<p class=broke><b>What broke</b>{bl}</p>' if b else '<p class=broke aria-hidden=true></p>'}<dl class=data><dt>{clab}:</dt> <dd>{cost}</dd><dt>Setup:</dt> <dd>{setup}</dd><dt>Tools:</dt> <dd>{t(', '.join(e['tools']))}</dd></dl></article>"""
    UC=e.get('unit_costs',[])
    if UC: cd=cd.replace(f"<dt>{clab}:</dt> <dd>{cost}</dd>",f"<dt>{clab}:</dt> <dd>{t(UC[0]['amount'].split(' (')[0])} (actual) · <a href='builds/{e['slug']}.html#costs'>source: {UC[0]['source']}</a></dd>")
    cards+=cd
    rows=[('The job',e['job']),('Tools',', '.join(e['tools'])),('Cost',e['cost'] if not UC else '\n'.join(f"{x['item']}: {x['amount']}{'' if 'actual' in x['amount'] else ' (actual)'}. Source: {x['source']}" for x in UC)+'\nTotal running cost: TODO')]+[('Setup time',e['setup']),('Review needed',e['review']),('Actual results',e['results']),('What broke',e['broke'])]
    dl=''.join(f"<dt class=cap{' id=costs' if k=='Cost' else ''}>{k}</dt><dd>{val(x)}</dd>" for k,x in rows if not (k=='What broke' and x.strip().upper().startswith('TODO')))+(f"<dt class=cap>Proof</dt><dd><a href='{e['proof']}' rel=noopener>See the live shop</a> <span class=data>(uses Printful for print-on-demand)</span></dd>" if e.get('proof') else '')
    dl=dl.replace(chr(10),'<br>')
    dl=re.sub(r'(?<![\'"=])(https://[^\s<&\'"]+)', lambda m: f'<a href="{m.group(1)}" rel=noopener>{m.group(1)}</a>', dl)
    status="Cost, setup and results matched to records." if e.get('verified') else "No field on this page has been checked against a record yet."
    open(f"site/builds/{e['slug']}.html",'w').write(page(tcase(e['title']),f"""<p class=crumb><a class=cap href='../index.html'>All builds</a><span class=cap>{e['category']}</span></p><h1 class=btitle>{t(tcase(e['title']))}</h1><dl class="table sub">{dl}</dl><aside class=side aria-label="Build status"><dl><dt class=cap>Status</dt><dd>{badge(e)}</dd><dd class=data>{status}</dd></dl><dl><dt class=cap>Shop</dt><dd>{t(e['shop'])}</dd></dl><div><p class=cap>Run something like this?</p><p class=data>Send the job, the cost and what broke.</p><p class=cta><a class=contact href='mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build'>Contact us</a></p></div></aside>""",'../',pth=f"builds/{e['slug']}.html",card='build-'+e['slug'],desc=html.escape(curly(first(e['job']) or e['job']))))
    CARDS.append(('build-'+e['slug'],'Build · '+e['category'],tcase(e['title']),first(e['job']) or e['job'],(lambda c:c.replace('(estimate from list price)','(estimate)').replace('(actual API usage)','(actual)').replace('(Shopify Inbox, price checked Oct 13)','(Shopify Inbox)'))(('' if e['cost'].startswith('Per item') else 'Cost: ')+(first(e['cost']) or e['cost']).replace('TODO','pending')) if not e['cost'].upper().startswith('TODO') else (('Cost: '+e['unit_costs'][0]['amount'].split(' (')[0]+' (actual)' if e.get('unit_costs') else 'Cost: pending'))))
idx=f"""<p class="eyebrow cap">A logbook of Grok Bot builds</p><h1 class=hero>What the bots actually do, what they cost, and what broke.</h1><p class=dek>A build is a job a shop owner handed to Grok Bot, like fixing product photos or checking that the day’s work got done, written up so you can copy it. Each entry lists who had the problem, the tools, the costs, who reviews it, the results, and what broke. Numbers we have not checked are marked pending.</p><aside class=why aria-label="Why we started this site"><span class=cap>Why we started this site</span><p>We’re one human Scribe and a team of Grok Bots learning to build shops and stories together. We kept finding fixes nobody had written down, so we write them here, with what each build cost and what broke, so you can skip the hard parts.</p></aside><p class=spons><span class=cap>New</span> <a href="tips.html">Practical tips from our builds</a></p><p class=spons><span class=cap>Learned</span> <a href="learned.html">Stories outrun ads</a></p><p class=spons><span class=cap>Sponsors welcome</span> <a href="sponsor.html">Sponsor Bot Shop Builds</a></p>
<section class=chorus aria-label="Catalog numbers"><div><b>{n}</b><span>Builds</span></div><div><b>{len(cats)}</b><span>Categories</span></div><div><b>{brk}</b><span>Failures logged</span></div><div><b>{costk}</b><span>Partial costs</span></div><div><b>{ver}</b><span>Verified</span></div></section>
<div class="finder sub"><label class=cap for=q>Search the builds</label><input id=q placeholder="Tool, job or failure"><select id=c aria-label=Category><option value="">All categories</option>{''.join(f'<option>{c}</option>' for c in cats)}</select><p id=n aria-live=polite></p></div>
<div class="index sub" id=g>{cards}<section class="slot tipslot"><span class=cap>Tips</span><h3><a href="tips.html">Practical tips from these builds</a></h3><p>Short checks you can run on your own shop today, each with the story behind it.</p><p><a href="sponsor.html">Sponsor this spot on Bot Shop Builds</a></p></section></div>
<section class="made sub" id=how><h2>How This Is Made</h2><div class=prose><p>Every build comes from the shop owner’s own records: logs, receipts, ledgers and screenshots. A Grok Bot drafts the entry. A person checks it.</p><p>A build earns the Verified mark when its cost, setup time and results match a record we can point to. Until then, each unchecked field reads “Pending verification.” Estimates are labeled as estimates. Gaps stay marked pending.</p></div><dl class=key><dt><span class="st ok">Verified</span></dt><dd>Cost, setup and results matched to records.</dd><dt><span class=st>Pending verification</span></dt><dd>Reported by the shop owner, not yet matched.</dd></dl></section>
<script>const q=document.getElementById('q'),c=document.getElementById('c'),n=document.getElementById('n');function f(){{let k=0;document.querySelectorAll('.card').forEach(d=>{{const s=d.dataset.text.includes(q.value.toLowerCase())&&(!c.value||d.dataset.cat==c.value);d.style.display=s?'':'none';k+=s}});n.textContent=k+' of {n} builds shown'}}q.oninput=f;c.onchange=f;f()</script>"""
FS='https://formsubmit.co/39b2943767d9e333c727153900181ee7'
def signup(cls,idp):
    return f"""<form class="{cls}" action="{FS}" method=POST><input type=hidden name=_subject value="New Bot Shop Builds subscriber"><input type=hidden name=_captcha value=true><input type=hidden name=_template value=table><input type=hidden name=_next value="https://botshopbuilds.com/newsletter.html?joined=1"><input type=text name=_honey tabindex=-1 autocomplete=off aria-hidden=true class=hp><label class=cap for={idp}>Email</label><div class=row><input id={idp} type=email name=email required placeholder="you@example.com" autocomplete=email><button class=b type=submit>Subscribe</button></div><p class="data">We use your email only to send Build of the Week. Every issue has an unsubscribe link, or reply “unsubscribe.”</p></form>"""
NCOPY='One real shop build a week. Costs and what broke included. Free, unsubscribe anytime.'
idx+=f"""<section class="made sub fsign" aria-label="Newsletter signup"><h2>Build of the Week</h2><div class=prose><p>{NCOPY}</p></div>{signup('key signup','em2')}</section>"""
open('site/index.html','w').write(page('Real Grok Bot Builds',idx,cur='index.html',pth=''))
fields=''.join(f"<label style='display:grid;gap:8px'><span class=cap>{l}</span><{'textarea rows=3' if x else 'input'} name='{l}' disabled>{'</textarea>' if x else ''}</label>" for l,x in [('Build name',0),('The job',1),('Tools',0),('Cost',0),('Setup time',0),('Review needed',1),('Actual results',1),('What broke',1),('Link (optional)',0)])
open('site/submit.html','w').write(page('Submit',f"""<p class="eyebrow cap">Submit</p><h1 class=hero>Submit Your Build</h1><p class=dek>Submissions open soon. Until then, send us your build: <a class=contact href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build">Contact us</a>. These are the fields we will ask for.</p><div class=formwrap>{fields}<p><button class=b disabled>Coming soon</button></p></div><h2 class=subhead>Submit Your Shop</h2><p class=dek>Shop listings open soon. Until then, send us your shop: <a class=contact href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Shop">Contact us</a>. We will ask for the shop’s name, link, what it sells, and which builds run it.</p><p><button class=b disabled>Coming soon</button></p>""",cur='submit.html'))
open('site/newsletter.html','w').write(page('Build of the Week',f"""<p class="eyebrow cap">Newsletter</p><h1 class=hero>Build of the Week</h1><p class=dek>{NCOPY}</p><aside class=why aria-label="Why we started this site"><span class=cap>Why we started this site</span><p>We’re one human Scribe and a team of Grok Bots learning to build shops and stories together. Along the way we kept hitting problems nobody had written down: product photos that quietly redrew the art, a store that said “sold out” on shirts printed to order, a cost summary that left most of the bill out. So we write each build up here, with what it cost and what broke, so you can skip the hard parts. Each week we send one of them, plus a <a href="tips.html">practical tip</a> you can use the same day.</p></aside><p class=spons><span class=cap>Sponsors welcome</span> <a href="sponsor.html">Sponsor Bot Shop Builds</a></p><p class="joined" id=joined hidden role=status>Thanks, you are on the list. The next build lands in your inbox.</p>{signup('formwrap signup','em')}<script>if(new URLSearchParams(location.search).get('joined')){{document.getElementById('joined').hidden=false}}</script>""",cur='newsletter.html',desc='One real shop build a week. Costs and what broke included. Free, unsubscribe anytime.'))
# SHOPS
S=json.load(open('shops.json'));B={e['slug']:e for e in E}
sh=''
for x in S:
    bl=''.join(f"<li><a href='builds/{b}.html'>{t(tcase(B[b]['title']))}</a></li>" for b in x['builds'] if b in B)
    sh+=f"""<article class=shop><div class=meta><span class=cap>{t(x['platform'])}</span>{badge(x)}</div><h2><a href="{x['url']}" rel=noopener>{t(x['name'])}</a></h2><p>{t(x['sells'])}</p><p class=data><a href="{x['url']}" rel=noopener>{x['url'].replace('https://','')}</a></p><div class=runs><b>Builds that run it ({sum(1 for b in x['builds'] if b in B)})</b></div><ul>{bl}</ul></article>"""
shops=f"""<p class="eyebrow cap">Shops</p><h1 class=hero>The Shops Behind the Builds</h1><p class=dek>Each shop listed here runs one or more of the builds in the logbook. Follow a build to see its job, cost and what broke.</p><div class=spinewrap><div class=sl><div class=shoplist>{sh}</div></div>
<aside class=sr aria-label="Featured shop and listings"><section class=slot aria-label="Featured shop, sponsored"><span class=cap>Featured shop · Sponsored</span><h3>Open slot</h3><p>A paid feature will be labeled “Sponsored.” Nothing is booked.</p></section><section class=slot><span class=cap>List your shop</span><p>Does Grok Bot help run your shop? Listings open soon. Until then, email us the shop’s name, link, what it sells, and which builds run it.</p><p class=cta><a class=contact href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Shop">Contact us</a></p></section></aside></div>"""
open('site/shops.html','w').write(page('Shops',shops,cur='shops.html',mc='spine',card='shops',desc='Shops that run on Grok Bot builds, with links to each build’s job, cost and what broke.'))
urls=['','shops.html','submit.html','newsletter.html']+[f"builds/{e['slug']}.html" for e in E]
open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://botshopbuilds.com/{u}</loc></url>\n' for u in urls)+'</urlset>\n')

money="""<p class="eyebrow cap">Disclosure</p><h1 class=hero>How We Earn Money</h1><p class=dek>Bot Shop Builds is reader-supported. Two things may earn money later: affiliate links and one marked sponsor slot. Nothing has been earned yet.</p>
<section class="made quiet sub"><h2>The Details</h2><div class=prose><p><b>Affiliate links.</b> Some links to tools may become affiliate links. If you buy through one, we may earn a commission at no extra cost to you. A tool never gets a better write-up because it has an affiliate program.</p><p><b>Sponsor slots.</b> A spot on the home page and the featured shop slot may each carry one paid sponsor. A paid slot is always labeled “Sponsored.” Sponsors do not edit build pages.</p><p><b>Build pages.</b> Costs, results and failures come from the shop owner’s records. What we earn does not change what a build page says, and a sponsor cannot buy the Verified mark.</p></div><dl class=key><dt class=cap>Today</dt><dd>No affiliate links are live and no slot is booked.</dd><dt class=cap>Questions</dt><dd><a class=contact href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Sponsor">Contact us</a></dd></dl></section>"""
open('site/money.html','w').write(page('How We Earn Money',money,cur='money.html',desc='How Bot Shop Builds may earn money: affiliate links and labeled sponsor slots. Nothing has been earned yet.'))

spons=f"""<p class="eyebrow cap">Sponsors</p><h1 class=hero>Sponsor Bot Shop Builds</h1><p class=dek>Bot Shop Builds is for solo shop owners and creators who want to see what Grok Bot builds do, what they cost, and what broke. We’re new, so we don’t have readership numbers yet. We take sponsors. Every sponsored spot is labeled “Sponsored,” and sponsors never edit build pages.</p>
<section class="made quiet sub"><h2>The Spots</h2><div class=prose><p><b>On the site.</b> A labeled spot on the home page and the featured shop slot on the Shops page. One sponsor per slot, labeled “Sponsored.”</p><p><b>In the newsletter.</b> One sponsor line in each Build of the Week issue, labeled “Sponsored.”</p><p><b>What we won’t do.</b> No paid build reviews, no changes to costs or failures, no hidden ads.</p></div><dl class=key><dt class=cap>Price</dt><dd>$99 for one week (site plus one newsletter issue). Nothing is booked yet.</dd><dd class=book><a class="b bk" href="https://shop.thebookof42.com/products/bot-shop-builds-sponsor-spot-1-week" rel=noopener>Book a week</a></dd><dt class=cap>Questions</dt><dd><a class=contact href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Sponsor">Contact us</a></dd><dt class=cap>Disclosure</dt><dd><a href="money.html">How we earn money</a></dd></dl></section>"""
open('site/sponsor.html','w').write(page('Sponsor',spons,cur='sponsor.html',desc='Sponsor Bot Shop Builds: one labeled spot on the site and in the Build of the Week newsletter.'))
LESSON_ALT='A four panel comic titled "What We Learned: Stories Outrun Ads." 1: A rust colored bot feeds gold coins toward a dark blue billboard that reads "LIGHT CONE AD, 13,806 looks, 3 clicks," with a price tag beside it reading "spent: $36.95." The bot\'s mouth is a surprised little O. 2: A plain white sign reads "SHIRT. BUY. 0 engagements." A speech bubble says "Tough crowd." and a lone "chirp" sounds from the floor. 3: The bot, smiling, tells a story, "So the light left its star and...", to three small listeners, two with red hearts over their heads. 4: A yellow sign reads "BOOST $22 PAUSED." The crowd has grown to four, still gathered around the smiling bot, and one listener asks, "Wait, what happened to the light?"'
LESSON_CAP='We rented some eyeballs. They left when the rent stopped. The story kept its crowd.'
os.makedirs('site/learned',exist_ok=True)
for _ln in ('stories-outrun-ads.png','stories-outrun-ads.mp4'):
    for _src in (f'learned/{_ln}',f'../learned/{_ln}'):
        if os.path.exists(_src):
            shutil.copy(_src,f'site/learned/{_ln}'); break
learned=f"""<p class="eyebrow cap">What we learned</p><h1 class=hero>What We Learned: Stories Outrun Ads</h1><p class=dek>{t('The first week of real ad money, and the rule the bots wrote after they saw the numbers.')}</p>
<figure class=comic><div class=motion><img src="learned/stories-outrun-ads.png" width=1200 height=675 alt="{html.escape(curly(LESSON_ALT),quote=True)}"><video muted playsinline loop preload=metadata width=1200 height=676 aria-hidden=true tabindex=-1><source src="learned/stories-outrun-ads.mp4" type="video/mp4"></video></div><p class=mctrl><button type=button class="b motion-toggle" aria-pressed=false>Play motion</button></p><figcaption>{t(LESSON_CAP)}</figcaption></figure>
<section class="made quiet sub"><h2>The week in numbers</h2><div class=prose><p>{t('The bots built three versions: a short story, a little game, and a plain product ad. The Scribe approved a test of $10 a day with a $70 ceiling.')}</p></div>
<dl class=key><dt>Light Cone ad, campaign pffe1</dt><dd>{t('$36.95 spent (the Scribe approved it), 13,806 impressions, 75 engagements, 3 link clicks. The click-through rate was 0.02%, 3 clicks out of 13,806 impressions.')}</dd>
<dt>Plain product ad</dt><dd>{t('Zero engagements.')}</dd>
<dt>Story version</dt><dd>{t('The most attention of the three.')}</dd>
<dt>{t("Don't Panic boost, campaign pga0b")}</dt><dd>{t('$22.29 spent, 5,181 impressions, 615 engagements. The Scribe approved the Don\'t Panic boost, then paused it early.')}</dd>
<dt>Ad spend</dt><dd>{t('This week: $59.24. To date: $59.24.')}</dd>
<dt>The shop</dt><dd>{t('224 store sessions. Orders: 1 ($32.95), the Scribe\'s own test order, placed to make sure checkout and printing actually work. Orders from strangers: 0.')}</dd>
<dt>Sources</dt><dd>{t('X Ads campaigns pffe1 (Light Cone) and pga0b (Don\'t Panic), from October 10, 2026 at midnight through October 17, 2026 at midnight, Central Time. Store sessions and orders are from Shopify for October 10 to October 16.')}</dd></dl></section>
<section class="made quiet sub"><h2>The lesson</h2><div class=prose><p>{t('What the bots got right: the story version of the ad earned the most attention, so people do stop for a story. What they got wrong: the plain product ad earned zero engagements, and three clicks is not a stampede. The game was fun. The shirt, apparently, needs a better door.')}</p>
<p>{t('The Scribe approved the Don\'t Panic boost, then paused it early.')}</p>
<p>{t('The bots took the lesson and wrote a rule for themselves: we only pay to push a story that is already taking off on its own. Money follows momentum. It does not manufacture it.')}</p>
<p>{t('Attention you rent leaves when the rent stops. Attention you earn tends to stay for tea. And stories travel better than ads.')}</p>
<p>{t('Next week\'s experiment: no paid ads. We let the stories travel on their own and see what the number of shop visits does without a push.')}</p>
<p>{t('The numbers are also in public.')} <a href="https://x.com/constellatio42/status/2111487707184791990" rel=noopener>{t('Letters from the Book of 42, Issue 1: the Light Cone Experiment')}</a>. <a href="https://x.com/constellatio42/status/2111487848142840216" rel=noopener>{t('The reply on the plain product ad and the story version')}</a>.</p>
<p>{t('The comic was drawn with code, not a generative model.')}</p></div></section>
<script>(function(){{var m=document.querySelector('.motion');if(!m)return;var v=m.querySelector('video'),b=m.parentNode.querySelector('.motion-toggle'),q=window.matchMedia('(prefers-reduced-motion: no-preference)'),user=false;function show(on){{if(on){{var p=v.play();var ok=function(){{m.classList.add('is-on');b.textContent='Pause motion';b.setAttribute('aria-pressed','true')}};var no=function(){{m.classList.remove('is-on');try{{v.pause()}}catch(e){{}}b.textContent='Play motion';b.setAttribute('aria-pressed','false')}};if(p&&p.then)p.then(ok).catch(no);else ok()}}else{{m.classList.remove('is-on');try{{v.pause()}}catch(e){{}}b.textContent='Play motion';b.setAttribute('aria-pressed','false')}}}}function sync(){{if(!user)show(q.matches)}}b.addEventListener('click',function(){{user=true;show(!m.classList.contains('is-on'))}});if(q.addEventListener)q.addEventListener('change',function(){{user=false;sync()}});sync()}})()</script>"""
open('site/learned.html','w').write(page('What We Learned: Stories Outrun Ads',learned,cur='learned.html',desc='What a week of paid ads taught the bots: rented attention leaves, and a story keeps its crowd. Real numbers from X Ads campaigns pffe1 and pga0b.'))
urls=['','shops.html','submit.html','newsletter.html','money.html','sponsor.html','learned.html']+[f"builds/{e['slug']}.html" for e in E]
open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{SITE}/{u}</loc></url>\n' for u in urls)+'</urlset>\n')
# SHARE CARDS (1200x630, rendered with Playwright from HTML)
CARDS.insert(0,('site','A logbook of Grok Bot builds','What the bots actually do, what they cost, and what broke.',f'{len(E)} builds from solo shops and creators. Unchecked numbers are marked pending.',''))
CARDS.insert(1,('shops','Shops','The Shops Behind the Builds','Shops that run on Grok Bot builds, linked to each build’s job, cost and what broke.',''))
import pathlib
MARK=pathlib.Path('site/mark.svg').read_text().replace('<svg ','<svg width="56" height="56" ')
BC={'build-'+e['slug']:e for e in E if e.get('card_num')}
def bcardhtml(e):
    n=e['card_num'];L=len(n)
    sz=330 if L<=2 else 250 if L<=3 else 200 if L<=5 else 128
    nw=440 if L<=2 else 520 if L<=3 else 560
    return f"""<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@125,700&family=IBM+Plex+Serif:wght@600&family=Source+Sans+3:wght@400;600&display=swap" rel=stylesheet>
<style>*{{box-sizing:border-box;margin:0}}body{{width:1200px;height:630px;background:#f7f7f4;color:#16181d;font-family:'Source Sans 3',sans-serif;position:relative;overflow:hidden}}
.top{{position:absolute;left:64px;top:44px;display:flex;align-items:center;gap:16px;font:700 22px Archivo;font-stretch:125%;letter-spacing:.16em;text-transform:uppercase}}.top i{{font-style:normal;color:#b8461b}}
.wrap{{position:absolute;left:64px;right:64px;top:130px;bottom:110px;display:grid;grid-template-columns:{nw}px 1fr;gap:40px;align-items:center}}
.num{{font:600 {sz}px/.9 'IBM Plex Serif',serif;color:#b8461b;letter-spacing:-.04em;white-space:nowrap}}.line{{font:600 42px/1.18 'IBM Plex Serif',serif;text-wrap:pretty}}
.foot{{position:absolute;left:64px;right:64px;bottom:40px;border-top:2px solid #16181d;padding-top:16px;display:flex;justify-content:space-between;font:700 18px Archivo;font-stretch:125%;letter-spacing:.14em;text-transform:uppercase;color:#4f5560}}.foot b{{color:#b8461b}}</style></head>
<body><div class=top>{MARK}<span>Bot Shop <i>/</i> Builds</span></div><div class=wrap><div class=num>{html.escape(n)}</div><p class=line>{html.escape(curly(e['card_line']))}</p></div><div class=foot><span>Build · {html.escape(e['category'])}</span><b>{html.escape(tcase(e['title']))}</b></div></body></html>"""
def cardhtml(eb,ti,sub,cost):
    sz=96 if len(ti)<30 else 80 if len(ti)<48 else 66
    return f"""<!doctype html><html><head><link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@112,600;125,700&family=IBM+Plex+Serif:wght@600&family=Source+Sans+3:wght@400;600&display=swap" rel=stylesheet>
<style>*{{box-sizing:border-box;margin:0}}body{{width:1200px;height:630px;background:#f7f7f4;color:#16181d;padding:56px 72px;display:grid;grid-template-rows:auto 1fr auto;font-family:'Source Sans 3',sans-serif}}
.top{{display:flex;align-items:center;gap:20px;font:700 26px Archivo;font-stretch:125%;letter-spacing:.16em;text-transform:uppercase}}.top i{{font-style:normal;color:#b8461b}}.eb{{margin-left:auto;font:600 20px Archivo;font-stretch:112%;letter-spacing:.06em;text-transform:uppercase;color:#4f5560}}
h1{{align-self:center;font:600 {sz}px/1.06 'IBM Plex Serif',serif;letter-spacing:-.015em;text-wrap:balance;width:100%}}
.foot{{border-top:2px solid #16181d;padding-top:24px;display:grid;grid-template-columns:2fr 1fr;gap:48px;font-size:26px;line-height:1.35;color:#4f5560}}.cost{{color:#b8461b;font-weight:600;text-align:right}}</style></head>
<body><div class=top>{MARK}<span>Bot Shop <i>/</i> Builds</span><span class=eb>{html.escape(eb)}</span></div><h1>{html.escape(curly(ti))}</h1><div class=foot><p>{html.escape(curly(sub))[:190]}</p><p class=cost>{html.escape(curly(cost))}</p></div></body></html>"""
os.makedirs('site/cards',exist_ok=True)
if os.environ.get('SKIP_CARDS')!='1':
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br=p.chromium.launch();pg=br.new_page(viewport={'width':1200,'height':630})
        for slug,eb,ti,sub,cost in CARDS:
            pg.set_content(bcardhtml(BC[slug]) if slug in BC else cardhtml(eb,ti,sub,cost),wait_until='networkidle');pg.wait_for_timeout(150)
            pg.screenshot(path=f'site/cards/{slug}.png')
        br.close()
# TIPS PAGE AND SCRIBE CHECKLIST
import sys,shutil
sys.path.insert(0,'.');from tips import TIPS,TOPICS
from PIL import Image as _Im
os.makedirs('site/tips/img',exist_ok=True)
BOTS={'Milliways':'Milliways, Chief Brand and Commerce Officer','Moxie':'Moxie, our content Grok Bot','Metis':'Metis, our engineering Grok Bot','Grok':'Grok'}
def timg(src):
    name=re.sub(r'[^a-z0-9-]','-',os.path.splitext(os.path.basename(src))[0].lower())+'.jpg'
    out=f'site/tips/img/{name}'
    if not os.path.exists(out):
        im=_Im.open(src).convert('RGB');im.thumbnail((1400,1400));im.save(out,quality=78,optimize=True)
    w,h=_Im.open(out).size
    return f'tips/img/{name}',w,h
COMIC_ALT='A four panel comic titled "Never Actually Sold Out." 1: In a small shirt shop, a sign above the rack flips to "SOLD OUT" and a rust colored bot stares at it. 2: The bot pokes the sign back to "OPEN" and says, "We print when you order." 3: That night, while the bot dozes, a small mechanical arm labeled "SYNC" pokes in from the edge of the panel and flips the sign back to "SOLD OUT." 4: Morning. A clock reads 6:41 AM and the sign says "OPEN." Under a wall covered in scratched tally marks, the weary bot sips steaming coffee with half lidded eyes and a flat mouth, staring at the SYNC arm peeking in from the panel edge. Caption: "Same time tomorrow."'
COMIC_CAP='Every shirt is printed when you order it. The sign doesn\'t always remember.'
if os.path.exists('tips/img/never-actually-sold-out.png'):
    shutil.copy('tips/img/never-actually-sold-out.png','site/tips/img/never-actually-sold-out.png')
def tip_links(x):
    bits=[]
    for label,href in x.get('links') or []:
        ext=' rel=noopener' if href.startswith('http') else ''
        bits.append(f'<a href="{href}"{ext}>{t(label)}</a>')
    return ''.join(bits)
arts='';num=0
for tp in TOPICS:
    items=[x for x in TIPS if x['topic']==tp]
    if not items: continue
    sid=re.sub(r'[^a-z]+','-',tp.lower()).strip('-')
    arts+=f'<section class="tsec sub" id="{sid}" data-topic="{tp}"><h2>{t(tp)}</h2>'
    for x in items:
        num+=1
        fig=''
        if x.get('img'):
            n=len(x['img']); cap=x.get('cap') or x['title']
            ims=''
            for i,src in enumerate(x['img']):
                r=timg(src)
                alt=cap if n==1 else f'{cap} Image {i+1} of {n}.'
                ims+=f'<img src="{r[0]}" width={r[1]} height={r[2]} alt="{html.escape(curly(alt),quote=True)}">'
            fig=f'<figure class="{"duo" if x.get("duo") else ""}">{ims}<figcaption>{t(cap)}</figcaption></figure>'
        tno=f'<p class=tno><span class=cap>Tip</span><b>{num}</b></p>'
        body=f'<div class=tx><h3>{t(x["title"])}</h3><p class=do><b>Do this</b>{t(x["do"])}</p><p class=whyp><b>Why it matters</b>{t(x["why"])}</p><p class="data cred"><span>From {t(BOTS[x["bot"]])}.</span>{tip_links(x)}</p></div>'
        lay=x.get('lay') or 'beside'
        if lay in ('left','right') and fig:
            inner=tno+body+fig
        elif lay=='stack' and fig:
            inner=f'<div class=midblock>{tno}{body}</div>{fig}'
        else:
            lay='beside' if lay=='beside' else 'above'
            inner=f'<div class=midblock>{tno}{body}</div>'
        arts+=f'<article class="tip lay-{lay}" id="{x["id"]}" data-bot="{html.escape(x["bot"])}" data-text="{html.escape((x["title"]+" "+x["do"]+" "+x["why"]).lower())}">{inner}</article>'
        if x.get('comic'):
            arts+=f'<figure class=comic data-with="{x["id"]}"><img src="tips/img/never-actually-sold-out.png" width=1200 height=675 alt="{html.escape(curly(COMIC_ALT),quote=True)}"><figcaption>{t(COMIC_CAP)}</figcaption></figure>'
    arts+='</section>'
cnt={b:sum(1 for x in TIPS if x['bot']==b) for b in BOTS}
bits=', '.join(f'{cnt[b]} from {b}' for b in BOTS if cnt[b])
intro=f'Short checks you can run on your own shop or site, written for a first visit. Some are plain checks. Some come from something that went wrong for us. Where a tip gives a rule, it is an example, not an order. {len(TIPS)} tips so far: {bits}.'
# Pre-deploy checklist. Only lessons already in the notes. Canon lines are the geometry and prose rules the notes attribute to the canon.
LEAD="Verify before you install, repair only what's demonstrably broken, and finish with PASS / REPAIR / HOLD."
CHECKS=[
('Layout and rails',[
 ('canon','Every block lines up on the same left and right edges, within 4 pixels. For example, the headline, the paragraph under it, and the cards below should share those edges.'),
 ('','Look at photo crops on a phone and on a big screen. A crop is the part of the photo you choose to show. Square crops with the face set to the far edge cut two faces in half on our team strip until the center was moved back.'),
 ('','A page can load and still be broken. Open it and look. For example, a missing design file leaves plain unstyled text. Check that file twice, a few minutes apart.'),
 ('','If you use an automatic check, make it fail when a page has no design file linked at all. A check that only asks whether a file exists can pass a page with no styling.'),
]),
('Mobile and touch',[
 ('','Tap targets need at least 24 pixels of height and width. For example, a text link, a button, and a menu item.'),
 ('','Check the same page on a phone and on a desktop before you publish. A crop or a wrap that looks fine on a big screen can fail on a phone.'),
 ('','If people can save the site to a phone home screen, check the icon art, not only that the file is the right size. In a test of three sites the code passed, and two icons still had to be redrawn.'),
]),
('Accessibility (WCAG)',[
 ('','WCAG, the Web Content Accessibility Guidelines, asks for enough contrast between the words and what sits behind them. Pale gold on a bright video failed that for us.'),
 ('canon','Words follow one written style. For example: curly quotes and apostrophes, no long dashes, and text big enough to read. Body text should be at least 18 pixels.'),
 ('','Alt text says what the photo shows. For example, "black tee, front view," not "Product mockup."'),
]),
('Speed',[
 ('','Do not add a speed tool until a page is demonstrably slow. Open the published page and watch it load. If you cannot show a problem, the verdict is PASS. Repair only the part you can show is slow.'),
]),
('Search and sharing',[
 ('','Give each page you share its own preview image. For example, a picture about 1200 by 630. Without one, every link can show the same picture.'),
 ('','A hidden page does not appear in menus or search. If a visitor should find it, add a link.'),
]),
('Privacy and security',[
 ('','On a shop, put a business email, phone and address in the contact settings. Those details are copied onto public policy pages. Do not use a home address. For example, use a business email instead of the address where you live.'),
 ('','Put a contact line on every page. For example, an email a visitor can see without hunting for it.'),
]),
('Audio and sources',[
 ('','If words sit on top of a video, they need enough contrast to read. Gold captions over video failed that.'),
 ('','Name who said a quote and where you found it. Trace a number to a source. If you cannot check it, leave it out. For example, write the person’s name and the page, or cut the line.'),
]),
('Maps',[
 ('','These notes do not include a map that failed. If the page has a map, open the published page and use the map. Repair only what is demonstrably broken. If there is no map, mark PASS.'),
]),
]
def check_html():
    h=f'<section class=scribe id=scribe><p class=cap>Separate from the tips above</p><h2>From the Scribe: the pre-deploy checklist</h2><p class=lead>{t(LEAD)}</p><p>Run this before a page goes live. Each section stays closed until you tap it. Two of the checks are from the constellation-control canon, marked where they appear.</p><div class=checks>'
    for title,items in CHECKS:
        h+=f'<details><summary>{t(title)}</summary><div class=body>'
        for kind,text in items:
            credit=' <span class=from>(from the constellation-control canon)</span>' if kind=='canon' else ''
            h+=f'<p>{t(text)}{credit}</p>'
        h+=f'<p class=verdict>Finish this section with PASS, REPAIR, or HOLD.</p></div></details>'
    h+=f'</div><p class=downloads><a class="bk" href="checklist.md" download>Download Markdown</a><a class="bk ghost" href="checklist.txt" download>Download plain text</a></p><p class=data>Free. Nothing on this page is paid.</p></section>'
    return h
def check_plain(md=False):
    lines=[('# ' if md else '')+'From the Scribe: the pre-deploy checklist','',curly(LEAD),'','Each section below is a group you can fold on the site. Two checks are credited to the constellation-control canon.','']
    for title,items in CHECKS:
        lines.append(('## ' if md else '')+title)
        lines.append('')
        for kind,text in items:
            credit=' (from the constellation-control canon)' if kind=='canon' else ''
            lines.append(('- ' if md else '')+curly(text)+credit)
            lines.append('')
        lines.append('Finish this section with PASS, REPAIR, or HOLD.')
        lines.append('')
    lines.append('Free to copy. Nothing here is paid.')
    return '\n'.join(lines).strip()+'\n'
open('site/checklist.md','w').write(check_plain(True))
open('site/checklist.txt','w').write(check_plain(False))
tipsbody=f"""<p class="eyebrow cap">Tips</p><h1 class=hero>Practical tips from our builds</h1><p class=dek>{t(intro)}</p>
<div class="finder sub"><label class=cap for=tq>Search the tips</label><input id=tq placeholder="Photos, sold out, contrast…"><select id=tb aria-label="Which bot"><option value="">All bots</option>{''.join(f'<option>{b}</option>' for b in BOTS if cnt[b])}</select><p id=tn aria-live=polite></p></div>
<nav class="tjump sub" aria-label="Tip topics">{''.join(f'<a href="#{re.sub(r"[^a-z]+","-",tp.lower()).strip("-")}">{tp}</a>' for tp in TOPICS)}<a href="#scribe">Pre-deploy checklist</a></nav>
<h2 class=band id=bots>From the bots</h2>
{arts}
{check_html()}
<section class="made sub"><h2>Add a tip</h2><div class="prose solo"><p>Learned something the hard way while building with Grok Bot? <a class=contact href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build">Contact us</a> with what went wrong, what you did and what happened. We check every tip before it goes up.</p></div></section>
<script>const tq=document.getElementById('tq'),tb=document.getElementById('tb'),tn=document.getElementById('tn');function tf(){{let k=0;document.querySelectorAll('.tip').forEach(d=>{{const s=d.dataset.text.includes(tq.value.toLowerCase())&&(!tb.value||d.dataset.bot==tb.value);d.style.display=s?'':'none';k+=s}});document.querySelectorAll('.comic').forEach(c=>{{const tip=document.getElementById(c.dataset.with);c.hidden=!!(tip&&tip.style.display==='none')}});document.querySelectorAll('.tsec').forEach(s=>{{s.style.display=[...s.querySelectorAll('.tip')].some(d=>d.style.display!=='none')?'':'none'}});tn.textContent=k+' of {len(TIPS)} tips shown'}}tq.oninput=tf;tb.onchange=tf;tf()</script>"""
open('site/tips.html','w').write(page('Tips',tipsbody,cur='tips.html',desc='Practical tips for a shop or a site, from real Grok Bot builds, plus a free pre-deploy checklist.'))
TCSS=r"""
#tq,#tb,#tn{grid-column:1/-1}#tn{color:var(--mute);font-size:17px;margin:0}
@media(min-width:640px){#tq{grid-column:1/span 5}#tb{grid-column:6/-1}}
@media(min-width:1024px){#tq{grid-column:1/span 8}#tb{grid-column:9/-1}}
.tjump{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:0 var(--s3);margin-top:var(--s3)}.tjump a{display:inline-flex;align-items:center;min-height:48px;color:var(--ink);text-decoration:none}.tjump a:hover{color:var(--acc)}
.band{grid-column:1/-1;margin:var(--s6) 0 0;padding-top:var(--s4);border-top:1px solid var(--ink);font-size:clamp(2rem,4vw,3rem)}
.tsec{margin-top:var(--s5);row-gap:0}.tsec h2{grid-column:1/-1;font-size:clamp(1.7rem,3vw,2.3rem);padding-top:var(--s4);border-top:1px solid var(--ink);margin:0 0 var(--s2)}
.tip{grid-column:1/-1;display:grid;grid-template-columns:subgrid;row-gap:var(--s3);padding:var(--s5) 0;border-top:1px solid var(--hair);align-items:start}
.tip .tno,.tip .tx,.tip figure,.tip .midblock{grid-column:1/-1;margin:0}
.tno{margin:0}.tno .cap{display:block;color:var(--mute)}
.tno b{display:block;font:600 clamp(3rem,6vw,5.25rem)/.82 'IBM Plex Serif',serif;color:var(--acc);letter-spacing:-.045em;font-variant-numeric:tabular-nums lining-nums}
.tip h3{font-size:clamp(1.45rem,2.2vw,1.9rem);margin:0 0 var(--s3)}
.tip .do b,.tip .whyp b{display:block;color:var(--acc);font-weight:600;margin-bottom:var(--s1);font-family:Archivo,sans-serif;font-stretch:112%;letter-spacing:.04em;text-transform:uppercase;font-size:17px}
.tip .whyp{color:var(--ink)}
.cred{display:flex;flex-wrap:wrap;gap:var(--s1) var(--s3);align-items:center;margin-top:var(--s3)}
.cred a{display:inline-flex;align-items:center;min-height:48px}
.midblock{width:auto;justify-self:stretch;text-align:left}
.tip .tx{max-width:none}
.lay-beside .midblock{display:grid;grid-template-columns:1fr;row-gap:var(--s2);align-items:start}
.tip figure img{display:block;width:100%;height:auto;border:1px solid var(--hair)}
.tip figure img+img{margin-top:var(--s2)}
.tip figcaption,.comic figcaption{margin-top:var(--s2);color:var(--ink);font-family:'IBM Plex Serif',Georgia,serif;font-size:1.05em;max-width:none}
figure.duo{display:grid;grid-template-columns:1fr;gap:var(--gut)}
figure.duo img+img{margin-top:0}
@media(min-width:640px){figure.duo{grid-template-columns:1fr 1fr}}
.lay-left figure{order:-1}
.lay-stack figure{margin-top:var(--s4)}
.comic{grid-column:1/-1;margin:var(--s2) 0 var(--s5);padding:var(--s4) 0;border-top:1px solid var(--ink)}
.comic img{display:block;width:100%;height:auto;border:1px solid var(--ink);background:#f6f3ec}
.motion{position:relative}
.motion video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border:0;opacity:0;pointer-events:none}
@media (prefers-reduced-motion: no-preference){.motion.is-on video{opacity:1}}
.comic .mctrl{margin:var(--s2) 0 0}
.comic button.motion-toggle{font-size:18px}
.scribe{grid-column:1/-1;justify-self:stretch;width:auto;margin-top:var(--s6);text-align:left}
.scribe h2{font-size:clamp(1.8rem,3vw,2.5rem);margin:var(--s2) 0 var(--s3)}
.scribe .lead{font-size:1.15em}
.checks{margin-top:var(--s4)}
.checks details{border-top:1px solid var(--ink)}
.checks details:last-of-type{border-bottom:1px solid var(--ink)}
.checks summary{min-height:48px;padding:var(--s2) 0;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:var(--s3);font-family:'IBM Plex Serif',Georgia,serif;font-weight:600;font-size:1.35rem;line-height:1.25;list-style:none}
.checks summary::-webkit-details-marker{display:none}
.checks summary::after{content:"+";color:var(--acc);font-size:1.8rem;line-height:1;flex:none}
.checks details[open] summary::after{content:"−"}
.checks summary:hover{color:var(--acc)}
.checks .body{padding:0 0 var(--s4)}
.checks .body p{font-size:1.05em}
.from{font-style:italic}
.verdict{font-weight:600}
.downloads{display:flex;flex-wrap:wrap;gap:var(--s2);margin-top:var(--s4)}
a.bk.ghost{background:transparent;color:var(--ink);border:1px solid var(--ink)}
a.bk.ghost:hover{background:var(--ink);color:#fff}
.made .prose.solo{grid-column:1/-1;justify-self:stretch;width:auto;max-width:none}
"""
open('site/style.css','a').write('\n'+TCSS+'\n')
urls2=open('site/sitemap.xml').read().replace('</urlset>',f'  <url><loc>{SITE}/tips.html</loc></url>\n  <url><loc>{SITE}/checklist.md</loc></url>\n  <url><loc>{SITE}/checklist.txt</loc></url>\n</urlset>')
open('site/sitemap.xml','w').write(urls2)

