# Abercrombie & Fitch + Hollister API - Prices, Store Stock, Promotions, Reviews

Read the Abercrombie & Fitch Co. storefronts: abercrombie.com (brand `anf`: Abercrombie & Fitch, abercrombie kids, YPB) and hollisterco.com (brand `hol`: Hollister, Gilly Hicks). Keyword search, category listings and the category tree, one product with every color and size SKU and its online units, exact units per SKU in stores, the store locator and one store, the banner offers, the newest reviews and search suggestions, on 16 storefronts. Every endpoint returns structured JSON at 1 credit per call (reviews 2 without the product url).

**The job this skill is for: what a piece costs on the brand's storefront today, per color and size, and how many units are online and in each store.** On 2026-11-27 the A&F Baggy Jean (product `59359439`, collection `607722`) read $90 with a member price of $67.50 that the site labels "Black Friday Price", in 15 colors and 480 SKUs; size 31 X 32 (SKU `662258406`) had 3 units online, and the stores near New York ZIP 10001 had 4 at Flatiron and 5 at Fifth Avenue. The same day the banner offer read "A Very Abercrombie Black Friday: 25-50% Off Everything A&F*", valid 2026-11-23 to 2026-11-30 in its own footnote. The second job is the same brand abroad: a Hollister graphic hoodie read AU$93.09 on the worldwide storefront for Australia, the site's own conversion of $59.95. Pair it with `gap-old-navy-api`, `hm-api`, `uniqlo-api` or `zara-api` for the same category at other apparel brands.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit, except reviews without the product `url` (2: one extra lookup). `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`) are not.
- **Pick the brand.** `brand` `anf` (the default) or `hol`. Hollister and Gilly Hicks products are brand `hol`; an A&F id asked on `hol` is a not-found.
- **16 storefronts, each in its own currency and language.** `us`, `us_es`, `ca`, `ca_fr`, `uk`, `eu` (English, EUR), `eu_de`, `eu_fr`, `eu_es`, `eu_it`, `eu_nl`, `am` (Hong Kong, HKD), `am_zh`, `am_ja` (Japan, JPY), `wd` (worldwide), `wd_es`. `country` picks the ship-to country on the eu and wd storefronts. Category ids are per region.
- **Worldwide prices are converted.** On `wd` and `wd_es` the price is the site's own conversion from USD into the ship-to country's currency (`converted_currency` true), and `usd_price` carries the USD price. The eu storefront prices in EUR only.
- **Member prices are the site's own label.** `member_price` {`text`, `value`, `label`} is the member price the storefront shows every visitor, with its label (`Black Friday Price`). Quote it with that label, never as the price.
- **Exact units, prices national.** `online_units` on product and `units` per store on store stock are the exact counts the site shows. Prices are national (online), not per store.
- **Reviews are the 8 newest.** The product page shows the 8 newest reviews; no deeper pages, other sorts or star filters. The full rating summary comes with product. Reviews work on us, ca, uk, eu and eu_de.
- **No history, no UPCs.** Everything is the storefront at the moment of the call; Scavio keeps nothing. No UPC or EAN is published. Poll and store your own series.

Abercrombie & Fitch Co. has no public API for its catalog, prices or inventory. Prices, stock and stores are shown on its storefronts, and this skill reads that public storefront data with one Scavio key.

See also: Gap, Old Navy and Banana Republic `gap-old-navy-api`; H&M `hm-api`; Uniqlo `uniqlo-api`; Zara `zara-api`; ASOS `asos-api`; American department stores `macys-product-data`, `kohls-product-data`, `nordstrom-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price an Abercrombie & Fitch, abercrombie kids, YPB, Hollister or Gilly Hicks product per color and size, with the original, was and discount text and the member price the site shows
- Check how many units of a size are online, or at the A&F or Hollister stores near a US ZIP or a point, and whether a size is backorderable and from when
- Search abercrombie.com or hollisterco.com by keyword, or list a category, sorted by newest, price, rating or best selling and filtered by gender, color family, size, style or any facet
- Compare one product's price across storefronts (US, Canada, UK, the EU, Hong Kong, Japan, a worldwide ship-to country)
- Read the banner offers a storefront shows now and the footnote terms and dates behind them
- Read the category tree of a storefront, including each department's clearance category
- Find A&F or Hollister stores near a place, with this week's hours, or one store's next 7 days
- Read the newest reviews of a product with fit rating and incentivized flags, or its rating summary
- Get the storefront's search suggestions for a few letters

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 1 credit (reviews without the product url 2), so 50 credits cover about 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Most calls take 2-6 seconds (in the captures: stores 2, suggestions 2.4, the category tree 2.9, product 3.3, store 3.4, a category 3.7, store stock 4.2, search 5.6); reviews take about 20. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/abercrombie/search` | Keyword search, 48 per page, 6 sorts, facets with counts and filter values | 1 |
| `POST /api/v1/abercrombie/product` | One product: every color with price, member price, fabric, care, measurements and every size SKU with exact online units and status; the rating summary | 1 |
| `POST /api/v1/abercrombie/store-stock` | Exact units of 1-10 SKUs at the stores near a US ZIP or a point, with status and each store's hours | 1 |
| `POST /api/v1/abercrombie/stores` | Stores of the brand near a US ZIP or a point, nearest first, with this week's hours | 1 |
| `POST /api/v1/abercrombie/store` | One store by store number, with 7 dated days of hours | 1 |
| `POST /api/v1/abercrombie/category` | One category's products, 1-90 per page, 6 sorts, facets | 1 |
| `POST /api/v1/abercrombie/categories` | The category tree of one storefront (regular, clearance and featured categories) | 1 |
| `POST /api/v1/abercrombie/promotions` | The banner offers the storefront shows now, with their footnote terms and dates | 1 |
| `POST /api/v1/abercrombie/reviews` | The 8 newest reviews of a product with the rating summary; no reviewer names | 1 with `url`, 2 without |
| `POST /api/v1/abercrombie/suggestions` | The storefront's search suggestions for a few letters | 1 |

Every answer carries `brand`, `brand_name`, `storefront`, `country` and `language`; listing and product answers add `currency` and `converted_currency`.

## Prices and stock

Every listing product and every product color carries `price` {`text` (as shown: `$90`, `AU$93.09`), `current`, `original`, `was`, `discount_text`, `flag` (`regular` or the site's sale flag)}, `member_price` {`text`, `value`, `label`} or null, `promo_message` (`50% Off! Price As Marked`), `badges` (`Top Rated`) and, on categories, `social_proof` (the site's own text, `567 people purchased`). On wd, `usd_price` {`original`, `current`}.

Each product color carries `item_numbers` {`kic`, `store`, `web`}, `fabric`, `care`, `measurements`, `final_sale`, `max_purchase_qty`, `sku_count`, `in_stock_skus` and `skus[]` {`sku`, `size` (`31 X 32`), `size_primary`, `size_secondary`, `online_units` (exact), `status` (`available`, `unavailable`, ...), `preorder`, `price`, `member_price`}.

Store stock per store: `stock[]` {`sku`, `units` (exact), `status` (`available`, `backorderable`, `unavailable`), `available_date`, `available_label` (`Today`)}.

- Quote "A&F Baggy Jean, medium wash, 31 X 32: $90 at abercrombie.com (us) on 2026-11-27; member price $67.50 (Black Friday Price)", with the storefront and date.
- A banner offer (`25-50% Off Everything A&F*`) is the storefront's text; never apply it to a price yourself. Sale prices show on the product as `discount_text` and `flag`.
- Report the storefront's prices, labels and counts as given and the arithmetic only. Never judge a price as a good deal and never describe how often a size is in stock.

## Workflow

1. **Find the product.** `/search` with `query` (`baggy jeans`) and `brand`; or `/categories` then `/category` with a `category_id` from that storefront. Each product's `product_id` and `collection_id` are the inputs of product and reviews.
2. **Colors, sizes and online units.** `/product` with `product_id` (and `collection_id`, which saves a lookup). Each color is its own `product_id`; read `colors[].skus[]` for `online_units` and `status`.
3. **Store units.** `/store-stock` with up to 10 SKUs from `colors[].skus[].sku` and a `zip` or `latitude` + `longitude` (`radius`, `unit`, `limit` optional). `/stores` lists the stores alone, and `/store` one store with dated hours.
4. **Abroad.** The same `product_id` on another `storefront` (and `country` on eu or wd). Category ids differ per region: list them with `/categories` on that storefront.
5. **Offers.** `/promotions` for the banner offers and their footnotes (`valid_from`, `valid_to` where the footnote states full dates).
6. **Reviews.** `/reviews` with `product_id` and the product `url` (1 credit; 2 without it).
7. **Watching prices or stock:** there is no history. Poll the same products or SKUs on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Market (search, product, category, categories, promotions, reviews, suggestions)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | `anf` | `anf` (abercrombie.com: Abercrombie & Fitch, abercrombie kids, YPB) or `hol` (hollisterco.com: Hollister, Gilly Hicks) |
| `storefront` | string | `us` | `us`, `us_es` (US in Spanish), `ca`, `ca_fr`, `uk`, `eu` (English, EUR), `eu_de`, `eu_fr`, `eu_es`, `eu_it`, `eu_nl`, `am` (Hong Kong, HKD), `am_zh` (Hong Kong, Traditional Chinese), `am_ja` (Japan, JPY), `wd` (worldwide, prices converted from USD), `wd_es` (worldwide in Spanish) |
| `country` | string | storefront default | Two-letter ship-to country on eu, eu_ storefronts and wd / wd_es (`DE`, `SE`, `AU`, `IL`); `eu_de` ships to DE, AT, CH; `eu_fr` to FR, BE, LU; `eu_nl` to NL, BE. Other storefronts ship to one country. Mexico, Saudi Arabia, Qatar, Indonesia and Taiwan are served by franchise partners' own sites and are refused |

### Search (`/search`) and category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required on search | Keywords, 1-100 chars |
| `category_id` | string | required on category | A category id from `/categories` on the same storefront (`12236`, US Men's Jeans) |
| `sort` | string | `best_match` | `best_match`, `newest`, `price_asc`, `price_desc`, `rating`, `best_selling` |
| `facets` | array | none | Up to 20 filters as `<facet id>:<value>` (`facets[].values[].filter` of an answer): `gender:Men's`, `colorFamily:Black`, `sizes:M` |
| `page` | integer | 1 | 1-200 (search 48 per page) |
| `page_size` | integer | 90 | Category only: 1-90 products per page |

### Product (`/product`) and reviews (`/reviews`)

`product_id` (required, 5-12 digits, `59359439`). Product: `collection_id` (optional, saves a lookup). Reviews: `url` (optional, the product link from a search or product answer; 1 credit with it, 2 without).

### Store stock (`/store-stock`), stores (`/stores`) and store (`/store`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | `anf` | `anf` (A&F and abercrombie kids stores) or `hol` (Hollister and Gilly Hicks stores) |
| `country` | string | `US` | Store country: US, CA, GB, the EU countries, JP, HK, MO, CN, AE |
| `zip` | string | one place | A US ZIP (US stores), placed at its US Census centroid |
| `latitude`, `longitude` | number | one place | A point (required outside the US) |
| `radius` | integer | 50 | 1-250 |
| `unit` | string | `mi` in the US, `km` elsewhere | `mi` or `km` |
| `limit` | integer | 10 | 1-25 stores, nearest first |
| `skus` | array | required on store-stock | 1-10 SKUs (`colors[].skus[].sku`) |
| `store_number` | string | required on store | A store number (`stores[].store_number`, `11958`) |

### Suggestions (`/suggestions`)

`query` (required, 1-100 chars) plus the market fields.

## Examples

### Product with every SKU

```bash
curl -X POST https://api.scavio.dev/api/v1/abercrombie/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "59359439", "collection_id": "607722"}'
```

Captured `data` (2026-11-27; sizes, breadcrumbs, the star distribution, images, care, per-SKU prices and 14 of 15 colors dropped, 2 of 32 SKUs shown):

```json
{
  "brand": "anf",
  "brand_name": "Abercrombie & Fitch",
  "storefront": "us",
  "country": "US",
  "language": "en-US",
  "currency": "USD",
  "converted_currency": false,
  "product_id": "59359439",
  "collection_id": "607722",
  "is_sold_out": false,
  "size_headings": { "primary": "Waist", "secondary": "Length" },
  "reviews_summary": { "average": 4.8, "count": 3822, "fit": "true to size" },
  "color_count": 15,
  "sku_count": 480,
  "colors": [
    {
      "product_id": "59359439",
      "name": "Baggy Jean",
      "color": "medium wash",
      "color_family": "Blue",
      "department": "men's",
      "gender": "M",
      "item_numbers": { "kic": "KIC_131-5149-00372-280", "store": "131-618-00372-280", "web": "607722/131-5149-00372-280" },
      "short_description": "Rigid Denim",
      "fabric": "Pocket Bag:65% Polyester, 35% Cotton / Body:100% Cotton",
      "measurements": { "measured_size": "32", "leg_opening_circumference": "20.00\"", "front_rise": "13.00\"" },
      "final_sale": false,
      "max_purchase_qty": 5,
      "badges": ["Top Rated"],
      "price": { "text": "$90", "current": 90, "original": 90, "was": null, "discount_text": null, "flag": "regular" },
      "member_price": { "text": "$67.50", "value": 67.5, "label": "Black Friday Price" },
      "url": "https://www.abercrombie.com/shop/us/p/baggy-jean-59359439",
      "sku_count": 32,
      "in_stock_skus": 28,
      "skus": [
        { "sku": "662258406", "size": "31 X 32", "size_primary": "31", "size_secondary": "32", "online_units": 3, "status": "available", "preorder": false },
        { "sku": "662257358", "size": "33 X 30", "size_primary": "33", "size_secondary": "30", "online_units": 0, "status": "unavailable", "preorder": false }
      ]
    }
  ]
}
```

Each SKU also carries its `price` and `member_price`. Another medium-wash color (`63328338`) read the same $90 with a member price of $45, and its 33 X 32 had 230 units online. A sold-out or unpublished product answers `is_sold_out` true with empty colors; an unknown product id is a charged `404` that names the brand and storefront.

### Store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/abercrombie/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10001", "skus": ["662258406", "662258414"]}'
```

Captured `data` (2026-11-27; 1 of 10 stores shown, hours shortened, notes dropped):

```json
{
  "brand": "anf",
  "brand_name": "Abercrombie & Fitch",
  "country": "US",
  "zip": "10001",
  "latitude": 40.751,
  "longitude": -73.997,
  "radius": 50,
  "unit": "mi",
  "skus": ["662258406", "662258414"],
  "total": 10,
  "count": 10,
  "stores": [
    {
      "store_number": "11113",
      "name": "Flatiron",
      "brand": "anf",
      "address": { "street": "139 5th Ave", "city": "New York", "state": "NY", "postal_code": "10010", "country": "US" },
      "distance": 0.83,
      "distance_unit": "mi",
      "phone": "332-910-9744",
      "hours": [ { "day": "monday", "open": "10:00", "close": "19:00", "closed": false } ],
      "messages": [],
      "stock": [
        { "sku": "662258406", "units": 4, "status": "available", "available_date": null, "available_label": "Today" },
        { "sku": "662258414", "units": 3, "status": "available", "available_date": null, "available_label": "Today" }
      ]
    }
  ]
}
```

Fifth Avenue (`11482`, 1.27 mi) had 5 and 5. `units` are the exact units the store shows; a backorderable SKU carries `available_date`. Store phone numbers are public business contact data.

### Search on the worldwide storefront

```bash
curl -X POST https://api.scavio.dev/api/v1/abercrombie/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "hol", "storefront": "wd", "country": "AU", "query": "hoodie"}'
```

Captured `data.products[0]` (2026-11-27; `total` 559, 12 pages of 48, `currency` AUD, `converted_currency` true; url and colors dropped):

```json
{
  "product_id": "61997359",
  "collection_id": "649280",
  "name": "Paris Saint-Germain F.C. Graphic Hoodie",
  "department": "men's",
  "gender": "M",
  "online_available": true,
  "descriptors": [],
  "badges": [],
  "price": { "text": "AU$93.09", "current": 93.09, "original": 93.09, "was": null, "discount_text": null, "flag": "regular" },
  "member_price": null,
  "promo_message": null,
  "usd_price": { "original": 59.95, "current": 59.95 }
}
```

On `us` with brand `anf`, `{"query": "baggy jeans"}` read `total` 1,219 (26 pages): the Baggy Jean at $90 (member $67.50) first, then the Ultra Baggy Jean at $90 with a member price of $45 and `promo_message` "50% Off! Price As Marked". Facets came as `gender` (Shop By), `logos` (Logo Type), `colorFamily`, `sizes` and more, each value with its `filter`. An empty search is a charged `404`: "Nothing matched this search."

### Category, categories, promotions, stores, store, reviews, suggestions

- `/category` `{"category_id": "12236", "page_size": 24}`: Men's Jeans, `total` 86, 4 pages of 24; the Relaxed Jean at $80 with member price $60 (Black Friday Price), and the Relaxed Straight Jean at $80 with `social_proof` "567 people purchased". Sale and Black Friday landing categories list no products: use a department's clearance category. An unknown id is a charged `404`: "The Abercrombie & Fitch us storefront has no category <id>. ..."
- `/categories` `{"storefront": "uk"}`: root `10001`, 71 nodes; New, then Women's with featured categories (Holiday Outfits, Party Collection). Each department's clearance category has `type` clearance.
- `/promotions` (us): 2 offers - "A Very Abercrombie Black Friday: 25-50% Off Everything A&F*" (`valid_from` 2026-11-23, `valid_to` 2026-11-30, footnote "Offer valid in stores and online November 23, 2026 to November 30, 2026 in US/CA. Excludes 3rd party branded product, clearance, and gift cards. ...") and "Free Standard Shipping and Handling On All Orders Over $99^".
- `/stores` `{"brand": "hol", "zip": "43215"}`: 3 Hollister stores in Columbus, Easton Town Center (7.71 mi) first, then Polaris Fashion Place, with this week's hours.
- `/store` `{"store_number": "11958"}`: Northpark Center, Dallas, with hours dated 2026-11-27 (Today, 10am-9pm) onward for 7 days. An unknown number is a charged `404`: "No store <n>. Check store_number (stores[].store_number) and country."
- `/reviews` `{"product_id": "59359439"}`: `total` 3,676, the 8 newest; `summary` {`average` 4.81, `recommended_count` 2,602, `fit_average` 3.09}; each review with `rating`, `title` ("Great jeans"), `text`, `submitted_at`, `recommended`, `incentivized` (true on both shown), `syndicated`, `language`, `fit_rating`, `ratings` ({`quality`: 5}) and `brand_responses`. No reviewer names.
- `/suggestions` `{"query": "hoo"}`: 10 (hoodie, hoodies & sweatshirts, ...).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def anf(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/abercrombie/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. One product: every color with price, member price and SKU online units (1 credit)
p = anf("product", {"product_id": "59359439", "collection_id": "607722"})["data"]
color = p["colors"][0]
mp = color["member_price"]
print(color["color"], color["price"]["text"], mp and (mp["text"], mp["label"]))
skus = [s["sku"] for s in color["skus"] if s["status"] == "available"][:10]

# 2. Exact units of those SKUs at stores near a ZIP (1 credit)
st = anf("store-stock", {"zip": "10001", "skus": skus})["data"]
for store in st["stores"]:
    print(store["name"], store["distance"], [(x["sku"], x["units"], x["status"]) for x in store["stock"]])

# 3. The same product on the UK storefront (1 credit)
uk = anf("product", {"product_id": "59359439", "storefront": "uk"})["data"]
print(uk["currency"], uk["colors"][0]["price"]["text"] if uk["colors"] else "sold out on uk")

# Prices and units change: store each answer with fetched_at and run this on a
# schedule; that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the storefront data when the request asks for it. Every `data` carries `brand`, `brand_name` and `notes`, and the market fields above.

- **search / category** - `query` or `category_id`, `name`, `title`, `breadcrumbs` (category), `sort`, `facets_applied`, `currency`, `converted_currency`, `page`, `page_size`, `total`, `total_pages`, `count`, `has_more`, `sort_options[]` {`id`, `name`}, `facets[]` {`id`, `name`, `values[]` {`name`, `count`, `selected`, `filter`}}, `products[]` {`product_id`, `collection_id`, `name`, `department`, `gender`, `url`, `online_available`, `descriptors`, `badges`, `price`, `member_price`, `promo_message`, `image`, `colors[]` {`name`, `product_id`}, `social_proof` (category), `usd_price` (wd)}.
- **product** - `currency`, `converted_currency`, `product_id`, `collection_id`, `is_sold_out`, `size_headings`, `sizes`, `breadcrumbs`, `reviews_summary` {`average`, `count`, `distribution`, `fit`}, `color_count`, `sku_count`, `colors[]` {`product_id`, `name`, `color`, `color_family`, `department`, `gender`, `item_numbers`, `short_description`, `fabric`, `care`, `measurements`, `final_sale`, `max_purchase_qty`, `badges`, `price`, `member_price`, `url`, `images`, `sku_count`, `in_stock_skus`, `skus[]` {`sku`, `size`, `size_primary`, `size_secondary`, `online_units`, `status`, `preorder`, `price`, `member_price`}}.
- **store-stock / stores** - `country`, `zip`, `latitude`, `longitude`, `radius`, `unit`, `skus` (store-stock), `total`, `count`, `stores[]` {`store_number`, `name`, `brand`, `brand_name`, `address` {`street`, `city`, `state`, `postal_code`, `country`}, `distance`, `distance_unit`, `phone`, `latitude`, `longitude`, `hours[]` {`day`, `open`, `close`, `closed`}, `messages`, `stock[]` (store-stock) {`sku`, `units`, `status`, `available_date`, `available_label`}}.
- **store** - `store_number`, `name`, `address`, `phone`, `latitude`, `longitude`, `hours[]` {`date`, `label`, `open`, `close`, `closed`}.
- **categories** - `root_category_id`, `count`, `categories[]` {`category_id`, `name`, `url`, `type` (regular, clearance, featured), `children[]`}.
- **promotions** - `count`, `offers[]` {`text`, `markers`, `valid_from`, `valid_to`, `terms`}, `terms[]` {`marker`, `text`, `dates`, `valid_from`, `valid_to`}.
- **reviews** - `product_id`, `sort` (newest), `total`, `count`, `summary` {`average`, `count`, `distribution`, `recommended_count`, `not_recommended_count`, `fit_average`}, `reviews[]` {`id`, `rating`, `title`, `text`, `submitted_at`, `recommended`, `incentivized`, `syndicated`, `language`, `fit_rating`, `ratings`, `helpful_yes`, `helpful_no`, `brand_responses`}.
- **suggestions** - `query`, `count`, `suggestions` (strings).

## Guardrails

- Name it "Abercrombie & Fitch (abercrombie.com)" or "Hollister (hollisterco.com)" on first mention, with the storefront when it is not us.
- Prices: quote `price.text` or `current` with `original` or `was` where given, the storefront, the currency and the `fetched_at` date. Quote `member_price` only with its `label`, as the price the site shows for members, never as the price.
- Worldwide storefront: say the price is the site's conversion from USD and give `usd_price` alongside.
- Offers: banner offers and footnotes are the storefront's text as given; never compute a price after an offer.
- Stock: quote `online_units` and store `units` as the counts at the time of the call. Never promise a unit will still be there.
- Reviews: the 8 newest only; no reviewer names are returned. Quote a review as "an Abercrombie & Fitch customer review" (or Hollister), and say when it is marked incentivized.
- Not available: UPCs or EANs, review paging, sorting or star filters, franchise-partner countries (Mexico, Saudi Arabia, Qatar, Indonesia, Taiwan), local currencies on the eu storefront, price history (poll and store), carts or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Abercrombie & Fitch Co. data: each call fetches the public storefront data at the moment the request asks for it and returns what it shows as JSON, with no response cache. Abercrombie & Fitch Co.'s terms of use cover how its sites may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, units, SKUs, product, collection, category or store ids, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "country must be a two-letter country code (e.g. DE, AU)."; a franchise-partner country ("Mexico is served by a franchise partner's own site (abercrombie.com.mx), not by this storefront."); "storefront <s> does not ship to <c>. It ships to: ..."; "product_id must be an Abercrombie & Fitch or Hollister product id (digits, e.g. 59359439: products[].product_id in search answers or the number at the end of a product link)."; "category_id must be a category id (digits, e.g. 12236: the categories endpoint lists them per storefront)."; "facets[0] must be <facet id>:<value>, e.g. colorFamily:Black or sizes:M (facets[].values[].filter in search answers)."; "skus takes at most 10 SKUs."; "zip must be a 5-digit US ZIP code."; "latitude and longitude go together."; "Send a place: zip, or latitude and longitude."; "country must be a store country: ..."; reviews on a storefront without them ("Reviews are not shown on the <s> storefront's product pages. Reviews work on: us, ca, uk, eu, eu_de."); a `url` that is not a product link of the brand's site; a `sort`, `page` or `page_size` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Nothing matched this search.", an unknown product ("Abercrombie & Fitch (us) has no product <id>: the id is unknown, or the product is not published on this storefront ..."), "The Abercrombie & Fitch us storefront has no category <id>. ...", "No stores near this place.", "No store <n>. Check store_number (stores[].store_number) and country.", "This storefront shows no promotions.", "No suggestions for this text.". Check the `brand`: Hollister and Gilly Hicks are `hol`. Take ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api).
- `502` means the storefront data was temporarily unavailable ("Abercrombie & Fitch is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.101.0
npm install scavio@0.102.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.abercrombie.search({ query: "baggy jeans", facets: ["gender:Men's"] });
const { data: jean } = await scavio.abercrombie.product({ product_id: "59359439", collection_id: "607722" });
const { data: units } = await scavio.abercrombie.storeStock({ zip: "10001", skus: ["662258406"] });
const { data: near } = await scavio.abercrombie.stores({ brand: "hol", zip: "43215" });
const { data: store } = await scavio.abercrombie.store({ store_number: "11958" });
const { data: jeans } = await scavio.abercrombie.category({ category_id: "12236", sort: "price_asc" });
const { data: tree } = await scavio.abercrombie.categories({ storefront: "uk" });
const { data: offers } = await scavio.abercrombie.promotions({ brand: "anf" });
const { data: reviews } = await scavio.abercrombie.reviews({ product_id: "59359439", url: "https://www.abercrombie.com/shop/us/p/baggy-jean-59359439" });
const { data: typed } = await scavio.abercrombie.suggestions({ query: "hoo" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.abercrombie.search(...)`, `product`, `store_stock`, `stores`, `store`, `category`, `categories`, `promotions`, `reviews` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 10 endpoints as tools: `search_abercrombie`, `get_abercrombie_product`, `get_abercrombie_store_stock`, `get_abercrombie_stores`, `get_abercrombie_store`, `get_abercrombie_category`, `get_abercrombie_categories`, `get_abercrombie_promotions`, `get_abercrombie_reviews` and `get_abercrombie_suggestions`. Abercrombie & Fitch is opt-in: add `abercrombie` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.101.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,abercrombie"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/abercrombie-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [product](https://scavio.dev/docs/abercrombie-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [store stock](https://scavio.dev/docs/abercrombie-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [stores](https://scavio.dev/docs/abercrombie-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [store](https://scavio.dev/docs/abercrombie-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [category](https://scavio.dev/docs/abercrombie-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [categories](https://scavio.dev/docs/abercrombie-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [promotions](https://scavio.dev/docs/abercrombie-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [reviews](https://scavio.dev/docs/abercrombie-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api), [suggestions](https://scavio.dev/docs/abercrombie-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api). Overview: [Abercrombie & Fitch API](https://scavio.dev/abercrombie-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=abercrombie-hollister-api).
