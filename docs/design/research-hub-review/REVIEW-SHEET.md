# Research hub: review sheet for James

Preview: `/preview/research/` (noindex). Built from v16 roles only. `python3 scripts/check_brand.py` reports no new violations (baseline 2777, unchanged). Nothing here adds a color, size, weight, radius or font.

Screenshots show **sample data**: one made-up Instagram card (a test card using the Watershed image) so the feed pattern is visible. The real data has no posts, so on the live preview the "From our feeds" section does not appear.

- `hub-390-sample.png`, `hub-1280-sample.png`
- `watershed-endcap-390-sample.png` (endcap and footer; the "Talked about on" module renders above it only when a post is tagged)

| # | Pattern | Where | Tokens used | Question for James |
|---|---|---|---|---|
| 1 | **Piece card** (meta line, title, dek, instruction link) | Hub "All research" (dark) | Surface `--gray-neutral-6` on `--color-surface-dark`; border `--color-border-on-dark`; meta = Tag (Source Code Pro 12px caps 0.08em); title = H3 20/600; dek = Small 13; link = `.link-instruction`; radius 6px | Card fill is step 6 on a step 7 surface. OK, or should cards be outline only? |
| 2 | **Placeholder state** ("Coming Thursday, Nov 5, 2026") | Hub, Nodes and Networks | Same card; meta line carries the state; no link, no image | The Placeholder Principle says no empty states in public design. This is the card the brief asked for until Nov 5. Confirm. |
| 3 | **Featured piece** (image + text, stacks on phones) | Hub top | Eyebrow in Acid on dark; H1 36 / 28px on phones (H2 is 28, not used); body 16; `.btn--primary` and `.link-instruction` on dark | Phone headline is 28px, a type-scale value. Fine? |
| 4 | **Social post card** (poster, meta, caption, link out) | Hub "From our feeds", piece pages | White card `--color-bg-card`, border `--color-border`, radius 6; poster radius 6; meta Tag; caption Small 13 | Platform names are in the meta line only; no platform colors or icons (no color coding by type). OK? |
| 5 | **Partners band** (name cards, optional logo, role) | Hub | White card, border `--color-border`, name Body 16/600, role Small 13; "Work with us" `.btn--primary` | No logos yet (none confirmed). Logo cap is 48px high. |
| 6 | **Hub signup band** | Hub bottom | Dark surface; Acid eyebrow; `.btn--primary` | None |
| 7 | **"Talked about on"** | Watershed, above the endcap | White surface (`--color-surface`), H3-size heading, same post card, 3-up from 1000px | Sits above the existing endcap, not inside it. |
| 8 | **Endcap change** | Watershed | Existing endcap kept; only the button now reads `cta_primary` (`tell-us-who-were-missing`) and links to `/contact?source=watershed&cta=tell-us-who-were-missing`. No new visual. | None |

## Flagged, not decided

- The endcap's own CSS comment already says "NEW PATTERN: needs James's sign-off." That stands.
- Eyebrow labels use Source Code Pro (Label, v16). The Oct 28 provisional says mono is for live or versioned data only. They conflict; I followed v16 § Eyebrows.
- Dark sections alternate with light bands (v16 § surfaces). The feed and partners bands are light.
