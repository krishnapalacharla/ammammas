"""Malgudi-inspired presentation layer shared by the offline review and Shopify."""
from pathlib import Path
from html import escape as e
import json,re,sys
sys.path.insert(0,str(Path(__file__).parent))
from reference_dom import Parser,Node
R=Path(__file__).resolve().parents[1];T=R/'theme';D=json.loads((R/'preview/reference-data.json').read_text(encoding='utf-8'))
home=Parser(next(p['content'] for p in D['pages'] if p['path']=='/')).root
sections={int(n.attrs['data-home-section']):n for n in home.all('section') if 'data-home-section' in n.attrs}
products={p['handle']:p for p in D['products']}
def first(n,t):return next(n.all(t),None)
def clean(n):
    if isinstance(n,str):return e(n)
    if n.tag in ['svg','script','style']:return ''
    attrs={k:v for k,v in n.attrs.items() if k in ['href','src','alt','type','name','placeholder','required']}
    if n.tag=='button':attrs['type']='button'
    at=''.join(' '+k+('="'+e(v or '',quote=True)+'"') for k,v in attrs.items())
    text=''.join(clean(c) for c in n.children)
    if not text.strip() and n.tag not in ['img','input','br','hr']:return ''
    return '<'+n.tag+at+'>'+text+('' if n.tag in ['img','input','br','hr'] else '</'+n.tag+'>')
def card(p):
    return f'''<article class="product-card pantry-card" data-reveal><div class="pantry-picture"><a class="product-photo" href="{p['url']}"><img src="{p['images'][0]}" alt="{e(p['title'],quote=True)}" loading="lazy"></a><button class="save-product" data-save="{p['handle']}" aria-label="Save {e(p['title'],quote=True)}" aria-pressed="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M20 5c-3-3-6-1-8 1-2-2-5-4-8-1-5 5 2 11 8 15 6-4 13-10 8-15Z"/></svg></button></div><div class="pantry-label"><span class="pantry-category">{e(p['category'].replace('-',' '))}</span><h3><a href="{p['url']}">{e(p['title'])}</a></h3><div class="pantry-card-bottom"><span class="pantry-price">₹{float(p['price']):,.0f}</span><a class="pantry-shop" href="{p['url']}">{'Choose options' if p['available'] else 'View product'}</a></div></div></article>'''
def native_card(p):
    return "{% assign captured_product = all_products['"+p['handle']+"'] %}{% if captured_product != blank %}{% render 'product-card', product: captured_product %}{% else %}"+card(p)+"{% endif %}"
def native(html):
    html=re.sub(r'/assets/([^" ]+)',lambda m:"{{ '"+m[1]+"' | asset_url }}",html)
    html=html.replace('href="/category/','href="/collections/').replace('href="/products"','href="/collections/all"').replace('href="/about"','href="/pages/about"').replace('href="/privacy-policy"','href="/pages/privacy-policy"')
    return html
def section(name,html,settings=None):return native(html)+'\n{% schema %}\n'+json.dumps({'name':name,'settings':settings or []})+'\n{% endschema %}'
out=[];template={'sections':{},'order':[]}
def add(handle,title,html,shopify=None,settings=None):
    out.append(html);(T/'sections'/(handle+'.liquid')).write_text(section(title,shopify or html,settings),encoding='utf-8');template['sections'][handle]={'type':handle};template['order'].append(handle)
imgs=[n.attrs['src'] for n in sections[0].all('img')]
slides=[('Homemade Goodness Delivered','Homemade\nGoodness\nDelivered.', '',imgs[0],'/products','Shop Now'),('New Arrivals This Week','Authentic\nAndhra\nPickles.','Hand-pounded spices, Premium quality oils, and recipes passed down through generations. No preservatives, just pure taste.',imgs[1],'/category/pickles','Shop Pickles'),('Healthy & Wholesome','Healthy &\nWholesome.','',imgs[2],'/category/ready-to-cook','Order Now')]
slide_html=[]
for i,(eyebrow,title,desc,img,url,cta) in enumerate(slides):
    slide_html.append(f'''<article class="heritage-slide {'is-active' if i==0 else ''}" data-slide="{i}" aria-roledescription="slide" aria-label="{i+1} of 3" aria-hidden="{'false' if i==0 else 'true'}"><div class="heritage-hero-copy"><span class="eyebrow">{e(eyebrow)}</span><h1>{e(title).replace(chr(10),'<br>')}</h1>{'<p>'+e(desc)+'</p>' if desc else ''}<div class="hero-actions"><a class="button" href="{url}">{cta}</a><a class="text-link" href="{'/recipes' if i==2 else '/products'}">{'See Recipes' if i==2 else 'View All Products'}</a></div></div><div class="heritage-hero-picture"><div class="liquid-picture"><img src="{img}" alt="{e(eyebrow)}" {'fetchpriority="high"' if i==0 else 'loading="lazy"'}></div></div></article>''')
hero='''<section class="heritage-slider" data-heritage-slider aria-roledescription="carousel" aria-label="From Ammamma’s kitchen"><img class="hero-kolam" src="/assets/kolam.svg" alt="">'''+''.join(slide_html)+'''<div class="slider-toolbar"><div class="slider-dots" role="group" aria-label="Choose a slide">'''+''.join(f'<button data-slide-to="{i}" aria-label="Show slide {i+1}" aria-pressed="{str(i==0).lower()}"><span></span></button>' for i in range(3))+'''</div><div class="slider-controls"><button data-slide-prev aria-label="Previous slide">‹</button><button data-slide-pause aria-label="Pause slideshow" aria-pressed="false">Ⅱ</button><button data-slide-next aria-label="Next slide">›</button></div></div><svg class="liquid-wave" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 35Q180 0 360 35T720 35T1080 35T1440 35V70H0Z"><animate attributeName="d" dur="12s" repeatCount="indefinite" values="M0 35Q180 0 360 35T720 35T1080 35T1440 35V70H0Z;M0 35Q180 65 360 35T720 35T1080 35T1440 35V70H0Z;M0 35Q180 0 360 35T720 35T1080 35T1440 35V70H0Z"/></path></svg></section><div class="heritage-proof"><span><strong>12</strong> States Available</span><img src="/assets/kolam.svg" alt=""><span><strong>40+</strong> Cities Served</span><img src="/assets/kolam.svg" alt=""><span><strong>10 lac+</strong> Happy Customers</span></div>'''
add('heritage-slider','Landing slideshow',hero)
cats=[('pickles','Pickles'),('spices','Spice Powders'),('ready-to-cook','Ready to Cook'),('ghee','Ghee'),('snacks','Snacks'),('fryum-factory','Fryum Factory'),('retro','Retro')]
tiles=[]
for h,title in cats:
    p=next((p for p in D['products'] if p['category']==h),None)
    if p:tiles.append(f'<a class="market-category" href="/category/{h}" data-reveal><span><img src="{p["images"][0]}" alt="{title}" loading="lazy"></span><strong>{title}</strong></a>')
add('heritage-categories','Kitchen categories','<section class="market-categories container"><div class="heritage-caption"><span></span><p>Explore Categories</p><span></span></div><div class="market-category-row">'+''.join(tiles)+'</div><div class="kitchen-sketches" aria-hidden="true"><span class="art-wash"><img src="/assets/spice-sprig.svg" alt=""></span><span>A little tradition in every kitchen.</span><span class="art-wash"><img src="/assets/coconut.svg" alt=""></span></div></section>')
for i,eyebrow,title in [(1,'Customer Favorites','Bestselling Products'),(2,'Fresh Additions','New Arrivals')]:
    handles=list(dict.fromkeys(n.attrs.get('data-product-handle') for n in sections[i].all('a') if n.attrs.get('data-product-handle') in products))
    selected=[products[h] for h in handles]
    head=f'<section class="pantry-section container"><div class="section-heading" data-reveal><div><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div><span class="art-wash heading-art" aria-hidden="true"><img src="/assets/mortar.svg" alt=""></span><a class="text-link" href="/products">View All Products</a></div><div class="product-grid pantry-grid">'
    add('heritage-featured' if i==1 else 'heritage-arrivals',title,head.replace('mortar.svg','tiffin.svg' if i==2 else 'mortar.svg')+''.join(card(p) for p in selected)+'</div></section>',head.replace('mortar.svg','tiffin.svg' if i==2 else 'mortar.svg')+''.join(native_card(p) for p in selected)+'</div></section>')
bundle_grid=next(n for n in sections[3].all('div') if 'grid-cols-1' in n.attrs.get('class',''))
bundles=''.join('<article class="market-bundle" data-reveal>'+clean(n)+'</article>' for n in bundle_grid.children if isinstance(n,Node))
add('heritage-bundles','Value packs','<section class="bundle-section"><div class="container"><div class="section-heading"><div><span class="eyebrow">Bundle & Save</span><h2>Value Packs</h2><p>Get more for less with our curated bundles. Hand-picked combos at special prices.</p></div></div><div class="market-bundles">'+bundles+'</div></div></section>')
story='<section class="village-story"><div class="container story-grid"><div class="story-portrait art-wash" data-reveal><img src="/assets/ammammas-granny.svg" alt="Ammamma’s"></div><div class="story-copy" data-reveal><span class="eyebrow">Our Story</span><h2>Made with Love<br>by Ammamma</h2><p>What started as a small kitchen experiment in 2019 has grown into a beloved brand that brings the taste of grandmother\'s cooking to homes across India.</p><a class="text-link" href="/about">Our Story</a><div class="story-facts"><span><strong>10 lac+</strong>Happy Families</span><span><strong>100%</strong>Homemade with Love</span><span><strong>Zero</strong>MAIDA</span><span><strong>4.8★</strong>Average Rating</span></div></div></div><img class="village-panorama" src="/assets/village-street.svg" alt="Illustrated South Indian street with tiled houses and a banyan tree"></section>'
add('heritage-story','Our story',story)
promises=[]
for n in sections[5].all('div'):
    if any(isinstance(c,Node) and c.tag=='h3' for c in n.children):promises.append('<article data-reveal><span class="art-wash promise-art"><img src="/assets/'+['ingredients','love','minutes','quality'][len(promises)%4]+'.svg" alt=""></span>'+clean(n)+'</article>')
add('heritage-promise','Our promise','<section class="promise-section container"><div class="center-heading"><span class="eyebrow">The Ammamma’s Promise</span><h2>Why Choose Us?</h2></div><div class="promise-grid">'+''.join(promises)+'</div></section>')
quotes=[]
for n in sections[6].all('div'):
    if any(isinstance(c,Node) and c.tag=='p' and '"' in c.text() for c in n.children):quotes.append('<blockquote data-reveal>'+clean(n)+'</blockquote>')
add('heritage-testimonials','Customer love','<section class="love-section"><div class="container"><div class="center-heading"><span class="eyebrow">Customer Love</span><h2>What Our Customers <span class="keep-together">Say About Us</span></h2></div><div class="quote-grid">'+''.join(quotes)+'</div></div></section>')
offer=[]
for n in sections[7].all():
    if any(isinstance(c,Node) and c.tag=='h3' for c in n.children):offer.append('<article data-reveal>'+clean(n)+'</article>')
description=first(sections[7],'p').text()
add('heritage-offerings','Crafted with tradition','<section class="offering-section container"><div class="center-heading"><span class="eyebrow">What We Offer</span><h2>Crafted With Tradition</h2><p>'+e(description)+'</p></div><div class="offering-grid">'+''.join(offer)+'</div></section>')
newsletter='''<section class="heritage-newsletter"><div class="container"><span class="art-wash"><img src="/assets/spice-sprig.svg" alt=""></span><div><p class="newsletter-quote">“One recipe a week, from my kitchen to yours.”</p><h2>Stay Updated</h2><p>Get recipes, offers & new product alerts straight to your inbox</p><form class="newsletter-form"><label class="sr-only" for="NewsletterEmail">Email address</label><input id="NewsletterEmail" name="contact[email]" type="email" placeholder="Your email address" required><button class="button" type="submit">Subscribe</button></form><small>No spam, unsubscribe anytime. By subscribing you agree to our <a href="/privacy-policy">Privacy Policy</a>.</small></div><span class="art-wash"><img src="/assets/tiffin.svg" alt=""></span></div></section>'''
native_news=newsletter.replace('<form class="newsletter-form">',"{% form 'customer', class: 'newsletter-form' %}<input type=\"hidden\" name=\"contact[tags]\" value=\"newsletter\">").replace('</form>','{{ form.errors | default_errors }}{% if form.posted_successfully? %}<p>Thank you for subscribing.</p>{% endif %}{% endform %}')
add('heritage-newsletter','Newsletter',newsletter,native_news)
(R/'preview/heritage-home.html').write_text(''.join(out),encoding='utf-8')
D['heritageHome']=''.join(out)
(R/'preview/reference-data.json').write_text(json.dumps(D,ensure_ascii=False),encoding='utf-8')
(T/'templates/index.json').write_text(json.dumps(template,indent=2),encoding='utf-8')
# Reuse the same card design for live Shopify collections.
(T/'snippets/product-card.liquid').write_text('''<article class="product-card pantry-card" data-reveal><div class="pantry-picture"><a class="product-photo" href="{{ product.url }}">{% if product.featured_image %}{{ product.featured_image | image_url: width: 800 | image_tag: loading: 'lazy', widths: '300, 500, 800' }}{% else %}{{ 'product-1' | placeholder_svg_tag }}{% endif %}</a><button class="save-product" data-save="{{ product.handle }}" aria-label="Save {{ product.title | escape }}" aria-pressed="false">{% render 'icon', name: 'heart' %}</button></div><div class="pantry-label"><span class="pantry-category">{{ product.type | escape }}</span><h3><a href="{{ product.url }}">{{ product.title | escape }}</a></h3><div class="pantry-card-bottom"><span class="pantry-price">{{ product.price | money }}</span><a class="pantry-shop" href="{{ product.url }}">{% if product.available %}Choose options{% else %}View product{% endif %}</a></div></div></article>''',encoding='utf-8')
# Include the same standalone motion system in Shopify and local review.
layout=T/'layout/theme.liquid';s=layout.read_text(encoding='utf-8')
if 'heritage.css' not in s:s=s.replace("{{ 'theme.css' | asset_url | stylesheet_tag }}","{{ 'theme.css' | asset_url | stylesheet_tag }}{{ 'heritage.css' | asset_url | stylesheet_tag }}")
if 'home-refinements.css' not in s:s=s.replace("{{ 'heritage.css' | asset_url | stylesheet_tag }}","{{ 'heritage.css' | asset_url | stylesheet_tag }}{{ 'home-refinements.css' | asset_url | stylesheet_tag }}")
if 'heritage.js' not in s:s=s.replace('<script src=',"<script src=\"{{ 'heritage.js' | asset_url }}\" defer></script><script src=",1)
layout.write_text(s,encoding='utf-8')
print('Heritage homepage: three-slide landing carousel and nine coherent content sections generated.')
