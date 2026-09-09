---
name: scavio
description: "Scavio web data API: one key, structured JSON from 50 platforms. Google Search, AI Mode, News, Trends, Maps, Shopping, Hotels, Flights, Play Store and Ads Transparency; Amazon, eBay, Walmart, Target, Home Depot, AliExpress, Etsy and TikTok Shop; Instagram, TikTok, YouTube, Twitter/X, Reddit, LinkedIn, Facebook, Threads, Pinterest, Twitch, Douyin, Weibo and Kuaishou; Airbnb, Booking.com and Tripadvisor; Indeed, Glassdoor, G2, Capterra and Yelp; Zillow and Redfin; Apple App Store; SEC EDGAR, Companies House and GitHub; the Meta, TikTok and LinkedIn ad libraries; URL to Markdown and website screenshots. Routes each request to the platform reference, quotes the credit cost before a paid call, and handles 402 and 429. Use when the user wants public data from any of these sites, code that calls Scavio, or a cost estimate."
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

# Scavio - One API Key for 50 Web Data Platforms

Scavio returns public pages from 50 platforms as structured JSON through one API key. This file is the router. It says which platform reference to read, how every request is shaped, what a call costs, and what to do when one fails. The files under `references/` hold the endpoints, parameters, measured response shapes and the traps for each platform. Open the reference before the first call to a platform in a session, and call from the reference, not from memory.

## When to trigger

Use this skill when the user asks to:
- Pull public data from any platform in the table below: profiles, posts, comments, products, prices, reviews, listings, jobs, salaries, filings, ads, search results, transcripts
- Write code that calls the Scavio API in any language
- Estimate what a data job will cost in credits, or check their balance
- Turn an arbitrary URL into Markdown or a screenshot

Do not use it for a site that is not in the table. For an arbitrary page, `references/url-to-markdown-api.md` and `references/website-screenshot-api.md` are the fallbacks.

## Platforms

Each row is one reference file. Open it before the first call to that platform. Endpoint counts and credits are per call unless the row says otherwise; the reference has the exact table.

**Search**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Google AI Mode | [google-ai-mode-api](references/google-ai-mode-api.md) | 1 | 1 |
| Google Maps | [google-maps-api](references/google-maps-api.md) | 4 | 1; geo-grid bills per point |
| Google News | [google-news-api](references/google-news-api.md) | 1 | 1 |
| Google Search | [google-search-api](references/google-search-api.md) | 1 | 1 |
| Google Trends | [google-trends-api](references/google-trends-api.md) | 2 | 1 |

**Commerce**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| AliExpress | [aliexpress-product-data](references/aliexpress-product-data.md) | 6 | 1 |
| Amazon | [amazon-product-data](references/amazon-product-data.md) | 3 | 1 |
| eBay | [ebay-product-data](references/ebay-product-data.md) | 3 | 1 |
| Etsy | [etsy-product-data](references/etsy-product-data.md) | 5 | 2 |
| Google Shopping | [google-shopping-api](references/google-shopping-api.md) | 3 | 1 |
| Home Depot | [home-depot-product-data](references/home-depot-product-data.md) | 3 | 2 |
| Target | [target-product-data](references/target-product-data.md) | 4 | 1 |
| TikTok Shop | [tiktok-shop-api](references/tiktok-shop-api.md) | 8 | 1 |
| Walmart | [walmart-product-data](references/walmart-product-data.md) | 7 | 1; 2 for walmart.com.mx search and category |

**Social and video**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Douyin | [douyin-scraper-api](references/douyin-scraper-api.md) | 27 | 1; search 10 |
| Facebook | [facebook-scraper-api](references/facebook-scraper-api.md) | 11 | 1 |
| Instagram | [instagram-scraper-api](references/instagram-scraper-api.md) | 12 | 2-10 |
| Kuaishou | [kuaishou-scraper-api](references/kuaishou-scraper-api.md) | 14 | 1, 2, 10 or 40 |
| LinkedIn | [linkedin-scraper-api](references/linkedin-scraper-api.md) | 9 | 1-30 |
| Pinterest | [pinterest-api](references/pinterest-api.md) | 6 | 1; url-stats 1-2 |
| Reddit | [reddit-search-api](references/reddit-search-api.md) | 12 | 1 |
| Threads | [threads-net-api](references/threads-net-api.md) | 6 | 2 by user_id, 4 by username |
| TikTok | [tiktok-scraper-api](references/tiktok-scraper-api.md) | 11 | 1 |
| Twitch | [twitch-api](references/twitch-api.md) | 4 | 1 |
| Twitter/X | [twitter-scraper-api](references/twitter-scraper-api.md) | 11 | 1 |
| Weibo | [weibo-scraper-api](references/weibo-scraper-api.md) | 31 | 1 |
| YouTube | [youtube-data-api](references/youtube-data-api.md) | 15 | 1-8 |

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
| Glassdoor | [glassdoor-salary-data](references/glassdoor-salary-data.md) | 4 | 1 |
| Indeed | [indeed-jobs-api](references/indeed-jobs-api.md) | 4 | 2 |
| Yelp | [yelp-business-data](references/yelp-business-data.md) | 3 | 2 |

**Real estate**

| Platform | Reference | Endpoints | Credits per call |
|---|---|---|---|
| Redfin | [redfin-property-data](references/redfin-property-data.md) | 3 | 1 |
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
| Website Screenshot | [website-screenshot-api](references/website-screenshot-api.md) | 1 | 1; ultra 5 |

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=scavio) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every call. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most endpoints cost 1 credit; the table above and each reference say where that differs.

Never print, log or paste the key. Keep `$SCAVIO_API_KEY` as a variable reference in every example and command. If the user has to set it, tell them to export it in their shell rather than paste it into the chat.

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
- Billing happens when the upstream fetch completes. A `400`, `401`, `402` or `429` is never billed, and neither is a `502` or `503` upstream failure. Some `404` answers are billed because the upstream call did complete; each reference says which. There are no refunds, so never retry in a tight loop.

Plans, for sizing a job:

| Plan | Price | Credits | Concurrent requests |
|---|---|---|---|
| Free | $0 | 50 one-time | 1 |
| Pay As You Go | $0.01 per credit, 2,500 minimum | as purchased | 1 |
| Project | $30/mo | 7,000/mo | 5 |
| Bootstrap | $100/mo | 28,000/mo | 10 |
| Startup | $250/mo | 85,000/mo | 15 |
| Growth | $500/mo | 200,000/mo | 50 |

## Failure handling

- `400` - an invalid or missing parameter. Re-read the reference and fix the body; nothing was billed.
- `401` - the API key is missing or invalid. Check `SCAVIO_API_KEY`.
- `402` - out of credits. The body carries `credit_balance`, a `message` and `billing_url`. Stop, report the balance and the link; the same key keeps working after a top-up.
- `404` - the platform had nothing for that id. Normal on some endpoints (the reference says which) and sometimes billed. Skip the item; do not retry it.
- `410` - the endpoint was retired upstream. Do not retry; the reference names the replacement if there is one.
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
