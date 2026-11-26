---
name: academy-sports-api
description: Academy Sports + Outdoors API for Academy (academy.com, the US sporting goods retailer; 21 states, USD) - Academy prices and store stock, every variant of a product with its own price, Academy's struck-through price, saving, percent off, UPC and online units (the YETI DuraCoat Rambler 20 oz Tumbler read 24 variants from $19.97 to $40, one color $24.50 against $35, 30% off, with 1,482 units to ship), the exact units of every variant at one Academy store for pickup (store 19 in Houston, TX held 51 units across 14 of the 24 variants), and the ship-to-store units and the nearest other store with stock; prices are national (the same at every store); keyword search, category listings and the Hot Deals, Clearance, Black Friday (with its sub-shops) and Flash Sale listings, 29 organic results per page with total and pages, sponsored placements kept apart, sorted by relevance, best selling, newest, top rated or price and filtered by any facet (brand, product type, color, deals, size) and a price range; Academy's minimum-advertised-price flag where the lowest price shows only in the cart; firearms and ammunition with Academy's own notices and flags, as Academy presents them; stores near a ZIP or a point with hours, services and pickup flags, up to 20 stores by id; the category navigation and search suggestions. 9 endpoints, 1 credit per call. No review text (rating and count only), weekly ad, price history or checkout.
version: 1.0.0
tags: academy, academy-sports, academy-sports-outdoors, academy-com, academy-api, academy-sports-api, academy-prices, academy-store-stock, academy-in-stock, academy-store-availability, academy-inventory, academy-deals, academy-hot-deals, academy-clearance, academy-black-friday, academy-flash-sale, academy-stores, academy-store-hours, academy-categories, academy-search, academy-suggestions, sporting-goods, outdoor-gear, hunting, fishing, camping, coolers, drinkware, athletic-shoes, fitness, per-variant-prices, store-stock, inventory, upc, variant-data, clearance-tracker, price-monitoring, product-search, product-data, category-browse, us-retail, usd, agents, ai-agents, structured-data, json, mcp
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 180
    throttle: 1
    homepage: https://scavio.dev/academy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api
---

# Academy Sports + Outdoors API - Prices, Store Stock, Deals

Read Academy Sports + Outdoors (academy.com, the US sporting goods retailer): keyword search, category listings and the deal listings, one product with every variant's own price, UPC and online units, the exact units of every variant at one Academy store, the Academy stores near a ZIP or a point, up to 20 stores by id, the category navigation and search suggestions. www.academy.com only (US, USD, English). Every endpoint returns structured JSON at 1 credit per call.

**The job this skill is for: Academy prices and store stock.** What a product costs at academy.com today, variant by variant, and how many of each variant one store has for pickup. On 2026-11-26 the YETI DuraCoat Rambler 20 oz Tumbler (part number `111805768`) read 24 variants (color and volume) from $19.97 to $40, with `map_price_applies` true (Academy shows the lowest price only in the cart). One color, 20 oz Pace Purple, read $24.50 against Academy's $35, a saving of $10.50 and 30% off, with 1,482 units Academy can ship; another, 20 oz Wild Rose, read $35 at the regular price. `/store-availability` at store 19 (Houston, TX) answered 51 units across 14 of the 24 variants: 5 of one variant ("In-Store Pickup Available"), 2 of another ("Limited Stock!"). Pair it with `dicks-sporting-goods-api` for the same item at Dick's, and with `amazon-product-data`, `walmart-product-data` and `target-product-data` for the same UPC elsewhere.

Eight limits shape every answer, so say them plainly:
- **1 credit per call.** Every endpoint is 1 credit. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Prices are national.** Academy shows the same price at every store; there is no store or ZIP input on any priced endpoint. Report "$24.50 at academy.com on 2026-11-26", never a store's price.
- **Prices are per variant.** A product's `price` {`min`, `max`} spans its variants; each `variants[]` entry has its own `price`, `was_price`, `saving` and `percent_off`. Read the variant you need. On a list, an item's `was_price`, `saving` and `percent_off` are those of the tile's default variant, as Academy lists them.
- **Cart-only prices are flagged.** `price_in_cart` (list items) and `map_price_applies` (product) are `true` where Academy shows the lowest price only in the cart (minimum advertised price); `price` is that price as the page carries it. Say so when quoting it.
- **Store stock is exact units per variant at ONE store.** `/store-availability` takes the part number, a `store_id` and the store's `state`, and returns `in_store_units` per variant (0 when the store has none). `ship_to_store_units` are units Academy can ship to that store, not units at the store. Academy does not check `store_id`: an id it has no store for reads as not available for every variant, so take `store_id` from `/stores`.
- **29 organic results per page.** Search, category and deals pages carry up to 29 organic results with `total`, `total_pages` and `has_more`; `sponsored` holds the paid placements apart (they repeat across pages). Pages go to 500; a page past the last returns an empty `items` list.
- **No review text.** Rating and review count only, on lists and products. There is no reviews endpoint.
- **No dates per deal item, no weekly ad, no history.** Deal listings carry no end date per item; `site_banner` is the schedule of the banner the page shows, and a product's `price_valid_until` and `rebate` dates come with `/product`. Nothing is cached or kept: poll and store your own series.

Academy has no public API for its catalog, prices or store stock; it runs an affiliate program (a links program, not a price API). Prices and store availability are shown on academy.com for the store you pick, and this skill reads those public pages with one Scavio key.

Academy Sports + Outdoors says it had 324 stores across 21 states as of April 23, 2026 (investors.academy.com). Quote this with its source, never from the samples.

See also: for the same item at Dick's Sporting Goods use `dicks-sporting-goods-api`; at Amazon `amazon-product-data`; at Walmart `walmart-product-data`; at Target `target-product-data`; prices across retailers `google-shopping-api`; per-store stock at other retailers `home-depot-product-data`, `staples-ink-prices-api`.

## When to trigger

Use this skill when the user asks to:
- Price a product at Academy Sports + Outdoors, every color and size with its own price, Academy's struck-through price and percent off
- Check how many units of each variant one Academy store has for pickup, or whether Academy can ship it to that store
- Search academy.com by keyword, sorted by best selling, newest, top rated or price, or filtered by brand, product type, color, deals, size or a price range
- List an Academy category (Coolers, Men's Running Shoes) with its subcategories and facets
- Read Academy's Hot Deals, Clearance, Black Friday (or one Black Friday sub-shop) or Flash Sale listings
- Read one Academy product in full: description, features, specifications, what's in the box, rebate, Academy's notices and warnings, and every variant with UPC and online units
- Find the Academy stores near a US ZIP code or a point, or read up to 20 stores by id with hours, services and pickup flags
- Read Academy's category navigation or its search suggestions for a partial query
- Compare one item at Academy and Dick's Sporting Goods (with `dicks-sporting-goods-api`) or at Amazon, Walmart and Target by UPC

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api) - email or Google, no card required.
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

Base URL: `https://api.scavio.dev`. In the captures, stores, store and store-availability took under 1 second, categories and suggestions 1-2, category and search 3-4, a product about 5 and the Black Friday deals about 7. Allow a client timeout of at least 180 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/academy/search` | Keywords: 29 organic results per page with total and pages, sponsored placements apart, facets, subcategories | 1 |
| `POST /api/v1/academy/product` | One product by link or slug: price range, every variant with its own price, struck-through price, saving, percent off, UPC, online units and flags; rebate, notices, warnings, features, specifications | 1 |
| `POST /api/v1/academy/store-availability` | Exact units of every variant of one product at one store for pickup, ship-to-store units, the nearest other store with stock | 1 |
| `POST /api/v1/academy/stores` | The Academy stores near a US ZIP or a point, nearest first, with hours, services and pickup flags | 1 |
| `POST /api/v1/academy/store` | 1 to 20 stores by id, in the order asked, with `not_found` for unknown ids | 1 |
| `POST /api/v1/academy/category` | One category by path or link, sorted and filtered like search | 1 |
| `POST /api/v1/academy/categories` | The category navigation as the site's header shows it: departments, groups, links | 1 |
| `POST /api/v1/academy/deals` | Hot Deals (default), Clearance, Black Friday (and one sub-shop) or the Flash Sale, sorted and filtered like search | 1 |
| `POST /api/v1/academy/suggestions` | Search-box keyword completions and products for a partial query, optionally popular searches | 1 |

US only (www.academy.com, USD). There is no `country` parameter.

## Prices: per variant, struck-through price, cart-only prices

Every list item carries:

| Field | Meaning |
|---|---|
| `price`, `price_max` | The current price as the tile shows it, and the top of its variant range |
| `was_price`, `saving`, `percent_off` | Academy's struck-through price for the tile's default variant, the saving and the percent off, as Academy lists them; `null` without one |
| `price_in_cart` | `true` where Academy shows the lowest price only in the cart (minimum advertised price) |
| `promotion` | {`message`, `promo_price`} where Academy shows one; `null` otherwise |
| `badges` | Academy's deal tags as given ("Hot Deal", "Clearance", "New Colors", "Ships to Store") |
| `default_variant` | {`item_id`, `sku`, `attributes`, `url`} of the variant the tile shows |

Every product variant (`variants[]`) carries its own `price`, `was_price`, `saving`, `percent_off`, `price_type` (`REGULAR`, `MAP` and others as given), `savings_text`, `unit_price_text` (where Academy states one, such as a price per round), `price_valid_until` (as the page gives it), `is_clearance`, `upc`, `online_units` (units Academy can ship) and `online_status`.

- **National:** one price per variant on academy.com. Report it with the date and the variant (color, size); never per store.
- **Per variant:** the YETI tumbler's 24 variants on 2026-11-26 ranged from $19.97 to $40; 2 were flagged `is_clearance`. A list's `price` and `price_max` give the range; the product gives each variant.
- **Cart-only:** where `price_in_cart` or `map_price_applies` is `true`, say that Academy shows this price only in the cart.
- Report Academy's labels and the arithmetic only. Never judge a struck-through price, a discount or a deal, and never describe how often an item is on sale.

## Workflow

1. **Find the item.** `/search` with `query`, or `/category` (a `path` from `/categories` or from `subcategories[].path`) or `/deals`. Each item's `slug` (or `url`) is the input of product; its `part_number` is the input of store-availability.
2. **Read it in full.** `/product` with `slug` or `url`: every variant with its own price, UPC and online units, plus rebate, notices and warnings.
3. **Pick a store.** `/stores` with `zip` (or `latitude` and `longitude`) and `radius` (miles, default 50, up to 250). Each store gives `store_id` and `address.state`.
4. **Units at that store.** `/store-availability` with `part_number`, `store_id` and `state`. Read `in_store_units` per variant, `variants_in_stock_at_store` and `in_store_units_total`; match variants to the product by `item_id`. Repeat per store to compare stores.
5. **Narrow a list.** `sort`, `facets` (`{facets[].id: values[].value}` exactly as an earlier answer gives them, up to 10 facets with up to 10 values each), `min_price` / `max_price`; `page` (1-500).
6. **Deals.** `/deals` with `type` `hot_deals`, `clearance`, `black_friday` or `flash_sale`; for one Black Friday sub-shop send `sub_shop` (a `sub_shops[].slug` of a `black_friday` answer).
7. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | An academy.com product link (`https://www.academy.com/p/<slug>`); a `?sku=` in it is not needed, every variant is returned |
| `slug` | string | one of | The product slug (`items[].slug`, the part after `/p/`), e.g. `yeti-duracoat-rambler-20-oz-tumbler` |

### Store availability (`/store-availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `part_number` | string | required | The product's part number, digits (`111805768`: `items[].part_number` or the product's `part_number`) |
| `store_id` | string or integer | required | The store (`stores[].store_id`): `19`, `0019` and `store-0019` all work |
| `state` | string | required | The store's state (`stores[].address.state`): one of AL, AR, FL, GA, IL, IN, KS, KY, LA, MD, MS, MO, NC, OH, OK, PA, SC, TN, TX, VA, WV |

### Search (`/search`), category (`/category`), deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | search: required | Keywords, 1-200 chars |
| `path` | string | category: one of | A category path (`/c/outdoors/coolers`), as categories and `subcategories[].path` give it |
| `url` | string | category: one of | An academy.com category link (its query string is not read: send filters in `facets`) |
| `type` | string | `hot_deals` | Deals: `hot_deals`, `clearance`, `black_friday` or `flash_sale` |
| `sub_shop` | string | none | Deals, `black_friday` only: one `sub_shops[].slug` (e.g. `black-friday-hunting-deals`) |
| `sort` | string | `relevance` | `relevance`, `best_selling`, `newest`, `top_rated`, `price_asc`, `price_desc` (Academy's own price order, by its list price: promotions and cart prices can sit slightly out of order) |
| `facets` | object | none | `{facets[].id: value or list}` from a previous answer, e.g. `{"facet_Brand": "Yeti"}`, `{"facet_Deals": "Clearance"}`. Values are case-sensitive (`Yeti` and `YETI` differ); facets combine |
| `min_price`, `max_price` | number | none | Price range in USD (0-100000). Not together with `facets.facet_Price` |
| `page` | integer | 1 | 1-500; up to 29 organic results per page |

### Stores (`/stores`), store (`/store`), categories (`/categories`), suggestions (`/suggestions`)

`/stores` takes `zip` (a 5-digit US ZIP) or `latitude` + `longitude` (not both) and `radius` (1-250 miles, default 50). `/store` takes `store_ids`: 1 to 20 ids, a list or a comma-separated string. `/categories` takes nothing. `/suggestions` takes `query` (1-100 chars) and `include_popular` (boolean, default false) for the site's popular searches.

## Examples

### One product with every variant's price and online units

```bash
curl -X POST https://api.scavio.dev/api/v1/academy/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "yeti-duracoat-rambler-20-oz-tumbler"}'
```

Captured `data` (2026-11-26; `description`, `images`, `features`, `whats_in_the_box` dropped, `specifications` cut to 4 of 12, `variants` to 2 of 24, `images` per variant dropped, `notes` cut to 3 of 5):

```json
{
  "id": "4179734",
  "part_number": "111805768",
  "name": "The YETI DuraCoat Rambler 20 oz Tumbler",
  "brand": "Yeti",
  "slug": "yeti-duracoat-rambler-20-oz-tumbler",
  "url": "https://www.academy.com/p/yeti-duracoat-rambler-20-oz-tumbler",
  "breadcrumbs": [
    { "name": "Outdoors", "path": "/c/outdoors" },
    { "name": "Outdoor + Insulated Drinkware", "path": "/c/outdoors/insulated-drinkware" },
    { "name": "Tumblers + Cups", "path": "/c/outdoors/insulated-drinkware/tumblers--cups" }
  ],
  "rating": 4.7,
  "review_count": 29355,
  "price": { "min": 19.97, "max": 40, "map_price_applies": true, "currency": "USD" },
  "badges": ["Clearance", "Hot Deal"],
  "ecom_code": "01 SELL ONLINE",
  "product_type": "standard",
  "special_order": false,
  "is_firearm": false,
  "is_ammo": false,
  "returnable": true,
  "shippable": true,
  "notices": [],
  "warnings": [],
  "rebate": null,
  "promotion": null,
  "option_axes": ["Color", "Volume"],
  "specifications": {
    "Product Type": "Tumblers",
    "Capacity (oz.)": "20",
    "Manufacturer warranty - general": "5-year Limited",
    "Product weight (oz.)": "14.4"
  },
  "selected_variant": "93599526",
  "variant_count": 24,
  "variants": [
    {
      "sku_id": "93599526",
      "item_id": "168285257",
      "manufacturer_item_id": "21071509314",
      "sku": "20-oz-wild-rose",
      "url": "https://www.academy.com/p/yeti-duracoat-rambler-20-oz-tumbler?sku=20-oz-wild-rose",
      "attributes": { "Volume": "20 Oz", "Color": "Wild Rose" },
      "upc": "0888830705551",
      "price": 35,
      "was_price": null,
      "saving": null,
      "percent_off": null,
      "price_type": "REGULAR",
      "savings_text": null,
      "unit_price_text": null,
      "price_valid_until": "2026-11-27",
      "availability": "InStock",
      "badges": ["New"],
      "is_clearance": false,
      "pickup_eligible": true,
      "ship_to_store_eligible": true,
      "free_shipping": true,
      "same_day_delivery": true,
      "rebate": null,
      "online_units": 1535,
      "online_status": "IN_STOCK",
      "add_to_cart": true,
      "special_order": false,
      "online_message": "In Stock Online",
      "online_message_detail": "Usually leaves warehouse in 3-4 business days"
    },
    {
      "item_id": "166849590",
      "sku": "20-oz-pace-purple",
      "price": 24.5,
      "was_price": 35,
      "saving": 10.5,
      "percent_off": 30,
      "price_type": "MAP",
      "savings_text": null,
      "is_clearance": false,
      "online_units": 1482,
      "online_status": "IN_STOCK"
    }
  ],
  "notes": [
    "Prices are in US dollars and national: Academy shows the same price at every store.",
    "map_price_applies true: Academy shows the lowest price only in the cart (minimum advertised price).",
    "Reviews: rating and review_count only (review text is not available)."
  ]
}
```

(The second variant is trimmed to its price fields.) $35 - $24.50 = $10.50, 30% off, as Academy lists it for 20 oz Pace Purple. An unknown product is a charged `404` ("No Academy product at this link.").

Firearms and ammunition are listed as Academy presents them: the product carries `is_firearm` or `is_ammo`, and `notices` and `warnings` hold Academy's own text, as given. A handgun captured on 2026-11-26 read `ecom_code` "04 DROP SHIP", `special_order` true, `returnable` false, `shippable` false, `online_units` 0 and `online_message` "Special Order Ships to Store Not Available", with Academy's notice "Firearms purchased online are shipped to your local Academy Sports + Outdoors as selected in the checkout process." Quote these fields as given and add nothing.

### Units of every variant at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/academy/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"part_number": "111805768", "store_id": "19", "state": "TX"}'
```

Captured `data` (2026-11-26; 2 of 24 variants shown, `notes` cut to 3 of 6):

```json
{
  "part_number": "111805768",
  "store": { "store_id": "19", "state": "TX", "pickup_eligible": true, "ship_to_store_eligible": true },
  "count": 24,
  "variants_in_stock_at_store": 14,
  "in_store_units_total": 51,
  "variants": [
    {
      "item_id": "111805776",
      "sku_id": "4179736",
      "store_status": "AVAILABLE",
      "store_message": "In-Store Pickup Available",
      "fulfillment": "BOPIS",
      "in_store_units": 5,
      "ship_to_store_units": null,
      "available_today_units": null,
      "nearest_store_with_stock": null,
      "online_units": 3374,
      "online_status": "IN_STOCK",
      "add_to_cart": true,
      "special_order": false,
      "is_clearance": false,
      "online_message": "In Stock Online"
    },
    {
      "item_id": "111805792",
      "sku_id": "4179740",
      "store_status": "LIMITED STOCK",
      "store_message": "Limited Stock!",
      "fulfillment": "BOPIS",
      "in_store_units": 2,
      "ship_to_store_units": null,
      "available_today_units": null,
      "nearest_store_with_stock": null,
      "online_units": 43,
      "online_status": "IN_STOCK",
      "add_to_cart": true,
      "special_order": false,
      "is_clearance": false,
      "online_message": "In Stock Online"
    }
  ],
  "notes": [
    "in_store_units: the exact units the chosen store holds for pickup (fulfillment BOPIS); 0 when the store has none.",
    "ship_to_store_units (fulfillment STS): units Academy can ship to this store from its distribution pool, not units at the store.",
    "Academy does not check store_id: an id it has no store for reads as not available for every variant, so take store_id from stores."
  ]
}
```

Store 19 (Houston, TX) held 51 units across 14 of the 24 variants. `fulfillment` is `BOPIS` (units at the store), `STS` (ship to store: `ship_to_store_units`) or `LSI` (in-store-only items: `available_today_units`). `nearest_store_with_stock` {`store_id`, `units`, `inventory_type`, `status`, `as_of`} names the nearest other store with units of that variant. An unknown part number is a charged `404` ("Academy knows no variant of this part number.").

### Stores near a ZIP

```bash
curl -X POST https://api.scavio.dev/api/v1/academy/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "77098", "radius": 25}'
```

Captured `data` (2026-11-26; 1 of 24 stores shown, `hours_by_day` cut to 2 of 7, `nearby_store_ids` to 4 of 16):

```json
{
  "zip": "77098",
  "latitude": 29.735,
  "longitude": -95.416,
  "radius_miles": 25,
  "count": 24,
  "stores": [
    {
      "store_id": "19",
      "name": "Academy Sports + Outdoors 0019",
      "address": { "street": "2404 Southwest Frwy", "city": "Houston", "state": "TX", "zip": "77098" },
      "neighborhood": "Kirby",
      "phone": "(713) 874-6020",
      "latitude": 29.73234804104351,
      "longitude": -95.41588559746737,
      "distance_miles": 0.18,
      "status": "Closed",
      "today": "Closed Today",
      "next_change": "Opens at 5:00 AM",
      "today_date": "2026-11-26",
      "time_zone_utc_offset": "-06:00",
      "hours": "Sun. 9am-9pm Mon. 8am-10pm Tues. 8am-10pm Weds. 8am-10pm Thurs. Closed Fri. 5am-11pm Sat. 8am-11pm",
      "hours_by_day": [
        { "day": "Thursday", "hours": "Closed" },
        { "day": "Friday", "hours": "5:00 am - 11:00 pm" }
      ],
      "services": ["Hunting and Fishing Licenses", "Line Spooling", "Bore-sighting and Scope Mounting", "Propane Exchange", "Product Delivery and Assembly"],
      "pickup_eligible": true,
      "ship_to_store_eligible": true,
      "special_order_eligible": true,
      "doordash_eligible": true,
      "temporarily_closed": false,
      "future_store": false,
      "nearby_store_ids": ["337", "116", "35", "10"]
    }
  ],
  "notes": [
    "Academy has stores in 21 US states; a location with none within the radius returns an empty list.",
    "hours and status are each store's own, as academy.com gives them (local time)."
  ]
}
```

Thanksgiving Day: every store read Closed, and the data was still returned. `/store` `{"store_ids": ["19", "327", "256"]}` answered Houston, TX (2404 Southwest Frwy), Dunwoody, GA (130 Perimeter Center West) and Orlando, FL (3557 Gardens Ridge Way) in that order, with `not_found` empty.

### Search, category, categories, deals and suggestions

- `/search` `{"query": "yeti tumbler"}`: `total` 140, 29 per page, 5 pages; The YETI DuraCoat Rambler 20 oz Tumbler (`111805768`) first at $19.97 to $40, `was_price` $35, `saving` $15.03, 43% off, `price_in_cart` true, badges Hot Deal, New Colors, Clearance, 24 colors; YETI Rambler 40 oz Travel Straw Mug $29.97 (was $55, 38% off). 6 facets: Product Type, Brand, Color (`facet_IndustrySubGroup`), Deals, Volume, Price.
- `/category` `{"path": "/c/outdoors/coolers"}`: Coolers, `total` 394, 14 pages, 2 sponsored placements kept apart, 9 subcategories (Hard Sided Coolers, Soft Sided Coolers, Coolers on Sale, Wheeled Coolers, ...) and 11 facets; YETI Roadie 15 Hard Cooler $140 first. An unknown category is a charged `404` ("No Academy category at this path.").
- `/categories`: 13 departments, 99 groups and 685 links (Holiday Gift Guide, Deals + Clearance, New + Trending, Men's, Women's, Kids', Shoes + Boots, Outdoors, Firearms + Ammo, Sports, Home + Recreation, Health + Fitness, Fan Shop). Any `path` works in category.
- `/deals` `{"type": "black_friday"}`: Black Friday Sale 2026, `total` 1,262, 44 pages, 9 `sub_shops` (Black Friday Hunting Deals `black-friday-hunting-deals`, Black Friday Deals on Grills and Smokers `black-friday-grills-smokers`, ...; two had no slug), `site_banner` 2026-11-26T00:00:00 to 2026-11-26T23:59:00; Pit Boss Navigator 1000 Wood Pellet Grill $399.99 (was $999.99, 60% off) first.
- `/suggestions` `{"query": "yeti"}`: 8 completions (yeti, yeti cooler, yeti cups, yeti rambler, yeti tumbler, yeti bucket, yeti bag, yeti lunch box) and 8 products, the DuraCoat Rambler 20 oz first at $19.97.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def academy(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/academy/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. Find the product (1 credit)
hits = academy("search", {"query": "yeti tumbler", "sort": "price_asc"})["data"]
item = hits["items"][0]
print(item["name"], item["price"], item["was_price"], item["price_in_cart"])

# 2. Every variant with its own price and online units (1 credit)
p = academy("product", {"slug": item["slug"]})["data"]
by_item = {v["item_id"]: v for v in p["variants"]}
for v in p["variants"]:
    print(v["attributes"], v["price"], v["was_price"], v["percent_off"], v["online_units"])

# 3. The stores near a ZIP, then units per variant at the nearest (2 credits)
store = academy("stores", {"zip": "77098"})["data"]["stores"][0]
stock = academy("store-availability", {
    "part_number": p["part_number"],
    "store_id": store["store_id"],
    "state": store["address"]["state"],
})["data"]
for v in stock["variants"]:
    print(v["item_id"], v["store_status"], v["in_store_units"])
print("total at store", stock["in_store_units_total"])

# Prices and units can change between calls. Store each answer with fetched_at
# and run this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Most `data` objects carry `notes`.

- **item** (search, category, deals, suggestions products) - `position`, `id`, `part_number`, `name`, `brand`, `slug`, `url`, `image`, `price`, `price_max`, `was_price`, `saving`, `percent_off`, `price_in_cart`, `promotion` {`message`, `promo_price`}, `rating`, `review_count`, `badges`, `color_count`, `ecom_code` (as given: 01 SELL ONLINE, 02 DISPLAY ONLY, 04 DROP SHIP...), `special_order`, `ships_to_store`, `same_day_delivery`, `free_shipping`, `default_variant` {`item_id`, `sku`, `attributes`, `url`}, `sponsored`, `ad_position`.
- **lists** - `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sort`, `items[]`, `sponsored[]`, `facets[]` {`id`, `label`, `values[]` {`value`, `label`, `count`, `selected`}}, `subcategories[]` {`id`, `name`, `path`, `url`, `image`}, `title`, `page_category_id`, `did_you_mean`, `filters_applied`. Search adds `query`; category `path`, `url`; deals `type`, `sub_shop`, `path`, `url`, `sub_shops[]` {`id`, `name`, `path`, `url`, `image`, `slug`}, `site_banner[]` {`starts_at`, `ends_at`}.
- **product** - `id`, `part_number`, `name`, `brand`, `slug`, `url`, `description`, `breadcrumbs[]` {`name`, `path`}, `images`, `rating`, `review_count`, `price` {`min`, `max`, `map_price_applies`, `currency`}, `badges`, `ecom_code`, `product_type`, `special_order`, `is_firearm`, `is_ammo`, `returnable`, `shippable`, `notices`, `warnings`, `rebate` {`text`, `starts_at`, `ends_at`, `link`}, `promotion`, `option_axes`, `features`, `specifications`, `whats_in_the_box`, `selected_variant`, `variant_count`, `variants[]` {`sku_id`, `item_id`, `manufacturer_item_id`, `sku`, `url`, `attributes`, `upc`, `price`, `was_price`, `saving`, `percent_off`, `price_type`, `savings_text`, `unit_price_text`, `price_valid_until`, `availability`, `image`, `images`, `badges`, `is_clearance`, `online_only`, `pickup_eligible`, `ship_to_store_eligible`, `free_shipping`, `same_day_delivery`, `rebate`, `online_units`, `online_status`, `add_to_cart`, `special_order`, `online_message`, `online_message_detail`}.
- **store-availability** - `part_number`, `store` {`store_id`, `state`, `pickup_eligible`, `ship_to_store_eligible`}, `count`, `variants_in_stock_at_store`, `in_store_units_total`, `variants[]` {`item_id`, `sku_id`, `store_status`, `store_message`, `fulfillment`, `in_store_units`, `ship_to_store_units`, `available_today_units`, `nearest_store_with_stock` {`store_id`, `units`, `inventory_type`, `status`, `as_of`}, `online_units`, `online_status`, `add_to_cart`, `special_order`, `is_clearance`, `online_message`}.
- **stores** - `zip`, `latitude`, `longitude`, `radius_miles`, `count`, `stores[]` {`store_id`, `name`, `address` {`street`, `city`, `state`, `zip`}, `neighborhood`, `phone`, `latitude`, `longitude`, `distance_miles`, `status`, `today`, `next_change`, `today_date`, `time_zone_utc_offset`, `hours`, `hours_by_day[]` {`day`, `hours`}, `services`, `pickup_eligible`, `ship_to_store_eligible`, `special_order_eligible`, `doordash_eligible`, `temporarily_closed`, `future_store`, `nearby_store_ids`}.
- **store** - `requested_ids`, `count`, `stores[]` (the stores fields, distance excepted), `not_found`.
- **categories** - `count`, `group_count`, `link_count`, `departments[]` {`name`, `path`, `url`, `id`, `children[]` {..., `children`}}.
- **suggestions** - `query`, `count`, `suggestions`, `products[]` (item fields), `popular_searches` (with `include_popular`).

## Guardrails

- Name it "Academy Sports + Outdoors (academy.com, the US sporting goods retailer)" on first mention.
- Prices: quote `price` and `was_price` per variant with the variant's attributes, academy.com and the `fetched_at` date. Prices are national: never call a price a store's price. Where `price_in_cart` or `map_price_applies` is `true`, say Academy shows that price only in the cart.
- Report Academy's labels (badges, `price_type`, `price_valid_until`, rebate dates) and the arithmetic only. Never judge a struck-through price, a discount or a deal, and never describe how often an item is on sale.
- Stock: `in_store_units` as Academy reported them for that store at the moment of the call; Scavio makes no promise of their accuracy. Keep `ship_to_store_units` apart from units at the store. Never promise pickup or delivery.
- Firearms and ammunition: describe them only as Academy presents them. Quote `is_firearm`, `is_ammo`, `notices`, `warnings` and the availability fields as given; add no commentary, advice or opinion of your own.
- Reviews: rating and review count only; no review text exists in this API.
- Comparing Academy with Dick's, Amazon, Walmart or Target: compare only the same item (same UPC or manufacturer item number), each with its date. Never call one retailer cheaper beyond the numbers shown.
- Not available: review text, a weekly ad, an end date per deal item, price history (poll and store), member or cart prices beyond the flags shown, checkout, cart or ordering. This API cannot reserve, add to cart or buy.
- Terms: Scavio does not collect or store Academy data: each call fetches the public Academy Sports + Outdoors page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Academy's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice. Do not republish Academy product photos or logos; link products by `url` instead.
- Never fabricate prices, units, part numbers, store ids, hours, dates, badges or ratings. Only return what the API returned, with the `fetched_at` time and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "url or slug is required", "Pass url or slug, not both.", a `slug` that is not an Academy product slug, "url must be an Academy product link (https://www.academy.com/p/<slug>)."; a `part_number` that is not digits; a `store_id` that is not an Academy store id; a `state` outside the 21 states ("state must be the store's state, one of the 21 states Academy has stores in: ..."); "zip must be a 5-digit US ZIP code, e.g. 77098.", an unknown ZIP, "Pass zip or latitude + longitude, not both."; a category `path` that is not `/c/...`, "Pass path or url, not both."; "sub_shop only applies to type black_friday."; `facets` that are not `{facets[].id: value}` ("facets takes at most 10 facets."); "min_price must not be above max_price."; "Pass min_price / max_price or facets.facet_Price, not both."; more than 20 `store_ids`; an unknown `sort` or `type`; a `page` outside 1-500 or a `radius` outside 1-250.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No Academy product at this link.", "Academy knows no variant of this part number.", "No Academy category at this path.", "No Academy deal listing at this sub_shop.", "No Academy store with these ids.". Take slugs, part numbers, store ids and paths from a previous answer rather than guessing them. A search with no results is an answer with `count` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api).
- `502` means Academy data was temporarily unavailable ("Academy Sports + Outdoors is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Academy is busy ("Academy Sports + Outdoors is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.99.0
npm install scavio@0.100.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.academy.search({ query: "yeti tumbler", sort: "price_asc" });
const { data: product } = await scavio.academy.product({ slug: "yeti-duracoat-rambler-20-oz-tumbler" });
const { data: stock } = await scavio.academy.storeAvailability({ part_number: "111805768", store_id: "19", state: "TX" });
const { data: near } = await scavio.academy.stores({ zip: "77098", radius: 25 });
const { data: stores } = await scavio.academy.store({ store_ids: ["19", "327", "256"] });
const { data: coolers } = await scavio.academy.category({ path: "/c/outdoors/coolers" });
const { data: tree } = await scavio.academy.categories();
const { data: deals } = await scavio.academy.deals({ type: "black_friday" });
const { data: typed } = await scavio.academy.suggestions({ query: "yeti" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.academy.search(...)`, `product`, `store_availability`, `stores`, `store`, `category`, `categories`, `deals` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 9 endpoints as tools: `search_academy`, `get_academy_product`, `get_academy_store_availability`, `get_academy_stores`, `get_academy_store`, `get_academy_category`, `get_academy_categories`, `get_academy_deals` and `get_academy_suggestions`. Academy is opt-in: add `academy` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.99.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,academy"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/academy-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [product](https://scavio.dev/docs/academy-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [store availability](https://scavio.dev/docs/academy-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [stores](https://scavio.dev/docs/academy-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [store](https://scavio.dev/docs/academy-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [category](https://scavio.dev/docs/academy-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [categories](https://scavio.dev/docs/academy-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [deals](https://scavio.dev/docs/academy-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api), [suggestions](https://scavio.dev/docs/academy-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api). Overview: [Academy Sports + Outdoors API](https://scavio.dev/academy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=academy-sports-api).
