"""Extract captured content without executing the previous application's scripts."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import re, json, shutil, hashlib, posixpath

ROOT = Path(__file__).resolve().parents[1]
REF, THEME, OUT = ROOT/'website-reference', ROOT/'theme', ROOT/'preview'
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class Node:
    def __init__(self, tag='', attrs=None): self.tag=tag; self.attrs=dict(attrs or []); self.children=[]
    def all(self, tag=None):
        for c in self.children:
            if isinstance(c, Node):
                if tag is None or c.tag==tag: yield c
                yield from c.all(tag)
    def text(self): return ' '.join(c.text() if isinstance(c,Node) else c for c in self.children).strip()
class Parser(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True); self.root=Node('document'); self.stack=[self.root]; self.feed(s)
    def handle_starttag(self,t,a):
        n=Node(t,a); self.stack[-1].children.append(n)
        if t not in VOID: self.stack.append(n)
    def handle_startendtag(self,t,a): self.handle_starttag(t,a); self.handle_endtag(t)
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==t: self.stack=self.stack[:i]; break
    def handle_data(self,d): self.stack[-1].children.append(d)
def first(n,t): return next(n.all(t),None)
assets, missing = {}, set()
def asset(url,page):
    if not url or url.startswith('data:'): return url
    if url.startswith(('https:','http:','//')): return url
    resolved=(page.parent/url.split('?')[0].split('#')[0]).resolve()
    if not resolved.is_relative_to(REF.resolve()) or not resolved.is_file(): missing.add(url); return ''
    if resolved not in assets:
        name='ref-'+hashlib.sha1(str(resolved.relative_to(REF)).encode()).hexdigest()[:12]+resolved.suffix.lower()
        shutil.copy2(resolved,THEME/'assets'/name); assets[resolved]=name
    return '/assets/'+assets[resolved]
def route(url,page,native=False):
    if not url or url.startswith(('#','mailto:','tel:','https:','http:','//')): return url
    p=posixpath.normpath(posixpath.join('/'+page.relative_to(REF).parent.as_posix(),url)).removesuffix('.html')
    p='/' if p=='/index' else p
    if p.startswith('/_www.'): return 'https://'+p[2:]
    if p.startswith('/www.linkedin.com/'): return 'https:/'+p
    if p in ['/recipes/classic-dosa-with-coconut-chutney','/recipes/mango-pickle-rice']: return 'https://www.ammammas.in'+p
    if native:
        if p.startswith('/category/'): p=p.replace('/category/','/collections/',1)
        elif p=='/products': p='/collections/all'
        elif p.startswith('/recipes/'): p=p.replace('/recipes/','/blogs/recipes/',1)
        elif p=='/recipes': p='/blogs/recipes'
        elif p!='/' and not p.startswith(('/products/','/cart','/account','/search')): p='/pages'+p
    return p
def serial(n,page,native=False):
    if isinstance(n,str): return escape(n)
    if n.tag in ['script','noscript','style']: return ''
    a={k:v for k,v in n.attrs.items() if not k.startswith('on') and k not in ['style','srcset','sizes','fetchpriority','tabindex','data-state']}
    if n.tag=='img':
        src=a.get('src','')
        if any(x in src for x in ['logo-','ammamma-heart','ammamma-namaste']): a['src']='/assets/ammammas-logo.svg'; a['alt']="Ammamma's"
        else: a['src']=asset(src,page)
        if not a.get('src'): return '<div class="captured-media-missing" role="img" aria-label="'+escape(a.get('alt','Image unavailable in supplied reference'),quote=True)+'"></div>'
        a['loading']='lazy'; a.pop('width',None); a.pop('height',None)
    if 'href' in a: a['href']=route(a['href'],page,native)
    attrs=''.join(' '+k+(('="'+escape(v,quote=True)+'"') if v is not None else '') for k,v in a.items())
    if native: attrs=re.sub(r'/assets/([^" ]+)',lambda m:"{{ '"+m[1]+"' | asset_url }}",attrs)
    return '<'+n.tag+attrs+'>'+''.join(serial(c,page,native) for c in n.children)+('' if n.tag in VOID else '</'+n.tag+'>')
def schema(name): return '\n{% schema %}\n'+json.dumps({'name':name[:25],'settings':[]})+'\n{% endschema %}'
for d in ['assets','sections','snippets','templates','config','layout','locales']: (THEME/d).mkdir(parents=True,exist_ok=True)
OUT.mkdir(exist_ok=True)
for p in (ROOT/'brand-assets/fonts').iterdir():
    if p.suffix.lower() in ['.otf','.ttf']: shutil.copy2(p,THEME/'assets'/p.name.replace(' ','-'))
shutil.copy2(ROOT/'brand-assets/logos/ammammas-logo.svg',THEME/'assets/ammammas-logo.svg')
# Structural utilities only. Every captured colour, font and decorative style is discarded.
css=(REF/'assets/index-BRt1Qw5u.css').read_text()
allowed={'display','grid-template-columns','grid-column','grid-row','gap','column-gap','row-gap','flex','flex-direction','flex-wrap','align-items','justify-content','position','inset','top','bottom','left','right','width','height','min-width','max-width','min-height','max-height','margin','margin-top','margin-bottom','margin-left','margin-right','padding','padding-top','padding-bottom','padding-left','padding-right','overflow','overflow-x','overflow-y','object-fit','aspect-ratio','text-align','white-space','vertical-align'}
def structural(m):
    decl=';'.join(d for d in m[2].split(';') if d.split(':',1)[0].strip() in allowed)
    return m[1]+'{'+decl+'}' if decl else ''
(THEME/'assets/reference-structure.css').write_text(re.sub(r'([^{}]+)\{([^{}]*)\}',structural,css),encoding='utf-8')
products,pages=[],[]
for p in sorted(REF.rglob('*.html')):
    dom=Parser(p.read_text(encoding='utf-8')).root; main=first(dom,'main')
    if not main:
        wrapper=next((n for n in dom.all('div') if 'min-h-screen' in n.attrs.get('class','') and any(c.tag=='header' for c in n.children if isinstance(c,Node))),None)
        if wrapper:
            main=Node('main');main.children=[c for c in wrapper.children if isinstance(c,Node) and c.tag not in ['header','footer']]
    if not main: continue
    path='/' if p.name=='index.html' else '/'+p.relative_to(REF).as_posix().removesuffix('.html')
    title=first(dom,'title').text() if first(dom,'title') else 'Ammamma’s'
    for a in main.all('a'):
        href=a.attrs.get('href','')
        if 'products/' in href: a.attrs['data-product-handle']=href.rsplit('/',1)[-1].removesuffix('.html')
    if p.parent.name=='products':
        structured=[]
        for script in dom.all('script'):
            if script.attrs.get('type')=='application/ld+json':
                try:
                    data=json.loads(script.text()); structured.extend(data if isinstance(data,list) else [data])
                except ValueError: pass
        prod=next((x for x in structured if x.get('@type')=='Product'),{})
        source_imgs=list(main.all('img'))
        imgs=list(dict.fromkeys(asset(x.attrs.get('src',''),p) for x in source_imgs if 'image' in x.attrs.get('alt','').lower() and 'buy online' not in x.attrs.get('alt','').lower()))
        if not imgs and source_imgs: imgs=[asset(source_imgs[0].attrs.get('src',''),p)]
        offers=prod.get('offers',{}); offers=offers[0] if isinstance(offers,list) and offers else offers
        name=prod.get('name') or (first(main,'h1').text() if first(main,'h1') else p.stem)
        options=[b.text() for b in main.all('button') if re.fullmatch(r'\d+(?:\.\d+)?\s*(?:g|kg|Kg|ml|L|pcs|pack.*)',b.text(),re.I)]
        cats=[a.text() for a in main.all('a') if '/category/' in a.attrs.get('href','')]
        products.append({'handle':p.stem,'title':name,'description':prod.get('description',''),'price':offers.get('price',0),'available':'OutOfStock' not in offers.get('availability',''),'images':[x for x in imgs if x],'options':list(dict.fromkeys(options)),'category':cats[0] if cats else '', 'url':path})
    if path=='/':
        sections=[x for x in main.children if isinstance(x,Node) and x.tag=='section']
        for i,section in enumerate(sections):
            section.attrs['data-home-section']=str(i)
            if i==0: section.attrs['class']='heritage-hero'
            (THEME/'sections'/f'home-{i:02}.liquid').write_text(serial(section,p,True)+schema('Home '+str(i+1)),encoding='utf-8')
        (THEME/'templates/index.json').write_text(json.dumps({'sections':{f's{i}':{'type':f'home-{i:02}'} for i in range(len(sections))},'order':[f's{i}' for i in range(len(sections))]},indent=2))
    content=serial(main,p)
    if p.parent.name not in ['products','category','recipes'] and path not in ['/','/products','/wishlist','/recipes']:
        handle=p.stem
        (THEME/'snippets'/f'reference-{handle}.liquid').write_text(serial(main,p,True),encoding='utf-8')
        (THEME/'sections'/f'page-{handle}.liquid').write_text("{% render 'reference-"+handle+"' %}"+schema(handle.replace('-',' ').title()),encoding='utf-8')
        (THEME/'templates'/f'page.{handle}.json').write_text(json.dumps({'sections':{'main':{'type':'page-'+handle}},'order':['main']},indent=2))
    pages.append({'path':path,'title':title,'source':str(p.relative_to(REF)),'content':content})
for page in pages:
    if page['path'].startswith('/category/'):
        category=page['path'].split('/')[-1]
        for handle in re.findall(r'data-product-handle="([^"]+)"',page['content']):
            for product in products:
                if product['handle']==handle: product['category']=category
captured_cards={}
for page in pages:
    dom=Parser(page['content']).root
    for card in dom.all('a'):
        handle=card.attrs.get('data-product-handle')
        if handle and first(card,'h3') and handle not in captured_cards: captured_cards[handle]=card
for product in products:
    card=captured_cards.get(product['handle'])
    if card:
        if product['title']==product['handle']: product['title']=first(card,'h3').text()
        if not product['images'] and first(card,'img'): product['images']=[first(card,'img').attrs['src']]
        if not float(product['price'] or 0):
            price=re.search(r'₹\s*([\d,]+)',card.text())
            if price: product['price']=price[1].replace(',','');product['available']='Out of Stock' not in card.text()
        if not product['category']:
            for label,handle in [('Fryum Factory','fryum-factory'),('Retro','retro'),('Pickles','pickles'),('Spices','spices'),('snacks','snacks'),('ghee','ghee')]:
                if any(n.text().lower()==label.lower() for n in card.all()): product['category']=handle;break
    if not product['images']:
        for page in pages:
            dom=Parser(page['content']).root
            for image in dom.all('img'):
                if image.attrs.get('alt','').lower().startswith(product['title'].lower()) and image.attrs.get('src'):
                    product['images']=[image.attrs['src']];break
            if product['images']:break
    if not product['category']:
        source=next(p['content'] for p in pages if p['path']==product['url'])
        if 'fryum factory' in source.lower(): product['category']='fryum-factory'
        elif 'retro' in source.lower(): product['category']='retro'
        elif 'snacks' in source.lower(): product['category']='snacks'
    if not product['images']:
        # The supplied crawl has no photo; preserve a visible placeholder, not another product's photo.
        product['images']=['/assets/missing-product.svg']
(OUT/'reference-data.json').write_text(json.dumps({'pages':pages,'products':products},ensure_ascii=False),encoding='utf-8')
(ROOT/'docs/catalog-snapshot.json').write_text(json.dumps(products,ensure_ascii=False,indent=2),encoding='utf-8')
base='''<!doctype html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ammamma’s</title><link rel="stylesheet" href="/assets/reference-structure.css"><link rel="stylesheet" href="/assets/theme.css"><link rel="stylesheet" href="/assets/heritage.css"><link rel="stylesheet" href="/assets/home-refinements.css"><script defer src="/assets/heritage.js"></script><script defer src="/preview.js"></script></head><body data-preview="true"><a class="skip-link" href="#MainContent">Skip to content</a><div id="site-header"></div><div id="MainContent"></div><div id="site-footer"></div><dialog id="cart-dialog" aria-label="Shopping bag"><button class="close-cart" aria-label="Close bag">×</button><h2>Your bag</h2><div id="cart-items"></div><p class="preview-note">Local design preview. Checkout will be available after Shopify connection.</p></dialog><div id="status" role="status" aria-live="polite"></div></body></html>'''
(OUT/'index.html').write_text(base,encoding='utf-8')
(ROOT/'docs/reference-audit.json').write_text(json.dumps({'pages':len(pages),'products':len(products),'copied_reference_assets':len(assets),'missing_reference_paths':sorted(missing),'source':str(REF),'note':'All captured main content retained. Old tracking and application scripts are not executed.'},indent=2))
print(json.dumps({'pages':len(pages),'products':len(products),'assets':len(assets),'missing_paths':sorted(missing)}))
