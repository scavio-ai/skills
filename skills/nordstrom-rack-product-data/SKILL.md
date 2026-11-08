---
name: nordstrom-rack-product-data
description: "Nordstrom Rack product data API: search nordstromrack.com or list any /shop or /clearance category, Clear the Rack, flash events or a brand catalog with price, compare-at price, percent off, the clearance price and any extra-off promotion price on top, rating, badges, every color and filter counts, read one product with every size and color as a SKU with UPC, price type, stock and units available to ship plus the star histogram, size-fit distribution and the reviews on the page, pull Rack's own review history (up to 200 per call) sorted and filtered by stars, verified purchase, photos or text with the rating summary and AI review summary, check per-SKU ship and Rack store-pickup availability with the stores that can do pickup, find Nordstrom Rack stores near a ZIP with hours, and pull search autocomplete. 8 endpoints, 5 credits each, availability and reviews 10."
version: 1.0.0
tags: nordstrom-rack, nordstrom-rack-api, nordstromrack, nordstrom-rack-product-data, nordstrom-rack-scraper, nordstrom-rack-clearance, clear-the-rack, flash-events, off-price, resale-sourcing, fashion, apparel, shoes, designer-brands, clothing-prices, clearance-tracking, price-drop-alerts, percent-off, sku-data, upc, size-fit, product-search, product-data, product-reviews, review-analysis, category-browse, brand-catalog, map-monitoring, store-locator, store-pickup, in-store-availability, autocomplete, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/nordstromrack-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data
---

# Nordstrom Rack Product Data API - Clearance, Flash Events, Store Pickup, Reviews

Search Nordstrom Rack (nordstromrack.com, US) by keyword, or list any category page under `/shop` or `/clearance` (departments such as `/shop/women`, deals such as `/shop/deals/black-friday`, new arrivals, Clear the Rack at `/clearance`, and flash events at `/shop/flash/event-N`) or a brand's catalog, 24 products per page, sorted by relevance, rating, price, newest or percent off: current price and price range, the compare-at price range Rack strikes through, percent off and on-sale flag, the clearance price range, any promotion price on top of it (Clear the Rack's extra percent off clearance) with its percent off, rating, review count, badges such as `new_markdown` or `final_sale`, a low-inventory flag, the marketplace seller when Nordstrom Rack is not the seller, and every color with its color family and image. Category and brand pages add the page's breadcrumbs, subcategories and the filter sidebar with product counts per option. Read one product by URL or style id with its description, feature bullets, fit notes, final-sale flag, the same price, clearance and promotion fields, the star histogram, the size-fit distribution, breadcrumbs and images, every color and size as a SKU with SKU id, UPC, price, compare-at price, percent off, price type, in-stock flag and the quantity available to ship, and the reviews the product page shows. Pull a product's Rack reviews (Rack has its own review pool, separate from nordstrom.com's), up to 200 per call, sorted and filtered by stars, verified purchase, photos or a text search, with the rating summary, size and width fit and the AI review summary. Check every SKU's ship and Rack store-pickup availability with the stores that can do in-store pickup, find Nordstrom Rack stores near a ZIP code or point with hours and services, and pull the search box's autocomplete suggestions. All endpoints return structured JSON.

See also: for nordstrom.com (the full-line Nordstrom store, its prices, stores and its own review pool) use the `nordstrom-product-data` skill. The two are separate sites with separate prices, stock and stores.

## When to trigger

Use this skill when the user asks to:
- Find clothing, shoes, bags or beauty at Nordstrom Rack by keyword, and compare prices, discounts and brands
- Track Nordstrom Rack clearance: list `/clearance` (or `/clearance/women/clothing`...) sorted by `percent_off`, and read the clearance price and any Clear the Rack extra-off price per item
- Watch a Clear the Rack event: which items carry the extra percent off clearance, and what they cost with it
- List a Nordstrom Rack flash event's products, or the flash events that are live now
- Pull a brand's full Nordstrom Rack catalog for off-price sourcing, resale research or MAP monitoring of the off-price channel
- Track Nordstrom Rack prices or price drops on a product, or compare a Rack price with the nordstrom.com price of the same style
- Check which sizes and colors of a Rack product are in stock, how many units ship online, and which Nordstrom Rack stores can do in-store pickup
- Find Nordstrom Rack stores near a ZIP code or location, with hours, holiday hours and pickup
- Get the UPC, SKU id and price of every size and color of a Rack style
- Read what Nordstrom Rack reviewers say about fit and quality, pull only the 1- and 2-star complaints, verified purchases, reviews with photos or reviews mentioning a word
- Get Nordstrom Rack search autocomplete suggestions for keyword research

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 5 credits except availability and reviews (10 each), so the free credits cover 10 calls (or 5 availability or review calls).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Nordstrom Rack endpoint costs **5 credits** except `/availability`, which costs **10** (it reads the product page and then looks up the pickup stores), and `/reviews`, which costs **10**. Most calls take 1-5 seconds; availability and large brand or category pages can take 10-30 seconds, and `/reviews` takes 15-60 seconds (up to about 100 seconds at `max_reviews: 200`), so allow a client timeout of at least 120 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/nordstromrack/search` | 5 | 24 products per page: position, style id, URL, name, brand, image, current price and price range, compare-at price range, percent off, on-sale flag, clearance price range, promotion price range and promotion percent off, rating, review count, badges, low-inventory flag, marketplace flag and seller, and every color with its color family and image. Plus the total result count, page count and the sorts the site offers |
| `POST /api/v1/nordstromrack/category` | 5 | One category page (any `/shop` or `/clearance` path: departments, deals, new arrivals, Clear the Rack, flash events), 24 products per page in the same shape as search, plus the category's name, title, path, URL, breadcrumbs and subcategories (for drilling down), and the filter sidebar: each filter group with its options and product counts |
| `POST /api/v1/nordstromrack/brand` | 5 | One brand's catalog from its brand page (`/brands/adidas`), 24 products per page in the same shape as search, plus the brand's name, path, URL, breadcrumbs, sub-pages and the filter sidebar with counts |
| `POST /api/v1/nordstromrack/product` | 5 | One product by URL or style id: name, brand, brand URL, description, feature bullets, fit notes, final-sale and in-stock flags, current, compare-at and clearance price ranges, percent off, promotion price range and promotion percent off, marketplace seller, rating, review count, star histogram, size-fit distribution, AI review summary and the most praised and criticized features when the site shows them, breadcrumbs, images, and every color with its images and every size as a SKU (SKU id, size, size type, UPC, price, compare-at price, percent off, price type, in stock, quantity to ship, final sale). Also the reviews shown on the product page (up to about 13), each with title, text, rating, size rating, author, date, helpful votes, verified-purchase flag, size and color purchased, and photos |
| `POST /api/v1/nordstromrack/reviews` | 10 | One product's Rack reviews by URL or style id, up to 200 per call (default 60), sorted most helpful, most recent, highest or lowest rated, optionally filtered to star ratings, verified purchases, reviews with photos or a text search. The review summary (average rating, total reviews, star histogram, size rating, width rating where the site has one, the most praised and criticized features with a quote each, count of rating-only reviews), the AI review summary, the number of reviews matching the filters and whether more exist. Each review: id, title, text, rating, size rating, author, date, helpful votes, verified-purchase flag, reviewer badges, size and color purchased, the reviewer's height, weight, body type and usual sizes when given, secondary ratings, the site it was first posted on when syndicated, and photos with thumbnails |
| `POST /api/v1/nordstromrack/availability` | 10 | Every SKU of one product (or one SKU): SKU id, size, color, UPC, in stock, ship available and quantity to ship, pickup available and quantity for pickup (both chain-wide), and the Nordstrom Rack stores that can do in-store pickup (store number, name, address, city, state, ZIP, phone). Plus SKU, in-stock and pickup-store counts |
| `POST /api/v1/nordstromrack/stores` | 5 | Nordstrom Rack stores near a US ZIP or latitude/longitude within up to 100 miles, nearest first, or by store number: store number, name, type (`rack`), address, phone, weekly hours, holiday hours when posted, open and close times for the next 8 days, time zone, distance, coordinates, pickup and curbside-pickup flags, amenities (the departments and services the store lists) and store page URL |
| `POST /api/v1/nordstromrack/suggestions` | 5 | The search box's autocomplete for a partial term: up to 20 suggested queries, most likely first |

## Workflow

1. **Find products:** call `/nordstromrack/search` with `query`, `/nordstromrack/category` with a path such as `/shop/women/clothing/dresses` or `/clearance/women`, or `/nordstromrack/brand` with a brand path such as `/brands/adidas`. Each row has a `url` and a `style_id`. Drill into a category with the `path` of any `category.subcategories[]` entry.
2. **Clearance and Clear the Rack:** list `/clearance` or a clearance department (`/clearance/women/clothing`) with `sort: "percent_off"`. Each row's `clearance_price_range` is the clearance price; while an extra-off event such as Clear the Rack runs, `promotion_price_range` is the price with the extra discount and `promotion_percent_off` the extra percent off the clearance price. `percent_off` is the total discount against the compare-at price.
3. **Flash events:** call `/nordstromrack/category` with `/shop/flash`; it has no products of its own, and its `subcategories[]` are the live events. Call `/nordstromrack/category` again with an event's `path` (`/shop/flash/event-N`): page 1 lists the event's featured products first, then the rest, with positions running on.
4. **A brand's catalog:** take `brand_url` from a product answer (or the `brand.path` a brand call returns) and pass it as `brand` to `/nordstromrack/brand`; page through with `page` until `page_count`.
5. **One product in full:** call `/nordstromrack/product` with the row's `url` or `style_id`. Read `colors[].skus[]`: each size of each color has its own `price`, `original_price`, `price_type`, `in_stock` and `quantity`.
6. **Store pickup:** call `/nordstromrack/availability` with the same `url` or `style_id` (and `sku_id` for one size). Each SKU lists `pickup_stores[]`; pass their `store_number`s to `/nordstromrack/stores` as `store_numbers` for hours and distance, or call `/nordstromrack/stores` with the user's `zip` and match store numbers.
7. **Fit and reviews:** `size_fit`, `rating_histogram` and the reviews shown on the page (`reviews[]`, up to about 13) come with the product answer. For more, call `/nordstromrack/reviews` with the same `url` or `style_id`: up to 200 reviews per call, sorted (`most_recent`, `lowest_rated`...) or filtered (`stars: [1, 2]`, `verified_only`, `with_photos`, or `search` for a word). Check `has_more` and `total_results`.
8. **Keyword research:** `/nordstromrack/suggestions` with a partial term returns what shoppers are offered as they type; feed a suggestion back into `/nordstromrack/search`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-100). 24 products per page |
| `sort` | string | `relevance` | `relevance`, `rating`, `price_high`, `price_low`, `newest` or `percent_off` |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | required | A nordstromrack.com category: the `/shop` or `/clearance` path or full URL of a category page, e.g. `/shop/women/clothing/dresses`, `/shop/deals/black-friday`, `/shop/new-arrivals`, `/clearance`, `/clearance/women/clothing`, `/shop/flash` or a flash event such as `/shop/flash/event-7`. A path without a prefix (`women/clothing/dresses`) is read as `/shop/...`. nordstrom.com `/browse` paths and nordstrom.com URLs are a 400 here. Query parameters in a URL (filters) are ignored |
| `page` | integer | 1 | Results page, 1-based (1-100). 24 products per page |
| `sort` | string | `relevance` | `relevance`, `rating`, `price_high`, `price_low`, `newest` or `percent_off` |

### Brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | required | A nordstromrack.com brand: the `/brands` path or full URL of a brand page, e.g. `/brands/adidas`, `/brands/sam-edelman` or `https://www.nordstromrack.com/brands/ugg` (a product's `brand_url` works). The `/brands` prefix is optional. Rack brand pages carry no brand id: the nordstrom.com form `/brands/<name>--<id>` is a 404 here |
| `page` | integer | 1 | Results page, 1-based (1-100). 24 products per page |
| `sort` | string | `relevance` | `relevance`, `rating`, `price_high`, `price_low`, `newest` or `percent_off` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | nordstromrack.com product URL, the `url` of a search, category or brand result: `https://www.nordstromrack.com/s/<slug>/<style id>`. A nordstrom.com URL is a 400; pass its style id instead |
| `style_id` | string | one of | Nordstrom Rack style id, the number at the end of a product URL (the `style_id` of a result). Used when `url` is not given |

### Availability (`/availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | nordstromrack.com product URL (the `url` of a search, category or brand result) |
| `style_id` | string | one of | Nordstrom Rack style id, used when `url` is not given |
| `sku_id` | string | all SKUs | Only this SKU (a product's `colors[].skus[].sku_id`, e.g. `A5819201`). An id that is not a SKU of the product is a 404 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | nordstromrack.com product URL (the `url` of a search, category or brand result) |
| `style_id` | string | one of | Nordstrom Rack style id, used when `url` is not given |
| `sort` | string | `most_helpful` | `most_helpful`, `most_recent`, `highest_rated` or `lowest_rated`. Cannot be combined with `search` (a 400): the site returns review search results in its own order |
| `stars` | array of integers | all | Only reviews with these star ratings, 1-5, e.g. `[1, 2]` for the critical ones |
| `verified_only` | boolean | `false` | Only reviews from verified purchasers |
| `with_photos` | boolean | `false` | Only reviews that include customer photos |
| `search` | string | none | Only reviews mentioning this text (the review search box), 1-100 characters |
| `max_reviews` | integer | 60 | Reviews to return, 1-200. Larger values take longer (about 50-100 seconds for 200) |

### Stores (`/stores`)

Pass exactly one of `zip`, `latitude` + `longitude`, or `store_numbers`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code to search around (`10001` or `10001-1234`) |
| `latitude` | number | one of | Latitude to search around, with `longitude` |
| `longitude` | number | one of | Longitude to search around, with `latitude` |
| `store_numbers` | array or string | one of | Look Rack stores up by number instead of location: an array or a comma-separated string, up to 100 (an availability result's `pickup_stores[].store_number`). Numbers of Nordstrom full-line stores are left out of the answer |
| `distance_miles` | integer | 100 | Search radius in miles around `zip` or `latitude`/`longitude`, 1-100 (the site's maximum) |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |
| `limit` | integer | 8 | Suggestions to return, 1-20. The site may return fewer |

## Examples

### Clearance and Clear the Rack

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "/clearance/women", "sort": "percent_off"}'
```

Captured response during Clear the Rack (6 of 8 subcategories, 21 of 24 filter groups, most options, 23 of 24 products and 2 of the first row's 4 colors trimmed):

```json
{
  "data": {
    "category": {
      "name": "Women",
      "title": "Women's Clearance",
      "path": "/clearance/women",
      "url": "https://www.nordstromrack.com/clearance/women",
      "breadcrumbs": [
        { "name": "Clearance", "url": "https://www.nordstromrack.com/clearance" },
        { "name": "Women", "url": "https://www.nordstromrack.com/clearance/women" }
      ],
      "subcategories": [
        { "name": "Clothing", "path": "/clearance/women/clothing", "url": "https://www.nordstromrack.com/clearance/women/clothing" },
        { "name": "Shoes", "path": "/clearance/women/shoes", "url": "https://www.nordstromrack.com/clearance/women/shoes" }
      ]
    },
    "page": 1,
    "sort": "percent_off",
    "total_results": 4256,
    "page_count": 178,
    "count": 24,
    "available_sorts": ["rating", "price_high", "price_low", "newest", "percent_off", "relevance"],
    "filters": [
      {
        "name": "Price",
        "option_count": 5,
        "options": [
          { "label": "$0 - $25", "count": null },
          { "label": "$25 - $50", "count": null }
        ]
      },
      {
        "name": "Brand",
        "option_count": 466,
        "options": [
          { "label": "Adornia", "count": 328 },
          { "label": "EFFY", "count": 170 }
        ]
      },
      {
        "name": "Discount",
        "option_count": 6,
        "options": [
          { "label": "60% off or more", "count": 3979 },
          { "label": "70% off or more", "count": 3340 }
        ]
      }
    ],
    "products": [
      {
        "position": 1,
        "style_id": "8903117",
        "url": "https://www.nordstromrack.com/s/max-studio-sleeveless-tiered-dress-plus/8903117",
        "name": "Sleeveless Tiered Dress",
        "brand": "MAX STUDIO",
        "image": "https://n.nordstrommedia.com/it/b41bd0a3-6530-4209-9b19-780b567cb40e.jpeg",
        "price": 7.86,
        "price_range": { "min": 7.86, "max": 17.04 },
        "original_price_range": { "min": 168, "max": 168 },
        "percent_off": 95,
        "on_sale": true,
        "clearance_price_range": { "min": 10.49, "max": 22.73 },
        "promotion_price_range": { "min": 7.86, "max": 17.04 },
        "promotion_percent_off": 25,
        "rating": 5,
        "review_count": 1,
        "badges": ["new_markdown", "enable_early_access", "final_sale"],
        "low_inventory": false,
        "is_marketplace": false,
        "seller": null,
        "colors": [
          { "name": "DENIM-DENIM", "color_family": "Blue", "image": "https://n.nordstrommedia.com/it/a26af44d-309f-4774-a843-07fa1500e3da.jpeg" },
          { "name": "BLACK", "color_family": "Black", "image": "https://n.nordstrommedia.com/it/b41bd0a3-6530-4209-9b19-780b567cb40e.jpeg" }
        ]
      }
    ]
  },
  "response_time": 2319,
  "credits_used": 5
}
```

Read the row as: compare-at $168, clearance $10.49-$22.73, and with Clear the Rack's extra 25% off clearance $7.86-$17.04, which is 95% off the compare-at price. The same listing also has clearance rows with no promotion (`"clearance_price_range": { "min": 19.98, "max": 19.98 }`, `"promotion_price_range": null`), so never assume every clearance item carries the extra discount.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "dress"}'
```

A captured row for `{"query": "dress"}` (21,249 results, 886 pages): a style whose colors sit at three price points, Rack's own price, clearance and the Clear the Rack price (2 of 8 colors kept):

```json
{
  "position": 4,
  "style_id": "7737947",
  "url": "https://www.nordstromrack.com/s/maeve-midi-dress/7737947",
  "name": "Maeve Midi Dress",
  "brand": "ASTR the Label",
  "image": "https://n.nordstrommedia.com/it/557c866b-2303-41fb-88bc-d377dd398e1d.jpeg",
  "price": 24,
  "price_range": { "min": 24, "max": 69.97 },
  "original_price_range": { "min": 128, "max": 128 },
  "percent_off": 81,
  "on_sale": true,
  "clearance_price_range": { "min": 32, "max": 32 },
  "promotion_price_range": { "min": 24, "max": 24 },
  "promotion_percent_off": 25,
  "rating": 4.1,
  "review_count": 129,
  "badges": ["new", "enable_early_access", "final_sale"],
  "low_inventory": false,
  "is_marketplace": false,
  "seller": null,
  "colors": [
    { "name": "LIGHT GREE", "color_family": "Green", "image": "https://n.nordstrommedia.com/it/5abe87fe-d3dc-4489-87ba-2766321a4057.jpeg" },
    { "name": "PINK", "color_family": "Pink", "image": "https://n.nordstrommedia.com/it/ab25b49e-824b-453b-a99a-f877e68da7c2.jpeg" }
  ]
}
```

A row with no clearance carries `"clearance_price_range": null`, `"promotion_price_range": null` and `"promotion_percent_off": null` (the first row of the same search: `"price": 54.97`, `"original_price_range": { "min": 138, "max": 138 }`, `"percent_off": 60`).

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"style_id": "8816500"}'
```

Captured response (description, features, fit notes, breadcrumbs, images, the CHESTNUT color, 3 of 5 IVORY PRINT SKUs and 5 of 6 reviews trimmed):

```json
{
  "data": {
    "style_id": "8816500",
    "url": "https://www.nordstromrack.com/s/love-by-design-devin-long-sleeve-maxi-dress/8816500",
    "name": "Devin Long Sleeve Maxi Dress",
    "brand": "Love By Design",
    "brand_url": "https://www.nordstromrack.com/brands/love-by-design",
    "is_final_sale": false,
    "in_stock": true,
    "price": 54.97,
    "price_range": { "min": 54.97, "max": 54.97 },
    "original_price_range": { "min": 138, "max": 138 },
    "percent_off": 60,
    "on_sale": true,
    "clearance_price_range": null,
    "promotion_price_range": null,
    "promotion_percent_off": null,
    "is_marketplace": false,
    "seller": null,
    "rating": 4.3,
    "review_count": 7,
    "rating_histogram": [
      { "rating": 5, "count": 5 },
      { "rating": 4, "count": 1 },
      { "rating": 1, "count": 1 }
    ],
    "size_fit": {
      "average": 3.4,
      "distribution": [
        { "value": 2, "label": "a little small", "count": 1 },
        { "value": 3, "label": "true to size", "count": 2 },
        { "value": 4, "label": "a little big", "count": 1 },
        { "value": 5, "label": "too big", "count": 1 }
      ]
    },
    "review_summary": null,
    "best_features": [],
    "worst_features": [],
    "color_count": 2,
    "sku_count": 10,
    "colors": [
      {
        "name": "IVORY PRINT",
        "color_family": "White",
        "in_stock": true,
        "skus": [
          {
            "sku_id": "AA341416",
            "size": "X-Large",
            "size_type": "Regular",
            "color": "IVORY PRINT",
            "upc": "871111082106",
            "price": 54.97,
            "original_price": 138,
            "percent_off": 60,
            "price_type": "regular",
            "in_stock": true,
            "quantity": 1,
            "is_final_sale": false
          },
          {
            "sku_id": "AA341415",
            "size": "X-Small",
            "size_type": "Regular",
            "color": "IVORY PRINT",
            "upc": "871111082069",
            "price": 54.97,
            "original_price": 138,
            "percent_off": 60,
            "price_type": "regular",
            "in_stock": true,
            "quantity": 0,
            "is_final_sale": false
          }
        ]
      }
    ],
    "reviews": [
      {
        "review_id": "248453676",
        "title": "Beautiful dress but so big!!",
        "text": "I'm a size L-XL, 10-12 in dresses. I ordered XL in this and it was SO big! An extra 3-4 inches at the waist. I definitely could have worn an L, maybe even M. I'm petite, about 5'3\" and this dress was definitely maxi-length on me but not so long that I would've needed to have it hemmed.\n\nThe dress itself is really pretty. A flowy burnout fabric with lovely details.",
        "rating": 4,
        "recommended": null,
        "size_rating": 5,
        "author": "CdlG",
        "date": "2026-02-27T19:05:26.000+00:00",
        "helpful_votes": 16,
        "verified_purchase": true,
        "size_purchased": "X-Large",
        "color_purchased": "IVORY PRINT",
        "photos": []
      }
    ]
  },
  "response_time": 1961,
  "credits_used": 5
}
```

`price_type: "regular"` with `percent_off: 60` is normal on Rack: the regular Rack price ($54.97) is already below the compare-at price ($138). The X-Small SKU reads `in_stock: true` with `quantity: 0`: it is held only in stores, so call `/availability` to see which Rack stores can do pickup.

### Brand

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/brand \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "/brands/adidas"}'
```

Captured `data.brand` (1,319 products over 55 pages; `filters` and `products` have the same shape as category):

```json
{
  "name": "adidas",
  "title": "adidas",
  "path": "/brands/adidas",
  "url": "https://www.nordstromrack.com/brands/adidas",
  "breadcrumbs": [
    { "name": "Brands", "url": "https://www.nordstromrack.com/brands" },
    { "name": "adidas", "url": "https://www.nordstromrack.com/brands/adidas" }
  ],
  "subcategories": []
}
```

### Availability

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"style_id": "7737947"}'
```

Captured response (38 of 40 SKUs and 3 of the second SKU's 5 pickup stores trimmed):

```json
{
  "data": {
    "style_id": "7737947",
    "url": "https://www.nordstromrack.com/s/maeve-midi-dress/7737947",
    "name": "Maeve Midi Dress",
    "brand": "ASTR the Label",
    "sku_id": null,
    "sku_count": 40,
    "in_stock_count": 29,
    "pickup_store_count": 71,
    "skus": [
      {
        "sku_id": "AAAA3714",
        "size": "Small",
        "color": "PINK",
        "upc": "191293766916",
        "in_stock": true,
        "ship_available": false,
        "ship_quantity": 0,
        "pickup_available": true,
        "pick_quantity": 2,
        "pickup_store_count": 2,
        "pickup_stores": [
          { "store_number": "150", "name": "Nordstrom Rack Tempe Marketplace", "address": "1900 East Rio Salado Parkway", "city": "Tempe", "state": "AZ", "zip": "85281", "phone": "480.603.4600" },
          { "store_number": "369", "name": "Nordstrom Rack Carmel Mountain Plaza", "address": "11940 Carmel Mountain Road", "city": "San Diego", "state": "CA", "zip": "92128", "phone": "858.312.7766" }
        ]
      },
      {
        "sku_id": "AAAA3713",
        "size": "X-Small",
        "color": "PINK",
        "upc": "191293766909",
        "in_stock": true,
        "ship_available": true,
        "ship_quantity": 1,
        "pickup_available": true,
        "pick_quantity": 6,
        "pickup_store_count": 5,
        "pickup_stores": [
          { "store_number": "166", "name": "Nordstrom Rack The Shops at La Jolla Village", "address": "8875 Villa La Jolla Drive", "city": "La Jolla", "state": "CA", "zip": "92037", "phone": "858.373.4600" },
          { "store_number": "476", "name": "Nordstrom Rack Persimmon Place", "address": "5300 Dublin Boulevard", "city": "Dublin", "state": "CA", "zip": "94568", "phone": "925.558.2900" }
        ]
      }
    ]
  },
  "response_time": 12781,
  "credits_used": 10
}
```

The Small SKU is pickup-only (`ship_available: false`, `ship_quantity: 0`, `in_stock: true`). `pick_quantity: 6` on the X-Small is the chain-wide pickup total across its 5 stores, not 6 units in each, and not a per-store count. The pickup stores span the whole US, not the area near the user.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10001", "distance_miles": 25}'
```

Captured response (8 of 9 stores, 10 of 12 holiday-hours lines and 6 of 8 days of `daily_hours` trimmed):

```json
{
  "data": {
    "zip": "10001",
    "latitude": null,
    "longitude": null,
    "store_numbers": null,
    "distance_miles": 25,
    "count": 9,
    "stores": [
      {
        "store_number": "509",
        "name": "Nordstrom Rack 31st & 6th",
        "type": "rack",
        "address": "865 Avenue of the Americas",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "US",
        "phone": "646.861.5440",
        "hours": ["Mon-Sat 10am-9pm", "Sun 11am-7pm"],
        "special_hours": { "label": "Holiday Store Hours", "hours": ["Nov 26: Closed", "Nov 27-28: 9am-10pm"] },
        "daily_hours": [
          { "opens": "2026-11-07T10:00:00-05:00", "closes": "2026-11-07T21:00:00-05:00" },
          { "opens": "2026-11-08T11:00:00-05:00", "closes": "2026-11-08T19:00:00-05:00" }
        ],
        "time_zone": "America/New_York",
        "distance_miles": 0.41,
        "latitude": 40.747839,
        "longitude": -73.989518,
        "pickup": true,
        "curbside_pickup": false,
        "amenities": [
          { "name": "Buy Online & Pick Up In Store", "type": "service", "phone": null, "hours": [] }
        ],
        "url": "https://www.nordstromrack.com/store-details/nordstrom-rack-31st-6th"
      }
    ]
  },
  "response_time": 1748,
  "credits_used": 5
}
```

Other stores in the same answer list the departments they carry as amenities (`"Designer Shoes"`, `"Plus Sizes"`, `"Petite Sizes"`, `"Kids"`...), next to `"Buy Online & Pick Up In Store"`.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "dre"}'
```

Captured response:

```json
{
  "data": {
    "query": "dre",
    "count": 8,
    "suggestions": ["dresses for women", "dress", "barefoot dreams", "sweater dress", "cocktail dress for women", "black dress", "wedding guest dress for women", "long sleeve dress"]
  },
  "response_time": 910,
  "credits_used": 5
}
```

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstromrack/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"style_id": "7737947", "max_reviews": 18}'
```

Captured response (17 of 18 reviews trimmed):

```json
{
  "data": {
    "style_id": "7737947",
    "url": "https://www.nordstromrack.com/s/maeve-midi-dress/7737947",
    "name": "Maeve Midi Dress",
    "brand": "ASTR the Label",
    "sort": "most_helpful",
    "filters": {
      "stars": [],
      "verified_only": false,
      "with_photos": false,
      "search": null
    },
    "max_reviews": 18,
    "total_results": 129,
    "returned": 18,
    "has_more": true,
    "summary": {
      "average_rating": 4.07,
      "total_reviews": 129,
      "ratings_histogram": [
        { "rating": 5, "count": 77 },
        { "rating": 4, "count": 14 },
        { "rating": 3, "count": 19 },
        { "rating": 2, "count": 8 },
        { "rating": 1, "count": 11 }
      ],
      "size_rating": 3,
      "width_rating": 3,
      "best_features": [],
      "worst_features": [],
      "ratings_only_count": 2
    },
    "ai_summary": "* Customers consistently praise the gorgeous appearance, silky fabric, and vibrant prints that look even better in person\n* Many appreciate the flattering smocked back, stretchy ruching, and supportive structure accommodating various body types\n* Several report fit inconsistencies, particularly a wide bodice, with recommendations to size up for fuller busts\n* A few mention construction defects including broken zippers, loose threads, and misaligned seams\n* Most reviewers consider the dress beautiful and comfortable despite some sizing and quality concerns",
    "reviews": [
      {
        "review_id": "249337691",
        "title": "LIVID!!! 100 polyester really?",
        "text": "So angry I just bought this. I forgot to look at the material section as I usually do for some reason it slipped my mind because I have been watching this dress and usually this company has very good fabric content but for the price I just paid for this dress I’m an absolute shock. It’s 100% polyester this dress is worth literally $15. What are you doing? Nordstrom Rack? This is scamming horrible. I can’t believe a company would do this. I’m sick of it. I’m sick of seeing it. It’s disgusting and you guys know it. What a waste of such an amazing design. Fit is great, but quality does not equate to the price so I will be returning.",
        "rating": 1,
        "size_rating": 4,
        "author": "Dahlia",
        "date": "2026-04-08T00:18:26.000+00:00",
        "helpful_votes": 3,
        "verified_purchase": true,
        "size_purchased": "Medium",
        "color_purchased": null,
        "badges": ["verified_purchaser"],
        "height": "5’4”",
        "weight": "119 lb.",
        "body_type": [],
        "usual_sizes": [],
        "secondary_ratings": [
          { "name": "Size", "rating": 4, "max": 5 }
        ],
        "syndicated_from": null,
        "photos": []
      }
    ]
  },
  "response_time": 13480,
  "credits_used": 10
}
```

The same style on nordstrom.com has 216 reviews; on Rack it has 129. 15 of the other 17 reviews in this answer carry `"syndicated_from": "nordstrom.com"` (first posted on nordstrom.com and shown on Rack), so the two pools overlap: never add the Rack and nordstrom.com totals together.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def rack(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/nordstromrack/{endpoint}", headers=HEADERS, json=body, timeout=150)
    r.raise_for_status()
    return r.json()["data"]

# 1. Deepest clearance first, with the Clear the Rack extra-off price when one runs (5 credits)
found = rack("category", {"category": "/clearance/women", "sort": "percent_off"})
for p in found["products"][:5]:
    promo = p["promotion_price_range"]
    print(p["brand"], p["name"], "clearance", p["clearance_price_range"],
          f'extra {p["promotion_percent_off"]}% off ->' if promo else "no extra off", promo,
          "compare-at", p["original_price_range"])

# 2. One product: every size and color with its price type and units to ship (5 credits)
item = rack("product", {"url": found["products"][0]["url"]})
for color in item["colors"]:
    for s in color["skus"]:
        print(color["name"], s["size"], s["upc"], s["price"], s["price_type"], "in stock" if s["in_stock"] else "out", s["quantity"])

# 3. Rack store pickup per SKU, then the user's nearby Rack stores (10 + 5 credits)
avail = rack("availability", {"url": item["url"]})
near = rack("stores", {"zip": "10001", "distance_miles": 25})
near_numbers = {st["store_number"]: st for st in near["stores"]}
for s in avail["skus"]:
    nearby = [p["name"] for p in s["pickup_stores"] if p["store_number"] in near_numbers]
    print(s["size"], s["color"], "ships", s["ship_quantity"], "pickup near you:", nearby or "none")

# 4. The newest 1- and 2-star Rack reviews (10 credits, 15-60 s)
rev = rack("reviews", {"url": item["url"], "stars": [1, 2], "sort": "most_recent", "max_reviews": 40})
print(rev["total_results"], "critical reviews of", (rev["summary"] or {}).get("total_reviews"))
for r in rev["reviews"]:
    print(r["rating"], (r["date"] or "")[:10], r["syndicated_from"], r["title"], (r["text"] or "")[:120])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Nordstrom Rack answered.

- **search** - `query`, `page`, `sort`, `total_results`, `page_count`, `count`, `available_sorts[]`, `products[]` (`position`, `style_id`, `url`, `name`, `brand`, `image`, `price`, `price_range` {`min`, `max`}, `original_price_range` {`min`, `max`}, `percent_off`, `on_sale`, `clearance_price_range` ({`min`, `max`} or null), `promotion_price_range` ({`min`, `max`} or null), `promotion_percent_off`, `rating`, `review_count`, `badges[]`, `low_inventory`, `is_marketplace`, `seller`, `colors[]` {`name`, `color_family`, `image`}).
- **category** - `category` {`name`, `title`, `path`, `url`, `breadcrumbs[]` {`name`, `url`}, `subcategories[]` {`name`, `path`, `url`}}, `page`, `sort`, `total_results`, `page_count`, `count`, `available_sorts[]`, `filters[]` {`name`, `option_count`, `options[]` {`label`, `count`}}, `products[]` (same fields as search).
- **brand** - `brand` {`name`, `title`, `path`, `url`, `breadcrumbs[]`, `subcategories[]`}, then the same fields as category.
- **product** - `style_id`, `url`, `name`, `brand`, `brand_url`, `description`, `features[]`, `fit_info[]`, `is_final_sale`, `in_stock`, `price`, `price_range`, `original_price_range`, `percent_off`, `on_sale`, `clearance_price_range`, `promotion_price_range`, `promotion_percent_off`, `is_marketplace`, `seller`, `rating`, `review_count`, `rating_histogram[]` {`rating`, `count`}, `size_fit` {`average`, `distribution[]` {`value`, `label`, `count`}} or null, `review_summary`, `best_features[]` and `worst_features[]` {`name`, `mentions`, `quote`}, `breadcrumbs[]` {`name`, `url`}, `images[]`, `color_count`, `sku_count`, `colors[]` (`name`, `color_family`, `in_stock`, `images[]`, `skus[]` {`sku_id`, `size`, `size_type`, `color`, `upc`, `price`, `original_price`, `percent_off`, `price_type`, `in_stock`, `quantity`, `is_final_sale`}), `reviews[]` (`review_id`, `title`, `text`, `rating`, `recommended`, `size_rating`, `author`, `date`, `helpful_votes`, `verified_purchase`, `size_purchased`, `color_purchased`, `photos[]`).
- **reviews** - `style_id`, `url`, `name`, `brand`, `sort` (null when `search` is set), `filters` {`stars[]`, `verified_only`, `with_photos`, `search`} and `max_reviews` (the request echoed), `total_results` (reviews matching the filters), `returned`, `has_more`, `summary` ({`average_rating`, `total_reviews`, `ratings_histogram[]` {`rating`, `count`}, `size_rating`, `width_rating`, `best_features[]` and `worst_features[]` {`name`, `mentions`, `quote`}, `ratings_only_count`} or null), `ai_summary`, `reviews[]` {`review_id`, `title`, `text`, `rating`, `size_rating`, `author`, `date`, `helpful_votes`, `verified_purchase`, `size_purchased`, `color_purchased`, `badges[]`, `height`, `weight`, `body_type[]`, `usual_sizes[]`, `secondary_ratings[]` {`name`, `rating`, `max`}, `syndicated_from`, `photos[]` {`url`, `thumbnail_url`}}.
- **availability** - `style_id`, `url`, `name`, `brand`, `sku_id` (the requested SKU or null), `sku_count`, `in_stock_count`, `pickup_store_count`, `skus[]` {`sku_id`, `size`, `color`, `upc`, `in_stock`, `ship_available`, `ship_quantity`, `pickup_available`, `pick_quantity`, `pickup_store_count`, `pickup_stores[]` {`store_number`, `name`, `address`, `city`, `state`, `zip`, `phone`}}.
- **stores** - `zip`, `latitude`, `longitude`, `store_numbers`, `distance_miles` (the request echoed), `count`, `stores[]` {`store_number`, `name`, `type` (`rack`), `address`, `city`, `state`, `zip`, `country`, `phone`, `hours[]`, `special_hours` ({`label`, `hours[]`} or null), `daily_hours[]` {`opens`, `closes`}, `time_zone`, `distance_miles`, `latitude`, `longitude`, `pickup`, `curbside_pickup`, `amenities[]` {`name`, `type`, `phone`, `hours[]`}, `url`}.
- **suggestions** - `query`, `count`, `suggestions[]` (strings).

## Guardrails

- Prices are in US dollars: `54.97` is $54.97. This is nordstromrack.com (US) only. nordstrom.com is a different site with different prices, stock, stores and reviews: use the `nordstrom-product-data` skill for it.
- `original_price_range` and a SKU's `original_price` are the compare-at price Rack strikes through, not a price Rack ever charged. `percent_off` is measured against it, so a Rack item at its everyday Rack price still shows a large `percent_off` with `price_type: "regular"`.
- `price` on a style is the low end of `price_range`, the lowest current price across its sizes and colors, including any promotion price. `percent_off` on a style is the largest discount across them. When the range spans more than one price (the Maeve dress above runs $24 to $69.97), quote the range or read the exact SKU's price from `/product`; never present the low end as the price of every size or color.
- `clearance_price_range` is set only when some SKUs are on clearance. `promotion_price_range` is the price with an extra discount on top, set only while one applies (Clear the Rack's extra percent off clearance, for example), and `promotion_percent_off` is that extra percent: off the clearance price on a clearance item, otherwise off Rack's regular price. Both are null on most items outside an event. No response carries an event's start or end date; never state when a sale starts or ends.
- A clearance item does not always carry the promotion: check `promotion_price_range` per item instead of applying an event's percent to every clearance price.
- `/shop/flash` has no products: its `subcategories[]` are the live flash events. On an event page (`/shop/flash/event-N`), page 1 shows the event's featured products first; positions keep counting across them.
- `final_sale` in `badges[]` (and `is_final_sale`) means the item cannot be returned; say so when quoting a clearance or Clear the Rack price.
- `in_stock` on a product SKU means the SKU can be shipped OR picked up in a Rack store. `quantity` is the units available to ship online only, so a SKU can be `in_stock: true` with `quantity: 0` when it is held only in stores. Call `/availability` to see whether it ships or is pickup-only and where.
- `pick_quantity` on `/availability` is chain-wide, the units available for pickup across all Rack stores, not per store. Per store, the site only says yes or no: a store in `pickup_stores[]` can do in-store pickup of that SKU. There is no per-store unit count; never claim a store has a number of units, and never divide `pick_quantity` across stores.
- `pickup_stores[]` lists every eligible Rack store across the US, not just stores near the user. To answer "can I pick it up near me", call `/stores` with the user's ZIP and intersect by `store_number`.
- `/stores` returns Nordstrom Rack stores only (`type: "rack"`); full-line Nordstrom store numbers passed in `store_numbers` are left out. It searches at most 100 miles (`distance_miles` 1-100, default 100). A ZIP with no Rack store in range returns `count: 0` and an empty `stores` list; that call is still charged.
- Rack has its own review pool. `review_count`, `rating` and `/reviews` are Rack's numbers, not nordstrom.com's (the Maeve dress: 129 on Rack, 216 on nordstrom.com). Reviews with `syndicated_from: "nordstrom.com"` were first posted on nordstrom.com, so the two pools overlap; never add the two totals.
- The same style id can exist on both sites (7737947 is the Maeve dress on both), with different prices, SKUs and stock. Do not reuse a nordstrom.com answer for a Rack question or the other way round.
- `reviews[]` on `/product` holds only the reviews shown on the product page (up to about 13), in the page's order, not every review: `review_count` is the full total and `rating_histogram` covers all of them. For the rest, call `/reviews`.
- `/reviews` returns up to `max_reviews` (at most 200) per call and has no page parameter. `has_more: true` means more reviews match than were returned (`total_results` is the matching total); raise `max_reviews`, or narrow with `stars`, `verified_only`, `with_photos` or `search`, or flip `sort`. Do not claim to have read every review unless `has_more` is false.
- `total_results` counts the reviews matching the filters, so with `stars: [1, 2]` it is the number of 1- and 2-star reviews, not the product's total; `summary.total_reviews` is the product's total.
- Rating-only reviews (a star rating with no written review) are included with `title` and `text` null; `summary.ratings_only_count` is how many the product has. Handle a null `text` before quoting or summarizing.
- `sort` and `search` cannot be combined (a 400): text-search results come in the site's own order, and `sort` reads null in the answer.
- `/reviews` is slow: 15-60 seconds, up to about 100 at `max_reviews: 200`. Use a client timeout of at least 120 seconds and ask for only as many reviews as the task needs.
- `size_rating` on a review and `size_fit.distribution[].value` run 1 (too small) to 5 (too big), 3 is true to size. `summary.width_rating` is null where the site has no width rating.
- `review_summary`, `best_features` and `worst_features` (and `ai_summary` on `/reviews`) appear only when the site shows them; they are `null` or empty on many products. A product with no reviews returns an empty `reviews` list from `/reviews`, still charged.
- Category and brand `filters[]` describe the whole listing, not just the page. A group with more than 100 options (such as Brand) lists the 100 with the most products and gives the full `option_count`. Price buckets carry `count: null` because the site shows no count for them. Filters cannot be applied: query parameters in a category URL are ignored, so drill down with `subcategories[].path` instead.
- `rating` and `review_count` can be `null` on a listing row with no reviews yet.
- `/suggestions` returns autocomplete strings only, no products, prices or search volumes.
- Never fabricate prices, sizes, stock, store pickup, sale dates or reviews. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, `category` or `brand`, a `page` outside 1-100, an unknown `sort`, a `url` that is not a nordstromrack.com `/s/` product URL, a nordstrom.com URL or `/browse` path, a `style_id` that is not numeric, neither `url` nor `style_id`, a malformed `sku_id`, a ZIP that is not 5 digits, `latitude` without `longitude`, more than one of `zip` / coordinates / `store_numbers`, `distance_miles` outside 1-100, `limit` outside 1-20, or on `/reviews` an unknown `sort`, `sort` together with `search`, `stars` outside 1-5, `search` over 100 characters, or `max_reviews` outside 1-200).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product, `sku_id`, category or brand (including a nordstrom.com-style `/brands/<name>--<id>` path). Re-run the search for a fresh `url`, or take a category path from `subcategories[]` or a brand path from a product's `brand_url`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data).
- `502` or `503` means Nordstrom Rack is temporarily unavailable or returned an unusable page (for `/availability`, including a failed pickup-store lookup). Upstream checks sometimes fail; it is not charged, so retry after a few seconds. `/reviews` already retries once on its own before answering `502`.
- `503` from `/reviews` with a `Retry-After: 30` header means the reviews endpoint is at capacity. It is not charged; wait the `Retry-After` seconds and send the same request again, and do not fire several review calls in parallel.

## SDKs

```bash
pip install scavio==0.38.0
npm install scavio@0.38.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.nordstromrack.category({ category: "/clearance/women", sort: "percent_off" });
const { data: item } = await scavio.nordstromrack.product({ url: found.products[0].url });
const { data: avail } = await scavio.nordstromrack.availability({ url: item.url }); // 10 credits
const { data: near } = await scavio.nordstromrack.stores({ zip: "10001" });
const { data: brand } = await scavio.nordstromrack.brand({ brand: item.brand_url });
const { data: ideas } = await scavio.nordstromrack.suggestions({ query: "dre" });
const { data: rev } = await scavio.nordstromrack.reviews({ url: item.url, sort: "most_recent", max_reviews: 100 }); // 10 credits, 15-60 s
```

## MCP

The Scavio MCP server exposes all eight endpoints as tools: `search_nordstromrack`, `get_nordstromrack_product`, `get_nordstromrack_category`, `get_nordstromrack_brand`, `get_nordstromrack_availability`, `get_nordstromrack_stores`, `get_nordstromrack_suggestions` and `get_nordstromrack_reviews`. Nordstrom Rack is opt-in: add `nordstromrack` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.36.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,nordstromrack"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/nordstromrack-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data), [category](https://scavio.dev/docs/nordstromrack-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data), [brand](https://scavio.dev/docs/nordstromrack-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data), [product](https://scavio.dev/docs/nordstromrack-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data), [reviews](https://scavio.dev/docs/nordstromrack-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data), [availability](https://scavio.dev/docs/nordstromrack-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data), [stores](https://scavio.dev/docs/nordstromrack-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data), [suggestions](https://scavio.dev/docs/nordstromrack-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data). Overview: [Nordstrom Rack API](https://scavio.dev/nordstromrack-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data). Sibling skill for nordstrom.com: [Nordstrom API](https://scavio.dev/nordstrom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-rack-product-data).
