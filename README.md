# Ammamma’s Shopify theme project

Open `ammammas.code-workspace` in VS Code. One working project, with Git checkpoints instead of duplicate version folders.

## Local review
Run `python scripts/preview_server.py` from this folder, or double-click `Start-Preview.cmd`. Open http://127.0.0.1:4180. You can also run the VS Code task **Preview website**.

The local review uses 97 captured pages and a 73-product snapshot, with existing product photographs and content. It shares the presentation brand assets and stylesheet with the Shopify theme. Search, categories, product galleries, wishlist and the review bag run locally. This is an offline design review, not a live Shopify storefront. Prices, inventory and review data are captured snapshots. Checkout, account services, forms and bundle purchases require integration.

## Current design
Malgudi-inspired South Indian imagery, original village and kolam-style SVGs, a three-slide landing carousel with flowing motion, arched pantry product cards and responsive sections. See `docs/DESIGN.md`.

## Project structure
- `theme/`: native Shopify Liquid, JSON templates, sections, snippets and theme assets.
- `preview/`: local review runtime and generated reference content.
- `brand-assets/`: presentation-derived originals, including the extracted SVG logo.
- `website-reference/`: preserved supplied crawl; excluded from Git.
- `scripts/`: repeatable content extraction, theme construction and local server.
- `docs/`: catalog snapshot, route mapping, source audit and development notes.

## Rebuild
Run `python scripts/build_preview.py`, then `python scripts/build_theme.py`. The generators overwrite generated theme templates and captured sections; make shared design changes in `theme/assets/theme.css`, preview interaction changes in `preview/preview.js`, and template changes in `scripts/build_theme.py` until the migration is complete.

## Brand rules
Use our launch presentation only for the logo, fonts, colours and visual treatment. The old website is a source for content, imagery, links and UX only. Its visual CSS is not used: extracted structural utility CSS contains layout declarations only.

## Shopify connection later
No store access is needed for this review. When access arrives, verify product and collection handles, import/match content, assign information-page templates, add recipes to the recipes blog, connect bundles/reviews/subscriptions, configure menus and review a development theme. Shopify route differences are recorded in `docs/route-map.json`. The theme has not been Shopify-validated or published.

## Version control
The repository is local; no remote is connected. Initial automated checkpoints use Codex as the author, never an inferred user identity. Small fixes belong in the next meaningful checkpoint. Establish the user's commit identity and private remote when available.
