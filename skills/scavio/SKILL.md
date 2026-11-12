---
name: scavio
description: "Scavio web data API: one key, structured JSON from 78 platforms. Google Search, AI Mode, News, Trends, Maps, Shopping, Hotels, Flights, Play Store and Ads Transparency; ChatGPT and Gemini answers; Amazon, eBay, Walmart, Target, Home Depot, Lowe's, Costco, Sam's Club, Kroger, H-E-B, ALDI, Whole Foods Market, Dollar General, Walgreens, CVS, iHerb, Sephora, Ulta Beauty, Nordstrom, PetSmart, Petco, Chewy, Micro Center, Harbor Freight, Menards, Canadian Tire, Decathlon, Spec's, Mercado Libre, AliExpress, Etsy and TikTok Shop; Instagram, TikTok, YouTube, Twitter/X, Reddit, LinkedIn, Facebook, Threads, Pinterest, Twitch, Douyin, Weibo and Kuaishou; Airbnb, Booking.com and Tripadvisor; Indeed, Glassdoor, G2, Capterra, Trustpilot and Yelp; Zillow, Redfin, Realtor.com and Rightmove; Apple App Store; SEC EDGAR, Companies House and GitHub; the Meta, TikTok and LinkedIn ad libraries; URL to Markdown, website crawling and website screenshots. Routes each request to the platform reference, quotes the credit cost before a paid call, and handles 402 and 429. Use when the user wants public data from any of these sites, code that calls Scavio, or a cost estimate."
version: 1.0.0
tags: scavio, web-data-api, scraper-api, serp-api, social-media-api, ecommerce-api, google-search, amazon, instagram, tiktok, youtube, linkedin, reddit, structured-data, json, ai-agents, langchain, crewai, autogen
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F310"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=scavio
---

# Scavio - One API Key for 78 Web Data Platforms

Scavio returns public pages from 78 platforms as structured JSON through one API key. This file is the router. It says which platform reference to read, how every request is shaped, what a call costs, and what to do when one fails. The files under `references/` hold the endpoints, parameters, measured response shapes and the traps for each platform. Open the reference before the first call to a platform in a session, and call from the reference, not from memory.

## When to trigger

Use this skill when the user asks to:
- Pull public data from any platform in the table below: profiles, posts, comments, products, prices, reviews, listings, jobs, salaries, filings, ads, search results, transcripts
- Write code that calls the Scavio API in any language
- Estimate what a data job will cost in credits, or check their balance
- Turn an arbitrary URL into Markdown or a screenshot, or crawl a whole site, its sitemap or a URL list to Markdown

Do not use it for a site that is not in the table. For an arbitrary page, `references/url-to-markdown-api.md` and `references/website-screenshot-api.md` are the fallbacks; for many pages of any site, `references/website-crawler-api.md`.

## Platforms

Each row is one reference file. Open it before the first call to that platform. Endpoint counts and credits are per call unless the row says otherwise; the reference has the exact table.

**Search**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| ChatGPT | [chatgpt-scraper-api](references/chatgpt-scraper-api.md) | 1 | 2 |
| Gemini | [gemini-scraper-api](references/gemini-scraper-api.md) | 1 | 5 |
| Google AI Mode | [google-ai-mode-api](references/google-ai-mode-api.md) | 1 | 1 |
| Google Maps | [google-maps-api](references/google-maps-api.md) | 4 | 1; geo-grid bills per point |
| Google News | [google-news-api](references/google-news-api.md) | 1 | 1 |
| Google Search | [google-search-api](references/google-search-api.md) | 2 | 1 |
| Google Trends | [google-trends-api](references/google-trends-api.md) | 2 | 1 |

**Commerce**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| ALDI | [aldi-grocery-data](references/aldi-grocery-data.md) | 3 | 1 |
| AliExpress | [aliexpress-product-data](references/aliexpress-product-data.md) | 6 | 1 |
| Amazon | [amazon-product-data](references/amazon-product-data.md) | 3 | 1 |
| Best Buy | [best-buy-product-data](references/best-buy-product-data.md) | 9 | 2; stores and suggestions 1, deals and pcmcat category pages 3 |
| Canadian Tire | [canadian-tire-api](references/canadian-tire-api.md) | 6 | 1 |
| Carrefour | [carrefour-api](references/carrefour-api.md) | 9 | 1; Belgium search and product 2 |
| Chewy | [chewy-product-data](references/chewy-product-data.md) | 2 | 10 |
| Costco | [costco-product-data](references/costco-product-data.md) | 13 | 1; US search, category, deals and clearance 2; multi-warehouse prices, stock and gas scale with warehouse count |
| CVS | [cvs-product-data](references/cvs-product-data.md) | 3 | 1 |
| Decathlon | [decathlon-product-data](references/decathlon-product-data.md) | 2 | 2 |
| Dick's Sporting Goods | [dicks-sporting-goods-api](references/dicks-sporting-goods-api.md) | 9 | 1; product, reviews 2 |
| Dollar General | [dollar-general-api](references/dollar-general-api.md) | 5 | 1 |
| eBay | [ebay-product-data](references/ebay-product-data.md) | 3 | 1 |
| Etsy | [etsy-product-data](references/etsy-product-data.md) | 5 | 2 |
| Fanatics | [fanatics-merchandise-api](references/fanatics-merchandise-api.md) | 5 | 1 |
| Foot Locker | [foot-locker-api](references/foot-locker-api.md) | 10 | 1 |
| Google Shopping | [google-shopping-api](references/google-shopping-api.md) | 3 | 1 |
| Harbor Freight | [harbor-freight-api](references/harbor-freight-api.md) | 7 | 1 |
| HEB | [heb-grocery-data](references/heb-grocery-data.md) | 3 | 2 |
| Home Depot | [home-depot-product-data](references/home-depot-product-data.md) | 3 | 2 |
| iHerb | [iherb-product-data](references/iherb-product-data.md) | 4 | 2 |
| JCPenney | [jcpenney-product-data](references/jcpenney-product-data.md) | 11 | 1 |
| Kohl's | [kohls-product-data](references/kohls-product-data.md) | 9 | 2; stores 1 |
| Kroger | [kroger-grocery-data](references/kroger-grocery-data.md) | 2 | 2 |
| Lowe's | [lowes-product-data](references/lowes-product-data.md) | 4 | 2; reviews 1 |
| Macy's | [macys-product-data](references/macys-product-data.md) | 9 | 1 |
| Menards | [menards-product-data](references/menards-product-data.md) | 3 | search 2; product 1, 2 with store_id; stores 1 |
| Mercado Libre | [mercadolibre-product-data](references/mercadolibre-product-data.md) | 5 | 2; reviews 1 |
| Micro Center | [micro-center-api](references/micro-center-api.md) | 3 | 2; stores 1 |
| Nordstrom | [nordstrom-product-data](references/nordstrom-product-data.md) | 8 | 5; availability and reviews 10 |
| Nordstrom Rack | [nordstrom-rack-product-data](references/nordstrom-rack-product-data.md) | 8 | 5; availability and reviews 10 |
| Petco | [petco-product-data](references/petco-product-data.md) | 5 | 1 |
| PetSmart | [petsmart-product-data](references/petsmart-product-data.md) | 6 | 1 |
| Saks Fifth Avenue | [saks-fifth-avenue-api](references/saks-fifth-avenue-api.md) | 9 | 2 |
| Sam's Club | [sams-club-product-data](references/sams-club-product-data.md) | 6 | 1 |
| Sephora | [sephora-product-data](references/sephora-product-data.md) | 3 | 1 |
| Spec's | [specs-liquor-prices](references/specs-liquor-prices.md) | 3 | 5 |
| Target | [target-product-data](references/target-product-data.md) | 5 | 1 |
| TCGplayer | [tcgplayer-api](references/tcgplayer-api.md) | 13 | 1 |
| TikTok Shop | [tiktok-shop-api](references/tiktok-shop-api.md) | 8 | 1 |
| Ulta Beauty | [ulta-beauty-api](references/ulta-beauty-api.md) | 4 | 1 |
| Vinted | [vinted-api](references/vinted-api.md) | 9 | 1 |
| Walgreens | [walgreens-product-data](references/walgreens-product-data.md) | 4 | 2; stock 4 |
| Walmart | [walmart-product-data](references/walmart-product-data.md) | 8 | 1; 2 for walmart.com.mx search/category or store-targeted search/product |
| Whole Foods Market | [whole-foods-grocery-data](references/whole-foods-grocery-data.md) | 7 | 1 |

**Social and video**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Douyin | [douyin-scraper-api](references/douyin-scraper-api.md) | 27 | 1; search 10 |
| Facebook | [facebook-scraper-api](references/facebook-scraper-api.md) | 11 | 1 |
| Instagram | [instagram-scraper-api](references/instagram-scraper-api.md) | 20 | 1-2 |
| Kuaishou | [kuaishou-scraper-api](references/kuaishou-scraper-api.md) | 14 | 1, 2, 10 or 40 |
| LinkedIn | [linkedin-scraper-api](references/linkedin-scraper-api.md) | 9 | 1-30 |
| Pinterest | [pinterest-api](references/pinterest-api.md) | 6 | 1; url-stats 1-2 |
| Reddit | [reddit-search-api](references/reddit-search-api.md) | 14 | 1 |
| Threads | [threads-net-api](references/threads-net-api.md) | 6 | 2 by user_id, 4 by username |
| TikTok | [tiktok-scraper-api](references/tiktok-scraper-api.md) | 24 | 1 |
| Twitch | [twitch-api](references/twitch-api.md) | 4 | 1 |
| Twitter/X | [twitter-scraper-api](references/twitter-scraper-api.md) | 14 | 1 |
| Weibo | [weibo-scraper-api](references/weibo-scraper-api.md) | 30 | 1 |
| YouTube | [youtube-data-api](references/youtube-data-api.md) | 17 | 1-5 |

**Travel**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Airbnb | [airbnb-scraper-api](references/airbnb-scraper-api.md) | 3 | 1 |
| Booking.com | [booking-com-hotel-data](references/booking-com-hotel-data.md) | 3 | 1 |
| Google Flights | [google-flights-api](references/google-flights-api.md) | 1 | 1 |
| Google Hotels | [google-hotels-api](references/google-hotels-api.md) | 2 | 1 |
| Tripadvisor | [tripadvisor-reviews-api](references/tripadvisor-reviews-api.md) | 4 | 2 |

**Jobs and reviews**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Capterra | [capterra-reviews-api](references/capterra-reviews-api.md) | 3 | 2 |
| G2 | [g2-software-reviews-api](references/g2-software-reviews-api.md) | 3 | 5 |
| Glassdoor | [glassdoor-salary-data](references/glassdoor-salary-data.md) | 4 | 2 |
| Indeed | [indeed-jobs-api](references/indeed-jobs-api.md) | 4 | 2 |
| Trustpilot | [trustpilot-reviews-api](references/trustpilot-reviews-api.md) | 6 | 2 |
| Yelp | [yelp-business-data](references/yelp-business-data.md) | 3 | 2 |

**Real estate**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Realtor.com | [realtor-com-property-data](references/realtor-com-property-data.md) | 6 | 1 |
| Redfin | [redfin-property-data](references/redfin-property-data.md) | 3 | 1 |
| Rightmove | [rightmove-property-data](references/rightmove-property-data.md) | 7 | 1 |
| Zillow | [zillow-property-data](references/zillow-property-data.md) | 3 | 1 |

**App stores**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Apple App Store | [apple-app-store-api](references/apple-app-store-api.md) | 3 | 1 |
| Google Play | [google-play-store-api](references/google-play-store-api.md) | 3 | 2 |

**Companies and code**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Companies House | [companies-house-api](references/companies-house-api.md) | 4 | 1 |
| GitHub | [github-api](references/github-api.md) | 13 | 1; dossier and top-issues 5, profile-velocity 10, user/email 2 |
| SEC EDGAR | [sec-edgar-api](references/sec-edgar-api.md) | 6 | 1 |

**Ads**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Google Ads Transparency | [google-ads-transparency-api](references/google-ads-transparency-api.md) | 3 | 1 |
| LinkedIn Ad Library | [linkedin-ad-library-api](references/linkedin-ad-library-api.md) | 2 | 6 |
| Meta Ad Library | [meta-ad-library-api](references/meta-ad-library-api.md) | 3 | 1 per page |
| TikTok Ad Library | [tiktok-ad-library-api](references/tiktok-ad-library-api.md) | 3 | 1 |

**Utility**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| URL to Markdown | [url-to-markdown-api](references/url-to-markdown-api.md) | 1 | 1; ultra 2 |
| Website Crawler | [website-crawler-api](references/website-crawler-api.md) | 7 | map 1; 1 per page, ultra 2 |
| Website Screenshot | [website-screenshot-api](references/website-screenshot-api.md) | 1 | 1; ultra 5 |

## Setup

Every call reads the key from `SCAVIO_API_KEY`. The quickest way to get one (Node.js 18+) is to sign in from the terminal; it saves the key to the shell profile without printing it:

```bash
npx -y scavio@0.39.2 login
```

Or create a free account at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=scavio) (50 free credits, no card required), copy the key from the dashboard and export it yourself:

```bash
export SCAVIO_API_KEY=sk_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every call. Sign the user in instead of asking for a key:

1. Run `npx -y scavio@0.39.2 login`. It prints a link and a code, and opens the browser when it can. Show the user both and ask them to open the link, sign in or create a free account, check that the page shows the same code, and click Approve.
2. Run `npx -y scavio@0.39.2 login --wait`. Exit 0 means the key is saved; exit 2 means not approved yet, so run it again (each run waits up to 60 seconds); exit 3 means the user denied it; exit 1 means the code expired or failed, so start again.
3. The key is in the user's shell profile, not in your current shell. `npx -y scavio@0.39.2 status` confirms it works. Tell the user to restart the agent so `SCAVIO_API_KEY` is loaded.
4. A new account starts with 50 credits. Most endpoints cost 1 credit; the Platforms table and each reference say where that differs.

If Node.js is not available, send the user to [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=scavio) to copy the key (created automatically at signup) and add it to their shell profile themselves.

Never print, log or paste the key, and never read the shell profile or `~/.config/scavio/credentials.json`. Keep `$SCAVIO_API_KEY` as a variable reference in every example and command. Never ask the user to paste the key into the chat.

## Cross-platform ad search

Three endpoints query the Meta, TikTok, LinkedIn and Google ad libraries in one call and merge the results. Use them when the user wants a brand's or a keyword's ads across platforms; for one platform, use that platform's reference instead.

| Endpoint | Body | Returns in `data` |
|---|---|---|
| `POST /api/v1/ads/search` | `query` (required), `platforms`, `country`, `limit` | `query`, `total`, `platforms` (per-platform `status` and `count`), `ads` |
| `POST /api/v1/ads/advertisers` | `brand` (required), `platforms`, `country` | `brand`, `resolutions` (per platform: `status`, `chosen`, ranked `candidates` with `id`, `confidence`) |
| `POST /api/v1/ads/dossier` | `brand` (required), `platforms`, `country`, `limit`, optional `meta_page_id`, `linkedin_company_id`, `google_advertiser_id` | `brand`, `resolved`, `summary` (`total_ads`, `platforms_active`, `by_platform`, `date_range`), `platforms`, `ads` |

- `platforms` is any of `meta`, `tiktok`, `linkedin`, `google` (default all four). `country` is ISO2, default `US`. `limit` is ads kept per platform, default 30, max 100.
- Each ad in `ads` has the same shape on every platform: `platform`, `ad_id`, `advertiser` (`name`, `id`, `profile_url`, `domain`), `creative` (`type`, `headline`, `body`, `cta`, `media_urls`), `landing_page`, `first_seen`, `last_seen`, `regions`, `metrics`, `is_active`, `detail_url`.
- Cost is per platform that answers: meta 1, tiktok 1, google 1-2, linkedin 6 (a dossier can spend up to 2 on Meta). A platform that errors is not billed. All four platforms: up to 10 credits for a search, 9 to resolve advertisers, 11 for a dossier. Narrow `platforms` when the user only needs some.
- If the dossier picked the wrong advertiser, call `/api/v1/ads/advertisers`, pick the right `id` from `candidates`, and pass it as `meta_page_id`, `linkedin_company_id` or `google_advertiser_id`.

## Request format

- Base URL `https://api.scavio.dev`. Most endpoints are `POST /api/v1/<platform>/<resource>`; the Google verticals built on the v2 engine are `POST /api/v2/...`. The reference gives the exact path, so copy it from there.
- Every request is a `POST` with a JSON body and the header `Authorization: Bearer $SCAVIO_API_KEY`.
- Every successful response is the envelope `{ data, response_time, credits_used, credits_remaining }`. A top-level `warnings` array appears only when the request carried a retired parameter.
- Unknown parameters are ignored, not rejected. A `200` does not prove a parameter was honoured; check the response against what was asked.
- A parameter sent as an empty string is treated as omitted.
- `GET /api/v1/usage` with the same header returns `plan`, `credit_balance`, `purchased_credits` and `searches_used`, and costs nothing.

```bash
curl -s -X POST https://api.scavio.dev/api/v1/reddit/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "best mechanical keyboard"}'
```

## Cost gate

Run this before every paid call. Costs in the references are per call; a loop over pages, ids or hashtags multiplies them.

```text
Cost check
Endpoint: POST /api/v1/<platform>/<resource>
Unit: N credits per call (from the reference)
Calls: how many, and why (pages x items, one per id, ...)
Total: unit x calls
Balance: credits_remaining from the last response, or GET /api/v1/usage -> balance after this job
```

Rules:
- Prefer the cheapest endpoint that fully answers the question. Do not fetch extra pages, replies, transcripts, followers or detail rows the user did not ask for.
- If the user already asked to run this exact request, the cost line is enough; do not add a redundant confirmation. Ask before widening the paid scope.
- After the call, report `credits_used` and `credits_remaining` from the response, not the estimate.
- Billing happens when a request is answered. A `400`, `401`, `402` or `429` is never billed, and neither is a `502` or `503`. Some `404` answers are billed because the lookup did complete; each reference says which. There are no refunds, so never retry in a tight loop.

Plans, for sizing a job:

| Plan | Price | Credits | Concurrent requests |
|---|---|---|---|
| Free | $0 | 50 one-time | 1 |
| Pay As You Go | $0.01 per credit, 2,500 minimum | as purchased | 1 |
| Hobby | $15/mo ($12/mo yearly) | 3,000/mo | 1 |
| Project | $30/mo ($24/mo yearly) | 10,000/mo | 5 |
| Bootstrap | $100/mo ($79/mo yearly) | 50,000/mo | 10 |
| Startup | $250/mo ($199/mo yearly) | 150,000/mo | 15 |
| Growth | $500/mo ($399/mo yearly) | 500,000/mo | 50 |

## Failure handling

- `400` - an invalid or missing parameter. Re-read the reference and fix the body; nothing was billed.
- `401` - the API key is missing or invalid. Check `SCAVIO_API_KEY`.
- `402` - out of credits. The body carries `credit_balance`, a `message` and `billing_url`. Stop, report the balance and the link; the same key keeps working after a top-up.
- `404` - the platform had nothing for that id. Normal on some endpoints (the reference says which) and sometimes billed. Skip the item; do not retry it.
- `410` - the endpoint was retired. Do not retry; the reference names the replacement if there is one.
- `429` - too many requests in flight for the plan. Scavio limits concurrency, not requests per minute. The body carries `plan`, `concurrency`, `in_flight`, `retry_after` and `docs_url`, and the response sets `Retry-After: 1`. Wait for an in-flight request to finish, retry, and cap the worker pool at the plan's concurrency. Nothing was billed.
- `502` / `503` - the platform is temporarily unavailable. Wait a few seconds and retry slowly; the request already spent an internal retry budget. Nothing was billed.
- If the response has no `data` key, branch on the status code, never on a field inside `data`.

## Workflow

1. Identify the platform and the resource the user wants.
2. Open that platform's reference and pick the cheapest endpoint that answers.
3. Resolve `SCAVIO_API_KEY`. If it is not set, stop and tell the user how to set it.
4. Show the cost gate.
5. Call the endpoint exactly as the reference shows it, then report the data with `credits_used` and `credits_remaining`.

Multi-platform requests: open each reference, then run the calls sequentially or with at most the plan's concurrency in flight. Retail price comparisons start with Google Shopping for the cross-merchant view, then go per retailer. Ambiguous platform ("get the profile for nike"): ask which platform before spending.

## Other ways to call Scavio

- Python and JavaScript SDKs: `scavio` on PyPI and npm
- Hosted MCP server: [mcp.scavio.dev](https://mcp.scavio.dev)
- Docs: [scavio.dev/docs](https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=scavio)
