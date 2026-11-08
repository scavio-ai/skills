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
    homepage: https://scavio.dev/docs
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

<!-- PLATFORMS -->

## Setup

Every call reads the key from `SCAVIO_API_KEY`. The quickest way to get one (Node.js 18+) is to sign in from the terminal; it saves the key to the shell profile without printing it:

```bash
npx -y scavio@0.39.2 login
```

Or create a free account at [scavio.dev](https://scavio.dev/) (50 free credits, no card required), copy the key from the dashboard and export it yourself:

```bash
export SCAVIO_API_KEY=sk_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every call. Sign the user in instead of asking for a key:

1. Run `npx -y scavio@0.39.2 login`. It prints a link and a code, and opens the browser when it can. Show the user both and ask them to open the link, sign in or create a free account, check that the page shows the same code, and click Approve.
2. Run `npx -y scavio@0.39.2 login --wait`. Exit 0 means the key is saved; exit 2 means not approved yet, so run it again (each run waits up to 60 seconds); exit 3 means the user denied it; exit 1 means the code expired or failed, so start again.
3. The key is in the user's shell profile, not in your current shell. `npx -y scavio@0.39.2 status` confirms it works. Tell the user to restart the agent so `SCAVIO_API_KEY` is loaded.
4. A new account starts with 50 credits. Most endpoints cost 1 credit; the Platforms table and each reference say where that differs.

If Node.js is not available, send the user to [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up) to copy the key (created automatically at signup) and add it to their shell profile themselves.

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
- Docs: [scavio.dev/docs](https://scavio.dev/docs)
