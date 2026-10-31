# Lowe's Product Data API - Store Price, Stock, Search, Reviews

Search Lowe's and read one item at the store you choose: that store's price, was-price and sale end date, units on hand, aisle and bay, and stock at nearby stores. A store locator turns a ZIP into store numbers, and a reviews endpoint pages customer reviews with the star breakdown. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find tools, appliances, lumber or hardware at Lowe's by keyword or category
- Check what an item costs at a specific Lowe's store, and whether it is in stock there
- Find which aisle and bay an item sits in at a Lowe's store
- See which nearby Lowe's stores have an item in stock
- List the deals (items on sale) at one Lowe's store
- Read Lowe's customer reviews or the rating breakdown for an item
- Find Lowe's stores near a ZIP code
- Monitor Lowe's prices, promotions or stock

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Search, product and stores cost 2 credits each; reviews cost 1.

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
| `POST /api/v1/lowes/search` | 2 | 24 items per page at one store: price, was-price, savings and sale end date, brand, model number, rating, review count, stock and availability for pickup, truck delivery, parcel shipping and same-day delivery. `on_sale: true` returns that store's deals |
| `POST /api/v1/lowes/product` | 2 | One item at one store: price and was-price, on-hand stock with lead time per fulfillment method, stock at nearby stores, aisle and bay, grouped specifications, bullets, UPC, dimensions, weight, images, and the store's address and hours |
| `POST /api/v1/lowes/stores` | 2 | Up to 10 stores near a ZIP, nearest first: `store_id`, name, address, phone, coordinates, distance, time zone, hours and features |
| `POST /api/v1/lowes/reviews` | 1 | 10 reviews per page with rating, title, text, date, reviewer, recommended, helpful votes, verified and incentivized flags, photos and brand replies, plus the average, total and count per star |

## Workflow

Every Lowe's price and stock figure belongs to one store, so pin the store first.

1. **Pick the store:** call `/lowes/stores` with the user's `zip`. Each store has a `store_id` and its own ZIP in `address.postal_code`.
2. **Search at that store:** call `/lowes/search` with `query` (or `category_id`), `store_id` and the store's own `zip`. Add `on_sale: true` for the store's deals.
3. **One item in full:** call `/lowes/product` with an `item_id` from search plus the same `store_id` and `zip`. It adds the aisle and bay (`aisle_locations[]`) and `pickup.nearby_stores[]`.
4. **Reviews (optional):** call `/lowes/reviews` with the `item_id`. Reviews are not store-scoped.

Pass the store's own ZIP with its `store_id`, not the user's home ZIP. The response echoes the store actually used in `store_id` and `store`; if Lowe's answers for a different store the call fails with an unbilled `502` instead of returning another store's prices.

There is no clearance endpoint. For markdowns at a store, search with `on_sale: true`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Keywords (1-200 chars). Pass this or `category_id`, not both |
| `category_id` | string | one of | The number at the end of a lowes.com/pl/ URL, e.g. `4294607842` |
| `store_id` | string | required | Store number, up to 4 digits, e.g. `"0595"` (from `/stores`) |
| `zip` | string | required | 5-digit ZIP; use the store's own ZIP from `/stores` |
| `page` | integer | 1 | 1-based page, 24 per page; page 31 is the last Lowe's serves |
| `on_sale` | boolean | false | Only items on sale at this store (with a was-price). A page can then hold fewer than 24 |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | Lowe's item id (the number at the end of a lowes.com/pd/ URL), or the full product URL |
| `store_id` | string | required | Store number from `/stores` |
| `zip` | string | required | The store's own 5-digit ZIP |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | 5-digit US ZIP to search near |
| `limit` | integer | 10 | Stores to return, nearest first, 1-10 |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | required | Lowe's item id or product URL |
| `page` | integer | 1 | 1-based page, 10 reviews per page |
| `sort` | string | `newest` | `newest`, `oldest` or `most_helpful` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/lowes/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "5016412045", "store_id": "0595", "zip": "28117"}'
```

Captured response (store 0595, Mooresville NC; trimmed to the price, stock and location fields, 2 of 8 nearby stores):

```json
{
  "data": {
    "item_id": "5016412045",
    "item_number": "6812916",
    "model_number": "CMCD714D1",
    "brand": "CRAFTSMAN",
    "title": "20-volt 1/2-in Keyless Brushless Cordless Drill 1 -Batteries Included, and Charger Included",
    "url": "https://www.lowes.com/pd/CRAFTSMAN-20-volt-Max-1-2-in-Keyless-Brushless-Cordless-Drill-1-Batteries-Included-Soft-Bag-Included/5016412045",
    "upc": "198706013438",
    "rating": 4.9,
    "review_count": 97,
    "price": 129,
    "original_price": null,
    "currency": "USD",
    "discount_amount": null,
    "discount_percent": null,
    "promotion_end": null,
    "price_type": "STORE",
    "promotions": ["Member Exclusive Offer"],
    "in_stock": true,
    "stock_quantity": 7,
    "pickup": {
      "available": true,
      "quantity": 7,
      "total_quantity": 430,
      "lead_time_days": 0,
      "earliest_date": "2026-10-31T15:25-04:00",
      "location_id": "0595",
      "location_type": "store",
      "service": null,
      "nearby_stores": [
        { "store_id": "2750", "distance_miles": 5.4, "available": true, "quantity": 8 },
        { "store_id": "0489", "distance_miles": 10.2, "available": true, "quantity": 5 }
      ]
    },
    "delivery": {
      "available": true,
      "quantity": 0,
      "total_quantity": 432,
      "lead_time_days": 1,
      "earliest_date": "2026-11-02T08:00:00-05:00",
      "location_id": "0595",
      "location_type": "store",
      "service": "Box Truck"
    },
    "aisle_locations": [
      { "aisle": "64", "bay": "7", "level": "TOOLS" },
      { "aisle": "64", "bay": "5", "level": "TOOLS" }
    ],
    "store_id": "0595",
    "zip": "28117",
    "store": {
      "store_id": "0595",
      "name": "Mooresville Lowe's",
      "address": { "street": "509 RIVER HWY", "city": "Mooresville", "state": "NC", "postal_code": "28117", "country": "US" },
      "phone": "(704) 660-7177",
      "time_zone": "America/New_York"
    }
  },
  "response_time": 11522,
  "credits_used": 2
}
```

On sale, the same fields carry the markdown. A captured search row at the same store: `"price": 99, "original_price": 179, "discount_amount": 80, "discount_percent": 44, "promotion_end": "2027-01-20T00:00:00.000Z"`.

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def lowes(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/lowes/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Nearest store, and its own ZIP
store = lowes("stores", {"zip": "28117", "limit": 1})["stores"][0]
sid, szip = store["store_id"], store["address"]["postal_code"]

# 2. That store's deals
deals = lowes("search", {"query": "cordless drill", "store_id": sid, "zip": szip, "on_sale": True})
for p in deals["products"][:5]:
    print(p["title"][:60], p["price"], "was", p["original_price"], "until", p["promotion_end"])

# 3. One item: stock, aisle and nearby stores
item = lowes("product", {"item_id": deals["products"][0]["item_id"], "store_id": sid, "zip": szip})
aisles = ", ".join(f"aisle {a['aisle']} bay {a['bay']}" for a in item["aisle_locations"])
print(store["name"], "has", item["stock_quantity"], "on hand at", aisles)
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Lowe's answered.

- **search** - `query`, `category_id`, `on_sale`, `store_id`, `zip`, `store` {store fields}, `page`, `page_size`, `total_results`, `total_pages`, `redirect_url`, `count`, `products[]` (`position`, `item_id`, `item_number`, `model_number`, `brand`, `title`, `url`, `image`, `rating`, `review_count`, `sponsored`, `price`, `original_price`, `currency`, `discount_amount`, `discount_percent`, `promotion_end`, `price_range`, `price_type`, `promotions[]`, `in_stock`, `stock_quantity`, `pickup`, `delivery`, `parcel`, `expedited_delivery`).
- **product** - the search item fields plus `description`, `bullets[]`, `upc`, `images[]`, `specifications[]` {`group`, `specs[]` {`name`, `value`}}, `featured_specs[]`, `dimensions` {`height`, `width`, `depth`, `unit`}, `weight` {`value`, `unit`}, `aisle_locations[]` {`aisle`, `bay`, `level`}, `pickup.nearby_stores[]` {`store_id`, `distance_miles`, `available`, `quantity`}, `store_id`, `zip`, `store`.
- Each fulfillment block (`pickup`, `delivery`, `parcel`, `expedited_delivery`) is {`available`, `quantity`, `total_quantity`, `lead_time_days`, `earliest_date`, `location_id`, `location_type`, `service`}.
- **stores** - `zip`, `count`, `stores[]` (`store_id`, `name`, `store_type`, `address` {`street`, `city`, `state`, `postal_code`, `country`}, `latitude`, `longitude`, `distance_miles`, `phone`, `pro_desk_phone`, `time_zone`, `hours` {`monday`..`sunday`: {`open`, `close`}}, `features[]`, `open_date`).
- **reviews** - `item_id`, `sort`, `page`, `page_size`, `total_results`, `total_pages`, `rating`, `recommended_count`, `not_recommended_count`, `rating_distribution[]` {`rating`, `count`}, `review_summary`, `count`, `reviews[]` (`id`, `rating`, `title`, `text`, `author`, `submitted_at`, `recommended`, `helpful_votes`, `unhelpful_votes`, `verified_purchase`, `incentivized`, `syndicated`, `photos[]`, `responses[]`).

## Guardrails

- Prices are in dollars: `129` is $129.00.
- `in_stock` and `stock_quantity` are units on the shelf at the pinned store (the pickup quantity). `total_quantity` on a fulfillment block is wider than the store; do not quote it as the store's stock.
- `price_type` `"STORE"` is the pinned store's own price. `"NETWORK"` or `"SOS"` means the store does not stock the item and the price is the online one; say so.
- `original_price`, `discount_amount`, `discount_percent` and `promotion_end` are only set when the item is on sale at that store.
- Always name the store (`store.name`) when quoting a price or stock figure; another store can differ.
- Never fabricate prices, stock or aisle locations. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (both `query` and `category_id`, a `store_id` longer than 4 digits, a ZIP that is not 5 digits, or `page` past 31).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such item; re-run the search for a fresh `item_id`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data).
- `502` means Lowe's is temporarily unavailable or answered for a different store. It is not charged; retry after a few seconds. Store-pinned calls are slow, so allow up to a minute per call.

## SDKs

```bash
pip install scavio==0.31.0
npm install scavio@0.31.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: near } = await scavio.lowes.stores({ zip: "28117", limit: 1 });
const store = near.stores[0];
const found = await scavio.lowes.search({ query: "cordless drill", store_id: store.store_id, zip: store.address.postal_code });
const item = await scavio.lowes.product({ item_id: found.data.products[0].item_id, store_id: store.store_id, zip: store.address.postal_code });
const reviews = await scavio.lowes.reviews({ item_id: found.data.products[0].item_id, sort: "most_helpful" });
```

MCP: the Scavio MCP server exposes all 4 endpoints as tools (`search_lowes`, `get_lowes_product`, `get_lowes_stores`, `get_lowes_reviews`). Lowe's is opt-in: add `lowes` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.29.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,lowes"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/lowes-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data), [product](https://scavio.dev/docs/lowes-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data), [stores](https://scavio.dev/docs/lowes-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data), [reviews](https://scavio.dev/docs/lowes-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data). Overview: [Lowe's API](https://scavio.dev/lowes-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lowes-product-data).
