# Website project rules

- Build a native Shopify theme, not a React app.
- Work inside this single repository; do not create numbered version folders or delivery ZIPs.
- Presentation brand assets are authoritative. Never use old website logos, mascots, colours or typography.
- First review preserves captured product photos, descriptions, pages and links.
- Keep store access optional for local design review. Never send preview actions to production APIs.
- Theme CSS and images are shared with the offline preview. Preserve both paths when changing designs.
- Generated content is rebuilt with scripts/build_preview.py then scripts/build_theme.py. Edit generators for generated templates.
- Record capture gaps and integration limits; never invent product prices, images, stock or backend success.
- Use meaningful Git checkpoints. Do not publish a theme without an explicit publishing request.
