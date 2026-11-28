# Zoro API - Industrial Supply Prices, Order Multiples, Availability, Reviews

Read Zoro (zoro.com, the US online industrial and business supply store, part of Grainger): keyword, part number and Zoro number search, category and brand listings, one product with its specifications and variants, its availability status and delivery estimate, and its rating summary with the first reviews. zoro.com only (United States, USD), as shown to a visitor who is not signed in.

**The job this skill is for: what a Zoro item costs today per selling unit, and what the multiple Zoro sells it in costs.** Every item carries the price of one selling unit (`unit_price`, for each, a pack or a pair), the pieces in it, and the number of selling units Zoro sells it in multiples of with that multiple's price. On 2026-11-28 the MCR Safety BearKat BK1 clear safety glasses (Zoro G2426514, part BK110) read $1.39 each, sold in multiples of 12 for $16.68, in stock with a lead time of 1 day.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Unit price and order-multiple price, labelled.** `unit_price` is one selling unit (`price_unit` EA each, PK pack, PR pair; `package_qty` pieces in it). `order_multiple` is how many selling units Zoro sells the item in multiples of, and `order_multiple_price` the price of one such multiple; `order_multiple_price_source` says whether it is the product page's figure (`page`) or worked out by Scavio as unit price times multiple (`computed`, on listings).
- **Stock is a status, not a count.** `/availability` returns Zoro's status (In Stock) and delivery estimate; Zoro shows no unit counts, so `inventory_units` is null. Listings carry `marked_out_of_stock` and `lead_time`.
- **Two slower endpoints.** `/availability` and `/reviews` usually take 60-120 seconds and up to about 230 when Zoro is slow, and can fail; a failed call is not charged and can be retried. Allow a client timeout of at least 240 seconds. Search, category, brand and product usually take 5-60 seconds.
- **Reviews are the first page only.** `/reviews` returns the rating summary (average, histogram, recommended ratio, Pros, Cons and Best Uses counts) and the first 5 reviews the product page shows, newest first; deeper pages are not offered, and no reviewer names or locations are returned.
- **No filters or history.** Zoro's listing filters are not returned (`facets` is empty), there are no search suggestions and no UK store. Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Zoro publishes no public developer API for its catalog or prices. Prices, availability and reviews are shown on zoro.com, and this skill reads those public pages with one Scavio key.

See also: MSC Industrial Supply `msc-industrial-api` and Global Industrial `global-industrial-api` (US industrial and MRO supply), Staples `staples-ink-prices-api`, Home Depot `home-depot-product-data`, Tractor Supply `tractor-supply-prices-api`, Harbor Freight `harbor-freight-api`.

## When to trigger

Use this skill when the user asks to:
- Price a Zoro item: unit price per each, pack or pair, pack quantity, order multiple and its price, was price
- Search zoro.com by keyword ("3m n95 respirator", "safety glasses", "nitrile gloves"), by manufacturer part number or by Zoro number (`G2426514`)
- Match a catalog by part number: Zoro number, manufacturer part number and UPC
- List a Zoro category (`safety-glasses/c/6214`) or a brand (`3M`, `Mcr Safety`, `Zoro Select`), 36 per page
- Read one product: every specification with country of origin, technical guides, variants with their prices, lead time, drop-ship, LTL freight, freight cost, states Zoro does not ship to, hazmat and discontinued flags
- Check whether a Zoro item is in stock and its delivery estimate
- Read a product's rating summary and its first reviews

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

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
| `POST /api/v1/zoro/search` | Keywords, a part number or a Zoro number: 36 products per page to page 100 in Zoro's order, with total, unit price, price unit, pack quantity, order multiple and its price, key specs, lead time and shipping flags; `redirected_to` when Zoro sends the keyword to a category, brand or product | 1 |
| `POST /api/v1/zoro/category` | A category by link, path or slug + code: the same items, plus the category | 1 |
| `POST /api/v1/zoro/brand` | One brand's products by name or link: the same items | 1 |
| `POST /api/v1/zoro/product` | One product by Zoro number or link: UPC, manufacturer part number, prices, availability, every specification, documents, variants with prices, lead time and shipping limits | 1 |
| `POST /api/v1/zoro/availability` | Zoro's availability status, delivery estimate, back-order and minimum order for one product, with its price | 1 |
| `POST /api/v1/zoro/reviews` | The rating summary and the first 5 reviews the product page shows, newest first (no names) | 1 |

United States only: `country` is `us` (the default); anything else is a `400`, not charged. Every answer carries `country` (us) and `currency` (USD), and most carry `notes`.

## Prices: unit price, pack quantity and order multiple

| Field | Meaning |
|---|---|
| `unit_price` | One selling unit, in USD ($1.39 each on the safety glasses below) |
| `price_unit`, `price_unit_name` | What one selling unit is: EA each, PK pack, PR pair, ... |
| `package_qty` | Pieces in one selling unit (20 in a pack of respirators) |
| `order_multiple` | How many selling units Zoro sells the item in multiples of (12) |
| `order_multiple_price` | The price of one such multiple ($16.68 for 12) |
| `order_multiple_price_source` | `page` (the product page's figure) or `computed` (unit price times multiple, worked out by Scavio on listings) |
| `was_price` | The earlier price where Zoro shows one |

- Quote "MCR Safety BearKat BK1 clear safety glasses, Zoro G2426514: $1.39 each, sold in multiples of 12 ($16.68), on zoro.com on 2026-11-28", with the date, the selling unit and the multiple.
- Quote `unit_price` and `order_multiple_price` each with its label; say when the multiple price is computed. Never judge a price as a good deal.

## Workflow

1. **Find products.** `/search` with `query` (keywords, a part number or a Zoro number). Read `redirected_to`: Zoro sends some keywords to a category or brand page (the items are then that page's) and some part numbers to a product page (no items: ask `/product` with `redirected_to.zoro_no`).
2. **Browse.** `/category` with `category` (a link or path such as `safety-glasses/c/6214`, or `redirected_to.url`) or `slug` + `code` (`items[].categories[].code`); `/brand` with `brand` (`items[].brand`) or a brand link.
3. **Next pages.** Send `page` 2, 3, ... with the same input, up to page 100. `has_more` false means the last page.
4. **One product.** `/product` with `zoro_no` (`items[].zoro_no`) or `url`.
5. **Stock and reviews.** `/availability` and `/reviews` with the same `zoro_no` or `url`. They are slower; retry a `502` (not charged).
6. **Watching prices:** there is no history. Poll the same Zoro numbers on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and brand (`/brand`)

| Parameter | Description |
|---|---|
| `query` (search, required) | Keywords, a part number or a Zoro number, 1-200 characters |
| `category` (category) | A zoro.com category link or path (`https://www.zoro.com/safety-glasses/c/6214/` or `safety-glasses/c/6214`). Or send `slug` + `code` |
| `slug`, `code` (category) | The category's slug (`safety-glasses`) and code (`6214`, `z1`: `items[].categories[].code`), together |
| `brand` (brand, required) | A brand as Zoro names it (`3M`, `Mcr Safety`, `Zoro Select`) or a zoro.com brand link (`https://www.zoro.com/b/3M/`) |
| `page` | 1-100 (36 per page); `total_pages` gives the last one |
| `country` | `us` (default) |

### Product (`/product`), availability (`/availability`) and reviews (`/reviews`)

Send `zoro_no` (the Zoro number, G followed by digits: `items[].zoro_no`, e.g. `G2426514`) or `url` (a zoro.com product link, `https://www.zoro.com/<name>/i/<Zoro number>/`).

## Examples

### One search item

Request `{"query": "3m n95 respirator"}` (1 credit): `total` 145, `total_pages` 5, 36 items, `redirected_to` null. One item, abridged:

```json
{
  "position": 1,
  "zoro_no": "G0660974",
  "name": "N95 Disposable Respirator, 8210, Dual Headstrap, Particulate Respirator, Nose Clip, PK20",
  "brand": "3M",
  "mfr_no": "8210",
  "categories": [{ "code": "z1", "name": "Safety" }, { "code": "13", "name": "Personal Protective Equipment (PPE)" }, { "code": "4451", "name": "Masks & Respiratory Protection" }, { "code": "6901", "name": "Disposable Respirators & Dust Masks" }],
  "unit_price": 23.99,
  "price_unit": "PK",
  "price_unit_name": "pack",
  "package_qty": 20,
  "order_multiple": 1,
  "order_multiple_price": 23.99,
  "order_multiple_price_source": "computed",
  "was_price": null,
  "currency": "USD",
  "key_specs": [{ "name": "NIOSH Rating", "value": "N95" }, { "name": "Mask Shape", "value": "Molded" }, { "name": "Exhalation Valve", "value": "No" }],
  "lead_time": 3,
  "drop_ship_direct": false,
  "ltl_freight": false,
  "freight_cost": 0,
  "restricted_states": [],
  "discontinued": false
}
```

The item also carried `url`, `image` and 10 `key_specs`. The 3M Aura N95 flat-fold respirator (pack of 20) in the same search read `unit_price` 34.39 a pack with `order_multiple` 12, `order_multiple_price` 412.68.

### One product

Request `{"zoro_no": "G2426514"}` (1 credit), abridged:

```json
{
  "requested_zoro_no": "G2426514",
  "zoro_no": "G2426514",
  "name": "BearKat (BK1), Safety Glasses, Duramass Hard Coat, Clear Lens, Non-Slip Temple, Frameless",
  "brand": "Mcr Safety",
  "mfr_no": "BK110",
  "upc": "766868231108",
  "unit_price": 1.39,
  "price_unit": "EA",
  "price_unit_name": "each",
  "package_qty": 1,
  "order_multiple": 12,
  "order_multiple_price": 16.68,
  "order_multiple_price_source": "page",
  "was_price": null,
  "availability": "in_stock",
  "variant_attributes": ["Lens Color", "Lens Coating"],
  "lead_time": 1,
  "ltl_freight": false,
  "restricted_states": [],
  "hazmat": false,
  "expeditable": true
}
```

The product also carried 4 `categories` (Safety > Personal Protective Equipment (PPE) > Eye Protection > Safety Glasses), 7 images, 1 document (Technical Guide), 59 `specifications` (Country of Origin (subject to change): Taiwan, Province of China, ...) and 13 `variants`, e.g. the amber-lens BK114 at $1.79 each in multiples of 12 ($21.48, computed).

### Availability, reviews, category and brand

- `/availability` `{"zoro_no": "G4152951"}` (3M N95 8210V, pack of 10): `status` "In Stock", `delivery_estimate` "Standard delivery time is 3-5 business days from ship date. Actual delivery times may vary.", `can_back_order` false, `orderable` true, `min_order_qty` 1, `inventory_units` null, `price` {`unit_price` 16.99, `price_unit` PK, `package_qty` 10}.
- `/reviews` `{"zoro_no": "G2426514"}`: `average_rating` 4.86, `rating_count` 50, `review_count` 45, `recommended_ratio` 0.98, histogram 43 five-star and 7 four-star, Pros "Clear ear piece", Cons "No rubber nose piece"; 5 reviews, e.g. `{"rating": 5, "headline": "purchased many times", "comments": "these are used in my food manufacturing facility for workers around glass. these are great, light weight and non slip. have bought these multiple times.", "verified_buyer": true, "created_at": "2026-09-29T14:20:50.212Z"}`.
- `/category` `{"category": "safety-glasses/c/6214"}`: `total` 3,325, 93 pages of 36, first the BearKat BK1 at $1.39 each.
- `/brand` `{"brand": "Mcr Safety"}`: `total` 2,901, 81 pages, glasses sold each and gloves sold by the pair (`price_unit` PR), e.g. Ninja Ice insulated work gloves at $6.99 a pair.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def zoro(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/zoro/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Search by keyword (1 credit)
hits = zoro("search", {"query": "3m n95 respirator"})["data"]
for it in hits["items"][:5]:
    print(it["zoro_no"], it["name"], it["unit_price"], it["price_unit"], it["order_multiple"], it["order_multiple_price"])

# 2. One product by Zoro number (1 credit)
item = zoro("product", {"zoro_no": "G2426514"})["data"]
print(item["mfr_no"], item["upc"], item["unit_price"], item["order_multiple_price"], item["lead_time"])

# 3. Availability (1 credit, slower: up to about 230 s; a 502 is not charged)
stock = zoro("availability", {"zoro_no": "G2426514"})["data"]
print(stock["status"], stock["delivery_estimate"])

# Zoro prices change. Store each answer with fetched_at and run this on a
# schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `country` and `currency`.

- **search / category / brand** - `query`, `redirected_to` {`type` (category, brand, product, page), `zoro_no`, `url`, `category` {`code`, `slug`, `name`}, `brand`} and `did_you_mean` (search), `category` {`code`, `slug`, `name`, `url`} (category), `brand` and `url` (brand), `total`, `page`, `page_size` (36), `total_pages`, `has_more`, `count`, `items[]` {`position`, `zoro_no`, `name`, `brand`, `mfr_no`, `url`, `image`, `categories[]` {`code`, `name`}, `unit_price`, `price_unit`, `price_unit_name`, `package_qty`, `order_multiple`, `order_multiple_price`, `order_multiple_price_source`, `was_price`, `currency`, `key_specs[]` {`name`, `value`}, `variant_attributes`, `lead_time`, `drop_ship_direct`, `ltl_freight`, `freight_cost`, `restricted_states`, `commercial_shipping_restriction`, `discontinued`, `marked_out_of_stock`}, `facets` (empty), `notes`.
- **product** - `requested_zoro_no`, `zoro_no`, `name`, `brand`, `mfr_no`, `upc`, `url`, `categories[]` {`code`, `name`, `slug`, `url`}, the price fields above, `availability`, `images`, `documents[]` {`name`, `url`}, `specifications[]` {`name`, `value`}, `variant_attributes`, `variants[]` {`zoro_no`, `name`, `mfr_no`, `url`, `unit_price`, `price_unit`, `order_multiple`, `order_multiple_price`, `was_price`, `attributes`, `marked_out_of_stock`}, `lead_time`, `drop_ship_direct`, `ltl_freight`, `freight_cost`, `restricted_states`, `commercial_shipping_restriction`, `discontinued`, `marked_out_of_stock`, `hazmat`, `expeditable`, `notes`.
- **availability** - `zoro_no`, `name`, `brand`, `mfr_no`, `url`, `status`, `status_type`, `delivery_estimate`, `can_back_order`, `orderable`, `min_order_qty`, `inventory_units` (null: Zoro shows no unit counts), `price` {`unit_price`, `price_unit`, `package_qty`, `order_multiple`, `order_multiple_price`, `currency`}, `notes`.
- **reviews** - `zoro_no`, `name`, `average_rating`, `rating_count`, `review_count`, `recommended_ratio`, `rating_histogram` {`1`-`5`}, `properties[]` {`name` (Pros, Cons, Best Uses), `values[]` {`label`, `count`}}, `answered_questions`, `page`, `page_size` (5), `total`, `total_pages`, `has_more`, `count`, `reviews[]` {`review_id`, `rating`, `headline`, `comments`, `bottom_line`, `created_at`, `updated_at`, `verified_buyer`, `verified_reviewer`, `staff_reviewer`, `disclosure`, `helpful_votes`, `not_helpful_votes`, `media_count`}, `notes`.

## Guardrails

- Name it "Zoro (zoro.com, the US online industrial and business supply store, part of Grainger)" on first mention. Zoro accounts, carts, quotes and checkout are not read or made.
- Prices: quote `unit_price` with its selling unit and `order_multiple_price` with its multiple, in USD, with the `fetched_at` date. Say when `order_multiple_price_source` is `computed`. Never present a pack price as a piece price.
- Stock: `status`, `delivery_estimate`, `availability` and `marked_out_of_stock` are Zoro's own. Zoro shows no unit counts; never present any of them as a stock count.
- Reviews: no reviewer names or locations are returned, and only the first 5 reviews are. Quote a review as "a Zoro customer review" with its rating and date, and say the summary counts every review.
- Comparing Zoro with MSC, Global Industrial or another supplier: compare the same manufacturer part number, the same selling unit and the same date. Never call one supplier cheaper beyond the numbers shown.
- Use: keep any use descriptive - looking up an item's price, order multiple, availability and specifications for purchasing and catalog matching by part number.
- Images and copy: refer to products by Zoro number and manufacturer part number; do not republish Zoro's product photos, page copy, reviews or catalog.
- Not available: Zoro's filters, search suggestions, review pages past the first, stock counts, delivery dates for a ZIP, account pricing, the UK store, price history (poll and store), carts or checkout. This API cannot buy or request a quote.
- Terms: Scavio does not store Zoro data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Zoro's terms of use restrict automated access to its site and how its content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, availability, specifications or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "country must be us: Zoro (zoro.com) serves the United States only."; "zoro_no or url is required (a Zoro number such as G2426514, or a zoro.com product link)."; "zoro_no must be a Zoro number: G followed by digits, e.g. G2426514 ..."; "url must be a zoro.com product link: https://www.zoro.com/<name>/i/<zoro number>/."; "category (a link or path such as safety-glasses/c/6214) or slug + code is required."; "slug is required with code: ..."; "brand is required: a brand as Zoro names it, e.g. 3M or Mcr Safety (items[].brand).".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: "No Zoro product <zoro_no>.", "No Zoro category <slug>/c/<code>.", "No Zoro brand <brand>.". A search with no products is a `200` with `total` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api).
- `502` and `503` mean Zoro data was temporarily unavailable ("Zoro is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds; `/availability` and `/reviews` fail more often than the others and a retry usually answers.
- Search, category, brand and product usually take 5-60 seconds; `/availability` and `/reviews` 60-120 seconds, up to about 230. Allow a client timeout of at least 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.107.0
npm install scavio@0.108.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.zoro.search({ query: "3m n95 respirator" });
const { data: glasses } = await scavio.zoro.category({ category: "safety-glasses/c/6214", page: 2 });
const { data: mcr } = await scavio.zoro.brand({ brand: "Mcr Safety" });
const { data: item } = await scavio.zoro.product({ zoro_no: "G2426514" });
const { data: stock } = await scavio.zoro.availability({ zoro_no: "G2426514" });
const { data: reviews } = await scavio.zoro.reviews({ zoro_no: "G2426514" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.zoro.search(...)`, `category`, `brand`, `product`, `availability` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 6 endpoints as tools: `search_zoro`, `get_zoro_category`, `get_zoro_brand`, `get_zoro_product`, `get_zoro_availability` and `get_zoro_reviews`. Zoro is opt-in: add `zoro` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.107.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,zoro"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/zoro-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api), [category](https://scavio.dev/docs/zoro-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api), [brand](https://scavio.dev/docs/zoro-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api), [product](https://scavio.dev/docs/zoro-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api), [availability](https://scavio.dev/docs/zoro-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api), [reviews](https://scavio.dev/docs/zoro-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api). Platform page: [scavio.dev/zoro-api](https://scavio.dev/zoro-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=zoro-api).
