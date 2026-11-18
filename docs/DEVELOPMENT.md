# Development status

The site is being rebuilt using supplied rendered pages without access to Shopify. An original theme export is not a blocker for design work.

The first local version includes 97 captured routes and 73 products. All product photography is reused from captured assets. Presentation typography, colours and extracted SVG identity are used throughout. Main page text is retained in the extraction data; redesigned views reuse that captured content, with supplementary source sections preserved. No backend credentials or legacy application scripts are used.

Native theme files exist for home, products, collections, pages, recipes, search, wishlist, cart and contact. Captured homepage cards and bundles remain reference snapshots until live collection and bundle configuration is supplied. The local review and Liquid rendering are separate renderers sharing the theme assets; exact parity must be checked in Shopify later.

Validation: JavaScript syntax, JSON templates, section schema JSON and asset-reference checks pass. Browser review now covers 1440px desktop and 390px mobile catalog/product views, working manual carousel controls, loaded images, horizontal overflow checks and a wishlist toggle restored to its prior state. Shopify validation remains pending. The local preview runs on 127.0.0.1:4180.

Outstanding: Shopify Theme Check, live responsive review, merchant content mapping, variant pricing/stock, shipping/markets, accounts, reviews, bundle pricing, newsletter integration and private remote backup.
