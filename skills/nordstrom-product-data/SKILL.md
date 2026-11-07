---
name: nordstrom-product-data
description: "Nordstrom product data API: search nordstrom.com with current price, original price, percent off, rating, review count, badges and every color, sorted by relevance, rating, price, newest or percent off, then read one product with every size and color as a SKU with UPC, price, regular, clearance or promotion price type, stock and units available to ship, plus the star histogram, size-fit distribution and the reviews shown on the page. 2 endpoints, 5 credits each."
version: 1.0.0
tags: nordstrom, nordstrom-api, nordstrom-product-data, nordstrom-scraper, fashion, apparel, shoes, designer-brands, clothing-prices, sale-tracking, price-drop-alerts, percent-off, clearance, sku-data, upc, size-fit, product-search, product-data, product-reviews, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
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

# Nordstrom Product Data API - Search, Prices, SKU Stock, Reviews

Search Nordstrom (nordstrom.com, US) by keyword, 24 products per page, sorted by relevance, rating, price, newest or percent off: current price and price range, original price range, percent off and on-sale flag, rating, review count, badges such as `new` or `new_markdown`, a low-inventory flag, the marketplace seller when Nordstrom is not the seller, and every color with its color family and image. Read one product by URL or style id with its description, feature bullets, fit notes, final-sale flag, current, original and clearance price ranges, the star histogram, the size-fit distribution, breadcrumbs and images, and every color and size as a SKU with SKU id, UPC, price, original price, percent off, price type, in-stock flag and the quantity available to ship. The reviews the product page shows come back on the same call. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find clothing, shoes, bags or beauty at Nordstrom by keyword, and compare prices, ratings and brands
- Track Nordstrom prices or price drops on a product, or list what is on sale (sort by `percent_off`)
- Check which sizes and colors of a Nordstrom product are in stock, and how many units are available online
- Get the UPC, SKU id, regular price and clearance price for every size and color of a style
- Read what Nordstrom reviewers say about fit (runs small, true to size, runs big) and quality
- Monitor a fashion brand's pricing and markdowns at Nordstrom (MAP monitoring, resale pricing)
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
3. A new account starts with 50 credits. Every endpoint in this skill costs 5 credits, so the free credits cover 10 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Nordstrom endpoints cost **5 credits**. Expect 3-7 seconds per call.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/nordstrom/search` | 5 | 24 products per page: position, style id, URL, name, brand, image, current price and price range, original price range, percent off, on-sale flag, rating, review count, badges, low-inventory flag, marketplace flag and seller, and every color with its color family and image. Plus the total result count, page count and the sorts the site offers |
| `POST /api/v1/nordstrom/product` | 5 | One product by URL or style id: name, brand, brand URL, description, feature bullets, fit notes, final-sale and in-stock flags, current, original and clearance price ranges, percent off, marketplace seller, rating, review count, star histogram, size-fit distribution, AI review summary and the most praised and criticized features when the site shows them, breadcrumbs, images, and every color with its images and every size as a SKU (SKU id, size, size type, UPC, price, original price, percent off, price type, in stock, quantity, final sale). Also the reviews the page shows (10-13), each with title, text, rating, size rating, author, date, helpful votes, verified-purchase flag, size and color purchased, and photos |

## Workflow

1. **Find products:** call `/nordstrom/search` with `query`. Each row has a `url` and a `style_id`.
2. **One product in full:** call `/nordstrom/product` with the row's `url` or `style_id`.
3. **Sizes, colors and stock:** read `colors[].skus[]` on the product answer. Each size of each color has its own `price`, `original_price`, `price_type`, `in_stock` and `quantity`.
4. **Sales and markdowns:** search with `sort: "percent_off"` for the deepest discounts first, or read `percent_off`, `on_sale` and `badges` (`new_markdown`) on any row. On a product, `price_type: "clearance"` marks the clearance SKUs.
5. **Fit and reviews:** read `size_fit`, `rating_histogram` and `reviews[]` on the same product answer. There is no separate review endpoint and no deeper review paging.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-100). 24 products per page |
| `sort` | string | `relevance` | `relevance`, `rating`, `price_high`, `price_low`, `newest` or `percent_off` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | nordstrom.com product URL, the `url` of a search result: `https://www.nordstrom.com/s/<slug>/<style id>` |
| `style_id` | string | one of | Nordstrom style id, the number at the end of a product URL (the `style_id` of a search result). Used when `url` is not given |

## Examples

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

A marketplace row from the same search carries `"is_marketplace": true` and `"seller": "Mac Duggal"`.

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

# 1. Deepest discounts first (5 credits)
found = nordstrom("search", {"query": "dress", "sort": "percent_off"})
for p in found["products"][:5]:
    print(p["brand"], p["name"], p["price"], "was", p["original_price_range"], f'{p["percent_off"]}% off')

# 2. One product: every size and color, clearance SKUs and units to ship (5 credits)
item = nordstrom("product", {"url": found["products"][0]["url"]})
for color in item["colors"]:
    for s in color["skus"]:
        print(color["name"], s["size"], s["upc"], s["price"], s["price_type"], "in stock" if s["in_stock"] else "out", s["quantity"])

# 3. Fit from the same answer
if item["size_fit"]:
    for d in item["size_fit"]["distribution"]:
        print(d["label"], d["count"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Nordstrom answered.

- **search** - `query`, `page`, `sort`, `total_results`, `page_count`, `count`, `available_sorts[]`, `products[]` (`position`, `style_id`, `url`, `name`, `brand`, `image`, `price`, `price_range` {`min`, `max`}, `original_price_range` {`min`, `max`}, `percent_off`, `on_sale`, `rating`, `review_count`, `badges[]`, `low_inventory`, `is_marketplace`, `seller`, `colors[]` {`name`, `color_family`, `image`}).
- **product** - `style_id`, `url`, `name`, `brand`, `brand_url`, `description`, `features[]`, `fit_info[]`, `is_final_sale`, `in_stock`, `price`, `price_range`, `original_price_range`, `percent_off`, `on_sale`, `clearance_price_range`, `is_marketplace`, `seller`, `rating`, `review_count`, `rating_histogram[]` {`rating`, `count`}, `size_fit` {`average`, `distribution[]` {`value`, `label`, `count`}} or null, `review_summary`, `best_features[]` and `worst_features[]` {`name`, `mentions`, `quote`}, `breadcrumbs[]` {`name`, `url`}, `images[]`, `color_count`, `sku_count`, `colors[]` (`name`, `color_family`, `in_stock`, `images[]`, `skus[]` {`sku_id`, `size`, `size_type`, `color`, `upc`, `price`, `original_price`, `percent_off`, `price_type`, `in_stock`, `quantity`, `is_final_sale`}), `reviews[]` (`review_id`, `title`, `text`, `rating`, `recommended`, `size_rating`, `author`, `date`, `helpful_votes`, `verified_purchase`, `size_purchased`, `color_purchased`, `photos[]`).

## Guardrails

- Prices are in US dollars: `195.3` is $195.30. This is nordstrom.com (US) only.
- `price` on a style is the low end of `price_range`, the lowest current price across its sizes and colors. `percent_off` on a style is the largest discount across them. When the range spans more than one price (as in the gown above, $195.30 to $279), quote the range or read the exact SKU's price from `/product`; never present the low end as the price of every size.
- `original_price_range` and a SKU's `original_price` are the regular price the discount is measured from. `price_type` on a SKU is `regular`, `clearance` or `promotion`; `clearance_price_range` is set only when some SKUs are on clearance.
- `quantity` is the units available to ship online for that SKU, not store stock. There is no store locator and no store-level stock; never claim a store has an item.
- `in_stock` on a color is true when any of its sizes is in stock. Read `skus[]` for the size the user wants.
- `is_marketplace: true` means a third-party seller (`seller`) sells the item through Nordstrom; say so when quoting it.
- `reviews[]` holds only the reviews the product page shows (10-13), in the page's order, not every review: `review_count` is the full total. There is no deeper review paging, so do not claim to have read all reviews. Use `rating_histogram` and `size_fit` for the whole-review picture.
- `size_rating` on a review and `size_fit.distribution[].value` run 1 (too small) to 5 (too big), 3 is true to size.
- `review_summary`, `best_features` and `worst_features` appear only when Nordstrom shows them; they are `null` or empty on many products.
- There is no category or browse endpoint; find products with search.
- Never fabricate prices, sizes, stock or reviews. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, a `page` outside 1-100, an unknown `sort`, a `url` that is not a nordstrom.com `/s/` product URL, a `style_id` that is not numeric, or neither `url` nor `style_id`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product; re-run the search for a fresh `url`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data).
- `502` or `503` means Nordstrom is temporarily unavailable or returned an unusable page. It is not charged; retry after a few seconds.

## MCP

The Scavio MCP server exposes both endpoints as tools (`search_nordstrom`, `get_nordstrom_product`). Nordstrom is opt-in: add `nordstrom` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.33.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,nordstrom"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/nordstrom-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data), [product](https://scavio.dev/docs/nordstrom-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data). Overview: [Nordstrom API](https://scavio.dev/nordstrom-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=nordstrom-product-data).
