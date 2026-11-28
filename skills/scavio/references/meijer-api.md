# Meijer API - Store Prices, Weekly Ad, mPerks Coupons, Aisles

Read Meijer (meijer.com, the Midwest grocery and general-merchandise chain: Michigan, Ohio, Indiana, Illinois, Kentucky, Wisconsin; US only, USD) store by store: product search, item lookup by Meijer id or UPC / EAN, department listings and deals collections priced at the store you choose with stock status and aisle, the departments and collections, stores near a ZIP, one store's hours and services, the store's current weekly ad, its mPerks coupons and an item's reviews. All 10 endpoints return structured JSON and cost 1 credit each.

**The one fact to get right: Meijer prices by store.** Every price, stock status and aisle is the store's you send as `store_id` (a Meijer store number from the stores endpoint). Measured 2026-11-28, Meijer Whole Milk, Gallon (Meijer id 4125010200, UPC 041250102007): $2.88 at Franklin IN (#295), $2.99 at Jeffersonville IN (#167) and Cincinnati OH (#224), $3.32 at Evergreen Park IL (#265) and $3.48 at Grand Rapids MI (#20). Without `store_id` Meijer picks a store by location and `store_used` names it, so always send the store you mean and always say which store a price came from.

Five limits shape every answer, so say them plainly:
- **Credits.** Every call costs 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Pages.** Search lists 52 items on page 1 and the next 48 on page 2; there is no page 3. Department and collection listings return their first 52 items with `total` counting them all: narrow with a subcategory path for more.
- **Coupons are listed, never clipped.** The coupons endpoint returns the mPerks coupons a visitor without an account sees: the first 48 with the total and department counts, or every coupon with `full_list` true (slower, up to about 2 minutes). Clipping needs the shopper's own Meijer account.
- **Reviews: first page only.** 8 written reviews plus the rating summary; reviewer nicknames, locations and ids are not returned.
- **Slow pages.** Search, category, deals, coupons and reviews can take minutes. Allow a client timeout of at least 240 seconds.

Meijer publishes no public developer API for prices. This skill reads meijer.com's public pages on request instead.

See also: for other US grocery store prices use `kroger-grocery-data`, `publix-api`, `aldi-grocery-data`, `heb-grocery-data` or `whole-foods-grocery-data`; for the cross-retailer view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Look up what an item costs at a given Meijer store, by name, Meijer id or the UPC on the package
- Compare one item's Meijer price across stores, or across Michigan, Indiana, Ohio and Illinois stores
- Check whether a Meijer store has an item in stock and in which aisle
- Get a Meijer store's current weekly ad, page by page, with each offer's price as printed (2/$6, $3.99)
- List a Meijer store's mPerks coupons, or the coupons of one department ("Baby", "Dairy")
- List the Meijer grocery sale or another deals collection at one store, with sale and regular prices
- Browse a Meijer department (produce, pantry, dairy) at one store
- Find Meijer stores near a ZIP code, with pharmacy, pickup, delivery, deli, bakery and gas station hours
- Read an item's rating summary and its first page of reviews

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every Meijer call costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/meijer/search` | Search by keywords or a Meijer id at one store: 52 items on page 1, the next 48 on page 2, with prices, stock, filter and department counts | 1 |
| `POST /api/v1/meijer/product` | One item by Meijer id or UPC / EAN at one store: price, stock, aisle, promotions, mPerks, SNAP and WIC flags, ingredients, sizes | 1 |
| `POST /api/v1/meijer/category` | One department's first 52 items at one store, with subcategories | 1 |
| `POST /api/v1/meijer/categories` | The departments and collections, or one department's subcategories | 1 |
| `POST /api/v1/meijer/deals` | One deals collection's first 52 items at one store (default the grocery sale) | 1 |
| `POST /api/v1/meijer/stores` | Stores within 50 miles of a US ZIP code (up to 50), with `store_id` | 1 |
| `POST /api/v1/meijer/store` | One store: address, phone, department hours, services, nearby stores | 1 |
| `POST /api/v1/meijer/weekly-ad` | A store's current weekly ad, page by page, every offer with its printed price | 1 |
| `POST /api/v1/meijer/coupons` | A store's mPerks coupons: the first 48 with department counts, or the full list | 1 |
| `POST /api/v1/meijer/reviews` | An item's first page of reviews (8) with the rating summary | 1 |

## Workflow

1. **Pick the store.** `/stores` with a `zip` returns the Meijer stores within 50 miles with their `store_id`. The ZIP 47274 (Seymour, IN) has no Meijer of its own; its nearest are Franklin (#295), New Albany (#220) and Jeffersonville (#167).
2. **Find the item.** `/search` with `query` and `store_id`, or `/product` with `meijer_id` (from `items[].meijer_id`) or the `upc` printed on the package. Read `price`, `regular_price`, `on_sale`, `stock_status` and, on product, `aisle`.
3. **Check the store you got.** `store_used` names the store the page used and `store_matches` says whether it is the one you asked for. Quote prices with that store.
4. **Deals.** `/weekly-ad` with `store_id` for the printed ad; `/deals` for a sale collection (`/categories` lists the collections, e.g. `black-friday`); `/coupons` for mPerks coupons.
5. **Browse.** `/categories` lists departments with the `path` that `/category` takes (`fresh/produce/fruit`, `grocery/pantry`).

## Parameters

| Parameter | Endpoint | Description |
|---|---|---|
| `query` | search | Keywords or a Meijer item id, 1-200 characters, e.g. `large eggs` |
| `store_id` | search, product, category, deals (optional); store, weekly-ad, coupons (required) | A Meijer store number (`stores[].store_id`), e.g. `295` |
| `page` | search | `1` (52 items, default) or `2` (the next 48; slower) |
| `meijer_id` | product, reviews | A Meijer item id (`items[].meijer_id`: the UPC without its check digit, leading zeros dropped). Send `meijer_id` or `upc`, not both |
| `upc` | product, reviews | A 12-digit UPC-A or 13-digit EAN as printed under the barcode, instead of `meijer_id` |
| `category` | category (required), categories (optional) | A department path as Meijer writes it (`categories[].path`) or a meijer.com department link |
| `collection` | deals | A collection path (default `grocery/grocery-sale`) or a meijer.com collection link |
| `zip` | stores | A US ZIP code |
| `department` | coupons | Only coupons in this department: `departments[].department_id` or a department or subcategory name |
| `full_list` | coupons | `true`: every coupon of the store (slower). Default: the first 48 with the total and department counts |

## Examples

### One item at one store

Request `{"meijer_id": "4125010200", "store_id": 167}`, abridged:

```json
{
  "store_requested": 167,
  "store_used": { "store_id": 167, "name": "Jeffersonville" },
  "store_matches": true,
  "meijer_id": "4125010200",
  "upc": "041250102007",
  "ean13": "0041250102007",
  "name": "Meijer Whole Milk, Gallon",
  "brand": "Meijer",
  "price": 2.99,
  "regular_price": 2.99,
  "clearance_price": null,
  "pricing_unit": "EA",
  "price_text": "$2.99",
  "on_sale": false,
  "stock_status": "inStock",
  "aisle": "B-16-52-4",
  "aisle_locations": ["B-16-52-7", "B-16-52-6", "B-16-52-5", "B-16-52-4"],
  "snap_eligible": true,
  "nutrition": null,
  "allergens": null,
  "breadcrumbs": [{ "group_id": "L1-865", "name": "Grocery" }, { "group_id": "L2-9974", "name": "Dairy" }, { "group_id": "L3-213", "name": "Milk" }]
}
```

`variations` listed the other fat contents (1% Lowfat, 2% Reduced Fat, Fat Free), each with its own price and stock at the store.

By UPC, `{"upc": "715141514643", "store_id": 224}` returned Eggland's Best Cage Free Large Brown Eggs, 12 Count at Marburg Ave (Cincinnati): `price` 3.99, `regular_price` 6.39, `on_sale` true, `savings_text` "$2.40 Off", aisle C-14-74-5.

### A multi-buy in the grocery sale

`/deals` at store 295 (Grocery On Sale, `total` 8,418, first 52 returned). One item, abridged:

```json
{
  "name": "Betty Crocker Favorites Fudge Brownie Mix, 16.3 oz",
  "price": 1.66,
  "price_text": "Buy 3 for $5.00",
  "multi_buy": { "quantity": 3, "total": 5 }
}
```

`price` is then the price of one; quote the deal as the page writes it.

### Weekly ad

`/weekly-ad` with `{"store_id": 224}`: `region` CIN, `ad` {`name` "Weekly Deals", `valid_from` 2026-11-27, `valid_to` 2026-12-01}, 35 pages, 339 blocks. Two blocks of page 1:

```json
[
  { "id": "12776272", "item": "Cottonelle Bath Tissue, Flushable Wipes or Viva Paper Towels", "price_text": "$9.99", "multi_buy": null, "has_coupons": false },
  { "id": "12776271", "item": "Meijer Party Size Potato Chips or Tortilla Chips*", "price_text": "2/$6", "multi_buy": { "quantity": 2, "total": 6 }, "has_coupons": false }
]
```

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
ENDPOINTS = f"{BASE}/api/v1/meijer"

def meijer(endpoint, body):
    r = requests.post(f"{ENDPOINTS}/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Stores near a ZIP (1 credit)
stores = meijer("stores", {"zip": "47274"})["data"]["stores"]
print([(s["store_id"], s["name"], s["address"]["city"]) for s in stores[:3]])

# 2. One item by UPC at each of those stores (1 credit each)
for s in stores[:3]:
    item = meijer("product", {"upc": "041250102007", "store_id": s["store_id"]})["data"]
    print(item["store_used"]["store_id"], item["name"], item["price"], item["stock_status"], item["aisle"])

# 3. The store's weekly ad (1 credit)
ad = meijer("weekly-ad", {"store_id": 295})["data"]
print(ad["region"], ad["ad"]["valid_from"], ad["ad"]["valid_to"], ad["block_count"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it.

- **search** - `query`, `country`, `currency`, `store_requested`, `store_used` {`store_id`, `name`}, `store_matches`, `total`, `page`, `max_page`, `count`, `has_more`, `items[]` {`position`, `meijer_id`, `upc`, `ean13`, `product_id`, `name`, `url`, `image`, `price`, `regular_price`, `clearance_price`, `pricing_unit`, `price_per_sold_by_unit`, `regular_price_per_sold_by_unit`, `clearance_price_per_sold_by_unit`, `sold_by_unit`, `avg_pricing_units_per_sold_by_unit`, `price_text`, `multi_buy`, `on_sale`, `on_clearance`, `savings_text`, `price_ends`, `deposit`, `currency`, `priced`, `stock_status`, `promotions`, `mperks`, `mperks_offer_ids`, `wic_eligible`, `sold_by_weight`, `alcohol`, `age_restricted`, `pickup_eligible`, `pickup_within_3_hours`, `home_delivery`, `marketplace`, `ships_from_third_party`, `max_order_quantity`, `sponsored`}, `facets[]` {`name`, `label`, `values[]` {`label`, `value`, `count`}}, `departments[]` {`group_id`, `name`, `count`}, `notes`.
- **product** - the store fields above, `meijer_id`, `upc`, `ean13`, `product_id`, `name`, `brand`, `short_description`, `url`, `image`, `images`, the price fields, `priced`, `price_displayed`, `stock_status`, `aisle`, `aisle_locations`, `promotions`, `mperks`, `snap_eligible`, `wic_eligible`, `sold_by_weight`, `unit_of_measure_quantity`, `alcohol`, `age_restricted`, `choking_hazard`, `pickup_eligible`, `pickup_within_3_hours`, `home_delivery`, `ships_from_third_party`, `marketplace_offers`, `max_order_quantity`, `ingredients`, `nutrition` (null), `allergens` (null), `breadcrumbs[]` {`group_id`, `name`}, `variations[]` {`name`, `options[]` {`name`, `meijer_id`, `selected`, `disabled`, `image`, `price_per_sold_by_unit`, `regular_price_per_sold_by_unit`, `stock_status`}}, `notes`.
- **category** - `category`, `group` {`group_id`, `name`, `count`}, the search list fields, `subcategories[]` {`group_id`, `name`, `count`, `path`}, `subcategory_links[]` {`name`, `path`}.
- **categories** - `category`, `count`, `categories[]` {`name`, `type` (department, collection), `path`, `group_id`, `collection_id`, `parent`, `url`}, `subcategories`, `subcategory_links`, `notes`.
- **deals** - `collection`, `collection_name`, `collection_id`, the search list fields, `departments[]`.
- **stores** - `zip`, `radius_miles`, `count`, `stores[]` {`position`, `store_id`, `name`, `address` {`street`, `city`, `state`, `zip`}, `latitude`, `longitude`, `time_zone`, `store_type`, `format`, `pickup`, `delivery`, `url`}, `notes`.
- **store** - `store_id`, `name`, `store_type`, `address`, `phone`, `latitude`, `longitude`, `features`, `hours` {`store`, `pharmacy`, `delivery`, `pickup`, `deli`, `bakery`, `gas_station`: {`title`, `phone`, `hours[]` {`days`, `hours`}, `amenities`}}, `other_sections`, `services`, `nearby_stores`, `url`, `notes`.
- **weekly-ad** - the store fields, `region`, `flyer_url`, `ad` {`ad_id`, `name`, `valid_from`, `valid_to`, `available_from`, `available_to`, `page_count`}, `ads[]` {`ad_id`, `name`, `valid_from`, `valid_to`, `image`}, `page_count`, `block_count`, `pages[]` {`page`, `image`, `starts`, `ends`, `blocks[]` {`id`, `item`, `label`, `price_text`, `multi_buy`, `has_coupons`}}, `notes`.
- **coupons** - the store fields, `full_list`, `department`, `total`, `count`, `coupons[]` {`position`, `offer_id`, `title`, `description`, `discount`, `discount_type` (amount, percent), `minimum_quantity`, `starts`, `ends`, `manufacturer_coupon`, `label`, `departments[]` {`department_id`, `name`, `subcategory`}, `image`, `terms`, `new_this_week`, `expiring_soon`, `clippable`}, `departments[]` {`department_id`, `name`, `count`, `special`, `subcategories[]`}, `notes`.
- **reviews** - `meijer_id`, `upc`, `ean13`, `url`, `name`, `rating` {`average`, `ratings_count`, `review_count`, `distribution`, `recommended` {`yes`, `no`}}, `questions` {`questions`, `answers`}, `total`, `page_size`, `offset`, `page`, `reviews[]` {`position`, `review_id`, `rating`, `rating_range`, `title`, `text`, `submitted_at`, `recommended`, `helpful_yes`, `helpful_no`, `badges`, `syndicated`, `photos`, `store_responses[]` {`department`, `date`, `response`}}, `notes`.

## Guardrails

- Name it "Meijer (meijer.com, the Midwest grocery and general-merchandise chain)" on first mention.
- Store scope: every price, stock status and aisle is one store's. Always name the store (`store_used.store_id` and `store_used.name`) next to a price, and never call one store's number "the Meijer price". If `store_matches` is false, say the page used a different store than the one asked for.
- Prices: quote `price` with its `pricing_unit` (EA each, LB pound) and the `fetched_at` time. A multi-buy is quoted as `price_text` says it ("Buy 3 for $5.00", "2/$6"); `price` is then the price of one. Never call a sale price the regular price; `regular_price` is the price without the sale.
- Weekly ad: quote `price_text` as printed; a null `price_text` means the block carries no single price (BOGO, percent off, mPerks, ranges): read the `item` and `label` text instead of inventing a number. Respect `valid_from` / `valid_to`.
- Coupons are listed, never clipped; the shopper clips them in their own Meijer account for them to apply.
- Stock: `stock_status` is the store's status when fetched (inStock, lowStock, outOfStock), not a unit count and not a promise the shelf still has it.
- Reviews: quote ratings with `ratings_count` (every rating) and `review_count` (written reviews) kept apart. Never attribute a review to a person.
- Use: keep any use descriptive - checking prices, stock, deals and coupons for a shopping or purchasing decision.
- Links and content: refer to items by name and Meijer id or UPC; do not republish Meijer's photos or product copy, and do not use the answers to copy or rebuild its catalogue.
- Not covered: search suggestions, gas prices, prescription prices, Meijer Express gas stations, nutrition panels and allergens (null), search pages beyond 2, more than the first 52 items of a department or collection, review pages beyond the first, coupon clipping, cart, ordering and checkout, price history.
- Terms: Scavio does not store Meijer data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Meijer's terms of use restrict automated access to its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, Meijer ids, UPCs, store numbers, deals or coupons. Only return what the API returned, with the store it came from.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "meijer_id or upc is required."; "Send meijer_id or upc, not both."; "upc: the check digit does not match (send the full code as printed under the barcode)."; a `store_id` that is not digits; "store_id is required" on store, weekly-ad and coupons; a ZIP that is not a US ZIP code; `page` above 2 on search, or any page other than 1 on category and deals.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: an unknown item, store number, department or collection, or a ZIP with no Meijer within 50 miles.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api).
- `502` and `503` mean Meijer data was temporarily unavailable. They are not charged.
- Search, category, deals, coupons and reviews can take minutes. Allow a client timeout of at least 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.113.0
npm install scavio@0.114.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: stores } = await scavio.meijer.stores({ zip: "47274" });
const { data: res } = await scavio.meijer.search({ query: "large eggs", store_id: 295 });
const { data: milk } = await scavio.meijer.product({ upc: "041250102007", store_id: 167 });
const { data: ad } = await scavio.meijer.weeklyAd({ store_id: 224 });
const { data: coupons } = await scavio.meijer.coupons({ store_id: 295, department: "Baby" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.meijer.search(...)`, `product`, `category`, `categories`, `deals`, `stores`, `store`, `weekly_ad`, `coupons` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_meijer`, `get_meijer_product`, `get_meijer_category`, `get_meijer_categories`, `get_meijer_deals`, `find_meijer_stores`, `get_meijer_store`, `get_meijer_weekly_ad`, `get_meijer_coupons` and `get_meijer_reviews`. Meijer is opt-in: add `meijer` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.113.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,meijer"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/meijer-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [product](https://scavio.dev/docs/meijer-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [category](https://scavio.dev/docs/meijer-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [categories](https://scavio.dev/docs/meijer-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [deals](https://scavio.dev/docs/meijer-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [stores](https://scavio.dev/docs/meijer-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [store](https://scavio.dev/docs/meijer-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [weekly ad](https://scavio.dev/docs/meijer-weekly-ad?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [coupons](https://scavio.dev/docs/meijer-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api), [reviews](https://scavio.dev/docs/meijer-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api). Platform page: [scavio.dev/meijer-api](https://scavio.dev/meijer-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=meijer-api).
