---
name: aldi-grocery-data
description: "ALDI grocery data API: search ALDI US at the store you choose with that store's price, sale price, unit price, stock level and in-store location, priced for in-store, pickup or delivery, read one product with ingredients, allergens and dietary labels, and find ALDI stores near a ZIP. 3 endpoints, 1 credit each."
version: 1.0.0
tags: aldi, aldi-us, aldi-api, aldi-grocery-data, grocery, groceries, supermarket, discount-grocery, store-prices, grocery-prices, store-inventory, in-stock, in-store-location, unit-price, ingredients, allergens, product-search, product-data, store-locator, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/aldi-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data
---

# ALDI Grocery Data API - Store Prices, Stock, Stores

Search ALDI US and read products at the store you choose: that store's price and sale price, unit price, stock level and where the item sits in the store, priced for in-store shopping, pickup or delivery. Read one product with its description, ingredients, allergen warnings and dietary labels, and find ALDI stores near a ZIP. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find groceries at ALDI by keyword, with prices at a specific store
- Check what an item costs at an ALDI store, or whether it is in stock there
- Compare ALDI's in-store shelf price with its pickup or delivery price
- List what is on sale at an ALDI store
- Read an ALDI product's ingredients, allergen warnings or dietary labels
- Find ALDI stores near a ZIP code
- Build a grocery basket or price comparison against other grocers, or monitor ALDI prices

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All ALDI endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/aldi/search` | 1 | Up to 60 products per page at one store: product id, name, brand, size, price and was-price, discount label, unit price, in stock and stock level, category, in-store location, ALDI-exclusive brand flag, dietary labels, image and URL |
| `POST /api/v1/aldi/product` | 1 | One product by id or aldi.us URL at one store: the search fields plus description, ingredients, allergen warnings, other detail sections and images |
| `POST /api/v1/aldi/stores` | 1 | ALDI stores near a ZIP, nearest first: `store_id`, name, street address, city, state, ZIP, coordinates and distance in miles |

## Workflow

Every ALDI price and stock figure belongs to one store and one shopping mode, so pin the store first.

1. **Pick the store:** call `/aldi/stores` with the user's `zip`. Each row has a `store_id`.
2. **Search at that store:** call `/aldi/search` with `query` and `store_id`. Pass `zip` instead of `store_id` to use the nearest store; the answer's `store.store_id` says which one was used.
3. **One product in full:** call `/aldi/product` with the row's `product_id` and the same `store_id`.
4. **Pickup or delivery price:** repeat the call with `service_type: "pickup"` or `"delivery"`. The default `instore` is the shelf price.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `store_id` | string | one of | ALDI store id from `/stores`, e.g. `"151248"` |
| `zip` | string | one of | US ZIP code; without `store_id`, the nearest ALDI store to it is used |
| `service_type` | string | `instore` | `instore` (shelf price), `pickup` or `delivery` (the online prices for ordering from that store) |
| `sort` | string | `best_match` | `best_match`, `price_low` or `price_high` |
| `limit` | integer | 30 | Products per page, 1-60 |
| `page` | integer | 1 | 1-based page (1-100) |
| `include_related` | boolean | false | Also return the related items ALDI lists after the exact matches |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | required | ALDI product id (the `product_id` of a search row, e.g. `16902710`), or an aldi.us product URL |
| `store_id` | string | one of | Store id |
| `zip` | string | one of | ZIP code for the nearest store, instead of `store_id` |
| `service_type` | string | `instore` | `instore`, `pickup` or `delivery` |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | US ZIP code to search around |
| `limit` | integer | 10 | Stores to return, nearest first, 1-50 |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/aldi/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "milk", "store_id": "151248"}'
```

Captured response (store 151248, Miami, in-store prices; trimmed to 2 of 15 products, images removed):

```json
{
  "data": {
    "query": "milk",
    "store": { "store_id": "151248", "service_type": "instore", "zip": null },
    "sort": "best_match",
    "include_related": false,
    "page": 1,
    "limit": 30,
    "total_results": 15,
    "total_pages": 1,
    "count": 15,
    "products": [
      {
        "position": 1,
        "product_id": "16902710",
        "name": "Friendly Farms Whole Milk",
        "brand": "Friendly Farms",
        "size": "1 gal",
        "price": 3.07,
        "was_price": null,
        "on_sale": false,
        "discount_label": null,
        "unit_price": "$0.02/fl oz",
        "in_stock": true,
        "stock_level": "highly_in_stock",
        "category": "Plain Milk",
        "in_store_location": "Cooler Doors",
        "store_brand": true,
        "dietary": ["Whole"],
        "url": "https://www.aldi.us/store/aldi/products/16902710-friendly-farms-vitamin-d-milk-1-gal"
      },
      {
        "position": 6,
        "product_id": "21059061",
        "name": "Simply Nature Organic Whole Omega-3 Milk",
        "brand": "Friendly Farms",
        "size": "64 fl oz",
        "price": 4.29,
        "was_price": 4.39,
        "on_sale": true,
        "discount_label": "2% off",
        "unit_price": "$0.07/fl oz",
        "in_stock": true,
        "stock_level": "highly_in_stock",
        "category": "Plain Milk",
        "in_store_location": "Cooler Doors",
        "store_brand": true,
        "dietary": ["Whole"],
        "url": "https://www.aldi.us/store/aldi/products/21059061-friendly-farms-whole-omega-3-milk-64-fl-oz"
      }
    ]
  },
  "response_time": 5577,
  "credits_used": 1
}
```

A captured `/stores` row for `{"zip": "33131"}` (2 of 10 stores):

```json
[
  {
    "store_id": "392415",
    "name": "ALDI - RPB 55 - Miami",
    "address": "249 NW 6th Street Unit #601",
    "city": "Miami",
    "state": "FL",
    "zip": "33136",
    "address_line_2": "Miami, FL 33136",
    "latitude": 25.7803302,
    "longitude": -80.1985816,
    "distance_miles": 1.4
  },
  {
    "store_id": "151248",
    "name": "ALDI - RPB 71 - Miami",
    "address": "3750 S Dixie Hwy",
    "city": "Miami",
    "state": "FL",
    "zip": "33133",
    "address_line_2": "Miami, FL 33133",
    "latitude": 25.7313238,
    "longitude": -80.254303,
    "distance_miles": 5.1
  }
]
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def aldi(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/aldi/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. The user's store
store = aldi("stores", {"zip": "33131", "limit": 1})["stores"][0]
sid = store["store_id"]

# 2. Shelf prices at that store, cheapest first
rows = aldi("search", {"query": "eggs", "store_id": sid, "sort": "price_low"})["products"]
for p in rows[:5]:
    print(p["name"][:40], p["size"], p["price"], p["unit_price"], p["stock_level"], p["in_store_location"])

# 3. The same item priced for pickup at the same store
item = aldi("product", {"product_id": rows[0]["product_id"], "store_id": sid, "service_type": "pickup"})
print("in-store", rows[0]["price"], "pickup", item["price"], "at", store["name"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when ALDI answered.

- **search** - `query`, `store` {`store_id`, `service_type`, `zip`}, `sort`, `include_related`, `page`, `limit`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `product_id`, `name`, `brand`, `size`, `price`, `was_price`, `on_sale`, `discount_label`, `unit_price`, `in_stock`, `stock_level`, `category`, `in_store_location`, `store_brand`, `dietary[]`, `image`, `url`).
- **product** - the search product fields plus `store` {`store_id`, `service_type`, `zip`}, `description`, `ingredients`, `warnings`, `additional_info[]` {`title`, `text`}, `images[]`.
- **stores** - `zip`, `total_results`, `count`, `stores[]` (`store_id`, `name`, `address`, `city`, `state`, `zip`, `address_line_2`, `latitude`, `longitude`, `distance_miles`).

## Guardrails

- Prices are in dollars: `3.07` is $3.07. `unit_price` is ALDI's own label (`"$0.02/fl oz"`), a string, not a number.
- Every price belongs to one store AND one `service_type`. The same milk was $2.71 at a store in Illinois and $3.07 in Miami; at one Miami store 2% milk was $3.98 in-store and $4.39 for pickup or delivery. Name the store and the mode when quoting, and never carry a price from one store or mode to another.
- `instore` is the shelf price and the default. `pickup` and `delivery` are the online prices for ordering from that store and are often higher.
- `was_price` and `discount_label` are only set when the item is on sale at that store; `on_sale` is true then.
- `stock_level` is a level such as `highly_in_stock`, `in_stock` or `low_stock`. ALDI publishes a level, not a unit count; never quote a quantity.
- `in_store_location` is the store section (`"Cooler Doors"`), not an aisle number.
- `store_brand` true means an ALDI-exclusive brand. ALDI has no product ratings or reviews, so none are returned.
- Search returns exact matches only unless `include_related` is true.
- Never fabricate prices, stock or store details. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, neither `store_id` nor `zip`, a ZIP that is not 5 digits, a `product_id` that is not an ALDI id or aldi.us URL, or an unknown `service_type` or `sort`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product id; re-run the search for a fresh `product_id`. `404` with only a `zip` means no ALDI store near it. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data).
- `502` means ALDI is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.32.0
npm install scavio@0.32.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.aldi.stores({ zip: "33131", limit: 1 });
const store_id = near.stores[0].store_id;
const found = await scavio.aldi.search({ query: "milk", store_id, sort: "price_low" });
const pickup = await scavio.aldi.product({ product_id: found.data.products[0].product_id, store_id, service_type: "pickup" });
```

MCP: the Scavio MCP server exposes all 3 endpoints as tools (`search_aldi`, `get_aldi_product`, `get_aldi_stores`). ALDI is opt-in: add `aldi` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.30.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,aldi"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/aldi-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data), [product](https://scavio.dev/docs/aldi-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data), [stores](https://scavio.dev/docs/aldi-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data). Overview: [ALDI API](https://scavio.dev/aldi-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=aldi-grocery-data).
