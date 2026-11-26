---
name: rakuten-cashback-api
description: Rakuten Cashback API for Rakuten (rakuten.com, the cashback site, formerly Ebates; Rakuten UK at rakuten.co.uk in GBP and Rakuten Canada at rakuten.ca in CAD, English or French) - the cash back rate every store pays right now as Rakuten writes it, with the was rate that marks a raised rate (Macy's read 12% Cash Back, was 2%, plus $10 In-Store; Expedia Up to 12%, was 3%; Kohl's 2%), the in-store card-linked rate, the per-category rates and Rakuten's own terms and exclusions (Macy's terms put Furniture & Mattresses at 1.5%), when cash back posts, and the store's coupons and deals with codes; the full store directory, 36 a page (3,208 stores on rakuten.com on 2026-11-26), sorted by highest cash back, Rakuten's order or A to Z and filtered by category (us) or by department and raised, top, new, Canadian or buy-now-pay-later flags (ca); current rates for up to 100 store ids in one call; search for a store, brand or product (top store, stores that carry it, coupons and product deals with sale and was price); search box suggestions; a category's stores and featured sections; the Black Friday, Cyber Monday and coupons event pages and a store's own Black Friday page; the card-linked in-store offers, 21 a page, with Rakuten's terms. 9 endpoints, 1 credit per call. Rakuten gives no end date for a cash back rate and no coupon end dates on US and UK; shopping-trip links are never returned; no rate history, no member account, no Rakuten Japan.
version: 1.0.0
tags: rakuten, rakuten-cashback, rakuten-api, rakuten-rewards, ebates, rakuten-cash-back-rates, rakuten-stores, rakuten-coupons, rakuten-promo-codes, rakuten-deals, rakuten-black-friday, rakuten-cyber-monday, rakuten-in-store, rakuten-uk, rakuten-canada, rakuten-ca, rakuten-co-uk, rakuten-double-cash-back, rakuten-store-rates, cashback, cash-back, cashback-rates, cashback-tracker, cashback-comparison, rewards, coupons, promo-codes, coupon-codes, deals, black-friday-deals, card-linked-offers, affiliate-research, retail-promotions, price-monitoring, us-retail, uk-retail, canada-retail, usd, gbp, cad, agents, ai-agents, structured-data, json, mcp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/rakuten-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api
---

# Rakuten Cashback API - Cash Back Rates, Store Coupons, Deals

Read Rakuten (rakuten.com, the cashback site, formerly Ebates; Rakuten UK at rakuten.co.uk and Rakuten Canada at rakuten.ca): the store directory with every store's current cash back rate, one store in full with its online and in-store rates, per-category rates, terms, exclusions and coupons, every coupon a store has, current rates for up to 100 stores in one call, search for a store, brand or product, the search box suggestions, a category's stores, Rakuten's event pages (Black Friday, Cyber Monday, coupons) and the card-linked in-store offers. rakuten.com (us, USD) for all 9 endpoints; rakuten.co.uk (gb, GBP) for stores, store, store coupons, rates and search; rakuten.ca (ca, CAD, English or French) for stores, store and search. Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: Rakuten cash back rates, and when they go up.** What a store pays back on Rakuten right now, and whether that is a raised rate. On 2026-11-26 `/rates` for Macy's, Kohl's, Expedia and Nike read Macy's "12% Cash Back" with `was_text` "was 2%" (`elevated` true) and "$10 In-Store", Kohl's "2% Cash Back", Expedia "Up to 12% Cash Back", was 3%, and Nike "2% Cash Back", in one call. The store page says what the headline rate covers: Macy's `category_rates` read 12% on "All Other Categories" and its terms "Furniture & Mattresses will earn 1.5% Cash Back", with "Cash Back will be automatically added to your Rakuten account today." The second job is the event pages: the Black Friday page listed 694 stores in its "12% Cash Back stores" section (adidas "Up to 12% Cash Back", was 2%), plus travel, fashion and beauty sections, coupons and product deals. Pair it with the retailer skills (`macys-product-data`, `kohls-product-data`, `target-product-data`, `best-buy-product-data`) for the price of the item itself.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **The rate text is Rakuten's.** `rate_text` is the rate as Rakuten writes it ("12% Cash Back", "Up to 12% Cash Back", "Up to 0.82% Cashback", "Jusqu’à 6% de remise $", "Coupons Only"); `reward` {`amount`, `type` (`percentage` or `fixed`), `up_to`, `tiered`} is the same rate as numbers. "Up to" and `tiered` mean the rate differs by category: read `category_rates` on `/store`.
- **Raised means a was rate.** `elevated` is true when Rakuten shows a was rate (`was_text` "was 2%", `was_amount` 2). Rakuten Canada also flags raised stores with its own `increased` flag. Report both as Rakuten's labels.
- **No end dates for rates.** Rakuten gives no start or end date for a cash back rate or an event, and Rakuten US and UK give no coupon end dates (a coupon `tag` carries Rakuten's own "ENDS TODAY" or "ENDS TOMORROW" when it has one). Never state when a raised rate ends. In-store offer terms and Rakuten Canada search coupons carry Rakuten's own text and dates as given.
- **Never a shopping-trip link.** Rakuten's tracked shopping links are never returned and must never be built. `page_path` (`/shop/macys`) is the store's Rakuten page path as a plain identifier; it is null on many list items, where `store_id` is the identifier.
- **Ids and slugs per market.** `store_id` and slugs are Rakuten's per market: `/rates` takes US or UK store ids; Rakuten Canada pages go by slug only (`best-buy`). An unknown store is a charged `404`.
- **Not every endpoint in every market.** gb: stores, store, store coupons, rates and search (no coupon search type). ca: stores, store and search. Suggestions, category, deals and in-store are rakuten.com only. Asking another market is a `400`, not charged.
- **No history, no account.** Nothing is cached or kept, no member account is read and no in-store offer is ever added to an account. Poll and store your own series.

Rakuten has no public API for its cash back rates. Rakuten Advertising, the affiliate network, has publisher APIs for advertisers a publisher is approved with, which is a different product. Rates, coupons and terms are shown on each store's Rakuten page, and this skill reads those public pages with one Scavio key.

Rakuten's store pages say "Over 3,500 stores pay us for sending them shoppers"; the rakuten.com all-stores list held 3,208 stores on 2026-11-26, rakuten.ca says 750+ stores and rakuten.co.uk 500 stores. The US site is run by Ebates Performance Marketing, Inc. dba Rakuten Rewards, part of Rakuten Group (Tokyo). Quote these with their source, never from the samples. Rakuten Japan (Rakuten Rebates, points rather than cash) and the Rakuten marketplaces are not served.

See also: the price of the item at the store `macys-product-data`, `kohls-product-data`, `target-product-data`, `best-buy-product-data`, `walmart-product-data`, `amazon-product-data`; prices across retailers `google-shopping-api`; a retailer's own coupons `staples-ink-prices-api`.

## When to trigger

Use this skill when the user asks to:
- Read a store's current Rakuten cash back rate, its was rate (raised or not), its in-store rate and its per-category rates
- Watch up to 100 stores' Rakuten rates in one call and spot raised rates
- List every Rakuten store, highest cash back first, A to Z or in Rakuten's order, by category (us) or by department and raised, top, new, Canadian or buy-now-pay-later flags (ca)
- Read a store's Rakuten terms, exclusions, special terms and how soon cash back posts
- List every coupon and deal a store has on Rakuten, with codes and Rakuten's ENDS TODAY / ENDS TOMORROW tags
- Search Rakuten for a store, brand or product: the top store, the stores that carry a brand, coupons and product deals with sale and was prices
- Read Rakuten's Black Friday, Cyber Monday or coupons pages, or one store's own Black Friday page
- List Rakuten's card-linked in-store offers with their terms
- Read the stores in a rakuten.com category with its featured sections
- Read Rakuten UK (GBP) or Rakuten Canada (CAD, English or French)

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, a UK store took under 1 second, category, in-store, search and the Canadian pages about 1.5-2, store coupons, a US store, suggestions and stores 3-4, rates about 6 and the Black Friday page about 7. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/rakuten/stores` | The store directory, 36 a page, each store with its current rate, was rate, in-store rate; us categories, ca departments and flag counts | us, gb, ca | 1 |
| `POST /api/v1/rakuten/store` | One store by slug, link or id: online and in-store rates, was rate, per-category rates, terms and exclusions, in-store terms, posting time, first coupons, Rakuten member reviews | us, gb, ca | 1 |
| `POST /api/v1/rakuten/store-coupons` | Every coupon and deal of one store, 18 a page, with code, restriction and Rakuten's tag | us, gb | 1 |
| `POST /api/v1/rakuten/rates` | Current online and in-store rates for up to 100 store ids, in the order asked | us, gb | 1 |
| `POST /api/v1/rakuten/search` | A store, brand or product: top store, store lists, coupons, product deals (type all); every matching store (type stores, 12 a page); coupons (type coupons) | us, gb, ca | 1 |
| `POST /api/v1/rakuten/suggestions` | The search box suggestions: stores with their rates, and product terms | us | 1 |
| `POST /api/v1/rakuten/category` | One category's stores with Cash Back, 36 a page; page 1 adds subcategories and the page's featured sections | us | 1 |
| `POST /api/v1/rakuten/deals` | Black Friday, Cyber Monday or the coupons hub (or a store's own Black Friday page): stores, coupons and product deals by section | us | 1 |
| `POST /api/v1/rakuten/in-store` | The card-linked in-store offers, 21 a page, with Rakuten's terms | us | 1 |

`country` is `us` (default, rakuten.com, USD), `gb` (rakuten.co.uk, GBP) or `ca` (rakuten.ca, CAD); `language` is `en` (default) or `fr` (with `ca` only: the /fr/ pages, French text). An endpoint asked for a market it does not serve is a `400`, not charged.

## Rates: rate text, was rate, in-store, per category

Every store carries:

| Field | Meaning |
|---|---|
| `rate_text` | The rate as Rakuten writes it ("12% Cash Back", "Up to 12% Cash Back", "Coupons Only") |
| `reward` | {`amount`, `type` (`percentage` or `fixed`), `up_to`, `tiered`}: the same rate as numbers (`tiered` us and gb) |
| `was_text`, `was_amount` | Rakuten's was rate ("was 2%", 2), given only on a raised rate; `null` otherwise |
| `elevated` | true when Rakuten shows a was rate: a raised rate |
| `in_store` | The card-linked in-store rate {`rate_text`, `was_text`, `amount`, `type`} ("$10 In-Store"), or `null` |
| `rate_with_type_text` | Rates: "12% Online", "$10 In-Store" as Rakuten labels them |
| `category_rates` | Store: the rate per category of purchase (us, gb: {`rate_text`, `amount`, `type`, `categories[]` {`id`, `name`}}; ca: {`category`, `rate_text`, `amount`, `type`}) |
| `flags` | ca only: {`increased`, `top`, `new`, `canadian`, `bnpl`}, Rakuten Canada's own store labels |

- **Headline against category.** "Up to" rates and `tiered` stores pay different rates per category: Rakuten UK's Argos read "Up to 0.82% Cashback", 0.82% for new customers and 0.37% for existing customers. Quote the category rate that fits the purchase, with Rakuten's terms.
- **Raised rates.** A raised rate is Rakuten's `was_text` next to the current rate. On the rakuten.com store list sorted by cash back, the first stores read "100% Cash Back", was 20% (VPN and privacy subscriptions). Report the two numbers and the date; never say when a raised rate ends.
- **Markets:** report each rate on its own site and currency (a fixed rate on rakuten.co.uk is in GBP, on rakuten.ca in CAD). Never carry a rate from one market to another.
- Report Rakuten's labels and numbers. Never judge whether a rate is good, never compute an amount earned on a purchase beyond the rate shown, and never describe how often a store's rate is raised.

## Workflow

1. **Find the store.** `/suggestions` (us) or `/search` with `query` gives `store_id` and, where Rakuten gives it, `slug`; `/stores` lists every store. On Rakuten Canada use the slug (`best-buy`).
2. **Read it in full.** `/store` with `store` (a slug such as `macys`, a Rakuten store page link, or a numeric `store_id` on us and gb): online and in-store rates, was rate, `category_rates`, `terms` (`text`, `exclusions`, `special_terms`), `in_store_terms`, `posting_time`, the first coupons and Rakuten member reviews (rating and text, no names).
3. **Watch rates.** `/rates` with up to 100 `store_ids` (us or gb) in one call; poll it on a schedule and store each answer with its `fetched_at`. A changed `rate_text` or a new `was_text` is a rate change.
4. **Coupons.** `/store-coupons` with `store` and `page` (18 a page) for every coupon and deal one store has; `/search` with `type` `coupons` for coupons matching a word (us, ca).
5. **Browse.** `/stores` with `sort` (`cashback`, `recommended`, `az`, `za`), `category` (us: a slug from `categories[]`; ca: a department) and `filter` (ca: `increased`, `top`, `new`, `canadian`, `bnpl`); `/category` (us) for one category's stores and featured sections.
6. **Events.** `/deals` with `page` `black_friday` (default), `cyber_monday` or `coupons`; `black_friday` with `store` (a slug) for that store's own Black Friday page.
7. **In-store.** `/in-store` with `page` (21 a page) for the card-linked offers. A member adds an offer in their own Rakuten account; this API reads the public list only.

## Parameters

### Stores (`/stores`) and category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country`, `language` | string | `us`, `en` | Stores: `us`, `gb` or `ca`; category: `us` |
| `category` | string or integer | stores: none; category: required | us: a category slug or id from `categories[]` (`electronics` or 651, `clothing` or 2, `travel-vacations` or 54; subcategories such as `electronics/computers-tablets` on category). ca: a Rakuten Canada department (`baby-kids-toys`, `computers-electronics-office`, `health-beauty`, ... 17 in all). Not on gb |
| `sort` | string | the site's | `cashback` (highest rate first), `recommended` (Rakuten's order), `az`, `za`. Defaults: us `cashback`, gb `az`, ca `recommended` (A to Z); category `recommended` |
| `filter` | string or array | none | ca only: up to 5 of `increased` (raised rate), `top`, `new`, `canadian`, `bnpl` (buy now, pay later), combined |
| `page` | integer | 1 | 1-200; 36 stores a page |

### Store (`/store`), store coupons (`/store-coupons`), rates (`/rates`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store` | string or integer | required | The store's Rakuten slug (`macys`; `best-buy` on rakuten.ca), its Rakuten page link, or its numeric store id (us, gb) |
| `country` | string | `us` | Store: `us`, `gb`, `ca` (with `language` `fr` for French); store coupons: `us`, `gb` |
| `page` | integer | 1 | Store coupons: 1-200, 18 coupons a page |
| `store_ids` | array or string | rates: required | 1-100 Rakuten store ids (`stores[].store_id`), as an array or comma-separated (`["8333", "7206", "3930"]`); rates: `us` or `gb` |

### Search (`/search`) and suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | A store, brand or product, 1-100 chars (suggestions: 1-60, what a member types) |
| `type` | string | `all` | `all` (top store, stores, coupons, products), `stores` (every store matching the query) or `coupons` (us and ca) |
| `page` | integer | 1 | us `type` `stores` only, 12 stores a page; every other search answers one page |
| `country`, `language` | string | `us`, `en` | Search: `us`, `gb`, `ca`; suggestions: `us` |

### Deals (`/deals`) and in-store (`/in-store`)

`/deals` takes `page` (`black_friday` default, `cyber_monday`, `coupons`) and, with `black_friday` only, `store` (a slug, not an id) for that store's own Black Friday page. `/in-store` takes `page` (1-200, 21 offers a page). Both are us only.

## Examples

### Rates for four stores in one call

```bash
curl -X POST https://api.scavio.dev/api/v1/rakuten/rates \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_ids": ["8333", "7206", "3930", "9528"]}'
```

Captured `data` (2026-11-26; 2 of 4 stores shown, `image` dropped):

```json
{
  "country": "us",
  "currency": "USD",
  "requested": 4,
  "count": 4,
  "stores": [
    {
      "store_id": 8333,
      "name": "Macy's",
      "slug": "macys",
      "page_path": "/shop/macys",
      "rate_text": "12% Cash Back",
      "rate_with_type_text": "12% Online",
      "amount": 12,
      "type": "percentage",
      "up_to": false,
      "was_text": "was 2%",
      "was_amount": 2,
      "elevated": true,
      "tiered": true,
      "in_store": { "rate_text": "$10 Cash Back", "rate_with_type_text": "$10 In-Store", "was_text": null, "amount": 10, "type": "fixed" }
    },
    {
      "store_id": 3930,
      "name": "Expedia",
      "slug": "expedia",
      "page_path": "/shop/expedia",
      "rate_text": "Up to 12% Cash Back",
      "rate_with_type_text": "Up to 12% Online",
      "amount": 12,
      "type": "percentage",
      "up_to": true,
      "was_text": "was 3%",
      "was_amount": 3,
      "elevated": true,
      "tiered": true,
      "in_store": null
    }
  ],
  "not_found": []
}
```

Kohl's (`7206`) read "2% Cash Back" and Nike (`9528`) "2% Cash Back", neither raised. An id Rakuten does not answer is listed in `not_found`; if none is found the call is a charged `404` ("Rakuten has none of these store ids.").

### One store with its category rates, terms and posting time

```bash
curl -X POST https://api.scavio.dev/api/v1/rakuten/store \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store": "macys"}'
```

Captured `data` (2026-11-26; `terms.text`, `in_store_terms` and `about` cut, `coupons` to 1 of 6, `reviews.items` to 2 of 8, `image` dropped):

```json
{
  "country": "us",
  "currency": "USD",
  "store_id": 8333,
  "name": "Macy's",
  "slug": "macys",
  "page_path": "/shop/macys",
  "rate_text": "12% Cash Back",
  "online": { "rate_text": "12% Online", "was_text": "was 2%", "amount": 12, "type": "percentage", "up_to": false, "tiered": true },
  "elevated": true,
  "was_amount": 2,
  "boosted": false,
  "in_store": { "rate_text": "$10 In-Store", "reward_text": "$10 Cash Back", "amount": 10, "type": "fixed" },
  "category_rates": [
    { "rate_text": "12% Cash Back", "amount": 12, "type": "percentage", "categories": [{ "id": 2523, "name": "All Other Categories" }] }
  ],
  "terms": {
    "text": "Furniture & Mattresses will earn 1.5% Cash Back.\nItems shipped and sold by Marketplace (third party sellers as indicated on the product page) and Electronics will earn 1.5% Cash Back. ...",
    "exclusions": "Furniture & Mattresses will earn 1.5% Cash Back. ...",
    "special_terms": "The portion of orders paid for using Macy's Star Dollars do not qualify for Cash Back."
  },
  "in_store_terms": "Offer valid through December 13, 2026. Minimum Spend of $100 required. $10 Cash Back. US stores only. ...",
  "posting_time": "Cash Back will be automatically added to your Rakuten account today.",
  "free_shipping": "Macy's offers free shipping on orders $49 or more.",
  "title": "Macy's Coupons, Promo Codes & 12% Cash Back - November 2026 | Rakuten",
  "coupons": {
    "total": 100,
    "has_more": true,
    "count": 6,
    "coupons": [
      { "coupon_id": "14659344", "store_id": 8333, "store_name": "Macy's", "description": "Get up to 70% off Black Friday deals + kitchen electrics under $50.", "code": null, "restriction": null, "tag": null, "rate_text": "12% Cash Back", "was_rate_text": "was 2%" }
    ]
  },
  "reviews": {
    "average": 4.7,
    "count_text": "Based on 2.5K Reviews",
    "items": [
      { "rating": 5, "text": "Love shopping at Macys" },
      { "rating": 5, "text": "Bought a cashmere jacket for my husband and he loves it. The quality is great and it arrived on time." }
    ]
  }
}
```

The 12% applies to "All Other Categories"; the terms put Furniture & Mattresses, Marketplace items and Electronics at 1.5%. `in_store_terms` is Rakuten's own text for the in-store offer, its date as given; the online rate has no end date. Reviews are Rakuten member reviews of the store, the 8 latest, with no names. On Rakuten UK, `{"store": "argos", "country": "gb"}` read "Up to 0.82% Cashback" (0.82% new customers, 0.37% existing) and "Cashback will be automatically added to your Rakuten account within one week." On Rakuten Canada in French, `{"store": "best-buy", "country": "ca", "language": "fr"}` read "Jusqu’à 6% de remise $", was "était 1%", 25 category rates, `days_to_report` "1 Jour" and 22 coupons. An unknown store is a charged `404`.

### Search for a brand

```bash
curl -X POST https://api.scavio.dev/api/v1/rakuten/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nike"}'
```

Captured `data` (2026-11-26; `store_lists` cut to 1 of 2 with 1 of 12 stores, `coupons` to 1 of 7, `products` to 1 of 12, images dropped):

```json
{
  "country": "us",
  "currency": "USD",
  "type": "all",
  "page": 1,
  "query": "nike",
  "top_store": { "store_id": 9528, "name": "Nike", "slug": null, "page_path": null, "rate_text": "2% Cash Back", "was_text": null, "elevated": false, "reward": { "amount": 2, "type": "percentage", "up_to": false, "tiered": false }, "was_amount": null, "in_store": null },
  "offers_cash_back": null,
  "no_cash_back_message": null,
  "store_lists": [
    {
      "title": "Stores that carry Nike",
      "total": 57,
      "has_more": true,
      "count": 12,
      "stores": [
        { "store_id": 8333, "name": "Macy's", "slug": null, "page_path": null, "rate_text": "12% Cash Back", "was_text": "was 2%", "elevated": true, "reward": { "amount": 12, "type": "percentage", "up_to": false, "tiered": true }, "was_amount": 2, "in_store": { "rate_text": "$10 In-Store", "was_text": null, "amount": 10, "type": "fixed", "was_amount": null } }
      ]
    }
  ],
  "coupons": {
    "total": 7,
    "count": 7,
    "items": [
      { "coupon_id": "14657648", "store_id": 9528, "store_name": "Nike", "description": "Black Friday: Get an extra 25% off select styles.", "code": "BFRIDAY", "restriction": null, "tag": null, "rate_text": "2% Cash Back", "was_rate_text": null }
    ]
  },
  "products": {
    "total": 437925,
    "has_more": true,
    "count": 12,
    "items": [
      { "product_id": "00193154042641_upc", "item_id": "9528-12784020-00193154042641", "name": "Nike Men's Flex Control 4 Workout Shoes in White | CD0197-100", "store_id": 9528, "store_name": "Nike", "price_text": "$59.97", "price": 59.97, "was_price_text": "$70.00", "was_price": 70, "tag": null, "rate_text": "2% Cash Back", "was_rate_text": null, "store_count": 1 }
      ]
  }
}
```

The second store list was "Other stores you might like" (346). `type` `stores` pages every store matching the query, 12 a page (us). When Rakuten says a store does not offer Cash Back, `offers_cash_back` is false with Rakuten's `no_cash_back_message`. Product prices are as Rakuten shows them; check the store's own page for the current price. On Rakuten Canada, `{"query": "nike", "country": "ca"}` answered 3 stores (Famous Footwear 2%, Sporting Life 12%, size? "Coupons Only"), 8 of 173 products and 3 coupons, each coupon with `expires` as an ISO date (null where Rakuten writes a far-future placeholder).

### Stores, store coupons, suggestions, category, deals, in-store and Canada

- `/stores` `{"sort": "cashback"}`: `total` 3,208, 90 pages of 36, the first "100% Cash Back", was 20% (Coveron, NordVPN, Incogni, Surfshark, NordPass, CyberGhost VPN); 19 `categories` (clothing, electronics, beauty-wellness, travel-vacations, ...). A filtered us list has `total` null until its last page.
- `/stores` `{"country": "ca", "filter": "increased"}`: 178 raised stores, 5 pages, A to Z (Adidas 12%, was 2%; Aldo Canada 15%, was 2%), with `departments` and flag counts (`increased` 178, `top` 155, `new` 118, `canadian` 109, `bnpl` 71).
- `/store-coupons` `{"store": "macys"}`: `total` 100, 6 pages of 18, such as "Up to 70% off 1,000s of Black Friday deals." with `tag` "ENDS TOMORROW". No coupon end dates on US and UK.
- `/suggestions` `{"query": "target"}`: 588 stores in `total`, 10 shown: Target "1.0% Cash Back", Best Buy "Up to 6.0% Cash Back", Target Optical 12.0%, Sam's Club "Up to 12.0%", Macy's 12.0% with "$10.00 In-Store", Old Navy 12.0%, ...
- `/category` `{"category": "electronics"}`: Electronics (id 651), 258 stores, 8 pages (Apple 2%, Sling TV 40% was 15%, Dell Refurbished Computers 12% was 2%), 7 `subcategories` and 8 `sections` ("Featured Cash Back on Electronics", "Deals and coupons of the week", "Cash Back on top-selling laptops", ...). An unknown category is a charged `404`.
- `/deals` (Black Friday): 8 sections, "12% Cash Back stores" (694), "Travel with 12% Cash Back" (28, Expedia Up to 12% was 3%), "Fashion with 12% Cash Back" (268), "Beauty & wellness with 12% Cash Back" (189), "Home deals with 12% Cash Back" (coupons), "Gifts with 12% Cash Back" (products, Apple AirPods 4 at Staples $116.99 against $129.00, tag "9% OFF"), "Earn 12% Cash Back In-Store" (13) and "All stores". Rakuten gives no start or end dates.
- `/in-store`: 84 offers, 4 pages of 21, such as Finish Line "2% In-Store" and Macy's "$10 In-Store", each with `status` and Rakuten's `terms` as given.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rakuten(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/rakuten/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Find a store id (1 credit)
s = rakuten("suggestions", {"query": "macys"})["data"]
for st in s["stores"]["items"][:3]:
    print(st["store_id"], st["name"], st["rate_text"])

# 2. Today's rates for a watch list, raised ones flagged (1 credit for up to 100 ids)
watch = ["8333", "7206", "3930", "9528"]
rates = rakuten("rates", {"store_ids": watch})["data"]
for st in rates["stores"]:
    raised = f" (raised, {st['was_text']})" if st["elevated"] else ""
    print(st["name"], st["rate_text"] + raised, st["in_store"]["rate_with_type_text"] if st["in_store"] else "")
print("not found:", rates["not_found"])

# 3. What the headline rate covers (1 credit)
m = rakuten("store", {"store": "macys"})["data"]
for c in m["category_rates"]:
    print(c["rate_text"], [x["name"] for x in c["categories"]])
print(m["terms"]["exclusions"])
print(m["posting_time"])

# Rates change without notice and Rakuten gives no end dates. Store each
# answer with fetched_at and run this on a schedule: that stored series is
# your rate history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `country` and, on most endpoints, `currency` (`USD`, `GBP` or `CAD`; Rakuten Canada adds `language` `en-CA` or `fr-CA`) and `notes`.

- **store** (list item; us, gb) - `store_id`, `name`, `slug`, `page_path`, `rate_text`, `was_text`, `elevated`, `reward` {`amount`, `type`, `up_to`, `tiered`}, `was_amount`, `in_store` {`rate_text`, `was_text`, `amount`, `type`} or null, `image`. ca adds `coupons_only` and `flags` {`increased`, `top`, `new`, `canadian`, `bnpl`}.
- **stores** - `sort`, `category`, `page`, `per_page`, `total`, `pages`, `has_more`, `count`, `stores[]`; us `categories[]` {`id`, `name`, `slug`}; ca `filter`, `departments`, `filters` (counts per flag).
- **store** (us, gb) - `store_id`, `name`, `slug`, `page_path`, `rate_text`, `online` {`rate_text`, `was_text`, `amount`, `type`, `up_to`, `tiered`}, `elevated`, `was_amount`, `boosted`, `in_store` {`rate_text`, `reward_text`, `amount`, `type`} or null, `category_rates[]` {`rate_text`, `amount`, `type`, `categories[]` {`id`, `name`}}, `terms` {`text`, `exclusions`, `special_terms`}, `in_store_terms`, `posting_time`, `free_shipping`, `about`, `title`, `coupons` {`total`, `has_more`, `count`, `coupons[]`}, `reviews` {`average`, `count_text`, `items[]` {`rating`, `text`}}.
- **store** (ca) - `store_id`, `name`, `slug`, `page_path`, `rate_text`, `was_text`, `elevated`, `reward`, `was_amount`, `coupons_only`, `category_rates[]` {`category`, `rate_text`, `amount`, `type`}, `special_conditions`, `days_to_report`, `total_cash_back_to_date`, `attributes`, `coupons` {`count`, `items[]` {`description`, `code`, `restriction`, `rate_text`}}, `image`.
- **coupon** - `coupon_id`, `store_id`, `store_name`, `description`, `code` (null on a deal), `restriction`, `tag` (Rakuten's own label), `rate_text`, `was_rate_text`, `image`; ca search coupons add `store_slug`, `expires_text`, `expires`.
- **store-coupons** - `store_id`, `name`, `page`, `per_page`, `total`, `pages`, `has_more`, `count`, `coupons[]`.
- **rates** - `requested`, `count`, `stores[]` {`store_id`, `name`, `slug`, `page_path`, `rate_text`, `rate_with_type_text`, `amount`, `type`, `up_to`, `was_text`, `was_amount`, `elevated`, `tiered`, `in_store` {`rate_text`, `rate_with_type_text`, `was_text`, `amount`, `type`} or null, `image`}, `not_found`.
- **search** (type all; us, gb) - `query`, `type`, `page`, `top_store`, `offers_cash_back`, `no_cash_back_message`, `store_lists[]` {`title`, `total`, `has_more`, `count`, `stores[]`}, `coupons` {`total`, `count`, `items[]`}, `products` {`total`, `has_more`, `count`, `items[]` {`product_id`, `item_id`, `name`, `store_id`, `store_name`, `price_text`, `price`, `was_price_text`, `was_price`, `tag`, `rate_text`, `was_rate_text`, `store_count`, `image`}}. type stores: `page`, `per_page`, `total`, `pages`, `has_more`, `count`, `stores[]`; type coupons: `total`, `count`, `has_more`, `coupons[]`. ca: `stores` {`total`, `count`, `items[]`}, `products` {`total`, `count`, `items[]` {`name`, `store_slug`, `store_name`, `price_text`, `price`, `was_price_text`, `was_price`, `rate_text`, `image`}}, `coupons` {`total`, `count`, `items[]`}.
- **suggestions** - `query`, `stores` {`total`, `items[]` {`store_id`, `name`, `slug`, `page_path`, `rate_text`, `amount`, `type`, `up_to`, `in_store_text`, `logo`}}, `products[]` {`term`, `categories`}.
- **category** - `category` {`id`, `name`, `slug`}, `sort`, `page`, `per_page`, `total`, `pages`, `has_more`, `count`, `stores[]`; page 1 adds `subcategories[]` {`id`, `name`, `slug`} and `sections[]` {`title`, `kind`, `total`, `has_more`, `count`, `items`}.
- **deals** - `page`, `store`, `count`, `sections[]` {`title`, `kind` (`stores`, `coupons` or `products`), `total`, `has_more`, `count`, `items`}.
- **in-store** - `page`, `per_page`, `total`, `pages`, `has_more`, `count`, `offers[]` {`offer_id`, `store_id`, `name`, `slug`, `page_path`, `rate_text`, `amount`, `type`, `status`, `terms`, `image`}.

## Guardrails

- Name it "Rakuten (rakuten.com, the cashback site, formerly Ebates)" on first mention, and name the market (rakuten.com, rakuten.co.uk or rakuten.ca) of every rate.
- Rates: quote `rate_text` as Rakuten writes it, with `was_text` when there is one, the market and the `fetched_at` date. Say "Up to" and per-category rates plainly and quote the category rate and terms that fit the purchase.
- End dates: Rakuten gives none for a cash back rate or an event, and none for US and UK coupons. Never state or guess when a raised rate or a coupon ends; quote Rakuten's own tag ("ENDS TODAY") or the date in Rakuten's own terms text as given.
- Links: never return, build or follow a Rakuten shopping-trip link. `page_path` is an identifier, not a link to send a shopper through.
- Report Rakuten's labels and numbers only. Never judge whether a rate is good, never promise that cash back will be paid or how much a purchase will earn, and never describe how often a store's rate is raised.
- Product prices in search and deals are as Rakuten shows them at the moment of the call; the store's own page has the current price. Never call one store cheaper beyond the numbers shown.
- Reviews: Rakuten member reviews of a store carry rating and text only; no reviewer names are returned.
- Not available: rate history (poll and store), end dates for rates, coupon end dates on US and UK, member accounts, adding in-store offers, shopping-trip links, Rakuten Japan (Rakuten Rebates) and the Rakuten marketplaces. This API cannot sign in, activate an offer or buy.
- Terms: Scavio does not collect or store Rakuten data: each call fetches the public Rakuten page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Rakuten's member terms cover how its services may be used, including access by automated means; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Rakuten or store logos; name the store and the market instead.
- Never fabricate rates, was rates, coupons, codes, store ids, terms or dates. Only return what the API returned, with the `fetched_at` time and the market.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside `us`, `gb`, `ca`, or an endpoint asked for a market it does not serve ("<endpoint> is available for country us only (Rakuten UK has no such page)."); "language fr is for country ca (Rakuten Canada) only."; a `store` that is not a slug, a Rakuten page link or a numeric id, or an id on Rakuten Canada ("store: Rakuten Canada pages go by slug (e.g. best-buy, amazon), not by id."); `store_ids` missing, not numeric or more than 100; "filter (increased, top, new, canadian, bnpl) is for country ca only; on us and gb a store's elevated flag says whether its rate is raised."; "category is for country us (and ca departments); Rakuten UK's all-brands list has no category filter."; a category not in Rakuten's list (the error lists them) or a ca department not in the 17; "type coupons is for country us and ca; Rakuten UK has no coupon search page (type all answers its results)."; `page` above 1 on a search that answers one page ("page applies to type stores (12 a page); type all and coupons answer one page."); "store applies to page black_friday (a store's own Black Friday page) only." or a store id on deals; a `page` outside 1-200.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Rakuten US has no store <slug>. Look it up with suggestions, search or stores.", "Rakuten Canada has no store <slug>. Look it up with stores (country ca) or search.", "Rakuten has none of these store ids.", "Rakuten has no category <slug>. Send a slug from stores' categories (e.g. electronics, clothing, travel-vacations).", "Rakuten Canada has no department <department>.", "Rakuten has no Black Friday page for <slug>.", "Rakuten answered no results page for this search.", "Rakuten has no store suggestions for <query>.". Take slugs and ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api).
- `502` means Rakuten data was temporarily unavailable ("Rakuten is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Rakuten is busy ("Rakuten is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: all } = await scavio.rakuten.stores({ sort: "cashback" });
const { data: raisedCa } = await scavio.rakuten.stores({ country: "ca", filter: "increased" });
const { data: macys } = await scavio.rakuten.store({ store: "macys" });
const { data: argos } = await scavio.rakuten.store({ store: "argos", country: "gb" });
const { data: coupons } = await scavio.rakuten.storeCoupons({ store: "macys", page: 2 });
const { data: rates } = await scavio.rakuten.rates({ store_ids: ["8333", "7206", "3930"] });
const { data: hits } = await scavio.rakuten.search({ query: "nike" });
const { data: sugg } = await scavio.rakuten.suggestions({ query: "target" });
const { data: cat } = await scavio.rakuten.category({ category: "electronics", sort: "cashback" });
const { data: bf } = await scavio.rakuten.deals({ page: "black_friday" });
const { data: inStore } = await scavio.rakuten.inStore({ page: 1 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.rakuten.stores(...)`, `store`, `store_coupons`, `rates`, `search`, `suggestions`, `category`, `deals` and `in_store`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `get_rakuten_stores`, `get_rakuten_store`, `get_rakuten_store_coupons`, `get_rakuten_rates`, `search_rakuten`, `get_rakuten_suggestions`, `get_rakuten_category`, `get_rakuten_deals` and `get_rakuten_in_store`. Rakuten is opt-in: add `rakuten` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,rakuten"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [stores](https://scavio.dev/docs/rakuten-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [store](https://scavio.dev/docs/rakuten-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [store coupons](https://scavio.dev/docs/rakuten-store-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [rates](https://scavio.dev/docs/rakuten-rates?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [search](https://scavio.dev/docs/rakuten-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [suggestions](https://scavio.dev/docs/rakuten-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [category](https://scavio.dev/docs/rakuten-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [deals](https://scavio.dev/docs/rakuten-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api), [in-store](https://scavio.dev/docs/rakuten-in-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api). Overview: [Rakuten API](https://scavio.dev/rakuten-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=rakuten-cashback-api).
