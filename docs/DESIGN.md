# Malgudi-inspired South Indian storefront

The visual direction uses original SVG neighbourhood drawings, tiled shopfronts, a banyan tree, banana leaves, pantry vessels and a kolam-inspired geometric motif. These SVGs were authored for this project; no third-party artwork was copied or downloaded. The illustrations use presentation brand colours.

The homepage has been rebuilt into clean sections rather than retaining captured layout utilities. Three original captured banners form a carousel with previous/next, direct selection, autoplay, pause, swipe and keyboard controls. Autoplay pauses on focus, hover and hidden tabs. Reduced-motion preferences disable decorative animation and autoplay by default.

Motion includes a flowing SVG wave, gently morphing image frames, leaf movement, product hover and one-time scroll reveals. Products use arched pantry frames, shelf lines and ticket-inspired labels. Both local review and native theme use the same CSS, motion script and SVG assets.

Generators: build_preview.py extracts source content; build_theme.py builds native templates and then runs build_heritage.py. Edits to generated sections belong in build_heritage.py. Shared presentation CSS: theme/assets/heritage.css. Slider code: theme/assets/heritage.js. Existing product photography, prices and copy remain captured reference data.

Browser review: desktop 1440px and narrow 390px checks; manual slider navigation, catalog images, product route and wishlist toggle tested. More exhaustive store testing awaits Shopify access.

Homepage refinement (19 November 2026): supplied horizontal SVG in navigation/footer, granny emblem extracted from Final Entire Logo.svg for the story. Shared home-refinements.css contains uncropped slide photography, aligned value packs, closed product labels, distinct kitchen line drawings and hover watercolour washes, custom navigation chevron and balanced review cards. Build sources retain these changes. JavaScript syntax, SVG XML and homepage asset references checked; offline desktop/mobile renders generated for inspection. Direct localhost browser inspection is restricted in the execution environment.

Homepage personality refinement: enlarged navigation/footer logo; removed bottom English/Hindi labels and vertically centred supplied wordmark and descriptor against the granny mark. Source preparation lives in scripts/build_kitchen_art.py. Seven original SVG category illustrations replace category pack photographs; product photography remains in product cards. Five interactive Ammamma notes provide ten short sayings, with reduced-motion support. Village SVG viewBox includes 48 units of space above the original bounds so the tree crown is complete. Shared preview/Shopify generator rebuilt; SVG parsing, asset references and JS syntax passed. Offline desktop/mobile-width renders inspected; live local-network inspection remains restricted.
