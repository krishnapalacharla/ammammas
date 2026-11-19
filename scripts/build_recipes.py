"""Recipe index and captured recipe pages, with native Shopify counterparts."""
from pathlib import Path
from html import escape as e
import json,re,sys
sys.path.insert(0,str(Path(__file__).parent))
from reference_dom import Parser,Node
R=Path(__file__).resolve().parents[1];T=R/'theme';D=json.loads((R/'preview/reference-data.json').read_text(encoding='utf-8'))
pages={p['path']:p for p in D['pages']};root=Parser(pages['/recipes']['content']).root
recipes=[]
for a in root.all('a'):
    title=next(a.all('h3'),None)
    if title is None:continue
    img=next(a.all('img'),None);desc=next(a.all('p'),None)
    badges=[n.text() for n in a.all('div') if 'inline-flex' in n.attrs.get('class','')]
    meta=next((n.text() for n in a.all('div') if 'text-xs' in n.attrs.get('class','') and 'gap-4' in n.attrs.get('class','')),'')
    recipes.append({'url':a.attrs['href'],'title':title.text(),'image':img.attrs['src'] if img else None,'description':desc.text() if desc else '', 'category':badges[0], 'difficulty':badges[1], 'meta':meta})
def picture(r):
    return '<img src="'+r['image']+'" alt="'+e(r['title'],quote=True)+'" loading="lazy">' if r['image'] else '<span class="recipe-drawn-photo"><img src="/assets/buttermilk-glass.svg" alt="Illustration of a glass of spiced buttermilk" loading="lazy"></span>'
def recipe_meta(r):
    m=re.search(r'(\d+)\s*min\s*\+\s*(\d+)\s*min\s*(\d+)\s*servings',r['meta'])
    return ''.join('<span>'+e(label)+'</span>' for label in ['Prep '+m[1]+' min','Cook '+m[2]+' min',m[3]+' servings']) if m else e(r['meta'])
def card(r):
    return '<article class="recipe-card" data-recipe-tags="'+e(r['category'],quote=True)+'"><a class="recipe-card-photo" href="'+e(r['url'],quote=True)+'">'+picture(r)+'</a><div class="recipe-card-copy"><div class="recipe-card-tags"><span>'+e(r['category'])+'</span><span>'+e(r['difficulty'])+'</span></div><h2><a href="'+e(r['url'],quote=True)+'">'+e(r['title'])+'</a></h2><p>'+e(r['description'])+'</p><div class="recipe-card-meta">'+recipe_meta(r)+'</div><a class="text-link" href="'+e(r['url'],quote=True)+'">Let’s make it <span aria-hidden="true">↗</span></a></div></article>'
cats=list(dict.fromkeys(r['category'] for r in recipes))
buttons='<button type="button" data-recipe-filter="All" aria-pressed="true">All recipes</button>'+''.join('<button type="button" data-recipe-filter="'+e(c,quote=True)+'" aria-pressed="false">'+e(c)+'</button>' for c in cats)
hero='''<section class="container recipe-index-hero"><div><span class="eyebrow">From our kitchen</span><h1>A little stirring.<br>A lot of <em>joy.</em></h1><p>Quick breakfasts, comforting lunches and weekend favourites. Make a little room for something delicious.</p><a class="text-link" href="#recipe-shelf">Find your next favourite</a></div><span class="art-wash recipe-hero-art" aria-hidden="true"><img src="/assets/recipe-cooking.svg" alt=""></span></section>'''
index='<div class="recipe-index">'+hero+'<section class="container recipe-shelf" id="recipe-shelf"><div class="recipe-filter-row"><nav class="recipe-filters" aria-label="Filter recipes">'+buttons+'</nav><span class="recipe-count" role="status" aria-live="polite">6 recipes</span></div><div class="recipe-card-grid">'+''.join(card(r) for r in recipes)+'</div></section></div>'
rendered={}
for r in recipes:
    if r['url'] not in pages:continue
    source=Parser(pages[r['url']]['content']).root;article=next(source.all('article'))
    ingredients=next(article.all('ul'));steps=next(article.all('ol'));tips=list(article.all('ul'))[1:]
    title=next(article.all('h1')).text();desc=next(article.all('p')).text()
    facts=next((n for n in article.all('div') if 'gap-6' in n.attrs.get('class','')),None)
    facts_html=''.join('<span>'+e(n.text())+'</span>' for n in facts.children if isinstance(n,Node) and n.tag=='span') if facts else ''
    tags=next((n for n in article.all('div') if 'flex-wrap gap-2' in n.attrs.get('class','')),None)
    tag_html=''.join('<span>'+e(n.text())+'</span>' for n in tags.children if isinstance(n,Node)) if tags else ''
    checks=''.join('<li><label><input type="checkbox"><span>'+e(n.text())+'</span></label></li>' for n in ingredients.all('li'))
    method=''.join('<li><p>'+e(re.sub(r'^\d+\s*','',n.text()))+'</p></li>' for n in steps.all('li'))
    tips_html=''.join('<li>'+e(re.sub(r'^[•\s]+','',n.text()))+'</li>' for ul in tips for n in ul.all('li'))
    html='<article class="recipe-detail"><div class="container recipe-back"><a class="text-link" href="/recipes">← Back to recipes</a></div><header class="container recipe-detail-hero"><div class="recipe-detail-copy"><div class="recipe-card-tags">'+tag_html+'</div><h1>'+e(title)+'</h1><p>'+e(desc)+'</p><div class="recipe-facts">'+facts_html+'</div><div class="recipe-actions"><a class="button" href="#recipe-method">Let’s get cooking</a><button type="button" class="text-link" data-print-recipe>Print recipe</button></div></div><div class="recipe-detail-photo">'+picture(r)+'</div></header><div class="container recipe-cook-layout" id="recipe-method"><aside class="recipe-ingredients"><span class="eyebrow">A little preparation</span><h2>Ingredients</h2><p class="recipe-check-hint">Tick as you go.</p><ul>'+checks+'</ul></aside><section class="recipe-method"><span class="eyebrow">One step at a time</span><h2>Let’s make it.</h2><ol>'+method+'</ol><aside class="recipe-tips"><span class="art-wash" aria-hidden="true"><img src="/assets/spice-sprig.svg" alt=""></span><div><h3>A little kitchen wisdom</h3><ul>'+tips_html+'</ul></div></aside></section></div><section class="container recipe-related"><div class="section-heading"><h2>What shall we make next?</h2><a class="text-link" href="/recipes">All recipes</a></div><div class="recipe-card-grid">'+'</div></section></article>'
    # Three complete cards, rather than truncating generated markup.
    related=''.join(card(other) for other in [o for o in recipes if o['url']!=r['url']][:3])
    html=html.replace('<div class="recipe-card-grid"></div></section></article>','<div class="recipe-card-grid">'+related+'</div></section></article>')
    rendered[r['url']]=html
def native(html):
    return re.sub(r'/assets/([^" ]+)',lambda m:"{{ '"+m[1]+"' | asset_url }}",html).replace('href="/recipes/','href="/blogs/recipes/').replace('href="/recipes"','href="/blogs/recipes"')
def write_section(name,html):
    (T/'sections'/(name+'.liquid')).write_text(html+'\n{% schema %}\n'+json.dumps({'name':'Recipes' if name=='main-blog' else 'Recipe detail','settings':[]})+'\n{% endschema %}',encoding='utf-8')
D['recipeIndex']=index;D['recipePages']=rendered
(R/'preview/reference-data.json').write_text(json.dumps(D,ensure_ascii=False),encoding='utf-8')
(R/'preview/recipes.html').write_text(index,encoding='utf-8')
live='''<div class="recipe-index"><section class="container recipe-index-hero"><div><span class="eyebrow">From our kitchen</span><h1>{{ blog.title | escape }}</h1><p>Quick breakfasts, comforting lunches and weekend favourites.</p></div><span class="art-wash recipe-hero-art"><img src="{{ 'recipe-cooking.svg' | asset_url }}" alt=""></span></section><section class="container recipe-shelf"><div class="recipe-filter-row"><nav class="recipe-filters" aria-label="Filter recipes"><button type="button" data-recipe-filter="All" aria-pressed="true">All recipes</button>{% for tag in blog.all_tags %}<button type="button" data-recipe-filter="{{ tag | escape }}" aria-pressed="false">{{ tag | escape }}</button>{% endfor %}</nav><span class="recipe-count" role="status" aria-live="polite"></span></div>{% paginate blog.articles by 24 %}<div class="recipe-card-grid">{% for article in blog.articles %}<article class="recipe-card" data-recipe-tags="{{ article.tags | join: '|' | escape }}"><a class="recipe-card-photo" href="{{ article.url }}">{% if article.image %}{{ article.image | image_url: width: 1000 | image_tag: loading: 'lazy' }}{% else %}<span class="recipe-drawn-photo"><img src="{{ 'recipe-cooking.svg' | asset_url }}" alt=""></span>{% endif %}</a><div class="recipe-card-copy"><div class="recipe-card-tags"><span>{{ article.tags | first | escape }}</span></div><h2><a href="{{ article.url }}">{{ article.title | escape }}</a></h2><div>{{ article.excerpt }}</div><a class="text-link" href="{{ article.url }}">Let’s make it ↗</a></div></article>{% endfor %}</div>{{ paginate | default_pagination }}{% endpaginate %}</section></div>'''
write_section('main-blog',"{% if blog.articles_count > 0 %}"+live+"{% else %}"+native(index)+"{% endif %}")
for path,html in rendered.items():
    handle=path.rsplit('/',1)[-1];name='recipe-'+handle
    write_section(name,native(html))
    (T/'templates'/('article.'+handle+'.json')).write_text(json.dumps({'sections':{'main':{'type':name}},'order':['main']},indent=2),encoding='utf-8')
write_section('main-article','''<article class="recipe-detail recipe-live-article"><div class="container recipe-back"><a class="text-link" href="{{ blog.url }}">← All recipes</a></div><header class="container recipe-detail-hero"><div class="recipe-detail-copy"><span class="eyebrow">From our kitchen</span><h1>{{ article.title | escape }}</h1><div>{{ article.excerpt }}</div><div class="recipe-actions"><a class="button" href="#recipe-method">Let’s get cooking</a><button type="button" class="text-link" data-print-recipe>Print recipe</button></div></div><div class="recipe-detail-photo">{% if article.image %}{{ article.image | image_url: width: 1400 | image_tag: loading: 'eager' }}{% else %}<span class="recipe-drawn-photo"><img src="{{ 'recipe-cooking.svg' | asset_url }}" alt=""></span>{% endif %}</div></header><div id="recipe-method" class="container recipe-article-body">{{ article.content }}</div></article>''')
print('Recipe shelf, 4 captured details and native blog/article layouts generated; 2 external source links retained.')
