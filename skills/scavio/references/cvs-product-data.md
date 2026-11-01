# CVS Product Data API - Prices, Coupons, Store Stock

Search CVS front-store products (health, beauty, personal care, household; nothing pharmacy) with regular and sale price, unit price, promotion text, ExtraBucks rewards and manufacturer coupons, and the units available at one store: on the shelf, for pickup and for same-day delivery. Read one product with UPC, description, ingredients, directions, warnings and every variant, and check stock for up to 20 SKUs at one store in one call. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find health, beauty, personal care or household items at CVS by keyword or item number
- Check a CVS product's price, sale price or unit price
- List the ExtraBucks rewards and manufacturer coupons on a CVS product
- Check how many units a CVS store has on the shelf, for pickup or for same-day delivery
- Check stock for a list of SKUs at one CVS store
- Read a product's ingredients, directions, warnings or UPC
- Compare CVS prices with Walgreens or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All CVS endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/cvs/search` | 1 | Up to 48 products per page: product id and SKU id, name, brand, URL, regular and sale price, unit price, promotion text, rating, review count, size, image, coupons (ExtraBucks rewards and manufacturer coupons), and stock at one store (in store, pickup, same-day delivery) plus online ship stock. Brand, price-range and rating facets |
| `POST /api/v1/cvs/product` | 1 | One product by URL or id: regular and sale price, unit price, promotion and its end date, rating, review count, UPC, size, description, highlights, ingredients, directions, warnings, attributes, breadcrumbs, images and every variant (SKU id, UPC, size, price, rating) |
| `POST /api/v1/cvs/stock` | 1 | Units at one store for up to 20 SKUs: in store, pickup and online ship stock (same-day units come from search) |

## Workflow

CVS has no store-locator endpoint: the store number is printed on every cvs.com store page ("Store ID: #7019") and in its URL (`.../storeid=7019`). Ask the user for it, or use the default.

1. **Search at a store:** call `/cvs/search` with `query` and `store_id`. Without `store_id` the stock is store 7019's (150 East 42nd St, New York). Each row has a `sku_id` and its `stock`.
2. **One product in full:** call `/cvs/product` with the row's `url` (or `product_id`). This call can take 10-30 seconds or more; give it a 60-second timeout or longer.
3. **Many SKUs at once:** call `/cvs/stock` with `store_id` and up to 20 `sku_ids`. This is the cheap way to watch a list of items at one store.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords or a CVS item number (1-200 chars) |
| `store_id` | string | `7019` | CVS store number for the stock fields. Prices are the same at every store |
| `page` | integer | 1 | 1-based page (1-100) |
| `limit` | integer | 20 | Results per page, 1-48 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | cvs.com product URL, `https://www.cvs.com/shop/<name>-prodid-<id>` |
| `product_id` | string | one of | CVS product id or SKU id (the number after `prodid-`, or a search row's `product_id` or `sku_id`) |

### Stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | CVS store number |
| `sku_ids` | string[] | required | 1-20 SKU ids: a search row's `sku_id` or a product's `variants[].sku_id` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/cvs/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "7019", "sku_ids": ["832677", "854346", "396475", "275748", "874110"]}'
```

Captured response (five toothpaste SKUs at store 7019, New York):

```json
{
  "data": {
    "store_id": "7019",
    "requested": 5,
    "count": 5,
    "items": [
      { "sku_id": "832677", "in_store": 0, "pickup": 0, "same_day_delivery": null, "ship": 8300, "ship_available": true },
      { "sku_id": "854346", "in_store": 0, "pickup": 0, "same_day_delivery": null, "ship": 8826, "ship_available": true },
      { "sku_id": "396475", "in_store": 0, "pickup": 0, "same_day_delivery": null, "ship": 6280, "ship_available": true },
      { "sku_id": "275748", "in_store": 4, "pickup": 4, "same_day_delivery": null, "ship": 8016, "ship_available": true },
      { "sku_id": "874110", "in_store": 19, "pickup": 19, "same_day_delivery": null, "ship": 6671, "ship_available": true }
    ]
  },
  "response_time": 1956,
  "credits_used": 1
}
```

A captured `/search` row for `{"query": "toothpaste"}` (store 7019), on sale with two coupons (image trimmed):

```json
{
  "position": 6,
  "product_id": "789787",
  "sku_id": "789787",
  "name": "Crest 3D White Fluoride Anticavity Whitening Toothpaste, Radiant Mint, 2.4 OZ",
  "brand": "Crest",
  "url": "https://www.cvs.com/shop/crest-3d-white-fluoride-anticavity-whitening-toothpaste-radiant-mint-2-4-oz-prodid-789787",
  "price": 4.69,
  "sale_price": 3.99,
  "on_sale": true,
  "unit_price": "$1.66/oz.",
  "promo": "Sale $3.99",
  "promo_condition": null,
  "rating": 4.5627,
  "review_count": 3044,
  "size": "2.40 OZ",
  "coupon_count": 2,
  "coupons": [
    {
      "type": "extrabucks",
      "description": "$4 ExtraBucks Rewards for purchasing 2 Crest3D 2.4z/StainEraser3.8z/ProHealth3.5-4.3z/Plus 5.4z/3in1 4.6zTP/Oral-BCharcoal/WhiteTB/Scope-Crest 500 mL",
      "coupon_number": null,
      "expires": null
    },
    {
      "type": "manufacturer",
      "description": null,
      "coupon_number": "1051068",
      "expires": "2026-11-15T23:59:59-05:00"
    }
  ],
  "stock": { "in_store": 50, "pickup": 46, "same_day_delivery": 4, "ship": 0, "ship_available": false },
  "pickup_eligible": true,
  "same_day_eligible": true,
  "is_new": false,
  "variants_count": 1
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def cvs(endpoint, body):
    # /product can take 10-30+ seconds; a generous timeout keeps it from failing early.
    r = requests.post(f"{BASE}/api/v1/cvs/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

STORE = "7019"  # from the cvs.com store page: "Store ID: #7019"

# 1. Search with this store's stock
rows = cvs("search", {"query": "toothpaste", "store_id": STORE, "limit": 48})["products"]
for p in rows:
    if p["stock"]["in_store"]:
        print(p["name"][:50], p["sale_price"], "on shelf:", p["stock"]["in_store"], [c["type"] for c in p["coupons"]])

# 2. Re-check the same SKUs later in one call
skus = [p["sku_id"] for p in rows[:20]]
for it in cvs("stock", {"store_id": STORE, "sku_ids": skus})["items"]:
    print(it["sku_id"], it["in_store"], it["pickup"])

# 3. One product in full
item = cvs("product", {"url": rows[0]["url"]})
print(item["upc"], item["ingredients"][:80] if item["ingredients"] else None)
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when CVS answered.

- **search** - `query`, `store_id`, `page`, `limit`, `total_results`, `total_pages`, `count`, `did_you_mean[]`, `products[]` (`position`, `product_id`, `sku_id`, `name`, `brand`, `url`, `price`, `sale_price`, `on_sale`, `unit_price`, `promo`, `promo_condition`, `rating`, `review_count`, `size`, `image`, `coupon_count`, `coupons[]` {`type` (`extrabucks` or `manufacturer`), `description`, `coupon_number`, `expires`}, `stock` {`in_store`, `pickup`, `same_day_delivery`, `ship`, `ship_available`}, `pickup_eligible`, `same_day_eligible`, `is_new`, `variants_count`), `facets` {`brands[]`, `price_ranges[]`, `ratings[]`: {`name`, `count`}}.
- **product** - `product_id`, `sku_id`, `name`, `brand`, `url`, `price`, `sale_price`, `on_sale`, `unit_price`, `promo`, `promo_end_date`, `rating`, `review_count`, `upc`, `size`, `max_quantity`, `description`, `highlights[]`, `ingredients`, `directions`, `warnings`, `attributes` {name: [values]}, `breadcrumbs[]` {`name`, `url`}, `category`, `images[]`, `pickup_eligible`, `same_day_eligible`, `variants[]` {`sku_id`, `name`, `upc`, `size`, `size_quantity`, `size_unit`, `price`, `sale_price`, `rating`, `review_count`, `url`, `image`}.
- **stock** - `store_id`, `requested`, `count`, `items[]` (`sku_id`, `in_store`, `pickup`, `same_day_delivery`, `ship`, `ship_available`).

## Guardrails

- Prices are in dollars and the same at every store: `4.69` is $4.69. `price` is the regular price and `sale_price` what it sells for now; they are equal when not on sale. `unit_price` is CVS's own label (`"$1.66/oz."`), a string.
- Stock belongs to `store_id`: `in_store` is on the shelf, `pickup` is what can be ordered for pickup there, `same_day_delivery` is from that store, and `ship` is the online warehouse (chain-wide, not the store). On `stock`, `same_day_delivery` is always `null` (that lookup does not report it); read same-day units from `search` with the same `store_id`.
- Without `store_id`, search stock is store 7019's (New York). Name the store when quoting stock.
- An unknown store number or SKU is NOT an error: everything reads 0. If every count is 0, check the store number before telling the user an item is out of stock.
- There is no store locator. Store numbers come from cvs.com store pages ("Store ID: #7019").
- ExtraBucks coupons carry text only (`coupon_number` and `expires` are `null`); manufacturer coupons carry a number and an end date, often with `description: null`.
- On `/product`, variant `price` can be `null`; use the product's own `price` and `sale_price`.
- Retail only: prescriptions and pharmacy services are not covered. Sponsored placements are excluded from search.
- Never fabricate prices, stock or coupons. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, neither `url` nor `product_id`, a non-numeric id, `limit` above 48, or more than 20 `sku_ids`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product; check the id, or pass the product's cvs.com `url`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data).
- `502` means CVS is temporarily unavailable. It is not charged; retry after a few seconds. `/product` is slow (10-30+ seconds), so allow at least a minute per call before treating it as failed.

## SDKs

```bash
pip install scavio==0.32.0
npm install scavio@0.32.0
```

```js
import { Scavio } from "scavio";

// reads SCAVIO_API_KEY; /product can take 30 seconds or more, so raise the 30s default timeout
const scavio = new Scavio({ timeout: 90_000 });
const { data: found } = await scavio.cvs.search({ query: "toothpaste", store_id: "7019" });
const stock = await scavio.cvs.stock({ store_id: "7019", sku_ids: found.products.slice(0, 20).map((p) => p.sku_id) });
const item = await scavio.cvs.product({ url: found.products[0].url });
```

MCP: the Scavio MCP server exposes all 3 endpoints as tools (`search_cvs`, `get_cvs_product`, `get_cvs_stock`). CVS is opt-in: add `cvs` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.30.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,cvs"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/cvs-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data), [product](https://scavio.dev/docs/cvs-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data), [stock](https://scavio.dev/docs/cvs-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data). Overview: [CVS API](https://scavio.dev/cvs-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cvs-product-data).
