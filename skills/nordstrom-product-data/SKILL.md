---
name: nordstrom-product-data
description: "Nordstrom product data API: search nordstrom.com or list any category, sale section or brand catalog with price, original price, percent off, rating, badges, every color and filter counts, read one product with every size and color as a SKU with UPC, regular, clearance or promotion price, stock and units available to ship plus the star histogram, size-fit distribution and the reviews on the page, pull a product's review history (up to 200 per call) sorted and filtered by stars, verified purchase, photos or text with the rating summary, size and width fit, praised and criticized features and the AI review summary, check per-SKU ship and store-pickup availability with the stores that can do pickup, find Nordstrom stores near a ZIP with hours, and pull search autocomplete. 8 endpoints, 5 credits each, availability and reviews 10."
version: 1.2.1
tags: nordstrom, nordstrom-api, nordstrom-product-data, nordstrom-scraper, nordstrom-reviews, fashion, apparel, shoes, designer-brands, clothing-prices, sale-tracking, price-drop-alerts, percent-off, clearance, sku-data, upc, size-fit, product-search, product-data, product-reviews, review-analysis, category-browse, brand-catalog, store-locator, store-pickup, in-store-availability, autocomplete, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/nordstrom-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data
---

# Nordstrom Product Data API - Search, Reviews, SKU Stock, Store Pickup

Search Nordstrom (nordstrom.com, US) by keyword, or list any category page (departments such as `/browse/women`, sale sections such as `sale/women`, new arrivals at `/browse/new`) or a brand's catalog, 24 products per page, sorted by relevance, rating, price, newest or percent off: current price and price range, original price range, percent off and on-sale flag, the clearance price range and any promotion price on top with its percent off, rating, review count, badges such as `new` or `new_markdown`, a low-inventory flag, the marketplace seller when Nordstrom is not the seller, and every color with its color family and image. Category and brand pages add the page's breadcrumbs, subcategories and the filter sidebar with product counts per option. Read one product by URL or style id with its description, feature bullets, fit notes, final-sale flag, current, original, clearance and promotion price ranges, the star histogram, the size-fit distribution, breadcrumbs and images, every color and size as a SKU with SKU id, UPC, price, original price, percent off, price type, in-stock flag and the quantity available to ship, and the reviews the product page shows. Pull a product's review history, up to 200 reviews per call, sorted most helpful, most recent, highest or lowest rated and filtered to star ratings, verified purchases, reviews with photos or a text search, with the rating summary, size and width fit, the most praised and criticized features with a quote each, the AI review summary, and per review the reviewer's height, weight, body type and usual sizes when given. Check every SKU's ship and store-pickup availability with the stores that can do in-store pickup, find Nordstrom stores near a ZIP code or point with hours, pickup options and services, and pull the search box's autocomplete suggestions. All endpoints return structured JSON.

See also: for Nordstrom Rack (nordstromrack.com, the off-price store with clearance, Clear the Rack and flash events, its own stores and its own review pool) use the `nordstrom-rack-product-data` skill. The two are separate sites with separate prices, stock and stores.

## When to trigger

Use this skill when the user asks to:
- Find clothing, shoes, bags or beauty at Nordstrom by keyword, and compare prices, ratings and brands
- List everything in a Nordstrom category or sale section (women's dresses, men's shoes, `sale/women`, new arrivals), with filter counts per size, color, brand and discount
- Pull a brand's full Nordstrom catalog (every product a designer or label sells there) for assortment or MAP monitoring
- Track Nordstrom prices or price drops on a product, or list what is on sale (sort by `percent_off`)
- Check which sizes and colors of a Nordstrom product are in stock, and how many units are available online
- Check whether a size can be picked up in a Nordstrom store, and which stores offer pickup for it
- Find Nordstrom stores near a ZIP code or location, with hours, phone, curbside pickup and in-store services
- Get Nordstrom search autocomplete suggestions for keyword research
- Get the UPC, SKU id, regular price and clearance price for every size and color of a style
- Read what Nordstrom reviewers say about fit (runs small, true to size, runs big) and quality
- Pull a Nordstrom product's reviews beyond the product page: the most recent, the most helpful, only the 1- and 2-star complaints, only verified purchases or reviews with photos, or reviews mentioning a word such as "zipper" or "wedding"
- Summarize Nordstrom review sentiment: the most praised and criticized features, the AI review summary, and fit by reviewer height, weight and usual size
- Compare Nordstrom with other retailers on price or availability

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 5 credits except availability and reviews (10 each), so the free credits cover 10 calls (or 5 availability or review calls).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every Nordstrom endpoint costs **5 credits** except `/availability`, which costs **10** (it reads the product page and then looks up the pickup stores), and `/reviews`, which costs **10**. Most calls take 2-7 seconds; availability and large category pages can take 15-30 seconds, and `/reviews` takes 20-60 seconds (up to about 100 seconds at `max_reviews: 200`), so allow a client timeout of at least 120 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/nordstrom/search` | 5 | 24 products per page: position, style id, URL, name, brand, image, current price and price range, original price range, percent off, on-sale flag, clearance price range, promotion price range and promotion percent off, rating, review count, badges, low-inventory flag, marketplace flag and seller, and every color with its color family and image. Plus the total result count, page count and the sorts the site offers |
| `POST /api/v1/nordstrom/category` | 5 | One category page (any `/browse` path: departments, sale sections, new arrivals), 24 products per page in the same shape as search, plus the category's name, title, path, URL, breadcrumbs and subcategories (for drilling down), and the filter sidebar: each filter group with its options and product counts |
| `POST /api/v1/nordstrom/brand` | 5 | One brand's catalog from its brand page, 24 products per page in the same shape as search, plus the brand's name, path, URL, breadcrumbs, sub-pages (Women, Men, Kids...) and the filter sidebar with counts |
| `POST /api/v1/nordstrom/product` | 5 | One product by URL or style id: name, brand, brand URL, description, feature bullets, fit notes, final-sale and in-stock flags, current, original and clearance price ranges, percent off, promotion price range and promotion percent off, marketplace seller, rating, review count, star histogram, size-fit distribution, AI review summary and the most praised and criticized features when the site shows them, breadcrumbs, images, and every color with its images and every size as a SKU (SKU id, size, size type, UPC, price, original price, percent off, price type, in stock, quantity to ship, final sale). Also the reviews shown on the product page (up to about 13), each with title, text, rating, size rating, author, date, helpful votes, verified-purchase flag, size and color purchased, and photos |
| `POST /api/v1/nordstrom/reviews` | 10 | One product's reviews by URL or style id, up to 200 per call (default 60), sorted most helpful, most recent, highest or lowest rated, optionally filtered to star ratings, verified purchases, reviews with photos or a text search. The review summary (average rating, total reviews, star histogram, size rating, width rating where the site has one, the most praised and criticized features with a quote each, count of rating-only reviews), the AI review summary, the number of reviews matching the filters and whether more exist. Each review: id, title, text, rating, size rating, author, date, helpful votes, verified-purchase flag, reviewer badges, size and color purchased, the reviewer's height, weight, body type and usual sizes when given, secondary ratings, the site it was first posted on when syndicated, and photos with thumbnails |
| `POST /api/v1/nordstrom/availability` | 10 | Every SKU of one product (or one SKU): SKU id, size, color, UPC, in stock, ship available and quantity to ship, pickup available and quantity for pickup (both chain-wide), and the stores that can do in-store pickup (store number, name, address, city, state, ZIP, phone). Plus SKU, in-stock and pickup-store counts |
| `POST /api/v1/nordstrom/stores` | 5 | Nordstrom stores (full-line and Nordstrom Local) near a US ZIP or latitude/longitude within up to 100 miles, nearest first, or by store number: store number, name, type, address, phone, weekly hours, holiday hours when posted, open and close times for the next 8 days, time zone, distance, coordinates, pickup and curbside-pickup flags, amenities (services and restaurants) and store page URL |
| `POST /api/v1/nordstrom/suggestions` | 5 | The search box's autocomplete for a partial term: up to 20 suggested queries, most likely first |

## Workflow

1. **Find products:** call `/nordstrom/search` with `query`, `/nordstrom/category` with a category path such as `/browse/women/clothing/dresses` or `sale/women`, or `/nordstrom/brand` with a brand path. Each row has a `url` and a `style_id`. Drill into a category with the `path` of any `category.subcategories[]` entry.
2. **A brand's catalog:** take `brand_url` from a product answer (or the `brand.path` a brand call returns) and pass it as `brand` to `/nordstrom/brand`; page through with `page` until `page_count`.
3. **One product in full:** call `/nordstrom/product` with the row's `url` or `style_id`.
4. **Sizes, colors and stock:** read `colors[].skus[]` on the product answer. Each size of each color has its own `price`, `original_price`, `price_type`, `in_stock` and `quantity`.
5. **Store pickup:** call `/nordstrom/availability` with the same `url` or `style_id` (and `sku_id` for one size). Each SKU lists `pickup_stores[]`; pass their `store_number`s to `/nordstrom/stores` as `store_numbers` for hours and distance, or call `/nordstrom/stores` with the user's `zip` and match store numbers.
6. **Sales and markdowns:** search or list a category with `sort: "percent_off"` for the deepest discounts first, list a sale section such as `sale/women`, or read `percent_off`, `on_sale` and `badges` (`new_markdown`) on any row. On a product, `price_type: "clearance"` marks the clearance SKUs.
7. **Fit and reviews:** `size_fit`, `rating_histogram` and the reviews shown on the page (`reviews[]`, up to about 13) come with the product answer. For more, call `/nordstrom/reviews` with the same `url` or `style_id`: up to 200 reviews per call, sorted (`most_recent`, `lowest_rated`...) or filtered (`stars: [1, 2]` for complaints, `verified_only`, `with_photos`, or `search` for a word). Check `has_more` and `total_results` to see whether the call returned every matching review.
8. **Keyword research:** `/nordstrom/suggestions` with a partial term returns what shoppers are offered as they type; feed a suggestion back into `/nordstrom/search`.

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
| `category` | string | required | A nordstrom.com category: the `/browse` path or full URL of a category page, e.g. `/browse/women/clothing/dresses`, `sale/women`, `/browse/new` or `https://www.nordstrom.com/browse/men/shoes`. The `/browse` prefix is optional. Query parameters in a URL (filters) are ignored |
| `page` | integer | 1 | Results page, 1-based (1-100). 24 products per page |
| `sort` | string | `relevance` | `relevance`, `rating`, `price_high`, `price_low`, `newest` or `percent_off` |

### Brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | required | A nordstrom.com brand: the `/brands` path or full URL of a brand page, usually ending in the brand id, e.g. `/brands/astr-the-label--53360` (a product's `brand_url` works). A brand name without its id is a 404 except where it is the brand page's own path (`/brands/ugg-australia`). Sub-pages such as `/brands/astr-the-label--53360/women` work too |
| `page` | integer | 1 | Results page, 1-based (1-100). 24 products per page |
| `sort` | string | `relevance` | `relevance`, `rating`, `price_high`, `price_low`, `newest` or `percent_off` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | nordstrom.com product URL, the `url` of a search, category or brand result: `https://www.nordstrom.com/s/<slug>/<style id>` |
| `style_id` | string | one of | Nordstrom style id, the number at the end of a product URL (the `style_id` of a result). Used when `url` is not given |

### Availability (`/availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | nordstrom.com product URL (the `url` of a search, category or brand result) |
| `style_id` | string | one of | Nordstrom style id, used when `url` is not given |
| `sku_id` | string | all SKUs | Only this SKU (a product's `colors[].skus[].sku_id`, e.g. `A7578713`). An id that is not a SKU of the product is a 404 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | nordstrom.com product URL (the `url` of a search, category or brand result) |
| `style_id` | string | one of | Nordstrom style id, used when `url` is not given |
| `sort` | string | `most_helpful` | `most_helpful`, `most_recent`, `highest_rated` or `lowest_rated`. Cannot be combined with `search` (a 400): Nordstrom returns review search results in its own order |
| `stars` | array of integers | all | Only reviews with these star ratings, 1-5, e.g. `[1, 2]` for the critical ones |
| `verified_only` | boolean | `false` | Only reviews from verified purchasers |
| `with_photos` | boolean | `false` | Only reviews that include customer photos |
| `search` | string | none | Only reviews mentioning this text (the review search box), 1-100 characters |
| `max_reviews` | integer | 60 | Reviews to return, 1-200. Larger values take longer (45-100 seconds for 200) |

### Stores (`/stores`)

Pass exactly one of `zip`, `latitude` + `longitude`, or `store_numbers`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code to search around (`10001` or `10001-1234`) |
| `latitude` | number | one of | Latitude to search around, with `longitude` |
| `longitude` | number | one of | Longitude to search around, with `latitude` |
| `store_numbers` | array or string | one of | Look stores up by number instead of location: an array or a comma-separated string, up to 100 (an availability result's `pickup_stores[].store_number`) |
| `distance_miles` | integer | 100 | Search radius in miles around `zip` or `latitude`/`longitude`, 1-100 (the site's maximum) |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |
| `limit` | integer | 8 | Suggestions to return, 1-20. The site may return fewer |

## Examples

### Product and search

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstrom/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"style_id": "8098974"}'
```

Captured response (a Betsy & Adam gown in three colors; description, fit notes, breadcrumbs, images, the PERIWINKLE color, 20 of 22 SKUs and 9 of 10 reviews trimmed, one regular and one clearance SKU kept):

```json
{
  "data": {
    "style_id": "8098974",
    "url": "https://www.nordstrom.com/s/betsy-and-adam-strapless-mixed-media-gown/8098974",
    "name": "Strapless Mixed Media Gown",
    "brand": "Betsy & Adam",
    "brand_url": "https://www.nordstrom.com/brands/betsy-adam--243",
    "features": ["60\" length", "Back zip closure", "Scoop neck", "Strapless", "Lined", "100% polyester", "Dry clean", "Made in the USA"],
    "is_final_sale": false,
    "in_stock": true,
    "price": 195.3,
    "price_range": { "min": 195.3, "max": 279 },
    "original_price_range": { "min": 279, "max": 279 },
    "percent_off": 30,
    "on_sale": true,
    "clearance_price_range": { "min": 195.3, "max": 195.3 },
    "is_marketplace": false,
    "seller": null,
    "rating": 3.9,
    "review_count": 34,
    "rating_histogram": [
      { "rating": 5, "count": 20 },
      { "rating": 4, "count": 3 },
      { "rating": 3, "count": 3 },
      { "rating": 2, "count": 2 },
      { "rating": 1, "count": 6 }
    ],
    "size_fit": {
      "average": 2.8636363,
      "distribution": [
        { "value": 1, "label": "too small", "count": 2 },
        { "value": 2, "label": "a little small", "count": 4 },
        { "value": 3, "label": "true to size", "count": 13 },
        { "value": 4, "label": "a little big", "count": 1 },
        { "value": 5, "label": "too big", "count": 2 }
      ]
    },
    "review_summary": null,
    "best_features": [],
    "worst_features": [],
    "color_count": 3,
    "sku_count": 22,
    "colors": [
      {
        "name": "BLACK",
        "color_family": "Black",
        "in_stock": true,
        "skus": [
          {
            "sku_id": "A4030658",
            "size": "2",
            "size_type": "Regular",
            "color": "BLACK",
            "upc": "195170324947",
            "price": 279,
            "original_price": 279,
            "percent_off": 0,
            "price_type": "regular",
            "in_stock": true,
            "quantity": 200,
            "is_final_sale": false
          }
        ]
      },
      {
        "name": "PLUM",
        "color_family": "Purple",
        "in_stock": true,
        "skus": [
          {
            "sku_id": "AAA80925",
            "size": "4",
            "size_type": "Regular",
            "color": "PLUM",
            "upc": "195170319455",
            "price": 195.3,
            "original_price": 279,
            "percent_off": 30,
            "price_type": "clearance",
            "in_stock": true,
            "quantity": 2,
            "is_final_sale": false
          }
        ]
      }
    ],
    "reviews": [
      {
        "review_id": "272633616",
        "title": "Fit like a glove!",
        "text": "It’s very figure flattering dress., just might need to sit on one hip kind of dress lol nice fabric and quality it good.",
        "rating": 4,
        "recommended": null,
        "size_rating": 3,
        "author": "Eviezahir",
        "date": "2026-10-06T02:26:23.000+00:00",
        "helpful_votes": null,
        "verified_purchase": true,
        "size_purchased": "6",
        "color_purchased": "Black",
        "photos": ["https://photos-us.bazaarvoice.com/photo/2/cGhvdG86bm9yZHN0cm9t/d46a7003-bb47-5a63-982e-3d2a522385fb"]
      }
    ]
  },
  "response_time": 2492,
  "credits_used": 5
}
```

A captured `/search` row for `{"query": "dress"}` (47,123 results, 1,964 pages), a product on sale:

```json
{
  "position": 1,
  "style_id": "8098974",
  "url": "https://www.nordstrom.com/s/betsy-and-adam-strapless-mixed-media-gown/8098974",
  "name": "Strapless Mixed Media Gown",
  "brand": "Betsy & Adam",
  "image": "https://n.nordstrommedia.com/it/fa2a7917-c41e-49e4-bf9d-cf4462a8814a.jpeg",
  "price": 195.3,
  "price_range": { "min": 195.3, "max": 279 },
  "original_price_range": { "min": 279, "max": 279 },
  "percent_off": 30,
  "on_sale": true,
  "rating": 3.9,
  "review_count": 34,
  "badges": ["new_markdown"],
  "low_inventory": false,
  "is_marketplace": false,
  "seller": null,
  "colors": [
    { "name": "BLACK", "color_family": "Black", "image": "https://n.nordstrommedia.com/it/fa2a7917-c41e-49e4-bf9d-cf4462a8814a.jpeg" },
    { "name": "PERIWINKLE", "color_family": "Blue", "image": "https://n.nordstrommedia.com/it/ed8fce34-f543-4621-9ac5-8b27abbb8947.jpeg" },
    { "name": "PLUM", "color_family": "Purple", "image": "https://n.nordstrommedia.com/it/4ebe38ad-7a41-477e-bd39-fc85cbbcc8a2.jpeg" }
  ]
}
```

A marketplace row from the same search carries `"is_marketplace": true` and `"seller": "Mac Duggal"`. Search, category and brand rows also carry `clearance_price_range`, `promotion_price_range` and `promotion_percent_off` (added after this capture; null when the style has no clearance or promotion).

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstrom/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "/browse/women/clothing/dresses", "sort": "price_low"}'
```

Captured response (28 of 30 subcategories, 13 of 16 filter groups, all but two options per group and 23 of 24 products trimmed):

```json
{
  "data": {
    "category": {
      "name": "Dresses",
      "title": "Women's Dresses",
      "path": "/browse/women/clothing/dresses",
      "url": "https://www.nordstrom.com/browse/women/clothing/dresses",
      "breadcrumbs": [
        { "name": "Women", "url": "https://www.nordstrom.com/browse/women" },
        { "name": "Clothing", "url": "https://www.nordstrom.com/browse/women/clothing" },
        { "name": "Dresses", "url": "https://www.nordstrom.com/browse/women/clothing/dresses" }
      ],
      "subcategories": [
        { "name": "Women's Sale Dresses", "path": "/browse/sale/women/clothing/dresses", "url": "https://www.nordstrom.com/browse/sale/women/clothing/dresses" },
        { "name": "New Arrivals", "path": "/browse/women/clothing/dresses/new", "url": "https://www.nordstrom.com/browse/women/clothing/dresses/new" }
      ]
    },
    "page": 1,
    "sort": "price_low",
    "total_results": 40339,
    "page_count": 1681,
    "count": 24,
    "available_sorts": ["rating", "price_high", "price_low", "newest", "percent_off", "relevance"],
    "filters": [
      {
        "name": "Brand",
        "option_count": 1012,
        "options": [
          { "label": "Mac Duggal", "count": 1712 },
          { "label": "Petal & Pup", "count": 1451 }
        ]
      },
      {
        "name": "Price",
        "option_count": 9,
        "options": [
          { "label": "$0 - $50", "count": null },
          { "label": "$50 - $100", "count": null }
        ]
      },
      {
        "name": "Discount",
        "option_count": 6,
        "options": [
          { "label": "20% off or more", "count": 12103 },
          { "label": "30% off or more", "count": 9567 }
        ]
      }
    ],
    "products": [
      {
        "position": 1,
        "style_id": "6414645",
        "url": "https://www.nordstrom.com/s/lnl-asymmetric-glitter-knit-minidress/6414645",
        "name": "Asymmetric Glitter Knit Minidress",
        "brand": "LNL",
        "image": "https://n.nordstrommedia.com/it/e73e1e52-52eb-4b9e-8f1a-a84d772cd26c.jpeg",
        "price": 14.97,
        "price_range": { "min": 14.97, "max": 14.97 },
        "original_price_range": { "min": 50, "max": 50 },
        "percent_off": 70,
        "on_sale": true,
        "rating": null,
        "review_count": null,
        "badges": [],
        "low_inventory": true,
        "is_marketplace": false,
        "seller": null,
        "colors": [
          { "name": "QUARTZ", "color_family": "Beige", "image": "https://n.nordstrommedia.com/it/e73e1e52-52eb-4b9e-8f1a-a84d772cd26c.jpeg" }
        ]
      }
    ]
  },
  "response_time": 28541,
  "credits_used": 5
}
```

### Brand

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstrom/brand \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "/brands/astr-the-label--53360"}'
```

Captured `data.brand` (371 products over 16 pages; `filters` and `products` have the same shape as category):

```json
{
  "name": "ASTR the Label",
  "title": "ASTR the Label",
  "path": "/brands/astr-the-label--53360",
  "url": "https://www.nordstrom.com/brands/astr-the-label--53360",
  "breadcrumbs": [
    { "name": "Brands", "url": "https://www.nordstrom.com/brands-list" },
    { "name": "ASTR the Label", "url": "https://www.nordstrom.com/brands/astr-the-label--53360" }
  ],
  "subcategories": [
    { "name": "Women", "path": "/brands/astr-the-label--53360/women", "url": "https://www.nordstrom.com/brands/astr-the-label--53360/women" }
  ]
}
```

### Availability

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstrom/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"style_id": "7737947"}'
```

Captured response (58 of 59 SKUs and 2 of this SKU's 4 pickup stores trimmed):

```json
{
  "data": {
    "style_id": "7737947",
    "url": "https://www.nordstrom.com/s/maeve-midi-dress/7737947",
    "name": "Maeve Midi Dress",
    "brand": "ASTR the Label",
    "sku_id": null,
    "sku_count": 59,
    "in_stock_count": 39,
    "pickup_store_count": 85,
    "skus": [
      {
        "sku_id": "A7578713",
        "size": "Large",
        "color": "DARK TEAL",
        "upc": "191293689772",
        "in_stock": true,
        "ship_available": true,
        "ship_quantity": 4,
        "pickup_available": true,
        "pick_quantity": 4,
        "pickup_store_count": 4,
        "pickup_stores": [
          { "store_number": "10", "name": "Nordstrom Alderwood Mall", "address": "3200 184th Street SW", "city": "Lynnwood", "state": "WA", "zip": "98037", "phone": "425.771.5755" },
          { "store_number": "425", "name": "Nordstrom Valley Fair", "address": "2400 Forest Avenue", "city": "San Jose", "state": "CA", "zip": "95128", "phone": "408.248.2180" }
        ]
      }
    ]
  },
  "response_time": 12585,
  "credits_used": 10
}
```

`pick_quantity: 4` is the chain-wide pickup total for that SKU, not 4 units in each listed store. The pickup stores span the whole US (Lynnwood WA, San Jose CA, Houston TX on this SKU), not the area near the user.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstrom/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10001"}'
```

Captured response (13 of 14 stores, 6 of 8 days of `daily_hours` and 5 of 7 amenities trimmed):

```json
{
  "data": {
    "zip": "10001",
    "latitude": null,
    "longitude": null,
    "store_numbers": null,
    "distance_miles": 100,
    "count": 14,
    "stores": [
      {
        "store_number": "201",
        "name": "Nordstrom Local West Village",
        "type": "local",
        "address": "13 7th Ave",
        "city": "New York",
        "state": "NY",
        "zip": "10011",
        "country": "US",
        "phone": "332.204.8965",
        "hours": ["Mon-Fri 10am-7pm", "Sat-Sun 10am-6pm"],
        "special_hours": null,
        "daily_hours": [
          { "opens": "2026-11-07T10:00:00-05:00", "closes": "2026-11-07T18:00:00-05:00" },
          { "opens": "2026-11-08T10:00:00-05:00", "closes": "2026-11-08T18:00:00-05:00" }
        ],
        "time_zone": "America/New_York",
        "distance_miles": 1.09,
        "latitude": 40.736918,
        "longitude": -74.000661,
        "pickup": true,
        "curbside_pickup": true,
        "amenities": [
          { "name": "Alterations", "type": "service", "phone": null, "hours": [] },
          { "name": "Buy Online & Pick Up In Store", "type": "service", "phone": null, "hours": [] }
        ],
        "url": "https://www.nordstrom.com/store-details/nordstrom-local-west-village"
      }
    ]
  },
  "response_time": 1306,
  "credits_used": 5
}
```

The same answer lists full-line stores such as `"store_number": "210"`, `"name": "Nordstrom NYC Flagship"`, `"type": "full_line"` at 1.2 miles. A restaurant amenity carries its own phone and hours (`"Bistro Verde"`, `"type": "restaurant"`, `"hours": ["Mon-Sat 11am-7:30pm", "Sun 11am-6:30pm"]`). Where holiday hours are posted, `special_hours` is `{ "label": "Holiday Store Hours", "hours": ["Nov 25: 10am-8pm", "Nov 26: Closed", ...] }`.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstrom/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nike air"}'
```

Captured response:

```json
{
  "data": {
    "query": "nike air",
    "count": 8,
    "suggestions": ["nike air force 1", "nike air max", "nike air max 90", "nike air rift", "nike air max 270", "nike air force 1 '07", "nike air force", "nike women's air jordan shoes"]
  },
  "response_time": 1577,
  "credits_used": 5
}
```

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/nordstrom/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"style_id": "7737947", "max_reviews": 18}'
```

Captured response (3 of 5 best features and 17 of 18 reviews trimmed):

```json
{
  "data": {
    "style_id": "7737947",
    "url": "https://www.nordstrom.com/s/maeve-midi-dress/7737947",
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
    "total_results": 216,
    "returned": 18,
    "has_more": true,
    "summary": {
      "average_rating": 4.13,
      "total_reviews": 216,
      "ratings_histogram": [
        { "rating": 5, "count": 136 },
        { "rating": 4, "count": 18 },
        { "rating": 3, "count": 32 },
        { "rating": 2, "count": 15 },
        { "rating": 1, "count": 15 }
      ],
      "size_rating": 2.976,
      "width_rating": null,
      "best_features": [
        { "name": "fit", "mentions": 38, "quote": "This dress is gorgeous and fits true to size." },
        { "name": "appearance", "mentions": 36, "quote": "We purchased for a wedding in June and the blue is beautiful!" }
      ],
      "worst_features": [
        { "name": "zipper", "mentions": 4, "quote": "But the zipper is junky and won’t lay flat." }
      ],
      "ratings_only_count": 78
    },
    "ai_summary": "* Customers praise the soft, lightweight, silky fabric that drapes gracefully and feels luxurious against skin\n* Many highlight the flattering, body-inclusive fit with smocked back and adjustable straps accommodating diverse shapes\n* Reviewers love the vibrant, elegant colors and romantic aesthetic perfect for weddings and special events\n* Several note comfortable, breathable wear without restriction, ideal for extended wear in warm weather\n* A few report fit inconsistencies around the bust or occasional zipper issues, though isolated concerns",
    "reviews": [
      {
        "review_id": "242289044",
        "title": "Bump Friendly for Petite Maternity Wear",
        "text": "This dress is cute and super lightweight but feels thin. It’s not clingy so can work just fine, but wish there was lining for the skirt part of the dress. I do feel like the chest area is a bit too wide but maybe an XS would have worked better. It’s bump friendly which was nice! Currently 28 weeks.",
        "rating": 4,
        "size_rating": 3,
        "author": "MishaMeta",
        "date": "2025-05-30T15:37:01.000+00:00",
        "helpful_votes": 24,
        "verified_purchase": false,
        "size_purchased": "Small",
        "color_purchased": "Multi Blue Floral",
        "badges": [],
        "height": "5' 2\"",
        "weight": "98 lbs.",
        "body_type": ["Waist narrower than shoulders and hips"],
        "usual_sizes": ["X-Small", "Small"],
        "secondary_ratings": [
          { "name": "Size", "rating": 3, "max": 5 }
        ],
        "syndicated_from": null,
        "photos": [
          { "url": "https://photos-us.bazaarvoice.com/photo/2/cGhvdG86bm9yZHN0cm9t/d99f0e94-4301-5a9d-8147-79b199c89a2e", "thumbnail_url": "https://photos-us.bazaarvoice.com/photo/2/cGhvdG86bm9yZHN0cm9t/e191c9b7-6c0f-5dc3-896b-5835e31ac8b3" },
          { "url": "https://photos-us.bazaarvoice.com/photo/2/cGhvdG86bm9yZHN0cm9t/94684334-2eab-5569-9cdb-7d9ce78c5c58", "thumbnail_url": "https://photos-us.bazaarvoice.com/photo/2/cGhvdG86bm9yZHN0cm9t/e3492d99-7a71-5836-8b08-d2f57e38c84e" }
        ]
      }
    ]
  },
  "response_time": 13765,
  "credits_used": 10
}
```

`has_more: true` with `total_results: 216` means 198 more reviews match; raise `max_reviews` (up to 200) to get them. For the complaints only, send `{"style_id": "7737947", "stars": [1, 2], "sort": "most_recent"}`; for reviews mentioning a word, send `{"style_id": "7737947", "search": "zipper"}` with no `sort`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def nordstrom(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/nordstrom/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Deepest discounts in a sale section first (5 credits)
found = nordstrom("category", {"category": "sale/women", "sort": "percent_off"})
for p in found["products"][:5]:
    print(p["brand"], p["name"], p["price"], "was", p["original_price_range"], f'{p["percent_off"]}% off')

# 2. One product: every size and color, clearance SKUs and units to ship (5 credits)
item = nordstrom("product", {"url": found["products"][0]["url"]})
for color in item["colors"]:
    for s in color["skus"]:
        print(color["name"], s["size"], s["upc"], s["price"], s["price_type"], "in stock" if s["in_stock"] else "out", s["quantity"])

# 3. Store pickup per SKU, then the user's nearby stores (10 + 5 credits)
avail = nordstrom("availability", {"url": item["url"]})
near = nordstrom("stores", {"zip": "10001", "distance_miles": 25})
near_numbers = {st["store_number"]: st for st in near["stores"]}
for s in avail["skus"]:
    nearby = [p["name"] for p in s["pickup_stores"] if p["store_number"] in near_numbers]
    print(s["size"], s["color"], "ships", s["ship_quantity"], "pickup near you:", nearby or "none")

# 4. The newest 1- and 2-star reviews, and what reviewers praise and criticize (10 credits, 20-60 s)
rev = nordstrom("reviews", {"url": item["url"], "stars": [1, 2], "sort": "most_recent", "max_reviews": 40})
summary = rev["summary"] or {}
print(rev["total_results"], "critical reviews; average", summary.get("average_rating"), "size rating", summary.get("size_rating"))
for f in summary.get("worst_features", []):
    print("criticized:", f["name"], f["mentions"], f["quote"])
for r in rev["reviews"]:
    print(r["rating"], (r["date"] or "")[:10], r["size_purchased"], r["title"], (r["text"] or "")[:120])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Nordstrom answered.

- **search** - `query`, `page`, `sort`, `total_results`, `page_count`, `count`, `available_sorts[]`, `products[]` (`position`, `style_id`, `url`, `name`, `brand`, `image`, `price`, `price_range` {`min`, `max`}, `original_price_range` {`min`, `max`}, `percent_off`, `on_sale`, `clearance_price_range` ({`min`, `max`} or null), `promotion_price_range` ({`min`, `max`} or null), `promotion_percent_off`, `rating`, `review_count`, `badges[]`, `low_inventory`, `is_marketplace`, `seller`, `colors[]` {`name`, `color_family`, `image`}).
- **category** - `category` {`name`, `title`, `path`, `url`, `breadcrumbs[]` {`name`, `url`}, `subcategories[]` {`name`, `path`, `url`}}, `page`, `sort`, `total_results`, `page_count`, `count`, `available_sorts[]`, `filters[]` {`name`, `option_count`, `options[]` {`label`, `count`}}, `products[]` (same fields as search).
- **brand** - `brand` {`name`, `title`, `path`, `url`, `breadcrumbs[]`, `subcategories[]`}, then the same fields as category.
- **product** - `style_id`, `url`, `name`, `brand`, `brand_url`, `description`, `features[]`, `fit_info[]`, `is_final_sale`, `in_stock`, `price`, `price_range`, `original_price_range`, `percent_off`, `on_sale`, `clearance_price_range`, `promotion_price_range`, `promotion_percent_off`, `is_marketplace`, `seller`, `rating`, `review_count`, `rating_histogram[]` {`rating`, `count`}, `size_fit` {`average`, `distribution[]` {`value`, `label`, `count`}} or null, `review_summary`, `best_features[]` and `worst_features[]` {`name`, `mentions`, `quote`}, `breadcrumbs[]` {`name`, `url`}, `images[]`, `color_count`, `sku_count`, `colors[]` (`name`, `color_family`, `in_stock`, `images[]`, `skus[]` {`sku_id`, `size`, `size_type`, `color`, `upc`, `price`, `original_price`, `percent_off`, `price_type`, `in_stock`, `quantity`, `is_final_sale`}), `reviews[]` (`review_id`, `title`, `text`, `rating`, `recommended`, `size_rating`, `author`, `date`, `helpful_votes`, `verified_purchase`, `size_purchased`, `color_purchased`, `photos[]`).
- **reviews** - `style_id`, `url`, `name`, `brand`, `sort` (null when `search` is set), `filters` {`stars[]`, `verified_only`, `with_photos`, `search`} and `max_reviews` (the request echoed), `total_results` (reviews matching the filters), `returned`, `has_more`, `summary` ({`average_rating`, `total_reviews`, `ratings_histogram[]` {`rating`, `count`}, `size_rating`, `width_rating`, `best_features[]` and `worst_features[]` {`name`, `mentions`, `quote`}, `ratings_only_count`} or null), `ai_summary`, `reviews[]` {`review_id`, `title`, `text`, `rating`, `size_rating`, `author`, `date`, `helpful_votes`, `verified_purchase`, `size_purchased`, `color_purchased`, `badges[]`, `height`, `weight`, `body_type[]`, `usual_sizes[]`, `secondary_ratings[]` {`name`, `rating`, `max`}, `syndicated_from`, `photos[]` {`url`, `thumbnail_url`}}.
- **availability** - `style_id`, `url`, `name`, `brand`, `sku_id` (the requested SKU or null), `sku_count`, `in_stock_count`, `pickup_store_count`, `skus[]` {`sku_id`, `size`, `color`, `upc`, `in_stock`, `ship_available`, `ship_quantity`, `pickup_available`, `pick_quantity`, `pickup_store_count`, `pickup_stores[]` {`store_number`, `name`, `address`, `city`, `state`, `zip`, `phone`}}.
- **stores** - `zip`, `latitude`, `longitude`, `store_numbers`, `distance_miles` (the request echoed), `count`, `stores[]` {`store_number`, `name`, `type` (`full_line` or `local`), `address`, `city`, `state`, `zip`, `country`, `phone`, `hours[]`, `special_hours` ({`label`, `hours[]`} or null), `daily_hours[]` {`opens`, `closes`}, `time_zone`, `distance_miles`, `latitude`, `longitude`, `pickup`, `curbside_pickup`, `amenities[]` {`name`, `type`, `phone`, `hours[]`}, `url`}.
- **suggestions** - `query`, `count`, `suggestions[]` (strings).

## Guardrails

- Prices are in US dollars: `195.3` is $195.30. This is nordstrom.com (US) only.
- `price` on a style is the low end of `price_range`, the lowest current price across its sizes and colors. `percent_off` on a style is the largest discount across them. When the range spans more than one price (as in the gown above, $195.30 to $279), quote the range or read the exact SKU's price from `/product`; never present the low end as the price of every size.
- `original_price_range` and a SKU's `original_price` are the regular price the discount is measured from. `price_type` on a SKU is `regular`, `clearance` or `promotion`; `clearance_price_range` (on products and listing rows) is set only when some SKUs are on clearance. `promotion_price_range` is the price with an extra discount on top, set only while one applies, and `promotion_percent_off` is that extra percent: off the clearance price on a clearance item, otherwise off the regular price. Both are null on most items. No response carries a sale's start or end date; never state one.
- `in_stock` on a product SKU means the SKU can be shipped OR picked up in a store. `quantity` is the units available to ship online only, so a SKU can be `in_stock: true` with `quantity: 0` when it is held only in stores. Call `/availability` to see whether it ships or is pickup-only and where.
- `pick_quantity` on `/availability` is chain-wide, the units available for pickup across all of Nordstrom, not per store. Per store, Nordstrom only says yes or no: a store in `pickup_stores[]` can do in-store pickup of that SKU. There is no per-store unit count; never claim a store has a number of units, and never divide `pick_quantity` across stores.
- `pickup_stores[]` lists every eligible store across the US, not just stores near the user. To answer "can I pick it up near me", call `/stores` with the user's ZIP and intersect by `store_number`.
- `/stores` searches at most 100 miles (`distance_miles` 1-100, default 100). A ZIP with no Nordstrom store in range returns `count: 0` and an empty `stores` list; that call is still charged. `type: "local"` is a Nordstrom Local service hub, not a full-line department store; say so when it matters.
- `in_stock` on a color is true when any of its sizes is in stock. Read `skus[]` for the size the user wants.
- `is_marketplace: true` means a third-party seller (`seller`) sells the item through Nordstrom; say so when quoting it.
- `reviews[]` on `/product` holds only the reviews shown on the product page (up to about 13), in the page's order, not every review: `review_count` is the full total and `rating_histogram` covers all of them. For the rest, call `/reviews`.
- `/reviews` returns up to `max_reviews` (at most 200) per call and has no page parameter. `has_more: true` means more reviews match than were returned (`total_results` is the matching total); raise `max_reviews`, or narrow with `stars`, `verified_only`, `with_photos` or `search`, or flip `sort`. Do not claim to have read every review unless `has_more` is false.
- `total_results` counts the reviews matching the filters, so with `stars: [1, 2]` it is the number of 1- and 2-star reviews, not the product's total; `summary.total_reviews` is the product's total.
- Rating-only reviews (a star rating with no written review) are included with `title` and `text` null; `summary.ratings_only_count` is how many the product has. Handle a null `text` before quoting or summarizing.
- `sort` and `search` cannot be combined (a 400): text-search results come in Nordstrom's own order, and `sort` reads null in the answer.
- `syndicated_from` is set when a review was first posted on another site and shown on nordstrom.com; null otherwise. `badges[]` holds reviewer badges such as `verified_purchaser`, `top_250` and `top_1000`. `height`, `weight`, `body_type` and `usual_sizes` are free text the reviewer chose to give, often null or empty.
- `/reviews` is slow: 20-60 seconds, up to about 100 at `max_reviews: 200`. Use a client timeout of at least 120 seconds and ask for only as many reviews as the task needs.
- `size_rating` on a review and `size_fit.distribution[].value` run 1 (too small) to 5 (too big), 3 is true to size. On `/reviews`, `summary.size_rating` is the average on the same scale (`2.976` is true to size) and `summary.width_rating` is null where the site has no width rating.
- `review_summary`, `best_features` and `worst_features` (and `ai_summary` on `/reviews`) appear only when Nordstrom shows them; they are `null` or empty on many products. A product with no reviews returns an empty `reviews` list from `/reviews`, still charged.
- Category and brand `filters[]` describe the whole listing, not just the page. A group with more than 100 options (such as Brand) lists the 100 with the most products and gives the full `option_count`. Price buckets carry `count: null` because the site shows no count for them. Filters cannot be applied: query parameters in a category URL are ignored, so drill down with `subcategories[].path` or a sale path instead.
- `rating` and `review_count` can be `null` on a listing row with no reviews yet.
- `/suggestions` returns autocomplete strings only, no products, prices or search volumes.
- Never fabricate prices, sizes, stock, store pickup or reviews. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, `category` or `brand`, a `page` outside 1-100, an unknown `sort`, a `url` that is not a nordstrom.com `/s/` product URL, a `style_id` that is not numeric, neither `url` nor `style_id`, a malformed `sku_id`, a ZIP that is not 5 digits, `latitude` without `longitude`, more than one of `zip` / coordinates / `store_numbers`, `distance_miles` outside 1-100, `limit` outside 1-20, or on `/reviews` an unknown `sort`, `sort` together with `search`, `stars` outside 1-5, `search` over 100 characters, or `max_reviews` outside 1-200).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product, `sku_id`, category or brand. Re-run the search for a fresh `url`, or take a category path from `subcategories[]` or a brand path from a product's `brand_url`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data).
- `502` or `503` means Nordstrom is temporarily unavailable or returned an unusable page (for `/availability`, including a failed pickup-store lookup). It is not charged; retry after a few seconds. `/reviews` already retries once on its own before answering `502`.
- `503` from `/reviews` with a `Retry-After: 30` header means the reviews endpoint is at capacity. It is not charged; wait the `Retry-After` seconds and send the same request again, and do not fire several review calls in parallel.

## SDKs

```bash
pip install scavio==0.37.0
npm install scavio@0.37.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.nordstrom.category({ category: "sale/women", sort: "percent_off" });
const { data: item } = await scavio.nordstrom.product({ url: found.products[0].url });
const { data: avail } = await scavio.nordstrom.availability({ url: item.url }); // 10 credits
const { data: near } = await scavio.nordstrom.stores({ zip: "10001" });
const { data: brand } = await scavio.nordstrom.brand({ brand: item.brand_url });
const { data: ideas } = await scavio.nordstrom.suggestions({ query: "nike air" });
const { data: rev } = await scavio.nordstrom.reviews({ url: item.url, sort: "most_recent", max_reviews: 100 }); // 10 credits, 20-60 s
```

## MCP

The Scavio MCP server exposes all eight endpoints as tools: `search_nordstrom`, `get_nordstrom_product`, `get_nordstrom_category`, `get_nordstrom_brand`, `get_nordstrom_availability`, `get_nordstrom_stores`, `get_nordstrom_suggestions` and `get_nordstrom_reviews`. Nordstrom is opt-in: add `nordstrom` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.35.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,nordstrom"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/nordstrom-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [category](https://scavio.dev/docs/nordstrom-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [brand](https://scavio.dev/docs/nordstrom-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [product](https://scavio.dev/docs/nordstrom-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [reviews](https://scavio.dev/docs/nordstrom-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [availability](https://scavio.dev/docs/nordstrom-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [stores](https://scavio.dev/docs/nordstrom-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [suggestions](https://scavio.dev/docs/nordstrom-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data). Overview: [Nordstrom API](https://scavio.dev/nordstrom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data). Sibling skill for nordstromrack.com: [Nordstrom Rack API](https://scavio.dev/nordstromrack-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data).
