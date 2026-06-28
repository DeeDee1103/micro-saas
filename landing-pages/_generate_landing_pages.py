#!/usr/bin/env python3
"""Generate 14 smoke-test landing pages (one per shortlist idea) from a shared template.
Each page: own palette + copy + pain calculator (or hero stat) + steps + proof + pricing + email capture.
Edit a config below and re-run to regenerate any page."""

import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

BASE_CSS = r"""
  *{box-sizing:border-box;margin:0;padding:0}
  html{scroll-behavior:smooth}
  body{background:var(--paper);color:var(--ink);font-family:"Hanken Grotesk",system-ui,sans-serif;font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased}
  .wrap{max-width:1140px;margin:0 auto;padding:0 28px}
  .mono{font-family:"Space Mono",monospace}.serif{font-family:"Fraunces",serif}
  a{color:inherit}::selection{background:var(--accent);color:var(--ink)}
  .eyebrow{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
  .nav{position:relative;z-index:3}
  .nav-inner{display:flex;align-items:center;justify-content:space-between;padding:22px 28px;max-width:1140px;margin:0 auto}
  .brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:19px;letter-spacing:-.01em;color:var(--paper)}
  .brand .dot{width:11px;height:11px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px var(--accent-glow)}
  .nav .ghost{font-size:14px;font-weight:600;color:var(--paper);text-decoration:none;border:1px solid var(--line-on-ink);padding:9px 16px;border-radius:999px;transition:background .2s,border-color .2s}
  .nav .ghost:hover{background:rgba(244,243,237,.08)}
  .hero{background:var(--ink);color:var(--paper);position:relative;overflow:hidden;padding-bottom:78px}
  .hero::after{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(120% 90% at 88% -10%,var(--accent-glow),transparent 55%)}
  .hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:54px;align-items:center;padding-top:34px;position:relative;z-index:2}
  h1{font-family:"Fraunces",serif;font-weight:400;font-size:clamp(38px,5.6vw,66px);line-height:1.04;letter-spacing:-.02em;margin:20px 0 0}
  h1 em{font-style:italic;color:var(--accent-bright)}
  .lede{font-size:clamp(17px,2vw,20px);color:rgba(244,243,237,.82);max-width:36ch;margin-top:22px;line-height:1.5}
  .form{margin-top:30px;display:flex;gap:10px;max-width:460px;flex-wrap:wrap}
  .form input[type=email]{flex:1;min-width:210px;background:rgba(244,243,237,.07);border:1px solid var(--line-on-ink);color:var(--paper);padding:15px 16px;border-radius:12px;font-size:15px;font-family:inherit}
  .form input[type=email]::placeholder{color:rgba(244,243,237,.5)}
  .form input[type=email]:focus{outline:none;border-color:var(--accent);background:rgba(244,243,237,.1)}
  .btn{background:var(--accent);color:var(--ink);border:none;font-family:inherit;font-weight:700;font-size:15px;padding:15px 22px;border-radius:12px;cursor:pointer;transition:transform .12s,background .2s;white-space:nowrap}
  .btn:hover{background:var(--accent-bright);transform:translateY(-1px)}
  .microcopy{font-size:13px;color:rgba(244,243,237,.6);margin-top:12px}
  .form-success{margin-top:18px;font-size:15px;color:var(--accent-bright);font-weight:600;display:none}
  .ticker{background:rgba(244,243,237,.04);border:1px solid var(--line-on-ink);border-radius:18px;padding:26px}
  .ticker .lbl{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:rgba(244,243,237,.6)}
  .ticker .big{font-family:"Space Mono",monospace;font-weight:700;font-size:clamp(32px,5vw,44px);color:var(--loss);margin-top:10px;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
  .ticker .sub{font-size:13px;color:rgba(244,243,237,.55);margin-top:8px;line-height:1.5}
  .ticker .live{display:flex;align-items:center;gap:8px;margin-top:20px;padding-top:18px;border-top:1px solid var(--line-on-ink);font-size:13px;color:rgba(244,243,237,.7)}
  .ticker .live .pulse{width:8px;height:8px;border-radius:50%;background:var(--loss);animation:pulse 1.6s ease-in-out infinite}
  .ticker .live .amt{margin-left:auto;font-family:"Space Mono",monospace;color:var(--loss);font-weight:700;font-variant-numeric:tabular-nums}
  .hero-stat{text-align:left}
  .hero-stat .sbig{font-family:"Fraunces",serif;font-size:clamp(54px,9vw,104px);line-height:.95;letter-spacing:-.03em;color:var(--accent-bright)}
  .hero-stat .scap{color:rgba(244,243,237,.7);font-size:15px;margin-top:14px;max-width:32ch}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.7)}}
  section{padding:84px 0}
  .calc{background:var(--paper);border-top:1px solid var(--line)}
  .section-head{max-width:600px}
  .section-head h2{font-family:"Fraunces",serif;font-weight:400;font-size:clamp(28px,4vw,42px);line-height:1.08;letter-spacing:-.02em;margin-top:12px}
  .section-head p{color:var(--muted);margin-top:14px;font-size:16px}
  .calc-card{margin-top:38px;background:#fff;border:1px solid var(--line);border-radius:20px;padding:34px;display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center;box-shadow:0 24px 48px -32px rgba(17,30,28,.4)}
  .calc-input label{display:block;font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}
  .mrr-field{display:flex;align-items:center;gap:6px;margin-top:14px;border-bottom:2px solid var(--ink);padding-bottom:8px}
  .mrr-field span{font-family:"Fraunces",serif;font-size:34px;color:var(--ink)}
  .mrr-field input{border:none;background:none;font-family:"Fraunces",serif;font-size:40px;color:var(--ink);width:100%;padding:0}
  .mrr-field input:focus{outline:none}
  .slider{width:100%;margin-top:22px;accent-color:var(--accent);height:4px}
  .calc-note{font-size:13px;color:var(--muted);margin-top:18px;line-height:1.5}
  .calc-out{border-left:1px solid var(--line);padding-left:34px}
  .out-row+.out-row{margin-top:26px}
  .out-row .k{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
  .out-row .v{font-family:"Space Mono",monospace;font-weight:700;font-size:clamp(28px,4.4vw,40px);letter-spacing:-.02em;margin-top:6px;font-variant-numeric:tabular-nums}
  .v.loss{color:var(--loss)}.v.gain{color:var(--accent-deep)}
  .out-row .per{font-size:13px;color:var(--muted);font-weight:400;letter-spacing:0;text-transform:none;font-family:"Hanken Grotesk",sans-serif}
  .steps{background:var(--ink);color:var(--paper)}
  .steps .eyebrow{color:var(--accent-bright)}.steps h2{color:var(--paper)}.steps p.intro{color:rgba(244,243,237,.7)}
  .step-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:46px}
  .step{border:1px solid var(--line-on-ink);border-radius:16px;padding:28px;background:rgba(244,243,237,.03)}
  .step .num{font-family:"Space Mono",monospace;font-size:13px;color:var(--accent-bright);letter-spacing:.1em}
  .step h3{font-family:"Fraunces",serif;font-weight:500;font-size:22px;margin-top:16px;line-height:1.15}
  .step p{color:rgba(244,243,237,.72);font-size:15px;margin-top:10px;line-height:1.55}
  .proof{background:var(--paper)}
  .stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:44px}
  .stat{border-top:2px solid var(--accent);padding-top:20px}
  .stat .n{font-family:"Fraunces",serif;font-size:clamp(36px,5vw,52px);line-height:1;letter-spacing:-.02em}
  .stat .d{color:var(--muted);font-size:15px;margin-top:12px;max-width:30ch}
  .proof .caveat{font-size:13px;color:var(--muted);margin-top:30px;max-width:64ch}
  .pricing{background:var(--ink);color:var(--paper)}
  .pricing .eyebrow{color:var(--accent-bright)}.pricing h2{color:var(--paper)}.pricing .intro{color:rgba(244,243,237,.7);max-width:48ch}
  .price-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:46px}
  .tier{border:1px solid var(--line-on-ink);border-radius:18px;padding:30px;background:rgba(244,243,237,.03);display:flex;flex-direction:column}
  .tier.featured{border-color:var(--accent);background:var(--accent-tint)}
  .tier .name{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-bright)}
  .tier .amt{font-family:"Fraunces",serif;font-size:46px;margin-top:14px;letter-spacing:-.02em}
  .tier .amt small{font-size:16px;color:rgba(244,243,237,.6);font-family:"Hanken Grotesk",sans-serif}
  .tier ul{list-style:none;margin:20px 0 26px;display:flex;flex-direction:column;gap:11px}
  .tier li{font-size:14.5px;color:rgba(244,243,237,.82);padding-left:24px;position:relative;line-height:1.45}
  .tier li::before{content:"";position:absolute;left:0;top:7px;width:13px;height:8px;border-left:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg)}
  .tier .btn{margin-top:auto;width:100%;text-align:center;text-decoration:none}
  .tier.featured .badge{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);background:var(--accent);display:inline-block;padding:3px 10px;border-radius:999px;margin-bottom:14px}
  .founding{text-align:center;font-size:14px;color:rgba(244,243,237,.65);margin-top:28px}
  .final{background:var(--paper);text-align:center}
  .final h2{font-family:"Fraunces",serif;font-weight:400;font-size:clamp(30px,4.6vw,50px);line-height:1.05;letter-spacing:-.02em;max-width:20ch;margin:0 auto}
  .final .form{margin:30px auto 0;justify-content:center}
  .final input[type=email]{background:#fff;border:1px solid var(--line);color:var(--ink)}
  .final input[type=email]::placeholder{color:var(--muted)}
  .final .microcopy{color:var(--muted)}.final .form-success{color:var(--accent-deep)}
  footer{background:var(--ink);color:rgba(244,243,237,.6);padding:30px 0;border-top:1px solid var(--line-on-ink)}
  .foot-inner{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;font-size:13px}
  .foot-inner .brand{color:var(--paper);font-size:16px}
  @media(max-width:860px){.hero-grid{grid-template-columns:1fr;gap:36px}.calc-card{grid-template-columns:1fr;gap:28px}.calc-out{border-left:none;border-top:1px solid var(--line);padding-left:0;padding-top:28px}.step-grid,.stat-grid,.price-grid{grid-template-columns:1fr}section{padding:60px 0}}
  @media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
"""

JS_BODY = r"""
(function(){"use strict";
  var FORM_ENDPOINT = ""; // <-- paste Formspree URL or your /api/subscribe; "" = demo mode
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function track(name,props){try{if(window.plausible)window.plausible(name,props?{props:props}:undefined);}catch(e){}}
  function fmt(n,pre,suf){return (pre||"")+Math.round(n).toLocaleString("en-US")+(suf||"");}
  function countUp(el,to,pre,suf,dur){
    if(reduceMotion){el.innerHTML=fmt(to,pre,suf);return;}
    var s=performance.now(),from=0;dur=dur||800;
    function t(now){var p=Math.min(1,(now-s)/dur),e=1-Math.pow(1-p,3);el.innerHTML=fmt(from+(to-from)*e,pre,suf);if(p<1)requestAnimationFrame(t);}
    requestAnimationFrame(t);
  }
  // hero ticker
  var al=document.getElementById("annual-loss");
  if(al){countUp(al,CFG.exampleAnnual,CFG.o1pre,CFG.o1suf,1100);
    var live=document.getElementById("live-loss");
    if(live&&CFG.o1pre==="$"){var ps=CFG.exampleAnnual/(365*24*60*60),st=performance.now();
      function lt(now){live.textContent="$"+(ps*((now-st)/1000)).toFixed(2);requestAnimationFrame(lt);}
      if(!reduceMotion)requestAnimationFrame(lt);else live.textContent="$0.00";}
  }
  // calculator
  var inp=document.getElementById("mrr"),sl=document.getElementById("mrr-slider"),
      o1=document.getElementById("out-loss"),o2=document.getElementById("out-gain");
  if(inp&&CFG.calc){
    var C=CFG.calc;
    function parse(v){var n=parseInt(String(v).replace(/[^0-9]/g,""),10);return isNaN(n)?0:n;}
    function render(x,anim){var a=x*C.f1,b=a*C.f2;
      if(anim){countUp(o1,a,C.o1pre,' <span class="per">'+C.o1suf+'</span>',600);countUp(o2,b,C.o2pre,' <span class="per">'+C.o2suf+'</span>',600);}
      else{o1.innerHTML=fmt(a,C.o1pre,' <span class="per">'+C.o1suf+'</span>');o2.innerHTML=fmt(b,C.o2pre,' <span class="per">'+C.o2suf+'</span>');}}
    inp.addEventListener("input",function(){var n=parse(inp.value);inp.value=n?n.toLocaleString("en-US"):"";if(n)sl.value=Math.max(C.min,Math.min(C.max,n));render(n,false);});
    sl.addEventListener("input",function(){var n=parseInt(sl.value,10);inp.value=n.toLocaleString("en-US");render(n,false);});
    render(C.def,true);
  }
  // tracked links
  document.querySelectorAll("[data-track]").forEach(function(el){el.addEventListener("click",function(){
    var n=el.getAttribute("data-track");
    if(n==="pricing-click")track("Pricing click",{tier:el.getAttribute("data-tier")});
    else if(n==="nav-pricing")track("Nav pricing");});});
  // forms
  function wire(fid,sid){var f=document.getElementById(fid),s=document.getElementById(sid);
    f.addEventListener("submit",function(e){e.preventDefault();var i=f.querySelector("input[type=email]"),em=(i.value||"").trim();
      if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){i.focus();i.style.borderColor="var(--loss)";return;}
      track("Early access",{source:fid});
      function done(){f.style.display="none";s.style.display="block";}
      if(!FORM_ENDPOINT){done();return;}
      fetch(FORM_ENDPOINT,{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify({email:em,source:fid})}).then(done).catch(done);});}
  wire("hero-form","hero-success");wire("final-form","final-success");
})();
"""

def theme_block(t):
    return ("<style>:root{"
        f"--ink:{t['ink']};--paper:#F4F3ED;--accent:{t['accent']};--accent-bright:{t['accent_bright']};"
        f"--accent-deep:{t['accent_deep']};--accent-glow:{t['glow']};--accent-tint:{t['tint']};"
        f"--loss:{t.get('loss','#BF4632')};--muted:#5B6A65;"
        "--line:rgba(17,30,28,.12);--line-on-ink:rgba(244,243,237,.16);}</style>")

def hero_right(cfg):
    if cfg.get("stat"):
        return (f'<div class="hero-stat"><div class="sbig serif">{cfg["stat"]["big"]}</div>'
                f'<div class="scap">{cfg["stat"]["cap"]}</div></div>')
    c=cfg["calc"];pre=c["o1pre"];suf=c["o1suf"]
    live = ('<div class="live"><span class="pulse"></span> Slipping away since you opened this page'
            '<span class="amt" id="live-loss">$0.00</span></div>') if pre=="$" else ''
    return (f'<div class="ticker"><div class="lbl">{cfg["ticker_label"]}</div>'
            f'<div class="big mono" id="annual-loss">{pre}0{suf}</div>'
            f'<div class="sub">{cfg["ticker_sub"]}</div>{live}</div>')

def calc_section(cfg):
    if not cfg.get("calc"): return ""
    c=cfg["calc"]
    return f"""
<section class="calc">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">The cost calculator</span>
      <h2>{cfg['calc_head']}</h2><p>{cfg['calc_sub']}</p></div>
    <div class="calc-card">
      <div class="calc-input"><label for="mrr">{c['label']}</label>
        <div class="mrr-field"><span>{c['prefix']}</span>
          <input id="mrr" class="mono" type="text" inputmode="numeric" value="{c['def']:,}" aria-label="{c['label']}" /></div>
        <input class="slider" id="mrr-slider" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['def']}" aria-label="Adjust value" />
        <p class="calc-note">{cfg['calc_note']}</p></div>
      <div class="calc-out">
        <div class="out-row"><div class="k">{c['out1']}</div><div class="v loss mono" id="out-loss">{c['o1pre']}0 <span class="per">{c['o1suf']}</span></div></div>
        <div class="out-row"><div class="k">{c['out2']}</div><div class="v gain mono" id="out-gain">{c['o2pre']}0 <span class="per">{c['o2suf']}</span></div></div>
      </div></div></div></section>"""

def steps_html(steps):
    items="".join(f'<div class="step"><div class="num">0{i+1}</div><h3>{s[0]}</h3><p>{s[1]}</p></div>' for i,s in enumerate(steps))
    return items

def stats_html(stats):
    return "".join(f'<div class="stat"><div class="n serif">{n}</div><div class="d">{d}</div></div>' for n,d in stats)

def tiers_html(tiers):
    out=""
    for i,t in enumerate(tiers):
        feat=" featured" if i==1 else ""
        badge='<span class="badge">Most popular</span>' if i==1 else ""
        lis="".join(f"<li>{x}</li>" for x in t["feats"])
        out+=(f'<div class="tier{feat}">{badge}<div class="name">{t["name"]}</div>'
              f'<div class="amt">${t["price"]}<small>/mo</small></div><ul>{lis}</ul>'
              f'<a class="btn" href="#get" data-track="pricing-click" data-tier="{t["name"].lower()}">Get early access</a></div>')
    return out

def build(cfg):
    fonts='https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Hanken+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap'
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{cfg['name']} — {cfg['tag']}</title>
<meta name="description" content="{cfg['lede']}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="{fonts}" rel="stylesheet"/>
<!-- ANALYTICS: add your Plausible/other <script> here. Events fired: "Early access", "Pricing click", "Nav pricing". -->
<style>{BASE_CSS}</style>{theme_block(cfg['theme'])}
</head><body>
<div class="hero"><nav class="nav"><div class="nav-inner">
  <div class="brand"><span class="dot"></span>{cfg['name']}</div>
  <a class="ghost" href="#pricing" data-track="nav-pricing">See pricing</a></div></nav>
  <div class="wrap"><div class="hero-grid">
    <div class="hero-copy"><span class="eyebrow">{cfg['eyebrow']}</span>
      <h1>{cfg['h1']}</h1><p class="lede">{cfg['lede']}</p>
      <form class="form" id="hero-form" novalidate>
        <input type="email" name="email" placeholder="you@company.com" aria-label="Email address" required/>
        <button class="btn" type="submit" data-track="early-access">Get early access</button></form>
      <p class="microcopy">{cfg['microcopy']}</p>
      <p class="form-success" id="hero-success">You're on the list. I'll email you the moment it's live.</p></div>
    {hero_right(cfg)}
  </div></div></div>
{calc_section(cfg)}
<section class="steps"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How it works</span><h2>{cfg['steps_head']}</h2>
    <p class="intro">{cfg['steps_intro']}</p></div>
  <div class="step-grid">{steps_html(cfg['steps'])}</div></div></section>
<section class="proof"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Why it matters</span><h2>{cfg['proof_head']}</h2></div>
  <div class="stat-grid">{stats_html(cfg['stats'])}</div>
  <p class="caveat">Figures are industry estimates, not promises about your account — which is exactly why this is worth testing on your real data.</p></div></section>
<section class="pricing" id="pricing"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Pricing</span><h2>{cfg['price_head']}</h2>
    <p class="intro">{cfg['price_intro']}</p></div>
  <div class="price-grid">{tiers_html(cfg['tiers'])}</div>
  <p class="founding">No charge today — early access reserves your founding price for launch.</p></div></section>
<section class="final" id="get"><div class="wrap"><h2>{cfg['final_h2']}</h2>
  <form class="form" id="final-form" novalidate>
    <input type="email" name="email" placeholder="you@company.com" aria-label="Email address" required/>
    <button class="btn" type="submit" data-track="early-access">Get early access</button></form>
  <p class="microcopy">Be first in line — and lock in the founding price.</p>
  <p class="form-success" id="final-success">You're on the list. I'll email you the moment it's live.</p></div></section>
<footer><div class="wrap foot-inner">
  <div class="brand"><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--accent);margin-right:8px"></span>{cfg['name']}</div>
  <div>Built in public · launching soon · © 2026</div></div></footer>
<script>var CFG={json.dumps(cfg.get('js',{}))};{JS_BODY}</script>
</body></html>"""

# ---- shared helper to assemble a calculator js config ----
def jscfg(calc):
    return {"exampleAnnual": calc["def"]*calc["f1"], "o1pre":calc["o1pre"],"o1suf":calc["o1suf"],
            "calc":{"def":calc["def"],"min":calc["min"],"max":calc["max"],
                    "f1":calc["f1"],"f2":calc["f2"],"o1pre":calc["o1pre"],"o1suf":calc["o1suf"],
                    "o2pre":calc["o2pre"],"o2suf":calc["o2suf"]}}

def jstat():
    return {"exampleAnnual":0,"o1pre":"","o1suf":"","calc":None}

T = {  # palettes: ink / accent / accent_bright / accent_deep / glow / tint
 "cyan":dict(ink="#13161D",accent="#3FB8C7",accent_bright="#5FD6E4",accent_deep="#1B7E8A",glow="rgba(63,184,199,.20)",tint="rgba(63,184,199,.08)"),
 "orange":dict(ink="#10243A",accent="#E07A2E",accent_bright="#F39A50",accent_deep="#B85C18",glow="rgba(224,122,46,.20)",tint="rgba(224,122,46,.08)"),
 "blue":dict(ink="#11302A",accent="#4C7DF0",accent_bright="#7099F5",accent_deep="#2F57C4",glow="rgba(76,125,240,.20)",tint="rgba(76,125,240,.08)"),
 "violet":dict(ink="#1A1430",accent="#8A6BF0",accent_bright="#A98FF7",accent_deep="#5E45C0",glow="rgba(138,107,240,.22)",tint="rgba(138,107,240,.08)"),
 "yellow":dict(ink="#0F2A43",accent="#E6B229",accent_bright="#F4C84B",accent_deep="#B98A12",glow="rgba(230,178,41,.20)",tint="rgba(230,178,41,.08)"),
 "brass":dict(ink="#2C1A1E",accent="#C79A45",accent_bright="#E0B85F",accent_deep="#9A722A",glow="rgba(199,154,69,.20)",tint="rgba(199,154,69,.08)"),
 "coral":dict(ink="#152A2E",accent="#E06A52",accent_bright="#F38C76",accent_deep="#B84B36",glow="rgba(224,106,82,.20)",tint="rgba(224,106,82,.08)"),
 "civic":dict(ink="#14301F",accent="#C79A45",accent_bright="#E0B85F",accent_deep="#3E7B4F",glow="rgba(199,154,69,.18)",tint="rgba(199,154,69,.08)"),
 "magenta":dict(ink="#1B1330",accent="#D2509A",accent_bright="#E876B4",accent_deep="#A23270",glow="rgba(210,80,154,.20)",tint="rgba(210,80,154,.08)"),
 "safety":dict(ink="#241E16",accent="#E8590C",accent_bright="#F6792F",accent_deep="#B8430A",glow="rgba(232,89,12,.20)",tint="rgba(232,89,12,.08)"),
 "datagreen":dict(ink="#0E2622",accent="#34C77B",accent_bright="#5BDD99",accent_deep="#1E9258",glow="rgba(52,199,123,.20)",tint="rgba(52,199,123,.08)"),
 "mint":dict(ink="#1A1330",accent="#36C7A0",accent_bright="#5BDDBC",accent_deep="#1E927A",glow="rgba(54,199,160,.20)",tint="rgba(54,199,160,.08)"),
 "navy":dict(ink="#0F2440",accent="#3FA34D",accent_bright="#5FC56C",accent_deep="#2A7836",glow="rgba(63,163,77,.18)",tint="rgba(63,163,77,.08)"),
 "slate":dict(ink="#19222E",accent="#D99B3C",accent_bright="#ECB85C",accent_deep="#A8741F",glow="rgba(217,155,60,.20)",tint="rgba(217,155,60,.08)"),
}

def page(**k): return k

IDEAS = {
"02-tracepoint":page(name="Tracepoint",theme=T["cyan"],tag="error alerts without the Datadog bill",
 eyebrow="For solo devs & small engineering teams",
 h1="Know your app is <em>broken</em> before your users tell you.",
 lede="Lightweight error monitoring and alerting for teams who can't justify Datadog. Send us your logs, get a Slack ping the moment errors spike. That's it.",
 microcopy="Send a test log in two minutes. No agent, no enterprise sales call.",
 ticker_label="A team hit by 8 incidents/month loses, per year",ticker_sub="to manually digging through logs to find the cause — time a good alert would have saved.",
 calc=dict(label="Production incidents per month",prefix="",def_=8,min=1,max=100,step=1,f1=24,f2=0.8,
           out1="Hours lost finding the cause",out2="Hours Tracepoint gives back",o1pre="",o1suf="hrs / year",o2pre="",o2suf="hrs / year"),
 calc_head="How much time do incidents cost you?",calc_sub="Every incident you find by accident is hours of log-spelunking. Here's the yearly tax.",
 calc_note="Assumes ~2 hours per incident spent locating the root cause. Your number depends on your stack — that's what early access measures.",
 steps_head="Three steps to never being surprised.",steps_intro="No agent to install, no per-host pricing.",
 steps=[("Pipe in your logs","Point a log drain or our HTTP endpoint at Tracepoint. We auto-parse nginx, Apache, and JSON app logs."),
        ("We watch for trouble","Error spikes, new exception types, and anomalies trip an alert — with sane cooldowns so one incident isn't fifty pings."),
        ("Get pinged where you work","Slack or email the moment something's wrong, with the context to start debugging immediately.")],
 proof_head="The errors you don't see are the expensive ones.",
 stats=[("Minutes","not hours — how fast you should learn your app is erroring"),("$0 agents","keyword-based ingest, no heavyweight collector to maintain"),("90% less","of the Datadog bill for the one feature you actually use")],
 price_head="Priced for indie budgets.",price_intro="Real alerting without the enterprise contract. Founding prices locked for life.",
 tiers=[dict(name="Solo",price=19,feats=["1 project","Slack + email alerts","7-day log retention","nginx/Apache/JSON parsing"]),
        dict(name="Team",price=39,feats=["5 projects","Custom alert rules","30-day retention","Anomaly detection"]),
        dict(name="Scale",price=99,feats=["Unlimited projects","90-day retention","Priority support","AI error summaries"])],
 final_h2="Stop finding out from your users."),

"03-bridgeline":page(name="Bridgeline",theme=T["orange"],tag="stop re-keying data between your systems",
 eyebrow="For ops teams stuck between two systems",
 h1="Make your <em>legacy</em> system talk to your modern one.",
 lede="The data you re-key by hand every week — between your old system and your new one — synced automatically, with conflict handling and a safety net so nothing gets lost.",
 microcopy="Book a 15-minute fit call. We'll tell you honestly if it's a match.",
 ticker_label="5 hours/week of manual entry costs, per year",ticker_sub="in loaded labor — before counting the errors that slip through when humans copy data by hand.",
 calc=dict(label="Hours per week re-keying data",prefix="",def_=5,min=1,max=40,step=1,f1=2080,f2=0.85,
           out1="Cost of manual data entry",out2="What Bridgeline recovers",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What is manual data entry costing you?",calc_sub="Drag in the hours your team spends moving data between systems each week.",
 calc_note="Assumes a ~$40/hour fully-loaded cost. The error-reduction upside is on top of this.",
 steps_head="Connect once. It runs in the background.",steps_intro="No replatforming, no rip-and-replace.",
 steps=[("Connect both systems","Source and destination, with credentials encrypted. We support files, SFTP, and modern APIs."),
        ("Map your fields","Tell Bridgeline how the two systems' data line up. Transforms handle the messy bits."),
        ("Sync on autopilot","Scheduled or triggered syncs with idempotent upserts, retries, and a dead-letter queue you can replay.")],
 proof_head="Integration gaps are the second-biggest SMB time sink.",
 stats=[("45%","of mid-sized firms lose hours each week to manual data entry between tools"),("8 hrs","a week per person can vanish when systems can't talk to legacy data"),("Zero loss","idempotent upserts + dead-letter replay mean records are never silently dropped")],
 price_head="Cheaper than the hours it gives back.",price_intro="One reliable sync pays for itself in reclaimed time. Founding prices locked for life.",
 tiers=[dict(name="Single",price=99,feats=["1 connection","Scheduled sync","Field mapping + transforms","Error dashboard"]),
        dict(name="Pro",price=199,feats=["5 connections","Triggered + scheduled sync","Dead-letter replay","Conflict review"]),
        dict(name="Business",price=399,feats=["Unlimited connections","Priority support","Custom connectors","Audit trail export"])],
 final_h2="Stop being the integration."),

"04-ledgerlytics":page(name="Ledgerlytics",theme=T["blue"],tag="the subscription reports Stripe won't build",
 eyebrow="For finance teams at subscription businesses",
 h1="The revenue reports your billing tool <em>won't</em> build for you.",
 lede="Connect Stripe, Chargebee, or Recurly and get the MRR, churn, and cohort reports leadership actually asks for — built once, scheduled, and emailed. No more rebuilding them in Excel.",
 microcopy="Read-only access. Connect in minutes, see your real numbers.",
 ticker_label="12 hours/month rebuilding reports costs, per year",ticker_sub="in finance time spent exporting to Excel and stitching together what native dashboards can't show.",
 calc=dict(label="Hours per month building reports",prefix="",def_=12,min=1,max=80,step=1,f1=600,f2=0.8,
           out1="Cost of manual reporting",out2="What Ledgerlytics gives back",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What does manual reporting cost you?",calc_sub="Drag in the hours your team spends each month assembling revenue reports.",
 calc_note="Assumes a ~$50/hour fully-loaded finance cost. Faster board prep is the bonus.",
 steps_head="From raw billing data to board-ready.",steps_intro="No data warehouse, no analyst required.",
 steps=[("Connect your biller","Read-only Stripe, Chargebee, or Recurly. We sync subscriptions, invoices, and customers."),
        ("Build the report once","Pick metrics, dimensions, and filters. MRR, churn, ARPU, cohorts — your definitions, saved."),
        ("Schedule and forget","Dashboards update automatically; PDF/CSV reports land in the right inboxes on your cadence.")],
 proof_head="\"Inadequate reporting\" is the #1 SaaS-tool complaint.",
 stats=[("4.2/5","severity of the reporting gap across 10+ subscription tools reviewed"),("Hours/week","finance teams burn rebuilding in Excel what their billing tool can't export"),("1 report","built once and scheduled beats rebuilding it every month forever")],
 price_head="Less than an afternoon of analyst time.",price_intro="One automated board report pays for the year. Founding prices locked for life.",
 tiers=[dict(name="Starter",price=99,feats=["Stripe connection","Core MRR/churn metrics","5 saved reports","CSV export"]),
        dict(name="Growth",price=199,feats=["Multi-provider","Custom report builder","Scheduled email reports","PDF export"]),
        dict(name="Scale",price=399,feats=["Unlimited reports","Cohort + forecast views","Priority support","AI change narratives"])],
 final_h2="Stop rebuilding the same report."),

"05-swiftcache":page(name="Swiftcache",theme=T["violet"],tag="make your slow API feel instant",
 eyebrow="For SaaS vendors with a speed problem",
 h1="Make your slow app feel <em>instant</em> — without a rewrite.",
 lede="A drop-in read-through caching and prefetch layer that sits in front of your API. Twelve-second loads become sub-second, your churn-from-frustration drops, and you didn't touch your core.",
 microcopy="Request a latency audit. We'll show you where the seconds go.",
 stat=dict(big="12s&nbsp;→&nbsp;&lt;1s",cap="What a read should feel like. Slow loads during time-sensitive work quietly cost you renewals."),
 steps_head="Front your API. Keep your stack.",steps_intro="No re-architecture, no database migration.",
 steps=[("Point traffic at Swiftcache","Reads route through our proxy with your auth passed straight through. Writes are untouched."),
        ("We cache and prefetch","Per-endpoint TTLs and scheduled prefetch keep hot data warm, so users rarely hit a cold miss."),
        ("Watch latency fall","A dashboard of hit rate and p50/p95 latency shows the speed-up — and the churn risk you removed.")],
 proof_head="Slow is a silent churn driver.",
 stats=[("4.5/5","severity buyers assign to slow loads during time-sensitive operations"),("Sub-second","what reads should feel like — cached and prefetched, not re-fetched"),("No rewrite","a layer in front of your API, not a rebuild of it")],
 price_head="A fraction of an engineering quarter.",price_intro="Cheaper than the perf project you keep deferring. Founding prices locked for life.",
 tiers=[dict(name="Indie",price=199,feats=["1 service","Read-through cache","Per-path TTLs","Latency dashboard"]),
        dict(name="Growth",price=399,feats=["5 services","Scheduled prefetch","Invalidation API","Vary-key rules"]),
        dict(name="Scale",price=799,feats=["Unlimited services","Stale-while-revalidate","Priority support","SLA"])],
 final_h2="Stop losing renewals to lag."),

"06-routemetrics":page(name="RouteMetrics",theme=T["yellow"],tag="driver KPIs without the spreadsheet grind",
 eyebrow="For courier & last-mile operations",
 h1="Driver and delivery KPIs <em>without</em> the spreadsheet grind.",
 lede="Import your delivery data and get on-time rates, driver scorecards, and weekly reports automatically. Stop rebuilding the same spreadsheet every Monday.",
 microcopy="Upload a sample CSV and see your metrics in minutes.",
 ticker_label="4 hours/week in spreadsheets costs, per year",ticker_sub="in ops-manager time compiling delivery data by hand — time that should be spent fixing the routes.",
 calc=dict(label="Hours per week compiling reports",prefix="",def_=4,min=1,max=30,step=1,f1=1820,f2=0.85,
           out1="Cost of spreadsheet reporting",out2="Hours RouteMetrics gives back",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What do spreadsheets cost your ops team?",calc_sub="Drag in the hours spent each week turning delivery data into reports.",
 calc_note="Assumes a ~$35/hour ops cost. Better decisions from better metrics are the real prize.",
 steps_head="From CSV to clear in minutes.",steps_intro="Works with the data you already export.",
 steps=[("Import your data","Upload a CSV or Excel export and map the columns once. We validate and normalize it."),
        ("We compute the KPIs","On-time rate, average delivery time, exceptions, and per-driver scorecards — calculated for you."),
        ("Reports on schedule","Dashboards plus weekly PDF reports emailed to whoever needs them.")],
 proof_head="Half the industry still runs on spreadsheets.",
 stats=[("~50%","of courier companies still compile performance data in spreadsheets"),("3-5 hrs","a week spent building basic reports by hand"),("Per-driver","scorecards your current tool probably can't produce")],
 price_head="Less than one driver-hour a week.",price_intro="One better routing decision covers the cost. Founding prices locked for life.",
 tiers=[dict(name="Starter",price=99,feats=["CSV/Excel import","Core delivery KPIs","Driver scorecards","Weekly email report"]),
        dict(name="Growth",price=199,feats=["Scheduled imports","Custom KPIs","PDF exports","Exception alerts"]),
        dict(name="Scale",price=399,feats=["API connector","Unlimited reports","Priority support","Multi-depot views"])],
 final_h2="Give your Mondays back."),

"07-caseguard":page(name="Caseguard",theme=T["brass"],tag="never lose your firm's data again",
 eyebrow="For small & solo law firms",
 h1="Know the moment your case software <em>breaks</em> — and never lose data.",
 lede="Your practice-management software crashes and loses data more than it should. Caseguard watches it around the clock and backs up your data automatically, so an outage is an inconvenience, not a catastrophe.",
 microcopy="No legal jargon, no IT project. Set up in an afternoon.",
 ticker_label="6 hours/week lost to software bugs costs, per year",ticker_sub="in billable time gone to crashes, freezes, and data you had to re-enter — before counting a real data-loss event.",
 calc=dict(label="Hours per week lost to software issues",prefix="",def_=6,min=1,max=40,step=1,f1=2340,f2=0.8,
           out1="Billable time lost to bugs",out2="What Caseguard protects",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What do crashes cost your firm?",calc_sub="Drag in the hours your team loses each week to your case software misbehaving.",
 calc_note="Assumes a ~$45/hour blended rate. A single avoided data-loss event dwarfs this.",
 steps_head="Set it up once. Sleep better.",steps_intro="Sits alongside your existing software — nothing to replace.",
 steps=[("Point us at your software","Uptime and performance checks start running on a schedule you control."),
        ("Automatic backups","Your data is pulled and stored on your schedule, with integrity verified — a backup that can't be validated alerts you."),
        ("Alerts when it counts","The moment it's down or a backup fails, you hear about it — by Slack or email.")],
 proof_head="Data loss is the complaint that never goes away.",
 stats=[("70%+","of legal-software users cite data corruption as a long-standing problem"),("5-7 hrs","a week lost to bugs and crashes in case-management tools"),("Verified","backups — integrity-checked, not just \"completed\"")],
 price_head="Cheaper than one lost afternoon.",price_intro="Peace of mind for less than an hour of billable time. Founding prices locked for life.",
 tiers=[dict(name="Solo",price=79,feats=["Uptime monitoring","Daily backups","Email alerts","Backup integrity checks"]),
        dict(name="Firm",price=149,feats=["Performance monitoring","Hourly backups","Slack + email alerts","Backup history"]),
        dict(name="Practice",price=299,feats=["Anomaly detection","Restore export","Priority support","Multi-app coverage"])],
 final_h2="Never lose a case file again."),

"08-claimsnap":page(name="ClaimSnap",theme=T["coral"],tag="file a damage claim in minutes",
 eyebrow="For short-term rental hosts & managers",
 h1="File a damage claim in <em>minutes</em> — snap photos, we draft the report.",
 lede="Guest trashed the place? Photograph the damage and ClaimSnap drafts an itemized, submittable claim report. You review, we generate the PDF, you get reimbursed faster.",
 microcopy="Built for hosts juggling turnovers, not paperwork.",
 ticker_label="6 claims a year of unreimbursed damage + time costs",ticker_sub="when claims are slow, painful, or abandoned because the paperwork wasn't worth the hassle.",
 calc=dict(label="Damage incidents per year",prefix="",def_=6,min=1,max=60,step=1,f1=250,f2=0.7,
           out1="Unrecovered damage + time",out2="What ClaimSnap helps recover",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What does slow claim-filing cost you?",calc_sub="Drag in how many damage incidents you deal with a year.",
 calc_note="Assumes ~$250 average unreimbursed cost + time per incident. Multi-property hosts feel this most.",
 steps_head="Three steps from damage to claim.",steps_intro="No more wrestling with photos and forms at midnight.",
 steps=[("Snap the damage","Upload photos to a claim. They're stored privately, tied to the booking."),
        ("We draft the report","ClaimSnap describes the damage and drafts an itemized claim you review and edit — nothing's submitted without your sign-off."),
        ("Generate and send","A branded PDF claim, ready to submit to your insurer or the platform.")],
 proof_head="The claim you don't file is money you don't get back.",
 stats=[("Minutes","to assemble a claim instead of an evening of photos and forms"),("Itemized","damage reports that hold up, drafted from your photos"),("Faster","reimbursement when the paperwork is clean the first time")],
 price_head="Less than one abandoned claim.",price_intro="One recovered claim pays for years. Founding prices locked for life.",
 tiers=[dict(name="Host",price=19,feats=["1 property","Photo-to-report drafts","Branded PDF claims","Claim tracking"]),
        dict(name="Plus",price=39,feats=["Up to 5 properties","Itemized cost estimates","Insurer-ready exports","Claim history"]),
        dict(name="Manager",price=79,feats=["Unlimited properties","Team access","Priority support","Bulk claim tools"])],
 final_h2="Stop eating the cost of damage."),

"09-ordinancewatch":page(name="OrdinanceWatch",theme=T["civic"],tag="catch violations before the fine",
 eyebrow="For HOA boards & community managers",
 h1="Catch ordinance violations <em>before</em> the fine arrives.",
 lede="City rules change constantly and a missed one means a fine. OrdinanceWatch reads your local ordinances, checks your properties against them, and flags issues — with the source rule cited — before they cost you.",
 microcopy="Pick your city to start. Advisory, not legal advice.",
 ticker_label="3 fines a year of exposure adds up to",ticker_sub="in penalties and surprise compliance costs that a heads-up would have prevented.",
 calc=dict(label="Potential fines/violations per year",prefix="",def_=3,min=1,max=40,step=1,f1=500,f2=0.9,
           out1="Annual fine exposure",out2="What early warning avoids",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What's your fine exposure?",calc_sub="Drag in how many potential violations or fines you face in a year.",
 calc_note="Assumes ~$500 average per fine/violation. Many ordinances carry per-day penalties on top.",
 steps_head="Compliance you don't have to chase.",steps_intro="We keep the rulebook current so you don't have to.",
 steps=[("We track your ordinances","OrdinanceWatch maintains a structured, current rule set for your jurisdiction."),
        ("We scan your properties","Each property is checked against the active rules, and findings are produced with a severity and the exact ordinance cited."),
        ("You get the heads-up","Alerts before a violation becomes a fine — with a link to the source rule.")],
 proof_head="A missed rule is a needless fine.",
 stats=[("Per-day","penalties make a single missed ordinance expensive fast"),("Cited","every finding links to the source ordinance — no guesswork"),("Current","a maintained rulebook beats checking the city site by hand")],
 price_head="Less than a single fine.",price_intro="One avoided penalty covers the year. Founding prices locked for life.",
 tiers=[dict(name="Board",price=49,feats=["1 jurisdiction","Property scans","Cited findings","Email alerts"]),
        dict(name="Manager",price=99,feats=["Up to 10 properties","Scheduled re-scans","Ordinance-change alerts","Dashboard"]),
        dict(name="Portfolio",price=199,feats=["Multiple jurisdictions","Unlimited properties","Priority support","Export reports"])],
 final_h2="Stop being surprised by fines."),

"10-stocksync":page(name="StockSync",theme=T["magenta"],tag="never oversell again",
 eyebrow="For multi-channel e-commerce sellers",
 h1="Never <em>oversell</em> again across Shopify, Etsy & more.",
 lede="Sell the same product on three platforms and stock drifts out of sync the moment something sells. StockSync keeps every channel accurate in real time — and warns you before you run out.",
 microcopy="Connect your store and watch a sale sync everywhere.",
 ticker_label="10 oversells a month cost, per year",ticker_sub="in refunds, cancellations, angry reviews, and the listings you had to pull to stop the bleeding.",
 calc=dict(label="Oversells / stockouts per month",prefix="",def_=10,min=1,max=200,step=1,f1=540,f2=0.95,
           out1="Lost sales + refund cost",out2="What StockSync prevents",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What do oversells cost you?",calc_sub="Drag in how many oversells or surprise stockouts you hit a month.",
 calc_note="Assumes ~$45 average cost per incident (refund, lost sale, review damage). Conservative for most sellers.",
 steps_head="One source of truth, every channel.",steps_intro="Real-time sync that won't create feedback loops.",
 steps=[("Connect your channels","Shopify, Etsy, and WooCommerce. Import your products in a click."),
        ("Map your SKUs","Link the same product across platforms to one canonical stock count."),
        ("Sync in real time","A sale anywhere updates everywhere instantly — loop-safe, so our own updates never trigger a cascade.")],
 proof_head="Overselling is a tax on growth.",
 stats=[("5 hrs/week","sellers waste managing stock across platforms by hand"),("$2,000/mo","in lost sales is a documented cost of poor cross-channel sync"),("Real-time","not hourly — the only speed that actually prevents oversells")],
 price_head="One prevented oversell a week pays for it.",price_intro="Stop refunding sales you couldn't fulfill. Founding prices locked for life.",
 tiers=[dict(name="Maker",price=99,feats=["2 channels","Real-time sync","SKU mapping","Low-stock alerts"]),
        dict(name="Brand",price=199,feats=["4 channels","Velocity-based alerts","Reconciliation job","Sync history"]),
        dict(name="Scale",price=399,feats=["Unlimited channels","Priority support","Bulk SKU tools","API access"])],
 final_h2="Stop refunding sales you can't fulfill."),

"11-waivertrack":page(name="WaiverTrack",theme=T["safety"],tag="never lose track of a lien waiver",
 eyebrow="For general contractors & project admins",
 h1="Never lose track of a <em>lien waiver</em> again.",
 lede="Lien waivers and bid securities tracked in one place, with automatic reminders before anything lapses. Stop chasing signatures in spreadsheets and stop letting payments get held up.",
 microcopy="Built for the office manager who's tracking it all by hand.",
 ticker_label="8 hours/month chasing paperwork costs, per year",ticker_sub="in admin time spent hunting down signatures and waiver status across email and spreadsheets.",
 calc=dict(label="Hours per month chasing paperwork",prefix="",def_=8,min=1,max=60,step=1,f1=480,f2=0.85,
           out1="Cost of manual tracking",out2="Time WaiverTrack gives back",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What does chasing waivers cost you?",calc_sub="Drag in the hours your team spends each month tracking waivers and securities.",
 calc_note="Assumes a ~$40/hour admin cost. Avoiding a single held-up payment is worth far more.",
 steps_head="Every waiver, one dashboard.",steps_intro="No more spreadsheet archaeology.",
 steps=[("Set up your projects","Add projects, subs, and vendors. Create waiver and bid-security records in seconds."),
        ("Request and track","Send waiver requests, upload signed docs, and watch statuses update in one view."),
        ("Get reminded automatically","Renewal and expiry reminders fire before anything lapses — no missed deadlines.")],
 proof_head="A missed waiver is a held-up payment.",
 stats=[("Manual","is how most GCs still track waivers and bid securities today"),("Delays","from lost paperwork hold up payments and close-outs"),("One view","of every active waiver and security, always current")],
 price_head="Less than one held-up payment.",price_intro="One avoided delay covers years. Founding prices locked for life.",
 tiers=[dict(name="Crew",price=49,feats=["Up to 5 projects","Waiver + security tracking","Document upload","Expiry reminders"]),
        dict(name="GC",price=99,feats=["Unlimited projects","Request links","Status dashboard","Email reminders"]),
        dict(name="Firm",price=199,feats=["E-signature integration","Priority support","Audit trail","Team access"])],
 final_h2="Stop letting payments get held up."),

"12-telemetryhub":page(name="TelemetryHub",theme=T["datagreen"],tag="dashboards your IoT platform won't build",
 eyebrow="For manufacturing & logistics IoT teams",
 h1="Turn device data into the dashboards your platform <em>won't</em> build.",
 lede="Your IoT platform collects everything and reports almost nothing useful. TelemetryHub ingests your device telemetry and turns it into the KPIs, dashboards, and alerts your native tool can't produce.",
 microcopy="Request access and pipe in a test device.",
 ticker_label="6 hours/week wrangling device data costs, per year",ticker_sub="in engineering time spent exporting telemetry and building reports the platform should have produced.",
 calc=dict(label="Hours per week wrangling device data",prefix="",def_=6,min=1,max=40,step=1,f1=2340,f2=0.8,
           out1="Cost of manual data wrangling",out2="What TelemetryHub gives back",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="What does manual data wrangling cost?",calc_sub="Drag in the hours your team spends each week turning telemetry into reports.",
 calc_note="Assumes a ~$45/hour engineering cost. Visibility you didn't have before is the bigger win.",
 steps_head="From raw telemetry to real KPIs.",steps_intro="Works alongside your existing IoT platform.",
 steps=[("Pipe in telemetry","HTTP ingest now, MQTT soon. Keyed and batched for high volume."),
        ("Define your KPIs","Aggregate and roll up the metrics that matter, your way."),
        ("Dashboards, alerts, exports","Charts your platform can't draw, threshold alerts, and scheduled CSV exports.")],
 proof_head="Great data, useless reporting.",
 stats=[("23 of 27","IoT analytics tools reviewed drew complaints about reporting"),("Premium","is what manufacturing/logistics teams pay for analytics that work"),("Your KPIs","not the handful the platform decided to show you")],
 price_head="A fraction of an engineer's week.",price_intro="Cheaper than building it in-house. Founding prices locked for life.",
 tiers=[dict(name="Line",price=199,feats=["HTTP ingest","Core KPI engine","Dashboards","Threshold alerts"]),
        dict(name="Plant",price=399,feats=["Higher volume","Custom aggregations","Scheduled exports","Anomaly alerts"]),
        dict(name="Enterprise",price=799,feats=["MQTT ingest","Retention controls","Priority support","SLA"])],
 final_h2="Stop exporting to Excel to see anything."),

"13-spendlens":page(name="SpendLens",theme=T["mint"],tag="find subscriptions you forgot you pay for",
 eyebrow="For small businesses & finance ops",
 h1="Find the subscriptions you <em>forgot</em> you're paying for.",
 lede="Connect your accounting or bank feed and SpendLens finds every recurring charge, flags the duplicates and dead ones, and shows you exactly what to cut. Saving money sells itself.",
 microcopy="Read-only access. See your savings before you commit.",
 ticker_label="30 subscriptions of likely waste add up to",ticker_sub="in tools nobody uses, duplicate services, and quiet price hikes hiding in your monthly spend.",
 calc=dict(label="Active SaaS subscriptions",prefix="",def_=30,min=1,max=300,step=1,f1=180,f2=0.4,
           out1="Likely wasted per year",out2="What you can realistically cut",o1pre="$",o1suf="/ year",o2pre="$",o2suf="/ year"),
 calc_head="How much are you wasting on software?",calc_sub="Drag in roughly how many active subscriptions your business pays for.",
 calc_note="Assumes ~$15/month of waste per tool and a conservative 40% you can actually cut. Most find more.",
 steps_head="Find it, flag it, cut it.",steps_intro="One connection, immediate clarity.",
 steps=[("Connect your books","Read-only access to your accounting tool or bank feed. We sync the transactions."),
        ("We find the recurring charges","SpendLens groups vendors and cadences to surface every subscription you're paying."),
        ("Cut the waste","Duplicates, dormant tools, and price hikes flagged with the savings — plus a monthly recap.")],
 proof_head="Subscription sprawl is real money.",
 stats=[("Forgotten","subscriptions are something nearly every business discovers it has"),("Duplicates","across categories quietly double-charge for the same job"),("Saves money","the easiest ROI pitch there is — you cut more than you pay us")],
 price_head="It pays for itself in the first cut.",price_intro="One cancelled tool usually covers the year. Founding prices locked for life.",
 tiers=[dict(name="Starter",price=20,feats=["1 connection","Recurring-charge detection","Duplicate flags","Savings dashboard"]),
        dict(name="Business",price=49,feats=["Multiple connections","Price-hike + dormant flags","Monthly email recap","Vendor notes"]),
        dict(name="Pro",price=99,feats=["Unlimited connections","Team access","Priority support","Export reports"])],
 final_h2="Stop paying for tools nobody uses."),

"14-inboxap":page(name="InboxAP",theme=T["navy"],tag="stop hand-keying invoices",
 eyebrow="For AP teams & bookkeepers",
 h1="Stop <em>hand-keying</em> invoices. Extract, match, approve.",
 lede="Forward or upload an invoice and InboxAP pulls out every field and line item, matches it to your PO, and routes it for approval. You review the uncertain bits — it never auto-pays.",
 microcopy="Try it on a single invoice. See the extraction yourself.",
 ticker_label="300 invoices/month of manual entry costs, per year",ticker_sub="in hours spent typing vendor names, amounts, and line items off PDFs — and fixing the typos later.",
 calc=dict(label="Invoices processed per month",prefix="",def_=300,min=10,max=5000,step=10,f1=0.6,f2=0.85,
           out1="Hours hand-keying invoices",out2="Hours InboxAP saves",o1pre="",o1suf="hrs / year",o2pre="",o2suf="hrs / year"),
 calc_head="How many hours go into data entry?",calc_sub="Drag in how many invoices your team processes a month.",
 calc_note="Assumes ~3 minutes of manual entry per invoice. Fewer errors downstream is the hidden saving.",
 steps_head="From inbox to approved.",steps_intro="Human-in-the-loop where it matters, automation where it doesn't.",
 steps=[("Invoices come in","Forward to a dedicated address or upload them. Stored securely."),
        ("We extract the data","Every field and line item, with a confidence score. Low-confidence fields are flagged for your review — nothing's assumed."),
        ("Match, approve, export","Match to a PO, route for approval, and sync the approved invoice to your accounting tool.")],
 proof_head="Manual AP is slow and error-prone.",
 stats=[("Hundreds","of invoices a month is normal for mid-market finance teams"),("Mission-critical","errors in AP cost real money — worth paying to prevent"),("Never auto-pays","you approve every invoice; the tedious part is what's automated")],
 price_head="Less than the hours it saves.",price_intro="One reclaimed afternoon a week covers it. Founding prices locked for life.",
 tiers=[dict(name="Solo",price=99,feats=["Upload + email intake","Field + line-item extraction","Review queue","CSV export"]),
        dict(name="Team",price=199,feats=["PO matching","Approval routing","Accounting sync","Audit trail"]),
        dict(name="Business",price=399,feats=["High volume","Priority support","Custom fields","Multi-entity"])],
 final_h2="Stop typing invoices by hand."),

"15-claimscribe":page(name="ClaimScribe",theme=T["slate"],tag="draft claim narratives in minutes",
 eyebrow="For insurance brokers & agencies",
 h1="Draft claim narratives in <em>minutes</em>, not hours.",
 lede="Enter the facts, pick the claim type, and ClaimScribe drafts a properly formatted narrative in the right tone. You edit and export. It writes from your facts only — it never invents details.",
 microcopy="Built for the repetitive writing, not the judgment calls.",
 ticker_label="15 narratives/week of drafting time costs, per year",ticker_sub="in broker hours spent writing the same kinds of claim narratives from a blank page, over and over.",
 calc=dict(label="Claim narratives per week",prefix="",def_=15,min=1,max=200,step=1,f1=26,f2=0.7,
           out1="Hours drafting narratives",out2="Hours ClaimScribe saves",o1pre="",o1suf="hrs / year",o2pre="",o2suf="hrs / year"),
 calc_head="How much time goes into narratives?",calc_sub="Drag in how many claim narratives you draft in a typical week.",
 calc_note="Assumes ~30 minutes per narrative from scratch. ClaimScribe gets you to a solid first draft instantly.",
 steps_head="Facts in, polished draft out.",steps_intro="Verticalized templates, not a generic chatbot.",
 steps=[("Enter the facts","Fill a structured form for the claim type. Your inputs are the only source."),
        ("Get a grounded draft","ClaimScribe writes the narrative in the right format and tone — and flags any missing fact rather than inventing one."),
        ("Edit and export","Tweak, regenerate, and export to PDF or Word. Every version is saved.")],
 proof_head="Claim writing is a top broker time-sink.",
 stats=[("320+","G2 insights flag claim-writing time as a top agency pain"),("3-5x","verticalized AI tools out-earn generic wrappers"),("No fabrication","drafts come from your facts only — missing details are flagged, not invented")],
 price_head="Less than an hour of broker time.",price_intro="A few reclaimed hours a week covers it. Founding prices locked for life.",
 tiers=[dict(name="Agent",price=49,feats=["Core claim types","Grounded AI drafts","PDF/Word export","Version history"]),
        dict(name="Agency",price=99,feats=["All claim types","Custom templates","Tone controls","Team access"]),
        dict(name="Brokerage",price=199,feats=["AMS integration","Priority support","Bulk drafting","Audit log"])],
 final_h2="Stop writing every narrative from scratch."),
}

def normalize(cfg):
    # move calc fields into the shapes build() + JS expect
    if "calc" in cfg and cfg["calc"]:
        c=cfg["calc"]; c["def"]=c.pop("def_")
        cfg["js"]=jscfg(c)
    else:
        cfg["js"]=jstat()
    return cfg

made=[]
for slug,cfg in IDEAS.items():
    cfg=normalize(cfg)
    html=build(cfg)
    path=os.path.join(OUT,f"{slug}-landing.html")
    with open(path,"w") as f: f.write(html)
    made.append(path)
    print("wrote",os.path.basename(path))

print(f"\n{len(made)} pages generated.")
