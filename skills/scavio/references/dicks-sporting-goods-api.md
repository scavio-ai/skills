# Dick's Sporting Goods API - Clearance, Per-Size Prices, Store Stock

Search Dick's Sporting Goods (dickssportinggoods.com, US only, prices in USD) by keyword, or browse a category by its page path, URL or id, one brand by name, or one of the deal lists (Clearance, Sale, This Week's Deals). A page holds 48 products by default and up to 144. Sort by relevance, top sellers, savings (biggest discount first), price, featured (the site's merchandised order), new arrivals or brand A-Z; filter by brand, an approximate price range, or any facet value the response lists (gender, shoe size, color, customer rating, sale...). Each item carries the id, the SKU the tile shows, title, brand, URL, image, the current price range, the list price range, percent off, a flag for prices Dick's shows only in the cart, rating, review count, badge, SKU count, its options (every color), whether Dick's pinned it to the top of the list, and `scheduled_prices`: the offer-price windows Dick's has planned for it. Read one product with its description, specs, attributes, category, rating, review and question counts, its price block, and every SKU with its own price, list price, percent off, clearance flag, UPC and online units (sizes and colors are priced separately, so one color can be on clearance while the rest sell at full price). Or read a fast style-level summary of up to 5 products in one call. Check up to 20 SKUs at up to 100 Dick's, Golf Galaxy or Public Lands stores near a ZIP, with the units each store can sell, its address, phone and weekly hours. Read the 15 newest reviews of a product with its rating statistics, and pull the search box's suggestions. All 9 endpoints return structured JSON: 1 credit each, `/product` and `/reviews` 2.

See also: for JCPenney clearance, coupons and store unit counts use the `jcpenney-product-data` skill; for Kohl's use `kohls-product-data`; for Decathlon outside the US use `decathlon-product-data`; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Track Dick's clearance: list the Clearance deals (optionally one brand, gender, size or price range), sort by savings, and detect new markdowns between runs
- Find which sizes or colors of a Dick's product are on clearance and which are still at full price
- Build a Dick's price tracker or sale alert: poll products (up to 5 per call for 1 credit) or listings and detect a price drop or a new clearance price
- Check whether a Dick's item (one size and color) is in stock at the Dick's, Golf Galaxy or Public Lands stores near a ZIP, and how many units each store has
- Search Dick's for a product and compare prices, percent off, ratings and brands, or browse a category (men's running shoes, golf drivers, kayaks...) or a brand's whole Dick's catalog
- Prepare a Dick's Black Friday or This Week's Deals watch list
- Gather the evidence for a price-match request: the Dick's price, the product URL and the time it was read
- Read what Dick's customers said most recently about a product, with the star distribution, recommend counts and fit / comfort averages
- Get Dick's search suggestions for keyword research

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most endpoints in this skill cost 1 credit and `/product` and `/reviews` cost 2, so the free credits cover 50 listing calls or 25 product reads.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. The seven 1-credit endpoints answered in 2.5 to 16 seconds in the captures (store availability about 3, suggestions about 4, products about 6, listings 10-16); allow a client timeout of at least 90 seconds for them. `/product` and `/reviews` read the full product page and take much longer: usually 20-75 seconds, up to about 2.5 minutes when the call is retried for you (the captures below took 29 and 61 seconds). Set a client timeout of at least 180 seconds for those two and run them one at a time.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/dicks/search` | 1 | 48 products per page by default (up to 144): id, `sku`, title, brand, URL, image, `price`, `price_max`, `list_price`, `list_price_max`, `percent_off`, `map_price_applies`, rating, review count, `badge`, `sku_count`, `options`, `is_pinned`, `scheduled_prices[]`. Plus `did_you_mean`, `redirected_to`, `category`, total, page, page size, total pages, sort, count, `applied_filters`, `facets[]` with values and counts, and `categories[]` the results fall in |
| `POST /api/v1/dicks/category` | 1 | One category by `path` (`/f/mens-running-shoes`), `url` or `category_id`, in the site's featured order by default: the same grid as search plus the category's id, name, path and URL |
| `POST /api/v1/dicks/brand` | 1 | Every product of one brand by name (`"YETI"`, `"Nike"`, `"Callaway"`), optionally narrowed by a keyword: the same grid as search plus the brand as Dick's writes it |
| `POST /api/v1/dicks/deals` | 1 | A deal list by `type`: `clearance` (default), `sale` or `weekly_deals` (This Week's Deals), in the featured order by default: the same grid as search plus the list's label |
| `POST /api/v1/dicks/product` | 2 | One product by `product_id` or `url`: title, brand, description, features, specs, attributes, product type, category, images, rating, review count, question and answer counts, the `price` block (min, max, list min / max, percent off, `map_price_applies`), `is_clearance`, `buyable`, the option axes (color, size, width...) and every variant: `sku`, UPC, options, color, size, its own `price`, `list_price`, `percent_off`, `map_price_applies`, `is_clearance`, `online_units`, `buyable`, `ship_class`, `lead_time`, image |
| `POST /api/v1/dicks/products` | 1 | Up to 5 products by `product_ids` in one call: the style-level summary (title, brand, URL, image, price and list-price ranges, percent off, `map_price_applies`, `is_clearance`, `buyable`, options, attributes, specs, product type, rating, review count, description). No variants, no per-SKU prices, no units. Unknown ids in `not_found` |
| `POST /api/v1/dicks/reviews` | 2 | The 15 newest reviews of one product by `product_id` or `url`, with `stats` (total, average, 1-5 distribution, recommended and not-recommended counts, photo count, first and last review dates, question and answer counts, secondary averages such as Size, Fit, Comfort) and per review: rating, title, text, pros, cons, author nickname, date, recommended, helpful / unhelpful votes, `verified_purchaser`, `incentivized`, `syndicated_from`, secondary ratings, photos, `brand_response`. No paging, sort or star filter |
| `POST /api/v1/dicks/store-availability` | 1 | 1-20 SKUs at up to 100 stores near a ZIP (or lat + lng), nearest first, for one `chain`: `dicks` (default), `golf_galaxy` or `public_lands`. Per store: store id, chain, name, address, shopping center, city, state, ZIP, phone, lat, lng, distance, status, weekly hours and per SKU `units` and `in_store_units`. Plus `count`, `stores_with_stock` and `sku_totals[]` |
| `POST /api/v1/dicks/suggestions` | 1 | The search box's suggestions for a partial term: `keywords[]`, `brands[]`, `categories[]` (id, name, path, URL, product count) and `products[]` (id, title, brand, URL, image, color, price and list-price ranges, percent off) |

## Workflow

1. **Find products:** call `/dicks/search` with `query`, `/dicks/deals` with a `type`, `/dicks/brand` with a `brand` name, or `/dicks/category` with a `path` such as `/f/mens-running-shoes` (or a `categories[].id` from any earlier answer). Each item has an `id` and a `url`.
2. **Narrow the listing:** pass `brand`, `min_price` / `max_price`, or any facet through `filters` as `{facets[].id: facets[].values[].value}` (`{"5495": "Men's", "rating": "4+"}`). Facet ids are the site's own (`5495` is Gender, `3232` Color, `5212` Mens Shoe Size); `brand`, `price` and `rating` are readable aliases. Read the ids and values from a previous answer's `facets[]`: never guess them.
3. **Page through:** `page` 1, 2, 3... up to `total_pages`, and `page_size` up to 144 to save calls. Under the featured sort, pinned items come first on page 1, so that page can hold a few more items than `page_size`.
4. **One product in full:** call `/dicks/product` with the item's `id` as `product_id` (or its `url`). Read `variants[]` for each SKU's own price, clearance flag and online units.
5. **Store stock:** call `/dicks/store-availability` with up to 20 `variants[].sku` and the user's `zip`. Set `chain` to `golf_galaxy` or `public_lands` for those stores. Each store lists `units` per SKU.
6. **Price tracking:** call `/dicks/products` with up to 5 ids per call (1 credit) for the style-level price range, `/dicks/product` (2 credits) when you need the price of one size or color, or walk `/dicks/deals` with `type: "clearance"`; store `id`, `price`, `price_max`, `list_price`, `percent_off` (and the variant prices) per run and compare runs yourself. There is no price history.
7. **Reviews:** call `/dicks/reviews` with the product's `id` (the `review_count` on any listing or product tells you whether there is anything to read). It always returns the 15 newest; the `stats` block covers every review.
8. **Keyword research:** `/dicks/suggestions` with a partial term returns completions, brands, categories and products.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `brand` | string or array | none | A brand as the Brand facet lists it (`"Nike"`, `"HOKA"`, `"YETI"`), or up to 20 (any of them) |
| `page` | integer | 1 | Results page, 1-based (1-500). A page past the last one returns an empty `items` list with the real `total` |
| `page_size` | integer | 48 | Items per page, 1-144 |
| `sort` | string | `relevance` | `relevance`, `top_sellers`, `savings` (biggest discount first), `price_low_to_high`, `price_high_to_low`, `featured` (merchandised order, pinned items first), `new_arrivals` or `brand_az` |
| `filters` | object | none | Any facet from a previous answer: `{facets[].id: value}` or `{facets[].id: [values]}`. Values of one facet are OR, facets combine (AND). E.g. `{"5495": "Men's"}` (gender), `{"3232": "Black"}` (color), `{"rating": "4+"}`, `{"price": "50-100"}`, `{"5004": "Sale"}` |
| `min_price` | number | none | Approximate lower price bound in USD (0-100000). The site's price filter is loose: a few items just outside the range can appear |
| `max_price` | number | none | Approximate upper price bound in USD |

At most 10 facets, 20 values per facet and 40 values in all per call. Send `min_price` / `max_price` or `filters.price`, not both.

### Category (`/category`)

Pass one of `path`, `url` or `category_id`, plus `brand` and any grid parameter (`page`, `page_size`, `sort`, `filters`, `min_price`, `max_price`). The default sort is `featured`, like the site.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | one of | A category page path, `/f/<name>` or `/c/<name>` (`/f/mens-running-shoes`), as dickssportinggoods.com links and a response's `categories[].path` carry it |
| `url` | string | one of | A dickssportinggoods.com category URL. Filters in the URL are not read: send them in `filters` |
| `category_id` | string or integer | one of | A category id (`"202105"`): a response's `categories[].id` or `category.id` |

### Brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | required | A brand name as Dick's lists it in the Brand facet (`"Nike"`, `"YETI"`, `"Callaway"`, `"Under Armour"`); case does not matter. An unknown brand is a 404 |
| `query` | string | none | Narrow the brand to a keyword (`"tumbler"`) |

Plus any grid parameter. The default sort is `relevance`. To add more brands, use `filters.brand`.

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `clearance` | `clearance`, `sale` or `weekly_deals` (This Week's Deals) |
| `brand` | string or array | none | Only these brands |

Plus any grid parameter. The default sort is `featured`; send `sort: "savings"` for the biggest discounts first.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | A Dick's product id (6-30 letters and digits, any case): a listing item's `id`, the last part of a product URL (`"23FHQMCLFTN9GTXBLMNS"`) |
| `url` | string | one of | A dickssportinggoods.com product URL (`/p/<name>/<id>`). If both are sent they must name the same product |

### Products (`/products`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_ids` | array | required | 1 to 5 product ids. Unknown ids are listed in `not_found`; when none is found it is a 404 |

### Reviews (`/reviews`)

Pass `product_id` or `url`, as on `/product`. There are no other parameters: no page, sort, star filter or count.

### Store availability (`/store-availability`)

Pass `skus` and one of `zip` or `lat` + `lng`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skus` | array | required | 1 to 20 SKU ids (6-12 digits) from `/product`'s `variants[].sku` (`["25535758", "26810079"]`). A product id is not a SKU |
| `zip` | string or integer | one of | US ZIP code (`60601` or `60601-1234`) |
| `lat`, `lng` | number | one of | A point, both required together |
| `radius` | integer | 25 | Search radius in miles, 1-250. Up to 100 stores are returned |
| `chain` | string | `dicks` | `dicks` (DICK'S Sporting Goods, including House of Sport and Going, Going, Gone! stores), `golf_galaxy` or `public_lands` |
| `in_stock_only` | boolean | `false` | Only the stores that have at least one of the SKUs |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

## Examples

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 180 \
  -d '{"product_id": "23FHQMCLFTN9GTXBLMNS"}'
```

Captured `data` (the description cut to its first paragraph, 9 of 13 specs, 7 of 11 attributes, 8 of 10 images and 25 of 27 variants trimmed; the call took 29 seconds):

```json
{
  "id": "23FHQMCLFTN9GTXBLMNS",
  "title": "HOKA Men's Clifton 9 GTX Running Shoes",
  "brand": "Hoka",
  "url": "https://www.dickssportinggoods.com/p/hoka-mens-clifton-9-gtx-running-shoes-23fhqmclftn9gtxblmns/23fhqmclftn9gtxblmns",
  "description": "The HOKA Clifton 9 GTX is your go-to for all-weather runs with sleek waterproof protection and bold 360-degree reflectivity. It’s ultra-plush yet stable, keeping you light on your feet with a smooth, responsive ride. Grippy traction pods and a durable outsole keep you confident on slick streets. Plus, it’s packed with eco-conscious materials so you can feel good while moving fast.",
  "features": [],
  "specs": {
    "Best Use": "Everyday run, walking",
    "Running Shoe Support": "Neutral",
    "Running Shoe Cushioning": "Balanced cushioning",
    "Heel Stack Height (mm)": "38mm"
  },
  "attributes": {
    "Gender": "Men's",
    "Product Type": "Athletic & Sneakers",
    "Activity": ["Running", "Casual"],
    "Shoe Width": "Medium"
  },
  "product_type": "Athletic & Sneakers",
  "category": {
    "id": "202105",
    "name": "Men's Running Shoes",
    "path": "/f/mens-running-shoes",
    "url": "https://www.dickssportinggoods.com/f/mens-running-shoes"
  },
  "images": [
    "https://dks.scene7.com/is/image/GolfGalaxy/23FHQMCLFTN9GTXBLMNS_Black_Foggy_Night",
    "https://dks.scene7.com/is/image/GolfGalaxy/1141470F-BGYN_BlackFoggyNight_TOP"
  ],
  "rating": 4.46,
  "review_count": 157,
  "question_count": 1,
  "answer_count": 0,
  "price": {
    "min": 94.97,
    "max": 164.99,
    "list_min": 164.99,
    "list_max": 164.99,
    "percent_off": 42.44,
    "map_price_applies": true
  },
  "is_clearance": true,
  "buyable": true,
  "options": {
    "Color": ["Black/Foggy Night", "Gravel/Eggshell", "Black/Black"],
    "Shoe Size": ["8.0", "8.5", "9.0", "9.5", "10.0", "10.5", "11.0", "11.5", "12.0", "12.5", "13.0", "14.0"],
    "Shoe Width": ["Medium/D"]
  },
  "variant_count": 27,
  "variants": [
    {
      "sku": "26810079",
      "upc": "198605127618",
      "options": { "Color": "Black/Foggy Night", "Shoe Size": "11.5", "Shoe Width": "Medium/D" },
      "color": "Black/Foggy Night",
      "size": "11.5",
      "price": 164.99,
      "list_price": 164.99,
      "percent_off": 0,
      "map_price_applies": false,
      "is_clearance": false,
      "online_units": 4,
      "buyable": true,
      "ship_class": "P",
      "lead_time": 2,
      "image": "https://images.dickssportinggoods.com/is/image/dkscdn/23FHQMCLFTN9GTXBLMNS_Black_Foggy_Night_is"
    },
    {
      "sku": "25535758",
      "upc": "197634406961",
      "options": { "Color": "Black/Black", "Shoe Size": "14.0", "Shoe Width": "Medium/D" },
      "color": "Black/Black",
      "size": "14.0",
      "price": 94.97,
      "list_price": 164.99,
      "percent_off": 42.44,
      "map_price_applies": true,
      "is_clearance": true,
      "online_units": 19,
      "buyable": true,
      "ship_class": "P",
      "lead_time": 2,
      "image": "https://images.dickssportinggoods.com/is/image/dkscdn/23FHQMCLFTN9GTXBLMNS_Black_Black_is"
    }
  ],
  "currency": "USD"
}
```

Prices are per SKU, and they differ: in this answer all 11 Black/Black SKUs were on clearance at $94.97 (42.44% off the $164.99 list price) while the 16 Black/Foggy Night and Gravel/Eggshell SKUs sold at the full $164.99. The product-level `price` block (94.97 to 164.99) and `is_clearance: true` only say that some SKU is on clearance: read the variant the user wants before quoting a price. `map_price_applies: true` means Dick's shows that price only in the cart (the clearance SKUs here); the price field still carries it, so say it is a cart price. `online_units` is the number of units available to ship online for that SKU (0 for 7 of the 11 clearance SKUs here, 19 for size 14.0): it is not store stock. Pass `variants[].sku` values (`"25535758"`, `"26810079"`) to `/store-availability` for store unit counts.

### Products (batch)

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/products \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_ids": ["23FHQMCLFTN9GTXBLMNS", "26UNDMFITN1HRI9WUAETC", "17YETARMBLR20WMGSODR"]}'
```

Captured `data` (1 of 3 products, most attributes and specs trimmed, descriptions cut):

```json
{
  "count": 3,
  "products": [
    {
      "id": "23FHQMCLFTN9GTXBLMNS",
      "title": "HOKA Men's Clifton 9 GTX Running Shoes",
      "brand": "Hoka",
      "url": "https://www.dickssportinggoods.com/p/hoka-mens-clifton-9-gtx-running-shoes-23fhqmclftn9gtxblmns/23fhqmclftn9gtxblmns",
      "image": "https://dks.scene7.com/is/image/GolfGalaxy/23FHQMCLFTN9GTXBLMNS",
      "price": 94.97,
      "price_max": 164.99,
      "list_price": 164.99,
      "list_price_max": 164.99,
      "percent_off": 42.44,
      "map_price_applies": true,
      "is_clearance": true,
      "buyable": true,
      "options": {
        "Color": ["Black/Foggy Night", "Gravel/Eggshell", "Black/Black"],
        "Shoe Size": ["8.0", "8.5", "9.0", "9.5", "10.0", "10.5", "11.0", "11.5", "12.0", "12.5", "13.0", "14.0"],
        "Shoe Width": ["Medium/D"]
      },
      "attributes": { "Gender": "Men's", "Product Type": "Athletic & Sneakers" },
      "specs": { "Best Use": "Everyday run, walking", "Running Shoe Support": "Neutral" },
      "product_type": "Athletic & Sneakers",
      "rating": 4.46,
      "review_count": 157,
      "description": "The HOKA Clifton 9 GTX is your go-to for all-weather runs wi...",
      "currency": "USD"
    }
  ],
  "not_found": []
}
```

`/products` is the cheap check: 5 ids for 1 credit in about 6 seconds, against 2 credits and 20-75 seconds for one `/product`. It gives the same style-level range (94.97 to 164.99) and `is_clearance`, but not which sizes or colors are on clearance, and no units. Use it to spot a change, then call `/product` for the SKUs. `specs` can be null (it was for the hoodie in this answer).

### Deals (clearance)

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "clearance"}'
```

Captured `data` (49 of 50 items, 11 of 14 colors, 9 of 10 facets, most facet values and 5 of 7 categories trimmed):

```json
{
  "type": "clearance",
  "label": "Clearance",
  "total": 12386,
  "page": 1,
  "page_size": 48,
  "total_pages": 259,
  "sort": "featured",
  "count": 50,
  "items": [
    {
      "id": "25NIKWFITNPR3SHRTXCQC",
      "sku": "28505075",
      "title": "Nike Women's Pro Mid-Rise 3\" Bike Shorts With No Front Seam",
      "brand": "Nike",
      "url": "https://www.dickssportinggoods.com/p/nike-womens-pro-mid-rise-3-bike-shorts-with-no-front-seam-25nikwfitnpr3shrtxcqc/25nikwfitnpr3shrtxcqc",
      "image": "https://dks.scene7.com/is/image/GolfGalaxy/25NIKWFITNPR3SHRTXCQC",
      "price": 14.97,
      "price_max": 21.97,
      "list_price": 34,
      "list_price_max": 34,
      "percent_off": 55.97,
      "map_price_applies": false,
      "rating": 4.74,
      "review_count": 294,
      "badge": null,
      "sku_count": 69,
      "options": { "Color": ["Black/Barely Volt", "Black/Crimson Bliss", "Black/Lt Magenta"] },
      "is_pinned": true,
      "scheduled_prices": [
        { "price": 25.5, "starts_at": "2026-11-01T04:00:00.000Z", "ends_at": "2026-12-06T07:58:59.999Z" },
        { "price": 34, "starts_at": "2026-12-06T07:59:00.000Z", "ends_at": null }
      ]
    }
  ],
  "applied_filters": [],
  "facets": [
    {
      "id": "5495",
      "label": "Gender",
      "values": [
        { "value": "Men's", "label": "Men's", "count": 6052, "selected": false },
        { "value": "Women's", "label": "Women's", "count": 5337, "selected": false },
        { "value": "Boys'", "label": "Boys'", "count": 1990, "selected": false }
      ]
    }
  ],
  "categories": [
    {
      "id": "2769557",
      "name": "Men's",
      "path": "/f/clearance-mens",
      "url": "https://www.dickssportinggoods.com/f/clearance-mens",
      "count": 3057
    },
    {
      "id": "2769558",
      "name": "Women's",
      "path": "/f/clearance-womens",
      "url": "https://www.dickssportinggoods.com/f/clearance-womens",
      "count": 3267
    }
  ],
  "currency": "USD"
}
```

The clearance list had 12,386 items on 259 pages of 48. `count` is 50, not 48: under the `featured` sort Dick's pins merchandised items (`is_pinned: true`, 5 here) to the top of page 1, so that page runs longer than `page_size`. The shorts are on clearance from $14.97 to $21.97 by color and size (55.97% off the $34 list price at the low end): quote a range as a range. `scheduled_prices` are the offer-price windows Dick's has planned for the style: $25.50 until December 6, then $34 with no end date (`ends_at: null`). They are the retailer's own schedule, can change at any time, and need not match what the item sells for now (the clearance price here is already below them): never present them as a forecast or as price history. The other facets on this answer were `brand` (515 values), `5382` Product Type, `5212` / `5213` / `5214` shoe sizes, `5471` Shoe Width, `299` Size, `rating` and `price`. `categories[]` splits the list (Men's, Women's, Youth...): pass a `categories[].id` to `/category` as `category_id` to browse one part.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "running shoes"}'
```

Captured `data` (47 of 48 items, 9 of 12 colors, 11 of 14 facets, most facet values and 3 of 5 categories trimmed):

```json
{
  "query": "running shoes",
  "did_you_mean": null,
  "redirected_to": null,
  "category": null,
  "total": 720,
  "page": 1,
  "page_size": 48,
  "total_pages": 15,
  "sort": "relevance",
  "count": 48,
  "items": [
    {
      "id": "24ADIMDZRVSLWHTBLMNS",
      "sku": null,
      "title": "adidas Men's Adizero EVO SL Running Shoes",
      "brand": "adidas",
      "url": "https://www.dickssportinggoods.com/p/adidas-mens-adizero-evo-sl-running-shoes-24adimdzrvslwhtblmns/24adimdzrvslwhtblmns",
      "image": "https://dks.scene7.com/is/image/GolfGalaxy/24ADIMDZRVSLWHTBLMNS",
      "price": 119.97,
      "price_max": 119.99,
      "list_price": 149.99,
      "list_price_max": 149.99,
      "percent_off": 20.01,
      "map_price_applies": false,
      "rating": 4.78,
      "review_count": 8878,
      "badge": null,
      "sku_count": 99,
      "options": { "Color": ["Black/Solar Turbo/Iron Mtllc", "Black/Utility Black/White", "White/Black/White"] },
      "is_pinned": false,
      "scheduled_prices": []
    }
  ],
  "applied_filters": [],
  "facets": [
    {
      "id": "5495",
      "label": "Gender",
      "values": [
        { "value": "Men's", "label": "Men's", "count": 393, "selected": false },
        { "value": "Women's", "label": "Women's", "count": 334, "selected": false },
        { "value": "Boys'", "label": "Boys'", "count": 63, "selected": false }
      ]
    },
    {
      "id": "price",
      "label": "Price",
      "values": [
        { "value": "*-25", "label": "Under $25", "count": 1, "selected": false },
        { "value": "25-50", "label": "$25 - $50", "count": 24, "selected": false },
        { "value": "50-100", "label": "$50 - $100", "count": 183, "selected": false },
        { "value": "100-150", "label": "$100 - $150", "count": 332, "selected": false },
        { "value": "150-250", "label": "$150 - $250", "count": 333, "selected": false },
        { "value": "250-500", "label": "$250 - $500", "count": 25, "selected": false }
      ]
    },
    {
      "id": "rating",
      "label": "Customer Rating",
      "values": [
        { "value": "5", "label": "5 stars", "count": 50, "selected": false },
        { "value": "4+", "label": "4 stars & up", "count": 568, "selected": false },
        { "value": "3+", "label": "3 stars & up", "count": 643, "selected": false }
      ]
    }
  ],
  "categories": [
    {
      "id": "202102",
      "name": "Shoes",
      "path": "/c/footwear",
      "url": "https://www.dickssportinggoods.com/c/footwear",
      "count": 720
    },
    {
      "id": "201051",
      "name": "Sports Equipment",
      "path": "/c/shop-by-sport",
      "url": "https://www.dickssportinggoods.com/c/shop-by-sport",
      "count": 657
    }
  ],
  "currency": "USD"
}
```

Under the `relevance` sort the tiles are style-level, so `sku` is null on every item (all 48 here) and `scheduled_prices` comes back empty; `sku_count` (99) is how many SKUs the style has. Take the `id` to `/product` for the SKUs. The other facets on this answer were `brand`, `4285` Activity, `5212` / `5213` / `5214` shoe sizes, `5471` Shoe Width, `3232` Color, `5066` Surface Type, `2483` Running Type, `5222` Cushioning and `5004` Sale; any `facets[].id` with one of its `values[].value` works in `filters`, e.g. `{"5495": "Women's", "price": "100-150"}`. A misspelled query (`yeti tumbller`) comes back with `did_you_mean` set to Dick's spelling suggestion (`yeti tumbler`). A keyword Dick's sends to a landing page (`golf balls`, `clearance`) is followed to that page: `redirected_to` holds its path, `category` the category behind it, and the items are that listing's, in the featured order unless you sent a `sort`.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/f/mens-running-shoes"}'
```

Captured `data` (48 of 49 items, 4 of 7 colors and the 12 facets trimmed):

```json
{
  "category": {
    "id": "202105",
    "name": "Men's Running Shoes",
    "path": "/f/mens-running-shoes",
    "url": "https://www.dickssportinggoods.com/f/mens-running-shoes"
  },
  "total": 393,
  "page": 1,
  "page_size": 48,
  "total_pages": 9,
  "sort": "featured",
  "count": 49,
  "items": [
    {
      "id": "26HOKMRUNNOAHJUEPKJU0A",
      "sku": "28106728",
      "title": "HOKA Men's Arahi 9 Running Shoes",
      "brand": "Hoka",
      "url": "https://www.dickssportinggoods.com/p/hoka-mens-arahi-9-running-shoes-26hokmrunnoahjuepkju0a/26hokmrunnoahjuepkju0a",
      "image": "https://dks.scene7.com/is/image/GolfGalaxy/26HOKMRUNNOAHJUEPKJU0A",
      "price": 154.99,
      "price_max": 154.99,
      "list_price": 154.99,
      "list_price_max": 154.99,
      "percent_off": 0,
      "map_price_applies": false,
      "rating": 5,
      "review_count": 5,
      "badge": "New Arrival",
      "sku_count": 121,
      "options": { "Color": ["Virtual Blue/Soft Cobalt", "Cosmic Grey/Stardust", "Frost/Black"] },
      "is_pinned": true,
      "scheduled_prices": [{"price": 154.99, "starts_at": "2026-09-04T01:04:21.000Z", "ends_at": null}]
    }
  ],
  "applied_filters": [],
  "categories": [
    {
      "id": "12519600",
      "name": "Road Running",
      "path": "/f/mens-road-running-shoes",
      "url": "https://www.dickssportinggoods.com/f/mens-road-running-shoes",
      "count": 340
    },
    {
      "id": "1314219",
      "name": "Trail Running",
      "path": "/f/shop-mens-trail-running-shoes",
      "url": "https://www.dickssportinggoods.com/f/shop-mens-trail-running-shoes",
      "count": 48
    }
  ],
  "currency": "USD"
}
```

The same category is reachable as `{"category_id": "202105"}` or by its URL. `categories[]` lists its subcategories with their counts (Road Running 340, Trail Running 48). Under `featured` the 7 pinned items came first, so page 1 held 49 items. The facets here included `5588` Footwear Features and `5081` Shoe Weight, which a search for the same shoes did not list: read the facets of the listing you are filtering.

### Brand

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/brand \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "YETI"}'
```

The captured answer opens with (then the same `items[]`, `facets[]` and `categories[]` as search):

```json
{
  "brand": "YETI",
  "query": null,
  "total": 763,
  "page": 1,
  "page_size": 48,
  "total_pages": 16,
  "sort": "relevance",
  "count": 48,
  "applied_filters": [{"facet": "brand", "values": ["YETI"]}]
}
```

`brand` echoes the brand as Dick's writes it, whatever case you sent. Add `"query": "tumbler"` to narrow it to a keyword.

### Store availability

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"skus": ["25535758", "26810079"], "zip": "60601"}'
```

Captured `data` (11 of 13 stores trimmed):

```json
{
  "skus": ["25535758", "26810079"],
  "location": { "zip": "60601", "resolved": "CHICAGO, IL 60601, US" },
  "radius": 25,
  "chain": "dicks",
  "in_stock_only": false,
  "count": 13,
  "stores_with_stock": 1,
  "sku_totals": [
    { "sku": "25535758", "stores_with_stock": 0, "units": 0, "in_store_units": 0 },
    { "sku": "26810079", "stores_with_stock": 1, "units": 1, "in_store_units": 1 }
  ],
  "stores": [
    {
      "store_id": "1149",
      "chain": "Dick's Sporting Goods",
      "name": "Chicago (Lincoln Park)",
      "address": "1538 N Clybourn Avenue",
      "shopping_center": "Lincoln Park",
      "city": "Chicago",
      "state": "IL",
      "zip": "60610-1095",
      "phone": "312-489-2136",
      "lat": 41.909246,
      "lng": -87.647825,
      "distance_miles": 2,
      "status": "4",
      "hours": [
        { "day": "sunday", "open": "10:00", "close": "19:00" },
        { "day": "monday", "open": "09:00", "close": "20:00" },
        { "day": "tuesday", "open": "09:00", "close": "20:00" },
        { "day": "wednesday", "open": "09:00", "close": "20:00" },
        { "day": "thursday", "open": "09:00", "close": "20:00" },
        { "day": "friday", "open": "09:00", "close": "20:00" },
        { "day": "saturday", "open": "09:00", "close": "20:00" }
      ],
      "skus": [
        { "sku": "25535758", "units": 0, "in_store_units": 0 },
        { "sku": "26810079", "units": 0, "in_store_units": 0 }
      ]
    },
    {
      "store_id": "4459",
      "chain": "Dick's Sporting Goods",
      "name": "Going, Going, Gone!",
      "address": "102 Yorktown Shopping Ctr",
      "shopping_center": "Yorktown Center",
      "city": "Lombard",
      "state": "IL",
      "zip": "60148",
      "phone": "630-599-4804",
      "lat": 41.83858282,
      "lng": -88.00769298,
      "distance_miles": 19.97,
      "status": "4",
      "hours": [
        { "day": "sunday", "open": "10:00", "close": "19:00" },
        { "day": "monday", "open": "09:00", "close": "21:00" },
        { "day": "tuesday", "open": "09:00", "close": "21:00" },
        { "day": "wednesday", "open": "09:00", "close": "21:00" },
        { "day": "thursday", "open": "09:00", "close": "21:00" },
        { "day": "friday", "open": "09:00", "close": "21:00" },
        { "day": "saturday", "open": "09:00", "close": "21:00" }
      ],
      "skus": [
        { "sku": "25535758", "units": 0, "in_store_units": 0 },
        { "sku": "26810079", "units": 1, "in_store_units": 1 }
      ]
    }
  ]
}
```

Both SKUs are sizes of the HOKA shoe above: the clearance Black/Black size 14.0 (`25535758`) had 19 units online and none in the 13 Dick's stores within 25 miles of downtown Chicago, while the full-price size 11.5 (`26810079`) had 1 unit, at a Going, Going, Gone! store 20 miles out. `units` is what a store can sell; `in_store_units` is what it has on hand, and is higher than `units` only at a store that does not take orders for that item (where `units` reads 0). The `dicks` chain includes House of Sport and Going, Going, Gone! stores, whose `chain` still reads "Dick's Sporting Goods": tell them apart by `name`. Send `"chain": "golf_galaxy"` or `"chain": "public_lands"` for those stores. `status` is Dick's own store status code (`"4"` for a regular store). Hours are 24-hour `HH:MM` per weekday. There is no standalone store locator: store addresses, phones and hours come with a SKU lookup. An unknown SKU reads 0 at every store, exactly like an out-of-stock one, so always take SKUs from `/product`. Stock changes through the day: give the `fetched_at` time with any count.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 180 \
  -d '{"product_id": "26UNDMFITN1HRI9WUAETC"}'
```

Captured `data` (13 of 15 reviews trimmed; the call took 61 seconds):

```json
{
  "product": {
    "id": "26UNDMFITN1HRI9WUAETC",
    "title": "Under Armour Men's Waffle Hoodie",
    "url": "https://www.dickssportinggoods.com/p/under-armour-mens-waffle-hoodie-26undmfitn1hri9wuaetc/26undmfitn1hri9wuaetc"
  },
  "stats": {
    "total": 669,
    "average": 4.86,
    "distribution": { "1": 4, "2": 2, "3": 4, "4": 64, "5": 595 },
    "recommended_count": 613,
    "not_recommended_count": 14,
    "photo_count": 5,
    "first_review_at": "2021-10-26T11:46:30.000Z",
    "last_review_at": "2026-11-09T23:17:24.000Z",
    "question_count": 6,
    "answer_count": 6,
    "secondary_averages": [
      { "name": "Size", "average": 3, "range": 5, "min_label": "Runs small", "max_label": "Runs big" },
      { "name": "Fit", "average": 3, "range": 5, "min_label": "Too loose", "max_label": "Too tight" },
      { "name": "Comfort", "average": 4, "range": 5, "min_label": "Poor", "max_label": "Excellent" }
    ]
  },
  "sort": "newest",
  "count": 15,
  "reviews": [
    {
      "id": "273835539",
      "rating": 5,
      "title": "Great fit",
      "text": "No complaints at all. Very warm and comfortable. Was exactly what I was hoping for.",
      "pros": null,
      "cons": null,
      "author": "JoshK2026",
      "submitted_at": "2026-11-09T23:17:24.000Z",
      "recommended": true,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "verified_purchaser": false,
      "incentivized": false,
      "syndicated_from": "Under Armour",
      "secondary_ratings": [],
      "photos": [],
      "brand_response": null
    },
    {
      "id": "281621792",
      "rating": 5,
      "title": "Casual or dress it up",
      "text": "Runs true to size, not too thick or too thin- nice material.",
      "pros": null,
      "cons": null,
      "author": "Koders",
      "submitted_at": "2026-11-08T04:51:05.000Z",
      "recommended": null,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "verified_purchaser": true,
      "incentivized": false,
      "syndicated_from": null,
      "secondary_ratings": [],
      "photos": [],
      "brand_response": null
    }
  ]
}
```

`/reviews` returns the 15 newest reviews and nothing else: there is no page, sort, star filter or way to ask for more, so never present these 15 as all of a product's 669 reviews, and never imply older reviews can be fetched. `stats` (total, average, distribution, recommended counts, secondary averages) covers every review, not just the 15. `secondary_averages` is on the scale between `min_label` and `max_label`: a Size average of 3 of 5 sits between "Runs small" and "Runs big". `question_count` and `answer_count` are counts only: question and answer text is not available. `syndicated_from` names the brand site a review was collected on (11 of these 15 came from Under Armour's site); `verified_purchaser: true` (4 of 15 here) and `incentivized` are Dick's own badges: report them with any summary. `recommended` can be null when the reviewer did not say. Reviewer age, gender and location are never returned.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/dicks/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "yeti tum"}'
```

Captured `data` (2 of 4 products trimmed):

```json
{
  "query": "yeti tum",
  "count": 9,
  "keywords": ["yeti tumbler", "yeti 20 oz tumbler", "yeti 30 oz tumbler", "yeti wine tumbler", "yeti coffee tumbler"],
  "brands": [],
  "categories": [],
  "products": [
    {
      "id": "17YETARMBLR20WMGSODR",
      "title": "YETI 20 oz. Rambler Tumbler with MagSlider Lid",
      "brand": "YETI",
      "url": "https://www.dickssportinggoods.com/p/yeti-20-ozrambler-tumbler-with-magslider-lid-17yetarmblr20wmgsodr/17yetarmblr20wmgsodr",
      "image": "https://dks.scene7.com/is/image/GolfGalaxy/17YETARMBLR20WMGSODR",
      "color": "Pace Purple",
      "price": 28,
      "price_max": 40,
      "list_price": 35,
      "list_price_max": 40,
      "percent_off": 20,
      "map_price_applies": false
    },
    {
      "id": "17YETARMBLR30WMGSODR",
      "title": "YETI 30 oz. Rambler Tumbler with MagSlider Lid",
      "brand": "YETI",
      "url": "https://www.dickssportinggoods.com/p/yeti-30-ozrambler-tumbler-with-magslider-lid-17yetarmblr30wmgsodr/17yetarmblr30wmgsodr",
      "image": "https://dks.scene7.com/is/image/GolfGalaxy/17YETARMBLR30WMGSODR",
      "color": "Ridgeline",
      "price": 32,
      "price_max": 40,
      "list_price": 40,
      "list_price_max": 40,
      "percent_off": 20,
      "map_price_applies": false
    }
  ],
  "currency": "USD"
}
```

`count` (9) is all suggestions together: 5 keywords and 4 products here, no brands or categories for this term. A suggested product's `id` works directly in `/product`, `/products` and `/reviews`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def dicks(endpoint, body, timeout=90):
    r = requests.post(f"{BASE}/api/v1/dicks/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

# 1. Clearance, biggest discounts first, men's only (1 credit per page)
page = dicks("deals", {"type": "clearance", "sort": "savings", "page_size": 144, "filters": {"5495": "Men's"}})
for p in page["items"][:5]:
    print(p["id"], p["title"], p["price"], "-", p["price_max"], "was", p["list_price"], p["percent_off"], "% off")

# 2. Which sizes are on clearance, then store units for them (2 + 1 credits; product is slow)
item = dicks("product", {"product_id": "23FHQMCLFTN9GTXBLMNS"}, timeout=180)
clearance = [v for v in item["variants"] if v["is_clearance"]]
for v in clearance:
    print(v["color"], v["size"], v["price"], "cart price" if v["map_price_applies"] else "", v["online_units"], "online")
near = dicks("store-availability", {"skus": [v["sku"] for v in clearance][:20], "zip": "60601"})
for s in near["stores"]:
    have = [x for x in s["skus"] if x["units"] > 0]
    if have:
        print(s["name"], s["distance_miles"], "mi", have)

# 3. Cheap price check for up to 5 products (1 credit)
batch = dicks("products", {"product_ids": ["23FHQMCLFTN9GTXBLMNS", "26UNDMFITN1HRI9WUAETC"]})
for p in batch["products"]:
    print(p["id"], p["price"], p["price_max"], "clearance" if p["is_clearance"] else "")

# 4. The 15 newest reviews (2 credits, slow)
rv = dicks("reviews", {"product_id": "26UNDMFITN1HRI9WUAETC"}, timeout=180)
print(rv["stats"]["total"], "reviews, average", rv["stats"]["average"])
for r in rv["reviews"]:
    print(r["rating"], r["title"], "| verified:", r["verified_purchaser"], "from:", r["syndicated_from"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when the answer was produced.

- **listing item** (search, category, brand, deals) - `id`, `sku` (the SKU the tile shows; null on style-level tiles, which the relevance sort returns), `title`, `brand`, `url`, `image`, `price`, `price_max`, `list_price`, `list_price_max`, `percent_off`, `map_price_applies`, `rating`, `review_count`, `badge` (New Color, New Arrival, Extended Sizes... or null), `sku_count`, `options` (e.g. `{"Color": [...]}`), `is_pinned`, `scheduled_prices[]` {`price`, `starts_at`, `ends_at` (null = no end date)}.
- **grid** (all four listings) - `total`, `page`, `page_size`, `total_pages`, `sort`, `count`, `items[]`, `applied_filters[]` {`facet`, `values[]`}, `facets[]` {`id`, `label`, `values[]` {`value`, `label`, `count`, `selected`}}, `categories[]` {`id`, `name`, `path`, `url`, `count`}, `currency`.
- **search** - `query`, `did_you_mean` (Dick's spelling suggestion, or null), `redirected_to` (the landing page path the keyword was sent to, or null), `category` ({`id`, `name`, `path`, `url`} of that landing page, or null) and the grid.
- **category** - `category` {`id`, `name`, `path`, `url`} and the grid.
- **brand** - `brand` (as Dick's writes it), `query` and the grid.
- **deals** - `type`, `label` and the grid.
- **product** - `id`, `title`, `brand`, `url`, `description`, `features[]`, `specs` {name: value}, `attributes` {name: value or values}, `product_type`, `category` {`id`, `name`, `path`, `url`}, `images[]`, `rating`, `review_count`, `question_count`, `answer_count`, `price` {`min`, `max`, `list_min`, `list_max`, `percent_off`, `map_price_applies`}, `is_clearance`, `buyable`, `options` {axis: [values]}, `variant_count`, `variants[]` {`sku`, `upc`, `options`, `color`, `size`, `price`, `list_price`, `percent_off`, `map_price_applies`, `is_clearance`, `online_units`, `buyable`, `ship_class`, `lead_time`, `image`}, `currency`.
- **products** - `count`, `products[]` {`id`, `title`, `brand`, `url`, `image`, `price`, `price_max`, `list_price`, `list_price_max`, `percent_off`, `map_price_applies`, `is_clearance`, `buyable`, `options`, `attributes`, `specs` (can be null), `product_type`, `rating`, `review_count`, `description`, `currency`}, `not_found[]`.
- **reviews** - `product` {`id`, `title`, `url`}, `stats` {`total`, `average`, `distribution` {`1`..`5`}, `recommended_count`, `not_recommended_count`, `photo_count`, `first_review_at`, `last_review_at`, `question_count`, `answer_count`, `secondary_averages[]` {`name`, `average`, `range`, `min_label`, `max_label`}}, `sort` (`newest`), `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `pros`, `cons`, `author`, `submitted_at`, `recommended`, `helpful_votes`, `unhelpful_votes`, `verified_purchaser`, `incentivized`, `syndicated_from`, `secondary_ratings[]`, `photos[]`, `brand_response` (text, date, author and department, or null)}.
- **store-availability** - `skus[]`, `location` ({`zip`} or {`lat`, `lng`}, with `resolved`, the address Dick's matched it to), `radius`, `chain`, `in_stock_only`, `count`, `stores_with_stock`, `sku_totals[]` {`sku`, `stores_with_stock`, `units`, `in_store_units`}, `stores[]` {`store_id`, `chain`, `name`, `address`, `shopping_center`, `city`, `state`, `zip`, `phone`, `lat`, `lng`, `distance_miles`, `status`, `hours[]` {`day`, `open`, `close`}, `skus[]` {`sku`, `units`, `in_store_units`}}.
- **suggestions** - `query`, `count`, `keywords[]`, `brands[]`, `categories[]` {`id`, `name`, `path`, `url`, `product_count`}, `products[]` {`id`, `title`, `brand`, `url`, `image`, `color`, `price`, `price_max`, `list_price`, `list_price_max`, `percent_off`, `map_price_applies`}, `currency`.

## Guardrails

- Prices are US dollars (`currency: "USD"`): `94.97` is $94.97. This is dickssportinggoods.com (US) only; there is no international site and no `country` parameter.
- Prices are per SKU. A listing's `price` / `price_max` and the product's `price` block are ranges across sizes and colors, and `is_clearance: true` means at least one SKU is on clearance, not all of them. Quote the price of the variant the user asked about from `/product`'s `variants[]`, or quote a range as a range.
- `percent_off` compares the current price with Dick's list price (on a range, the low ends). Report the list price as Dick's list price, not as proof of a past selling price.
- `map_price_applies: true` means Dick's shows that price only in the cart. The price fields still carry it; say it is the price shown in the cart, and never present it as an advertised shelf price.
- `scheduled_prices` are the offer-price windows Dick's has planned for an item, as the retailer set them. They can change or be withdrawn at any time and need not match today's price. Never call them a forecast, a guaranteed future price or price history.
- There is no price history. To track clearance or prices, poll the listings, `/products` (5 ids per credit) or `/product` on a schedule and store the results yourself.
- Pinned items: under the `featured` sort (the default on category and deals) Dick's puts merchandised items (`is_pinned: true`) first on page 1, so page 1 can hold more than `page_size` items. Pinned placement is merchandising, not relevance or sales rank. There is no sponsored-item flag.
- Filters: `filters` keys are `facets[].id` (the site's numeric ids such as `5495`, or the aliases `brand`, `price`, `rating`) and values are `facets[].values[].value` from a previous answer. Facets differ by listing: read the facets of the listing you filter. `min_price` / `max_price` are approximate (a few items just outside the range can appear); filter `items` by `price` yourself when you need a strict range. A filter that matches nothing returns a 200 with `total: 0`. A category cannot be chosen through `filters`: use `/category` with a `categories[].id`.
- `did_you_mean` set means Dick's suggested another spelling: say so. `redirected_to` set means the keyword was sent to a landing page and the items are that page's listing (with `category` naming it); when the landing page has no product grid, the answer has `total: 0` and that `redirected_to`.
- `/product` and `/reviews` are slow (usually 20-75 seconds, up to about 2.5 minutes) and cost 2 credits. Use a client timeout of at least 180 seconds, run them one at a time, prefer `/products` for a price check, and tell the user the call takes a while rather than retrying early.
- `online_units` on `/product` is online stock for that SKU, not store stock. `/store-availability` takes variant `skus`, never a product id; an unknown SKU reads 0 at every store, the same as out of stock, so only pass SKUs from `/product`. Golf Galaxy and Public Lands stores need `chain`; the default `dicks` chain covers Dick's, House of Sport and Going, Going, Gone! stores. Give the `fetched_at` time with any count.
- Reviews: only the 15 newest come back, with no paging, sort or star filter. Never present them as all reviews or as a representative sample of older ones; `stats` describes the whole product. Report `verified_purchaser`, `incentivized` and `syndicated_from` with any summary: a syndicated review was written on the brand's own site. Quote review text verbatim with its rating and date. Questions and answers are counts only.
- Privacy: reviewer age, gender and location are never returned. Reviewers appear by the nickname they chose to publish.
- Not covered: ScoreCard prices, points or rewards, account data, order status, and anything at checkout. Dick's Best Price Guarantee is Dick's own policy, decided by Dick's: this API can show a Dick's price with its URL and time, but it does not submit price-match requests and cannot say whether Dick's will match.
- Dick's Sporting Goods does not publish a public developer API: suppliers exchange orders and inventory with it over EDI, and approved affiliates get a product datafeed through CJ; neither offers a public endpoint for searching the catalog, reading live prices or checking store stock. This API reads public product data for research, price monitoring and stock alerts. It does not add to cart, check out or hold stock; never present it as a purchasing bot or as a way to buy ahead of other shoppers.
- Never fabricate prices, clearance status, stock, unit counts or ratings. Only return what the API returned, with the product `url` or `id`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`; `page` outside 1-500 or `page_size` outside 1-144; an unknown `sort` or deal `type`; `filters` that is not an object of facet id to value(s), a key that is not a facet id, a category facet, more than 10 facets, more than 20 values for one or 40 in all; `min_price` above `max_price`, or `min_price` / `max_price` with `filters.price`; more than one of `path`, `url` and `category_id`, or none; a category path that is not `/f/<name>` or `/c/<name>`; a `product_id` that is not 6-30 letters and digits; a product `url` without `/p/<name>/<id>`; `product_id` and `url` naming different products; more than 5 `product_ids`; no `skus`, more than 20, or a SKU that is not 6-12 digits; a ZIP that is not 5 digits; both `zip` and `lat` / `lng`, or `lat` without `lng`; a `radius` outside 1-250; an unknown `chain`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product (none of the `product_ids` either), no such brand, no such category page, no products under a category, or a ZIP Dick's could not locate (try a nearby ZIP or `lat` + `lng`). Not charged. Re-run the search for a fresh `id`, or use a brand as the Brand facet of a search lists it.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api).
- `502` means Dick's Sporting Goods was temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means too many Dick's calls are running at once: wait the `Retry-After` seconds (5) and send it again. Not charged.

## SDKs

```bash
pip install scavio==0.47.0
npm install scavio@0.48.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.dicks.search({ query: "running shoes", filters: { "5495": "Men's" } });
const { data: next } = await scavio.dicks.search({ query: "running shoes", page: 2, page_size: 144 });
const { data: clearance } = await scavio.dicks.deals({ type: "clearance", sort: "savings" });
const { data: shoes } = await scavio.dicks.category({ path: "/f/mens-running-shoes" });
const { data: yeti } = await scavio.dicks.brand({ brand: "YETI", query: "tumbler" });
const { data: batch } = await scavio.dicks.products({ product_ids: ["23FHQMCLFTN9GTXBLMNS", "26UNDMFITN1HRI9WUAETC"] });
const { data: ideas } = await scavio.dicks.suggestions({ query: "yeti tum" });
// Slow (20-75 s, up to ~2.5 min): the SDK allows a longer timeout for these two
const { data: item } = await scavio.dicks.product({ product_id: "23FHQMCLFTN9GTXBLMNS" });
const { data: reviews } = await scavio.dicks.reviews({ product_id: "26UNDMFITN1HRI9WUAETC" });
const skus = item.variants.filter((v) => v.is_clearance).map((v) => v.sku);
const { data: near } = await scavio.dicks.storeAvailability({ skus, zip: "60601" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.dicks.search(...)`, `client.dicks.product(...)`, `client.dicks.products(...)`, `client.dicks.reviews(...)`, `client.dicks.category(...)`, `client.dicks.brand(...)`, `client.dicks.deals(...)`, `client.dicks.store_availability(...)` and `client.dicks.suggestions(...)`.

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_dicks`, `get_dicks_product`, `get_dicks_products`, `get_dicks_reviews`, `get_dicks_category`, `get_dicks_brand`, `get_dicks_deals`, `get_dicks_store_availability` and `get_dicks_suggestions`. Dick's is opt-in: add `dicks` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.45.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,dicks"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/dicks-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [product](https://scavio.dev/docs/dicks-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [products](https://scavio.dev/docs/dicks-products?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [reviews](https://scavio.dev/docs/dicks-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [category](https://scavio.dev/docs/dicks-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [brand](https://scavio.dev/docs/dicks-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [deals](https://scavio.dev/docs/dicks-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [store availability](https://scavio.dev/docs/dicks-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api), [suggestions](https://scavio.dev/docs/dicks-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api). Overview: [Dick's Sporting Goods API](https://scavio.dev/dicks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=dicks-sporting-goods-api).
