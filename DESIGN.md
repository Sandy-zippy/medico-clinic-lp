# Medico landing page design tokens

Source: ../brand/BRAND-2026-09-23.md (colours from the logo SVG's own fills; fonts measured on the live site).

## Colour
--brand #1475bc (primary, CTAs, links) · --charcoal #404041 (headings, dark band) · --text #333333 (body)
--muted #707070 (captions) · --slate #6c7781 (dividers, input borders) · --bg #ffffff · --ink #000000
Tints used on surfaces, derived from --brand at low chroma: --bg-2 #EFF8FF (the site's own light blue), --bg-3 #F4F4F4.
Strategy: Committed. Medico blue carries the CTA, the callout, the priority chip and the flow nodes; charcoal carries the proof band.

## Typography
Headings: Montserrat 700, self-hosted woff2, preloaded. Body: Open Sans 400, self-hosted woff2, swap.
Scale (tokens on :root): h1 clamp 1.9 to 3rem · callout 0.45 of h1 · h2 clamp 1.5 to 2.1rem · card/lg 1.125rem · body 1rem · small .875rem · label .8125rem · stat 1.75rem.

## Spacing
4px scale: 4 8 12 16 24 32 48 64 96. Radius 12px. Max width 1120px.

## Components
Form card (hero), proof band, stage list, five-node flow, project figures with 4:3 placeholders, area chips,
numbered next-steps, native details accordion, single CTA button style.
