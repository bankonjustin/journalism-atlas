#!/usr/bin/env node
// scripts/fetch_chicago_feeds.js
// Run: node scripts/fetch_chicago_feeds.js
// Output: data/chicago-pulse.json
//
// Fetches up to 3 recent items from each feed in CHICAGO_FEEDS.
// Commit the output to trigger a page refresh on next Cloudflare deploy.

import { writeFileSync, mkdirSync } from 'fs';

// ── FEED LIST ────────────────────────────────────────────────────────────────
// Mirror of CHICAGO_FEEDS in city-lab-chicago.html.
// When you add/remove feeds from the HTML, update this list too.
// Fields: layer, name, channel, beat, url, rss, beatColor, volume (optional)

const FEEDS = [
  // City Hall & Politics — creators
  {layer:'creator',name:'Eric Zorn',channel:'The Picayune Sentinel',beat:'City Hall & Politics',url:'https://ericzorn.substack.com',rss:'https://ericzorn.substack.com/feed',beatColor:'#0044cc'},
  {layer:'creator',name:'Austin Berg',channel:'The Last Ward',beat:'City Hall & Politics',url:'https://www.thelastward.org',rss:'https://www.thelastward.org/feed',beatColor:'#0044cc'},
  {layer:'creator',name:'Charlie Meyerson',channel:'Chicago Public Square',beat:'City Hall & Politics',url:'https://www.chicagopublicsquare.com',rss:'https://www.chicagopublicsquare.com/feed',beatColor:'#0044cc'},
  {layer:'creator',name:'Rich Miller',channel:'Capitol Fax',beat:'City Hall & Politics',url:'https://capitolfax.com',rss:'https://capitolfax.com/feed',beatColor:'#0044cc'},
  {layer:'creator',name:'Patrick Pfingsten',channel:'The Illinoize',beat:'City Hall & Politics',url:'https://www.theillinoize.com',rss:'https://www.theillinoize.com/feed',beatColor:'#0044cc'},
  {layer:'creator',name:'Ben Joravsky',channel:'The Ben Joravsky Show',beat:'City Hall & Politics',url:'https://benjoravsky.substack.com',rss:'https://benjoravsky.substack.com/feed',beatColor:'#0044cc'},
  {layer:'creator',name:'Politically Illinois',channel:'Politically Illinois',beat:'City Hall & Politics',url:'https://politicallyillinois.substack.com',rss:'https://politicallyillinois.substack.com/feed',beatColor:'#0044cc'},
  {layer:'creator',name:'H Kapp-Klote',channel:'The Chicago 312',beat:'City Hall & Politics',url:'https://hs-newsletter-e91163.beehiiv.com',rss:'https://hs-newsletter-e91163.beehiiv.com/feed',beatColor:'#0044cc'},
  // Sports
  {layer:'creator',name:'Andrew Donlan',channel:'Still Gotta Come Through Chicago',beat:'Sports',url:'https://sgctc.substack.com',rss:'https://sgctc.substack.com/feed',beatColor:'#006600'},
  // Arts & Culture
  {layer:'creator',name:'Caroline Patton',channel:'Chicago Show Calendar',beat:'Arts & Culture',url:'https://chicagoshowcal.substack.com',rss:'https://chicagoshowcal.substack.com/feed',beatColor:'#660066'},
  {layer:'creator',name:'Theresa Goodrich',channel:'Living Landmarks of Chicago',beat:'Arts & Culture',url:'https://chicagolandmarks.substack.com',rss:'https://chicagolandmarks.substack.com/feed',beatColor:'#660066'},
  // Media & Press Freedom
  {layer:'creator',name:'Nathan Graber-Lipperman',channel:'Creator Mag',beat:'Media & Press Freedom',url:'https://www.creatormag.blog',rss:'https://www.creatormag.blog/feed',beatColor:'#884400'},
  {layer:'creator',name:'Igor Studenkov',channel:'Chicago Media Journal',beat:'Media & Press Freedom',url:'https://chimediajournal.substack.com',rss:'https://chimediajournal.substack.com/feed',beatColor:'#884400'},
  {layer:'creator',name:'Mark Jacob',channel:'Stop the Presses',beat:'Media & Press Freedom',url:'https://www.stopthepresses.news',rss:'https://www.stopthepresses.news/feed',beatColor:'#884400'},
  // Education / CPS
  {layer:'creator',name:'Maureen Kelleher',channel:'Board Rule',beat:'Education / CPS',url:'https://board-rule.ghost.io',rss:'https://board-rule.ghost.io/rss',beatColor:'#880000'},
  {layer:'creator',name:'Daniel B. Rodriguez',channel:'Daniel B. Rodriguez',beat:'Education / CPS',url:'https://danielbrodriguez.substack.com',rss:'https://danielbrodriguez.substack.com/feed',beatColor:'#880000'},
  // Black Chicago
  {layer:'creator',name:'Charlene Rhinehart',channel:'Chicago Southsider',beat:'Black Chicago',url:'https://chicagosouthsider.substack.com',rss:'https://chicagosouthsider.substack.com/feed',beatColor:'#884400'},
  {layer:'creator',name:'The JAAM',channel:'The JAAM',beat:'Black Chicago / City Hall & Politics',url:'https://thejaampod.substack.com',rss:'https://thejaampod.substack.com/feed',beatColor:'#884400'},
  {layer:'creator',name:'Ricardo Gamboa',channel:'The Hoodoise',beat:'Black Chicago',url:'https://hoodoisie.wordpress.com',rss:'https://hoodoisie.wordpress.com/feed',beatColor:'#884400'},
  {layer:'creator',name:'Ernest Crim III',channel:"Crim's Class",beat:'Black Chicago',url:'https://ernestcrim.com',rss:'https://crimsclass.substack.com/feed',beatColor:'#884400'},
  // LGBTQ+
  {layer:'creator',name:'Anna DeShawn',channel:'Queer News',beat:'LGBTQ+',url:'https://annadeshawn.com',rss:'https://annadeshawn.substack.com/feed',beatColor:'#660066'},
  // Labor
  {layer:'creator',name:'Jerry Mead-Lucero',channel:'Labor Express Radio',beat:'Labor',url:'https://laborexpress.net',rss:'https://anchor.fm/s/faa5ac8/podcast/rss',beatColor:'#555500'},
  // Black Chicago
  {layer:'creator',name:'Hermene Hartman',channel:"N'DIGO Studio",beat:'Black Chicago',url:'https://ndigo.com',rss:'https://ndigo.com/feed',beatColor:'#884400'},
  // Solopreneur / Collective additions
  {layer:'creator',name:'Unraveled',channel:'Unraveled',beat:'General News',url:'https://www.unraveledpress.com',rss:'https://www.unraveledpress.com/rss.xml',beatColor:'#555555'},
  {layer:'creator',name:'350 Chicago',channel:'350 Chicago',beat:'Environment / Climate',url:'https://350chicago.substack.com',rss:'https://350chicago.substack.com/feed',beatColor:'#3a7a00'},
  {layer:'creator',name:'Sixty Inches From Center',channel:'Sixty Inches From Center',beat:'Arts & Culture',url:'https://sixtyinchesfromcenter.org',rss:'https://sixtyinchesfromcenter.org/feed',beatColor:'#660066'},
  // Institutions — core civic newsrooms
  {layer:'institution',name:'Block Club Chicago',channel:'Block Club Chicago',beat:'City Hall & Neighborhoods',url:'https://blockclubchicago.org',rss:'https://blockclubchicago.org/feed',beatColor:'#0044cc'},
  {layer:'institution',name:'Injustice Watch',channel:'Injustice Watch',beat:'Criminal Justice',url:'https://injusticewatch.org',rss:'https://injusticewatch.org/feed/',beatColor:'#880000'},
  {layer:'institution',name:'Chalkbeat Chicago',channel:'Chalkbeat Chicago',beat:'Education / CPS',url:'https://chicago.chalkbeat.org',rss:'https://chicago.chalkbeat.org/rss/feed.xml',beatColor:'#880000'},
  {layer:'institution',name:'South Side Weekly',channel:'South Side Weekly',beat:'Black Chicago / Community',url:'https://southsideweekly.com',rss:'https://southsideweekly.com/feed',beatColor:'#884400'},
  {layer:'institution',name:'Illinois Answers Project',channel:'Illinois Answers Project',beat:'City Hall & Politics',url:'https://illinoisanswers.org',rss:'https://illinoisanswers.org/feed',beatColor:'#0044cc'},
  {layer:'institution',name:'Borderless Magazine',channel:'Borderless Magazine',beat:'Immigration / Latino',url:'https://borderlessmag.org',rss:'https://borderlessmag.org/feed',beatColor:'#005522'},
  {layer:'institution',name:'Chicago Reporter',channel:'Chicago Reporter',beat:'Race / Equity',url:'https://chicagoreporter.com',rss:'https://chicagoreporter.com/feed',beatColor:'#660022'},
  {layer:'institution',name:'Capitol News Illinois',channel:'Capitol News Illinois',beat:'City Hall & Politics / Statewide',url:'https://capitolnewsillinois.com',rss:'https://capitolnewsillinois.com/feed',beatColor:'#0044cc'},
  // Nonprofits — expanded
  {layer:'institution',name:'Evanston Roundtable',channel:'Evanston Roundtable',beat:'City Hall & Neighborhoods',url:'https://evanstonroundtable.com',rss:'https://evanstonroundtable.com/feed',beatColor:'#0044cc'},
  {layer:'institution',name:'In These Times',channel:'In These Times',beat:'Labor / Politics',url:'https://inthesetimes.com',rss:'https://inthesetimes.com/rss',beatColor:'#555500'},
  {layer:'institution',name:'Streetsblog Chicago',channel:'Streetsblog Chicago',beat:'City Hall & Neighborhoods',url:'https://chi.streetsblog.org',rss:'https://chi.streetsblog.org/feed',beatColor:'#0044cc'},
  {layer:'institution',name:'WBEZ 91.5 FM',channel:'WBEZ 91.5 FM',beat:'General News',url:'https://wbez.org',rss:'https://wbez.org/rss',beatColor:'#555555',volume:'high'},
  {layer:'institution',name:'Wednesday Journal',channel:'Wednesday Journal',beat:'City Hall & Neighborhoods',url:'https://wednesdayjournalonline.com',rss:'https://wednesdayjournalonline.com/feed',beatColor:'#0044cc'},
  {layer:'institution',name:'Capital B Gary',channel:'Capital B Gary',beat:'Black Chicago / Community',url:'https://capitalbnews.org/gary',rss:'https://capitalbnews.org/feed',beatColor:'#884400'},
  {layer:'institution',name:'PBS Chicago WTTW',channel:'PBS Chicago WTTW',beat:'General News',url:'https://wttw.com',rss:'https://news.wttw.com/rss.xml',beatColor:'#555555'},
  // Legacy broadcast & print
  {layer:'institution',name:'ABC 7 News Chicago',channel:'ABC 7 News Chicago',beat:'General News',url:'https://abc7chicago.com',rss:'https://abc7chicago.com/feed',beatColor:'#555555',volume:'high'},
  {layer:'institution',name:'Chicago Magazine',channel:'Chicago Magazine',beat:'Arts & Culture',url:'https://chicagomag.com',rss:'https://chicagomag.com/feed',beatColor:'#660066'},
  {layer:'institution',name:'Fox 32 Chicago',channel:'Fox 32 Chicago',beat:'General News',url:'https://fox32chicago.com',rss:'https://fox32chicago.com/rss.xml',beatColor:'#555555',volume:'high'},
  {layer:'institution',name:'NBC 5 News Chicago',channel:'NBC 5 News Chicago',beat:'General News',url:'https://nbcchicago.com',rss:'https://nbcchicago.com/feed',beatColor:'#555555',volume:'high'},
  {layer:'institution',name:'Telemundo Chicago',channel:'Telemundo Chicago',beat:'Immigration / Latino',url:'https://telemundochicago.com',rss:'https://telemundochicago.com/feed',beatColor:'#005522'},
  {layer:'institution',name:'WGN 9 TV',channel:'WGN 9 TV',beat:'General News',url:'https://wgntv.com',rss:'https://wgntv.com/feed',beatColor:'#555555',volume:'high'},
  {layer:'institution',name:'WGN 720 AM',channel:'WGN 720 AM',beat:'General News',url:'https://wgnradio.com',rss:'https://wgnradio.com/feed',beatColor:'#555555'},
  {layer:'institution',name:'Chicago Sun-Times',channel:'Chicago Sun-Times',beat:'General News',url:'https://chicago.suntimes.com',rss:'https://chicago.suntimes.com/rss/index.xml',beatColor:'#555555',volume:'high'},
  // Niche
  {layer:'institution',name:'Chicago Reader',channel:'Chicago Reader',beat:'Arts & Culture',url:'https://chicagoreader.com',rss:'https://chicagoreader.com/feed',beatColor:'#660066'},
  {layer:'institution',name:'Third Coast Review',channel:'Third Coast Review',beat:'Arts & Culture',url:'https://thirdcoastreview.com',rss:'https://thirdcoastreview.com/feed',beatColor:'#660066'},
  {layer:'institution',name:'Windy City Times',channel:'Windy City Times',beat:'LGBTQ+',url:'https://windycitytimes.com',rss:'https://windycitytimes.com/feed',beatColor:'#660066'},
  {layer:'institution',name:'Chicago Parent',channel:'Chicago Parent',beat:'General News',url:'https://chicagoparent.com',rss:'https://chicagoparent.com/rss.xml',beatColor:'#555555'},
  {layer:'institution',name:'Chicago Crusader',channel:'Chicago Crusader',beat:'Black Chicago',url:'https://chicagocrusader.com',rss:'https://chicagocrusader.com/feed',beatColor:'#884400'},
  {layer:'institution',name:'Negocios Now',channel:'Negocios Now',beat:'Business',url:'https://negociosnow.com',rss:'https://negociosnow.com/feed',beatColor:'#0066aa'},
  {layer:'institution',name:'Urbanize Chicago',channel:'Urbanize Chicago',beat:'City Hall & Neighborhoods',url:'https://chicago.urbanize.city',rss:'https://chicago.urbanize.city/rss.xml',beatColor:'#0044cc'},
  {layer:'institution',name:'Chicago Classical Review',channel:'Chicago Classical Review',beat:'Arts & Culture',url:'https://chicagoclassicalreview.com',rss:'https://chicagoclassicalreview.com/feed',beatColor:'#660066'},
  {layer:'institution',name:'La Raza',channel:'La Raza',beat:'Immigration / Latino',url:'https://laraza.com',rss:'https://laraza.com/feed',beatColor:'#005522'},
  {layer:'institution',name:'The Real Deal Chicago',channel:'The Real Deal Chicago',beat:'Business',url:'https://therealdeal.com/chicago',rss:'https://therealdeal.com/chicago/feed',beatColor:'#0066aa'},
  {layer:'institution',name:'Crib Chatter',channel:'Crib Chatter',beat:'Business',url:'https://cribchatter.com',rss:'https://cribchatter.com/feed',beatColor:'#0066aa'},
  {layer:'institution',name:'Eater Chicago',channel:'Eater Chicago',beat:'Arts & Culture',url:'https://chicago.eater.com',rss:'https://chicago.eater.com/rss/index.xml',beatColor:'#660066'},
  // Student media
  {layer:'institution',name:'The Chicago Maroon',channel:'The Chicago Maroon',beat:'General News',url:'https://chicagomaroon.com',rss:'https://chicagomaroon.com/feed',beatColor:'#555555'},
  {layer:'institution',name:'The Daily Northwestern',channel:'The Daily Northwestern',beat:'General News',url:'https://dailynorthwestern.com',rss:'https://dailynorthwestern.com/feed',beatColor:'#555555'},
  {layer:'institution',name:'The DePaulia',channel:'The DePaulia',beat:'General News',url:'https://depauliaonline.com',rss:'https://depauliaonline.com/feed',beatColor:'#555555'},
  {layer:'institution',name:'The Loyola Phoenix',channel:'The Loyola Phoenix',beat:'General News',url:'https://loyolaphoenix.com',rss:'https://loyolaphoenix.com/feed',beatColor:'#555555'},
];

// ── CONFIG ───────────────────────────────────────────────────────────────────
const ITEMS_PER_FEED = 3;
const TIMEOUT_MS = 10000;
const CONCURRENCY = 8; // parallel fetches
const OUTPUT_PATH = 'data/chicago-pulse.json';

// ── FETCH + PARSE ────────────────────────────────────────────────────────────
async function fetchFeed(feed) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(feed.rss, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; AtlasBot/1.0; +https://journalismatlas.com)',
        'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*',
      },
    });
    clearTimeout(timer);
    if (!res.ok) return { feed, items: [], error: `HTTP ${res.status}` };
    const xml = await res.text();
    const items = parseXML(xml, feed);
    return { feed, items, error: null };
  } catch (err) {
    clearTimeout(timer);
    return { feed, items: [], error: err.name === 'AbortError' ? 'timeout' : err.message };
  }
}

function extractTag(xml, tag) {
  const re = new RegExp(`<${tag}[^>]*>(?:<!\\[CDATA\\[)?([\\s\\S]*?)(?:\\]\\]>)?<\\/${tag}>`, 'i');
  const m = xml.match(re);
  return m ? m[1].trim() : '';
}

function extractAttr(xml, tag, attr) {
  const re = new RegExp(`<${tag}[^>]*\\s${attr}="([^"]*)"`, 'i');
  const m = xml.match(re);
  return m ? m[1].trim() : '';
}

function parseXML(xml, feed) {
  const items = [];
  // RSS <item>
  const itemRe = /<item[\s>]([\s\S]*?)<\/item>/gi;
  let m;
  while ((m = itemRe.exec(xml)) !== null && items.length < ITEMS_PER_FEED) {
    const chunk = m[1];
    const title = extractTag(chunk, 'title');
    const link = extractTag(chunk, 'link') || extractAttr(chunk, 'link', 'href') || feed.url;
    const pubDate = extractTag(chunk, 'pubDate') || extractTag(chunk, 'dc:date') || '';
    if (title) items.push({ title, link, pubDate });
  }
  // Atom <entry> fallback
  if (!items.length) {
    const entryRe = /<entry[\s>]([\s\S]*?)<\/entry>/gi;
    while ((m = entryRe.exec(xml)) !== null && items.length < ITEMS_PER_FEED) {
      const chunk = m[1];
      const title = extractTag(chunk, 'title');
      const link = extractAttr(chunk, 'link', 'href') || extractTag(chunk, 'link') || feed.url;
      const pubDate = extractTag(chunk, 'published') || extractTag(chunk, 'updated') || '';
      if (title) items.push({ title, link, pubDate });
    }
  }
  return items;
}

// ── CONCURRENCY POOL ─────────────────────────────────────────────────────────
async function fetchAll(feeds, concurrency) {
  const results = [];
  let idx = 0;
  async function worker() {
    while (idx < feeds.length) {
      const i = idx++;
      results[i] = await fetchFeed(feeds[i]);
    }
  }
  await Promise.all(Array.from({ length: concurrency }, worker));
  return results;
}

// ── MAIN ─────────────────────────────────────────────────────────────────────
async function main() {
  const startTime = Date.now();
  console.log(`\nAtlas Chicago Pulse — fetching ${FEEDS.length} feeds...\n`);

  mkdirSync('data', { recursive: true });

  const results = await fetchAll(FEEDS, CONCURRENCY);

  // Build output
  const items = [];
  const ok = [], failed = [];

  for (const { feed, items: feedItems, error } of results) {
    if (feedItems.length) {
      ok.push(feed.name);
      for (const item of feedItems) {
        items.push({
          // Feed metadata (pass-through for renderer)
          layer: feed.layer,
          name: feed.name,
          channel: feed.channel,
          beat: feed.beat,
          url: feed.url,
          beatColor: feed.beatColor,
          ...(feed.volume ? { volume: feed.volume } : {}),
          // Item data
          title: item.title,
          link: item.link,
          pubDate: item.pubDate || null,
        });
      }
    } else {
      failed.push({ name: feed.name, rss: feed.rss, error: error || 'empty feed' });
    }
  }

  // Sort by pubDate descending (renderer will re-group by beat)
  items.sort((a, b) => {
    if (!a.pubDate && !b.pubDate) return 0;
    if (!a.pubDate) return 1;
    if (!b.pubDate) return -1;
    return new Date(b.pubDate) - new Date(a.pubDate);
  });

  const output = {
    generated: new Date().toISOString(),
    source_count: ok.length,
    item_count: items.length,
    items,
    failed, // kept for visibility — not rendered on page
  };

  writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2));

  // ── SUMMARY ─────────────────────────────────────────────────────────────────
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log(`✅  ${ok.length} sources / ${items.length} stories → ${OUTPUT_PATH}`);
  console.log(`⏱   ${elapsed}s\n`);

  if (failed.length) {
    console.log(`❌  ${failed.length} feeds failed:`);
    for (const f of failed) {
      console.log(`    ${f.name.padEnd(35)} ${f.error}`);
    }
    console.log('');
  }

  // Beat breakdown
  const beats = {};
  items.forEach(i => { beats[i.beat] = (beats[i.beat] || 0) + 1; });
  console.log('Beat breakdown:');
  Object.entries(beats).sort((a, b) => b[1] - a[1]).forEach(([b, c]) => {
    console.log(`  ${b.padEnd(40)} ${c}`);
  });
  console.log('');
}

main().catch(err => { console.error(err); process.exit(1); });
