# Atlas Design Questions — For James
**From:** Justin
**Context:** Async design/dev coordination doc. These are the open questions across the live Atlas pages where I need your input before I build or change anything. Some are quick decisions, some need assets from you.

Reply inline with answers, or add comments — whatever works. I'll action each one once you've responded.

---

## 1. Starter Pack page — Instructional Video

There's a `<!-- TODO: instructional video slot -->` reserved in the header of the Starter Pack page, sitting between the intro copy and the "Start curating →" CTA.

**You suggested:** A short screen-recording (Loom-style) showing browse → select → build → share.

**Questions:**
- Who makes this? Are you producing it or should I commission it / record it myself?
- How long should it be? (My assumption: 30–45 seconds, no voiceover, just screencap with maybe music)
- Should it autoplay muted, or be a play-to-start?

---

## 2. Partner Pages — Curator Photo / Logo Spec

We now have a stacked header layout on partner pages: Atlas logo → separator → "In collaboration with" → partner avatar/logo → description.

**Current state:**
- Chris Cillizza: has his headshot (`Cillizza-1.jpg`) — displaying in a 52×52 acid-green-bordered circle
- Grist: has `Grist-rebrand-logo-announcement.webp` — displaying as a 44px-tall rectangle with border-radius 6px
- Future partners: no spec exists yet

**Questions:**
- Is the circle crop (52×52) right for individual curators, or should headshots be larger now that we're in a stacked layout? Could go bigger — there's room.
- For institutional logos (Grist, CalMatters etc.), should they always be a fixed height rectangle, or is there a preferred container/treatment?
- Should we define a spec now for the "partner identity upload" — e.g. "submit a square PNG, 400×400 minimum" for individuals and "submit a horizontal PNG on transparent background" for institutions?

---

## 3. Grist Logo — Background Color

The Grist logo we have (`Grist-rebrand-logo-announcement.webp`) has a **solid lime green background** — it's not a transparent PNG. On the dark Atlas background it renders as a lime-green box with "Grist" text inside.

**Options:**
- a) Keep as-is — the colored box looks like a deliberate brand badge (might actually work)
- b) Get a transparent PNG from Grist (correct solution, requires asset from them)
- c) I render their name as styled text until we have the asset

**Question:** What's your call? If (b), do you have a Grist contact or should I source from their press kit?

---

## 4. Canvas / Generated Image — Logo Sizing

The Starter Pack generated image now uses the horizontal wordmark at the top (replacing the all-caps text). It's drawn at 28px height on a 1080×1080 canvas.

**Question:** Can you look at a generated pack image and tell me if the logo size/placement feels right? Too small? Too much top padding? I want your eye on this before we call it done.

*(Build a quick test pack at journalismatlas.com/postcard and copy the image.)*

---

## 5. Beat Pages — Off-Brand Accent Color

`beat-climate.html`, `beat-finance.html`, `beat-tech.html` use `#00a896` (a teal green) as their eyebrow/accent color instead of `#ceff00` (Atlas acid green).

**Question:** Was this intentional — like a sub-brand treatment for the beat labs? Or is it legacy and should those pages just use the standard acid green?

---

## 6. Index Hero — Stacked Logo

The index.html hero uses the **stacked logo** variant (`Journalism_Atlas_wordmark_stacked_green_white (3).png`).
Everywhere else uses the horizontal lockup.

**Questions:**
- Is the stacked version intentional for the hero, or should we standardize to the lockup everywhere?
- Also: that filename has `(3)` in it — is that the final export or do you have a clean version I should replace it with?

---

## 7. Advisory Page — Headshot Filenames

The advisory board headshots have inconsistent, messy filenames — some have spaces, commas, search query strings, version numbers:
- `find photographer near me, portrait_Austin_headshot (1).jpeg`
- `K Merida Headshot 2M (1).jpg`
- `MicahGelman3 copy.jpg`

This doesn't affect display but is a mess in the repo and can cause issues on some servers.

**Ask:** Can you do a clean pass on these filenames? Rename each to `firstname-lastname.jpg` format and send back, or just tell me what the correct names are and I'll rename in place.

---

## 8. og:image — Social Preview Cards

Nine live pages are missing `og:image` meta tags, meaning link previews on social/Slack/iMessage show no image:

| Page | Missing |
|------|---------|
| postcard.html | og:image |
| lists.html | og:image + og:description |
| beat-climate.html | og:image |
| beat-finance.html | og:image |
| beat-tech.html | og:image |
| city-lab-dc-v2.html | og:image |
| city-lab-chicago.html | og:image |
| advisory.html | og:image |

There's already one OG image in assets: `Atlas_green_gray_social_media_preview.png`.

**Questions:**
- Should all these pages use the generic OG image, or do some pages need custom previews?
- Do the beat pages / city lab pages need their own OG images, or is the Atlas default fine for now?
- Is the existing OG image (`Atlas_green_gray_social_media_preview.png`) current/final, or is there a newer version?

---

## 9. Navigation — Beat Pages Have No Nav

`beat-climate.html`, `beat-finance.html`, `beat-tech.html` have no top nav bar at all. They go straight to a header section.

**Question:** Intentional (standalone landing pages that shouldn't link back to Atlas)? Or oversight? If they should have nav, I'll add the standard Atlas bar.

---

## 10. City Lab — Which Version Is Live?

There are four DC city lab files in the repo:
- `city-lab-dc.html`
- `city-lab-dc2.html`
- `city-lab-dc-v2.html` ← I believe this is the current one (it's what city-lab-dc-v2 refers to)
- `city-lab-dc-v3.html`

And one Chicago:
- `city-lab-chicago.html`

**Ask:** Confirm which DC file is production/live, so I can archive or delete the others and stop working around them. Also — is Chicago live or still in progress?

---

## Standing question — Partner Page Template

As we add more partner pages (CalMatters, etc.), we'll want a template rather than hand-editing each one. I can build a simple template once we've confirmed the design is locked.

**Question:** After seeing Cillizza and Grist live, is the stacked layout right? Anything you'd change before I lock the template?

---

*Last updated: Apr 8, 2026*
*Next steps tracked in main codebase — reply here and Justin will action*
