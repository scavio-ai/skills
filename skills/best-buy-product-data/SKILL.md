---
name: best-buy-product-data
description: "Best Buy product data API: search bestbuy.com or browse any category or deals page, 18 products per page, with price, regular price, savings, deal badge, condition, rating and seller type, filtered by brand, on sale, clearance, open box or a price range, read one product by SKU with UPC, model, every open-box offer by condition (fair, good, excellent) with its price and savings against new and regular, the full spec table and the AI review summary, check store pickup status (in stock, limited, ship to store, out of stock) of a SKU at up to 8 stores near a ZIP, find stores with 35 days of dated hours, get today's Deal of the Day, batch prices for up to 15 SKUs, page first-party reviews with the star histogram and pros and cons, and pull search autocomplete. 9 endpoints, 2 credits each; stores and suggestions 1, deals and pcmcat category pages 3."
version: 1.0.0
tags: best-buy, bestbuy, best-buy-api, best-buy-product-data, best-buy-scraper, best-buy-open-box, open-box-prices, best-buy-price-tracker, price-drop-alerts, best-buy-stock-checker, in-stock-tracker, store-pickup, in-store-availability, deal-of-the-day, best-buy-deals, clearance, electronics, consumer-electronics, tvs, laptops, gaming, upc, sku-data, product-specs, product-search, product-data, product-reviews, review-analysis, category-browse, store-locator, store-hours, batch-prices, autocomplete, retail, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/bestbuy-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data
---

# Best Buy Product Data API - Open-Box Prices, Store Stock, Deals, Reviews

Search Best Buy (bestbuy.com, US) by keyword, or browse a category or deals page by category id or URL (catalogue categories such as `abcat0101001` All Flat-Screen TVs, and merchandised pages such as `pcmcat1674241939957` All Electronics on Sale), 18 organic products per page, sorted by best match, best selling, best discount, price, rating or newest, filtered by brand, on sale, clearance, open box or a price range: SKU, BSIN, name, brand, model number, URL, image, current price, regular price, savings in dollars and percent, on-sale flag, the deal badge (`Holiday Deal`, `BlackFriday`, `Doorbuster`...) and deal end time, condition, rating, review count, seller type (`best_buy` or `marketplace`), product type, badges and release date, plus the total result count, the filter sidebar with product counts, the sort options and related searches. Read one product by SKU or URL with its UPC, model, status, category path, price block, financing offer, every open-box offer by condition (fair, good, excellent) with its price and its savings against new and against the regular price, other conditions and sellers of the same product, the AI review summary and what customers love, description, features, what is included, the full specification table by group, dimensions, images and manuals. Check one SKU's store pickup status at up to 8 Best Buy stores (the stores nearest a ZIP, or store ids you pass): in stock, limited (with the real count when Best Buy shows "only N left"), ship to store, out of stock, not available for pickup, or unknown with a reason, plus the pickup date. Find the stores near a ZIP with 35 days of dated opening hours, get today's Deal of the Day and the more-deals row with live prices, price up to 15 SKUs in one call, page Best Buy's own customer reviews 20 at a time with the star histogram, recommended percent and the most mentioned pros and cons, and pull the search box's autocomplete. All endpoints return structured JSON.

See also: for PC parts with per-store stock counts and open-box units at Micro Center use the `micro-center-api` skill; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Find TVs, laptops, phones, gaming, appliances or any product at Best Buy by keyword, and compare prices, savings, ratings and brands
- Track Best Buy prices or price drops on a list of SKUs, or build a Best Buy price tracker (one `/prices` call covers up to 15 SKUs)
- Get Best Buy open-box prices by condition (fair, good, excellent) and how much each saves against new and against the regular price
- Check whether a Best Buy item is in stock for store pickup near a ZIP code, or at specific stores, for an in-stock tracker or restock monitor
- Get today's Best Buy Deal of the Day and the other deals on that page with live prices
- List a Best Buy category or deals page (All Electronics on Sale, clearance, open-box only) sorted by best discount or price
- Read the UPC, model number and full specification table of a Best Buy product
- Find Best Buy stores near a ZIP code with their hours, including holiday hours and closed days
- Read what Best Buy reviewers say, pull only the 1-star reviews, the newest reviews, or the most mentioned pros and cons
- Get Best Buy search autocomplete suggestions for keyword research

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most endpoints in this skill cost 2 credits (stores and suggestions 1, deals and pcmcat category pages 3), so the free credits cover about 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most calls take 2-6 seconds; `/availability` takes 5-20 seconds (it checks each store in turn), so allow a client timeout of at least 60 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/bestbuy/search` | 2 | 18 organic products per page: position, SKU, BSIN, name, brand, model, URL, image, price, regular price, savings and savings percent, on-sale flag, deal badge, deal end time, condition, rating, review count, seller type, product type, badges, release date. Plus total results and pages, the applied sort and filters, the category, the filter sidebar (`facets[]` with values and counts), sort options, related searches and any spelling correction |
| `POST /api/v1/bestbuy/category` | 2 for an `abcat` id, 3 for a `pcmcat` page | One category or deals page by `category_id` or URL, 18 products per page in the same shape as search, with the same filters and sorts (no `best_match`) |
| `POST /api/v1/bestbuy/product` | 2 | One product by SKU or URL: SKU, BSIN, name, brand, model, UPC, URL, status, condition, product type, category path, price block, financing, `open_box[]` per condition (fair, good, excellent) with price, savings vs new, savings vs regular, savings percent and URL, seller type, other offers, rating, review count, AI review summary, what customers love, description, features, included items, specifications, dimensions, images, manuals, badges, release date |
| `POST /api/v1/bestbuy/reviews` | 2 | One product's Best Buy reviews, 20 per page, sorted or filtered to one star rating: average rating, review count, recommended percent, star distribution, pros and cons with mention counts, total results for the filter, page count and `has_more`. Each review: id, title, text, rating, author, date, recommended, verified-purchase and incentivized flags, days of ownership, helpful and not-helpful votes, badges, photos, syndication source, the SKU reviewed when it is a sibling SKU, and the brand's response |
| `POST /api/v1/bestbuy/availability` | 2 | Store pickup status of one SKU at up to 8 stores (nearest a ZIP, default 5, or the `store_ids` you pass): status, quantity (only for `limited`), pickup date, minimum hours until pickup, the nearby store Best Buy suggests when this one cannot fill it, and a reason when the status is `unknown`. Plus store and in-stock counts and a count per status |
| `POST /api/v1/bestbuy/stores` | 1 | Best Buy stores near a US ZIP, nearest first, up to 15: store id, name, address, city, state, ZIP, country, phone, open status, store type, distance in miles, and dated hours for the next 35 days (holiday hours and closed days included) |
| `POST /api/v1/bestbuy/deals` | 3 | Today's Deal of the Day and the more-deals row under it, up to 15 products with live prices: SKU, name, URL, image, rating, review count, price, regular price, savings, savings percent, on-sale flag, badge, deal end time, plus the page's countdown end. No parameters |
| `POST /api/v1/bestbuy/prices` | 2 per call | Current prices for 1-15 SKUs in one call: price, regular price, savings, savings percent, on-sale flag and deal badge per SKU (`deal_ends_at` is usually null here; read the end time from `/product`), `found: false` for a SKU Best Buy does not know |
| `POST /api/v1/bestbuy/suggestions` | 1 | The search box's autocomplete for a partial term: each suggested term with the categories (id and name) and SKUs Best Buy shows for it, plus any spelling correction |

## Workflow

1. **Find products:** call `/bestbuy/search` with `query`, or `/bestbuy/category` with a `category_id` (or a category page `url`). Each row has a `sku` and a `url`. To drill down, take a `category_id` from the `category_facet` values in `facets[]`, or a category id from a product's `category_path[]`.
2. **Narrow the listing:** pass `filters` (`brand`, `on_sale`, `clearance`, `open_box`, and `min_price` with `max_price`) and a `sort` such as `best_discount` or `price_low`. `applied_filters[]` echoes what Best Buy applied. The `brand` value must be spelled as in the Brand filter (a `brand_facet` value).
3. **One product in full:** call `/bestbuy/product` with the row's `sku` (or its `url`). Read `open_box[]` for each open-box condition's price, `specifications[]` for the spec table, and `upc` and `model` for matching against other retailers.
4. **Store pickup:** call `/bestbuy/availability` with the `sku` and the user's `zip` (and `max_stores`, up to 8), or with `store_ids` from a `/bestbuy/stores` answer. Read each store's `status` and `pickup_date`.
5. **Store hours:** call `/bestbuy/stores` with the `zip` for addresses, phone numbers and dated hours; a store's `store_id` feeds `store_ids` on `/availability`.
6. **Price tracking:** keep a list of SKUs and call `/bestbuy/prices` with up to 15 at a time. Compare `price` across runs to detect a drop; `badge` and `deal_ends_at` say which deal applies and when it ends when Best Buy publishes it.
7. **Daily deals:** call `/bestbuy/deals` once a day for the Deal of the Day (`deal_of_the_day`) and the rest of the row (`deals[]`).
8. **Reviews:** call `/bestbuy/reviews` with the `sku`; page with `page`, sort with `sort` (`newest`, `lowest_rated`...) or keep one star rating with `rating`. Check `has_more` and `total_results`.
9. **Keyword research:** `/bestbuy/suggestions` with a partial term returns the suggested terms with category ids and SKUs; feed a term back into `/bestbuy/search` or a SKU into `/bestbuy/product`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-100). 18 products per page |
| `sort` | string | `best_match` | `best_match`, `best_selling`, `best_discount`, `price_low`, `price_high`, `rating` or `newest` |
| `filters` | object | none | `brand` (string, as spelled in the Brand filter), `on_sale` (boolean), `clearance` (boolean), `open_box` (boolean), `min_price` and `max_price` (dollars, pass both, `min_price` below `max_price`). Combine freely |
| `include_sponsored` | boolean | `false` | Also return the sponsored tiles Best Buy mixes into the grid, flagged `sponsored: true` with `position: null` |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | one of | Best Buy category id: `abcat` plus 7 digits (catalogue categories, e.g. `abcat0101001` All Flat-Screen TVs), `pcmcat` plus digits (merchandised pages, e.g. `pcmcat1674241939957` All Electronics on Sale), or `cat` plus digits |
| `url` | string | one of | A bestbuy.com category page URL (`.../<id>.c?id=<id>`), used when `category_id` is not given. Filters in the URL (`qp=...`) are kept; its sort is not, use `sort` |
| `page` | integer | 1 | Results page, 1-based (1-100). 18 products per page |
| `sort` | string | page default | `best_selling` (the default on most pages), `best_discount`, `price_low`, `price_high`, `rating` or `newest`. `best_match` is search-only |
| `filters` | object | none | The same as search |
| `include_sponsored` | boolean | `false` | The same as search |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | Best Buy SKU, the 6-9 digit number after `/sku/` in a product URL (a result's `sku`, e.g. `6607832`) |
| `url` | string | one of | bestbuy.com product URL that names a SKU: `/product/<name>/<id>/sku/<sku>` or `/site/<name>/<sku>.p?skuId=<sku>`. Used when `sku` is not given |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | Best Buy SKU |
| `url` | string | one of | bestbuy.com product URL that names a SKU, used when `sku` is not given |
| `page` | integer | 1 | Reviews page, 1-based (1-500). 20 reviews per page |
| `sort` | string | `most_relevant` | `most_relevant`, `most_helpful`, `newest`, `oldest`, `highest_rated` or `lowest_rated` |
| `rating` | integer | all | Only reviews with this many stars, 1-5 |

### Availability (`/availability`)

Pass `sku` or `url`, and exactly one of `zip` or `store_ids`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | Best Buy SKU |
| `url` | string | one of | bestbuy.com product URL that names a SKU, used when `sku` is not given |
| `zip` | string | one of | US ZIP code: check the stores nearest it (`94103` or `94103-1234`) |
| `max_stores` | integer | 5 | With `zip`: how many of the nearest stores to check, 1-8 |
| `store_ids` | array or string | one of | Check these stores instead: Best Buy store numbers (a `/stores` result's `store_id`), an array or a comma-separated string, up to 8 |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | US ZIP code (`94103` or `94103-1234`). There is no latitude/longitude or radius parameter |

### Deals (`/deals`)

No parameters: send `{}`.

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skus` | array or string | required | 1-15 Best Buy SKUs, an array (`["6607832", "6673112"]`) or a comma-separated string |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

## Examples

### Product with open-box prices

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "6607832"}'
```

Captured `data` (13 of 14 features, 4 of 7 included items, 92 of 95 specifications, 15 of 16 images, 6 of 7 manuals and 2 of 4 "what customers love" lines trimmed; the description shortened):

```json
{
  "sku": "6607832",
  "bsin": "J2FPJKSV76",
  "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
  "brand": "Insignia™",
  "model": "NS-55F501NA26",
  "upc": "600603311888",
  "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832",
  "status": "active",
  "condition": "new",
  "product_type": "Televisions",
  "category_path": [
    { "id": "abcat0100000", "name": "TV & Home Theater", "url": "https://www.bestbuy.com/site/electronics/tv-home-theater/abcat0100000.c?id=abcat0100000" },
    { "id": "abcat0101000", "name": "TVs", "url": "https://www.bestbuy.com/site/tv-home-theater/tvs/abcat0101000.c?id=abcat0101000" },
    { "id": "abcat0101001", "name": "All Flat-Screen TVs", "url": "https://www.bestbuy.com/site/tvs/all-flat-screen-tvs/abcat0101001.c?id=abcat0101001" }
  ],
  "price": 189.99,
  "regular_price": 349.99,
  "savings": 160,
  "savings_percent": 45,
  "on_sale": true,
  "badge": "Holiday Deal",
  "deal_ends_at": "2026-11-08T23:59:59 CST",
  "financing": null,
  "open_box": [
    { "condition": "fair", "price": 165.99, "savings_vs_new": 24, "savings_vs_regular": 184, "savings_percent": 52, "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832/openbox?condition=fair" },
    { "condition": "good", "price": 171.99, "savings_vs_new": 18, "savings_vs_regular": 178, "savings_percent": 50, "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832/openbox?condition=good" },
    { "condition": "excellent", "price": 176.99, "savings_vs_new": 13, "savings_vs_regular": 173, "savings_percent": 49, "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832/openbox?condition=excellent" }
  ],
  "seller_type": "best_buy",
  "other_offers": [],
  "rating": 4.6,
  "review_count": 4031,
  "review_summary": "Customers admire the excellent picture quality, ease of setup, and ideal size of the 55\" Class F50 Series LED 4K UHD Smart Fire TV. The lightweight design is also appreciated by some users. However, a few customers have noted that the button layout could be more user-friendly and the volume could be improved.",
  "what_customers_love": ["Picture quality looks vibrant and impressive", "Sets up quickly right out of the box"],
  "description": "This 55-inch screen uses 4K Ultra HD technology for vibrant, true-to-life images. HDR10 contrasts bright highlights with dark shadows, so you can catch subtle details. ...",
  "features": [
    { "title": "4k Ultra HD (2160p resolution)", "description": "Enjoy breathtaking HDR10 4K movies and TV shows at 4 times the resolution of Full HD, and upscale your current content to Ultra HD-level picture quality." }
  ],
  "included_items": ["Insignia 55\" Class F50 Series LED 4K UHD Smart Fire TV", "Voice Remote with Alexa", "Batteries (AAA*2)"],
  "specifications": [
    { "group": "Key Specs", "name": "Display Type", "value": "LED" },
    { "group": "Key Specs", "name": "Resolution", "value": "4K (2160p)" },
    { "group": "Key Specs", "name": "Screen Size Class", "value": "55 inches" }
  ],
  "dimensions": { "height": null, "width": "48.4 inches", "depth": null, "weight": null },
  "images": ["https://pisces.bbystatic.com/image2/BestBuy_US/images/products/2c3f0bff-9d72-4850-97ac-879cc3cd8162.jpg"],
  "manuals": [
    { "type": "Warranty Manual", "url": "https://files.bbystatic.com/xR%2BLqpEeZ1WAOL8A%2FGIPkQ%3D%3D/b6e4c80f-2b83-4f4b-b780-e87ba5bd3091" }
  ],
  "badges": ["Best Selling", "Trending Deal", "A Best Buy brand", "A Best Buy Brand"],
  "release_date": "2025-05-01"
}
```

Read the open-box rows as: new is $189.99 on sale (regular $349.99); open-box fair is $165.99, which is $24 below the new sale price and $184 below the regular price (52% off regular). `open_box[]` is sorted by price, cheapest first, and lists only the conditions Best Buy offers right now; it is an empty list when there is no open-box offer.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "tv"}'
```

Captured `data` for `{"query": "tv"}` (17 of 18 products, 26 of 28 facets and 2 of the category facet's 4 values trimmed):

```json
{
  "query": "tv",
  "page": 1,
  "page_size": 18,
  "total_results": 1417,
  "total_pages": 79,
  "sort": "best_match",
  "category": { "id": "abcat0101000", "name": "TVs" },
  "applied_filters": [],
  "corrected_query": null,
  "redirect_url": null,
  "count": 18,
  "sponsored_count": 6,
  "products": [
    {
      "position": 2,
      "sponsored": false,
      "sku": "6607832",
      "bsin": "J2FPJKSV76",
      "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
      "brand": "Insignia",
      "model": "NS-55F501NA26",
      "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832",
      "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/2c3f0bff-9d72-4850-97ac-879cc3cd8162.jpg",
      "price": 189.99,
      "regular_price": 349.99,
      "savings": 160,
      "savings_percent": 45,
      "on_sale": true,
      "badge": "Holiday Deal",
      "deal_ends_at": "2026-11-08T23:59:59 CST",
      "condition": "new",
      "rating": 4.6,
      "review_count": 4031,
      "seller_type": "best_buy",
      "product_type": "Television",
      "badges": ["Best Selling", "Trending Deal", "A Best Buy brand", "A Best Buy Brand"],
      "release_date": "2025-05-01"
    }
  ],
  "facets": [
    {
      "field": "category_facet",
      "name": "Category",
      "value_count": 4,
      "values": [
        { "value": "All Flat-Screen TVs", "count": null, "category_id": "abcat0101001" },
        { "value": "Frame TVs", "count": null, "category_id": "pcmcat1769545828021" }
      ]
    },
    {
      "field": "condition_facet",
      "name": "Condition",
      "value_count": 3,
      "values": [
        { "value": "New", "count": 1937 },
        { "value": "Open-Box", "count": 80 },
        { "value": "Refurbished", "count": 54 }
      ]
    }
  ],
  "sort_options": ["best_match", "best_selling", "best_discount", "price_low", "price_high", "rating", "newest"],
  "related_searches": ["laptop", "monitor", "ps5", "ipad", "xbox"]
}
```

`count: 18` is the organic products on the page; the 6 sponsored tiles on the same page (`sponsored_count: 6`) were left out because `include_sponsored` was not set. The category facet's values carry `category_id`s to pass to `/category`, and `count: null` there because the site shows no count for them.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "abcat0101001"}'
```

The captured page for All Flat-Screen TVs (`total_results: 1329`, `total_pages: 74`, `sort: "best_selling"`, `sponsored_count: 0`, 31 facets) has the same envelope as search with `category_id` in place of `query`. Its first row:

```json
{
  "position": 1,
  "sponsored": false,
  "sku": "6685581",
  "bsin": "J3Z9Z424FK",
  "name": "Hisense - 55\" Class QD5 Hi-QLED Series 4K UHD Smart Roku TV (2026)",
  "brand": "Hisense",
  "model": "55QD5SR",
  "url": "https://www.bestbuy.com/product/hisense-55-class-qd5-hi-qled-series-4k-uhd-smart-roku-tv-2026/J3Z9Z424FK/sku/6685581",
  "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/4044db39-586f-4074-8410-d8deefe260d7.png",
  "price": 179.99,
  "regular_price": 379.99,
  "savings": 200,
  "savings_percent": 52,
  "on_sale": true,
  "badge": "BlackFriday",
  "deal_ends_at": "2026-11-08T23:59:59 CST",
  "condition": "new",
  "rating": 4.1,
  "review_count": 12,
  "seller_type": "best_buy",
  "product_type": "Television",
  "badges": ["Best Selling", "Trending Deal", "Only at Best Buy"],
  "release_date": null
}
```

For open-box listings, add `"filters": {"open_box": true}`; for the biggest markdowns first, `"sort": "best_discount"`.

### Availability

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "6607832", "zip": "94103", "max_stores": 3}'
```

Captured `data`:

```json
{
  "sku": "6607832",
  "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
  "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76",
  "zip": "94103",
  "store_count": 3,
  "in_stock_count": 3,
  "status_counts": { "in_stock": 3 },
  "stores": [
    { "store_id": "187", "name": "San Francisco (13th and Harrison St.)", "zip": "94103", "distance_miles": 0.4, "status": "in_stock", "quantity": null, "pickup_date": "2026-11-08", "min_pickup_hours": 1, "nearby_alternative": null, "reason": null },
    { "store_id": "873", "name": "Colma", "zip": "94014", "distance_miles": 7.3, "status": "in_stock", "quantity": null, "pickup_date": "2026-11-08", "min_pickup_hours": 1, "nearby_alternative": null, "reason": null },
    { "store_id": "499", "name": "Emeryville", "zip": "94608", "distance_miles": 7.9, "status": "in_stock", "quantity": null, "pickup_date": "2026-11-08", "min_pickup_hours": 1, "nearby_alternative": null, "reason": null }
  ]
}
```

`quantity: null` on `in_stock` is expected: Best Buy publishes no unit count for a well-stocked item, so say "in stock for pickup today", never a number of units. The `url` here is a product-family URL (no `/sku/`), so pass `sku`, not this `url`, to the other endpoints.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "94103"}'
```

Captured `data` (14 of 15 stores and 32 of the first store's 35 days of hours trimmed; the closed day kept):

```json
{
  "zip": "94103",
  "count": 15,
  "stores": [
    {
      "store_id": "187",
      "name": "San Francisco (13th and Harrison St.)",
      "address": "1717 Harrison St",
      "address2": null,
      "city": "San Francisco",
      "state": "CA",
      "zip": "94103",
      "country": "US",
      "phone": "415-626-9682",
      "status": "Open",
      "store_type": "Big Box",
      "distance_miles": 0.4,
      "hours": [
        { "date": "2026-11-08", "open": "10:00", "close": "20:00", "closed": false },
        { "date": "2026-11-09", "open": "10:00", "close": "21:00", "closed": false },
        { "date": "2026-11-26", "open": null, "close": null, "closed": true }
      ]
    }
  ]
}
```

The hours are dated, so holiday changes show up on their own day: the same store opens 06:00-22:00 on 2026-11-27 and is closed on 2026-11-26.

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (13 of 14 more-deals rows trimmed):

```json
{
  "countdown_ends": "2026-11-09 00:00",
  "deal_of_the_day": {
    "sku": "6583282",
    "name": "Greenworks - 80-Volt 750 CFM Cordless Handheld Blower (1 x 2.5Ah Battery and 1 x Charger) - Green",
    "url": "https://www.bestbuy.com/product/greenworks-80-volt-750-cfm-cordless-handheld-blower-1-x-2-5ah-battery-and-1-x-charger-green/JJG744553Y",
    "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/c41493e7-fd16-42dc-976e-9d08e4e2defa.jpg",
    "rating": 4.4,
    "review_count": 167,
    "price": 99.99,
    "regular_price": 299.99,
    "savings": 200,
    "savings_percent": 66,
    "on_sale": true,
    "badge": null,
    "deal_ends_at": null
  },
  "count": 15,
  "deals": [
    {
      "sku": "6667482",
      "name": "HP - 14\" Laptop - Intel Processor N150 2025 - 4GB Memory - 128GB Storage - Willow Green",
      "url": "https://www.bestbuy.com/product/hp-14-laptop-intel-processor-n150-2025-4gb-memory-128gb-storage-willow-green/JJGW3FGF97",
      "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/d7fd5894-07b3-4182-bf0d-8332b09021ea.jpg",
      "rating": 4.3,
      "review_count": 47,
      "price": 204.99,
      "regular_price": 349.99,
      "savings": 145,
      "savings_percent": 41,
      "on_sale": true,
      "badge": null,
      "deal_ends_at": null
    }
  ]
}
```

`count: 15` includes the Deal of the Day: `deals[]` holds the other 14. `countdown_ends` is the countdown as the page shows it, with no time zone.

### Prices

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"skus": ["6607832", "6673112", "6679316"]}'
```

Captured `data`:

```json
{
  "count": 3,
  "requested": 3,
  "prices": [
    { "sku": "6607832", "found": true, "price": 189.99, "regular_price": 349.99, "savings": 160, "savings_percent": 45, "on_sale": true, "badge": "Holiday Deal", "deal_ends_at": null },
    { "sku": "6673112", "found": true, "price": 1399.99, "regular_price": 2699.99, "savings": 1300, "savings_percent": 48, "on_sale": true, "badge": "Holiday Deal", "deal_ends_at": null },
    { "sku": "6679316", "found": true, "price": 399.99, "regular_price": 599.99, "savings": 200, "savings_percent": 33, "on_sale": true, "badge": "BlackFriday", "deal_ends_at": null }
  ]
}
```

`count` is the SKUs found, `requested` the SKUs asked for. A SKU Best Buy does not know comes back `"found": false` with every price field null; the call is 2 credits whether it carries 1 SKU or 15.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "6607832", "sort": "newest"}'
```

Captured `data` (19 of 20 reviews trimmed; the review kept is one with a photo):

```json
{
  "sku": "6607832",
  "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
  "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832",
  "page": 1,
  "page_size": 20,
  "sort": "newest",
  "rating_filter": null,
  "average_rating": 4.6,
  "review_count": 4031,
  "recommended_percent": 93,
  "star_distribution": [
    { "stars": 5, "count": 3256, "percent": 81 },
    { "stars": 4, "count": 468, "percent": 12 },
    { "stars": 3, "count": 109, "percent": 3 },
    { "stars": 2, "count": 55, "percent": 1 },
    { "stars": 1, "count": 143, "percent": 3 }
  ],
  "pros": [
    { "feature": "Picture Quality", "mentions": 1917 },
    { "feature": "Setup Ease", "mentions": 245 },
    { "feature": "Size", "mentions": 119 },
    { "feature": "Weight", "mentions": 54 },
    { "feature": "Features", "mentions": 25 }
  ],
  "cons": [
    { "feature": "Volume", "mentions": 7 }
  ],
  "total_results": 4029,
  "total_pages": 202,
  "has_more": true,
  "count": 20,
  "reviews": [
    {
      "id": "91cb7bf0-99ed-35de-b712-95344c256523",
      "title": "Great picture, and color is perfect",
      "text": "I love my 55 inch tv. It shows good quality and sound",
      "rating": 5,
      "author": "SharonM",
      "submitted_at": "2026-11-06T21:34:48.000-06:00",
      "recommended": true,
      "verified_purchase": true,
      "incentivized": false,
      "days_of_ownership": 31,
      "helpful_count": 0,
      "not_helpful_count": 0,
      "badges": ["Incentivized", "Verified Purchaser"],
      "images": ["https://pisces.bbystatic.com/image2/BestBuy_US/ugc/photos/thumbnail/9646250637e1e3ca8f1bfa2a04e8c44a.jpg"],
      "syndicated_from": null,
      "reviewed_sku": null,
      "brand_response": null
    }
  ]
}
```

`review_count` (4,031) is the product's total; `total_results` (4,029) is what the review list returns for this request, so the two can differ slightly. In this capture every review carries an `"Incentivized"` badge while its `incentivized` flag is `false`: report the two as Best Buy gives them and do not infer one from the other.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "ps5 con"}'
```

Captured `data` (11 of 13 suggestions trimmed):

```json
{
  "query": "ps5 con",
  "corrected_query": null,
  "count": 13,
  "suggestions": [
    {
      "term": "ps5 controller",
      "categories": [{ "id": "pcmcat1546550106595", "name": "Gaming Controllers" }],
      "skus": ["6601464", "6430163", "6522931", "6497953", "6492317", "6464307", "6464309", "6669065", "6669064"]
    },
    {
      "term": "ps5 console disc",
      "categories": [],
      "skus": ["6646419", "6646420", "10413388", "12906125", "6601553", "12224139", "11939512", "6565695", "12348331"]
    }
  ]
}
```

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bestbuy(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/bestbuy/{endpoint}", headers=HEADERS, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["data"]

# 1. Biggest open-box markdowns in a category (2 credits)
found = bestbuy("category", {"category_id": "abcat0101001", "sort": "best_discount", "filters": {"open_box": True}})
for p in found["products"][:5]:
    print(p["sku"], p["name"], p["condition"], p["price"], "regular", p["regular_price"], p["badge"])

# 2. One product: open-box price per condition (2 credits)
item = bestbuy("product", {"sku": found["products"][0]["sku"]})
for ob in item["open_box"]:
    print(ob["condition"], ob["price"], "saves", ob["savings_vs_new"], "vs new,", ob["savings_vs_regular"], "vs regular")

# 3. Store pickup near the user (2 credits, 5-20 s)
avail = bestbuy("availability", {"sku": item["sku"], "zip": "94103", "max_stores": 5})
for s in avail["stores"]:
    qty = f' (only {s["quantity"]} left)' if s["status"] == "limited" else ""
    print(s["name"], s["distance_miles"], "mi:", s["status"] + qty, "pickup", s["pickup_date"], s["reason"] or "")

# 4. Price check for a watch list, up to 15 SKUs per call (2 credits)
watch = bestbuy("prices", {"skus": ["6607832", "6673112", "6679316"]})
for p in watch["prices"]:
    print(p["sku"], p["price"] if p["found"] else "not found", p["badge"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Best Buy answered.

- **search** - `query`, `page`, `page_size` (18), `total_results`, `total_pages`, `sort`, `category` ({`id`, `name`} or null), `applied_filters[]` {`field`, `values[]`}, `corrected_query`, `redirect_url`, `count`, `sponsored_count`, `products[]` (`position`, `sponsored`, `sku`, `bsin`, `name`, `brand`, `model`, `url`, `image`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`, `condition`, `rating`, `review_count`, `seller_type`, `product_type`, `badges[]`, `release_date`), `facets[]` {`field`, `name`, `value_count`, `values[]` {`value`, `count`, `category_id` on category values}}, `sort_options[]`, `related_searches[]`.
- **category** - the same as search with `category_id` in place of `query`.
- **product** - `sku`, `bsin`, `name`, `brand`, `model`, `upc`, `url`, `status`, `condition`, `product_type`, `category_path[]` {`id`, `name`, `url`}, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`, `financing` ({`months`, `monthly_payment`, `rate`, `plan_type`} or null), `open_box[]` {`condition`, `price`, `savings_vs_new`, `savings_vs_regular`, `savings_percent`, `url`}, `seller_type`, `other_offers[]` {`sku`, `condition`, `seller_type`}, `rating`, `review_count`, `review_summary`, `what_customers_love[]`, `description`, `features[]` {`title`, `description`}, `included_items[]`, `specifications[]` {`group`, `name`, `value`}, `dimensions` {`height`, `width`, `depth`, `weight`}, `images[]`, `manuals[]` {`type`, `url`}, `badges[]`, `release_date`.
- **reviews** - `sku`, `name`, `url`, `page`, `page_size` (20), `sort`, `rating_filter`, `average_rating`, `review_count`, `recommended_percent`, `star_distribution[]` {`stars`, `count`, `percent`}, `pros[]` and `cons[]` {`feature`, `mentions`}, `total_results`, `total_pages`, `has_more`, `count`, `reviews[]` {`id`, `title`, `text`, `rating`, `author`, `submitted_at`, `recommended`, `verified_purchase`, `incentivized`, `days_of_ownership`, `helpful_count`, `not_helpful_count`, `badges[]`, `images[]`, `syndicated_from`, `reviewed_sku`, `brand_response` ({`text`, `responded_at`, `department`} or null)}.
- **availability** - `sku`, `name`, `url`, `zip` (null with `store_ids`), `store_count`, `in_stock_count` (stores with `in_stock` or `limited`), `status_counts` {status: number of stores}, `stores[]` {`store_id`, `name`, `zip`, `distance_miles`, `status`, `quantity`, `pickup_date`, `min_pickup_hours`, `nearby_alternative` ({`store_id`, `name`, `zip`, `distance_miles`, `pickup_date`, `quantity`} or null), `reason`}.
- **stores** - `zip`, `count`, `stores[]` {`store_id`, `name`, `address`, `address2`, `city`, `state`, `zip`, `country`, `phone`, `status`, `store_type`, `distance_miles`, `hours[]` {`date`, `open`, `close`, `closed`}}.
- **deals** - `countdown_ends`, `deal_of_the_day` (one deal or null), `count`, `deals[]` {`sku`, `name`, `url`, `image`, `rating`, `review_count`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`}.
- **prices** - `count` (SKUs found), `requested`, `prices[]` {`sku`, `found`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`}.
- **suggestions** - `query`, `corrected_query`, `count`, `suggestions[]` {`term`, `categories[]` {`id`, `name`}, `skus[]`}.

## Guardrails

- Prices are in US dollars: `189.99` is $189.99. This is bestbuy.com (US) only; Best Buy Canada (bestbuy.ca) is not covered.
- `savings` and `savings_percent` are measured against `regular_price`. On an open-box offer, `savings_vs_new` is against the current new price (the sale price when the item is on sale) and `savings_vs_regular` against the regular price; `savings_percent` on an open-box offer is against the regular price.
- `open_box[]` lists only the conditions Best Buy offers right now, cheapest first, and is empty when there is none. Never quote an open-box price for a condition that is not in the list, and never claim a number of open-box units: the response has none.
- `deal_ends_at` is the deal's end time as Best Buy gives it (`"2026-11-08T23:59:59 CST"`), and is null on many items, including all of the captured `/prices` and `/deals` rows. When it is null, do not state when the price ends. `countdown_ends` on `/deals` carries no time zone.
- Availability is store PICKUP status, not a shelf count. `quantity` is set only on `limited` (Best Buy shows "only N left"); on `in_stock` it is null because Best Buy publishes no unit count for well-stocked items. Never claim a store has a number of units unless `status` is `limited`, and then quote exactly that `quantity`.
- The statuses: `in_stock` (in the store now), `limited` (in the store now, `quantity` units), `ship_to_store` (not on the shelf; Best Buy can ship it to the store for pickup by `pickup_date`), `out_of_stock` (pickup-eligible but none in the store), `not_available_for_pickup` (the item cannot be picked up at this store), and `unknown`. `unknown` is never out of stock: `reason` says why the store's answer was missing (`store_check_failed`, `sku_not_in_store_results`, `store_not_applied`). Say "could not confirm" for `unknown`, or retry.
- `in_stock_count` counts stores with `in_stock` or `limited`. `pickup_date` is null for `out_of_stock` and `not_available_for_pickup`; `min_pickup_hours` is set only for `in_stock` and `limited`.
- With `store_ids` instead of `zip`, `distance_miles` is null (there is no point to measure from) and `zip` at the top level is null.
- `/availability` checks at most 8 stores per call (default 5 nearest the ZIP). For more stores, call again with the next `store_ids` from `/stores`.
- `/stores` takes a US ZIP only: no latitude/longitude, no radius, and no lookup by store id. It returns up to 15 stores, nearest first. The hours are dated for 35 days: read the entry for the day the user asks about rather than assuming a weekly pattern.
- Search and category return 18 organic products per page; `position` counts organic products only. Sponsored tiles are left out unless `include_sponsored: true`, and then carry `sponsored: true` and `position: null`. `sponsored_count` is how many sponsored tiles the page had either way.
- `min_price` and `max_price` go together: one without the other is a 400. `brand` must match the site's Brand filter spelling (a `brand_facet` value); `applied_filters[]` shows what Best Buy actually applied, so check it before claiming a list is filtered.
- `best_match` is a search sort only; on `/category` it is a 400. A category's default sort is the page's own, usually `best_selling`.
- A `pcmcat` category page costs 3 credits (the page is read first for its built-in filters); an `abcat` id costs 2. A page with no product grid is a 404: pick one of its subcategories from `facets[]` (`category_facet`) instead.
- The `url` on `/availability` and `/deals` rows can be a product-family URL without `/sku/` (every captured one is); passing such a URL as `url` is a 400. Use the row's `sku`.
- `brand` can be spelled differently on a listing row and the product answer (`"Insignia"` in search, `"Insignia™"` on `/product`), and `badges[]` can repeat with different capitalization (`"A Best Buy brand"`, `"A Best Buy Brand"`). Match on `sku`, not on brand or name text.
- `dimensions` fields are null when Best Buy does not list them (the captured TV gives only `width`); read `specifications[]` for the full set.
- `/prices` is 2 credits per call for 1 to 15 SKUs; batch SKUs instead of calling `/product` per SKU when only the price is needed. If every SKU is unknown, the call is a 404.
- Reviews are Best Buy's own first-party reviews. `has_more: true` means more pages exist; do not claim to have read every review unless `has_more` is false. `total_results` counts the reviews matching the request (with `rating` set, only that star rating); `review_count` is the product's total.
- `reviewed_sku` is set when a review was written for a sibling SKU of the same product (another color or size); `syndicated_from` names the site a review was first posted on. `brand_response` is the manufacturer's reply when there is one.
- `/suggestions` returns suggested terms with category ids and SKUs only, no prices or search volumes.
- There is no price history, no price-match data and no Q&A endpoint: track prices by calling `/prices` on a schedule and storing the results yourself.
- This API reads public product data for research, price monitoring and stock alerts. It does not add to cart, check out or reserve stock; do not present it as a purchasing bot.
- Never fabricate prices, open-box offers, stock, pickup dates, deal end times or reviews. Only return what the API returned, with the product `url` or `sku`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, a `page` outside 1-100 (reviews 1-500), an unknown `sort` or `best_match` on `/category`, `min_price` without `max_price` or `min_price` not below `max_price`, a `sku` that is not 6-9 digits, a `url` that is not bestbuy.com or names no SKU, a `category_id` that is not `abcat`/`pcmcat`/`cat` plus digits, neither `sku` nor `url`, both or neither of `zip` and `store_ids`, `max_stores` outside 1-8, more than 8 `store_ids`, a ZIP that is not 5 digits, `rating` outside 1-5, or more than 15 `skus`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product (unknown SKU), no such category or a page without a product grid, or a `/prices` call where every SKU is unknown. Not charged. Re-run the search for a fresh `sku`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data).
- `502` or `503` means Best Buy is temporarily unavailable or returned an unusable page (on `/availability`, when no store could be checked at all). Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds. A single store that could not be checked comes back as `status: "unknown"` with `reason: "store_check_failed"` instead of failing the call.

## SDKs

```bash
pip install scavio==0.39.0
npm install scavio@0.40.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.bestBuy.search({ query: "tv", sort: "best_discount", filters: { open_box: true } });
const { data: item } = await scavio.bestBuy.product({ sku: found.products[0].sku });
const { data: pickup } = await scavio.bestBuy.availability({ sku: item.sku, zip: "94103" });
const { data: near } = await scavio.bestBuy.stores({ zip: "94103" });
const { data: prices } = await scavio.bestBuy.prices({ skus: ["6607832", "6673112"] });
const { data: today } = await scavio.bestBuy.deals();
const { data: cat } = await scavio.bestBuy.category({ category_id: "abcat0101001" });
const { data: rev } = await scavio.bestBuy.reviews({ sku: item.sku, rating: 1, sort: "newest" });
const { data: ideas } = await scavio.bestBuy.suggestions({ query: "ps5 con" });
```

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_bestbuy`, `get_bestbuy_product`, `get_bestbuy_reviews`, `get_bestbuy_category`, `get_bestbuy_deals`, `get_bestbuy_stores`, `get_bestbuy_availability`, `get_bestbuy_suggestions` and `get_bestbuy_prices`. Best Buy is opt-in: add `bestbuy` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.37.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bestbuy"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/bestbuy-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [product](https://scavio.dev/docs/bestbuy-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [reviews](https://scavio.dev/docs/bestbuy-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [category](https://scavio.dev/docs/bestbuy-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [deals](https://scavio.dev/docs/bestbuy-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [stores](https://scavio.dev/docs/bestbuy-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [availability](https://scavio.dev/docs/bestbuy-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [suggestions](https://scavio.dev/docs/bestbuy-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [prices](https://scavio.dev/docs/bestbuy-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data). Overview: [Best Buy API](https://scavio.dev/bestbuy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data).
