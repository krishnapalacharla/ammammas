# Cloudflare Pages

This deploys the reviewed static design preview. Checkout and forms retain their existing preview behaviour; the Shopify theme is separate.

- Framework preset: None
- Build command: `python scripts/export_cloudflare.py`
- Build output directory: `dist`
- Root directory: repository root

The reviewed `preview/reference-data.json` snapshot is committed so deployment does not depend on the excluded reference crawl. Do not run the extraction generators in Cloudflare.

For direct upload with an authenticated Wrangler CLI: `npx wrangler pages deploy dist --project-name ammammas`.

Git integration can run the build after each push. Connect the intended repository to the existing `ammammas` Pages project to preserve its pages.dev address.
