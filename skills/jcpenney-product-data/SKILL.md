---
name: jcpenney-product-data
description: "JCPenney API: search jcpenney.com or browse any category, a brand, or the Clearance, Sale, Black Friday, Big Buy, Limited Time Special, Closeout and Buy 1 Get 1 deal lists, 48 products per page (up to 25 pages) with the current and regular price range, price type (sale, clearance, original), percent off, deal label, the price after today's coupon with the coupon code, rating, review count, badge and colors, filtered by brand, color, size, price range, deal label or any facet (store pickup, rating, gender), for JCPenney clearance tracking and price alerts; read one product with every variant's SKU, UPC, color, size and online stock level, or up to 20 products in one call (prices are product-level ranges; review text is not available); get real unit counts for one SKU at the 5 nearest JCPenney stores to a ZIP; find stores with hours and services; pull search suggestions and today's public JCPenney coupon codes. 9 endpoints, 1 credit each. JCPenney publishes no public developer API."
version: 1.0.0
tags: jcpenney, jcpenney-api, jcpenney-product-data, jcpenney-scraper, jcp, jcpenney-clearance, jcpenney-price-tracker, jcpenney-coupons, jcpenney-coupon-codes, jcpenney-in-stock, jcpenney-store-availability, jcpenney-black-friday, jcpenney-deals, jcpenney-sale, clearance-tracker, price-drop-alerts, coupon-codes, store-availability, store-locator, inventory, department-store, apparel, home-goods, beauty, upc, variant-data, batch-products, product-search, product-data, category-browse, brand-catalog, autocomplete, retail, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/jcpenney-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data
---

# JCPenney Product Data API - Clearance, Coupons, Store Stock

Search JCPenney (jcpenney.com, US with Puerto Rico stores, prices in USD) by keyword, or browse a category by its path or URL, one brand by name, or one of the deal lists (Clearance, Sale, Black Friday deals, Big Buy, Limited Time Special, Best Value, Gotta Have It, Closeout, Buy 1 Get 1, or any Deals & Promotions label), 48 products per page and at most 25 pages (1,200 items) per query. Sort by relevance, new arrivals, best sellers, rating or price; filter by brand, color, size, price range, deal label, or any facet value the response lists (store availability, average rating, gender, rise...). Each item carries the id, title, brand, URL, image, SKU id, current price and the top of its range, regular price, `price_type` (`sale`, `clearance`, `original`), percent off, deal label, the price after today's coupon (`coupon_price`) with the `coupon_code`, the average rating, review count, badge (Only at JCP, NEW, Few Left), availability labels, colors with their SKU ids, and a marketplace flag with the seller for third-party items. Read one product by id or URL with its description, features, breadcrumbs, rating, review and question counts, the price block (regular, sale and clearance ranges, percent off, deal label, the after-coupon price and when the price starts and ends), and every variant (SKU, UPC, color, size, status, max per order, online stock as high, low or out); or read up to 20 products in one call for price checks. Check one SKU's real unit count at the 5 nearest stores to a ZIP. Find stores with weekly hours, services (salon, portrait studio, JCPenney Beauty, curbside pickup...) and pickup directions, pull the search box's suggestions and today's public coupon codes. All endpoints return structured JSON, 1 credit each.

See also: for Kohl's clearance, Kohl's Cash and store pickup use the `kohls-product-data` skill; for Macy's use `macys-product-data`; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Track JCPenney clearance: list the Clearance deals (optionally one brand, size, department or price range) and detect new markdowns between runs
- Build a JCPenney price tracker or sale alert: poll products (up to 20 per call) or listings and detect a price drop, a new sale or clearance price, or a better after-coupon price
- Get today's JCPenney coupon codes, or the price of an item after today's coupon
- Check whether a JCPenney item (one color and size) is in stock at the stores near a ZIP code, and how many units each store has
- Search JCPenney for a product and compare prices, percent off, ratings and brands, or browse a category (dresses, jeans, bedding...) or a brand's whole JCPenney catalog
- Prepare a JCPenney Black Friday watch list from the Black Friday deal list
- Find JCPenney stores near a ZIP, a city or a point, with hours, salon, portrait studio, JCPenney Beauty and curbside pickup
- Get JCPenney search suggestions for keyword research

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Every endpoint answered in 3 to 7 seconds in the captures (listings 3-6, product about 4, suggestions about 7). Allow a client timeout of at least 60 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/jcpenney/search` | 1 | 48 products per page: id, title, brand, URL, image, `sku_id`, `price`, `price_max`, `regular_price`, `regular_price_max`, `price_type`, `percent_off`, `price_in_cart`, `deal_label`, `coupon_price`, `coupon_price_max`, `coupon_code`, rating, review count, `badge`, `availability_label[]`, `colors[]` with SKU ids, `is_marketplace`, `seller`. Plus `corrected_query`, `redirected_to`, total, page, total pages, per page, max pages, sort, count, `applied_filters`, `facets[]` with values and counts |
| `POST /api/v1/jcpenney/category` | 1 | One category by `path` or `url` (a `/g/` page with its `id=cat...`), the same grid as search, plus the category's name, id, path, URL and breadcrumbs |
| `POST /api/v1/jcpenney/brand` | 1 | One brand by name as JCPenney lists it (`"Nike"`, `"St. John's Bay"`) or by brand page URL, the same grid as search, plus the brand's name, value and URL |
| `POST /api/v1/jcpenney/deals` | 1 | A deal list by `type`: `clearance` (default), `sale`, `black_friday`, `big_buy`, `limited_time_special`, `best_value`, `gotta_have_it`, `closeout` or `bogo`, or any Deals & Promotions `label`, across all products or one `department`; the same grid as search plus the labels applied |
| `POST /api/v1/jcpenney/product` | 1 | One product by `product_id` or `url`: title, brand, description, features, category, breadcrumbs, product and item type, images, rating, review count, question and answer counts, the `price` block (current, regular, sale and clearance min / max, percent off, price type, deal label, `coupon` {code, price min / max}, `starts_at`, `ends_at`), channel, in-store pickup, marketplace flag, and every variant (sku, UPC, color, size, options, status, `online_stock` high / low / out, max quantity). Or up to 20 by `product_ids` in one call (no online stock), with `not_found` |
| `POST /api/v1/jcpenney/stores` | 1 | JCPenney stores near a ZIP, a city + state or a lat/lng point within 1-100 miles (default 25), paged: store id, name, address, city, state, ZIP, phone, lat, lng, distance, weekly hours, timezone, services, curbside and in-store pickup directions, bookable appointments (Sephora, salon) and the store page URL |
| `POST /api/v1/jcpenney/store-availability` | 1 | One SKU at the 5 nearest stores to a ZIP (or lat + lng): per store `quantity` (a real unit count), `status` (`in_stock`, `low`, `out_of_stock`, `not_stocked`), `stocked`, `updated_at`, address, phone, distance and hours. Plus `count`, `stores_with_stock`, `total_quantity` |
| `POST /api/v1/jcpenney/suggestions` | 1 | The search box's suggestions for a partial term: each `term` with its search URL and, where JCPenney offers them, department refinements |
| `POST /api/v1/jcpenney/coupons` | 1 | Today's public JCPenney coupons: `code` (null for in-store offers that need none), `channel` (`online`, `in store`, `both`), headline, details, every offer under the coupon, `starts_at`, `ends_at`, the full disclaimer with its exclusions, and the eligible-products URL |

## Workflow

1. **Find products:** call `/jcpenney/search` with `query`, `/jcpenney/deals` with a `type`, `/jcpenney/brand` with a `brand` name, or `/jcpenney/category` with a `/g/` `path`. Each item has an `id` and a `url`.
2. **Narrow the listing:** pass `brand`, `color`, `size`, `price_range` or `deal` (search and category), or any facet through `filters` as `{facets[].id: facets[].values[].value}` (`{"gender": "women", "store_availability": "same day pickup"}`). Price is a facet bucket like `$20 - $24`, not a free range.
3. **Page through:** `page` 1, 2, 3... up to `total_pages`. A page holds 48 products and the deepest page is 25, so a query reaches at most 1,200 items: narrow with filters to see the rest.
4. **One product in full:** call `/jcpenney/product` with the item's `id` as `product_id` (or its `url`). Read `price` for the price ranges and today's coupon, and `variants[]` for each SKU's color, size, UPC and online stock.
5. **Store stock:** call `/jcpenney/store-availability` with a `variants[].sku` and the user's `zip`. Each of the 5 nearest stores gives `quantity`, a real unit count.
6. **Price tracking:** call `/jcpenney/product` with up to 20 `product_ids` per call (1 credit), or walk `/jcpenney/deals` with `type: "clearance"`, and store `id`, `price`, `regular_price`, `price_type`, `percent_off`, `coupon_price` per run. Compare runs yourself: there is no price history.
7. **Coupons:** `/jcpenney/coupons` lists today's public codes. A listing item's `coupon_price` and `coupon_code` (and `price.coupon` on `/product`) already show what today's coupon does to that item.
8. **Keyword research:** `/jcpenney/suggestions` with a partial term returns completions with their department refinements.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-25). 48 products per page. A page past the last one returns an empty `items` list with the real `total` |
| `sort` | string | `relevance` | `relevance`, `new_arrivals`, `best_sellers`, `rating` (highest rated first), `price_low_to_high` or `price_high_to_low` |
| `brand` | string or array | none | A brand as the `Brand` facet lists it (`"levi's"`, `"nike"`, `"st. john's bay"`), or several (any of them) |
| `color` | string or array | none | A color as the `Color` facet lists it (`black`, `blue`, `beige`...) |
| `size` | string or array | none | A size as the `Size` facet lists it (`m`, `12`, `32x30`...) |
| `price_range` | string or array | none | A `Price Range` facet value (`"under $5"`, `"$20 - $24"`) |
| `deal` | string or array | none | A Deals & Promotions label as the facet lists it (`"SALE"`, `"CLEARANCE"`, `"BIG BUY!"`) |
| `filters` | object | none | Any facet from a previous answer: `{facets[].id: value}` or `{facets[].id: [values]}` (any of them), e.g. `{"gender": "women"}`, `{"store_availability": "same day pickup"}`, `{"average_rating": "4 rating"}`, `{"rise": ["mid rise", "high rise"]}`. Several facets combine (AND) |
| `exact` | boolean | `false` | JCPenney narrows many keywords to a category on its own (`jeans` lands in the Jeans category, visible in `applied_filters`). `true` searches the keyword across every category instead |

Each of `brand`, `color`, `size`, `price_range` and `deal` takes one value or a list of up to 20; at most 10 facets per call.

### Category (`/category`)

Pass `path` or `url` (not both), plus any search parameter except `query` and `exact`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | one of | A JCPenney category path WITH its `id=cat...` part: `/g/women/dresses?id=cat100210008`. Take it from a jcpenney.com category link or a response's `category.breadcrumbs[].path` |
| `url` | string | one of | A jcpenney.com category URL (`https://www.jcpenney.com/g/women/dresses?id=cat100210008`). Filters, a sort or a page in the URL are kept |

### Brand (`/brand`)

Pass `brand` or `url` (not both), plus any search parameter except `query`, `exact` and the `brand` filter.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | one of | A brand name as JCPenney lists it in the `Brand` facet (`"Nike"`, `"St. John's Bay"`, `"Carter's"`). An unknown brand is a 404 |
| `url` | string | one of | A jcpenney.com brand page URL (`https://www.jcpenney.com/g/brands/nike?id=cat11100023787`). A curated brand page's assortment can differ slightly from the brand name listing |

### Deals (`/deals`)

Any search parameter except `query`, `exact` and `deal`, plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `clearance` | `clearance`, `sale`, `black_friday`, `big_buy`, `limited_time_special`, `best_value`, `gotta_have_it`, `closeout` or `bogo` (every Buy 1 Get 1 offer) |
| `label` | string | none | Any Deals & Promotions label verbatim from a previous answer's `s1_deals_and_promotions` facet (`"BUY 1 GET 1 50% OFF"`), instead of `type` |
| `department` | string | all products | Limit the deal to one department or category id (`dept20000011`, `cat100210008`), from breadcrumbs or a category URL |

### Product (`/product`)

Pass one of `product_id`, `url` or `product_ids`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | A JCPenney product id (`ppr` / `ppm` / `pp` + digits): a listing item's `id`, the last part of a product URL (`"ppr5008604049"`) |
| `url` | string | one of | A jcpenney.com product URL ending in its product id |
| `product_ids` | array | one of | Up to 20 product ids in one call (still 1 credit). Unknown ids are listed in `not_found`. Batch results carry no online stock |

### Stores (`/stores`)

Pass one of `zip`, `city` + `state`, or `lat` + `lng`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string or integer | one of | US or Puerto Rico ZIP code (`75024` or `75024-1234`) |
| `city`, `state` | string | one of | A US city and its 2-letter state code (`Austin`, `TX`), both required together |
| `lat`, `lng` | number | one of | A point, both required together |
| `radius` | integer | 25 | Radius in miles, 1-100 |
| `page` | integer | 1 | Results page, 1-based (1-50) |
| `page_size` | integer | 10 | Stores per page, 1-20 |

### Store availability (`/store-availability`)

Pass `sku` and one of `zip` or `lat` + `lng` (no city).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | required | A JCPenney SKU id (8-16 digits): a product's `variants[].sku` (`"84630160042"`), or a listing item's `sku_id` / `colors[].sku_id`. A product id is not a SKU |
| `zip` | string or integer | one of | US or Puerto Rico ZIP code: the 5 nearest stores are checked |
| `lat`, `lng` | number | one of | A point, both required together |
| `radius` | integer | 25 | Search radius in miles, 1-100 |
| `in_stock_only` | boolean | `false` | Drop the stores (of the 5 nearest) that have none |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

### Coupons (`/coupons`)

No parameters: send `{}`.

## Examples

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "ppr5008604049"}'
```

Captured `data` (3 of 14 features, 2 of 8 images and 279 of 281 variants trimmed):

```json
{
  "id": "ppr5008604049",
  "title": "St. John's Bay Womens Mid Rise Straight Leg Jean",
  "brand": "St. John's Bay",
  "url": "https://www.jcpenney.com/p/st-johns-bay-womens-mid-rise-straight-leg-jean/ppr5008604049",
  "description": "St. John’s Bay womens Mid Rise Straight Leg Jean delivers everyday comfort with its classic cut and soft denim feel. The mid-rise waist and straight leg create a flattering silhouette that pairs effortlessly with any top. Style with sneakers or loafers for an easy, timeless look.",
  "features": ["Features: Essentials", "Closure Type: Button & Zipper", "Concerns: Tummy Solutions"],
  "category": { "id": "cat100250096", "name": "jeans" },
  "breadcrumbs": [{ "id": "dept20000013", "name": "women" }, { "id": "cat100250096", "name": "jeans" }],
  "product_type": "Jeans",
  "item_type": "Straight Leg Jeans",
  "images": ["https://sc-images.jcpenney.com/JCPenney/DP1124202509032184M", "https://sc-images.jcpenney.com/JCPenney/DP1124202509032079M"],
  "image": "https://sc-images.jcpenney.com/JCPenney/DP1124202509032184M",
  "rating": 4.06,
  "review_count": 161,
  "question_count": 27,
  "answer_count": 19,
  "price": {
    "current_min": 19.99,
    "current_max": 19.99,
    "regular_min": 48,
    "regular_max": 48,
    "sale_min": 19.99,
    "sale_max": 19.99,
    "clearance_min": null,
    "clearance_max": null,
    "percent_off": 58,
    "percent_off_min": 58,
    "price_type": "sale",
    "deal_label": "GOTTA HAVE IT PRICE!",
    "coupon": { "code": "2HONOR", "price_min": 15.99, "price_max": 15.99 },
    "starts_at": "2026-11-10T06:00:00.000Z",
    "ends_at": "2026-11-11T05:59:59.000Z",
    "currency": "USD"
  },
  "online_stock_checked": true,
  "variant_count": 281,
  "variants": [
    {
      "sku": "84630160042",
      "upc": "198272041828",
      "color": "Rinse",
      "size": "6",
      "options": { "size_range": "misses", "size": "6", "color": "Rinse" },
      "lot_id": "8463016",
      "status": "Available",
      "online_stock": "high",
      "max_quantity": 8
    },
    {
      "sku": "84603150117",
      "upc": "198272047370",
      "color": "Dk Formation",
      "size": "20",
      "options": { "size_range": "misses", "size": "20", "color": "Dk Formation" },
      "lot_id": "8460315",
      "status": "AvailableLow",
      "online_stock": "low",
      "max_quantity": 8
    }
  ],
  "is_marketplace": false,
  "channel": "Omnichannel",
  "in_store_pickup": true,
  "can_add_to_cart": true,
  "currency": "USD"
}
```

`price` on `/product` is a block of product-level ranges, not a number: JCPenney does not expose a price per size or per color, so every one of the 281 variants shares the $19.99 sale price and none carries a price of its own. `percent_off` (58) compares the sale price with the $48 regular price. `price.coupon` is the price after today's coupon: $15.99 with `2HONOR`. `starts_at` / `ends_at` bound the price window (this "GOTTA HAVE IT PRICE!" ran one day). `online_stock` is a level (`high`, `low`, `out`), not a count: in this answer 252 variants were `high`, 19 `low` and 10 `out`; `status` is the site's own (`Available`, `AvailableLow`, `NotAvailable`). `rating` (4.06) and `review_count` (161) are all the API gives about reviews: review text is not available. Pass `variants[0].sku` (`"84630160042"`) to `/store-availability`.

With `product_ids` (up to 20) the answer is `{count, products[], not_found[]}`, each product in the same shape with `online_stock` null and `online_stock_checked: false`.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jeans"}'
```

Captured `data` for `{"query": "jeans"}` (47 of 48 items, 5 of 7 colors of the first item, 12 of 14 facets and most facet values trimmed):

```json
{
  "query": "jeans",
  "corrected_query": null,
  "redirected_to": null,
  "total": 1135,
  "page": 1,
  "total_pages": 24,
  "per_page": 48,
  "max_pages": 25,
  "sort": "relevance",
  "count": 48,
  "items": [
    {
      "id": "ppr5008604049",
      "title": "St. John's Bay Womens Mid Rise Straight Leg Jean",
      "brand": "St. John's Bay",
      "url": "https://www.jcpenney.com/p/st-johns-bay-womens-mid-rise-straight-leg-jean/ppr5008604049",
      "image": "https://sc-images.jcpenney.com/JCPenney/DP1124202509032184M",
      "sku_id": "84603150026",
      "price": 19.99,
      "price_max": null,
      "regular_price": 48,
      "regular_price_max": null,
      "price_type": "sale",
      "percent_off": 58,
      "price_in_cart": false,
      "deal_label": "GOTTA HAVE IT PRICE!",
      "coupon_price": 15.99,
      "coupon_price_max": 15.99,
      "coupon_code": "2HONOR",
      "rating": 4.06,
      "review_count": 160,
      "badge": "Only at JCP",
      "availability_label": ["FREE Same Day Pickup", "Available for Shipping"],
      "colors": [{ "name": "Dk Formation", "sku_id": "84603150026" }, { "name": "Rinse", "sku_id": "84630160026" }],
      "is_marketplace": false,
      "seller": null,
      "currency": "USD"
    }
  ],
  "applied_filters": [{ "facet": "product_type", "label": "Category", "value": "jeans", "value_label": "jeans" }],
  "facets": [
    {
      "id": "brand",
      "label": "Brand",
      "values": [
        { "label": "Levi's", "value": "levi's", "count": 137, "selected": false },
        { "label": "A.N.A", "value": "a.n.a", "count": 80, "selected": false }
      ]
    },
    {
      "id": "s1_deals_and_promotions",
      "label": "Deals & Promotions",
      "values": [
        { "label": "SALE", "value": "SALE", "count": 525, "selected": false },
        { "label": "CLEARANCE", "value": "CLEARANCE", "count": 150, "selected": false }
      ]
    }
  ],
  "currency": "USD"
}
```

JCPenney put `jeans` in the Jeans category on its own (`applied_filters` shows `product_type: jeans`); send `"exact": true` to search the word across every category. `total_pages` is 24 because 1,135 items fill 24 pages of 48. `coupon_price` ($15.99) is the $19.99 price after today's `2HONOR` coupon. The other facets on this answer were `store_availability`, `product_type`, `item_type`, `gender`, `color`, `size_range`, `product_size` (465 values), `waist`, `rise`, `features`, `average_rating` and `s1_price_range`; any `facets[].id` with one of its `values[].value` works in `filters`. A keyword the site sends to a deal or category listing (`doorbusters`) comes back with `redirected_to` set to that listing's path and that listing's items.

### Deals (clearance)

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "clearance"}'
```

Captured `data` (47 of 48 items, 2 of 4 colors and the 10 facets trimmed):

```json
{
  "type": "clearance",
  "labels": ["CLEARANCE"],
  "department": null,
  "total": 7662,
  "page": 1,
  "total_pages": 25,
  "per_page": 48,
  "max_pages": 25,
  "sort": "relevance",
  "count": 48,
  "items": [
    {
      "id": "ppr5008660235",
      "title": "Liz Claiborne Womens Crew Neck Short Sleeve Blouse",
      "brand": "Liz Claiborne",
      "url": "https://www.jcpenney.com/p/liz-claiborne-womens-crew-neck-short-sleeve-blouse/ppr5008660235",
      "image": "https://sc-images.jcpenney.com/JCPenney/DP0119202617023549M",
      "sku_id": "81401690034",
      "price": 13.19,
      "price_max": 17.59,
      "regular_price": 44,
      "regular_price_max": null,
      "price_type": "clearance",
      "percent_off": 70,
      "price_in_cart": false,
      "deal_label": null,
      "coupon_price": 11.87,
      "coupon_price_max": 15.83,
      "coupon_code": "2HONOR",
      "rating": 3.8,
      "review_count": 5,
      "badge": "Few Left",
      "availability_label": ["Unavailable for Pickup", "Available for Shipping"],
      "colors": [{ "name": "Black", "sku_id": "81401690232" }, { "name": "Peach Whip", "sku_id": "81401690034" }],
      "is_marketplace": false,
      "seller": null,
      "currency": "USD"
    }
  ],
  "applied_filters": [{ "facet": "s1_deals_and_promotions", "label": "Deals & Promotions", "value": "CLEARANCE", "value_label": "CLEARANCE" }],
  "currency": "USD"
}
```

The blouse is on clearance from $13.19 to $17.59 by color and size (70% off the $44 regular price at the low end), and $11.87 to $15.83 after today's coupon: quote a range as a range. The clearance list had 7,662 items, more than the 1,200 that 25 pages reach: split it with `brand`, `department`, `size` or `price_range` to cover it all.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/g/women/dresses?id=cat100210008"}'
```

The captured answer opens with (then the same `items[]`, `applied_filters` and `facets[]` as search, 11 facets here including `dress_type`, `dress_length` and `occasion`):

```json
{
  "category": {
    "name": "dresses",
    "id": "cat100210008",
    "path": "/g/women/dresses?id=cat100210008",
    "url": "https://www.jcpenney.com/g/women/dresses?id=cat100210008",
    "breadcrumbs": [
      { "name": "women", "id": "dept20000013", "path": "/d/women" },
      { "name": "dresses", "id": "cat100210008", "path": "/g/women/dresses?id=cat100210008" }
    ]
  },
  "total": 3979,
  "page": 1,
  "total_pages": 25,
  "per_page": 48,
  "max_pages": 25,
  "sort": "relevance",
  "count": 48
}
```

The `women` breadcrumb is a department (`dept20000013`, path `/d/women`): a department page lists no products by itself, so `/category` answers 400 for it unless a deal or another filter is added. Pick one of its categories (`/g/...?id=cat...`) instead.

### Brand

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/brand \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "Nike"}'
```

The captured answer opens with (then the same `items[]` and `facets[]` as search):

```json
{
  "brand": { "name": "Nike", "value": "nike", "url": "https://www.jcpenney.com/g/shops/shop-all-products?brand=nike&id=cat1007450013" },
  "total": 1247,
  "page": 1,
  "total_pages": 25,
  "per_page": 48,
  "max_pages": 25,
  "sort": "relevance",
  "count": 48,
  "applied_filters": [{ "facet": "brand", "label": "Brand", "value": "nike", "value_label": "Nike" }]
}
```

### Store availability

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "84630160042", "zip": "90012"}'
```

Captured `data` (3 of 5 stores trimmed):

```json
{
  "sku": "84630160042",
  "location": { "zip": "90012" },
  "radius": 25,
  "in_stock_only": false,
  "count": 5,
  "stores_with_stock": 5,
  "total_quantity": 34,
  "stores": [
    {
      "store_id": "0699",
      "name": "Glendale Galleria",
      "address": "1169 Glendale Galleria",
      "city": "Glendale",
      "state": "CA",
      "zip": "91210",
      "phone": "818-240-8700",
      "lat": 34.144416,
      "lng": -118.2595761,
      "distance_miles": 5.5,
      "hours": [{ "day": "Mon-Sat", "open": "10:00am", "close": "9:00pm" }, { "day": "Sun", "open": "11:00am", "close": "7:00pm" }],
      "quantity": 9,
      "status": "in_stock",
      "stocked": true,
      "updated_at": "2026-11-10T17:36:50Z"
    },
    {
      "store_id": "0955",
      "name": "Gage & Pacific Store",
      "address": "6420 S Pacific Blvd",
      "city": "Huntington Park",
      "state": "CA",
      "zip": "90255",
      "phone": "323-587-3261",
      "lat": 33.98106,
      "lng": -118.22498,
      "distance_miles": 5.9,
      "hours": [
        { "day": "Mon-Thu", "open": "10:00am", "close": "7:00pm" },
        { "day": "Fri-Sat", "open": "10:00am", "close": "9:00pm" },
        { "day": "Sun", "open": "11:00am", "close": "7:00pm" }
      ],
      "quantity": 3,
      "status": "in_stock",
      "stocked": true,
      "updated_at": "2026-11-10T17:36:50Z"
    }
  ]
}
```

The answer always covers the 5 nearest stores, nearest first; there is no way to ask for more. `quantity` is the store's unit count for that SKU (9, 3, 7, 6 and 9 here, 34 in all), `updated_at` is when JCPenney last refreshed it. `status` is `low` when JCPenney flags the store as low on it, `out_of_stock` at 0 units, and `not_stocked` when the store does not carry the SKU at all. Stock changes through the day: give the `fetched_at` time with any count.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "75024"}'
```

Captured `data` (5 of 6 stores trimmed):

```json
{
  "location": { "zip": "75024" },
  "radius": 25,
  "total": 6,
  "page": 1,
  "total_pages": 1,
  "count": 6,
  "stores": [
    {
      "store_id": "2795",
      "name": "Stonebriar Mall",
      "address": "2607 Preston Rd",
      "city": "Frisco",
      "state": "TX",
      "zip": "75034",
      "phone": "972-712-2707",
      "lat": 33.09948,
      "lng": -96.80954,
      "distance_miles": 1.4,
      "country": "USA",
      "hours": [
        { "day": "Monday", "open": "10:00", "close": "20:00" },
        { "day": "Tuesday", "open": "10:00", "close": "20:00" },
        { "day": "Wednesday", "open": "10:00", "close": "20:00" },
        { "day": "Thursday", "open": "10:00", "close": "20:00" },
        { "day": "Friday", "open": "10:00", "close": "21:00" },
        { "day": "Saturday", "open": "10:00", "close": "21:00" },
        { "day": "Sunday", "open": "11:00", "close": "19:00" }
      ],
      "timezone": "America/Chicago",
      "services": ["Curbside Pickup", "jewelry", "In-Home Custom Window", "Mattresses", "JCPenney Beauty", "portrait studio", "salon"],
      "curbside": { "available": true, "directions": "Park in designated area on 2nd floor by Mens Apparel entrance." },
      "in_store_pickup": { "available": true, "directions": "See an associate in the MENS DEPARTMENT on the 2nd Floor" },
      "appointments": ["Sephora", "salon"],
      "store_url": "https://stores.jcpenney.com/tx/frisco/clothing-stores-frisco-tx-2795.html"
    }
  ]
}
```

Hours here are 24-hour `HH:MM` per weekday with the store's `timezone`; store availability lists hours as the site prints them (`"Mon-Sat"`, `"10:00am"`). Puerto Rico stores are included.

### Coupons

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/coupons \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (5 of 7 coupons trimmed, disclaimers shortened):

```json
{
  "count": 7,
  "codes": 2,
  "coupons": [
    {
      "code": "2HONOR",
      "channel": "online",
      "headline": "BIGGEST SALE OF THE SEASON! - EXTRA 20% OFF ANY OTHER WAY YOU PAY",
      "details": "select apparel, shoes, accessories",
      "offers": [
        {
          "headline": "BIGGEST SALE OF THE SEASON! - EXTRA 20% OFF ANY OTHER WAY YOU PAY",
          "details": "select apparel, shoes, accessories"
        },
        {
          "headline": "EXTRA 30% OFF WITH YOUR JCPENNEY CREDIT CARD OR JCPENNEY MASTERCARD",
          "details": "select apparel, shoes, accessories"
        },
        { "headline": "EXTRA 30% OFF ANY WAY YOU PAY", "details": "select bedding, bath, curtains" }
      ],
      "starts_at": "2026-11-05T00:00:00-06:00",
      "ends_at": "2026-11-11T23:59:59-06:00",
      "disclaimer": "*Extra 30% off select original, regular and sale-priced bedding, bath and curtain purchase any way you pay. Extra 30% off select original, regular and ...",
      "url": "https://www.jcpenney.com/g/shops/shop-all-products?s1_deals_and_promotions=SALE&id=cat1007450013"
    },
    {
      "code": null,
      "channel": "in store",
      "headline": "JCPenney Salon - 20% OFF $30 OR MORE select salon services new clients only",
      "details": null,
      "offers": [{ "headline": "JCPenney Salon - 20% OFF $30 OR MORE select salon services new clients only", "details": null }],
      "starts_at": "2026-11-01T00:00:00-05:00",
      "ends_at": "2026-11-30T23:59:59-06:00",
      "disclaimer": "*20% off any salon service of $30 or more at JCPenney Salon, excluding taxes, valid 11/1/26-11/30/26. New clients only. Offer may not be available at all ...",
      "url": "https://www.jcpenney.com/findastore"
    }
  ]
}
```

7 coupons, 2 of them with a code (`codes`). In-store offers come with `code: null`. These are the public coupons on JCPenney's coupons page with the offer text and disclaimer as JCPenney states them; account-specific offers and JCPenney Rewards balances are not covered.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/jcpenney/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jea"}'
```

Captured `data` (9 of 13 suggestions trimmed):

```json
{
  "query": "jea",
  "count": 13,
  "suggestions": [
    { "term": "jeans womens", "url": "https://www.jcpenney.com/s?searchTerm=jeans%20womens", "departments": [] },
    { "term": "jeans ana", "url": "https://www.jcpenney.com/s?searchTerm=jeans%20ana", "departments": [] },
    { "term": "jeans", "url": "https://www.jcpenney.com/s?searchTerm=jeans", "departments": [] },
    { "term": "jeans girls", "url": "https://www.jcpenney.com/s?searchTerm=jeans%20girls", "departments": [] }
  ]
}
```

`departments[]` holds `{name, url}` refinements where JCPenney offers them for a term; it was empty for every `jea` completion.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def jcpenney(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/jcpenney/{endpoint}", headers=HEADERS, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["data"]

# 1. Clearance for one brand, with today's coupon price (1 credit per page)
page = jcpenney("deals", {"type": "clearance", "brand": "st. john's bay"})
for p in page["items"][:5]:
    print(p["id"], p["title"], p["price"], "was", p["regular_price"], p["percent_off"], "after coupon", p["coupon_price"], p["coupon_code"])

# 2. One product, then unit counts at the 5 nearest stores (2 calls, 1 credit each)
item = jcpenney("product", {"product_id": "ppr5008604049"})
v = item["variants"][0]
near = jcpenney("store-availability", {"sku": v["sku"], "zip": "90012"})
for s in near["stores"]:
    print(s["name"], s["distance_miles"], "mi", s["quantity"], "units", s["status"])

# 3. Price check for up to 20 products in one call (1 credit)
batch = jcpenney("product", {"product_ids": ["ppr5008604049", "ppr5008660235"]})
for p in batch["products"]:
    print(p["id"], p["price"]["current_min"], p["price"]["price_type"], p["price"]["coupon"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when the answer was produced.

- **listing item** (search, category, brand, deals) - `id`, `title`, `brand`, `url`, `image`, `sku_id`, `price`, `price_max`, `regular_price`, `regular_price_max`, `price_type` (`sale`, `clearance`, `original`), `percent_off`, `price_in_cart`, `deal_label`, `coupon_price`, `coupon_price_max`, `coupon_code`, `rating`, `review_count`, `badge`, `availability_label[]`, `colors[]` {`name`, `sku_id`}, `is_marketplace`, `seller` ({`name`, `id`} or null), `currency`.
- **grid** (all four listings) - `total`, `page`, `total_pages`, `per_page` (48), `max_pages` (25), `sort`, `count`, `items[]`, `applied_filters[]` {`facet`, `label`, `value`, `value_label`}, `facets[]` {`id`, `label`, `values[]` {`label`, `value`, `count`, `selected`}}, `currency`.
- **search** - `query`, `corrected_query` (the site's autocorrect message, or null), `redirected_to` (the listing path the keyword was sent to, or null) and the grid.
- **category** - `category` {`name`, `id`, `path`, `url`, `breadcrumbs[]` {`name`, `id`, `path`}} and the grid.
- **brand** - `brand` {`name`, `value`, `url`} and the grid.
- **deals** - `type`, `labels[]`, `department` and the grid.
- **product** - `id`, `title`, `brand`, `url`, `description`, `features[]`, `category` {`id`, `name`}, `breadcrumbs[]` {`id`, `name`}, `product_type`, `item_type`, `images[]`, `image`, `rating`, `review_count`, `question_count`, `answer_count`, `price` {`current_min`, `current_max`, `regular_min`, `regular_max`, `sale_min`, `sale_max`, `clearance_min`, `clearance_max`, `percent_off`, `percent_off_min`, `price_type`, `deal_label`, `coupon` ({`code`, `price_min`, `price_max`} or null), `starts_at`, `ends_at`, `currency`}, `online_stock_checked`, `variant_count`, `variants[]` {`sku`, `upc`, `color`, `size`, `options`, `lot_id`, `status`, `online_stock`, `max_quantity`}, `is_marketplace`, `channel`, `in_store_pickup`, `can_add_to_cart`, `currency`. With `product_ids`: `count`, `products[]`, `not_found[]`.
- **stores** - `location` ({`zip`}, {`city`, `state`} or {`lat`, `lng`}), `radius`, `total`, `page`, `total_pages`, `count`, `stores[]` {`store_id`, `name`, `address`, `city`, `state`, `zip`, `phone`, `lat`, `lng`, `distance_miles`, `country`, `hours[]` {`day`, `open`, `close`}, `timezone`, `services[]`, `curbside` {`available`, `directions`}, `in_store_pickup` {`available`, `directions`}, `appointments[]`, `store_url`}.
- **store-availability** - `sku`, `location`, `radius`, `in_stock_only`, `count`, `stores_with_stock`, `total_quantity`, `stores[]` {`store_id`, `name`, `address`, `city`, `state`, `zip`, `phone`, `lat`, `lng`, `distance_miles`, `hours[]` {`day`, `open`, `close`}, `quantity`, `status`, `stocked`, `updated_at`}.
- **suggestions** - `query`, `count`, `suggestions[]` {`term`, `url`, `departments[]` {`name`, `url`}}.
- **coupons** - `count`, `codes`, `coupons[]` {`code`, `channel`, `headline`, `details`, `offers[]` {`headline`, `details`}, `starts_at`, `ends_at`, `disclaimer`, `url`}.

## Guardrails

- Prices are US dollars (`currency: "USD"`): `19.99` is $19.99. This is jcpenney.com (US, Puerto Rico stores included) only; there is no international site.
- Prices are product-level. On a listing, `price` is the low end of the current price and `price_max` the high end when the item sells at a range; on `/product`, `price` is a block of min / max ranges. JCPenney does not expose a price per size or per color, so never quote a variant's own price: quote the product's range.
- `percent_off` compares the low end of the current price with the low end of JCPenney's regular price, so on a range item it is not every variant's discount. JCPenney's terms say pricing errors occur and cart prices can differ; report the regular price as JCPenney's regular price, not as proof of a past selling price.
- `price_in_cart: true` means JCPenney shows the price only in the cart: the price fields and `coupon_price` are null. Say so; never guess the cart price.
- `coupon_price` (and `price.coupon` on `/product`) is the price after today's coupon in `coupon_code`, as JCPenney computes it. This API does not apply it at checkout, codes have end dates (see `/coupons`), and JCPenney's terms say its coupon codes do not apply to marketplace products unless stated.
- Marketplace items: `is_marketplace: true` marks a third-party seller's product (its id usually starts `ppm`), with `seller` when the listing names one. There is no sponsored-item flag: the grid carries none.
- Reviews: `rating` and `review_count` (and `question_count`, `answer_count` on `/product`) only. Review text is not available from any endpoint, so never summarize or quote what reviewers say.
- Filters: `filters` keys are `facets[].id` and values are `facets[].values[].value` from a previous answer. Price is a bucket from the `s1_price_range` facet; there is no free `min_price` / `max_price`. A filter that matches nothing returns a 200 with `total: 0`; check `total` and the `selected` flags before claiming a list is filtered. At most 10 facets and 40 values per call.
- Depth: 48 items per page, at most 25 pages (1,200 items) per query, whatever `total` says. Split a larger list with filters (brand, size, price range, department) rather than paging further; a page past the last one returns an empty `items` list.
- The `price_low_to_high` and `price_high_to_low` sorts are JCPenney's own and loose: sort the items by `price` yourself when you need a strict order.
- `corrected_query` set means the site autocorrected the keyword: say so. `redirected_to` set means the site sent the keyword to a listing (`doorbusters` goes to a deal listing) and the items are that listing's; when it sends a keyword to a page with no product grid, the answer has `total: 0` and that `redirected_to`.
- `/category` needs a `/g/` path or URL with its `id=cat...` part; a department (`dept...`, `/d/` pages) lists no products unless a deal or another filter is added. Deal types that are seasonal (`black_friday`) list nothing once the event ends.
- Store stock: `/store-availability` takes a variant `sku`, never a product id, and always covers the 5 nearest stores. `quantity` is a real unit count per store; `online_stock` on `/product` is a level (`high`, `low`, `out`), never a count, and is online stock, not store stock. Give the `fetched_at` time with any count.
- There is no price history. To track clearance or prices, poll the listings or `/product` (up to 20 ids per call) on a schedule and store the results yourself.
- Coupons: `/coupons` returns the public coupons on JCPenney's coupons page only. Report codes with their headline, details and `ends_at`; do not promise a code works on a given item beyond what `coupon_code` says. JCPenney Rewards balances, account offers and credit-card offers tied to an account are not covered.
- JCPenney publishes no public developer API: vendors and marketplace sellers connect through EDI and integration partners, and publishers can join its affiliate program, none of which offers a public endpoint for searching the catalog, reading prices or checking store stock. This API reads public product data for research, price monitoring and stock alerts. It does not add to cart, check out or reserve stock; do not present it as a purchasing bot.
- Never fabricate prices, sale or clearance status, coupon codes, stock, unit counts or ratings. Only return what the API returned, with the product `url` or `id`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`; `page` outside 1-25; an unknown `sort` or deal `type`; both `type` and `label`; a `filters` value that is not an object of facet id to value(s), a facet name that is not a `facets[].id`, more than 10 facets or more than 20 values for one; a `brand` filter on `/brand` or a `deal` filter on `/deals`; both `path` and `url`, or both `brand` and `url`; a category path that is not `/g/...?id=cat...`; a department page with no filter; a `department` that is not a `dept...` / `cat...` id; a `product_id` that is not `ppr` / `ppm` / `pp` + digits; a product `url` without its id; more than 20 `product_ids`, or `product_ids` with `product_id` / `url`; `product_id` and `url` naming different products; a `sku` that is not 8-16 digits; a ZIP that is not 5 digits; more than one location; `city` without `state` or `lat` without `lng`; `city` on store availability; a `radius` outside 1-100; a `page_size` outside 1-20).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product (none of the `product_ids` either), no such brand, no products under that category, or no such SKU. Not charged. Re-run the search for a fresh `id`, or use a brand as the `Brand` facet of a search lists it. `/stores` with no store in range answers 200 with `count: 0`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data).
- `502` or `503` means JCPenney is temporarily unavailable or returned an unusable page. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.

## SDKs

```bash
pip install scavio==0.45.0
npm install scavio@0.46.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.jcpenney.search({ query: "jeans", size: "8", deal: "SALE" });
const { data: item } = await scavio.jcpenney.product({ product_id: found.items[0].id });
const { data: near } = await scavio.jcpenney.storeAvailability({ sku: item.variants[0].sku, zip: "90012" });
const { data: next } = await scavio.jcpenney.search({ query: "jeans", page: 2 });
const { data: clearance } = await scavio.jcpenney.deals({ type: "clearance", brand: "st. john's bay" });
const { data: dresses } = await scavio.jcpenney.category({ path: "/g/women/dresses?id=cat100210008" });
const { data: brand } = await scavio.jcpenney.brand({ brand: "Nike" });
const { data: batch } = await scavio.jcpenney.product({ product_ids: ["ppr5008604049", "ppr5008660235"] });
const { data: stores } = await scavio.jcpenney.stores({ zip: "75024" });
const { data: ideas } = await scavio.jcpenney.suggestions({ query: "jea" });
const { data: codes } = await scavio.jcpenney.coupons();
```

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_jcpenney`, `get_jcpenney_product`, `get_jcpenney_category`, `get_jcpenney_brand`, `get_jcpenney_deals`, `get_jcpenney_stores`, `get_jcpenney_store_availability`, `get_jcpenney_suggestions` and `get_jcpenney_coupons`. JCPenney is opt-in: add `jcpenney` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.43.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,jcpenney"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/jcpenney-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [product](https://scavio.dev/docs/jcpenney-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [category](https://scavio.dev/docs/jcpenney-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [brand](https://scavio.dev/docs/jcpenney-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [deals](https://scavio.dev/docs/jcpenney-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [stores](https://scavio.dev/docs/jcpenney-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [store availability](https://scavio.dev/docs/jcpenney-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [suggestions](https://scavio.dev/docs/jcpenney-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data), [coupons](https://scavio.dev/docs/jcpenney-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data). Overview: [JCPenney API](https://scavio.dev/jcpenney-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=jcpenney-product-data).
