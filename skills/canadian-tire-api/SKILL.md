---
name: canadian-tire-api
description: "Canadian Tire API: search canadiantire.ca at the store you choose with that store's CAD price, regular price and stock, read full product detail, check price and stock for up to 50 SKUs in one call, find stores near a postal code with their stock and aisle for an item, and list each store's clearance and deals. 6 endpoints, 1 credit each."
version: 1.0.0
tags: canadian-tire, canadiantire, canadian-tire-api, canada, canadian-retail, cad-prices, store-prices, store-inventory, in-store-stock, aisle-location, clearance, deals, rebates, product-search, product-data, store-locator, retail, price-monitoring, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/canadiantire-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api
---

# Canadian Tire API - Store Prices, Stock, Clearance, Deals

Search Canadian Tire and read products at the store you choose: that store's price and regular price in CAD, units in stock and aisle, sale and clearance flags, and pickup and delivery dates. Check up to 50 SKUs at once, find stores near a postal code with their stock of one item, and list a store's clearance and deals. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find tools, automotive, home or outdoor products at Canadian Tire by keyword or category
- Check what an item costs at a specific Canadian Tire store, and how many are in stock there and in which aisle
- Find which Canadian Tire stores near a postal code have an item in stock
- Check price and stock for a list of SKUs at one store
- List clearance items at a Canadian Tire store
- List a store's sale prices, instant rebates, special buys or Triangle Rewards offers
- Compare Canadian Tire prices across stores or provinces, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Canadian Tire endpoints cost **1 credit**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/canadiantire/search` | 1 | 24 results per page at one store: price and regular price (CAD), price range for multi-variant items, savings, badges, rebate, rating, review count, brand, part number, SKUs, and stock at the store and online |
| `POST /api/v1/canadiantire/product` | 1 | One product by code: breadcrumb, images, videos, descriptions, features, specifications, price and regular price, warranty, manuals, variants with their SKUs, and the store's stock and pickup and ship-to-home dates |
| `POST /api/v1/canadiantire/stores` | 1 | Stores near a postal code or coordinates, nearest first: `store_id`, name, address, phone, coordinates, distance, weekly hours, services. With `sku`, each store's stock quantity and aisle for it |
| `POST /api/v1/canadiantire/availability` | 1 | Up to 50 SKUs at one store in one call: price, regular price, sale and clearance flags, price valid-until date, quantity, aisle, online stock, pickup and delivery dates. Unknown SKUs are listed in `not_found` |
| `POST /api/v1/canadiantire/clearance` | 1 | Every clearance item at one store, 100 per page, in-stock only by default |
| `POST /api/v1/canadiantire/deals` | 1 | Items on a deal at one store, 100 per page: `sale`, `instant_rebate`, `special_buy` or `loyalty` (Triangle Rewards) |

## Workflow

Prices and stock are per store, and differ by province (Quebec prices differ from Ontario's), so pin the store first.

1. **Pick the store:** call `/canadiantire/stores` with the user's `postal_code` (or `latitude` and `longitude`). Each row has a `store_id`.
2. **Search at that store:** call `/canadiantire/search` with `query` (or `category_id`) and `store_id`. Each row has a `code` (like `0547273P`) and its 7-digit `sku`.
3. **One product in full:** call `/canadiantire/product` with the `code` as `product_code` and the same `store_id`.
4. **Many SKUs at once:** call `/canadiantire/availability` with `store_id` and up to 50 `skus`. This is the cheap way to watch a list of items at one store.
5. **Which nearby store has it:** call `/canadiantire/stores` with `sku`. Each store gets `quantity` and `aisle` for that item.
6. **Markdowns:** call `/canadiantire/clearance` or `/canadiantire/deals` with `store_id`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keywords. Pass this or `category_id`. A broad word like "drill" that the site answers with a category page returns that category's products |
| `category_id` | string | one of | `DC` followed by 7 digits (e.g. `DC0002209`), or a canadiantire.ca category URL ending in one |
| `store_id` | string | required | Store number from `/stores`, e.g. `"600"` |
| `page` | integer | 1 | 1-based page (1-100), 24 results per page |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc`, `newest`, `rating` or `bestseller` |
| `in_stock_only` | boolean | false | Only items in stock at `store_id` |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_code` | string | required | The `code` of a search result, e.g. `0547273P` |
| `store_id` | string | required | Store number |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `postal_code` | string | one of | Canadian postal code (or its first 3 characters), e.g. `M5V 2T6` |
| `latitude`, `longitude` | number | one of | Coordinates to search around, instead of `postal_code` |
| `radius_km` | number | 25 | Search radius in km, 1-200 |
| `limit` | integer | 10 | Stores to return, nearest first, 1-50 |
| `sku` | string | - | 7-digit SKU; each store also gets its stock quantity and aisle for it |

### Availability (`/availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | Store number |
| `skus` | string[] | required | 1-50 SKUs, 7 digits each (the `sku` of a search result or product variant) |

### Clearance (`/clearance`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | Store number |
| `page` | integer | 1 | 1-based page (1-100), 100 results per page |
| `in_stock_only` | boolean | true | Only clearance items in stock at `store_id` |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | Store number |
| `type` | string | required | `sale` (this week's sale prices), `instant_rebate`, `special_buy` or `loyalty` (Triangle Rewards offers) |
| `page` | integer | 1 | 1-based page (1-100), 100 results per page |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/canadiantire/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "600", "skus": ["0547273", "0438858"]}'
```

Captured response (store 600; trimmed to 1 of 2 items):

```json
{
  "data": {
    "store_id": "600",
    "count": 2,
    "not_found": [],
    "items": [
      {
        "sku": "0547273",
        "sku_number": "054-7273-0",
        "part_number": "DCK277D2",
        "price": 199.99,
        "was_price": 299.99,
        "price_range": null,
        "was_price_range": null,
        "savings": "Save 33% ($100.00)",
        "is_on_sale": true,
        "is_clearance": false,
        "badges": ["BESTSELLER", "TESTEDFORLIFE", "PROMO"],
        "rebate": null,
        "price_valid_until": "2026-11-05T23:59:59.000Z",
        "quantity": 3,
        "aisle": "Aisle 219",
        "warehouse_quantity": 1596,
        "sellable": true,
        "orderable": true,
        "pickup": { "enabled": true, "eta": "2026-10-31T12:30:00.000Z" },
        "ship_to_home": { "enabled": false, "eta_earliest": "2026-11-02T00:00:00.000Z", "eta_latest": null },
        "express_delivery": { "enabled": true, "eta": "2026-10-31T13:00:00.000Z", "order_by": "2026-10-31 16:30:00.0" },
        "warehouse_pickup_eta": "2026-11-06T00:00:00.000Z",
        "warehouse_ship_eta": "2026-11-07T00:00:00.000Z"
      }
    ]
  },
  "response_time": 1974,
  "credits_used": 1
}
```

A captured `/stores` row for `{"postal_code": "M5V 2T6", "sku": "0438858"}` (hours trimmed to one day):

```json
{
  "store_id": "621",
  "name": "Liberty Village, ON",
  "address": {
    "line1": "5 Joe Shuster Way",
    "line2": null,
    "city": "Toronto",
    "province": "ON",
    "postal_code": "M6K 0C7",
    "formatted": "5 Joe Shuster Way, Ontario, Toronto, M6K 0C7"
  },
  "phone": "4165883232",
  "latitude": 43.639935,
  "longitude": -79.423492,
  "distance_km": 1.94,
  "timezone": "America/Toronto",
  "hours": [{ "day": "Sunday", "open": "8:00 AM", "close": "10:00 PM" }],
  "services": [],
  "curbside_pickup": true,
  "quantity": 2,
  "aisle": null,
  "warehouse_quantity": 4
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def ct(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/canadiantire/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. The user's store
store = ct("stores", {"postal_code": "M5V 2T6", "limit": 1})["stores"][0]
sid = store["store_id"]

# 2. Search at that store, in stock only
rows = ct("search", {"query": "dewalt drill", "store_id": sid, "in_stock_only": True})["products"]

# 3. Price and stock for every hit in one call
skus = [r["sku"] for r in rows if r["sku"]][:50]
for it in ct("availability", {"store_id": sid, "skus": skus})["items"]:
    print(it["sku"], it["price"], "was", it["was_price"], "qty", it["quantity"], it["aisle"])

# 4. This store's clearance
clr = ct("clearance", {"store_id": sid})
print(clr["total_results"], "clearance items at", store["name"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Canadian Tire answered.

- **search / clearance / deals** - `query`, `category_id`, `category_name`, `corrected_query`, `redirect_url` (search) or `deal_type` (clearance, deals), `store_id`, `page`, `page_size`, `total_results`, `total_pages`, `count`, `categories[]` {`category_id`, `name`}, `products[]` (`position`, `code`, `sku`, `skus[]`, `sku_number`, `part_number`, `title`, `brand`, `url`, `image`, `rating`, `review_count`, `price`, `was_price`, `price_range` {`min`, `max`}, `was_price_range`, `savings`, `is_on_sale`, `is_clearance`, `badges[]`, `rebate` {`message`, `price_after_rebate`}, `is_multi_variant`, `store_quantity`, `warehouse_quantity`, `sellable`, `warranty`).
- **product** - `code`, `name`, `brand`, `url`, `breadcrumb[]`, `images[]`, `videos[]`, `rating`, `review_count`, `short_description`, `description`, `features[]`, `specifications[]` {`label`, `value`}, `part_number`, the price fields above, `warranty`, `manuals[]`, `status`, `sellable`, `store_id`, `store_quantity`, `warehouse_quantity`, `pickup`, `ship_to_home`, `express_delivery`, `warehouse_pickup_eta`, `warehouse_ship_eta`, `options[]`, `variants[]` {`sku`, `sku_number`, `part_number`, `name`, `url`, `status`, `sellable`, `badges[]`, `specifications[]`}.
- **stores** - `latitude`, `longitude`, `location_source`, `postal_code`, `fsa`, `radius_km`, `sku`, `count`, `stores[]` (`store_id`, `name`, `url`, `address` {`line1`, `line2`, `city`, `province`, `postal_code`, `formatted`}, `phone`, `latitude`, `longitude`, `distance_km`, `timezone`, `hours[]` {`day`, `open`, `close`}, `services[]`, `curbside_pickup`, and with `sku`: `quantity`, `aisle`, `warehouse_quantity`).
- **availability** - `store_id`, `count`, `not_found[]`, `items[]` (`sku`, `sku_number`, `part_number`, price fields, `price_valid_until`, `quantity`, `aisle`, `warehouse_quantity`, `sellable`, `orderable`, `pickup`, `ship_to_home`, `express_delivery`, `warehouse_pickup_eta`, `warehouse_ship_eta`).

## Guardrails

- Prices are in Canadian dollars: `199.99` is CA$199.99.
- Every price and stock figure belongs to `store_id`. Prices differ by province (Quebec differs from Ontario), so never carry a price from one store to another; name the store when quoting.
- A multi-variant product (tires, sizes, colours) has `price: null` and a `price_range` instead. Use `/availability` with the variant's 7-digit `sku` for one exact price.
- `store_quantity` / `quantity` is units at the store; `warehouse_quantity` is the online warehouse, not the store.
- Canadian Tire returns `rating` and `review_count` only; there is no review text endpoint.
- Never fabricate prices, stock or aisles. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (no `store_id`, neither `query` nor `category_id`, a `product_code` not like `0547273P`, a SKU that is not 7 digits, or an unknown deal `type`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product code; re-run the search for a fresh `code`. Not charged. On `/availability` unknown SKUs are not an error: they come back in `not_found`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api).
- `502` means Canadian Tire is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.31.0
npm install scavio@0.31.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.canadianTire.stores({ postal_code: "M5V 2T6", limit: 1 });
const store_id = near.stores[0].store_id;
const found = await scavio.canadianTire.search({ query: "dewalt drill", store_id });
const stock = await scavio.canadianTire.availability({ store_id, skus: ["0547273", "0438858"] });
const deals = await scavio.canadianTire.deals({ store_id, type: "sale" });
```

MCP: the Scavio MCP server exposes all 6 endpoints as tools (`search_canadian_tire`, `get_canadian_tire_product`, `get_canadian_tire_stores`, `get_canadian_tire_availability`, `get_canadian_tire_clearance`, `get_canadian_tire_deals`). Canadian Tire is opt-in: add `canadiantire` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.29.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,canadiantire"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/canadiantire-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api), [product](https://scavio.dev/docs/canadiantire-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api), [stores](https://scavio.dev/docs/canadiantire-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api), [availability](https://scavio.dev/docs/canadiantire-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api), [clearance](https://scavio.dev/docs/canadiantire-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api), [deals](https://scavio.dev/docs/canadiantire-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api). Overview: [Canadian Tire API](https://scavio.dev/canadiantire-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=canadian-tire-api).
