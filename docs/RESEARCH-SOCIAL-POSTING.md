# Research hub: posting and editing guide

Everything on the research hub comes from two JSON files. Edit them on github.com (pencil icon), commit to `main`, and Cloudflare rebuilds. No code changes.

- `data/research.json`: one record per research piece, plus the CTA list.
- `data/social.json`: posts we want shown, plus the live Bluesky settings.
- `assets/research/<slug>/`: poster images and partner logos for a piece (`<slug>` is the piece's `slug`).

## 1. Tag every link you post

Put `?src=` on any link to journalismatlas.com in a post. Use one code per platform:

| Platform | Code | Example |
|---|---|---|
| Bluesky | `bsky` | `https://journalismatlas.com/watershed/?src=bsky` |
| Instagram | `ig` | `.../watershed/?src=ig` |
| TikTok | `tt` | `.../watershed/?src=tt` |
| LinkedIn | `li` | `.../watershed/?src=li` |
| Threads | `threads` | `.../watershed/?src=threads` |
| YouTube | `yt` | `.../watershed/?src=yt` |

The site already runs Google Analytics 4, which records the full address a reader landed on, so `?src=` shows up there as part of the page location. Check that it appears in your GA4 reports after launch; nothing in the code reads it.

Signup and contact links from the hub and piece pages carry `?source=<piece-slug>&cta=<cta-id>`. `/updates` writes both into the Formspree submission as hidden fields. `/contact` is a Google Form embed, so those two values reach the page address only, not the form. For now, contact attribution is via GA4 `page_location` only. The clean fix, after launch, is moving "Tell us" to a native Formspree form like `/updates`.

## 2. Add a post (Instagram, TikTok, LinkedIn, Threads, YouTube, or a Bluesky post you want to pin)

1. Save a poster image to `assets/research/<slug>/`, for example `assets/research/watershed/ig-oct-26.jpg`. These platforms are shown as a poster image that links out. There are no embed scripts.
2. Add an object to `posts` in `data/social.json`:

```json
{
  "id": "ig-watershed-2026-10-26",
  "piece_slug": "watershed",
  "platform": "instagram",
  "account": "atlas",
  "url": "https://www.instagram.com/p/XXXXXXXX/",
  "poster_image": "/assets/research/watershed/ig-oct-26.jpg",
  "alt": "Describe the image for someone who cannot see it.",
  "caption_short": "Our own words, one or two sentences.",
  "date": "2026-10-26"
}
```

- `platform`: `bluesky`, `instagram`, `tiktok`, `linkedin`, `threads` or `youtube`.
- `account`: `atlas`, or a team member's name.
- `piece_slug`: the piece it is about. Leave it `""` for a general post; it then appears on the hub only.
- `alt` is required for any poster image.
- `caption_short` is our words only. Never paste someone else's text.
- `date` is `YYYY-MM-DD`.

A post appears on the hub under "From our feeds" and, if `piece_slug` is set, on that piece's page under "Talked about on". Neither section appears while there are no posts.

## 3. Live Bluesky

`data/social.json` > `bluesky.accounts` lists the accounts to read. Each needs a real handle; while a handle is `TBD` or empty it is skipped. With no handles, nothing from Bluesky shows.

- Only posts that link to `journalismatlas.com` (`match_domain`) are shown. A post that links to a piece's URL is tagged to that piece automatically.
- `pinned_uris`: add `at://...` addresses to always show specific posts.
- It reads Bluesky's public API from the reader's browser. No keys, no login. If Bluesky is down or blocked, the section just doesn't appear.

## 4. Add or change a piece

Add an object to `pieces` in `data/research.json` (copy an existing one).

| Field | Notes |
|---|---|
| `slug` | lowercase, hyphens; also the folder name under `assets/research/` |
| `title`, `dek` | the dek is shown on the card |
| `type` | `essay`, `paper`, `field-brief`, `data-release`, `explainer`, `toolkit`, `map` |
| `status` | `live`, `coming`, or `placeholder`. `placeholder` and `coming` show "Coming <weekday, date>" and no link, using `date` |
| `date` | `YYYY-MM-DD` (or `YYYY-MM` if the day is unknown). Newest first |
| `url`, `link_label`, `external` | where "Read the ..." goes; `external: true` opens a new tab |
| `authors`, `partners` | partners are `{name, role, logo, url}`; the partners band shows when at least two distinct partners exist across all pieces |
| `hero_image` | `{src, alt}` |
| `cta_primary`, `cta_secondary` | one of: `updates-signup`, `partner-inquiry`, `funder-inquiry`, `tell-us-who-were-missing`, `trust-lab-interest` |
| `featured` | `true` puts a live piece at the top of the hub. Use it on one piece |

Leave any fact you do not have as `""`. The page shows nothing for an empty field; it never fills in a placeholder.

`trust-lab-interest` has no button label yet (`ctas` in `research.json`), so it renders nothing until one is written.

## 5. Piece pages

A piece page gets two chrome hooks, kept outside the essay text:

- `<div data-research-talked data-piece="<slug>" hidden></div>` above the endcap. Empty until a post is tagged to the piece.
- The endcap's main button carries `data-research-cta="primary" data-piece="<slug>"`. Its label and link come from the record's `cta_primary`. The text around the button (heading and sentence) is written for `tell-us-who-were-missing`; if you change `cta_primary`, that copy has to change with it.
- Also load `/assets/css/research-hub.css` and `/assets/js/research-hub.js` (deferred) on the page.

## 6. Nodes and Networks, Nov 5

Change its record: `status` to `live`, fill `url`, `link_label`, `hero_image`, `partners`, `cta_primary`; add posts. Data only.
