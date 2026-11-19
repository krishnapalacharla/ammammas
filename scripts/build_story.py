"""Our Story presentation with original team facts, portraits and links preserved."""
from pathlib import Path
from html import escape as e
import json,re,sys
sys.path.insert(0,str(Path(__file__).parent))
from reference_dom import Parser,Node
R=Path(__file__).resolve().parents[1];T=R/'theme'
D=json.loads((R/'preview/reference-data.json').read_text(encoding='utf-8'))
source=Parser(next(p['content'] for p in D['pages'] if p['path']=='/about')).root
cards=[]
for n in source.all('div'):
    if not any(isinstance(c,Node) and c.tag=='h3' for c in n.children):continue
    title=next(n.all('h3')).text();img=next(n.all('img'),None)
    paras=[p.text() for p in n.all('p') if p.text().strip()]
    links=''.join('<a href="'+e(a.attrs.get('href',''),quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(a.text())+' <span aria-hidden="true">↗</span></a>' for a in n.all('a') if a.attrs.get('href'))
    cards.append('<article class="story-person" data-reveal><div class="story-person-photo"><img src="'+img.attrs['src']+'" alt="'+e(title,quote=True)+'" loading="lazy"></div><div class="story-person-copy"><h3>'+e(title)+'</h3>'+''.join('<p class="'+('story-role' if i==0 else 'story-bio')+'">'+e(p)+'</p>' for i,p in enumerate(paras))+links+'</div></article>')
hero='''<section class="our-story-hero container"><div><span class="eyebrow">Our Story · Since 2019</span><h1>Some flavours<br>feel like <em>home.</em></h1><p>Every jar, every pack, every batter carries the warmth of a home kitchen. That is where our story begins.</p><a class="text-link" href="#people-behind-the-kitchen">Meet the people behind it</a></div><div class="story-granny-frame art-wash"><img src="/assets/ammammas-granny.svg" alt="Ammamma, the heart of our kitchen"><span>“Come, have a little more.”</span></div></section>'''
origin='''<section class="story-origin container"><span class="eyebrow">From Ammamma’s kitchen to yours</span><div class="story-origin-grid"><h2>A small kitchen.<br>A lot of love.</h2><div><p>We started Ammamma’s in 2019 with a simple mission: to bring the authentic taste of traditional Indian kitchens to modern homes, without compromises.</p><p>What began as a small kitchen experiment has grown into a brand bringing the taste of grandmother’s cooking to homes across India. Pickles, spice powders, chapatis, parotas and more: familiar food for the way we live today.</p></div></div></section><div class="story-village"><img src="/assets/village-street.svg" alt="An illustrated South Indian neighbourhood with tiled homes and a banyan tree"></div>'''
ritual='''<section class="story-rituals"><div class="container"><div class="center-heading"><span class="eyebrow">The feeling we carry forward</span><h2>More than a recipe.</h2></div><div class="story-ritual-grid"><article><span class="art-wash"><img src="/assets/love.svg" alt=""></span><h3>The extra serving.</h3><p>Love has a way of asking, “A little more?”</p></article><article><span class="art-wash"><img src="/assets/tiffin.svg" alt=""></span><h3>The box for home.</h3><p>Because nobody leaves Ammamma’s empty-handed.</p></article><article><span class="art-wash"><img src="/assets/mortar.svg" alt=""></span><h3>The familiar flavour.</h3><p>A little reminder of the kitchen you grew up around.</p></article></div></div></section>'''
groups=[('Founders & Core Team','The people who started it all.',cards[:4]),('The Next Generation','Taking the story forward.',cards[4:9]),('Industry Experts','Experience at the table.',cards[9:10]),('Mentors & Advisors','A little guidance goes a long way.',cards[10:])]
team='<div id="people-behind-the-kitchen" class="container story-team">'+''.join('<section class="story-team-group"><div class="story-team-heading"><span class="eyebrow">Our people</span><h2>'+name+'</h2><p>'+desc+'</p></div><div class="story-people-grid">'+''.join(items)+'</div></section>' for name,desc,items in groups)+'</div>'
end='''<section class="story-invitation"><div class="container"><span class="eyebrow">There is always room at our table</span><h2>A little home,<br>wherever you are.</h2><a class="button" href="/products">Come into our kitchen</a></div></section>'''
numbers='<div class="container story-numbers"><div><strong>10 lac+</strong><span>Happy Customers</span></div><div><strong>50+</strong><span>Products</span></div><div><strong>40+</strong><span>Cities Served</span></div><div><strong>4.8&#9733;</strong><span>Average Rating</span></div></div>'
html='<div class="our-story-page">'+hero+origin+ritual+team+numbers+end+'</div>'
D['storyPage']=html
(R/'preview/reference-data.json').write_text(json.dumps(D,ensure_ascii=False),encoding='utf-8')
(R/'preview/our-story.html').write_text(html,encoding='utf-8')
native=re.sub(r'/assets/([^" ]+)',lambda m:"{{ '"+m[1]+"' | asset_url }}",html).replace('href="/products"','href="/collections/all"')
(T/'sections/page-about.liquid').write_text(native+'\n{% schema %}\n'+json.dumps({'name':'Our story','settings':[]})+'\n{% endschema %}',encoding='utf-8')
print('Our Story refreshed; '+str(len(cards))+' original team portraits and profiles preserved.')
