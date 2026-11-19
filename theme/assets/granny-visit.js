'use strict';
window.initGrannyVisit=function(){
 if(window.grannyVisitStarted||!document.querySelector('.brand-logo'))return;
 window.grannyVisitStarted=true;
 const sayings=[
  'Keep this money. No need to tell anyone.',
  'I saved the best mango for you. Shh.',
  'You said you were coming. I started cooking yesterday.',
  'Full already? That was only the first serving.',
  'I put a little money in your bag. For the journey.',
  'You look tired. Come, sit near me.',
  'I said one spoon of ghee. This is my spoon.',
  'Take the bigger piece. I like the little one.',
  'Tell me everything. The food can wait a minute.',
  'I kept your favourite tin. It is still yours.',
  'Take a box home. Bring back yourself.',
  'No special occasion. I just missed you.',
  'A little more? I will pretend I did not hear no.',
  'Your mother said no sweets. I did not hear her.',
  'Call when you reach. Even if it is late.',
  'You are never too grown up for my lap.'
 ];
 const popup=document.createElement('aside');popup.className='granny-visit';popup.hidden=true;
 const image=document.createElement('img');image.alt='';image.src=document.querySelector('.brand-logo').src.replace('ammammas-logo.svg','ammammas-granny.svg');
 const copy=document.createElement('div');copy.className='granny-visit-copy';
 const label=document.createElement('span');label.textContent='Ammamma says';
 const line=document.createElement('p');line.setAttribute('role','status');line.setAttribute('aria-live','polite');line.setAttribute('aria-atomic','true');
 copy.append(label,line);
 const close=document.createElement('button');close.type='button';close.className='granny-visit-close';close.setAttribute('aria-label','Dismiss Ammamma sayings for this visit');close.textContent='\u00d7';
 popup.append(image,copy,close);document.body.append(popup);
 let queue=[],timer,fadeTimer,holdTimer,visible=false,dismissed=false;
 const delay=()=>35000+Math.random()*25000;
 function schedule(ms=delay()){clearTimeout(timer);if(!dismissed)timer=setTimeout(show,ms)}
 function hide(){clearTimeout(holdTimer);visible=false;popup.classList.remove('is-visible');fadeTimer=setTimeout(()=>{popup.hidden=true;line.textContent='';schedule()},1100)}
 function hold(){clearTimeout(holdTimer)}
 function release(){if(visible)holdTimer=setTimeout(hide,12000)}
 function show(){
  if(dismissed)return;
  if(document.hidden||document.querySelector('dialog[open]')||document.querySelector('.search-bar:not([hidden])')){schedule(12000);return}
  if(!queue.length)queue=sayings.map((_,i)=>i).sort(()=>Math.random()-.5);
  popup.hidden=false;line.textContent=sayings[queue.pop()];visible=true;
  requestAnimationFrame(()=>requestAnimationFrame(()=>popup.classList.add('is-visible')));
  holdTimer=setTimeout(hide,14000);
 }
 popup.addEventListener('pointerenter',hold);popup.addEventListener('pointerleave',release);
 popup.addEventListener('focusin',hold);popup.addEventListener('focusout',release);
 close.onclick=()=>{dismissed=true;clearTimeout(timer);clearTimeout(holdTimer);clearTimeout(fadeTimer);popup.classList.remove('is-visible');setTimeout(()=>popup.hidden=true,1100)};
 document.addEventListener('keydown',e=>{if(e.key==='Escape'&&visible)close.click()});
 document.addEventListener('visibilitychange',()=>{if(document.hidden){clearTimeout(timer);if(visible)hide()}else if(!visible)schedule(14000)});
 schedule(10000+Math.random()*6000);
};
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>window.initGrannyVisit());else window.initGrannyVisit();
