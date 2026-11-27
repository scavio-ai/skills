# Belk API - Prices, Coupons, Doorbusters, Store Availability, Reviews

Read Belk (belk.com, the US Southern department store): keyword search, category listings, the deal listings (Doorbusters, Super Buys, Clearance, Sale Items, Today's Offers), Belk's department menu, one product with every color and size variant, one variant with its UPC and sale end date, exact store units for variants at chosen stores, the stores near a US ZIP, one store, and a product's newest reviews. www.belk.com only (US, USD, English), as shown to a visitor who is not signed in. Every endpoint returns structured JSON; most calls are 2 credits.

**The job this skill is for: what an item costs at Belk today, with which deal, and which Belk store has it.** Belk prices carry several layers and this skill returns each one as Belk shows it, never computed. On 2026-11-27 the Vince Camuto Women's Dolman Sleeve Crew Neck Sweater (product `18000269151219`) read `sale_price` $29.99 against `original_price` $69, `price_label` Doorbuster, a "Spend $50, Get Lab Grown Diamond Earrings or Pendant for $49.99." promotion, 147 variants and 51 of them in stock online. Its medium Cobalt Sea variant (`0480046046048`) showed `sale_ends` 2026-11-28, `coupon_excluded` true and 293 units online, and at size M the colors were priced $20.70, $29.99 or $34.50 (`include_color_prices`). In the Women's Sweaters category a $59.50 Crown & Ivy petite sweater that was not on sale carried coupon `BFISHERE` at 60 percent off with Belk's own price with the code, `promo_price` $23.80, ending 2026-11-29T04:59Z. The second job is store stock: a Tree Hut variant showed exactly 2, 3 and 4 units at three Florida stores (status `limited`, Belk's "Only N left!"). Pair it with `macys-product-data`, `kohls-product-data` or `jcpenney-product-data` for the same brand at other department stores (match on the UPC `/variant` returns).

Eight limits shape every answer, so say them plainly:
- **Credits follow what the call spent.** 2 credits on search, category, deals, categories, stores, store and reviews. Product is 2 with Belk's canonical link and 4 with a product id or any other link (Belk redirects once). Variant is 2, or 4 with `include_color_prices`. Store availability is 1 when every `orin` is given, plus 2 per variant whose orin is looked up (3 for one variant, 5 for two, up to 11 for five). `credits_used` in the response is the truth. A not-found (`404`) is charged what it spent; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Tier prices are Belk's labels, not a member price.** `belk_rewards_tier_prices` {`insider`, `premier`, `elite`} are the Belk Rewards+ tier prices Belk shows to logged-out visitors, when it lists them (null on some products). In every capture of 2026-11-27 they equaled the sale price. Quote them as "Belk Rewards+ insider price as shown on belk.com", never as what a given shopper pays.
- **Coupons are as given.** `coupons[]` carry `code`, `discount_percent`, `promo_price` (Belk's own price with the code), `ends` and `requirement` as Belk writes them. Never compute a price from a percent; quote `promo_price`, or nothing when it is null or `price_hidden` is true.
- **60 items per page, page 1-200.** `total` can be a lower bound: `total_is_lower_bound` true means Belk shows "10,000+" (the Doorbusters list), and then `total_pages` is null.
- **Store prices are national.** Belk prices are the same in every store; store availability gives units, not a store price.
- **Exact units need the right orin.** A wrong `orin` answers 0 at every store, so pass the `orin` `/variant` returned or leave it out and it is looked up.
- **Reviews are the 8 newest.** No paging, sort or star filter (each is a `400`). `total` is the count in Belk's review block and can differ from the product's `review_count`.
- **No history, no suggestions.** Everything is the page at the moment of the call; Scavio keeps nothing. There is no search-suggestions endpoint, no weekly ad and no Belk coupon page. Poll and store your own series.

Belk has no public API for its catalog, prices or store stock. Prices and stock are shown on belk.com for each item, and this skill reads those public pages with one Scavio key.

See also: Macy's `macys-product-data`, Kohl's `kohls-product-data`, JCPenney `jcpenney-product-data`, Nordstrom `nordstrom-product-data`; the same item at Amazon `amazon-product-data` or Walmart `walmart-product-data` (match on UPC from `/variant`).

## When to trigger

Use this skill when the user asks to:
- Price an item at Belk: original price, sale price, Doorbuster or Sale label, Belk Rewards+ tier prices, coupon codes with Belk's after-code price, promotions
- Search belk.com by keyword, sorted by relevance, newest, price, top rated, discount or Doorbusters first, filtered by brand, color, size, discount band, price range, coupon code or sales promotion
- List Belk Doorbusters, Super Buys, Clearance, Sale Items or Today's Offers, across Belk or inside one department
- Browse one Belk category (Women's Sweaters, Bath & Body, Men) or read Belk's department menu
- Read one Belk product: brand, style number, details, material and care, colors, sizes and every variant's online stock
- Read one variant (a color and size): UPC, sale end date, pickup and ship eligibility, coupon exclusion, max quantity, and the price of every color at that size
- Check exact store stock for up to 5 variants at up to 10 Belk stores, or which items can be picked up free at one store
- Find Belk stores near a US ZIP with this week's hours (Thanksgiving and Black Friday hours), or one store's address, phone and pickup location
- Read the newest Belk customer reviews of a product

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most calls in this skill cost 2 credits, so 50 credits cover about 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls usually take 2-15 seconds (in the captures: stores 1.4, reviews 1.4, store 1.4, variant 1.6, category 1.7, categories 2.2, product 2.4, store availability 2.7, search 2.8, deals 3.1). Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/belk/search` | Keywords: 60 items per page with total, prices, tier prices, coupons, promotions, badge, Doorbuster and Belk Market flags, colors; facets and matching categories | 2 |
| `POST /api/v1/belk/category` | One category by path or link, same items, sorts, filters and facets as search | 2 |
| `POST /api/v1/belk/deals` | Doorbusters (default), Super Buys, Clearance, Sale Items or Today's Offers, across Belk or in one category | 2 |
| `POST /api/v1/belk/categories` | Belk's department menu: 15 departments, about 700 nodes, each with the path category takes | 2 |
| `POST /api/v1/belk/product` | One product: prices, label, coupons, promotions, details, breadcrumbs, colors, sizes, every variant with online units | 2 with Belk's canonical link, 4 otherwise |
| `POST /api/v1/belk/variant` | One variant: UPC, orin, prices, sale end date, pickup and ship flags, coupons, coupon exclusion; optionally every color's price at its size | 2, 4 with `include_color_prices` |
| `POST /api/v1/belk/store-availability` | Exact units for 1-5 variants at 1-10 stores, with Belk's status per store | 1 with every orin given, plus 2 per variant looked up |
| `POST /api/v1/belk/stores` | Every Belk store within about 150 miles of a US ZIP, nearest first, with hours and this week's hours | 2 |
| `POST /api/v1/belk/store` | One store: address, phone, coordinates, this week's hours, pickup location, events | 2 |
| `POST /api/v1/belk/reviews` | The 8 newest reviews of one product (no reviewer names) | 2 |

US only: there is no `country` parameter. Every answer carries `country` (us), `currency` (USD) and `language` (en-US).

## Prices: original, sale, tier, coupon and promotion

Every listing item, product and variant carries Belk's price layers as belk.com shows them to a visitor who is not signed in:

| Field | Meaning |
|---|---|
| `original_price` | Belk's original price (`{min, max}` on items and products, a number on a variant) |
| `sale_price` | Belk's current price (`{min, max}` across variants, or a number on a variant) |
| `on_sale` | Belk marks the item as on sale |
| `price_label` (product), `price_type` (variant) | Belk's own label: Doorbuster, Sale |
| `sale_ends` (variant) | Belk's sale end date for that variant (2026-11-28 on the Doorbuster sweater) |
| `belk_rewards_tier_prices` | `{insider, premier, elite}` Belk Rewards+ tier prices as Belk shows them to logged-out visitors, when Belk lists them; null otherwise |
| `coupons[]` | `{code, discount_percent, promo_price, ends, requirement, price_hidden}`: the coupon, Belk's own price with the code and its end date as Belk writes them |
| `coupon_excluded` (variant) | Belk excludes this variant from coupons |
| `promotions[]` | `{id, type, message}`: Belk's promotion text (PWP gift-with-purchase offers) |
| `badge`, `is_doorbuster`, `is_belk_market` | Belk's tile badge (`badge-db-buys`, `badge-new-arrival`), the Doorbuster flag and the Belk Market (third-party marketplace) flag |

- Quote "Vince Camuto Women's Dolman Sleeve Crew Neck Sweater: $29.99 at belk.com on 2026-11-27 (original $69, Doorbuster, sale ends 2026-11-28)", with the date.
- A coupon price is "Belk shows $23.80 with code BFISHERE (ends 2026-11-29T04:59Z)". Never apply `discount_percent` yourself, never stack a coupon on a tier price, and never apply a coupon to a variant with `coupon_excluded` true.
- Colors of one product can be priced differently: read `/variant` with `include_color_prices` for the color you mean before quoting a product range.
- Report Belk's prices, labels and dates and the arithmetic only. Never judge a price as a good deal and never describe how often an item goes on sale.

## Workflow

1. **Find the item.** `/search` with `query` (`sweater`), `/category` with a `path` from `/categories` (`women/womens-clothing/sweaters`), or `/deals` with a `type`. Each item's `id` is the input of product and reviews; its `url` is Belk's canonical link (2 credits on product instead of 4).
2. **One product.** `/product` with `url` (or `product_id`): read `variants[]` for each color and size with `online_units`, and `default_variant_id`.
3. **One variant.** `/variant` with `variant_id` for UPC, `orin`, `sale_ends`, `pickup_eligible`, `coupon_excluded`; add `include_color_prices` for every color's price at that size.
4. **Stores.** `/stores` with a US `zip` for `store_id`s, hours and the pickup flag; `/store` for one store's pickup location and coordinates.
5. **Store stock.** `/store-availability` with `variant_id` and `orin` (1 credit) or `items` of up to 5 `{variant_id, orin}` and `store_ids` (up to 10). Read `stores[].units` and `status`.
6. **Pickup at one store.** Add `pickup_store_id` to search, category or deals for items Belk offers for free store pickup there.
7. **Reviews.** `/reviews` with `product_id` or `url`: the 8 newest.
8. **Watching prices:** there is no history. Poll the same products or variants on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required on search | Keywords, 1-200 chars. Belk answers a query it cannot match with its closest matches |
| `category` | string | required on category | A path from `/categories` (`women/womens-clothing/sweaters`) or a belk.com category link. On deals: optional, deals inside that category |
| `type` | string | `doorbusters` | Deals only: `doorbusters`, `super_buys`, `clearance`, `sale` (Sale Items), `todays_offers` (Today's Offers) |
| `sales_promotion` | string or array | none | Search and category: `doorbusters`, `super_buys`, `sale`, `clearance`, `todays_offers`, `belk_market` (Belk Market); a list matches any |
| `sort` | string | `relevance` | `relevance`, `newest`, `price_low_to_high`, `price_high_to_low`, `top_rated`, `discount` (highest percent off first), `doorbusters_first` |
| `page` | integer | 1 | 1-200, 60 items per page |
| `brand` | string or array | none | Brands as the Brand facet spells them (`Calvin Klein`, `Michael Kors`) |
| `color` | string or array | none | Color groups (`Black`, `Blue`, `Red`) |
| `size` | string or array | none | `group/size` from the size facets (`Women's Regular/10`, `Plus/1X`, `Men's Regular/L`) |
| `coupon_code` | string or array | none | Items a Belk coupon applies to (the Coupon Eligible facet, `BFISHERE`) |
| `min_discount` | integer | none | One of Belk's discount bands: 20, 30, 40, 50, 60, 70, 80 (percent off or more) |
| `min_price`, `max_price` | number | none | USD |
| `pickup_store_id` | string or integer | none | Items available for free store pickup at this store (`stores[].store_id`) |
| `filters` | object | none | Any other facet id from a previous answer to one value or a list (`{"Gender": "Women", "Occasion": "Casual"}`), up to 8 facets |

Up to 20 values per list. Facet ids and values come from `facets[]` of an earlier answer.

### Product (`/product`) and reviews (`/reviews`)

`product_id` (`18000269151219`, an item's `id`) or `url` (a belk.com product link of the form `https://www.belk.com/p/<name>/<id>.html`), not both. Product: Belk's canonical link (`items[].url`) costs 2; a product id or another link costs 4 (`redirected` true). Reviews take no `page`, `sort` or `rating` (each is an unbilled `400`).

### Variant (`/variant`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `variant_id` | string | required | `variants[].variant_id` from `/product` (`0480046046048`) |
| `include_color_prices` | boolean | false | Also every color's price and stock flag at this variant's size (4 credits) |

### Store availability (`/store-availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `variant_id` | string | none | One variant; or send `items` |
| `orin` | string | none | The variant's `orin` from `/variant`; with it no lookup and 1 credit |
| `items` | array | none | Up to 5 `{variant_id, orin?}` instead of `variant_id` |
| `store_ids` | array or string | required | 1-10 store ids (`["452", "329", "270"]` or comma-separated) |

### Stores (`/stores`) and store (`/store`)

`/stores` takes `zip` (required, a 5-digit US ZIP); Belk answers every store within about 150 miles and takes no `radius` (an unbilled `400`); a ZIP far from any Belk answers an empty list (ZIP 10001 returned 0). `/store` takes `store_id` (required, `452`). `/categories` takes no parameters.

## Examples

### One listing item with a coupon

```bash
curl -X POST https://api.scavio.dev/api/v1/belk/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "women/womens-clothing/sweaters", "sort": "newest"}'
```

Captured `data.items[47]` (2026-11-27; `total` 2,334, 39 pages; `image` and color swatches dropped, 2 of its colors shown):

```json
{
  "position": 48,
  "id": "1804523BC2116P",
  "title": "Petite Pearl Embellished V-Neck Sweater",
  "brand": "Crown & Ivy™",
  "rating": null,
  "review_count": null,
  "original_price": { "min": 59.5, "max": 59.5 },
  "sale_price": { "min": 59.5, "max": 59.5 },
  "on_sale": false,
  "belk_rewards_tier_prices": {
    "insider": { "min": 59.5, "max": 59.5 },
    "premier": { "min": 59.5, "max": 59.5 },
    "elite": { "min": 59.5, "max": 59.5 }
  },
  "coupons": [
    {
      "code": "BFISHERE",
      "discount_percent": 60,
      "promo_price": { "min": 23.8, "max": 23.8 },
      "ends": "2026-11-29T04:59:00.000Z",
      "requirement": [],
      "price_hidden": false
    }
  ],
  "promotions": [
    { "id": "FJ_PWP_111026_112826", "type": "PWP", "message": "Spend $50, Get Lab Grown Diamond Earrings or Pendant for $49.99." }
  ],
  "badge": "badge-new-arrival",
  "is_doorbuster": false,
  "is_belk_market": false,
  "colors": [
    { "color_id": "509477140982", "name": "BLUEBERRY" },
    { "color_id": "260477140982", "name": "HEATHER OAT" }
  ]
}
```

`promo_price` $23.80 is Belk's own price with the code; quote it as given with `ends`. The answer also carries `category` {`path`, `cgid`, `name` "Women's Sweaters"}, `facets` and `categories`. `/search` `{"query": "sweater"}` answered `total` 7,193 in 120 pages, Vince Camuto's Dolman sweater first ($29.99, original $69, `badge-db-buys`, `is_doorbuster` true, 11 colors). `/deals` `{"type": "doorbusters"}` answered `total` 10000 with `total_is_lower_bound` true and `total_pages` null. An unknown category is a charged `404`: "No Belk category at <path>. Check the path (categories[].path from /belk/categories)."

### One variant with its sale end date

```bash
curl -X POST https://api.scavio.dev/api/v1/belk/variant \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"variant_id": "0480046046048"}'
```

Captured `data` (2026-11-27; `images` and `notes` dropped):

```json
{
  "country": "us",
  "currency": "USD",
  "language": "en-US",
  "variant_id": "0480046046048",
  "product_id": "18000269151219",
  "upc": "0198898333109",
  "orin": "472209216",
  "color_id": "491435457624",
  "size_id": "33903_M",
  "availability": "InStock",
  "pickup_eligible": true,
  "ship_eligible": true,
  "online_only": false,
  "dropship": false,
  "max_buy_quantity": 50,
  "price_type": "Doorbuster",
  "original_price": 69,
  "sale_price": 29.99,
  "sale_ends": "2026-11-28",
  "badge": "Doorbuster",
  "coupons": [],
  "coupon_excluded": true,
  "promotions": [
    { "id": "FJ_PWP_111026_112826", "type": "PWP", "message": "Spend $50, Get Lab Grown Diamond Earrings or Pendant for $49.99." }
  ]
}
```

With `"include_color_prices": true` (4 credits) the same size M answered `color_prices[]` {`color_id`, `price`, `price_text`, `price_type`, `out_of_stock`, `all_sizes_on_sale`}: $29.99 for most colors, $20.70 for some (out of stock) and $34.50 for one. An unknown variant is a charged `404`: "No Belk variant <id>. Check the variant id (variants[].variant_id from /belk/product)."

### Exact store units

```bash
curl -X POST https://api.scavio.dev/api/v1/belk/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"variant_id": "0480063873511", "store_ids": ["234", "345", "497"]}'
```

Captured `data.variants[0]` (2026-11-27; orin looked up, so 3 credits):

```json
{
  "variant_id": "0480063873511",
  "orin": "477438021",
  "orin_source": "looked_up",
  "product_id": "5900559B400010989",
  "upc": "0075371003233",
  "color_id": "000477438019",
  "size_id": "00000_18Ounces",
  "pickup_eligible": true,
  "price_type": "Sale",
  "original_price": 11.99,
  "sale_price": 11.99,
  "sale_ends": null,
  "in_stock_store_count": 3,
  "stores": [
    { "store_id": "234", "units": 2, "status": "limited" },
    { "store_id": "345", "units": 3, "status": "limited" },
    { "store_id": "497", "units": 4, "status": "limited" }
  ]
}
```

`status` is `in_stock` above 5 units, `limited` at 1-5 (Belk's "Only N left!") and `out_of_stock` at 0. With the orin given (`{"variant_id": "0480046046048", "orin": "472209216", "store_ids": ["270", "334", "196"]}`, 1 credit) the answer carries `orin_source` "given" and no price fields: the Dolman sweater in medium Cobalt Sea read 0, 4 and 1 units.

### Product, stores, store, categories and reviews

- `/product` `{"url": "<items[].url>"}` (2 credits): Vince Camuto Women's Dolman Sleeve Crew Neck Sweater, `style_number` 9151219, `availability` InStock, `price_label` Doorbuster, `belk_rewards_tier_prices` null, breadcrumbs Women > Women's Clothing > Sweaters > Pullover Sweaters, `details` (Product Details, Product Specifications, Material & Care), 29 colors, 7 sizes, `variant_count` 147, 51 variants in stock with 10,333 `online_units` in all. With `product_id` alone the answer has `redirected` true (4 credits). An unknown id is a charged `404`: "No Belk product <id>. Check the product id (items[].id) or link."
- `/stores` `{"zip": "28202"}`: 79 stores, Charlotte NC - Southpark first at 5.2 miles, `regular_hours` ("Mon-Thu 10:00am - 8:00pm"), `this_week_hours` Thursday Closed and Friday 6AM-10PM (`differs_from_regular` true), `pickup` true, `closed_today` true.
- `/store` `{"store_id": "452"}`: address, phone 704-364-4251, latitude and longitude, this week's hours, `pickup_location` "Mens Shoe Department", `events` null. An unknown store is a charged `404`: "No Belk store <id>. Check the store id (stores[].store_id from /belk/stores)."
- `/categories` `{}`: `count` 15 departments (Holiday Gifts, Women, Men, Kids, Shoes, Handbags, Jewelry, Beauty, Home, Bed & Bath, Brands, New & Trending, Holiday Decor, Belk Market, Clearance), `node_count` 728, each node {`name`, `path`, `url`, `cgid`, `children`}.
- `/reviews` `{"product_id": "590014100580155"}` (a philosophy body emulsion): `total` 2267, `count` 8, each {`review_id`, `rating`, `title` ("Amazing Grace!"), `text`, `date` (2026-11-13), `incentivized`}. Incentivized reviews carry Belk's promotion disclosure at the start of `text`. No reviewer names.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def belk(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/belk/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Doorbusters in women's, highest percent off first (2 credits)
deals = belk("deals", {"type": "doorbusters", "category": "women", "sort": "discount"})["data"]
item = deals["items"][0]
print(item["title"], item["original_price"], item["sale_price"], [c["promo_price"] for c in item["coupons"]])

# 2. The product by its canonical link (2 credits), then one variant (2 credits)
prod = belk("product", {"url": item["url"]})["data"]
var = belk("variant", {"variant_id": prod["default_variant_id"]})["data"]
print(var["upc"], var["sale_price"], var["sale_ends"], var["coupon_excluded"])

# 3. Stores near a ZIP (2 credits), then exact units with the orin given (1 credit)
stores = [s["store_id"] for s in belk("stores", {"zip": "28202"})["data"]["stores"][:10]]
stock = belk("store-availability", {"variant_id": var["variant_id"], "orin": var["orin"], "store_ids": stores})["data"]
for s in stock["variants"][0]["stores"]:
    print(s["store_id"], s["units"], s["status"])

# Belk prices and stock change daily. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `country`, `currency` and `language`, and most carry `notes`.

- **search / category / deals** - (`query` on search; `category` {`path`, `cgid`, `name`} on category and deals, null on deals across Belk; `type`, `belk_filter` on deals), `filters` (the filters applied), `pickup_store_id`, `title`, `page`, `page_size`, `total`, `total_is_lower_bound`, `total_pages`, `count`, `sort`, `applied_filters`, `items[]` {`position`, `id`, `title`, `brand`, `url`, `image`, `rating`, `review_count`, `original_price` {`min`, `max`}, `sale_price` {`min`, `max`}, `on_sale`, `belk_rewards_tier_prices` {`insider`, `premier`, `elite`}, `coupons[]` {`code`, `discount_percent`, `promo_price`, `ends`, `requirement`, `price_hidden`}, `promotions[]` {`id`, `type`, `message`}, `badge`, `is_doorbuster`, `is_belk_market`, `colors[]` {`color_id`, `name`, `swatch`}}, `facets[]` {`name`, `id`, `values[]` {`value`, `label`, `count`, `selected`}}, `categories[]` {`name`, `path`, `cgid`, `count`, `children`}.
- **categories** - `count`, `node_count`, `categories[]` {`name`, `path`, `url`, `cgid`, `children[]`}.
- **product** - `requested` {`product_id`, `url`}, `redirected`, `id`, `name`, `brand`, `brand_url`, `url`, `style_number`, `availability`, `original_price`, `sale_price`, `price_label`, `on_sale`, `belk_rewards_tier_prices`, `badge`, `is_doorbuster`, `coupons`, `promotions`, `rating`, `review_count`, `breadcrumbs[]` {`name`, `url`}, `details[]` {`title`, `items`}, `images` {`main`, `gallery`}, `size_chart_url`, `is_belk_market`, `dropship`, `default_variant_id`, `colors[]` {`color_id`, `name`, `image`, `swatch`, `all_sizes_on_sale`}, `sizes[]` {`size_id`, `name`}, `variant_count`, `variants[]` {`variant_id`, `color_id`, `color`, `size_id`, `size`, `online_units`, `out_of_stock`}.
- **variant** - `variant_id`, `product_id`, `upc`, `orin`, `color_id`, `size_id`, `availability`, `pickup_eligible`, `ship_eligible`, `online_only`, `dropship`, `max_buy_quantity`, `price_type`, `original_price`, `sale_price`, `sale_ends`, `badge`, `coupons`, `coupon_excluded`, `promotions`, `images`, and with `include_color_prices` `color_prices[]` {`color_id`, `price`, `price_text`, `price_type`, `out_of_stock`, `all_sizes_on_sale`}.
- **store-availability** - `store_ids`, `count`, `variants[]` {`variant_id`, `orin`, `orin_source` (given or looked_up), (when looked up: `product_id`, `upc`, `color_id`, `size_id`, `pickup_eligible`, `price_type`, `original_price`, `sale_price`, `sale_ends`), `in_stock_store_count`, `stores[]` {`store_id`, `units`, `status`}}.
- **stores** - `zip`, `count`, `stores[]` {`store_id`, `name`, `address` {`line1`, `city`, `state`, `zip`}, `distance_miles`, `phone`, `regular_hours`, `this_week_hours[]` {`day`, `hours`, `differs_from_regular`}, `pickup`, `closed_today`}.
- **store** - `store_id`, `name`, `address` {`line1`, `line2`, `city`, `state`, `zip`, `country`}, `phone`, `latitude`, `longitude`, `this_week_hours[]`, `pickup_location`, `events`.
- **reviews** - `product_id`, `total`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `date`, `incentivized`}.

## Guardrails

- Name it "Belk (belk.com, the US Southern department store)" on first mention. Belk accounts, Belk Rewards+ balances and Belk credit card offers are not read.
- Prices: quote `sale_price`, `original_price`, Belk's label and the `fetched_at` date. Prices are what a visitor who is not signed in sees on belk.com. Call `belk_rewards_tier_prices` "Belk Rewards+ tier prices as shown on belk.com", never a price a given shopper pays.
- Coupons: quote `code`, `promo_price` and `ends` exactly as given. Never compute an after-code price from `discount_percent`, never combine a coupon with a tier price or another coupon, and say when `coupon_excluded` is true.
- Store stock: quote `units` per store with the date; units change through the day. Store prices are national, so never quote a store price that differs from the online one.
- Comparing Belk with Macy's, Kohl's or Amazon: compare the same item (same UPC from `/variant`), color and size, each with its date. Never call one retailer cheaper beyond the numbers shown.
- Reviews: no reviewer names or ids are returned. Quote a review as "a Belk customer review" and say when `incentivized` is true.
- Images and copy: do not republish Belk's product images or product copy; link items by `id` or `url` instead.
- Not available: search suggestions, review paging or sorting, the weekly ad, Belk's coupon page, per-store prices, price history (poll and store), account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Belk data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Belk's terms of use restrict automated access or commercial use of its site; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, coupons, units, ids, UPCs, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "Send product_id or url, not both."; a link that is not a product page ("url must be a belk.com product link (https://www.belk.com/p/<name>/<id>.html)."); a bad category ("category must be a Belk category path (categories[].path from /belk/categories, e.g. women/womens-clothing/sweaters)."); "min_discount must be one of Belk's discount bands: 20, 30, 40, 50, 60, 70, 80 (percent off or more)."; "min_price must not be above max_price."; "filters takes at most 8 facets."; "Send items, or variant_id (+ orin), not both."; "radius is not supported: Belk answers every store within about 150 miles of the ZIP and ignores a radius."; on reviews "page is not supported: Belk serves its 8 newest reviews, with no paging, sort or star filter." (the same for `sort` and `rating`); a `sort`, `type` or `page` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged what the call spent: "No Belk product <id>. Check the product id (items[].id) or link.", "No Belk variant <id>. ...", "No Belk store <id>. ...", "No Belk category at <path>. ...", "Belk returned no listing for \"<query>\".", "Belk gives no store stock key for variant <id>.". A product without reviews and a ZIP far from any Belk answer an empty list instead. Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api).
- `502` and `503` mean Belk data was temporarily unavailable ("Belk is temporarily unavailable. Please try again." or "Belk is busy right now. Please retry in a few seconds.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.101.0
npm install scavio@0.102.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.belk.search({ query: "sweater", sort: "discount", min_discount: 50 });
const { data: grid } = await scavio.belk.category({ category: "women/womens-clothing/sweaters", coupon_code: "BFISHERE" });
const { data: deals } = await scavio.belk.deals({ type: "doorbusters", category: "women" });
const { data: menu } = await scavio.belk.categories({});
const { data: product } = await scavio.belk.product({ product_id: "18000269151219" });
const { data: variant } = await scavio.belk.variant({ variant_id: "0480046046048", include_color_prices: true });
const { data: stock } = await scavio.belk.storeAvailability({ variant_id: "0480046046048", orin: "472209216", store_ids: ["270", "334", "196"] });
const { data: near } = await scavio.belk.stores({ zip: "28202" });
const { data: store } = await scavio.belk.store({ store_id: "452" });
const { data: reviews } = await scavio.belk.reviews({ product_id: "590014100580155" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.belk.search(...)`, `category`, `deals`, `categories`, `product`, `variant`, `store_availability`, `stores`, `store` and `reviews`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_belk`, `get_belk_category`, `get_belk_deals`, `get_belk_categories`, `get_belk_product`, `get_belk_variant`, `get_belk_store_availability`, `get_belk_stores`, `get_belk_store` and `get_belk_reviews`. Belk is opt-in: add `belk` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.101.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,belk"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/belk-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [category](https://scavio.dev/docs/belk-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [deals](https://scavio.dev/docs/belk-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [categories](https://scavio.dev/docs/belk-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [product](https://scavio.dev/docs/belk-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [variant](https://scavio.dev/docs/belk-variant?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [store availability](https://scavio.dev/docs/belk-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [stores](https://scavio.dev/docs/belk-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [store](https://scavio.dev/docs/belk-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api), [reviews](https://scavio.dev/docs/belk-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api). Overview: [Belk API](https://scavio.dev/belk-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=belk-api).
