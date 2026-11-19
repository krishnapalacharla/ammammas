'use strict';
window.initHeritage=function(root=document){
 window.initGrannyVisit?.();
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 root.querySelectorAll('[data-heritage-slider]').forEach(slider=>{
  if(slider.dataset.initialized)return;slider.dataset.initialized='true';
  const slides=[...slider.querySelectorAll('[data-slide]')],dots=[...slider.querySelectorAll('[data-slide-to]')];
  let index=0,paused=reduced,timer,hover=false,touchStart=null;
  const pauseButton=slider.querySelector('[data-slide-pause]');
  function show(next){index=(next+slides.length)%slides.length;slides.forEach((slide,i)=>{const active=i===index;slide.classList.toggle('is-active',active);slide.setAttribute('aria-hidden',String(!active));slide.inert=!active});dots.forEach((dot,i)=>dot.setAttribute('aria-pressed',String(i===index)));}
  function schedule(){clearInterval(timer);if(!paused&&!hover&&!document.hidden)timer=setInterval(()=>show(index+1),6500)}
  function manual(next){show(next);schedule()}
  slider.querySelector('[data-slide-next]').onclick=()=>manual(index+1);
  slider.querySelector('[data-slide-prev]').onclick=()=>manual(index-1);
  dots.forEach(dot=>dot.onclick=()=>manual(Number(dot.dataset.slideTo)));
  pauseButton.onclick=()=>{paused=!paused;pauseButton.textContent=paused?'\u25b6':'\u23f8';pauseButton.setAttribute('aria-label',paused?'Play slideshow':'Pause slideshow');pauseButton.setAttribute('aria-pressed',String(paused));schedule()};
  slider.addEventListener('pointerenter',()=>{hover=true;schedule()});slider.addEventListener('pointerleave',()=>{hover=false;schedule()});
  slider.addEventListener('focusin',()=>{hover=true;schedule()});slider.addEventListener('focusout',e=>{if(!slider.contains(e.relatedTarget)){hover=false;schedule()}});
  slider.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();manual(index+1)}if(e.key==='ArrowLeft'){e.preventDefault();manual(index-1)}});
  slider.addEventListener('touchstart',e=>{touchStart=e.changedTouches[0].clientX},{passive:true});slider.addEventListener('touchend',e=>{if(touchStart!==null){const delta=e.changedTouches[0].clientX-touchStart;if(Math.abs(delta)>50)manual(index+(delta<0?1:-1));touchStart=null}},{passive:true});
  document.addEventListener('visibilitychange',schedule);
  show(0);schedule();if(reduced){pauseButton.textContent=String.fromCharCode(9654);pauseButton.setAttribute('aria-label','Play slideshow');pauseButton.setAttribute('aria-pressed','true');slider.querySelectorAll('animate').forEach(a=>a.remove())}
 });
 document.body.classList.add('motion-ready');
 if(reduced||!('IntersectionObserver'in window)){root.querySelectorAll('[data-reveal]').forEach(n=>n.classList.add('is-revealed'))}else{
  const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-revealed');observer.unobserve(entry.target)}})},{threshold:.07});
  root.querySelectorAll('[data-reveal]:not(.is-revealed)').forEach(n=>observer.observe(n));
 }
};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>window.initHeritage());else window.initHeritage();
document.addEventListener('shopify:section:load',event=>window.initHeritage(event.target));

document.addEventListener('click',e=>document.querySelectorAll('.nav-shop[open]').forEach(menu=>{if(!menu.contains(e.target))menu.open=false}));
document.addEventListener('keydown',e=>{if(e.key==='Escape')document.querySelectorAll('.nav-shop[open]').forEach(menu=>{menu.open=false;menu.querySelector('summary').focus()})});
