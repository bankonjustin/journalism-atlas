# SMARTNEWS-PAGE-BRIEF-v1.1

Revision of `SMARTNEWS-PAGE-BRIEF-v1.0.md` after Justin's first look at the built page (Oct 20, 2026). Everything in v1.0 still applies unless changed here. Saved as given in chat; implementation notes are in `SMARTNEWS-PAGE-REPORT-v1.0.md` under "v1.1 revision".

**Cut:** the hero What/When/Who strip; the "Why are you here?" routing row (keep `setMode()` and the `data-mode` deep links).
**Merge:** creator terms stated once (cards) plus one `[DRAFT]` release sentence: "The program is built around independent publishers: creators keep ownership and control, only free content runs, no one may train AI on their work, and every piece links back to the creator's own publication."; SmartNews boilerplate only in "About SmartNews" (delete "Who SmartNews is" from Why SmartNews); delete the tracks section and make the form's "Interested in" options the first thing in the form (title, status pill, one-line description from `TRACKS`; keep `data-interest` deep links; join copy says it is a standing sign-up, not a one-time call).
**Tighten:** hero = kicker, headline, deck, two buttons; Atlas story = two sentences, live count, "Explore the Atlas"; release = no intro line.
**Fix:** fonts match v14 (quote it in the report); hero deck, release cohort paragraph, "How it works" cards and the interest options are static HTML that reads with JS off (comment at top of `COHORT`); ungate checklist adds "deploy the Apps Script, submit one real test, confirm the row lands in the Sheet."
**Target order:** co-brand band, hero, release (+ sidebar), Why SmartNews, founding cohort, How it works, the Atlas, Apply to join, About/media, footer.
**Report back with:** before/after sections, screenshots at 390 and 1440 (light and dark) plus one with JS off, the v14 font quote and every type change, copy changed beyond the brief, updated placeholder list and ungate checklist.
