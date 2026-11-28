# Sally Beauty API - Beauty Supply Prices, Online and Store Stock, CosmoProf, Reviews

Read Sally Beauty (sallybeauty.com, the US and Canadian beauty supply chain) and CosmoProf (its professional beauty distributor), chosen by `site`: search, category and clearance listings, one product with sizes and the exact online units, the exact units per Sally Beauty store near a ZIP or postal code, store locations, search suggestions, the brand directory and reviews. As shown to a visitor who is not signed in.

**The job this skill is for: what a Sally Beauty item costs today and where it is in stock.** Every product carries the price, the regular price when a lower price applies and the running promotions; one product adds the exact count of units the site can sell online, and store stock gives the exact units at each Sally Beauty store nearby. On 2026-11-28 ion Color Defense Sulfate Free Shampoo 10.5 oz (SBS-302313) read $9.59 against $11.99, 77,098 units online, in stock at 29 of 30 stores near 90012 with 8 units at the nearest.

Six limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Four sites, one parameter.** `site` is `sally-us` (sallybeauty.com, USD, the default), `sally-ca` (sallybeauty.ca, CAD), `cosmoprof-us` (cosmoprofbeauty.com) or `cosmoprof-ca` (cosmoprofbeauty.ca). Sally Beauty UK and Ireland are a separate storefront and are not covered.
- **CosmoProf is for licensed professionals.** Its prices, availability and store stock show to signed-in professionals only, so they are null; `/store-stock` and `/reviews` refuse CosmoProf sites (`400`, not charged).
- **Stock per size.** A product with sizes is stocked per size: send a size's sku (`variations[].values[].sku`) for that size's price and units; `/store-stock` with a product that has sizes is a `400` listing them.
- **Reviews: first page only.** `/reviews` returns the rating summary, the first 8 reviews and up to 10 questions with answers; no further pages and no reviewer names. It is slower (30-120 seconds).
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Sally Beauty offers no public, self-serve API for its prices or store stock. They are shown on sallybeauty.com, and this skill reads those public pages with one Scavio key.

See also: Ulta Beauty `ulta-beauty-api`, Sephora `sephora-product-data`, CVS `cvs-product-data`, Walgreens `walgreens-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price a Sally Beauty item: price, regular price, sale and clearance flags, promotions, price per size
- Check how many units of a product the site can sell online, or which Sally Beauty stores near a ZIP or postal code have it and how many
- Search sallybeauty.com or sallybeauty.ca ("purple shampoo", "nail polish"), list a category (`hair-color`) or the clearance by department
- List the brands, find stores with hours and phone, or read the search box suggestions
- Read a product's rating summary, first reviews and questions
- Look up CosmoProf catalogue facts (sizes, UPCs, ingredients, rating) without prices

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api) - email or Google, no card required.
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
| `POST /api/v1/sallybeauty/search` | Keyword search: 24 a page, sorted and filtered by facet or price, with price, list price, promotions, rating and the facets | 1 |
| `POST /api/v1/sallybeauty/category` | One category by category id, sorted and filtered like search | 1 |
| `POST /api/v1/sallybeauty/clearance` | Clearance products: Sally Beauty by department, CosmoProf in one list | 1 |
| `POST /api/v1/sallybeauty/product` | One product: price, regular price, promotions, sizes, exact online units, specs, shipping flags | 1 |
| `POST /api/v1/sallybeauty/stores` | Stores near a ZIP / postal code or a point, with address, phone, hours and distance | 1 |
| `POST /api/v1/sallybeauty/store-stock` | The exact units of one product at each Sally Beauty store nearby (Sally Beauty only) | 1 |
| `POST /api/v1/sallybeauty/suggestions` | Search box suggestions: phrases, products, brands, popular searches | 1 |
| `POST /api/v1/sallybeauty/brands` | The brand directory (about 370 on Sally Beauty, 140 on CosmoProf) | 1 |
| `POST /api/v1/sallybeauty/reviews` | Rating summary, the first 8 reviews and up to 10 questions (Sally Beauty only, no names) | 1 |

## Workflow

1. **Find products.** `/search` with `query`, or `/category` with a category id, or `/clearance` with a `department` (`hair_care`, `hair_color`, `nails`, `tools`, `beauty`). Read `redirected_to`: the site sends some keywords to a category or a product.
2. **Narrow.** Send `filters` as `{attribute_id: value}` from `facets[]` (e.g. `{"ValueBrand": "ion"}`), `price_min` / `price_max`, `sort` (`best_match`, `price_asc`, `price_desc`, `top_rated`), and `page` up to `total_pages`.
3. **One product.** `/product` with `product_id` (`items[].product_id`, or a size's sku) or `url`.
4. **Store stock.** `/store-stock` with the product (a size's sku) and `postal_code` (or `latitude` + `longitude`), `radius` 15, 30, 50 or 100 miles.
5. **Watching prices or stock:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`.

## Parameters

| Parameter | Endpoints | Description |
|---|---|---|
| `site` | all | `sally-us` (default), `sally-ca`, `cosmoprof-us`, `cosmoprof-ca` (store-stock and reviews: Sally Beauty only) |
| `query` | search (required), suggestions (required) | Keywords, up to 200 characters (suggestions: what a shopper has typed, up to 100) |
| `category` | category (required) | A category id as the site's menu names it (`hair-color`, `shampoo`, `nails-clearance`) |
| `department` | clearance | `hair_care` (default), `hair_color`, `nails`, `tools`, `beauty`; Sally Beauty sites only |
| `sort`, `page`, `page_size`, `filters`, `price_min`, `price_max` | search, category, clearance | Sort; page 1-200; 1-24 per page; up to 6 facet filters; a price range (Sally Beauty sites) |
| `product_id`, `url` | product, store-stock, reviews | A product id or a size's sku (e.g. `SBS-302313`), or a product link on the site |
| `postal_code`, `latitude`, `longitude`, `radius` | stores, store-stock | A ZIP or Canadian postal code, or a point; 15 (default), 30, 50 or 100 miles |

## Examples

### One product

Request `{"product_id": "SBS-302313"}` (1 credit), abridged:

```json
{
  "site": "sally-us",
  "product_id": "SBS-302313",
  "master_product_id": "ION159",
  "type": "variant",
  "name": "Color Defense Sulfate Free Shampoo 10.5 oz",
  "brand": "ion",
  "price": 9.59,
  "list_price": 11.99,
  "on_sale": true,
  "availability": { "in_stock": true, "message": "In Stock", "online_units": 77098 },
  "unit": "10.5 OZ",
  "promotions": [{ "name": "20% off select hair care and men's grooming", "callout": "20% off", "details": "20% off select hair care and men's grooming. Expires 11/29/2026.", "type": "product" }],
  "rating": 4.08,
  "review_count": 1117,
  "pickup_eligible": true
}
```

### Store stock

Request `{"product_id": "SBS-302313", "postal_code": "90012"}` (1 credit): `count` 30, `in_stock_count` 29. The nearest store, abridged:

```json
{
  "store_id": "2709",
  "name": "Sally Beauty #2709",
  "address": { "line1": "2708 East First St Ste B", "city": "Los Angeles", "state": "CA", "postal_code": "90033", "country": "US" },
  "distance_miles": 2.5,
  "phone": "(323) 263-3982",
  "pickup_eligible": true,
  "stock": { "units": 8, "in_stock": true, "status": "In stock" }
}
```

### Search, CosmoProf and reviews

- `/search` `{"query": "purple shampoo"}`: `total` 107, 5 pages; first Clairol Professional Shimmer Lights Conditioning Purple Shampoo, `price_min` 9.99, `price_max` 24.99 across 3 sizes, rated 4.3 over 1,457 reviews.
- `/search` `{"query": "shampoo", "site": "cosmoprof-us"}`: `redirected_to` the shampoo category, `total` 589, prices null.
- `/product` `{"product_id": "USA-M-310006", "site": "cosmoprof-us"}`: Flourish Shampoo for Thinning Hair, `pro_only` true, `price` null, 2 sizes with their UPCs, ingredients, rated 4.3 over 1,046 reviews.
- `/reviews` `{"product_id": "SBS-345331"}`: `average_rating` 3.97, `total_reviews` 113, 8 reviews and 10 questions, no names.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def sally(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/sallybeauty/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# 1. Search (1 credit)
hits = sally("search", {"query": "purple shampoo"})["data"]
for it in hits["items"][:5]:
    print(it["product_id"], it["name"], it["price"], it["price_min"], it["price_max"], it["rating"])

# 2. Units at each store near a ZIP (1 credit)
stock = sally("store-stock", {"product_id": "SBS-302313", "postal_code": "90012"})["data"]
for st in stock["stores"][:5]:
    print(st["name"], st["distance_miles"], st["stock"]["units"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `site`, `store`, `country`, `currency` and `language`.

- **search / category / clearance** - `query` / `category` / `department`, `category_name`, `sort`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `items[]` {`position`, `product_id`, `master_product_id`, `name`, `brand`, `category`, `url`, `image`, `price`, `list_price`, `price_min`, `price_max`, `currency`, `on_sale`, `clearance`, `promotions`, `rating`, `review_count`, `variation_count`, `variation_type`, `sizes`, `pickup_eligible`, `same_day_delivery_eligible`}, `facets[]` {`name`, `attribute_id`, `values[]` {`value`, `count`, `selected`}}, `price_ranges[]`, `filters_applied`, `redirected_to` (search), `notes`.
- **product** - `product_id`, `master_product_id`, `type`, `name`, `brand`, `short_description`, `url`, `breadcrumb`, `images`, `price`, `list_price`, `price_range`, `on_sale`, `clearance` {`is_clearance`, `original_price`}, `availability` {`in_stock`, `message`, `out_of_stock_label`, `online_units`, `in_stock_date`}, `min_order_quantity`, `max_order_quantity`, `unit`, `promotions[]`, `manufacturer_sku`, `manufacturer_name`, `rating`, `review_count`, `variations[]` {`attribute`, `values[]` {`sku`, `label`, `selectable`, `selected`}}, `specs[]`, `pickup_eligible`, `same_day_delivery_eligible`, `ship_to_home`, `no_ship_states`, `notes`. CosmoProf adds `brand_url`, `upc`, `pro_only`, `ingredients`, `prop65_warning`, `badges`.
- **stores** - `center`, `radius_miles`, `count`, `stores[]` {`store_id`, `name`, `address`, `latitude`, `longitude`, `distance_miles`, `phone`, `hours[]` {`day`, `hours`}, `pickup_eligible`, `url`}, `notes`.
- **store-stock** - `product` {`product_id`, `name`, `brand`, `url`, `price`, `currency`, `online_units`}, `center`, `radius_miles`, `count`, `in_stock_count`, `stores[]` (as stores, plus `stock` {`units`, `in_stock`, `status`}), `notes`.
- **suggestions** - `query`, `count`, `phrases`, `products[]`, `brands`, `popular_searches`, `notes`.
- **brands** - `count`, `brands[]` {`name`, `slug`, `url`}, `notes`.
- **reviews** - `product_id`, `average_rating`, `total_reviews`, `rating_distribution`, `recommended`, `total`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `submitted_at`, `recommended`, `helpful_votes`, `unhelpful_votes`, `verified_purchaser`, `incentivized`, `syndicated`, `photos`, `secondary_ratings`, `brand_response`}, `total_questions`, `total_answers`, `questions[]`, `notes`.

## Guardrails

- Name it "Sally Beauty (sallybeauty.com, the US and Canadian beauty supply chain)" and "CosmoProf (its professional beauty distributor)" on first mention.
- Prices: quote `price` and `list_price` with the currency and the `fetched_at` date; say which promotion applies. Never present a CosmoProf product as priced.
- Stock: quote `online_units` as "units the site can sell online" and `stock.units` as the store's count at the fetch; both change through the day.
- Reviews: no reviewer names are returned. Quote a review as "a Sally Beauty customer review" with its rating and date, and say only the first 8 are returned.
- Use: keep any use descriptive - looking up prices, promotions, stock and reviews for shopping and price monitoring.
- Images and copy: refer to products by name and product id; do not republish the site's photos, descriptions or reviews.
- Not available: Sally Beauty UK and Ireland, CosmoProf prices and stock, review pages past the first, carts, checkout, accounts, price history (poll and store).
- Terms: Scavio does not store Sally Beauty data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Sally Beauty's terms restrict automated access to its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, stock counts or reviews. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "site must be one of: sally-us, sally-ca, cosmoprof-us, cosmoprof-ca."; "department is for Sally Beauty sites; CosmoProf has one clearance category."; "store_stock is for Sally Beauty sites (sally-us, sally-ca): CosmoProf shows store stock to signed-in licensed professionals."; a product with sizes on store-stock (the answer lists the sizes' skus).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged 1 credit: an unknown product or category id.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api).
- `502` and `503` mean the site's data was temporarily unavailable. They are not charged, so retry after a few seconds.
- Most calls take 3-20 seconds; reviews 30-120. Allow a client timeout of at least 240 seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.108.0
npm install scavio@0.109.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.sallybeauty.search({ query: "purple shampoo" });
const { data: item } = await scavio.sallybeauty.product({ product_id: "SBS-302313" });
const { data: stock } = await scavio.sallybeauty.storeStock({ product_id: "SBS-302313", postal_code: "90012" });
const { data: reviews } = await scavio.sallybeauty.reviews({ product_id: "SBS-345331" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.sallybeauty.search(...)`, `category`, `clearance`, `product`, `stores`, `store_stock`, `suggestions`, `brands` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_sallybeauty`, `get_sallybeauty_category`, `get_sallybeauty_clearance`, `get_sallybeauty_product`, `get_sallybeauty_stores`, `get_sallybeauty_store_stock`, `get_sallybeauty_suggestions`, `get_sallybeauty_brands` and `get_sallybeauty_reviews`. Sally Beauty is opt-in: add `sallybeauty` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.108.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,sallybeauty"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/sallybeauty-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [category](https://scavio.dev/docs/sallybeauty-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [clearance](https://scavio.dev/docs/sallybeauty-clearance?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [product](https://scavio.dev/docs/sallybeauty-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [stores](https://scavio.dev/docs/sallybeauty-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [store stock](https://scavio.dev/docs/sallybeauty-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [suggestions](https://scavio.dev/docs/sallybeauty-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [brands](https://scavio.dev/docs/sallybeauty-brands?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api), [reviews](https://scavio.dev/docs/sallybeauty-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api). Platform page: [scavio.dev/sallybeauty-api](https://scavio.dev/sallybeauty-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=sally-beauty-api).
