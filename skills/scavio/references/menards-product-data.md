# Menards Product Data API - Search, Prices, Rebates, Store Stock

Read one Menards product by item id or menards.com URL with the full price ladder: everyday price, sale price and its end date, mail-in rebates (Menards' 11% rebate and others) and the final price after rebates, plus brand, model number, SKU, description, specifications, images, videos and documents. Add a store number to get that store's stock quantity, stock message and aisle location. Search menards.com at a chosen store, 40 products a page, each with its price after rebate and that store's stock count. Find Menards stores near a ZIP code or a city and state. All endpoints return structured JSON.

## When to trigger

Use this skill when the user asks to:
- Search Menards for a product by keyword and see what a nearby store has in stock and at what price
- Check a Menards product's price, sale price or price after rebate, from a menards.com link or item id
- See the mail-in rebates on a Menards item (the 11% rebate) and the dates they run
- Check whether a Menards store has an item in stock, how many units, and which aisle it is in
- Find Menards stores near a ZIP code or a city, with their services (garden center, rental center, propane)
- Read a Menards product's specifications, model number, SKU or documents
- Compare Menards prices with Home Depot, Lowe's or other retailers, or monitor them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. A search costs 2 credits; a product costs 1 credit, or 2 credits with a `store_id`; stores cost 1 credit.

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
| `POST /api/v1/menards/search` | 2 | Keyword search at one store, 40 products a page: item id, SKU, name, URL, image, price, everyday price, sale price, price type, mail-in rebates, final price after rebates, and that store's stock quantity, stock message, pickup and delivery flags. Total results and facets |
| `POST /api/v1/menards/product` | 1, or 2 with `store_id` | One product by item id or URL: name, brand, model number, SKU, description, bullets, specifications, images, videos, documents, everyday price, sale price and end date, mail-in rebates (text, amount, dates), final price after rebates, you-save amount, pickup, delivery and ship-to-store flags. With `store_id`: that store's stock quantity, stock message, aisle location and whether the item is sold there |
| `POST /api/v1/menards/stores` | 1 | Menards stores near a ZIP or a city and state, nearest first: store number, name, address, coordinates, distance in miles, open flag and services |

## Workflow

1. **Nearby store:** call `/menards/stores` with the user's `zip` (or `city` and `state`). Each row has a `store_id`.
2. **Find products:** call `/menards/search` with `query` and that `store_id`. 2 credits, 40 products a page, each with its price after rebate and the store's stock count. If the user already has a menards.com link, skip this: the item id is the number after `p-` (`.../p-60893666613-c-10085.htm` is item `60893666613`).
3. **Detail and aisle:** call `/menards/product` with a result's `item_id` (or the URL). 1 credit at the default store (3598, no stock), or 2 credits with `store_id` for that store's stock and aisle; that call typically takes 10-40 seconds, so give it a 60-second timeout or longer.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords, up to 200 characters |
| `store_id` | string | required | Menards store number from `/stores` (e.g. `"3181"`). An unknown store number is a 400 |
| `page` | number | `1` | Results page, 1-100, 40 products a page |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc`, `brand_asc` or `brand_desc`. Price sorts order by `everyday_price`, not the sale price |
| `in_stock_today` | boolean | `false` | Only products in stock at the store today |
| `min_price` | number | - | Lowest price in dollars |
| `max_price` | number | - | Highest price in dollars |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `item_id` | string | one of | Menards item id (8-16 digits): the number after `p-` in a menards.com product URL. Not the SKU or model number |
| `url` | string | one of | A menards.com product URL (the long SEO form, `/main/p-<id>.htm`, or `storeitem.html?iid=<id>`) |
| `store_id` | string | - | Menards store number from `/stores` (e.g. `"3181"`). Adds that store's stock and aisle, priced for that store. Costs 2 credits instead of 1 and is slower |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code to search around |
| `city` | string | one of | City to search around, with `state` |
| `state` | string | with `city` | 2-letter US state code, e.g. `WI` |

## Examples

```bash
curl -X POST https://api.scavio.dev/api/v1/menards/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "sledge hammer", "store_id": "3181"}'
```

Captured search result row ("sledge hammer" at store 3181, 27 results):

```json
{
  "position": 1,
  "item_id": "4364363664906880",
  "sku": "2482246",
  "name": "Masterforce® 12 lb. Fiberglass Sledge Hammer",
  "url": "https://www.menards.com/main/outdoors/gardening/garden-landscaping-tools/sledge-hammers/masterforce-reg-12-lb-fiberglass-sledge-hammer/md-12f-men/p-4364363664906880-c-13244.htm",
  "currency": "USD",
  "price": 38.98,
  "everyday_price": 38.98,
  "sale_price": null,
  "on_sale": false,
  "price_type": "regular",
  "rebates": [{ "text": "11% REBATE*", "amount": 4.29 }],
  "final_price": 34.69,
  "price_in_cart": false,
  "in_stock": true,
  "stock_quantity": 13,
  "stock_message": "In-Stock at",
  "not_available_at_store": false,
  "pickup_available": true,
  "delivery_available": true
}
```

```bash
curl -X POST https://api.scavio.dev/api/v1/menards/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "60893666613", "store_id": "3181"}'
```

Captured response (a hole cutter at store 3181, St Paul Midway; bullets, specifications and images trimmed):

```json
{
  "data": {
    "item_id": "60893666613",
    "sku": "3646905",
    "model_number": "CHC7-8",
    "name": "Southwire® 7/8\" Carbide-Tipped Hole Cutter",
    "brand": "Southwire",
    "url": "https://www.menards.com/main/tools/power-tool-accessories/hole-saws-sets-accessories/southwire-reg-7-8-carbide-tipped-hole-cutter/chc7-8/p-60893666613-c-10085.htm",
    "category_id": "10085",
    "currency": "USD",
    "price": 29.49,
    "everyday_price": 29.49,
    "sale_price": null,
    "sale_end_date": null,
    "rebates": [
      { "text": "11% REBATE*", "amount": 3.24, "start_date": "2026-11-02", "end_date": "2026-11-08", "limit": null }
    ],
    "final_price": 26.25,
    "unit_of_measure": "each",
    "you_save": 3.24,
    "you_save_text": "You Save $3.24 After Mail-In Rebate*",
    "not_available_at_store": false,
    "availability": "InStock",
    "pickup_available": true,
    "delivery_available": true,
    "ship_to_store_available": false,
    "store": {
      "store_id": "3181",
      "selected": true,
      "fulfillment": "Pick Up At Store",
      "in_stock": true,
      "stock_quantity": 3,
      "stock_message": "In-Stock",
      "locations": ["Item Located in Aisle 221 Section L"],
      "service_desk_department": "Electrical",
      "notes": []
    }
  },
  "response_time": 13242,
  "credits_used": 2
}
```

A captured `/stores` row for `{"zip": "55401"}` (24 stores returned):

```json
{
  "store_id": "3181",
  "name": "ST PAUL MIDWAY",
  "address": "2005 UNIVERSITY AVE W",
  "city": "SAINT PAUL",
  "state": "MN",
  "zip": "55104",
  "latitude": 44.959353,
  "longitude": -93.184011,
  "distance_miles": 4.4,
  "open": true,
  "services": ["Appliances", "Garden Center", "Grocery", "Propane Exchange", "Rental Center", "Truck Rental"]
}
```

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def menards(endpoint, body):
    # A product with a store_id typically takes 10-40 seconds; a generous timeout keeps it from failing early.
    r = requests.post(f"{BASE}/api/v1/menards/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Stores near a ZIP (1 credit)
store = menards("stores", {"zip": "55401"})["stores"][0]

# 2. Search that store, cheapest first (2 credits)
hits = menards("search", {"query": "sledge hammer", "store_id": store["store_id"], "sort": "price_asc"})
for p in hits["products"][:5]:
    print(p["name"], p["price"], "after rebate", p["final_price"], "on hand", p["stock_quantity"])

# 3. Detail and aisle for the first result (2 credits)
here = menards("product", {"item_id": hits["products"][0]["item_id"], "store_id": store["store_id"]})
print(here["model_number"], here["store"]["locations"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Menards answered.

- **search** - `query`, `store_id`, `page`, `sort`, `in_stock_today`, `min_price`, `max_price`, `total_results`, `total_pages`, `count`, `products[]` (`position`, `item_id`, `sku`, `name`, `url`, `image`, `currency`, `price`, `everyday_price`, `sale_price`, `on_sale`, `price_type`, `rebates[]` {`text`, `amount`}, `final_price`, `price_in_cart`, `unit_of_measure`, `in_stock`, `stock_quantity`, `stock_message`, `not_available_at_store`, `pickup_available`, `delivery_available`, `pickup_message`, `delivery_message`, `variation_count`), `facets[]` {`name`, `values[]` {`value`, `count`}}.
- **product** - `item_id`, `sku`, `model_number`, `name`, `brand`, `description`, `bullets[]`, `specifications[]` {`name`, `value`}, `url`, `category_id`, `images[]`, `videos[]`, `documents[]`, `safety_data_sheets[]`, `currency`, `price`, `everyday_price`, `sale_price`, `sale_end_date`, `rebates[]` {`text`, `amount`, `start_date`, `end_date`, `limit`}, `final_price`, `unit_of_measure`, `you_save`, `you_save_text`, `not_available_at_store`, `availability`, `pickup_available`, `delivery_available`, `ship_to_store_available`, `store` {`store_id`, `selected`, `fulfillment`, `in_stock`, `stock_quantity`, `stock_message`, `locations[]`, `service_desk_department`, `notes[]`}.
- **stores** - `zip`, `city`, `state`, `count`, `stores[]` (`store_id`, `name`, `address`, `city`, `state`, `zip`, `latitude`, `longitude`, `distance_miles`, `open`, `services[]`).

## Guardrails

- Search always runs at one store: `store_id` is required, and stock in the results is that store's. There is no category listing. A product needs its item id (from a search result or the number after `p-` in the menards.com URL) or the URL itself. The SKU and model number are not item ids.
- Search results carry no model number or aisle; call `/product` for those. When `price_in_cart` is true the rebate amount and `final_price` are null because Menards shows them only in the cart; items priced only in store have every price field null.
- Prices are in dollars. Without `store_id` the product is priced for the site's default store (3598) and every stock field is null; with `store_id` it is priced for that store. Name the store when quoting a price or stock.
- The price ladder: `everyday_price` is the regular price, `sale_price` a temporary price ending on `sale_end_date`, and `price` what the item sells for now. `rebates` are mail-in rebates (Menards' 11% rebate is one); `final_price` is the site's own "price after rebate", not what is charged at the register. Quote `price` as the purchase price and `final_price` as the after-rebate value, and give the rebate dates.
- `store_id` costs 2 credits instead of 1 and typically takes 10-40 seconds. Call without it when the user only needs the price.
- `store.stock_quantity` is that store's unit count and `store.locations` the aisle text ("Item Located in Aisle 221 Section L"). `not_available_at_store: true` means the store does not sell the item, which is different from out of stock.
- No ratings, reviews or UPC are returned.
- Never fabricate prices, rebates or stock. Only return what the API returned, with the product `url`.

## Failure handling

- `400` means a missing or invalid parameter (search without `query` or `store_id`, a `store_id` that is not a Menards store, neither `item_id` nor `url`, an item id that is not 8-16 digits, a URL that is not a menards.com product URL, a `store_id` that is not a store number, or `/stores` without `zip` or `city` plus `state`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` on `/product` means no such item id, or no such store number; check the id after `p-` in the URL, and take store numbers from `/stores`. Not charged.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data).
- `502` means Menards is temporarily unavailable. It is not charged; retry after a few seconds. A product with `store_id` is slow (10-40 seconds), so allow at least a minute per call before treating it as failed.

## SDKs

```bash
pip install scavio==0.34.0
npm install scavio@0.34.0
```

```js
import { Scavio } from "scavio";

// reads SCAVIO_API_KEY; a product with a store_id can take 40 seconds, so raise the 30s default timeout
const scavio = new Scavio({ timeout: 90_000 });
const { data: near } = await scavio.menards.stores({ zip: "55401" });
const store_id = near.stores[0].store_id;
const { data: hits } = await scavio.menards.search({ query: "sledge hammer", store_id });
const item = await scavio.menards.product({ item_id: hits.products[0].item_id, store_id });
```

MCP: the Scavio MCP server exposes all three endpoints as tools (`search_menards`, `get_menards_product`, `get_menards_stores`). Menards is opt-in: add `menards` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.32.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,menards"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/menards-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data), [product](https://scavio.dev/docs/menards-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data), [stores](https://scavio.dev/docs/menards-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data). Overview: [Menards API](https://scavio.dev/menards-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=menards-product-data).
