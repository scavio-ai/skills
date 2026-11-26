# Gap and Old Navy API - Prices, Sizes, Store Stock, Banana Republic, Athleta

Read Gap Inc. (gap.com, the US apparel company): one API for its six banners, Gap, Old Navy, Banana Republic, Athleta, Gap Factory and Banana Republic Factory, picked with `brand`. Keyword search and category listings with the list price, the price shown, Gap's price type and percent off; one product with every fit, color and size, each size with its own price, online stock status and UPC; current prices for up to 100 colors in one call, banners mixed; the pickup stock bucket of up to 20 SKUs at up to 10 stores; stores near a ZIP or postal code and one store; the banner's menu tree, current promotions as its promo drawer words them, search suggestions and trending searches. The US sites (USD, English) and the Canadian sites (CAD, English or French). Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: Gap and Old Navy prices, sale and clearance, per size.** What a style costs on its banner today, list against shown price, and which sizes are left. On 2026-11-26 a Gap search for `jeans` matched 713 styles; the first, Mid Rise UltraSoft Baggy Jeans (color id `403540002`, style `403540`), read `regular_price` 89.95 and `effective_price` 35 with `price_type` `promotion`, `percent_off` 61 and the flag "60% off: really big deal", rated 4.52 from 1,843 reviews. Its product page listed 3 fits (REGULAR with 14 colors, TALL 4, PETITE 5); the REGULAR fit's sizes read 237 in stock, 9 low stock and 100 out of stock online. The second job is clearance: Old Navy's Shop All Clearance category (cid `3033077`) listed 2,481 colors, the first a Bounce Fleece V-Neck Sweatshirt for Girls at $7.47 against $29.99 (`markdown`, 75% off) with 5,787 online units and Gap's flag "Clearance: Final sale. No returns or exchanges." Pair it with `nordstrom-product-data`, `macys-product-data`, `kohls-product-data` and `target-product-data` for apparel prices at other US retailers.

Nine limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **A checkout code is never in a price.** `effective_price` is the price shown, with "price as marked" sales already in it. Offers applied at checkout ("Extra 50% off at checkout", Gap's "Black Friday 50% off sitewide ... Applied at checkout", Athleta's "Code PLUS10") appear only as text in `flags` and in `deals`. Never compute or claim a price after a code.
- **Price type and percent off are Gap's.** `price_type` is `regular`, `promotion` (a sale price as marked) or `markdown` (clearance); `percent_off` is Gap's figure as given. `regular_price` is the list price Gap shows struck through; Gap's own pricing policy says it is "a price at which we previously offered the product, or a comparable product ... or the value of a similar item in the market". Report it as Gap's list price, never judge it.
- **Prices are online prices.** Every price is the banner's online price. Gap gives no per-store price and its terms say the in-store price may differ between stores and from the online price.
- **Store stock is a bucket, never a count.** `/store-stock` returns `in_stock`, `low_stock` or `out_of_stock` per SKU per store for in-store pickup. No unit counts exist for stores. `online_units` on a category item is Gap's online unit count for that color, not store stock.
- **Ids are per banner and per market.** A color id (`pid`), category id (`cid`) and store id belong to one banner in one market: a Gap id sent with `brand` `old_navy`, or a US id with `country` `ca`, is a charged `404`. Take ids from an earlier answer on the same banner and market.
- **No zero-results answer.** A query Gap cannot match answers its closest products. Check that item names fit the query before reporting them.
- **No review texts.** `rating`, `rating_count`, `review_count` and `review_summary` (Gap's own summary of its reviews, with likes and dislikes) are returned; individual reviews and reviewer names are not.
- **No history, no end dates.** Nothing is cached or kept, and Gap gives no promotion end dates. Poll and store your own series.

Gap Inc. has no public API for its catalog, prices or store stock; no developer program was found. Prices, sizes and store pickup are shown on each banner's site, and this skill reads those public pages with one Scavio key.

Gap Inc.'s fiscal 2025 annual report (10-K, year ended January 31, 2026) lists 2,474 company-operated stores (Old Navy North America 1,242; Gap North America 459 and Asia 123; Banana Republic North America 358 and Asia 40; Athleta 252) and about 1,000 franchise stores. Quote these with their source, never from the samples. gap.co.jp and the franchise sites outside the US and Canada are not served.

See also: apparel at other US retailers `nordstrom-product-data`, `nordstrom-rack-product-data`, `macys-product-data`, `kohls-product-data`, `jcpenney-product-data`, `target-product-data`; other fashion brands `hm-api`, `zara-api`, `uniqlo-api`, `asos-api`; the same item across retailers `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Price a Gap, Old Navy, Banana Republic, Athleta, Gap Factory or Banana Republic Factory style: list price, price shown, Gap's price type (regular, promotion, markdown) and percent off
- Track sale and clearance on a banner: the clearance or sale categories, the `sale_type` search filter, markdown prices and final-sale flags
- List every size of a style with its own price, online stock status (in stock, low stock, out of stock, on order) and UPC, across REGULAR, TALL and PETITE fits
- Check whether chosen sizes are in stock, low or out for pickup at up to 10 stores of a banner
- Price up to 100 colors in one call, banners mixed (a watch list)
- Search a banner by keyword, sorted by price, rating or best sellers, filtered by department, color, price, rating, a pickup store or any facet (rise, leg shape, wash, fit)
- Browse a banner's menu tree and list a category with each color's online unit count
- Read a banner's current promotions as its promo drawer words them, and its sale and clearance menu links
- Find a banner's stores near a US ZIP or Canadian postal code with this week's hours, dated holiday hours and pickup, or read one store's services
- Read the search box's suggestions or trending searches on a banner
- Read the Canadian sites in CAD, in English or French

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, suggestions took under 1 second, search, prices, stores, deals, category and trending 1.5-3.5, store about 5, categories about 8 and a product about 11. A 200-item search page can take 25 seconds. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/gap/search` | Keyword search on one banner: styles with their colors, list price, price shown, price type, percent off, rating, badges, flags; total, pages, facets | 1 |
| `POST /api/v1/gap/category` | One category by cid or link: colors with prices and each color's online unit count and status; sub-groups and facets | 1 |
| `POST /api/v1/gap/categories` | The banner's menu tree: divisions, sections and categories with their cid and style | 1 |
| `POST /api/v1/gap/product` | One product by color id or link: every fit, color and size with its own price, stock status and UPC; details, rating, Gap's review summary | 1 |
| `POST /api/v1/gap/prices` | Current prices for up to 100 colors in one call, banners mixed | 1 |
| `POST /api/v1/gap/stores` | Stores of one banner near a ZIP / postal code or a point: address, phone, distance, hours, dated holiday hours, pickup | 1 |
| `POST /api/v1/gap/store` | One store by id: status, opening date, address, phone, languages, services | 1 |
| `POST /api/v1/gap/store-stock` | Pickup stock bucket (in_stock, low_stock, out_of_stock) of up to 20 SKUs, or every SKU of a style, at up to 10 stores | 1 |
| `POST /api/v1/gap/suggestions` | The search box's suggestions with department filters, and the products it shows | 1 |
| `POST /api/v1/gap/trending` | The trending searches the banner's search box shows | 1 |
| `POST /api/v1/gap/deals` | The banner's current promotions as its promo drawer words them, and its sale, deal and clearance menu links | 1 |

Every endpoint takes `brand`: `gap` (default), `old_navy`, `banana_republic`, `athleta`, `gap_factory` or `banana_republic_factory`; `country` `us` (default, USD) or `ca` (the Canadian sites, CAD); and, where the endpoint has text, `language` `en` (default) or `fr` (with `ca` only). `fr` with `us` is a `400`, not charged.

## Prices: list price, price shown, price type

Every priced item, color and size carries:

| Field | Meaning |
|---|---|
| `regular_price` | Gap's list price (the struck-through price), as given |
| `effective_price` | The price shown, sales "as marked" included; never a checkout code |
| `price_type` | `regular`, `promotion` (a sale price as marked) or `markdown` (clearance), as Gap types it |
| `percent_off` | Gap's percent off, as given (product SKUs: `discount_percentage` and `discount_saving`) |
| `regular_price_range`, `sale_price_range` | Search: {`min`, `max`} over a style's colors and sizes |
| `flags` | Gap's marketing text on the item: "60% off: really big deal", "Extra 50% off at checkout", "Clearance: Final sale. No returns or exchanges." |
| `badges` | Gap's badges ("Best seller", "Now on Sale", "Online Exclusive") |
| `excluded_from_promotion` | Gap's flag that the style is excluded from promotions |
| `max_regular_price`, `max_effective_price`, `price_types` | Prices: the highest over a color's sizes (`regular_price` and `effective_price` are the lowest) and every price type seen |

- **One price per size.** A product's sizes can carry different prices: Gap's Mid Rise UltraSoft Baggy Jeans read $35 to $99.95 across sizes and colors with price types regular, markdown and promotion. Quote the size's own `effective_price`.
- **Checkout offers stay text.** A color of the same jeans read $44.99 `markdown` with the flag "Extra 50% off at checkout": report $44.99 and the flag as Gap words it. Never apply the 50%.
- **Canada:** `currency` `CAD`; French labels on `language` `fr` (flag "60 % de rabais: grandes aubaines", badge "Meilleur vendeur"). Report each market in its own currency; never convert or call one cheaper.
- Report Gap's labels and the numbers. Never judge a list price or a discount, never describe how often an item is on sale, and never compute a price after a code.

## Workflow

1. **Pick the banner and market.** `brand` (`old_navy` for Old Navy) and `country` (`ca` for Canada, `language` `fr` for French). Ids from one banner and market only work there.
2. **Find the style.** `/search` with `query`, or `/categories` then `/category` with a `cid` (and `style` when the link has one), or a sale link from `/deals`. Each color's `pid` is the input of product and prices; `style_id` the input of store-stock.
3. **Read it in full.** `/product` with `pid` (or the item's `url`): every fit (`variants[].variant` REGULAR, TALL, PETITE), color and size with `sku_id`, price, `stock_status` and `upc`.
4. **Pickup at stores.** `/stores` with `zip` (or `latitude` with `longitude`) gives `store_id`s; `/store-stock` with up to 10 `store_ids` and up to 20 `sku_ids` (or one `style_id`) gives each SKU's bucket per store.
5. **Watch prices.** `/prices` with up to 100 colors (`{"brand": "old_navy", "pid": "903453022"}` or `"athleta:1177198082"`) in one call; poll it on a schedule and store each answer with its `fetched_at`.
6. **Narrow a list.** `sort`, `department`, `sale_type` (`regular`, `sale`, `clearance`), `color`, `min_price` / `max_price`, `rating` (1-4, "& up"), `store_id` (pickup) and `facets` (up to 10 facet name to value pairs from `facets[].name` and `facets[].options[].value`); `page` and `page_size` (1-200, default 50).
7. **Promotions.** `/deals` gives the promo drawer offers as worded and the sale and clearance menu links; send a link's `cid` and `style` to `/category`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, 1-100 chars |
| `brand`, `country`, `language` | string | `gap`, `us`, `en` | Banner and market, as above |
| `sort` | string | `featured` | `featured` (the site's order), `price_asc`, `price_desc`, `top_rated`, `best_sellers` |
| `page` | integer | 1 | 1-1000; a page past the last is a charged `404` |
| `page_size` | integer | 50 | 1-200; large pages are slow (200 items can take 25 s) |
| `department` | string | none | A department as the facets list it (`Women`, `Men`, `Girls`, `Boys`, ...) |
| `sale_type` | string | none | `regular`, `sale` (promotion) or `clearance` (markdown): styles with at least one color of that type |
| `color` | string | none | A color family as the facets list it (`Black`) |
| `min_price`, `max_price` | number | none | Price range in the market's currency |
| `rating` | integer | none | Minimum stars, 1-4 ("4 & up") |
| `store_id` | string | none | Only products available for pickup at this store (`stores[].store_id`) |
| `facets` | object | none | Up to 10 facet name to value pairs, e.g. `{"fit": "Baggy"}` (names and values from an answer's `facets`) |

### Category (`/category`) and categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `cid` | string | one of | A category id: `categories[].cid` (the cid of the category link, not the nav node id) |
| `style` | string | none | The link's `style=` (`categories[].style`), when it has one |
| `url` | string | one of | Or a category link (sets brand and country) |
| `sort`, `page`, `page_size`, `facets` | | | As on search; `page_size` counts colors, not styles |

`/categories` takes `brand`, `country` and `language` only.

### Product (`/product`) and prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `pid` | string | one of | A color id, 9-11 digits (search `items[].pid` or `colors[].pid`) |
| `url` | string | one of | Or a product link (sets brand and country) |
| `items` | array | prices: required | 1-100 colors, banners may mix: `{"brand": "old_navy", "pid": "903453022"}` or `"old_navy:903453022"` |
| `brand` | string | `gap` | Prices: the banner of items that do not name one |

### Stores (`/stores`), store (`/store`), store stock (`/store-stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | A US ZIP (country `us`) or a Canadian postal code (`A1A 1A1`, country `ca`) |
| `latitude`, `longitude` | number | one of | Or a point |
| `radius` | integer | the site's | Miles, 1-100 |
| `limit` | integer | 10 | Stores to return, 1-20 |
| `store_id` | string | store: required | A store id (`stores[].store_id`) |
| `store_ids` | array | store-stock: required | 1-10 store ids from stores (same banner and market) |
| `sku_ids` | array | one of | 1-20 SKU ids (product `colors[].skus[].sku_id`) |
| `style_id` | string | one of | Or a style id: every SKU of the style |

### Suggestions (`/suggestions`), trending (`/trending`), deals (`/deals`)

`/suggestions` takes `query` (1-100 chars, what has been typed so far) with `brand`, `country`, `language`. `/trending` and `/deals` take `brand`, `country`, `language` only.

## Examples

### One product with every size's price, stock status and UPC

```bash
curl -X POST https://api.scavio.dev/api/v1/gap/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pid": "403540002"}'
```

Captured `data` (2026-11-26; `details`, `highlights`, `sizes`, images, color `url` and `notes` dropped, `variants` cut to 1 of 3, `colors` to 1 of 14, `skus` to 1 of 37):

```json
{
  "pid": "403540002",
  "style_id": "403540",
  "brand": "gap",
  "brand_name": "Gap",
  "name": "Mid Rise UltraSoft Baggy Jeans",
  "url": "https://www.gap.com/browse/product.do?pid=403540002",
  "currency": "USD",
  "category": "Jeans",
  "category_id": "5664",
  "product_type": "petite jeans",
  "rating": 4.52,
  "rating_count": 1843,
  "review_count": 1843,
  "review_summary": {
    "summary": "These baggy jeans are loved for their lightweight feel and comfortable fit. The wide-leg style and range of lengths are highlights. Sizing can be inconsistent, so many suggest sizing down. They’re a versatile wardrobe staple.",
    "likes": ["Comfort", "Fabric", "Fit", "Style"],
    "dislikes": []
  },
  "flags": [],
  "excluded_from_promotion": false,
  "max_order_quantity": 5,
  "fully_out_of_stock": false,
  "pickup_available": true,
  "variant_count": 3,
  "variants": [
    {
      "variant": "REGULAR",
      "price": { "min_effective_price": 35, "max_effective_price": 99.95, "min_regular_price": 89.95, "max_regular_price": 99.95, "min_discount_percentage": 17, "max_discount_percentage": 61, "price_types": ["regular", "markdown", "promotion"] },
      "size_label": "Size",
      "size2_label": "Inseam",
      "sizes2": ["Short", "Regular", "Long"],
      "colors": [
        {
          "pid": "403540002",
          "style_id": "403540",
          "name": "Light indigo wash",
          "price": { "min_effective_price": 35, "max_effective_price": 35, "min_regular_price": 89.95, "max_regular_price": 89.95, "min_discount_percentage": 61, "max_discount_percentage": 61, "price_types": ["promotion"] },
          "stock_status": "in_stock",
          "low_stock": false,
          "out_of_stock": false,
          "final_sale": false,
          "flags": ["60% off: really big deal"],
          "badges": ["Best seller"],
          "skus": [
            {
              "sku_id": "4035400023503",
              "size": "35 Long",
              "size_dimension1": "35",
              "size_dimension2": "Long",
              "regular_price": 89.95,
              "effective_price": 35,
              "price_type": "promotion",
              "discount_percentage": 61,
              "discount_saving": 54.95,
              "on_clearance": null,
              "final_markdown": false,
              "stock_status": "in_stock",
              "backordered": false,
              "backorder_date": null,
              "estimated_ship_date": null,
              "upc": "500140532589",
              "retail_upc": "500140533975"
            }
          ]
        }
      ]
    }
  ],
  "country": "us",
  "language": "en",
  "locale": "en_US"
}
```

The REGULAR fit had 14 colors, TALL 4 and PETITE 5, each with its own sizes. `stock_status` is online stock: `on_order` means backordered, with `backorder_date` and `estimated_ship_date` as given. A Banana Republic Hammered Satin Flutter-Sleeve Dress (`{"pid": "1180146012", "brand": "banana_republic"}`) read $139.99 against $248 (`markdown`, 44%) in Cinnamon Bark Brown, sizes 0, 2 and 4 `low_stock` and the rest `out_of_stock`, while its Black color read $148.80 with every size in stock. A dead id is a charged `404`.

### Pickup stock at three stores

```bash
curl -X POST https://api.scavio.dev/api/v1/gap/store-stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_ids": ["220", "1519", "1456"], "sku_ids": ["4035400023503", "4035400023401", "4035400023202", "4035400022601"]}'
```

Captured `data` (2026-11-26; 2 of 4 SKUs shown):

```json
{
  "brand": "gap",
  "brand_name": "Gap",
  "country": "us",
  "store_ids": ["220", "1519", "1456"],
  "sku_ids": ["4035400023503", "4035400023401", "4035400023202", "4035400022601"],
  "sku_count": 4,
  "skus": [
    {
      "sku_id": "4035400023202",
      "stores": [
        { "store_id": "220", "status": "in_stock" },
        { "store_id": "1456", "status": "in_stock" },
        { "store_id": "1519", "status": "out_of_stock" }
      ]
    },
    {
      "sku_id": "4035400023503",
      "stores": [
        { "store_id": "220", "status": "out_of_stock" },
        { "store_id": "1456", "status": "out_of_stock" },
        { "store_id": "1519", "status": "out_of_stock" }
      ]
    }
  ],
  "notes": [
    "status per SKU per store is the site's pickup stock bucket: in_stock, low_stock or out_of_stock. Gap gives no unit counts and no per-store price (an in-store price may differ from the online price).",
    "Sizes and colors of each sku_id are on product (colors[].skus[])."
  ]
}
```

These are four sizes of the Light indigo wash jeans above (35 Long, 34 Short, 32 Regular, 26 Short) at Gap stores 220 (Glendale Galleria, CA), 1519 (Inwood Village, TX) and 1456 (Southport, IL). Only 32 Regular was in stock, at two of the three; 35 Long was in stock online and out at all three. Send `style_id` instead of `sku_ids` for every SKU of a style (each answered with its `pid`, `variant` and `status`).

### Prices for five colors across five banners

```bash
curl -X POST https://api.scavio.dev/api/v1/gap/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"brand": "old_navy", "pid": "903453022"}, "banana_republic:906192032", "athleta:1177198082", "gap_factory:1177187021", "banana_republic_factory:1175510021"]}'
```

Captured `data` (2026-11-26; 1 of 5 items shown, `notes` dropped):

```json
{
  "country": "us",
  "language": "en",
  "locale": "en_US",
  "currency": "USD",
  "requested": 5,
  "found": 5,
  "items": [
    {
      "brand": "old_navy",
      "pid": "903453022",
      "found": true,
      "style_id": "903453",
      "name": "Seaside Cotton Shaker Oversized Tunic Sweater",
      "color": "Hearthwood",
      "category": "Sweaters & Cardigans",
      "url": "https://oldnavy.gap.com/browse/product.do?pid=903453022",
      "currency": "USD",
      "regular_price": 39.99,
      "effective_price": 19.99,
      "max_regular_price": 39.99,
      "max_effective_price": 19.99,
      "percent_off": 50,
      "min_percent_off": 50,
      "price_types": ["promotion"],
      "online_status": "in_stock",
      "rating": 4.13,
      "review_count": 409,
      "flags": ["50% Off Black Friday Deal!"],
      "badges": ["Best Seller"],
      "excluded_from_promotion": false
    }
  ]
}
```

The other four: Banana Republic Merino Wool Crew-Neck Sweater $50 against $90 ("Event Exclusive: price as marked"); Athleta Coaster Luxe Open Cardigan $44.50 against $89 ("50% Off + Extra 10% Off: Code PLUS10" - the code is not in the price); Gap Factory Cashsoft Relaxed Crewneck Sweater $27.99 against $69.99 ("Black Friday doorbuster!"); Banana Republic Factory Cozy Textured Sweater $35 against $90 ("The Find, Extra 25% Off At Checkout"). A color the banner does not have answers `found: false` in place.

### Search, category, categories, stores, store, deals, suggestions, trending and Canada

- `/search` `{"query": "jeans", "page_size": 10}` (Gap): `total` 713, 72 pages; each item a style with `color_count` and `colors[]`, and 17 facets (department, rise, fabric material, length, leg shape, `priceType` REGULAR / PROMO / MARKDOWN, review score, color, ...). `{"query": "sweater", "brand": "old_navy"}` matched 393, the Seaside tunic sweater first.
- `/category` `{"cid": "3033077", "brand": "old_navy"}`: Shop All Clearance, `total_colors` 2,481, 249 pages of 10, each color with `online_units`, `online_status` and `backorder_units`, plus `groups` (sub-groups with color counts) and 31 facets. An unknown cid is a charged `404`.
- `/categories` (Gap): 10 divisions and 302 categories, such as Women > New & Featured > New Arrivals (cid `8792`). A heading without a link has `cid` null.
- `/stores` `{"zip": "10001"}` (Gap): 10 stores nearest first, TIMES SQUARE (store `4132`, 1514 Broadway) at 0.77 miles, each with this week's `hours` ("Mon: 10:00 AM - 1:00 AM"), dated `holiday_hours` ("Thu, Nov 26th: CLOSED" at several stores) and `pickup`.
- `/store` `{"store_id": "4132"}`: status Open, opened 2017-10-25, phone (646) 866-5850, `services` in_store_pickup, order_in_store, ship_from_store. Hours are on `/stores`. An unknown id is a charged `404`.
- `/deals` (Gap): 5 offers, "Black Friday 50% off sitewide Applied at checkout. Exclusions apply.", "60% off really big deals Online only.", "60% off our best jeans Online only.", an app-exclusive extra 10% and a card offer, each `applied` "Applied at checkout"; 16 `deal_links` (Really Big Deals and Sale per division, with their cid). Gap gives no end dates.
- `/suggestions` `{"query": "jea"}`: 10 suggestions (jeans, jeans women, jean shorts, ...) each with department filters, and 6 products with prices.
- `/trending` (Gap): pajamas, hoodie, sweatpants, sweater, disney, cashsoft, socks, easy pant, toddler boy, cardigan.
- Canada: `/search` `{"query": "chandail", "country": "ca", "language": "fr"}` matched 278 on Gap Canada in French, the first "Chandail ras du cou Effet cachemire" at 35 CAD against 89.95 CAD.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def gap(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/gap/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Old Navy clearance sweaters, lowest price first (1 credit)
hits = gap("search", {"query": "sweater", "brand": "old_navy", "sale_type": "clearance", "sort": "price_asc", "page_size": 20})["data"]
for i in hits["items"][:5]:
    print(i["pid"], i["name"], i["effective_price"], i["regular_price"], i["price_type"], i["flags"])

# 2. Every size of one color with its own price and online status (1 credit)
p = gap("product", {"pid": "403540002"})["data"]
for v in p["variants"]:
    for c in v["colors"][:1]:
        for s in c["skus"]:
            print(v["variant"], c["name"], s["size"], s["effective_price"], s["stock_status"], s["sku_id"])

# 3. Pickup buckets at the stores near a ZIP (2 credits)
stores = gap("stores", {"zip": "10001", "limit": 5})["data"]["stores"]
ids = [s["store_id"] for s in stores if s["pickup"]][:10]
skus = [s["sku_id"] for s in p["variants"][0]["colors"][0]["skus"][:20]]
stock = gap("store-stock", {"store_ids": ids, "sku_ids": skus})["data"]
for k in stock["skus"]:
    print(k["sku_id"], [(st["store_id"], st["status"]) for st in k["stores"]])

# Prices and stock change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history (Gap shows
# only the current price and status, and no promotion end dates).
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries the banner (`brand`, `brand_name`) and market (`country`, and on text endpoints `language`, `locale`, `currency`) and `notes`.

- **search** - `query`, `sort`, `page`, `page_size`, `total`, `pages`, `has_more`, `count`, `items[]` {`style_id`, `pid`, `name`, `url`, `regular_price`, `effective_price`, `price_type`, `percent_off`, `regular_price_range`, `sale_price_range`, `rating`, `review_count`, `product_type`, `excluded_from_promotion`, `free_shipping`, `color_count`, `image`, `badges`, `flags`, `colors[]` {`pid`, `name`, `description`, `url`, `regular_price`, `effective_price`, `price_type`, `percent_off`, `badges`, `flags`, `image`}}, `facets[]` {`name`, `label`, `type`, `options[]` {`value`, `label`, `count`}, `range`}.
- **category** - `cid`, `style`, `sort`, `page`, `page_size`, `total_colors`, `pages`, `has_more`, `count`, `items[]` {the item fields, `colors[]` adding `online_units`, `online_status`, `backorder_units`}, `groups[]` {`category_id`, `category_name`, `subcategory_id`, `subcategory_name`, `color_count`}, `facets`.
- **categories** - `url`, `division_count`, `category_count`, `categories[]` {`name`, `type` (`division`, `section`, `category`), `cid`, `style`, `url`, `children`}.
- **product** - `pid`, `style_id`, `name`, `url`, `currency`, `category`, `category_id`, `product_type`, `rating`, `rating_count`, `review_count`, `review_summary` {`summary`, `likes`, `dislikes`}, `highlights`, `details[]` {`section`, `description`, `bullets`}, `flags`, `excluded_from_promotion`, `max_order_quantity`, `fully_out_of_stock`, `pickup_available`, `variant_count`, `variants[]` {`variant`, `price` {`min_effective_price`, `max_effective_price`, `min_regular_price`, `max_regular_price`, `min_discount_percentage`, `max_discount_percentage`, `price_types`}, `size_label`, `sizes`, `size2_label`, `sizes2`, `colors[]` {`pid`, `style_id`, `name`, `url`, `price`, `stock_status`, `low_stock`, `out_of_stock`, `final_sale`, `flags`, `badges`, `swatch_image`, `image`, `skus[]` {`sku_id`, `size`, `size_dimension1`, `size_dimension2`, `regular_price`, `effective_price`, `price_type`, `discount_percentage`, `discount_saving`, `on_clearance`, `final_markdown`, `stock_status` (`in_stock`, `low_stock`, `out_of_stock`, `on_order`), `backordered`, `backorder_date`, `estimated_ship_date`, `upc`, `retail_upc`}}}.
- **prices** - `requested`, `found`, `items[]` {`brand`, `pid`, `found`, `style_id`, `name`, `color`, `category`, `url`, `currency`, `regular_price`, `effective_price`, `max_regular_price`, `max_effective_price`, `percent_off`, `min_percent_off`, `price_types`, `online_status`, `rating`, `review_count`, `flags`, `badges`, `excluded_from_promotion`, `image`}.
- **stores** - `zip`, `latitude`, `longitude`, `radius`, `count`, `stores[]` {`store_id`, `brand`, `brand_name`, `name`, `address` {`lines`, `city`, `state`, `postal_code`, `country`}, `phone`, `latitude`, `longitude`, `distance_mi`, `time_zone`, `hours`, `holiday_hours`, `pickup`}.
- **store** - `store_id`, `name`, `status`, `opened`, `address`, `phone`, `latitude`, `longitude`, `time_zone`, `languages`, `pickup`, `services`.
- **store-stock** - `store_ids`, `sku_ids` or `style_id`, `sku_count`, `skus[]` {`sku_id`, (`pid`, `variant`, `status` for a style), `stores[]` {`store_id`, `status`}}.
- **suggestions** - `query`, `count`, `suggestions[]` {`query`, `display_query`, `filters[]` {`key`, `value`, `name`}}, `product_count`, `products[]` {`pid`, `name`, `url`, `regular_price`, `effective_price`, `price_type`, `sale_price_range`, `colors`, `image`}.
- **trending** - `count`, `searches`.
- **deals** - `url`, `offer_count`, `offers[]` {`promo_id`, `text`, `message`, `applied`, `links[]` {`name`, `cid`, `url`}}, `deal_link_count`, `deal_links[]` {`name`, `path`, `cid`, `style`, `url`}.

## Guardrails

- Name it "Gap Inc. (gap.com: Gap, Old Navy, Banana Republic, Athleta and the factory stores)" on first mention, and name the banner of every price.
- Prices: quote `effective_price` and `regular_price` with Gap's `price_type` and `percent_off`, the banner, the market and the `fetched_at` date. They are online prices: never call one a store's price.
- Checkout codes: report a code or "at checkout" offer as Gap's text from `flags` or `deals`, and never compute or claim a price after it. Gap gives no promotion end dates: never state one.
- Report Gap's labels and the numbers only. Never judge a list price, a discount or a clearance price, and never describe how often an item is on sale.
- Stock: report store stock as Gap's bucket (`in_stock`, `low_stock`, `out_of_stock`) at the moment of the call, never as a count; `online_units` is online stock, not store stock. Scavio makes no promise of its accuracy, and Gap's own terms say availability is not guaranteed. Never promise pickup.
- Comparing banners or markets: compare only the same `pid` on the same banner over time, or label different products as different. Never carry a US price to Canada or the reverse, and never convert currencies.
- Reviews: only the rating, counts and Gap's own `review_summary` are returned; quote the summary as Gap's, never as Scavio's finding.
- Not available: review texts, store unit counts, per-store prices, promotion end dates, price history (poll and store), gap.co.jp and franchise sites, loyalty or credit card member prices, checkout, cart or ordering. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store Gap Inc. data: each call fetches the public Gap Inc. page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Gap's terms of use say its sites are intended for personal, non-commercial use; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Gap product photos or logos; link products by `url` instead.
- Never fabricate prices, sizes, stock statuses, ids, store hours, promotions or ratings. Only return what the API returned, with the `fetched_at` time, the banner, the market and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `brand`, `country`, `sort` or `sale_type` outside its list; "language fr is served on country ca only (the Canadian site); the US site is English only."; a `pid` that is not 9-11 digits; both or neither of `pid` and `url` ("send one of pid (...) or url (a product link).") or of `cid` and `url`; a `url` that is not a product or category link of a Gap Inc. site, or "brand does not match the link's site; send one or the other."; `facets` that are not names and values from an answer, or more than 10; "min_price must not be above max_price."; more than 100 price items or an item without its brand; "zip must be a US ZIP code (5 digits, e.g. 10001) for country us." / "zip must be a Canadian postal code (A1A 1A1, e.g. M5V 2T6) for country ca."; both or neither of `zip` and a point; more than 10 store ids or 20 SKU ids, or both or neither of `sku_ids` and `style_id`. A request Gap itself refuses answers "Gap refused this request. Check the ids and filters (filter names and values come from an answer's facets)." and is not charged.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Page N is past the last page of results for this search (or the search has no results).", "Gap has no category <cid> on this banner and market, or page N is past its last page.", "Gap has no product <pid> on <banner> (<country>).", "None of these products was found.", "Gap found no store near this place.", "Gap has no store <id> in this market. Use stores for store ids.", "Gap has no store stock for these ids.", "No suggestions.", "No trending searches.". Ids are per banner and market: take them from a previous answer on the same banner and market.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api).
- `502` means Gap data was temporarily unavailable ("Gap is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Gap is busy ("Gap is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.gap.search({ query: "jeans", sort: "price_asc" });
const { data: onavy } = await scavio.gap.search({ query: "sweater", brand: "old_navy", sale_type: "clearance" });
const { data: product } = await scavio.gap.product({ pid: "403540002" });
const { data: prices } = await scavio.gap.prices({ items: [{ brand: "old_navy", pid: "903453022" }, "athleta:1177198082"] });
const { data: stores } = await scavio.gap.stores({ zip: "10001" });
const { data: store } = await scavio.gap.store({ store_id: "4132" });
const { data: stock } = await scavio.gap.storeStock({ store_ids: ["220", "1519", "1456"], sku_ids: ["4035400023202"] });
const { data: tree } = await scavio.gap.categories({ brand: "old_navy" });
const { data: clearance } = await scavio.gap.category({ cid: "3033077", brand: "old_navy" });
const { data: deals } = await scavio.gap.deals({ brand: "gap" });
const { data: sugg } = await scavio.gap.suggestions({ query: "jea" });
const { data: trending } = await scavio.gap.trending({ brand: "gap" });
const { data: canada } = await scavio.gap.search({ query: "chandail", country: "ca", language: "fr" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.gap.search(...)`, `category`, `categories`, `product`, `prices`, `stores`, `store`, `store_stock`, `suggestions`, `trending` and `deals`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_gap`, `get_gap_category`, `get_gap_categories`, `get_gap_product`, `get_gap_prices`, `get_gap_stores`, `get_gap_store`, `get_gap_store_stock`, `get_gap_suggestions`, `get_gap_trending` and `get_gap_deals`. Gap Inc. is opt-in: add `gap` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,gap"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/gap-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [category](https://scavio.dev/docs/gap-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [categories](https://scavio.dev/docs/gap-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [product](https://scavio.dev/docs/gap-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [prices](https://scavio.dev/docs/gap-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [stores](https://scavio.dev/docs/gap-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [store](https://scavio.dev/docs/gap-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [store stock](https://scavio.dev/docs/gap-store-stock?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [suggestions](https://scavio.dev/docs/gap-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [trending](https://scavio.dev/docs/gap-trending?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api), [deals](https://scavio.dev/docs/gap-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api). Overview: [Gap Inc. API](https://scavio.dev/gap-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=gap-old-navy-api).
