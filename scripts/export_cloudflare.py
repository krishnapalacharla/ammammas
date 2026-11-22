"""Export the reviewed storefront as a static Cloudflare Pages design preview."""
from pathlib import Path
import shutil,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
OUT.mkdir(exist_ok=True)
for name in ['index.html','preview.js','reference-data.json']:
    source=ROOT/'preview'/name
    if not source.is_file():raise SystemExit('Missing reviewed preview file: '+name)
    shutil.copy2(source,OUT/name)
shutil.copytree(ROOT/'theme/assets',OUT/'assets',dirs_exist_ok=True)
(OUT/'_redirects').write_text('/* /index.html 200\n',encoding='utf-8')
(OUT/'_headers').write_text('/reference-data.json\n  Cache-Control: no-cache\n/index.html\n  Cache-Control: no-cache\n/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n',encoding='utf-8')
data=json.loads((OUT/'reference-data.json').read_text(encoding='utf-8'))
files=list(OUT.rglob('*'))
large=[str(p.relative_to(OUT)) for p in files if p.is_file() and p.stat().st_size>=25*1024*1024]
if large:raise SystemExit('Cloudflare Pages file-size limit: '+str(large))
print(f'Cloudflare Pages ready: {len(data["pages"])} routes, {len(data["products"])} products; publish directory: dist')
