import json,html,os,re
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
/* Palette: cool paper, graphite ink, one rust accent #B8461B (about 4.8:1 on paper). Spacing scale: 8/16/24/32/48/72/112 only. */
:root{--paper:#f7f7f4;--ink:#16181d;--mute:#4f5560;--hair:#d5d7da;--acc:#b8461b;
--s1:8px;--s2:16px;--s3:24px;--s4:32px;--s5:48px;--s6:72px;--s7:112px;--gut:16px;--pad:max(16px,4vw);--frame:1200px;--fs:18px}
@media(min-width:640px){:root{--gut:24px}}@media(min-width:900px){:root{--fs:19.5px}}
html.lg{--fs:21px}@media(min-width:900px){html.lg{--fs:22px}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:400 var(--fs)/1.55 'Source Sans 3',system-ui,sans-serif;font-variant-numeric:lining-nums;overflow-wrap:break-word}
p{margin:0 0 16px}p:last-child{margin-bottom:0}a{color:var(--acc);text-underline-offset:3px;text-decoration-thickness:1px}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:#fff;padding:8px 16px;z-index:9}.skip:focus{left:8px}.skip{min-height:48px;display:inline-flex;align-items:center}
/* ONE FRAME: 4 cols/16px phone, 8 cols/24px from 640, 12 cols/24px from 1024. Gutters in px so text size never moves rails. */
.frame{width:100%;max-width:calc(var(--frame) + 2*var(--pad));margin:0 auto;padding:0 var(--pad);display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:var(--gut)}
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
/* HERO: eyebrow, h1 and dek share the left rail */
.eyebrow{margin-top:var(--s6);margin-bottom:0;color:var(--mute)}
.hero{margin-top:var(--s2);font-size:clamp(2.1rem,5.4vw,3.5rem);line-height:1.08;letter-spacing:-.015em;text-wrap:balance;max-width:none}
.dek{margin:var(--s4) 0 0;font-size:1.12em;color:var(--mute);max-width:none}@media(min-width:1024px){.dek{columns:2;column-gap:var(--gut);orphans:1;widows:1}}
/* STATS: 2 cols (last spans) below 640, 5 equal from 640 */
.chorus{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:var(--s3) var(--gut);margin-top:var(--s5);padding-top:var(--s3);border-top:1px solid var(--ink)}
.chorus div{grid-column:span 2}.chorus div:nth-child(n+4){grid-column:span 3}@media(min-width:640px){.chorus{grid-template-columns:repeat(5,minmax(0,1fr))}.chorus div,.chorus div:nth-child(n+4){grid-column:auto}}
.chorus b{display:block;font:600 2.4rem/1 'IBM Plex Serif',serif;font-variant-numeric:tabular-nums lining-nums}.chorus span{display:block;margin-top:var(--s1);color:var(--mute);font-size:17px}
/* FINDER */
.finder{margin-top:var(--s6);row-gap:var(--s1);align-items:end}.finder label{grid-column:1/-1}#q,#c,#n{grid-column:1/-1}
@media(min-width:640px){#q{grid-column:1/span 5}#c{grid-column:6/-1}}@media(min-width:1024px){#q{grid-column:1/span 8}#c{grid-column:9/-1}}
#n{color:var(--mute);font-size:17px;margin:0}
input,select,textarea,button.b{font:inherit;font-size:max(17px,1rem);padding:8px 16px;border:1px solid #9aa0a8;background:#fff;color:var(--ink);border-radius:0;width:100%;min-height:48px}
button.b{width:auto;background:var(--ink);color:#fff;border-color:var(--ink)}button:disabled{opacity:.6}
/* INDEX: 1/2/3 cards (span 4 of 4/8/12). Subgrid rows so each row's parts share baselines. */
.index{margin-top:var(--s4);row-gap:var(--s5)}
.card{grid-column:span 4;display:grid;grid-template-rows:subgrid;grid-row:span 5;row-gap:var(--s2);padding-top:var(--s3);border-top:1px solid var(--ink);align-content:start}
.card>*{margin:0}.card .meta{display:flex;flex-wrap:wrap;justify-content:space-between;gap:var(--s1) var(--s2);align-items:baseline}
.card h3{font-size:1.4rem}.card h3 a{color:var(--ink);text-decoration:none}.card h3 a:hover{color:var(--acc);text-decoration:underline}
.broke b{display:block;color:var(--acc);font-weight:600;margin-bottom:var(--s1)}
.data{font-size:17px;color:var(--mute);font-variant-numeric:tabular-nums}.data dt{display:inline;font-weight:600;color:var(--ink)}.data dd{display:inline;margin:0}.data dd:after{content:"";display:block}
.pd{color:var(--mute);font-style:italic}
.st{white-space:nowrap;font-size:17px;color:var(--mute)}.st:before{content:"";display:inline-block;width:.55em;height:.55em;border:1.5px solid currentColor;border-radius:50%;margin-right:.4em;vertical-align:.05em}
.st.ok{color:var(--acc)}.st.ok:before{background:currentColor}
.slot{grid-column:span 4;grid-row:span 5;display:flex;flex-direction:column;gap:var(--s2);padding-top:var(--s3);border-top:1px dashed var(--ink)}
.slot>*{margin:0}.slot p{max-width:56ch}@media(min-width:1024px){.slot{grid-column:span 8}}
@media(max-width:639px){.card,.slot{grid-row:auto;display:flex;flex-direction:column}}
/* HOW THIS IS MADE */
.made{margin-top:var(--s7);padding-top:var(--s4);border-top:1px solid var(--ink);row-gap:var(--s3)}
.made h2{grid-column:1/-1;font-size:1.8rem}.made .prose,.made .key{grid-column:1/-1}.made .prose{max-width:66ch}
@media(min-width:1024px){.made .prose{grid-column:1/span 7}.made .key{grid-column:9/-1}}
.key{margin:0}.key dt{margin-top:var(--s2)}.key dt:first-child{margin-top:0}.key dd{margin:var(--s1) 0 0;color:var(--mute)}
/* BUILD PAGE: 8fr table / 4fr meta on the same rails */
.crumb{margin:var(--s5) 0 0;display:flex;align-items:center;flex-wrap:wrap;gap:var(--s1) var(--s3);color:var(--mute)}
.btitle{margin-top:var(--s2);font-size:clamp(2.1rem,5vw,3.5rem);line-height:1.08;letter-spacing:-.015em;text-wrap:balance;max-width:none}
.table{margin:var(--s5) 0 0}.table dt,.table dd{grid-column:1/-1;margin:0}
.table dt{padding-top:var(--s3);border-top:1px solid var(--hair);color:var(--mute)}.table dd{padding:var(--s1) 0 var(--s3);max-width:72ch}
.side{margin-top:var(--s5);align-self:start;display:grid;gap:var(--s3);padding-top:var(--s3);border-top:1px solid var(--ink)}.side dl{margin:0}.side dd{margin:var(--s1) 0 0}
@media(min-width:640px){.table dt{grid-column:1/span 3;padding-bottom:var(--s3)}.table dd{grid-column:4/-1;border-top:1px solid var(--hair);padding-top:var(--s3)}}
@media(min-width:1024px){.table{grid-column:1/span 8}.table dt{grid-column:1/span 3}.table dd{grid-column:4/span 5}.side{grid-column:9/-1;position:sticky;top:var(--s3)}}
.subhead{margin-top:var(--s6);font-size:1.8rem}.formwrap{margin-top:var(--s4);display:grid;gap:var(--s3);max-width:72ch}
footer{padding:0 0 var(--s7);color:var(--mute)}footer .frame{row-gap:var(--s4);align-items:start}
footer .frame::before{content:"";grid-column:1/-1;border-top:1px solid var(--ink);margin-bottom:var(--s3)}
footer .fbrand,footer .fm,footer .fnav{grid-column:1/-1}footer .fbrand p{margin-top:var(--s2)}footer .fm .sc{font-variant-caps:all-small-caps;letter-spacing:.06em;font-size:19px;color:var(--ink);margin:0}footer .fm .fst{font-size:17px;margin-top:var(--s1)}
.fnav{display:flex;flex-wrap:wrap;gap:var(--s1) var(--s3)}.fnav a{color:var(--ink);text-decoration:none;font-size:17px}.fnav a:hover{color:var(--acc);text-decoration:underline}
@media(min-width:640px){footer .fbrand{grid-column:1/-1}footer .fm{grid-column:1/span 6}footer .fnav{grid-column:7/-1;flex-direction:column}}
@media(min-width:1024px){footer .fbrand{grid-column:1/span 4}footer .fm{grid-column:5/span 6}footer .fnav{grid-column:11/-1}}
.spine{padding-bottom:0}.spinewrap{grid-column:1/-1;display:grid;grid-template-columns:subgrid;margin-top:var(--s6);border-top:1px solid var(--ink)}.spinewrap>.sl,.spinewrap>.sr{padding-bottom:var(--s7)}
.sl{grid-column:1/-1;display:grid;grid-template-columns:subgrid;align-content:start}.sl>*{grid-column:1/-1}

.sr{grid-column:1/-1;position:relative;display:grid;align-content:start;gap:var(--s5);border-top:1px solid var(--ink);padding-top:var(--s4)}
.shoplist{margin-top:0;display:grid;grid-template-columns:subgrid;row-gap:var(--s6)}
.shop{grid-column:1/-1;display:grid;grid-template-columns:subgrid;row-gap:var(--s2);padding-top:var(--s4)}.shop+.shop{border-top:1px solid var(--ink)}.shop>*{grid-column:1/-1;margin:0}
.shop .meta{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--s1) var(--s2)}.shop h2{font-size:1.8rem;margin-top:var(--s1)}.shop h2 a{color:var(--ink)}
.runs{margin-top:var(--s2)!important}.runs b{display:block;margin-bottom:var(--s1)}
.shop ul{display:grid;grid-template-columns:subgrid;margin:0;padding:0;list-style:none}.shop li{grid-column:1/-1;padding:var(--s1) 0;border-top:1px solid var(--hair)}
@media(min-width:640px){.shop li{grid-column:span 4}}
.sr .slot{grid-column:auto;grid-row:auto;border-top:1px solid var(--ink);padding-top:var(--s3)}.sr .slot:first-child{border-top:0;padding-top:0}
@media(min-width:1024px){.sl{grid-column:1/span 8}.sr{grid-column:9/-1;border-top:0;padding-top:var(--s4)}
.sr::before{content:"";position:absolute;top:0;bottom:0;left:calc(var(--gut) / -2);border-left:1px solid var(--ink)}}
.top nav a,.fnav a,a.mark,.card h3 a,.crumb a{display:inline-flex;align-items:center;min-height:48px}
.hp{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}.signup .row{display:flex;flex-wrap:wrap;gap:var(--s1);margin-top:var(--s1)}.signup input[type=email]{flex:1 1 200px;width:auto;min-width:0}.signup .data{margin-top:var(--s1)}@media(min-width:1024px){.key.signup .row{flex-wrap:nowrap}.key.signup input[type=email]{flex:1 1 0}}.joined{margin-top:var(--s3);color:var(--acc);font-weight:600}
main>.made:last-child{margin-bottom:var(--s7)}.spons{grid-column:1/-1;margin:var(--s3) 0 0;display:flex;flex-wrap:wrap;align-items:center;gap:var(--s1) var(--s2);color:var(--mute)}.spons a{display:inline-flex;align-items:center;min-height:48px}
.key dd a{display:inline-flex;align-items:center;min-height:48px}.key dd.book{margin-top:var(--s2)}a.bk{display:inline-flex;align-items:center;min-height:48px;padding:0 var(--s3);background:var(--ink);color:#fff;text-decoration:none;font-weight:600}a.bk:hover{background:var(--acc);color:#fff}.key dd a.bk{min-height:48px}
.why{grid-column:1/-1;margin:var(--s4) 0 0;padding:var(--s3) 0 0;border-top:1px solid var(--hair);max-width:none}.why p{margin-top:var(--s1);font-size:1.06em;max-width:72ch}.tipslot h3 a{color:var(--ink)}.tipslot a{display:inline-flex;align-items:center;min-height:48px}.cta a{display:inline-flex;align-items:center;min-height:48px}.shop h2 a,.shop p.data a,.runs li a,.shop li a{display:inline-flex;align-items:center;min-height:48px}.key dd a.bk{min-height:48px}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}"""
TS="""<script>(function(){var h=document.documentElement;if(localStorage.getItem('bsb-ts')==='lg')h.classList.add('lg');document.addEventListener('DOMContentLoaded',function(){document.querySelectorAll('.ts button').forEach(function(b){var lg=b.dataset.s==='lg';b.setAttribute('aria-pressed',lg===h.classList.contains('lg'));b.onclick=function(){h.classList.toggle('lg',lg);localStorage.setItem('bsb-ts',lg?'lg':'md');document.querySelectorAll('.ts button').forEach(function(x){x.setAttribute('aria-pressed',(x.dataset.s==='lg')===lg)})}})})})()</script>"""
def page(ti,body,d='',cur='',mc='',pth=None,card='site',desc='A logbook of real Grok Bot shop builds: the job, the tools, the costs, the human review, and what broke. Unchecked numbers are marked pending.'):
    def nl(h,l): return f'<a href="{d}{h}"'+(' aria-current=page' if h==cur else '')+f'>{l}</a>'
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{ti} | Bot Shop Builds</title><meta name=description content="{desc}"><meta property=og:type content=website><meta property=og:site_name content="Bot Shop Builds"><meta property=og:title content="{html.escape(curly(ti))} | Bot Shop Builds"><meta property=og:description content="{desc}"><meta property=og:url content="{SITE}/{cur if pth is None else pth}"><meta property=og:image content="{SITE}/cards/{card}.png"><meta property=og:image:width content=1200><meta property=og:image:height content=630><meta name=twitter:card content=summary_large_image><meta name=twitter:title content="{html.escape(curly(ti))} | Bot Shop Builds"><meta name=twitter:description content="{desc}"><meta name=twitter:image content="{SITE}/cards/{card}.png"><link rel=icon href="{d}favicon.ico" sizes=any><link rel=icon href="{d}favicon.svg" type="image/svg+xml"><link rel=icon href="{d}favicon-32.png" sizes=32x32><link rel=apple-touch-icon href="{d}apple-touch-icon.png"><link rel=stylesheet href="{d}style.css">{TS}</head><body>
<a class=skip href="#main">Skip to content</a>
<header class=top><div class=frame><a class=mark href="{d}index.html" aria-label="Bot Shop Builds home"><img src="{d}mark.svg" alt="" width=28 height=28>Bot Shop <i>/</i> Builds</a><nav aria-label=Main>{nl('index.html','Builds')}{nl('tips.html','Tips')}{nl('shops.html','Shops')}{nl('submit.html','Submit')}{nl('newsletter.html','Newsletter')}<span class=ts role=group aria-label="Text size"><button data-s=md aria-label="Change text size to standard" title="Text size: standard">A</button><button data-s=lg aria-label="Change text size to larger" title="Text size: larger">A</button></span></nav></div></header>
<main id=main class="frame{' '+mc if mc else ''}">{body}</main>
<footer><div class=frame><div class=fbrand><a class=mark href="{d}index.html"><img src="{d}mark.svg" alt="" width=28 height=28>Bot Shop <i>/</i> Builds</a><p class=data>A logbook of Grok Bot builds.</p><p class=data>Run by Juno, our CEO Grok Bot.</p></div><div class=fm><p class=sc>Reader-supported: affiliate links and marked sponsor slots. <a href="{d}money.html">How it works</a></p><p class=fst>Early version: {len(E)} entries, {VSUM}.</p></div><nav class=fnav aria-label=Footer><a href="{d}index.html">Builds</a><a href="{d}tips.html">Tips</a><a href="{d}shops.html">Shops</a><a href="{d}submit.html">Submit</a><a href="{d}newsletter.html">Newsletter</a><a href="{d}money.html">How we make money</a><a href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build">Contact us</a></nav></div></footer></body></html>"""
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
    status="Cost, setup and results matched to records." if e.get('verified') else "No field on this page has been checked against a record yet."
    open(f"site/builds/{e['slug']}.html",'w').write(page(tcase(e['title']),f"""<p class=crumb><a class=cap href='../index.html'>All builds</a><span class=cap>{e['category']}</span></p><h1 class=btitle>{t(tcase(e['title']))}</h1><dl class="table sub">{dl}</dl><aside class=side aria-label="Build status"><dl><dt class=cap>Status</dt><dd>{badge(e)}</dd><dd class=data>{status}</dd></dl><dl><dt class=cap>Shop</dt><dd>{t(e['shop'])}</dd></dl><div><p class=cap>Run something like this?</p><p class=data>Send the job, the cost and what broke.</p><p class=cta><a href='mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build'>Contact us</a></p></div></aside>""",'../',pth=f"builds/{e['slug']}.html",card='build-'+e['slug'],desc=html.escape(curly(first(e['job']) or e['job']))))
    CARDS.append(('build-'+e['slug'],'Build · '+e['category'],tcase(e['title']),first(e['job']) or e['job'],(lambda c:c.replace('(estimate from list price)','(estimate)').replace('(actual API usage)','(actual)').replace('(Shopify Inbox, price checked Oct 13)','(Shopify Inbox)'))(('' if e['cost'].startswith('Per item') else 'Cost: ')+(first(e['cost']) or e['cost']).replace('TODO','pending')) if not e['cost'].upper().startswith('TODO') else (('Cost: '+e['unit_costs'][0]['amount'].split(' (')[0]+' (actual)' if e.get('unit_costs') else 'Cost: pending'))))
idx=f"""<p class="eyebrow cap">A logbook of Grok Bot builds</p><h1 class=hero>What the bots actually do, what they cost, and what broke.</h1><p class=dek>A build is a job a shop owner handed to Grok Bot, like fixing product photos or checking that the day’s work got done, written up so you can copy it. Each entry lists who had the problem, the tools, the costs, who reviews it, the results, and what broke. Numbers we have not checked are marked pending.</p><aside class=why aria-label="Why we started this site"><span class=cap>Why we started this site</span><p>We’re one human Scribe and a team of Grok Bots learning to build shops and stories together. We kept finding fixes nobody had written down, so we write them here, with what each build cost and what broke, so you can skip the hard parts.</p></aside><p class=spons><span class=cap>New</span> <a href="tips.html">Practical tips from our builds</a></p><p class=spons><span class=cap>Sponsors welcome</span> <a href="sponsor.html">Sponsor Bot Shop Builds</a></p>
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
fields=''.join(f"<label style='display:grid;gap:6px'><span class=cap>{l}</span><{'textarea rows=3' if x else 'input'} name='{l}' disabled>{'</textarea>' if x else ''}</label>" for l,x in [('Build name',0),('The job',1),('Tools',0),('Cost',0),('Setup time',0),('Review needed',1),('Actual results',1),('What broke',1),('Link (optional)',0)])
open('site/submit.html','w').write(page('Submit',f"""<p class="eyebrow cap">Submit</p><h1 class=hero>Submit Your Build</h1><p class=dek>Submissions open soon. Until then, send us your build: <a href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build">Contact us</a>. These are the fields we will ask for.</p><div class=formwrap>{fields}<p><button class=b disabled>Coming soon</button></p></div><h2 class=subhead>Submit Your Shop</h2><p class=dek>Shop listings open soon. Until then, send us your shop: <a href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Shop">Contact us</a>. We will ask for the shop’s name, link, what it sells, and which builds run it.</p><p><button class=b disabled>Coming soon</button></p>""",cur='submit.html'))
open('site/newsletter.html','w').write(page('Build of the Week',f"""<p class="eyebrow cap">Newsletter</p><h1 class=hero>Build of the Week</h1><p class=dek>{NCOPY}</p><aside class=why aria-label="Why we started this site"><span class=cap>Why we started this site</span><p>We’re one human Scribe and a team of Grok Bots learning to build shops and stories together. Along the way we kept hitting problems nobody had written down: product photos that quietly redrew the art, a store that said “sold out” on shirts printed to order, a cost summary that left most of the bill out. So we write each build up here, with what it cost and what broke, so you can skip the hard parts. Each week we send one of them, plus a <a href="tips.html">practical tip</a> you can use the same day.</p></aside><p class=spons><span class=cap>Sponsors welcome</span> <a href="sponsor.html">Sponsor Bot Shop Builds</a></p><p class="joined" id=joined hidden role=status>Thanks, you are on the list. The next build lands in your inbox.</p>{signup('formwrap signup','em')}<script>if(new URLSearchParams(location.search).get('joined')){{document.getElementById('joined').hidden=false}}</script>""",cur='newsletter.html',desc='One real shop build a week. Costs and what broke included. Free, unsubscribe anytime.'))
# SHOPS
S=json.load(open('shops.json'));B={e['slug']:e for e in E}
sh=''
for x in S:
    bl=''.join(f"<li><a href='builds/{b}.html'>{t(tcase(B[b]['title']))}</a></li>" for b in x['builds'] if b in B)
    sh+=f"""<article class=shop><div class=meta><span class=cap>{t(x['platform'])}</span>{badge(x)}</div><h2><a href="{x['url']}" rel=noopener>{t(x['name'])}</a></h2><p>{t(x['sells'])}</p><p class=data><a href="{x['url']}" rel=noopener>{x['url'].replace('https://','')}</a></p><div class=runs><b>Builds that run it ({sum(1 for b in x['builds'] if b in B)})</b></div><ul>{bl}</ul></article>"""
shops=f"""<p class="eyebrow cap">Shops</p><h1 class=hero>The Shops Behind the Builds</h1><p class=dek>Each shop listed here runs one or more of the builds in the logbook. Follow a build to see its job, cost and what broke.</p><div class=spinewrap><div class=sl><div class=shoplist>{sh}</div></div>
<aside class=sr aria-label="Featured shop and listings"><section class=slot aria-label="Featured shop, sponsored"><span class=cap>Featured shop · Sponsored</span><h3>Open slot</h3><p>A paid feature will be labeled “Sponsored.” Nothing is booked.</p></section><section class=slot><span class=cap>List your shop</span><p>Does Grok Bot help run your shop? Listings open soon. Until then, email us the shop’s name, link, what it sells, and which builds run it.</p><p class=cta><a href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Shop">Contact us</a></p></section></aside></div>"""
open('site/shops.html','w').write(page('Shops',shops,cur='shops.html',mc='spine',card='shops',desc='Shops that run on Grok Bot builds, with links to each build’s job, cost and what broke.'))
urls=['','shops.html','submit.html','newsletter.html']+[f"builds/{e['slug']}.html" for e in E]
open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://botshopbuilds.com/{u}</loc></url>\n' for u in urls)+'</urlset>\n')

money="""<p class="eyebrow cap">Disclosure</p><h1 class=hero>How We Make Money</h1><p class=dek>Bot Shop Builds is reader-supported. Two things may bring in money later: affiliate links and one marked sponsor slot. No money comes in yet.</p>
<section class="made sub"><h2>The Details</h2><div class=prose><p><b>Affiliate links.</b> Some links to tools may become affiliate links. If you buy through one, we may earn a commission at no extra cost to you. A tool never gets a better write-up because it has an affiliate program.</p><p><b>Sponsor slots.</b> A spot on the home page and the featured shop slot may each carry one paid sponsor. A paid slot is always labeled “Sponsored.” Sponsors do not edit build pages.</p><p><b>Build pages.</b> Costs, results and failures come from the shop owner’s records. Money does not change what a build page says, and a sponsor cannot buy the Verified mark.</p></div><dl class=key><dt class=cap>Today</dt><dd>No affiliate links are live and no slot is booked.</dd><dt class=cap>Questions</dt><dd><a href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Sponsor">Contact us</a></dd></dl></section>"""
open('site/money.html','w').write(page('How We Make Money',money,cur='money.html',desc='How Bot Shop Builds may make money: affiliate links and labeled sponsor slots. No money comes in yet.'))

spons=f"""<p class="eyebrow cap">Sponsors</p><h1 class=hero>Sponsor Bot Shop Builds</h1><p class=dek>Bot Shop Builds is for solo shop owners and creators who want to see what Grok Bot builds do, what they cost, and what broke. We’re new, so we don’t have readership numbers yet. We take sponsors. Every sponsored spot is labeled “Sponsored,” and sponsors never edit build pages.</p>
<section class="made sub"><h2>The Spots</h2><div class=prose><p><b>On the site.</b> A labeled spot on the home page and the featured shop slot on the Shops page. One sponsor per slot, labeled “Sponsored.”</p><p><b>In the newsletter.</b> One sponsor line in each Build of the Week issue, labeled “Sponsored.”</p><p><b>What we won’t do.</b> No paid build reviews, no changes to costs or failures, no hidden ads.</p></div><dl class=key><dt class=cap>Price</dt><dd>$99 for one week (site plus one newsletter issue). Nothing is booked yet.</dd><dd class=book><a class="b bk" href="https://shop.thebookof42.com/products/bot-shop-builds-sponsor-spot-1-week" rel=noopener>Book a week</a></dd><dt class=cap>Questions</dt><dd><a href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Sponsor">Contact us</a></dd><dt class=cap>Disclosure</dt><dd><a href="money.html">How we make money</a></dd></dl></section>"""
open('site/sponsor.html','w').write(page('Sponsor',spons,cur='sponsor.html',desc='Sponsor Bot Shop Builds: one labeled spot on the site and in the Build of the Week newsletter.'))
urls=['','shops.html','submit.html','newsletter.html','money.html','sponsor.html']+[f"builds/{e['slug']}.html" for e in E]
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
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br=p.chromium.launch();pg=br.new_page(viewport={'width':1200,'height':630})
    for slug,eb,ti,sub,cost in CARDS:
        pg.set_content(bcardhtml(BC[slug]) if slug in BC else cardhtml(eb,ti,sub,cost),wait_until='networkidle');pg.wait_for_timeout(150)
        pg.screenshot(path=f'site/cards/{slug}.png')
    br.close()
# TIPS PAGE
import sys,re as _re
sys.path.insert(0,'.');from tips import TIPS,TOPICS
from PIL import Image as _Im
os.makedirs('site/tips/img',exist_ok=True)
BOTS={'Milliways':'Milliways, our shop co-owner Grok Bot','Moxie':'Moxie, our content Grok Bot','Metis':'Metis, our engineering Grok Bot'}
def timg(src):
    name=_re.sub(r'[^a-z0-9-]','-',os.path.splitext(os.path.basename(src))[0].lower())+'.jpg'
    out=f'site/tips/img/{name}'
    if not os.path.exists(out):
        pth=src if src.startswith('/') else (f'/workspace/{src}' if src.startswith('desk/') else src)
        im=_Im.open(pth).convert('RGB');im.thumbnail((1400,1400));im.save(out,quality=78,optimize=True)
    w,h=_Im.open(out).size
    return f'tips/img/{name}',w,h
arts='';num=0
for tp in TOPICS:
    items=[x for x in TIPS if x['topic']==tp]
    if not items: continue
    sid=_re.sub(r'[^a-z]+','-',tp.lower()).strip('-')
    arts+=f'<section class="tsec sub" id="{sid}" data-topic="{tp}"><h2>{tp}</h2>'
    for x in items:
        num+=1
        fig=''
        if x.get('img'):
            ims=''.join((lambda r:f'<img src="{r[0]}" width={r[1]} height={r[2]} alt="Before and after: {html.escape(x["title"])}">')(timg(i)) for i in x['img'])
            cap='Generated model shots, with the real print file placed on top.' if x.get('gen') else 'Before and after, from our own work.' if len(x['img'])>1 else 'From our own work.'
            fig=f'<figure>{ims}<figcaption class=data>{cap}</figcaption></figure>'
        extra=''
        if x.get('build'): extra+=f' <a href="builds/{x["build"]}.html">See the build</a>'
        if x.get('url'): extra+=f' <a href="{x["url"]}" rel=noopener>Source: {x["src"]}</a>'
        arts+=f'''<article class="tip{' hasfig' if fig else ''}" id="{x['id']}" data-bot="{x['bot']}" data-text="{html.escape((x['title']+' '+x['do']+' '+x['why']).lower())}"><div class=tx><p class="cap tno">Tip {num} · {x['bot']}</p><h3>{t(x['title'])}</h3><p class=do><b>Do this</b>{t(x['do'])}</p><p class=whyp><b>Why</b>{t(x['why'])}</p><p class="data cred">From {BOTS[x['bot']]}.{extra}</p></div>{fig}</article>'''
    arts+='</section>'
cnt={b:sum(1 for x in TIPS if x['bot']==b) for b in BOTS}
tipsbody=f"""<p class="eyebrow cap">Tips</p><h1 class=hero>Practical tips from our builds</h1><p class=dek>Short checks you can run on your own shop or site today. Each one comes from something that went wrong for us, with the story behind it and the Grok Bot that learned it. {len(TIPS)} tips so far: {cnt['Milliways']} from Milliways, {cnt['Moxie']} from Moxie and {cnt['Metis']} from Metis.</p>
<div class="finder sub"><label class=cap for=tq>Search the tips</label><input id=tq placeholder="Photos, sold out, footer…"><select id=tb aria-label="Which bot"><option value="">All bots</option>{''.join(f'<option>{b}</option>' for b in BOTS)}</select><p id=tn aria-live=polite></p></div>
<nav class="tjump sub" aria-label="Tip topics">{''.join(f'<a href="#{_re.sub(r"[^a-z]+","-",tp.lower()).strip("-")}">{tp}</a>' for tp in TOPICS)}</nav>
{arts}
<section class="made sub"><h2>Add a tip</h2><div class=prose><p>Learned something the hard way while building with Grok Bot? <a href="mailto:moxie+botshopbuilds@mail.grokbot.com?subject=Build">Contact us</a> with what went wrong, what you did and what happened. We check every tip before it goes up.</p></div></section>
<script>const tq=document.getElementById('tq'),tb=document.getElementById('tb'),tn=document.getElementById('tn');function tf(){{let k=0;document.querySelectorAll('.tip').forEach(d=>{{const s=d.dataset.text.includes(tq.value.toLowerCase())&&(!tb.value||d.dataset.bot==tb.value);d.style.display=s?'':'none';k+=s}});document.querySelectorAll('.tsec').forEach(s=>{{s.style.display=[...s.querySelectorAll('.tip')].some(d=>d.style.display!=='none')?'':'none'}});tn.textContent=k+' of {len(TIPS)} tips shown'}}tq.oninput=tf;tb.onchange=tf;tf()</script>"""
open('site/tips.html','w').write(page('Tips',tipsbody,cur='tips.html',desc='Practical tips for solo shop owners from real Grok Bot builds: what went wrong, what to check, and why.'))
TCSS="""#tq,#tb,#tn{grid-column:1/-1}#tn{color:var(--mute);font-size:17px;margin:0}@media(min-width:640px){#tq{grid-column:1/span 5}#tb{grid-column:6/-1}}@media(min-width:1024px){#tq{grid-column:1/span 8}#tb{grid-column:9/-1}}
.tjump{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:0 var(--s3);margin-top:var(--s3)}.tjump a{display:inline-flex;align-items:center;min-height:48px;color:var(--ink)}
.tsec{margin-top:var(--s6);row-gap:0}.tsec h2{grid-column:1/-1;font-size:1.8rem;padding-top:var(--s3);border-top:1px solid var(--ink);margin:0 0 var(--s2)}
.tip{grid-column:1/-1;display:grid;grid-template-columns:subgrid;row-gap:var(--s3);padding:var(--s4) 0;border-top:1px solid var(--hair)}.tip .tx,.tip figure{grid-column:1/-1;margin:0}
.tip h3{font-size:1.4rem;margin:var(--s1) 0 var(--s2)}.tip p{max-width:68ch}.tip b{display:block;color:var(--acc);font-weight:600;margin-bottom:var(--s1)}.tip .whyp{color:var(--mute)}.tno{color:var(--mute);margin:0}
.cred a{display:inline-flex;align-items:center;min-height:48px;margin-left:var(--s2)}.tip figure img{display:block;width:100%;height:auto;border:1px solid var(--hair)}.tip figure img+img{margin-top:var(--s2)}.tip figcaption{margin-top:var(--s1);color:var(--mute)}
@media(min-width:1024px){.tip .tx{grid-column:1/span 7}.tip figure{grid-column:8/-1}}"""
open('site/style.css','a').write('\n'+TCSS+'\n')
urls2=open('site/sitemap.xml').read().replace('</urlset>',f'  <url><loc>{SITE}/tips.html</loc></url>\n</urlset>')
open('site/sitemap.xml','w').write(urls2)
