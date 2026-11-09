---
name: vinted-api
description: "Vinted API: search second-hand listings on any of 27 Vinted country sites (France, UK, US, Germany, Poland, Spain, Italy, the Netherlands, Australia and more) by keyword, category, brand, condition, size, color, material and price range, 96 items per page with price, the Vinted fee and the total, read one listing in full with its category path, photos and sold or reserved state, pull a seller's public profile, listed items and reviews, and look up brand ids, filter options with live counts, the localized category tree and search autocomplete. 9 endpoints, 1 credit each. The official Vinted API serves only allowlisted Vinted Pro businesses and has no marketplace search."
version: 1.0.0
tags: vinted, vinted-api, vinted-scraper, vinted-search, vinted-bot, vinted-alerts, vinted-monitor, vinted-price-tracker, vinted-prices, vinted-listings, vinted-seller, vinted-brands, vinted-categories, second-hand, secondhand-fashion, resale, reseller, price-research, resale-prices, brand-research, market-sizing, discord-bot, new-listing-alerts, marketplace, fashion, clothing, europe, multi-country, seller-reputation, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/vinted-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api
---

# Vinted API - Listings, Prices, Sellers Across 27 Markets

Search Vinted's second-hand listings on any of its 27 country sites by keywords, category, brand, condition, size, color, material and price range, sorted by relevance, newest first or price: 96 items per page, pages 1-10, each with item id, title, URL, price and currency, the Vinted fee and the total the buyer pays, brand, size, condition, favourite count, promoted flag, photos and the seller's id and business flag, plus the filters Vinted actually applied. Read one listing by id or URL with its description, brand, size, condition, color, material, category path, every photo, favourite count, reserved and sold state and the seller's rating. Pull a seller's public profile (feedback counts, rating, item count, verifications), the items they have listed and the reviews they have received. Resolve brand names to ids, list a filter's options (size, condition, color, material) with live item counts, read the localized category tree, and get the search box's autocomplete. All endpoints return structured JSON and cost 1 credit each.

Vinted's own API, Vinted Pro Integrations, is available only to a limited set of allowlisted Vinted Pro businesses and manages that business's own items and orders; it has no marketplace search. This skill reads the public marketplace instead, with one Scavio key.

See also: for eBay listings and seller cards use the `ebay-product-data` skill; for handmade and vintage on Etsy use `etsy-product-data`.

## When to trigger

Use this skill when the user asks to:
- Search Vinted for an item (a brand, a model, a size) on a given country site and get prices in that site's currency
- Build a Vinted alert bot or new-listing monitor (Discord, Telegram, email) that polls a search sorted newest first
- Research resale prices for a brand or category before buying or listing: the asks on live listings, by condition and size
- Size a brand or category on Vinted: how many listings a brand has, what sizes, colors and conditions are listed
- Read one Vinted listing in full from a link: description, category, photos, sold or reserved state, seller rating
- Check a seller before buying: rating, feedback counts, how many items they list, verifications, and their recent reviews
- See what a shop (a business seller) currently has listed
- Get Vinted's category ids, brand ids, filter option ids or autocomplete in a market's own language
- Replace the Vinted API for a project that is not an allowlisted Vinted Pro business

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most calls take 1-5 seconds, some up to 11 seconds; allow a client timeout of at least 60 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/vinted/search` | 1 | Listings, 96 per page, pages 1-10: id, title, URL, price, currency, `price_with_discount`, `service_fee` (the Vinted fee), `total_price`, brand, size, condition, favourite count, promoted flag, image, thumbnail, photos and the seller's id and business flag. Plus `listed_results`, `total_is_capped`, `total_pages`, `has_more` and the filters Vinted applied |
| `POST /api/v1/vinted/product` | 1 | One listing by item id or URL: title, description, price and currency (the seller's), brand, size, condition, color, material, `uploaded_relative`, category id and path, all photos, favourite count, reserved and sold state, `can_buy`, and the seller (id, login, profile URL, business flag, feedback count, rating 0-1, badges) |
| `POST /api/v1/vinted/seller` | 1 | One member's public seller profile: login, profile URL, business flag, feedback count, rating 0-1, positive / neutral / negative counts, listed item count, country, city (only when shown), email / Facebook / Google verification, average response time, holiday mode and the day last seen |
| `POST /api/v1/vinted/seller-products` | 1 | The items one member has listed, up to 96 per page, newest first, cheapest first or by relevance: the search item shape plus reserved and sold flags. Plus `total_results`, `total_pages`, `has_more` |
| `POST /api/v1/vinted/seller-feedback` | 1 | Reviews left for one member, newest first, up to 50 per page: rating 1-5, text, date, whether it is Vinted's automatic feedback, and the member's reply. No reviewer identity, no item |
| `POST /api/v1/vinted/brands` | 1 | Brands matching a name: brand id (what search's `brand_ids` takes), title, slug, URL, number of listings, luxury flag and whether Vinted authenticity-checks it |
| `POST /api/v1/vinted/suggestions` | 1 | Up to 10 autocomplete suggestions for a partial query in the site's language, each with its type (`popular_search`, `brand`, `brand+parent_cat`, `attr`...) |
| `POST /api/v1/vinted/filters` | 1 | The options of one search filter (`size`, `status` for condition, `color`, `material`) with live item counts, optionally for a query and a category: option id, localized title, item count, size group and, for conditions, the description |
| `POST /api/v1/vinted/categories` | 1 | The category tree in the site's language (9 top-level categories, about 3,000 in all) with id, title, URL and children, or one category's subtree with its path |

## Markets

Every endpoint takes `country` (default `fr`): `fr`, `be`, `lu`, `es`, `nl`, `lt`, `de`, `at`, `it`, `uk` (vinted.co.uk), `pt`, `us` (vinted.com), `cz`, `sk`, `pl`, `se`, `ro`, `hu`, `dk`, `fi`, `hr`, `gr`, `ie`, `ee`, `lv`, `si`, `au` (vinted.com.au).

- Every site can show listings from sellers in other countries, with the price converted to that site's currency: EUR, or CZK (`cz`), PLN (`pl`), SEK (`se`), RON (`ro`), HUF (`hu`), DKK (`dk`), GBP (`uk`), USD (`us`), AUD (`au`). `uk`, `us` and `au` are not closed catalogs: a `uk` search returned an Australian seller's 20 AUD item at 10.43 GBP.
- The EU sites share one cross-border pool: the same listings come back on vinted.fr, vinted.de or vinted.pl, each priced in that site's currency. A search on `pl` returns prices in PLN, not a separate Polish catalog.
- `/vinted/product` returns the seller's own price and currency, which can differ from the search price. Compare search prices within one site, and quote the product price with its own currency.
- Category names, condition labels, filter titles and suggestions come back in the site's language (category `10` is `Robes` on `fr` and `Kleider` on `de`). Ids are shared, so a `category_id` or `brand_ids` value works on every site.

## Workflow

1. **Search:** call `/vinted/search` with `country` and `query`. Each item has an `id`, a `url`, the `price` and `total_price`, and `seller.id`.
2. **Narrow it:** resolve a brand with `/vinted/brands` (its `id` goes into `brand_ids`), a category with `/vinted/categories` (`category_id`), and sizes, conditions, colors or materials with `/vinted/filters` (each option's `id` goes into `size_ids`, `status_ids`, `color_ids` or `material_ids`). Then search again with those ids and a `price_from` / `price_to`.
3. **Check what applied:** read the search response's `filters`. An id Vinted ignored is missing there; say so rather than presenting unfiltered results as filtered.
4. **Read a listing:** call `/vinted/product` with the `item_id` (or the listing `url`) for the description, category path, every photo, sold or reserved state and the seller's rating.
5. **Judge the seller:** `seller.id` from a search item or product feeds `/vinted/seller` (counts and rating), `/vinted/seller-feedback` (recent reviews) and `/vinted/seller-products` (what else they list).
6. **Alert bot:** poll `/vinted/search` with `sort: "newest_first"` and the user's filters, remember the `id`s already seen, and report only new ones.
7. **Autocomplete:** `/vinted/suggestions` returns what shoppers type on that site, to seed searches in the market's language.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | One of the 27 sites above |
| `query` | string | one of | Search keywords (up to 200 chars). Optional when `category_id` or `brand_ids` is given (browse a category or brand) |
| `category_id` | integer or string | all | One category id from `/categories`, subcategories included (`1907` is Women > Clothing > Outerwear > Coats) |
| `brand_ids` | array or string | all | Brand ids from `/brands` (Nike `53`, Levi's `10`, Barbour `46805`). Array or comma-separated, up to 20 |
| `status_ids` | array or string | all | Conditions: `6` New with tags, `1` New without tags, `2` Very good, `3` Good, `4` Satisfactory |
| `size_ids` | array or string | all | Size option ids from `/filters` with `filter: "size"` (`4` is women's M / UK 12-14 / US 8-10) |
| `color_ids` | array or string | all | Color option ids from `/filters` with `filter: "color"` (`1` is black) |
| `material_ids` | array or string | all | Material option ids from `/filters` with `filter: "material"` (`123` is cashmere) |
| `price_from` / `price_to` | number | none | Price range in the site's currency. `price_from` must not be above `price_to` |
| `sort` | string | `relevance` | `relevance`, `newest_first`, `price_low_to_high` or `price_high_to_low` |
| `page` | integer | 1 | 1-10. There is no `limit`: every page holds 96 items |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | Used with `item_id`. Ignored with `url`: a URL's own site is used and echoed as `country` |
| `item_id` | integer or string | one of | Vinted item id, a search item's `id` or the number after `/items/` in a listing URL (`10671938315`) |
| `url` | string | one of | A Vinted item URL on any country site (`https://www.vinted.co.uk/items/10671938315-nike-air-max-size-uk-75`) |

### Seller (`/seller`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | Site to read the profile on |
| `user_id` | integer or string | required | Vinted member id: a search item's or product's `seller.id`, or the number after `/member/` in a profile URL (`65958245`) |

### Seller products (`/seller-products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | As above |
| `user_id` | integer or string | required | As on `/seller` |
| `sort` | string | `newest_first` | `newest_first`, `price_low_to_high` or `relevance` |
| `page` | integer | 1 | 1-500 |
| `limit` | integer | 20 | Items per page, 1-96 |

### Seller feedback (`/seller-feedback`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | As above |
| `user_id` | integer or string | required | As on `/seller` |
| `page` | integer | 1 | 1-500, newest first |
| `limit` | integer | 20 | Reviews per page, 1-50 |

### Brands (`/brands`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | As above |
| `query` | string | required | Brand name or part of it (1-100 chars) |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | As above; suggestions are in this site's language |
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

### Filters (`/filters`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | As above; titles are in this site's language |
| `filter` | string | required | `size`, `status` (condition), `color` or `material` |
| `query` | string | none | Count options for this search |
| `category_id` | integer or string | none | Count options within this category. Sizes are grouped per category, so pass one for `size` |

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | As above; titles are in this site's language |
| `parent_id` | integer or string | none | Return only this category's subtree (`1904` is Women). Omit for the whole tree |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "uk", "query": "barbour jacket"}'
```

Captured `data` (94 of 96 items trimmed):

```json
{
  "country": "uk",
  "currency": "GBP",
  "query": "barbour jacket",
  "page": 1,
  "per_page": 96,
  "count": 96,
  "listed_results": 960,
  "total_is_capped": true,
  "total_pages": 10,
  "has_more": true,
  "items": [
    {
      "id": 10721513194,
      "title": "Barbour Bronwyn Check Showerproof Jacket",
      "url": "https://www.vinted.co.uk/items/10721513194-barbour-bronwyn-check-showerproof-jacket",
      "price": 85,
      "currency": "GBP",
      "price_with_discount": null,
      "service_fee": 4.95,
      "total_price": 89.95,
      "brand": "Barbour",
      "size": "S / UK 8-10",
      "condition": "New without tags",
      "favourite_count": 55,
      "is_promoted": false,
      "image": "https://images1.vinted.net/t/02_01edd_2151N2YpSqo11rv9ptc154pe/f800/262b9080.webp?s=7c13e47c656fe07238b62931497824b3a6f137d2",
      "thumbnail": "https://images1.vinted.net/t/02_01edd_2151N2YpSqo11rv9ptc154pe/310x430/262b9080.webp?s=704ef435060e8592151075dbd06ee9f5be70c4ad",
      "photos": [
        "https://images1.vinted.net/t/02_01edd_2151N2YpSqo11rv9ptc154pe/f800/262b9080.webp?s=7c13e47c656fe07238b62931497824b3a6f137d2"
      ],
      "seller": { "id": 111684490, "is_business": false }
    },
    {
      "id": 10719665762,
      "title": "Barbour Ganni Leopard Coat",
      "url": "https://www.vinted.co.uk/items/10719665762-barbour-ganni-leopard-coat",
      "price": 395,
      "currency": "GBP",
      "price_with_discount": null,
      "service_fee": 20.45,
      "total_price": 415.45,
      "brand": "Barbour",
      "size": "M / UK 12-14",
      "condition": "Very good",
      "favourite_count": 94,
      "is_promoted": true,
      "image": "https://images1.vinted.net/t/05_00983_pAztyQFwNuiXAGZxkuTrKdF3/f800/16887e85.webp?s=7b3614d579c8aa31d8f53a8287fcd1420e7d3477",
      "thumbnail": "https://images1.vinted.net/t/05_00983_pAztyQFwNuiXAGZxkuTrKdF3/310x430/16887e85.webp?s=8203d3fc2bdc8524a265280af8e8afda0ddcf98a",
      "photos": [
        "https://images1.vinted.net/t/05_00983_pAztyQFwNuiXAGZxkuTrKdF3/f800/16887e85.webp?s=7b3614d579c8aa31d8f53a8287fcd1420e7d3477"
      ],
      "seller": { "id": 164770239, "is_business": false }
    }
  ],
  "filters": {
    "query": "barbour jacket",
    "category_ids": [],
    "brand_ids": [],
    "status_ids": [],
    "size_ids": [],
    "color_ids": [],
    "material_ids": [],
    "price_from": null,
    "price_to": null,
    "currency": null,
    "sort": "relevance"
  }
}
```

Read an item as: the seller asks £85.00, the Vinted fee is £4.95, so the buyer pays £89.95 before shipping. `service_fee` is the Vinted fee (called the Buyer Protection fee before Vinted's terms of 2026-10-08) and `total_price` is price plus that fee; shipping is not included and not returned. `listed_results: 960` with `total_is_capped: true` means at least 960 matches: Vinted serves 10 pages of 96 and no deeper, so 960 is the ceiling, not the real count. The second item is `is_promoted: true`, a promoted listing. 10 of the 96 items in this capture are from business sellers (`seller.is_business: true`).

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.vinted.co.uk/items/10671938315-nike-air-max-size-uk-75"}'
```

Captured `data` (3 of 5 photos trimmed):

```json
{
  "country": "uk",
  "id": 10671938315,
  "url": "https://www.vinted.co.uk/items/10671938315-nike-air-max-size-uk-75",
  "title": "Nike Air Max Size UK 7.5",
  "description": "Size UK 7.5/ EU 42",
  "description_translated": false,
  "price": 25,
  "currency": "GBP",
  "brand": { "id": 53, "name": "Nike" },
  "size": "7.5",
  "condition": "Very good",
  "color": "Black",
  "material": null,
  "uploaded_relative": "4 days ago",
  "category": {
    "id": 1242,
    "name": "Trainers",
    "path": [
      { "id": 5, "title": "Men", "url": "https://www.vinted.co.uk/catalog/5-men" },
      { "id": 1231, "title": "Shoes", "url": "https://www.vinted.co.uk/catalog/1231-shoes" },
      { "id": 1242, "title": "Trainers", "url": "https://www.vinted.co.uk/catalog/1242-trainers" }
    ]
  },
  "photos": [
    "https://images1.vinted.net/t/02_00957_ASq4bGt55vR1ptRurQqGQSXC/f800/68b3c547.webp?s=a6242b0503be6167ebd0d78a0a767bbc829b1a90",
    "https://images1.vinted.net/t/02_01ed7_VjTmS1jSataCkKu6WNkerhRM/f800/caca1283.webp?s=ce2988de1888e4a34ac6c0787326e65e1421b81a"
  ],
  "favourite_count": 13,
  "is_reserved": false,
  "is_sold": false,
  "status_label": null,
  "can_buy": true,
  "instant_buy": true,
  "is_hidden": false,
  "seller": {
    "id": 82327389,
    "login": "quicksell11",
    "profile_url": "https://www.vinted.co.uk/member/82327389-quicksell11",
    "is_business": false,
    "feedback_count": 1491,
    "feedback_reputation": 0.98,
    "badges": ["ACTIVE_LISTER"]
  }
}
```

The product price is in the seller's currency, which can differ from the site's: on an EU site a search shows the listing converted to that site's currency, while `/product` shows what the seller set. The product response carries no `service_fee` or `total_price`; take those from the search item. `feedback_reputation` is 0-1 (`0.98` is 98%), not a star rating. `uploaded_relative` is Vinted's own wording ("4 days ago"), not a timestamp. A sold listing still returns its last `price` with `is_sold: true`, `status_label: "Sold"` and `can_buy: false`.

### Seller

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "uk", "user_id": 65958245}'
```

Captured `data`:

```json
{
  "country": "uk",
  "id": 65958245,
  "login": "dw_clothing",
  "profile_url": "https://www.vinted.co.uk/member/65958245-dwclothing",
  "is_business": true,
  "feedback_count": 239,
  "feedback_reputation": 1,
  "positive_feedback_count": 238,
  "neutral_feedback_count": 0,
  "negative_feedback_count": 1,
  "item_count": 16,
  "country_code": "UK",
  "country_name": "United Kingdom",
  "city": null,
  "verification": { "email": true, "facebook": false, "google": true },
  "avg_response_time": null,
  "is_on_holiday": false,
  "last_seen_date": "2026-11-09"
}
```

This is a business seller (`is_business: true`). `feedback_reputation: 1` sits next to one negative review: it is Vinted's own score, not a share of the counts, so quote the counts when the user asks about complaints. `city` is `null` because the member does not show it; `last_seen_date` is a day, never a time.

### Seller products

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/seller-products \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "uk", "user_id": 65958245, "limit": 10}'
```

Captured `data` (9 of 10 items and 7 of 8 photos trimmed):

```json
{
  "country": "uk",
  "user_id": 65958245,
  "sort": "newest_first",
  "page": 1,
  "per_page": 10,
  "total_results": 16,
  "total_pages": 2,
  "count": 10,
  "has_more": true,
  "items": [
    {
      "id": 10726905690,
      "title": "Barbour Ashby Wax Jacket Olive Size XXL (RRP £269)",
      "url": "https://www.vinted.co.uk/items/10726905690-barbour-ashby-wax-jacket-olive-size-xxl-rrp-ps269",
      "price": 155,
      "currency": "GBP",
      "price_with_discount": null,
      "service_fee": 8.45,
      "total_price": 163.45,
      "brand": "Barbour",
      "size": "XXL",
      "condition": "Very good",
      "favourite_count": 7,
      "is_reserved": false,
      "is_sold": false,
      "is_promoted": false,
      "image": "https://images1.vinted.net/t/02_00de3_5cVMYc3SD5QKM3yYzRdKiaab/f800/fcf7ff42.jpeg?s=f8d6a2b25591dd5c590fa22482f27979fcebd3b3",
      "photos": [
        "https://images1.vinted.net/t/02_00de3_5cVMYc3SD5QKM3yYzRdKiaab/f800/fcf7ff42.jpeg?s=f8d6a2b25591dd5c590fa22482f27979fcebd3b3"
      ]
    }
  ]
}
```

`total_results` (16) matches the profile's `item_count`. Seller-products items have no `seller` block (they are all this member's) and no `thumbnail`.

### Seller feedback

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/seller-feedback \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "uk", "user_id": 65958245, "limit": 10}'
```

Captured `data` (8 of 10 rows trimmed):

```json
{
  "country": "uk",
  "user_id": 65958245,
  "page": 1,
  "per_page": 10,
  "total_results": 239,
  "total_pages": 24,
  "count": 10,
  "has_more": true,
  "feedback": [
    { "id": 4705059523, "rating": 5, "text": "Excellent jacket and great seller very happy with my purchase", "created_at": "2026-11-07T22:02:28.000Z", "is_automatic": false, "seller_reply": null },
    { "id": 4696195757, "rating": 5, "text": "Auto-feedback: Sale completed successfully", "created_at": "2026-11-06T15:36:45.000Z", "is_automatic": true, "seller_reply": null }
  ]
}
```

8 of the 10 rows on this page are Vinted's automatic feedback (`is_automatic: true`, "Auto-feedback: Sale completed successfully"), not words a buyer wrote. Filter them out before quoting what buyers said. Rows carry no reviewer and no item, by design.

### Brands

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/brands \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "uk", "query": "barbour"}'
```

Captured `data` (7 of 10 brands trimmed):

```json
{
  "country": "uk",
  "query": "barbour",
  "count": 10,
  "brands": [
    { "id": 46805, "title": "Barbour", "slug": "barbour", "url": "https://www.vinted.co.uk/brand/46805-barbour", "item_count": 1021628, "is_luxury": true, "requires_authenticity_check": true },
    { "id": 959088, "title": "Barbour International", "slug": "barbour-international", "url": "https://www.vinted.co.uk/brand/959088-barbour-international", "item_count": 24217, "is_luxury": false, "requires_authenticity_check": false },
    { "id": 179640, "title": "Barbouillage", "slug": "barbouillage", "url": "https://www.vinted.co.uk/brand/179640-barbouillage", "item_count": 21734, "is_luxury": false, "requires_authenticity_check": false }
  ]
}
```

Matching is fuzzy: the same answer also lists `Barbara Lebek`, `Hanna Barbera` and `Augustinus Bader`. Pick the exact `title`, and include sub-brands (Barbour International, Barbour Heritage) in `brand_ids` only when the user wants them.

### Filters

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/filters \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "us", "filter": "status"}'
```

Captured `data` (3 of 5 options trimmed):

```json
{
  "country": "us",
  "filter": "status",
  "search_param": "status_ids",
  "query": null,
  "category_id": null,
  "count": 5,
  "options": [
    { "id": 6, "title": "New with tags", "item_count": 34538, "description": "A brand-new, unused item with tags attached or in the original packaging." },
    { "id": 2, "title": "Very good", "item_count": 83802, "description": "A lightly used item that may have slight imperfections, but still looks great." }
  ]
}
```

`search_param` names the search parameter the option ids go into. `item_count` is a live count for this filter, query and category on that site.

### Suggestions and categories

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "uk", "query": "barb"}'
```

Captured `data` (6 of 10 suggestions trimmed):

```json
{
  "country": "uk",
  "query": "barb",
  "count": 10,
  "suggestions": [
    { "text": "barbour women's", "type": "brand+parent_cat" },
    { "text": "barbour men", "type": "brand+parent_cat" },
    { "text": "barbour men’s jacket", "type": "popular_search" },
    { "text": "barbie house", "type": "popular_search" }
  ]
}
```

```bash
curl -X POST https://api.scavio.dev/api/v1/vinted/categories \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "uk", "parent_id": 1904}'
```

Captured `data` (4 of 5 top-level children and most of the subtree trimmed):

```json
{
  "country": "uk",
  "parent": {
    "id": 1904,
    "title": "Women",
    "url": "https://www.vinted.co.uk/catalog/1904-women",
    "path": [{ "id": 1904, "title": "Women" }]
  },
  "count": 273,
  "categories": [
    {
      "id": 4,
      "title": "Clothing",
      "url": "https://www.vinted.co.uk/catalog/4-clothing",
      "children": [
        {
          "id": 1037,
          "title": "Outerwear",
          "url": "https://www.vinted.co.uk/catalog/1037-outerwear",
          "children": [
            { "id": 1773, "title": "Capes & ponchos", "url": "https://www.vinted.co.uk/catalog/1773-capes-and-ponchos", "children": [] },
            { "id": 1907, "title": "Coats", "url": "https://www.vinted.co.uk/catalog/1907-coats", "children": [] }
          ]
        }
      ]
    }
  ]
}
```

`count` (273) is every category in the subtree, not just the 5 direct children (Clothing, Shoes, Bags, Accessories, Beauty). A leaf has `children: []`. Without `parent_id` the whole tree is about 3,000 categories.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def vinted(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/vinted/{endpoint}", headers=HEADERS, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["data"]

# 1. Resolve the brand id (1 credit)
brand = next(b for b in vinted("brands", {"country": "uk", "query": "barbour"})["brands"] if b["title"] == "Barbour")

# 2. Newest Barbour listings in Very good or better, under 100 GBP (1 credit)
found = vinted("search", {"country": "uk", "brand_ids": [brand["id"]], "status_ids": [6, 1, 2],
                          "price_to": 100, "sort": "newest_first"})
print("applied:", found["filters"]["brand_ids"], found["filters"]["status_ids"])
for it in found["items"][:10]:
    print(it["total_price"], it["currency"], it["title"], it["url"])

# 3. Check the seller of the first hit (2 credits)
sid = found["items"][0]["seller"]["id"]
profile = vinted("seller", {"country": "uk", "user_id": sid})
reviews = vinted("seller-feedback", {"country": "uk", "user_id": sid, "limit": 50})
written = [f for f in reviews["feedback"] if not f["is_automatic"]]
print(profile["feedback_count"], profile["negative_feedback_count"], len(written), "written reviews on this page")
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Listings, profiles and feedback are fetched live; the category tree is refreshed at most every 12 hours per site.

- **search** - `country`, `currency`, `query`, `page`, `per_page` (96), `count`, `listed_results`, `total_is_capped`, `total_pages`, `has_more`, `items[]` {`id`, `title`, `url`, `price`, `currency`, `price_with_discount`, `service_fee`, `total_price`, `brand`, `size`, `condition`, `favourite_count`, `is_promoted`, `image`, `thumbnail`, `photos[]`, `seller` {`id`, `is_business`}}, `filters` {`query`, `category_ids[]`, `brand_ids[]`, `status_ids[]`, `size_ids[]`, `color_ids[]`, `material_ids[]`, `price_from`, `price_to`, `currency`, `sort`}.
- **product** - `country`, `id`, `url`, `title`, `description`, `description_translated`, `price`, `currency`, `brand` {`id`, `name`}, `size`, `condition`, `color`, `material`, `uploaded_relative`, `category` {`id`, `name`, `path[]` {`id`, `title`, `url`}}, `photos[]`, `favourite_count`, `is_reserved`, `is_sold`, `status_label`, `can_buy`, `instant_buy`, `is_hidden`, `seller` {`id`, `login`, `profile_url`, `is_business`, `feedback_count`, `feedback_reputation`, `badges[]`}.
- **seller** - `country`, `id`, `login`, `profile_url`, `is_business`, `feedback_count`, `feedback_reputation`, `positive_feedback_count`, `neutral_feedback_count`, `negative_feedback_count`, `item_count`, `country_code`, `country_name`, `city`, `verification` {`email`, `facebook`, `google`}, `avg_response_time`, `is_on_holiday`, `last_seen_date`.
- **seller-products** - `country`, `user_id`, `sort`, `page`, `per_page`, `total_results`, `total_pages`, `count`, `has_more`, `items[]` {`id`, `title`, `url`, `price`, `currency`, `price_with_discount`, `service_fee`, `total_price`, `brand`, `size`, `condition`, `favourite_count`, `is_reserved`, `is_sold`, `is_promoted`, `image`, `photos[]`}.
- **seller-feedback** - `country`, `user_id`, `page`, `per_page`, `total_results`, `total_pages`, `count`, `has_more`, `feedback[]` {`id`, `rating`, `text`, `created_at`, `is_automatic`, `seller_reply`}.
- **brands** - `country`, `query`, `count`, `brands[]` {`id`, `title`, `slug`, `url`, `item_count`, `is_luxury`, `requires_authenticity_check`}.
- **suggestions** - `country`, `query`, `count`, `suggestions[]` {`text`, `type`}.
- **filters** - `country`, `filter`, `search_param`, `query`, `category_id`, `count`, `options[]` {`id`, `title`, `item_count`, plus `group` on sizes (`"Women > Women's items"`) and `description` on conditions}.
- **categories** - `country`, `parent` ({`id`, `title`, `url`, `path[]`} or absent for the whole tree), `count`, `categories[]` {`id`, `title`, `url`, `children[]`}.

## Guardrails

- Prices are in the site's currency on search and seller-products (`price: 85` with `currency: "GBP"` is £85.00), and in the seller's currency on `/product`. Always say the currency. On the EU sites the same listing is shown converted into each site's currency, so do not compare a `pl` price in PLN with an `fr` price in EUR as if they were different listings.
- `service_fee` is the Vinted fee the buyer pays on top of the price (formerly the Buyer Protection fee; renamed in Vinted's terms of 2026-10-08), and `total_price` is price plus that fee. Shipping is not included and there is no shipping price, pickup point or delivery option data. Say "before shipping" when quoting `total_price`.
- Search pages are always 96 items and stop at page 10. `listed_results` tops out at 960 and `total_is_capped: true` then means "960 or more", never an exact market size. To reach listings beyond the cap, narrow by category, brand, size or price range and search each slice.
- Price sorts (`price_low_to_high`, `price_high_to_low`) also rank loosely matching listings, including very cheap or placeholder-priced ones. Pair a price sort with a `category_id`, `brand_ids` or a `price_from` / `price_to` range, and read titles before calling anything the cheapest.
- Sold items are not searchable. Search returns live listings only, so there are no sold comps, sale prices or sell-through rates. A sold listing can still be read by id on `/product` (`is_sold: true`, last price kept), but that is one listing, not a sales history. Quote asks as asking prices, never as what items sold for.
- `is_promoted: true` marks a promoted listing. Report it when the order of results matters.
- Read the search response's `filters` echo. If an id you sent is missing there, Vinted did not apply it; say so.
- Category names, conditions, filter titles and suggestions are in the site's language. Ids are shared across sites.
- `feedback_reputation` is a 0-1 score (`0.98` is 98%) and is Vinted's own score: `1` can sit beside a negative review. Use the positive / neutral / negative counts for complaints.
- Automatic feedback (`is_automatic: true`, text such as "Auto-feedback: Sale completed successfully") is generated by Vinted, not written by a buyer. Exclude it when summarizing what buyers said.
- Seller data is limited on purpose to public, buyer-relevant fields: no real name, contact details, address or exact last-online time (`last_seen_date` is a day), and `city` only when the member shows it. Feedback rows carry no reviewer identity and no item. Most Vinted sellers are private individuals: use these endpoints to judge a seller before a purchase, not to follow, profile or contact a person, and do not try to identify reviewers.
- `/seller-products` with an unknown member id usually returns an empty list rather than a 404; check `/seller` when the id itself is in doubt.
- There are no similar-item, trending, item view count, sold-listing, shipping or pickup-point endpoints, and this API cannot post, edit, buy, message or manage listings. Do not claim any of them, and do not present it as a buying or auto-purchase bot.
- Never fabricate prices, fees, listings or seller data. Only return what the API returned, with the listing `url` or `id`.

## Failure handling

- `400` means a missing or invalid parameter (an unknown `country`; no `query` on `/search` without `category_id` or `brand_ids`; `price_from` above `price_to`; more than one `category_id`; more than 20 ids in a list; a `status_ids` value that is not a condition id; neither `item_id` nor `url`, or a `url` that is not a Vinted `/items/<id>` URL, or an `item_id` and `url` naming different items; a `user_id` that is not numeric; `page` or `limit` out of range; a `filter` other than `size`, `status`, `color` or `material`; a missing `query` on `/brands` or `/suggestions`; or a `/filters` request Vinted rejects, usually a bad `category_id`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such item on that site, no such member, or no such category. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api).
- `502` or `503` means Vinted is temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.

## SDKs

```bash
pip install scavio==0.41.0
npm install scavio@0.42.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: brands } = await scavio.vinted.brands({ country: "uk", query: "barbour" });
const { data: found } = await scavio.vinted.search({ country: "uk", brand_ids: [brands.brands[0].id], sort: "newest_first" });
const { data: item } = await scavio.vinted.product({ country: "uk", item_id: found.items[0].id });
const { data: seller } = await scavio.vinted.seller({ country: "uk", user_id: 65958245 });
const { data: stock } = await scavio.vinted.sellerProducts({ country: "uk", user_id: 65958245, limit: 96 });
const { data: reviews } = await scavio.vinted.sellerFeedback({ country: "uk", user_id: 65958245, limit: 50 });
const { data: sizes } = await scavio.vinted.filters({ country: "uk", filter: "size", category_id: 1904 });
const { data: tree } = await scavio.vinted.categories({ country: "uk", parent_id: 1904 });
const { data: typed } = await scavio.vinted.suggestions({ country: "uk", query: "barb" });
```

Python uses the same namespace with snake_case methods: `client.vinted.search(...)`, `product`, `seller`, `seller_products`, `seller_feedback`, `brands`, `suggestions`, `filters`, `categories`.

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_vinted`, `get_vinted_product`, `get_vinted_seller`, `get_vinted_seller_products`, `get_vinted_seller_feedback`, `get_vinted_brands`, `get_vinted_suggestions`, `get_vinted_filters` and `get_vinted_categories`. Vinted is opt-in: add `vinted` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.39.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,vinted"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/vinted-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [product](https://scavio.dev/docs/vinted-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [seller](https://scavio.dev/docs/vinted-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [seller products](https://scavio.dev/docs/vinted-seller-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [seller feedback](https://scavio.dev/docs/vinted-seller-feedback?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [brands](https://scavio.dev/docs/vinted-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [suggestions](https://scavio.dev/docs/vinted-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [filters](https://scavio.dev/docs/vinted-filters?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api), [categories](https://scavio.dev/docs/vinted-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api). Overview: [Vinted API](https://scavio.dev/vinted-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=vinted-api).
