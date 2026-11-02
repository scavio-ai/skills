---
name: chewy-product-data
description: "Chewy product data API: search chewy.com or browse a category, 36 products per page, with the one-time price, Autoship price and discount, first-Autoship price and savings cap, MAP price, rating and rating count, and read one product with the star distribution, review count, GTIN, specifications, ingredients, promotions and every size and flavor variant with its own price. 2 endpoints, 10 credits each."
version: 1.0.0
tags: chewy, chewy-api, chewy-product-data, pet-supplies, pet-food, dog-food, cat-food, autoship, pet-prices, map-price, product-search, product-data, category-listing, ratings, gtin, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/chewy-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data
---

# Chewy Product Data API - Prices, Autoship, Ratings

Search Chewy pet products by keyword, or browse any chewy.com category, 36 per page, with the one-time price, the Autoship (repeat delivery) price and discount, the first-Autoship price with its discount and savings cap, the strike-through and per-unit price, rating, rating count, stock and deal flags. Read one product with list, offer and minimum advertised (MAP) price, star distribution, review count, GTIN, specifications, ingredients and feeding details where Chewy lists them, promotions, and every size and flavor variant with its own price and stock. Both endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find dog food, cat food, treats, toys or other pet supplies on Chewy by keyword
- Check a Chewy product's price, Autoship price or first-Autoship discount
- Compare one-time vs Autoship pricing, or prices across sizes and flavors of one product
- Read a product's rating, star distribution, review count, specifications or ingredients
- List the best-selling, newest, cheapest or top-rated products in a Chewy category
- Check MAP pricing or the promotions running on a Chewy product
- Compare Chewy prices with PetSmart, Petco or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every Chewy call costs 10 credits, so the free credits cover 5 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Both Chewy endpoints cost **10 credits** per call.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/chewy/search` | 10 | 36 products per page for a keyword or a category: product id, part number, name, brand, URL, image, one-time price, offer and strike-through price, Autoship price and discount, first-Autoship price, discount and savings cap, MAP price, per-unit price, rating, rating count, in-stock, deal, new, exclusive and prescription flags, key benefits. Sponsored listings removed. A `redirect` when Chewy sends the query to a category |
| `POST /api/v1/chewy/product` | 10 | One product by id or URL: one-time, offer, list and strike-through price with savings, MAP price and whether it is enforced, Autoship and first-Autoship price, per-unit price, stock, rating, rating count, review count, star distribution, attribute scores, GTIN, description, key benefits, specifications, details (ingredients, feeding), breadcrumbs, images, promotions and every variant with its own price, Autoship price and stock |

## Workflow

Every call costs 10 credits, so plan the calls before making them and say the cost before running more than a few.

1. **Find products:** call `/chewy/search` with `query`, or with `category_id` to browse a category. Each row has a `product_id` and already carries the one-time, Autoship and first-Autoship prices, so a price comparison often needs no product call.
2. **Check for a redirect:** if `redirect` is not null, Chewy sent the query to that category page and the rows are that category's products, not a keyword match.
3. **One product in full:** call `/chewy/product` with the row's `product_id` (or a chewy.com URL) for the star distribution, review count, specifications, ingredients and every size and flavor in `variants`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keywords (1-200 chars). Pass this or `category_id`, not both |
| `category_id` | string | one of | Category to browse: the number at the end of a chewy.com `/b/` URL (`332` is Dog Food in `/b/food-332`), or that URL itself |
| `page` | integer | 1 | 1-based page (1-100), 36 results per page |
| `sort` | string | `relevance` | `relevance`, `bestselling`, `newest`, `price_low`, `price_high`, `rating` or `most_reviewed` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | Chewy product id: the number after `/dp/` in the product URL, or a search row's `product_id` (`"128666"`) |
| `url` | string | one of | A chewy.com product URL, `https://www.chewy.com/<name>/dp/<id>` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/chewy/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "128666"}'
```

Captured response (Purina Pro Plan dry dog food, 30-lb bag; description, specifications, details, images and 15 of 17 variants trimmed):

```json
{
  "data": {
    "product_id": "128666",
    "part_number": "101143",
    "name": "Purina Pro Plan Adult Sensitive Skin & Stomach Salmon & Rice Formula Dry Dog Food, 30-lb bag",
    "brand": "Purina Pro Plan",
    "url": "https://www.chewy.com/purina-pro-plan-adult-sensitive-skin/dp/128666",
    "gtin": "038100175526",
    "price": 77.48,
    "offer_price": 77.48,
    "list_price": 79.99,
    "strike_price": 79.99,
    "strike_price_type": "LIST",
    "strike_savings": 2.51,
    "strike_savings_pct": 3,
    "map_price": 77.48,
    "map_enforced": false,
    "autoship_allowed": true,
    "autoship_price": 73.61,
    "autoship_discount_pct": 5,
    "first_autoship_price": 57.48,
    "first_autoship_discount_pct": 35,
    "first_autoship_max_savings": 20,
    "price_per_unit": 2.59,
    "price_per_unit_unit": "lb",
    "number_of_units": 30,
    "in_stock": true,
    "shipping_message": "FREE 1-3 day delivery",
    "rating": 4.5069,
    "rating_count": 23729,
    "review_count": 9945,
    "rating_distribution": [
      { "stars": 1, "count": 1655, "percent": 6.9746 },
      { "stars": 2, "count": 606, "percent": 2.5538 },
      { "stars": 3, "count": 790, "percent": 3.3293 },
      { "stars": 4, "count": 1682, "percent": 7.0884 },
      { "stars": 5, "count": 18996, "percent": 80.0539 }
    ],
    "attribute_scores": { "Digestibility": 82, "Ingredient Quality": 84, "Nutritional Content": 83, "Palatability": 81 },
    "attributes": { "Flavor": "Salmon & Rice", "Size": "30-lb bag" },
    "variant_options": [
      { "name": "Flavor", "values": ["Lamb & Oat Meal", "Salmon & Rice", "Turkey & Oat Meal"] },
      { "name": "Size", "values": ["4-lb bag", "16-lb bag", "24-lb bag", "30-lb bag", "40-lb bag"] }
    ],
    "variants": [
      { "product_id": "129809", "part_number": "102301", "attributes": { "Flavor": "Lamb & Oat Meal", "Size": "4-lb bag" }, "price": 20.68, "autoship_price": 19.65, "price_per_unit": 5.17, "price_per_unit_unit": "lb", "in_stock": true, "selected": false },
      { "product_id": "129810", "part_number": "102302", "attributes": { "Flavor": "Lamb & Oat Meal", "Size": "16-lb bag" }, "price": 54.48, "autoship_price": 51.76, "price_per_unit": 3.41, "price_per_unit_unit": "lb", "in_stock": true, "selected": false }
    ],
    "promotions": [
      { "id": "19082", "group": "PRODUCT", "description": "New Customers Only: Spend $49+, Get $25 eGift Card + Free Shipping with code: WELCOME", "code": "WELCOME" }
    ]
  },
  "credits_used": 10
}
```

A captured `/search` for `{"query": "dog chew toys"}`, which Chewy redirected to a category (first row, key benefits trimmed):

```json
{
  "query": "dog chew toys",
  "category_id": null,
  "category_name": "Dog Chew Toys",
  "redirect": { "type": "category", "category_id": "316", "name": "Dog Chew Toys", "url": "https://www.chewy.com/b/chew-toys-316" },
  "page": 1,
  "sort": "relevance",
  "page_size": 36,
  "total_results": 2250,
  "total_pages": 63,
  "count": 36,
  "sponsored_removed": 9,
  "products": [
    {
      "product_id": "56874",
      "name": "Benebone Bacon Flavor Wishbone Tough Dog Chew Toy, Medium",
      "brand": "Benebone",
      "url": "https://www.chewy.com/benebone-bacon-flavor-wishbone-tough/dp/56874",
      "price": 12.78,
      "strike_price": 13.45,
      "strike_price_type": "LIST",
      "strike_savings_pct": 5,
      "autoship_allowed": true,
      "autoship_price": 12.14,
      "autoship_discount_pct": 5,
      "first_autoship_price": null,
      "rating": 4.5151,
      "rating_count": 12768,
      "in_stock": true,
      "is_deal": true
    }
  ]
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def chewy(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/chewy/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Cheapest dry dog food in a category (10 credits)
page = chewy("search", {"category_id": "294", "sort": "price_low"})
for p in page["products"][:10]:
    print(p["name"][:60], p["price"], "autoship", p["autoship_price"], "first autoship", p["first_autoship_price"])

# 2. One product with every size and flavor (10 credits)
item = chewy("product", {"product_id": page["products"][0]["product_id"]})
print(item["rating"], item["rating_count"], item["review_count"])
for v in item["variants"]:
    print(v["attributes"], v["price"], v["autoship_price"], v["in_stock"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Chewy answered.

- **search** - `query`, `category_id`, `category_name`, `redirect` (null, or {`type`, `category_id`, `name`, `url`}), `page`, `sort`, `page_size`, `total_results`, `total_pages`, `count`, `sponsored_removed`, `breadcrumbs[]` {`category_id`, `name`, `url`}, `products[]` (`product_id`, `part_number`, `parent_part_number`, `name`, `brand`, `url`, `image`, `price`, `offer_price`, `strike_price`, `strike_price_type`, `strike_savings_pct`, `autoship_allowed`, `autoship_price`, `autoship_discount_pct`, `autoship_deal`, `first_autoship_price`, `first_autoship_discount_pct`, `first_autoship_max_savings`, `map_price`, `map_enforced`, `price_per_unit`, `price_per_unit_unit`, `rating`, `rating_count`, `in_stock`, `has_more_choices`, `is_deal`, `is_new`, `is_chewy_exclusive`, `is_discontinued`, `is_prescription`, `is_vet_diet`, `is_fresh`, `is_frozen`, `is_dropshipped`, `key_benefits[]`).
- **product** - `product_id`, `part_number`, `product_part_number`, `name`, `product_name`, `brand`, `brand_url`, `url`, `gtin`, `description`, `key_benefits[]`, `price`, `offer_price`, `list_price`, `strike_price`, `strike_price_type`, `strike_savings`, `strike_savings_pct`, `map_price`, `map_enforced`, `autoship_allowed`, `autoship_price`, `autoship_discount_pct`, `first_autoship_price`, `first_autoship_discount_pct`, `first_autoship_max_savings`, `price_per_unit`, `price_per_unit_unit`, `number_of_units`, `on_special`, `in_stock`, `is_discontinued`, `is_new`, `is_prescription`, `is_vet_diet`, `is_fresh`, `is_frozen`, `max_quantity`, `shipping_message`, `rating`, `rating_count`, `review_count`, `rating_distribution[]` {`stars`, `count`, `percent`}, `attribute_scores` {name: score}, `attributes` {name: value}, `weight`, `dimensions`, `specifications[]` {`name`, `values[]`}, `details[]` {`group`, `title`, `content`}, `breadcrumbs[]` {`category_id`, `name`, `url`}, `images[]`, `variant_options[]` {`name`, `values[]`}, `variants[]` {`product_id`, `part_number`, `name`, `attributes`, `price`, `autoship_price`, `price_per_unit`, `price_per_unit_unit`, `in_stock`, `image`, `url`, `selected`}, `promotions[]` {`id`, `group`, `description`, `code`}.

## Guardrails

- Every call costs 10 credits. Prefer search rows (which already carry one-time, Autoship and first-Autoship prices) over a product call per item, and never loop over pages or products without telling the user the credit cost first.
- Prices are in US dollars and national; Chewy is online only, with no stores, store stock or store locator.
- Three prices, three meanings: `price` is the one-time purchase price, `autoship_price` the recurring Autoship (repeat delivery) price, and `first_autoship_price` the first Autoship order only, a bigger discount capped at `first_autoship_max_savings` dollars. Name which one you quote.
- `autoship_price` can be `null` even when `autoship_allowed` is true (deal items often carry no Autoship price). Say so; do not compute one from `autoship_discount_pct`.
- `map_price` is the minimum advertised price and `map_enforced` whether it is enforced. `strike_price` is the crossed-out comparison price, and `strike_price_type` says what it is (`LIST`).
- A broad query can be redirected: when `redirect` is not null, the products are that category's listing, not a keyword match. Tell the user which category they are looking at.
- `sort` in the response echoes the order the results are actually in.
- `rating` is the average out of 5 and `rating_count` the number of ratings; `review_count` (product only) counts written reviews and is lower. Review text is not returned.
- Sponsored listings are removed from search; `sponsored_removed` counts them.
- Never fabricate prices, ratings or stock. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (neither or both of `query` and `category_id`, an unknown `sort`, `page` above 100, neither `product_id` nor `url`, or a URL that is not a chewy.com `/dp/` product URL).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means Chewy does not know that product id; use the number after `/dp/` in the URL or a search row's `product_id`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data).
- `502` means Chewy is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.33.0
npm install scavio@0.33.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.chewy.search({ query: "grain free cat treats", sort: "rating" });
if (found.redirect) console.log("Chewy redirected to", found.redirect.name);
const item = await scavio.chewy.product({ product_id: found.products[0].product_id });
```

MCP: the Scavio MCP server exposes both endpoints as tools (`search_chewy`, `get_chewy_product`). Chewy is opt-in: add `chewy` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.31.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,chewy"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/chewy-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data), [product](https://scavio.dev/docs/chewy-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data). Overview: [Chewy API](https://scavio.dev/chewy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=chewy-product-data).
