"""Apply approved pack sizes and studio images without changing prices or stock."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1]
STUDIO=json.loads((R/'brand-assets/studio-products.json').read_text(encoding='utf-8'))
def apply_studio_catalog(products,pages):
    for p in products:
        shot=STUDIO['products'].get(p['handle'])
        if not shot or not (R/'theme/assets'/shot['asset']).is_file():continue
        p.setdefault('captured_images',list(p['images']))
        p['studio_title']=shot['title'];p['studio_pack']=shot['pack'];p['studio_scale']=shot['scale']
        p['title']=shot['title']+(' '+shot['pack'] if shot['pack'] else '')
        p['images']=list(dict.fromkeys(['/assets/'+shot['asset'],*p['captured_images']]))
        if 'options' in shot:p['options']=shot['options']
        if p['handle'] in ['mango-pickle-300g','lemon-pickle-300g']:
            p['description']=re.sub(r'300\s*g\b','250 g',p['description'],flags=re.I)
        if p['handle']=='cow-ghee':p['description']=re.sub(r'200\s*ml\b','250 ml',p['description'],flags=re.I)
        for page in pages:
            if page['path']==p['url']:page['title']=p['title']+" | Ammamma’s"
def liquid_studio_cases():
    parts=["{% assign studio_asset = '' %}{% assign studio_title = product.title %}{% assign studio_pack = '' %}{% assign studio_scale = 1 %}{% case product.handle %}"]
    for handle,shot in STUDIO['products'].items():
        if not (R/'theme/assets'/shot['asset']).is_file():continue
        parts.append("{% when '"+handle+"' %}{% assign studio_asset = '"+shot['asset']+"' %}{% assign studio_title = '"+shot['title']+"' %}{% assign studio_pack = '"+shot['pack']+"' %}{% assign studio_scale = "+str(shot['scale'])+" %}")
    parts.append('{% endcase %}')
    return ''.join(parts)
