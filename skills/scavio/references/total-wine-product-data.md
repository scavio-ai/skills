# Total Wine Product Data API - Store Prices, Stock, Store Locator

Search Total Wine & More, read one product in full, and find stores near a location. Total Wine prices and stock are set per store, so search and product take a `store_id` and return that store's price, units on hand and aisle. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find wine, spirits or beer at Total Wine by keyword or brand
- Check the price or stock of a bottle at a specific Total Wine store
- Find the aisle, bay or shelf of a product in a Total Wine store
- Find Total Wine stores near a ZIP code or city
- Compare Total Wine prices between stores, or against other liquor retailers
- Monitor Total Wine prices, stock or restocks

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=total-wine-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=total-wine-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 10 credits.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. All Total Wine endpoints cost **10 credits**.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/totalwine/stores` | 10 | Stores near a ZIP or city, nearest first: `store_id`, address, phone, coordinates, distance in miles |
| `POST /api/v1/totalwine/search` | 10 | Search at one store: price (cents), units in stock, purchase limit, aisle, size, rating, pickup/delivery/shipping. `store_id` required |
| `POST /api/v1/totalwine/product` | 10 | One product at one store: price, units in stock, aisle, bay, shelf, last restock date, ABV, taste profile. `store_id` required |

## Workflow

1. **Find the store:** call `/totalwine/stores` with `query` (a ZIP or city). Take `store_id` from the nearest store.
2. **Search at that store:** call `/totalwine/search` with `query` and `store_id`. Every row is that store's price and stock.
3. **Product detail:** call `/totalwine/product` with the row's `id` as `product_id` (or a `product_url`) and the same `store_id`.

A response is only returned when Total Wine answered for the requested store. If the store carries none of the matches, Total Wine falls back to other stores; those rows are dropped, `products` is empty and `searched_all_stores` is `true` (Virginia stores, for example, sell no spirits).

## Parameters

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | ZIP code, city, or "city, state" |
| `radius` | integer | 50 | Miles, 1-200 |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords (1-200 chars) |
| `store_id` | string | required | Store number from `/stores`, e.g. `"503"` |
| `page` | integer | 1 | 1-based page, 24 results per page |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | Numeric id from search or the URL's `/p/<id>` |
| `product_url` | string | one of | Total Wine product URL ending in `/p/<id>` |
| `store_id` | string | required | Store number from `/stores` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/totalwine/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "titos", "store_id": "503"}'
```

Captured response (store 503, San Antonio Del Norte; trimmed to one product):

```json
{
  "data": {
    "query": "titos",
    "store_id": "503",
    "page": 1,
    "total_results": 13,
    "total_pages": 1,
    "searched_all_stores": false,
    "count": 13,
    "products": [
      {
        "position": 1,
        "id": "96260175",
        "sku_id": "96260175-1",
        "name": "Tito's Handmade Vodka",
        "brand": "Tito's",
        "size": "1.75L Bottle",
        "pack": "Single",
        "container": "Bottle",
        "url": "https://www.totalwine.com/spirits/vodka/vodka/titos-handmade-vodka/p/96260175",
        "image": "https://www.totalwine.com/images/96260175/96260175-1-fr.png",
        "price": 2999,
        "prices": [
          {
            "price": 2999,
            "type": "EDLP"
          }
        ],
        "in_stock": true,
        "stock": 1204,
        "purchase_limit": 6,
        "aisle": "Aisle 03, Left",
        "rating": 4.8,
        "review_count": 3302,
        "pickup": true,
        "delivery": true,
        "shipping": false
      }
    ]
  },
  "response_time": 11108,
  "credits_used": 10
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def totalwine(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/totalwine/{endpoint}", headers=HEADERS, json=body)
    r.raise_for_status()
    return r.json()["data"]

# 1. Nearest store to a ZIP
store = totalwine("stores", {"query": "78801", "radius": 100})["stores"][0]
print(store["store_id"], store["name"], store["distance_miles"])

# 2. Prices and stock at that store (price is in cents)
found = totalwine("search", {"query": "titos", "store_id": store["store_id"]})
for row in found["products"]:
    print(row["name"], row["size"], row["price"] / 100, row["stock"], row["aisle"])

# 3. Full detail at the same store
p = totalwine("product", {"product_id": found["products"][0]["id"], "store_id": store["store_id"]})
print(p["price"], p["stock"], p["aisle"], p["bay"], p["shelf"], p["last_received_date"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Total Wine answered.

- **stores** - `query`, `radius`, `count`, `stores[]` (`store_id`, `name`, `address`, `city`, `state`, `zip`, `phone`, `latitude`, `longitude`, `distance_miles`, `delivery`).
- **search** - `query`, `store_id`, `page`, `total_results`, `total_pages`, `searched_all_stores`, `count`, `products[]` (`position`, `id`, `sku_id`, `name`, `brand`, `size`, `pack`, `container`, `url`, `image`, `price`, `prices[]` {`price`, `type`}, `in_stock`, `stock`, `purchase_limit`, `aisle`, `rating`, `review_count`, `pickup`, `delivery`, `shipping`).
- **product** - `id`, `sku_id`, `store_id`, `name`, `brand`, `size`, `pack`, `alcohol_percentage`, `url`, `images[]`, `price`, `prices[]`, `in_stock`, `stock`, `aisle`, `bay`, `shelf`, `last_received_date`, `rating`, `review_count`, `taste_profile[]`, `characteristics[]`, `breadcrumbs[]`, `pickup`, `delivery`, `shipping`.

## Guardrails

- `price` is an integer in cents: `2999` is $29.99. `prices[]` lists each price with its type; `EDLP` is the everyday price.
- Prices and stock are per store. Always name the store you quote, and never present one store's price as another's.
- `stock` is units on hand at that store when it was fetched; it can change within minutes.
- Never fabricate prices, stock or store details. Only return what the API returned, with the product `url` so the user can verify.

## Failure handling

- `400` means a missing or invalid parameter, most often a missing or non-numeric `store_id`. Look the store up with `/totalwine/stores`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such product.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=total-wine-product-data).
- `502` means Total Wine did not answer for the requested store or is temporarily unavailable. It is not charged; retry after a few seconds.

## SDKs

```bash
pip install scavio==0.29.1
npm install scavio@0.29.1
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.totalwine.stores({ query: "78801", radius: 100 });
const storeId = near.stores[0].store_id;
const found = await scavio.totalwine.search({ query: "titos", store_id: storeId });
const product = await scavio.totalwine.product({ product_id: found.data.products[0].id, store_id: storeId });
```

MCP: the Scavio MCP server exposes all 3 endpoints as tools (`search_totalwine`, `get_totalwine_product`, `get_totalwine_stores`). Total Wine is opt-in: add `totalwine` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.27.1"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,totalwine"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/totalwine-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=total-wine-product-data), [product](https://scavio.dev/docs/totalwine-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=total-wine-product-data), [stores](https://scavio.dev/docs/totalwine-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=total-wine-product-data). Overview: [Total Wine API](https://scavio.dev/totalwine-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=total-wine-product-data).
