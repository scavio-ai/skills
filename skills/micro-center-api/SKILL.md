---
name: micro-center-api
description: "Micro Center API: search Micro Center by keyword or category at the store you choose with price and that store's stock count (capped at 25+) and open-box units, read one product with specs, UPC, recent reviews, the store's open-box units with condition and price and which stores have it, and list every store id. 3 endpoints; search and product 2 credits, stores 1."
version: 1.0.0
tags: micro-center, microcenter, micro-center-api, computer-parts, pc-parts, graphics-cards, gpu, cpu, electronics, open-box, store-inventory, in-store-stock, product-search, product-data, product-specs, store-locator, retail, price-monitoring, stock-alerts, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/microcenter-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api
---

# Micro Center API - Store Stock, Open Box, Prices

Search Micro Center by keyword or category at the store you choose: price, original price and that store's stock as printed ("4 IN STOCK", "25+ IN STOCK"), open-box units with the lowest open-box price, rebates and in-store-only flags. Read one product with SKU, MPN, UPC, the full spec table, recent reviews, the store's open-box units with condition and price, and an in-stock flag for every store. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find graphics cards, CPUs, motherboards, laptops or other PC parts at Micro Center
- Check whether a Micro Center store has an item in stock, and how many
- Find which Micro Center stores have a product in stock
- List open-box units at a store, with condition, warranty and price
- Read a product's full spec table, UPC or MPN, or recent customer reviews
- Watch a GPU or CPU launch for stock at a local Micro Center
- Compare Micro Center prices with other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Search and product cost 2 credits each; stores costs 1.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/microcenter/search` | 2 | Up to 96 products per page at one store: product id, SKU, name, brand, category, price, original price, image, URL, highlights, the store's stock (label, quantity, capped flag, in stock, not carried), open-box count and lowest price, rebate text, in-store-only and sponsored flags |
| `POST /api/v1/microcenter/product` | 2 | One product: SKU, MPN, UPC, name, brand, description, price, original price, availability, ship and pickup flags, images, rating, review count, up to 10 recent reviews, breadcrumbs with category ids, the full spec table, the selected store with its stock and every open-box unit, and an in-stock flag per store |
| `POST /api/v1/microcenter/stores` | 1 | Every Micro Center store with its 3-digit `store_id`, name, city, state, street address, ZIP and store page URL, optionally by state |

## Workflow

Stock and open-box units belong to one store, so pin the store first.

1. **Pick the store:** call `/microcenter/stores` (optionally with `state`). Each row has a 3-digit `store_id` (`131` is Dallas, `151` Chicago). The list rarely changes; cache it.
2. **Search at that store:** call `/microcenter/search` with `query` (or `category`) and `store_id`. Each row has a `product_id` and the store's `stock`.
3. **One product in full:** call `/microcenter/product` with the `product_id` and the same `store_id`. `selected_store.open_box[]` lists each open-box unit; `stores_in_stock[]` says which other stores have it.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keywords (1-200 chars). Pass this, `category`, or both |
| `category` | string | one of | Category id (`518` is Graphics Cards), a `"category:Graphics Cards\|518"` value, or a microcenter.com listing URL carrying one. Product breadcrumbs carry category ids |
| `store_id` | string | `029` | 3-digit store id from `/stores`. Omitted, the web store `029` is used, which lists shippable items only |
| `page` | integer | 1 | 1-based page (1-100) |
| `per_page` | integer | 96 | `24`, `48` or `96` |
| `sort` | string | `best_match` | `best_match`, `rating`, `review_count`, `price_low`, `price_high` or `newest` |
| `include_out_of_stock` | boolean | false | Also list products the store has none of or does not carry |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | Micro Center product id (a search row's `product_id`, the number after `/product/` in a microcenter.com URL), or the product URL itself. Not the SKU |
| `store_id` | string | `029` | 3-digit store id; `selected_store` is that store |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `state` | string | - | 2-letter US state code to filter by, e.g. `TX` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/microcenter/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "691231", "store_id": "131"}'
```

Captured response (RTX 5070 at Dallas 131; description, images, reviews, specs and breadcrumbs trimmed, 4 of 32 `stores_in_stock`):

```json
{
  "data": {
    "product_id": "691231",
    "sku": "813972",
    "mpn": "GVN5070WF3OC12G",
    "upc": "889523048191",
    "name": "Gigabyte NVIDIA GeForce RTX 5070 WINDFORCE SFF OC Triple Fan 12GB GDDR7 PCIe 5.0 Graphics Card",
    "brand": "Gigabyte",
    "price": 839.99,
    "original_price": 839.99,
    "currency": "USD",
    "availability": "InStock",
    "can_ship": false,
    "can_pickup": true,
    "url": "https://www.microcenter.com/product/691231/gigabyte-nvidia-geforce-rtx-5070-windforce-sff-oc-triple-fan-12gb-gddr7-pcie-50-graphics-card",
    "rating": 4.7619,
    "review_count": 105,
    "category": "Graphics Cards",
    "category_id": "518",
    "selected_store": {
      "store_id": "131",
      "name": "Dallas",
      "address": "13929 N Central Expy",
      "city": "Dallas",
      "state": "TX",
      "zip": "75243",
      "stock": {
        "label": "4 NEW IN STOCK",
        "quantity": 4,
        "quantity_capped": false,
        "in_stock": true,
        "not_carried": false
      },
      "open_box": []
    },
    "stores_in_stock": [
      { "store_id": "205", "name": "AZ - Phoenix", "in_stock": false },
      { "store_id": "215", "name": "TX - Austin", "in_stock": false },
      { "store_id": "195", "name": "CA - Santa Clara", "in_stock": false },
      { "store_id": "101", "name": "CA - Tustin", "in_stock": false }
    ]
  },
  "response_time": 3689,
  "credits_used": 2
}
```

A captured `/search` row for `{"query": "rtx 5070", "store_id": "131"}`, with one open-box unit (image trimmed):

```json
{
  "position": 7,
  "sponsored": false,
  "product_id": "691225",
  "sku": "813949",
  "name": "Gigabyte NVIDIA GeForce RTX 5070 Ti WINDFORCE SFF Overclocked Triple Fan 16GB GDDR7 PCIe 5.0 Graphics Card",
  "brand": "Gigabyte",
  "category": "Graphics Cards",
  "price": 1449.99,
  "original_price": null,
  "url": "https://www.microcenter.com/product/691225/gigabyte-nvidia-geforce-rtx-5070-ti-windforce-sff-overclocked-triple-fan-16gb-gddr7-pcie-50-graphics-card",
  "highlights": [],
  "stock": {
    "label": "1 IN STOCK",
    "quantity": 1,
    "quantity_capped": false,
    "in_stock": true,
    "not_carried": false
  },
  "open_box": { "count": 1, "from_price": 1304.96 },
  "rebate": null,
  "in_store_only": true
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def mc(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/microcenter/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. The user's store (1 credit)
store = next(s for s in mc("stores", {"state": "TX"})["stores"] if s["city"] == "Dallas")
sid = store["store_id"]

# 2. Graphics cards in stock at that store, cheapest first (2 credits)
rows = mc("search", {"category": "518", "store_id": sid, "sort": "price_low"})["products"]
for p in rows[:5]:
    print(p["name"][:50], p["price"], p["stock"]["label"], "open box:", p["open_box"])

# 3. One card: open-box units here, and other stores with stock (2 credits)
item = mc("product", {"product_id": rows[0]["product_id"], "store_id": sid})
for u in item["selected_store"]["open_box"]:
    print(u["id"], u["condition"], u["price"])
print([s["name"] for s in item["stores_in_stock"] if s["in_stock"]])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Micro Center answered.

- **search** - `query`, `category_id`, `store` {`store_id`, `name`}, `page`, `per_page`, `sort`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `sponsored`, `product_id`, `sku`, `name`, `brand`, `category`, `price`, `original_price`, `url`, `image`, `highlights[]`, `stock` {`label`, `quantity`, `quantity_capped`, `in_stock`, `not_carried`}, `open_box` {`count`, `from_price`}, `rebate`, `in_store_only`).
- **product** - `product_id`, `sku`, `mpn`, `upc`, `name`, `brand`, `description`, `price`, `original_price`, `currency`, `availability`, `can_ship`, `can_pickup`, `url`, `images[]`, `rating`, `review_count`, `reviews[]` {`author`, `rating`, `date`, `body`}, `category`, `category_id`, `breadcrumbs[]` {`name`, `category_id`, `url`}, `specs[]` {`group`, `label`, `value`}, `selected_store` {`store_id`, `name`, `address`, `city`, `state`, `zip`, `stock` {same five}, `open_box[]` {`id`, `condition`, `warranty`, `terms`, `price`}}, `stores_in_stock[]` {`store_id`, `name`, `in_stock`}.
- **stores** - `state`, `count`, `stores[]` (`store_id`, `name`, `city`, `state`, `address`, `zip`, `url`).

## Guardrails

- Prices are in dollars: `839.99` is $839.99. Prices were identical across stores in every comparison; stock and open-box units differ by store.
- `stock.label` is the store's label as printed; `quantity` is read from it. Micro Center caps the count at 25: `"25+ IN STOCK"` reads `quantity: 25` with `quantity_capped: true`, so say "25 or more", never "25".
- `stock.not_carried: true` means the store does not carry the item at all, which is different from out of stock. Even the in-stock-only listing can include a few not-carried rows, so filter on `stock.in_stock`.
- Without `store_id` the web store `029` answers: shippable items only, a far shorter list than a physical store, and its `stock.label` is a shipping estimate rather than a count. Pass a real store for in-store stock.
- `stores_in_stock[]` is a yes/no per store, not a unit count. Only `selected_store.stock` has a count, so call `/product` with that `store_id` for a number at another store.
- `open_box` on a search row is a count and the lowest open-box price; `selected_store.open_box[]` on `/product` lists each unit with its id, condition, warranty and price.
- Search matches loosely (a nonsense query still returns products), so check that results match before answering. Sponsored rows are flagged `sponsored: true` and have no `position`.
- Never fabricate prices, stock or open-box units. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (neither `query` nor `category`, a `store_id` that is not a known 3-digit Micro Center store, a `state` that is not 2 letters, a `per_page` other than 24, 48 or 96, or an unknown `sort`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product id; use the `product_id` from search, not the SKU. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api).
- `502` means Micro Center is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.32.0
npm install scavio@0.32.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: tx } = await scavio.microCenter.stores({ state: "TX" });
const store_id = tx.stores[0].store_id;
const found = await scavio.microCenter.search({ query: "rtx 5070", store_id, sort: "price_low" });
const item = await scavio.microCenter.product({ product_id: found.data.products[0].product_id, store_id });
```

MCP: the Scavio MCP server exposes all 3 endpoints as tools (`search_micro_center`, `get_micro_center_product`, `get_micro_center_stores`). Micro Center is opt-in: add `microcenter` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.30.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,microcenter"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/microcenter-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api), [product](https://scavio.dev/docs/microcenter-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api), [stores](https://scavio.dev/docs/microcenter-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api). Overview: [Micro Center API](https://scavio.dev/microcenter-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=micro-center-api).
