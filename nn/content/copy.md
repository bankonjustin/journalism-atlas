<!--
Every reader-facing word of the Nodes and Networks kit lives in this file.

HOW TO EDIT (github.com: open this file, click the pencil, edit, commit):
  - One heading per string: "## some.id", then the text on the lines below it.
  - Leave numbers as tokens like {over10m_total}. The build fills them from the data.
    Typing a number by hand gives a warning in the build log.
  - {@other.id} pastes another string in, so a sentence is written once.
  - {name|cap} capitalizes the first letter.
  - Tokens that hold a name or a count (for example {cut}) are listed in nn/README.md.
  - Strings marked [locked] quote the paper. The build stops if they change.
  - Video captions (video.*) are burned into the video. Changing them needs a re-render:
    python3 nn/tools/render_media.py  (see nn/README.md). Everything else updates on the next deploy.
-->

# Header and footer

## header.eyebrow
Nodes and Networks · Explorer

## header.title
Nodes and Networks

## header.sub
{n_orgs} U.S. journalism organizations, sorted into {cohorts_word} kinds of newsroom

## footer.data
Data: {n_orgs} organizations, current as of October 2026, available on request.

## attr.line
{publisher_line}

## report.fallback_label
About the report

# Tabs

## tabs.short
In short

## tabs.governance
1 Who pays

## tabs.ways
2 How they got big

## tabs.history
3 When they started

## chapter_nav.label
Chapter

## chapter_nav.aria
Chapter {n}: {name}

## chart.aria
Chart of {n} organizations. {title}. {sentence} {stat}

## how_to_read.summary
How to read this

## explore.summary
Explore

# In short

## in_short.top_line
Who pays for journalism shapes how big it gets.

## in_short.encoding
Color shows who pays. A square started above $10M. A triangle grew past it. A dashed triangle is the exception.

## in_short.see_chart
See the chart

## in_short.thumb_aria
{name} thumbnail

# Chapter 1: who pays

## chapter1.name
Who pays

## chapter1.sentence
{cohorts_word|cap} kinds of newsroom, sorted by who pays. {top_word|cap} of them hold {top_hold} of the {over10m_total} organizations over $10 million. The other {rest_word} hold {rest_hold}.

## chapter1.title
{top_word|cap} of {cohorts_word} kinds of newsroom hold {top_pct}% of the organizations over $10 million.

## chapter1.paper [locked]
Nine cohorts capture the range of journalism operators currently producing in the United States, in three groups.

## chapter1.stat
{n_orgs} organizations. {cohorts_word|cap} cohorts. Three groups.

## chapter1.position
Each wedge is one cohort.

# Chapter 2: how they got big

## chapter2.name
How they got big

## chapter2.sentence
{crossed} organizations grew past $10 million. {six_way_growers} of them did it one of six ways.

## chapter2.title
{ways_word|cap} ways to grow past $10 million

## chapter2.paper [locked]
Organizations that break past their cohort's typical ceiling almost always do so through one of six specific mechanisms — and rarely more than one.

## chapter2.stat
Of the {crossed} organizations that grew past $10M, {six_way_growers} did it one of six ways. {exceptions_phrase|cap}.

## chapter2.position
Each sector is one mechanism. Organizations that started above $10M and those still under it have their own sections.

## chapter2.position_bundle
Mechanism 1, Bundle, is an empty slot: {@chapter2.bundle_note}

## chapter2.bundle_note
No organization grew past $10M this way. Every bundle in the dataset started above it.

# Chapter 3: when they started

## chapter3.name
When they started

## chapter3.sentence
The oldest are the biggest: {hist_pre_over} of {hist_pre} founded before {cut} run over $10 million. But who pays matters more than when an organization started.

## chapter3.title
When they started matters. Who pays them matters more.

## chapter3.dek
The internet began reshaping print and broadcast distribution in {cut}. Organizations founded before then mostly run above $10 million: {hist_pre_over} of {hist_pre}. Those founded since mostly don't: {hist_post_over} of {hist_post}. Only {hist_old_kinds_word} of the {cohorts_word} kinds of newsroom in this study existed before {cut}. The rest are new ways to pay for journalism, and most of their organizations are still small.

## chapter3.foot
Position is founding year, left to right. The axis is compressed before {cut}. Filled marks are over $10M in revenue. {unverified_orgs} with no verified founding year {unverified_be} not shown. Who pays predicts an organization's revenue more strongly than when it was founded.

# Legend and labels

## legend.color
Color

## legend.shape
Shape

## legend.started_above
Started above $10M

## legend.grew_past
Grew past $10M

## legend.grew_past_exception
Grew past $10M without one of the six

## legend.under
Under $10M

## legend.ten_or_under
$10M or under

## list.no_mechanism
No mechanism

## list.no_mechanism_note
grew past $10M on a platform licensing deal

## labels.exception_short
Exc.

## labels.exception_1
Exception

## labels.exception_2
platform licensing

## labels.above_wide
Started above $10M ({n})

## labels.above_narrow
Above $10M

## labels.under_1
Under $10M

## labels.under_2
not yet grown past it

# Cards (the box that opens on a mark)

## card.mechanism
Mechanism: {name}

## card.over
Over $10M in revenue

## card.under
$10M or under in revenue

## card.unverified
Revenue estimate unverified

## card.founded
Founded {year}

## card.status
Status: {status}

## card.revenue
Revenue: {value}

## card.none_of_six
Mechanism: none of the six

# Notes on the charts

## ann.gov_top
{gov_top_name}: {gov_top_up} of {gov_top_n} over $10M.

## ann.gov_second
{gov_second_name}: {gov_second_up} of {gov_second_n}.

## ann.gov_small
{gov_small_names}: {gov_small_up} of {gov_small_n} over $10M.

## ann.ways_six
{six_way_growers} of {crossed} that grew past $10M used one of the six.

## ann.ways_exception
The exception: {exception_name}, a platform licensing deal.

## ann.ways_started
{started_above} started above $10M, among them {older_two}.

## ann.hist_c5
{hist_c5_name}: {hist_c5_pre} of {hist_c5_n} founded before {cut}.

## ann.hist_c2
{hist_c2_name}: {hist_c2_up} of {hist_c2_n} over $10M.

## ann.hist_c7
{hist_c7_name}: {hist_c7_up} of {hist_c7_n} over $10M.

# History chart

## hist.era_title
Share over $10M, by when they started

## hist.key_started
Started above $10M (lighter)

## hist.main_title
Every organization, by cohort and founding year

## hist.hero
{cut}: the internet starts reshaping print and broadcast distribution.

## hist.row_wide
{over} of {tot} over $10M

## hist.row_narrow
{over} of {tot}

## hist.col_over
over $10M

## hist.axis_before
Before {cut} (compressed)

## hist.axis_since
{cut} to 2026

## hist.era_aria
{label}: {over} of {n} over $10M

## hist.era_aria_full
{label}: {over} of {n} over $10M ({grew} grew past, {above} started above)

## hist.mark_aria
{name}, {cohort}, founded {year}, {shape}

# Names from the paper [locked]

## cohort.C1 [locked]
Legacy Publishers

## cohort.C2 [locked]
Creator Brands

## cohort.C3 [locked]
Barbell Hybrids

## cohort.C4 [locked]
Philanthropic Mesh Networks

## cohort.C5 [locked]
Public Media Networks

## cohort.C6 [locked]
Collaboration Layers

## cohort.C7 [locked]
Worker-Owned Co-ops

## cohort.C8 [locked]
Emerging Civic Actors

## cohort.C9 [locked]
B2B/Professional Services

## group.a [locked]
Journalism as most people picture it

## group.b [locked]
Funded by philanthropy and public money

## group.c [locked]
Funded directly by audiences and the market

## mechanism1.short
Bundle

## mechanism1.full [locked]
A bundle big enough to capture a subscriber's whole information budget

## mechanism2.short
Ideology

## mechanism2.full [locked]
An audience captured by ideology rather than reporting

## mechanism3.short
Team + portfolio

## mechanism3.full [locked]
A newer organization that grew a team and a portfolio at once

## mechanism4.short
B2B

## mechanism4.full [locked]
B2B pricing built for an employer's expense account rather than a household budget

## mechanism5.short
Philanthropy

## mechanism5.full [locked]
Philanthropic scale large enough to function like an endowment

## mechanism6.short
Diversified

## mechanism6.full [locked]
Genuine diversification, with no single stream large enough to hurt if it disappeared

# Landing page: /nodes-and-networks/

## landing.page_title
Nodes and Networks | Independent Journalism Atlas

## landing.meta_description
{@in_short.top_line} A study of {n_orgs} U.S. journalism organizations in {cohorts_word} kinds of newsroom. Watch the video and explore the data.

## landing.eyebrow
A study of {n_orgs} U.S. journalism organizations

## landing.h1
Nodes and Networks

## landing.top_line
{@in_short.top_line}

## landing.intro
The study sorts {n_orgs} organizations into {cohorts_word} kinds of newsroom, then asks which ones grew past $10 million, and how.

## landing.report_cta
{report_label}

## landing.video_heading
Watch the {video_seconds}-second version

## landing.video_label
Nodes and Networks: a short video

## landing.video_fallback
Your browser can't play this video. Open the explorer below instead.

## landing.video_tall_link
Vertical version for phones and social

## landing.chapters_heading
Three chapters

## landing.chapter_link
Open this chapter

## landing.explorer_heading
Explore the {n_orgs} organizations

## landing.explorer_note
Hover or tap a mark to see the organization.

## landing.explorer_title
Nodes and Networks explorer: {n_orgs} U.S. journalism organizations

## landing.open_full
Open the full explorer

## landing.use_heading
Use this on your site

## landing.use_body
Embed the explorer with one line of code. The embed page has the code, the tab links and the credit line.

## landing.use_link
Get the embed code

## landing.credit_label
From

# Embed page: /nodes-and-networks/embed/

## embed.page_title
Embed the explorer | Nodes and Networks

## embed.meta_description
Copy-paste code to put the Nodes and Networks explorer on your page, with tab links, sizes and the credit line.

## embed.eyebrow
Nodes and Networks

## embed.h1
Embed the explorer

## embed.intro
Paste one of these into your page. The address ends in `?embed=1`, which removes the header and footer and makes the background clear.

## embed.who
The explorer can be framed on asu.edu pages and on journalismatlas.com. To use it on another site, [ask us first](/contact).

## embed.size_heading
Size

## embed.size_body
Use a width of {embed_width}px or less. The explorer fills the width you give it. Height depends on the tab and the width. A fixed frame needs {embed_h_narrow}px under {embed_breakpoint}px wide and {embed_h_wide}px from {embed_breakpoint}px up, which fits every tab and leaves empty space on the shorter ones. The auto-height code below has no empty space.

## embed.plain_heading
1. Plain iframe

## embed.plain_body
Works in any system that allows iframes.

## embed.responsive_heading
2. Plain iframe with two heights

## embed.responsive_body
If your system allows a style block, this switches the height at {embed_breakpoint}px.

## embed.auto_heading
3. Auto-height iframe

## embed.auto_body
If your system allows scripts, this resizes the frame to fit. There is no empty space and no inner scrollbar. The explorer sends its height each time its size changes, and the listener accepts messages only from this frame. To embed two explorers on one page, copy the code and change the id.

## embed.still_heading
4. Still image, if your system strips iframes

## embed.still_body
A still of the first chapter, linked to the live explorer. Upload the image to your media library and change the image address to match.

## embed.tabs_heading
Links to each tab

## embed.tabs_body
Add `&embed=1` to any of these when you embed.

## embed.tab_col_view
View

## embed.tab_col_value
tab value

## embed.tab_col_link
Link

## embed.tab.short
In short (opens first)

## embed.tab.governance
1 Who pays

## embed.tab.ways
2 How they got big

## embed.tab.history
3 When they started

## embed.credit_heading
Credit line

## embed.credit_body
Place this under the embed. The explorer also shows it at the bottom of the frame.

## embed.credit_line
Nodes and Networks. {publisher_line}. journalismatlas.com

## embed.notes_heading
Good to know

## embed.note_keyboard
Tabs work with the keyboard. Arrow keys move between them.

## embed.note_motion
With "reduce motion" on, tabs switch with no animation.

## embed.note_theme
The explorer follows the visitor's light or dark setting. The chart area is always black.

## embed.note_privacy
No cookies, no network requests, no outside fonts or scripts. The explorer is one self-contained page.

## embed.note_cards
Hover or tap a mark to see the organization, its kind of newsroom, how it grew, its revenue and the year it was founded.

## embed.back
Back to Nodes and Networks

## embed.still_alt
{n_orgs} U.S. journalism organizations sorted into {cohorts_word} kinds of newsroom and colored by who pays. Open the interactive explorer.

# Share images

## share.title
Nodes and Networks

## share.line
{@in_short.top_line}

## share.chapter1
{@chapter1.sentence}

## share.chapter2
{@chapter2.sentence}

## share.chapter3
{@chapter3.sentence}

## share.alt_landing
Nodes and Networks. {@in_short.top_line} {publisher_line}.

## share.alt_chapter
Nodes and Networks, {name}: {sentence}

# Video (burned in: re-render after editing)

## video.cue1
{@in_short.top_line}

## video.cue2
{cohorts_word|cap} kinds of newsroom, sorted by who pays.

## video.cue3
{top_word|cap} of them hold {top_hold} of the {over10m_total} organizations over $10 million.

## video.cue4
{crossed} organizations grew past $10 million.

## video.cue5
{six_way_growers} of them did it one of six ways.

## video.cue6
The oldest are the biggest: {hist_pre_over} of {hist_pre} founded before {cut} run over $10 million.

## video.cue7
But who pays matters more than when an organization started.

## video.end_title
Nodes and Networks

## video.end_publisher
{publisher_line}

## video.end_site
journalismatlas.com
