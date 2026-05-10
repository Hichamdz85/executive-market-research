# Quality Standards — Pre-Delivery Checklist

Run through this checklist before showing any report to the user. The benchmark is: **"Would I be proud to put my consulting firm's logo on this and bill a client $50,000?"**

## Content quality

### Numbers & data
- [ ] Every number has a unit (USD, tons, %, units, persons)
- [ ] Every number has a time period (year or year range)
- [ ] CAGR calculated correctly: `(End / Start)^(1/years) - 1`, not approximated
- [ ] Currency basis stated (current USD, constant 2020 USD, etc.)
- [ ] No "growing rapidly" without a number; no "significant" without a magnitude
- [ ] Data comes from Tier 1 or Tier 2 sources (see `data_sources.md`)
- [ ] At least 2 sources cross-checked for any critical headline number
- [ ] Data is no older than 18 months unless explicitly historical analysis

### Sourcing
- [ ] Every chart has a "Source:" line in 9pt grey text
- [ ] Every quoted statistic has an inline citation
- [ ] Bibliography in appendix lists every source with a working URL
- [ ] No source labeled "Internet", "AI", "ChatGPT", or "internal estimate" without explanation
- [ ] Where data was estimated/triangulated, the method is disclosed

### Analytical depth
- [ ] Executive summary fits on a single page
- [ ] At least 3 charts in the import characteristics section
- [ ] Regulatory section covers: HS codes, duties, FTAs, certifications, payment terms, restrictions
- [ ] Recommendations are specific (not "consider exploring") and tied to evidence in the report
- [ ] Risk register has at least 5 risks with likelihood × impact
- [ ] SWOT has 3–4 items per quadrant, each as a complete thought

### Tone & language
- [ ] Corporate consulting register throughout — no marketing fluff
- [ ] No emojis in body content (icons are SVG line art, not emoji)
- [ ] No first-person ("I", "we") except in author bio
- [ ] No second-person ("you") except in recommendations
- [ ] Active voice preferred over passive
- [ ] Stop-words avoided: "very", "really", "quite", "actually", "basically"
- [ ] No filler phrases: "in today's market", "in the digital age", "the world is changing"
- [ ] Every sentence has information density — could a busy CEO learn something from this?

## Visual quality

### Cover page
- [ ] Hero image is high-resolution (at least 1920px wide), product-relevant
- [ ] Country flag is present and correctly oriented
- [ ] Report title is in primary navy
- [ ] Date is in format "Month YYYY" (e.g., "May 2026")
- [ ] Author logo is in top-right or bottom-right
- [ ] No clipart, no stock-photo cliché ("handshake over globe")

### Table of contents
- [ ] All sections listed with correct page numbers
- [ ] Section icons rendered (book, demand, supply, regulatory, etc.)
- [ ] Roman numerals (I–IX) for sections
- [ ] Right-aligned page numbers with leader dots OR clean spacing

### Section dividers
- [ ] Full-bleed image on left half
- [ ] Section title (e.g., "III. Market review") in primary navy on right half
- [ ] No body content on dividers

### Headers & footers
- [ ] Every content page has the header bar (light grey background, navy section title, logo top-right)
- [ ] Every content page has footer: date | report title | page number
- [ ] Cover and section dividers have NO header/footer (clean look)

### Charts
- [ ] Title is a finding, not a label
- [ ] Axis labels include units
- [ ] Data labels on bars / data points
- [ ] Source citation below chart
- [ ] Consistent color palette (primary navy as fill, accent for comparisons)
- [ ] No chart junk (3D effects, drop shadows, busy gridlines)
- [ ] Charts are vector (SVG) where possible, sharp at any zoom level

### Tables
- [ ] Header row in primary navy with white text
- [ ] Alternating row colors (white / light grey) for readability
- [ ] Numbers right-aligned, text left-aligned
- [ ] Consistent decimal places
- [ ] Currency symbols at column header, not repeated per cell

### Typography
- [ ] One font family per language (Helvetica/Arial for Latin, Cairo or Tajawal for Arabic)
- [ ] Heading hierarchy: H1 (24pt navy), H2 (18pt navy), H3 (14pt navy bold), body (10pt black)
- [ ] Body line spacing 1.4–1.5
- [ ] No widows or orphans (single line at top/bottom of page)

### RTL (Arabic) specifics
- [ ] Layout fully mirrored (logo on left, page numbers on left)
- [ ] Charts: y-axis on right, x-axis read right-to-left
- [ ] Numbers in Arabic-Indic numerals OR Western Arabic numerals — pick one and be consistent
- [ ] Mixed-direction text (e.g., "USD 50M") handled with proper bidi controls

## Structural quality

- [ ] Page count between 25–60 pages (not too thin, not bloated)
- [ ] Every section has a divider page
- [ ] TOC page numbers match actual page numbers
- [ ] Cross-references to other sections work (e.g., "see Appendix A")
- [ ] Appendix has full bibliography, glossary, methodology notes
- [ ] No broken images, no missing fonts, no Lorem ipsum

## Functional quality (HTML version)

- [ ] Charts are interactive (hover for data labels)
- [ ] TOC links jump to correct sections
- [ ] Print stylesheet works (`window.print()` produces a clean PDF)
- [ ] Mobile-responsive (readable on tablets)
- [ ] No external CDN dependencies that could break (vendor everything)
- [ ] Loads in under 3 seconds on a typical connection

## Functional quality (PDF version)

- [ ] Generates as A4 landscape (or A4 portrait — pick and stay consistent)
- [ ] Text is selectable (not rasterized)
- [ ] Hyperlinks in references are clickable in the PDF
- [ ] File size under 15MB (compress images appropriately)
- [ ] Renders identically across Acrobat, Preview, Chrome PDF viewer

## Final sanity checks

- [ ] Spell-check passed in the chosen language
- [ ] No placeholder text ("[Insert XYZ here]", "TODO", "FIXME")
- [ ] All client/author names spelled correctly
- [ ] Date is current (not from a previous engagement)
- [ ] Country name spelled correctly throughout
- [ ] Product name consistent throughout (no synonym drift)
- [ ] Confidentiality footer if applicable

If any item is unchecked, fix it before delivery. Don't ship a half-baked deliverable.
