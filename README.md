<div align="center">

# Scavio Agent Skills

**Give your AI agent live data from 50 platforms as structured JSON, through one API key**

[![Platforms](https://img.shields.io/badge/Platforms-50-blue?style=flat-square)](https://scavio.dev)
[![Endpoints](https://img.shields.io/badge/Endpoints-298-green?style=flat-square)](https://scavio.dev/docs)
[![Skills](https://img.shields.io/badge/Skills-51-orange?style=flat-square)](#skills)
[![skills.sh](https://img.shields.io/badge/skills.sh-listed-black?style=flat-square)](https://skills.sh/scavio-ai/skills)
[![Agents](https://img.shields.io/badge/Agents-40+-blueviolet?style=flat-square)](https://skills.sh)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[Overview](#overview) | [Install](#install) | [Setup](#setup) | [Skills](#skills) | [Which skill](#which-skill-do-i-want) | [Links](#links)

</div>

---

## Overview

[Scavio](https://scavio.dev) is a unified web data API: one key, 50 platforms, structured JSON instead of HTML. This repo holds 51 Agent Skills: one per platform, plus `scavio`, an umbrella that covers all 50 from a single install. A skill teaches your agent which Scavio endpoints exist for a platform, what parameters they take, what the response looks like, and what each call costs in credits, so the agent can call the API correctly without you writing an integration. Every skill is in the open Agent Skills format and loads in Claude Code, Cursor, Codex, OpenCode, Goose, OpenHands, Hermes Agent, OpenClaw, and any other client that reads the format.

## Install

One skill for everything:

```
npx skills add scavio-ai/skills --skill scavio
```

Or one skill per platform, picking the ones you use:

```
npx skills add scavio-ai/skills --skill amazon-product-data --skill google-search-api
```

Without `--skill` the CLI opens a picker; `--all` installs every skill into every agent it detects. To see what is in the repo before installing anything:

```
npx skills add scavio-ai/skills --list
```

To install straight into a specific agent, pass `-a`:

```
npx skills add scavio-ai/skills --skill scavio -a claude-code -a opencode
```

Any client that reads the Agent Skills format can also load a folder directly. Clone this repo and point the client at the repo root, or copy a single skill directory into wherever that client keeps its skills.

### Umbrella or per-platform

`scavio` is one `SKILL.md` that routes to a `references/` file per platform. Your agent carries one description in its context instead of fifty, and the platform detail loads only when a platform is used. The per-platform skills are the same content split up: each one is a fifth of what the umbrella loads per call, and each has its own trigger, so they fit a project that uses two or three platforms. Install one or the other, not both.

Hermes Agent caps a community skill at 50 files and the umbrella ships 51, so on Hermes install the per-platform skills instead; every one of them passes the Hermes scan.

## Setup

The skills need one environment variable:

```
export SCAVIO_API_KEY=...
```

Get the key at [scavio.dev](https://scavio.dev). The free tier is 50 credits on signup, no card required.

## Skills

### Search

| Skill | What it does |
| --- | --- |
| `google-search-api` | Full Google SERP as JSON: organic, ads, knowledge graph, AI Overview, PAA |
| `google-ai-mode-api` | Google AI Mode answers with their cited sources |
| `google-news-api` | Headlines by keyword, topic, story or publication |
| `google-trends-api` | Search interest over time, by region, and related queries |
| `google-maps-api` | Local business search, place detail, reviews, and a local-SEO geo-grid |

### Commerce

| Skill | What it does |
| --- | --- |
| `amazon-product-data` | Keyword search, ASIN detail, and all seller offers with the buy box |
| `ebay-product-data` | Live and sold listings for comps, plus listing and seller detail |
| `walmart-product-data` | Search, item detail, reviews, categories, offers, and seller storefronts |
| `target-product-data` | Search, category browse, TCIN detail, and reviews with store-aware pricing |
| `home-depot-product-data` | Search with per-store pickup and delivery, item specs, and reviews |
| `google-shopping-api` | Product search with price filters, product detail, and every store selling it |
| `aliexpress-product-data` | Search, category browse, product with every SKU variant, translated reviews, and seller storefronts |
| `etsy-product-data` | Listing search, listing detail with variations and reviews, shop profiles and shop reviews |
| `tiktok-shop-api` | Catalog search, product detail, reviews, categories, and shop catalogs |

### Social and video

| Skill | What it does |
| --- | --- |
| `instagram-scraper-api` | Profiles, posts, reels, stories, comments, followers, and search |
| `tiktok-scraper-api` | Profiles, user videos, video detail, comments, hashtags, and search |
| `youtube-data-api` | Video and channel search, metadata, comments, transcripts, and streams |
| `twitter-scraper-api` | Tweet and people search, tweet detail, profiles, followers, and trends |
| `reddit-search-api` | Search, post detail, threaded comments, subreddits, and redditor profiles |
| `linkedin-scraper-api` | Person and company profiles, their posts, job search, and job detail |
| `facebook-scraper-api` | Page profile, posts, reels and photos, post comments, groups, events, and hashtag posts |
| `threads-net-api` | Threads profiles, posts, replies, post detail, and people search |
| `pinterest-api` | Pin search, pin detail with save counts, user profiles, boards, and URL save counts |
| `twitch-api` | Channel profile and live status, VODs, stream schedule, and clip download URLs |
| `douyin-scraper-api` | Videos, profiles, feeds, comments, hashtags, music, live rooms, hot search, and keyword search |
| `weibo-scraper-api` | Profiles, posts, comments, keyword search, hot-search and ranking boards, and channel feeds |
| `kuaishou-scraper-api` | Kuaishou.com profiles, videos, comments, hashtags, and search |

### Travel

| Skill | What it does |
| --- | --- |
| `airbnb-scraper-api` | Stay search with the discount ledger, listing detail, and guest reviews |
| `booking-com-hotel-data` | Destination search with live nightly prices, property detail, and reviews |
| `google-hotels-api` | Hotel search for a stay, plus per-property booking-site vendor prices |
| `google-flights-api` | Route search by date with price, carrier, duration, and stops |
| `tripadvisor-reviews-api` | Resolve places, list ranked venues in a geo, location detail, and reviews |

### Jobs and reviews

| Skill | What it does |
| --- | --- |
| `indeed-jobs-api` | Job search, full posting detail with the ATS link, employers, and reviews |
| `glassdoor-salary-data` | Salary percentiles by title, employer profiles, ratings, and reviews |
| `g2-software-reviews-api` | B2B product search, profiles with pricing editions, and faceted reviews |
| `capterra-reviews-api` | Software search, full profiles with the pricing table, and scored reviews |
| `yelp-business-data` | Business search, full business detail with hours, and review pages |

### Real estate

| Skill | What it does |
| --- | --- |
| `zillow-property-data` | For sale, rent and sold listings, property detail, Zestimate, agent profiles |
| `redfin-property-data` | Listing search, property detail with Redfin Estimate, and market stats |

### App stores

| Skill | What it does |
| --- | --- |
| `apple-app-store-api` | App search, listing detail by App Store or bundle id, and user reviews |
| `google-play-store-api` | Android app search, listing with install counts and Data safety, reviews |

### Companies and code

| Skill | What it does |
| --- | --- |
| `sec-edgar-api` | Ticker to CIK, filer profile, filings with documents, XBRL, full-text search |
| `companies-house-api` | UK company search, register entry, officers, and filing history PDFs |
| `github-api` | Profiles, repos, READMEs, releases, issues, search, and repo dossier and velocity composites |

### Ads

| Skill | What it does |
| --- | --- |
| `google-ads-transparency-api` | Advertiser lookup and the live ad creatives a brand runs, with dates |
| `meta-ad-library-api` | Facebook and Instagram ad search by keyword, Page id, or archive id |
| `tiktok-ad-library-api` | Ad search by keyword or industry, top-performing ads, and single-ad detail with video |
| `linkedin-ad-library-api` | Ad search by keyword or advertiser, and single-ad detail with media and payer |

### Utility

| Skill | What it does |
| --- | --- |
| `url-to-markdown-api` | Any URL to clean Markdown, plain text, or raw HTML for prompts and RAG |
| `website-screenshot-api` | Full-page PNG of any public URL as an inline base64 image |

### Umbrella

| Skill | What it does |
| --- | --- |
| `scavio` | All 50 platforms behind one trigger: routing table, shared setup, request format, cost gate, and failure handling, with a reference file per platform |

## Which skill do I want

**I need prices for a product across retailers.** Start with `google-shopping-api` for the cross-merchant view, then go per retailer: `amazon-product-data` for ASIN detail and offers, `walmart-product-data`, `target-product-data`, `home-depot-product-data`, `aliexpress-product-data`. For resale and used comps, `ebay-product-data` searches sold listings. For handmade and vintage, `etsy-product-data`.

**I need a lead list of local businesses.** `google-maps-api` gives places, addresses, phone numbers, hours, and coordinates for a query and map center. `yelp-business-data` adds price band, amenities, and review text for the same kind of venue. `tripadvisor-reviews-api` covers restaurants, hotels, and attractions ranked within a geo.

**I need to feed a RAG index or an LLM prompt.** `url-to-markdown-api` converts arbitrary pages to Markdown chunks. For discussion text, `reddit-search-api` returns threaded comments. For video, `youtube-data-api` returns transcripts. For code and issues, `github-api` returns READMEs, releases, and issue threads.

**I need to see what a competitor is doing.** `google-ads-transparency-api`, `meta-ad-library-api`, `tiktok-ad-library-api` and `linkedin-ad-library-api` return the ad creatives a brand is running and when they ran. `g2-software-reviews-api` and `capterra-reviews-api` return their pricing tables and review facets. `glassdoor-salary-data` and `indeed-jobs-api` return what they pay and what they are hiring for.

**I need one install that covers everything.** `scavio`.

## Links

- Docs: [scavio.dev/docs](https://scavio.dev/docs)
- Hosted MCP server: [mcp.scavio.dev](https://mcp.scavio.dev)
- Python SDK: `pip install scavio`
- JavaScript SDK: `npm i scavio`

## Regenerating

`skills/` is generated from `../openclaw/`, the single source of truth shared with ClawHub.
Do not hand-edit it. Edit the source skill, then:

```
python3 build.py       # regenerate skills/, including the scavio umbrella
python3 verify.py      # prove nothing but naming, H1 and UTM changed
python3 build.py --check   # exits 1 if skills/ is stale
```

The umbrella is generated too: `umbrella.md` is its router template, the platform table
comes from `naming.json`, and every `skills/scavio/references/<slug>.md` is the body of the
matching per-platform skill, byte for byte.

`verify.py` asserts the technical body is byte-identical to the source, the umbrella
references are byte-identical to the generated skills, the frontmatter parses as YAML, names
are unique, every prose link carries a UTM, every skill is listed in this README, no example
reads an environment key, and every install is version-pinned.
