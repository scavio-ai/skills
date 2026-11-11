---
name: foot-locker-api
description: "Foot Locker API: the Foot Locker release calendar for the US, Canada and the UK (launch date and time, retail price, colorway, heat level, size run, reservation windows) as monitoring data, filtered by upcoming or launched, dates and brand; search footlocker.com or 12 country storefronts (Canada, UK, Germany, France, Italy, Spain, Netherlands, Belgium, Austria, Ireland, Australia, New Zealand) in local language and currency, or browse a category, a brand, the Sale list, Foot Locker Exclusives or promo-eligible items, 48 per page with price, list price, percent off, EU 30-day lowest price, rating and each colorway's price, filtered by brand, gender, color, price, shoe size or any facet; read one product with per-size availability (yes / no to ship and pick up, and how many stores show each size) and launch info; find US stores and which nearby stores show a size available; read US reviews and shopper Q&A. 10 endpoints, 1 credit each. No unit counts, no checkout. Foot Locker publishes no public developer API."
version: 1.0.0
tags: foot-locker, footlocker, foot-locker-api, footlocker-api, foot-locker-release-dates, foot-locker-release-calendar, foot-locker-releases, sneaker-release-calendar, sneaker-release-dates, release-monitoring, foot-locker-restock, foot-locker-in-stock, size-availability, foot-locker-store-availability, foot-locker-sale, foot-locker-deals, foot-locker-exclusives, foot-locker-black-friday, foot-locker-reviews, foot-locker-scraper, sneakers, athletic-shoes, jordan, nike, adidas, new-balance, store-locator, per-size-availability, multi-country, europe, canada, uk, australia, product-reviews, questions-and-answers, product-search, product-data, category-browse, brand-catalog, retail, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/docs/footlocker-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api
---

# Foot Locker API - Release Calendar, Size Availability, Prices in 13 Markets

Read the Foot Locker release calendar for the US, Canada or the UK: every upcoming or launched release with its launch date and time, online time, retail price, colorway, gender, heat level, the size run and, where the storefront runs them, the reservation status and windows. It is monitoring data: nothing here enters, reserves or buys a release. Search Foot Locker by keyword on footlocker.com or any of 12 country storefronts (titles in the storefront's language, prices in its currency), or browse a category by its page path, one brand by name, or a deal list (Sale, Foot Locker Exclusives, promo-code-eligible items): 48 products per page with the SKU, title, brand, URL, image, price, list price, percent off, the 30-day lowest price on European storefronts, sale / new / launch flags, rating, review count and every colorway's own price, sorted 7 ways and filtered by brand, gender, color, price bucket, shoe size or any facet the response lists. Read one product with its description, category, style code, price block, launch info, every colorway and every size: available, ships, can be picked up, and in how many stores it shows as available. In the US, find Foot Locker stores near a ZIP, a city or a point, check which nearby stores show a product or one size as available, and read customer reviews (up to 98, five sorts, a star filter) and shopper questions with every answer. All 10 endpoints return structured JSON and cost 1 credit each.

Foot Locker does not publish a public developer API. Affiliates join through impact.com and suppliers integrate through trading-partner platforms; neither offers a public endpoint for searching the catalog, reading live prices and size availability, or pulling the release calendar. This skill reads public Foot Locker pages with one Scavio key. Foot Locker has been owned by Dick's Sporting Goods since September 2025; the two run separate sites.

See also: for Dick's Sporting Goods (dickssportinggoods.com) clearance, per-SKU prices and store unit counts use the `dicks-sporting-goods-api` skill; for resale comps use `ebay-product-data`; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- List Foot Locker release dates: what launches this week or month, at what time and retail price, in which sizes, with the heat level and the reservation window, or filter the calendar by brand (Nike, Jordan, adidas, New Balance...)
- Build a release calendar feed, a launch-date reminder or a "what dropped this week" digest for the US, Canada or the UK
- Check which sizes of a Foot Locker shoe are available online, to ship or for pickup, and how many stores show each size
- Watch a style for a restock: poll the product and record when a size turns available again
- Find which Foot Locker stores near a US ZIP show a size as available, or list Foot Locker stores with their hours
- Search Foot Locker for a shoe and compare prices, percent off and ratings, or browse a category (Men's Shoes, Women's Clothing, Kids) or a brand's whole Foot Locker catalog
- Track the Foot Locker Sale list, Foot Locker Exclusives or promo-code-eligible items, for example ahead of Black Friday
- Compare a shoe's price across Foot Locker storefronts (US, Canada, UK, Germany, France, Italy, Spain, the Netherlands, Belgium, Austria, Ireland, Australia, New Zealand) in local currency
- Read what Foot Locker customers say about a shoe (fit, comfort, quality), or the questions shoppers asked and Foot Locker's answers

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Eight endpoints answered in about 2 to 9 seconds in the captures (brand 2, stores and store availability 3, releases 4, category and product 4-5, deals 5, search 8); allow a client timeout of at least 90 seconds for them. `/reviews` and `/questions` are slow: usually 25-90 seconds, up to about 3-4 minutes when a call is retried for you (the captures took 25 and 31 seconds). Set a client timeout of at least 240 seconds for those two and run them one at a time.

| Endpoint | Credits | Markets | What it returns |
|---|---|---|---|
| `POST /api/v1/footlocker/releases` | 1 | us, ca, gb | The release calendar: `sku`, `title`, `brand`, `style` (colorway), `style_code`, `gender`, `launch_at`, `online_at`, `heat_level`, `in_stock`, `image`, `url`, `retail_price`, `currency`, `reservation` (status, windows, store procedures) and `sizes[]` (US, EU, UK size and the channels taking part). Plus `total`, `count` and `data_as_of`. Filter by `status`, a date window and `brand` |
| `POST /api/v1/footlocker/search` | 1 | all 13 | 48 products per page: `id` (the SKU), `base_product`, `title`, `brand`, `url`, `image`, `price`, `list_price`, `percent_off`, `lowest_price_30d`, `on_sale`, `is_new`, `is_launch`, `member_only_sale`, `rating`, `review_count`, `color_count`, `colors[]` (sku, color, price, list price). Plus `redirected_to`, `country`, `language`, `currency`, total, page, page size, total pages, sort, `applied_filters`, `data_as_of`, count and `facets[]` with values and counts |
| `POST /api/v1/footlocker/category` | 1 | all 13 | One category by `path` (`/category/mens/shoes.html`), `url` or `collection_id`: the same grid as search plus the category's id, name, path and URL |
| `POST /api/v1/footlocker/brand` | 1 | all 13 | Every product of one brand by name (`"New Balance"`, `"HOKA"`, any case) or brand page URL, optionally narrowed by a keyword: the same grid plus `brand` as Foot Locker writes it, `brand_id` and `matched_by` |
| `POST /api/v1/footlocker/deals` | 1 | all 13 (`exclusives`: us, ca) | A deal list by `type`: `sale` (default), `exclusives` (Foot Locker Exclusives) or `discount_eligible` (items a promo code applies to): the same grid plus the list's label |
| `POST /api/v1/footlocker/product` | 1 | all 13 | One product by `product_id` (SKU) or `url`: title, brand, model number, description, genders, sports, category, color, primary color, width, style code, images, rating, review count, the `price` block (price, list price, percent off, 30-day lowest price), `available`, `available_to_ship`, `available_for_pickup`, `launch` info, `flags`, every size (`available`, `ship`, `pickup`, `stores_available`, UPC, store SKU, price), every colorway (sku, color, price, availability, URL) and the size chart |
| `POST /api/v1/footlocker/stores` | 1 | us | Foot Locker stores near a ZIP, a city + state or a point, nearest first (up to 50): store id, name, location name, address, city, state, ZIP, phone, lat, lng, distance, weekly hours, opening date, alert and closure notices, store page URL |
| `POST /api/v1/footlocker/store-availability` | 1 | us | Which Foot Locker stores near a ZIP or a point show a product (or one size) as available: each store as in `/stores` plus `available` and `sizes_available`, and per size whether it ships, can be picked up and in how many of the listed stores it shows |
| `POST /api/v1/footlocker/reviews` | 1 | us | 1-98 reviews (default 38) of one product with `sort` and a star filter, and `stats`: total reviews, displayed reviews, average, distribution, recommended percent, comfort / fit / quality averages, photo count. Per review: rating, title, text, author, date, recommended, helpful votes, verified, incentivized, syndicated and its source, secondary ratings, photos, videos, brand response |
| `POST /api/v1/footlocker/questions` | 1 | us | 1-50 shopper questions (default 10) of one product with every answer: question, details, author, date, answer count, helpful votes, and per answer its text, author, `author_type` (brand, retailer or customer), best-answer flag, date and votes |

## Markets

Every endpoint takes `country` (default `us`). Titles come in the storefront's language and prices in its currency.

| `country` | Storefront | Currency | Language | Endpoints |
|---|---|---|---|---|
| `us` | footlocker.com | USD | en | all 10 |
| `ca` | footlocker.ca | CAD | `language`: `en` (default) or `fr` | search, category, brand, deals (incl. exclusives), product, releases |
| `gb` | footlocker.co.uk | GBP | en | search, category, brand, deals, product, releases (no prices, reservations, heat level or sizes on the gb calendar) |
| `de` | footlocker.de | EUR | de | search, category, brand, deals, product |
| `fr` | footlocker.fr | EUR | fr | search, category, brand, deals, product |
| `it` | footlocker.it | EUR | it | search, category, brand, deals, product |
| `es` | footlocker.es | EUR | es | search, category, brand, deals, product |
| `nl` | footlocker.nl | EUR | nl | search, category, brand, deals, product |
| `be` | footlocker.be | EUR | `language`: `nl` (default) or `fr` | search, category, brand, deals, product |
| `at` | footlocker.at | EUR | de | search, category, brand, deals, product |
| `ie` | footlocker.ie | EUR | en | search, category, brand, deals, product |
| `au` | footlocker.com.au | AUD | en | search, category, brand, deals, product |
| `nz` | footlocker.co.nz | NZD | en | search, category, brand, deals, product |

`exclusives` (Foot Locker Exclusives) exists on `us` and `ca` only. `/stores`, `/store-availability`, `/reviews` and `/questions` are US only. Foot Locker's other storefronts (Poland, Portugal, Denmark, Sweden, Norway, Switzerland and Asia) are not served.

## Workflow

1. **Release calendar:** call `/footlocker/releases` with `status: "upcoming"` (or `launched`), an optional `from` / `to` date window and `brand`. Each release has a `sku`, `launch_at`, `retail_price` and `sizes[]`. Record it; nothing on this endpoint reserves or buys anything.
2. **Find products:** call `/footlocker/search` with `query`, `/footlocker/brand` with a `brand`, `/footlocker/deals` with a `type`, or `/footlocker/category` with a `path` such as `/category/mens/shoes.html`. Set `country` for a non-US storefront. Each item has an `id` (the SKU) and a `url`.
3. **Narrow the listing:** pass `brand`, `gender`, `color`, `price_range`, `on_sale`, or any facet through `filters` as `{facets[].id: facets[].values[].value}` (`{"mensShoesSize": "10.0"}`). Facet ids and values differ by storefront and language (`herrenSchuheSize` and `"Herren"` on `de`): read them from a previous answer's `facets[]`, never guess them.
4. **Page through:** `page` 1, 2, 3... up to `total_pages` (48 per page, at most page 200).
5. **One product in full:** call `/footlocker/product` with the item's `id` as `product_id` (or its `url`) and the same `country`. Read `sizes[]` for each size's availability and `stores_available`.
6. **Nearby stores (US):** call `/footlocker/store-availability` with the `product_id`, an optional `size` and the user's `zip`. Each store reads `available` with the `sizes_available` it shows. `/footlocker/stores` lists stores with hours without a product.
7. **Restock or price watch:** poll `/footlocker/product` (or a listing) on a schedule and store `available`, each size's `available` / `stores_available` and the `price` per run; compare runs yourself. There is no price or availability history.
8. **Reviews and questions (US):** call `/footlocker/reviews` with the product's `id` (`review_count` on any listing tells you whether there is anything to read), or `/footlocker/questions`.

## Parameters

### Releases (`/releases`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | `us`, `ca` or `gb` |
| `language` | string | `en` | `ca` only: `en` or `fr` |
| `status` | string | `all` | `all`, `upcoming` (launch date ahead) or `launched` |
| `from` | string | none | Only releases launching on or after this ISO date (`2026-11-15`) |
| `to` | string | none | Only releases launching on or before this ISO date; a bare date includes that whole day |
| `brand` | string | none | Only this brand (`"Jordan"`, `"Nike"`); case does not matter |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars, no `:`) |
| `country` | string | `us` | A storefront from the Markets table |
| `language` | string | storefront's | Only for `ca` (`en`, `fr`) and `be` (`nl`, `fr`) |
| `brand` | string or array | none | Brand filter value(s) (`"Nike"`, `"Jordan"`, `"adidas"`, `"New Balance"`, `"HOKA"`); case does not matter |
| `gender` | string or array | none | As `facets` `gender` lists it (`"Men's"`, `"Women's"`; in the storefront's language, `"Herren"` on `de`) |
| `color` | string or array | none | As `facets` `primaryColor` lists it (`"Black"`) |
| `price_range` | string or array | none | As `facets` `price` lists it: `-inf-25`, `25-50`, `50-75`, `75-100`, `100-150`, `150-inf` |
| `on_sale` | boolean | none | Only items on sale |
| `filters` | object | none | Any facet from a previous answer: `{facets[].id: value}` or `{facets[].id: [values]}`. Values of one facet are OR, facets combine (AND). E.g. `{"mensShoesSize": "10.0"}`, `{"womensShoesSize": "8.0"}`, `{"style": "Casual Sneakers"}`, `{"sport": "Running"}`, `{"eligibleForDiscount": "True"}` |
| `page` | integer | 1 | Results page, 1-200, 48 items each. A page past the last one returns an empty `items` list with the real `total` |
| `sort` | string | `relevance` | `relevance` (the site's Featured order), `price_low_to_high`, `price_high_to_low`, `new_arrivals`, `top_rated`, `name_az` or `brand_az` |

At most 20 values per filter and 30 filter values in all per call.

### Category (`/category`)

Pass one of `path`, `url` or `collection_id`, plus `country`, `language`, `brand` and any grid parameter (`gender`, `color`, `price_range`, `on_sale`, `filters`, `page`, `sort`).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | one of | A category page path, `/category/<path>.html` (`/category/mens/shoes.html`), as the site's category links carry it |
| `url` | string | one of | A Foot Locker category URL on any covered storefront (its storefront and page are used) |
| `collection_id` | string | one of | A previous category answer's `category.id` (`"men-s-shoes"`); saves time on page 2 and later |

### Brand (`/brand`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | one of | A brand name (`"Nike"`, `"Jordan"`, `"adidas"`, `"New Balance"`, `"HOKA"`, `"PUMA"`); case does not matter. An unknown brand is a 404 |
| `url` | string | one of | A Foot Locker brand page URL (`/category/brands/<brand>.html`) |
| `query` | string | none | Narrow the brand to a keyword (`"running shoes"`) |

Plus `country`, `language` and any grid parameter except `brand`.

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `sale` | `sale` (every storefront), `exclusives` (Foot Locker Exclusives; `us` and `ca` only) or `discount_eligible` (items a promo code applies to) |
| `brand` | string or array | none | Only these brands |

Plus `country`, `language` and any grid parameter.

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string | one of | A Foot Locker SKU (5-14 letters and digits): a listing item's `id`, the last part of a product URL (`Q5495005` in the US, 12 digits such as `316707025504` in Europe) |
| `url` | string | one of | A Foot Locker product URL on any covered storefront; its storefront is used. A `country` that names another storefront is a 400 |
| `country`, `language` | string | `us` | As on search. A SKU belongs to its storefront: European SKUs differ from US ones |

### Stores (`/stores`)

Pass one of `zip`, `city` + `state`, or `lat` + `lng`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string or integer | one of | US ZIP code (`10001` or `10001-1234`) |
| `city`, `state` | string | one of | US city with its 2-letter state (`"Atlanta"`, `"GA"`) |
| `lat`, `lng` | number | one of | A point, both required together |
| `radius` | integer | 25 | Search radius in miles, 1-120 |
| `limit` | integer | 10 | Stores to return, nearest first, 1-50 |

### Store availability (`/store-availability`)

Pass `product_id` or `url`, and one of `zip` or `lat` + `lng` (no city search here), plus `radius` and `limit` as on `/stores`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `size` | string or number | none | One size as `/product`'s `sizes[].size` lists it (`"10.0"`, `10`, `"XL"`). Without it, every size. A size the product does not list is a 404 that names its sizes |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `url` | string | one of | As on `/product` (US) |
| `sort` | string | `most_recent` | `most_recent`, `most_helpful`, `highest_rating`, `lowest_rating` or `relevance` |
| `rating` | integer | none | Only reviews with this many stars (1-5) |
| `limit` | integer | 38 | Reviews to return, 1-98. More reviews take longer (about 4 seconds per 30) |

### Questions (`/questions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` / `url` | string | one of | As on `/product` (US) |
| `limit` | integer | 10 | Questions to return, 1-50 |

## Examples

### Release calendar

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/releases \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "upcoming"}'
```

Captured `data` (42 of 44 releases and 13 of 15 sizes each trimmed):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "status": "upcoming",
  "from": null,
  "to": null,
  "brand": null,
  "total": 146,
  "count": 44,
  "data_as_of": "2026-11-11T10:00:10.505Z",
  "releases": [
    {
      "sku": "Z1800200",
      "title": "Air Jordan Retro 11 Space Jam Magic Ball",
      "brand": "Jordan",
      "style": "LIGHT BRITISH TAN/OFF WHITE/LAPIS",
      "style_code": null,
      "gender": "womens",
      "launch_at": "2026-11-11T15:00:00.000Z",
      "online_at": "2026-11-11T14:55:00.000Z",
      "heat_level": "unassigned",
      "in_stock": true,
      "image": "https://images.footlocker.com/is/image/EBFL2/Z1800200?wid=400&hei=400&fmt=png-alpha",
      "url": null,
      "retail_price": 235,
      "currency": "USD",
      "reservation": {
        "status": "store_only",
        "store_only": false,
        "web_only": false,
        "starts_at": null,
        "ends_at": null,
        "assignment_at": null,
        "awarding_at": null,
        "online_reveal_at": null,
        "store_procedures": null
      },
      "sizes": [
        { "us": "5", "eu": null, "uk": null, "participating": ["online", "store"] },
        { "us": "5.5", "eu": null, "uk": null, "participating": ["online", "store"] }
      ]
    },
    {
      "sku": "6259800",
      "title": "Nike Kobe 8 Protro Shanghai - In Store Only",
      "brand": "Nike",
      "style": "LASER ORANGE/CINNABAR/SAFETY ORANGE",
      "style_code": null,
      "gender": "mens",
      "launch_at": "2026-11-11T15:00:00.000Z",
      "online_at": "2026-11-11T14:55:00.000Z",
      "heat_level": "unassigned",
      "in_stock": true,
      "image": "https://images.footlocker.com/is/image/EBFL2/6259800?wid=400&hei=400&fmt=png-alpha",
      "url": null,
      "retail_price": 200,
      "currency": "USD",
      "reservation": {
        "status": "closed",
        "store_only": false,
        "web_only": false,
        "starts_at": "2026-11-05T15:00:00.000Z",
        "ends_at": "2026-11-12T23:00:00.000Z",
        "assignment_at": "2026-11-10T21:00:00.000Z",
        "awarding_at": "2026-11-10T22:00:00.000Z",
        "online_reveal_at": "2026-11-11T14:00:00.000Z",
        "store_procedures": { "first_come_first_served": false, "reservations": true, "sweepstakes": false }
      },
      "sizes": [
        { "us": "7.5", "eu": null, "uk": null, "participating": ["store"] },
        { "us": "8", "eu": null, "uk": null, "participating": ["store"] }
      ]
    }
  ]
}
```

`total` (146) is the whole US calendar; `count` (44) is what matched `status: "upcoming"`. Upcoming releases are sorted soonest first, launched ones newest first. Times are UTC: `launch_at` 15:00 UTC is 10:00 AM in New York in November, and `online_at` is when the product page goes live. `reservation.status` is Foot Locker's own label for the release (`open`, `closed` or `store_only` in the captures: 36 of these 44 were `store_only`, 7 `open`, 1 `closed`); the windows say when reservations open and close and when Foot Locker assigns and awards them. Report them as dates; never describe them as something to automate. `heat_level` is Foot Locker's demand label (`unassigned` for 43 of 44 here, `hot` for one; `moderate` also appeared on launched releases). `sizes[].participating` says whether a size is offered online, in store or both. `url` is null until a product page exists, and a release SKU can have no online product page even after launch (store-only): `/product` then answers a charged 404, so check `participating` before calling it. On `gb` the calendar carries dates, colorways and links but no retail price, reservation, heat level or sizes.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "Q5495005"}'
```

Captured `data` (description cut, 21 of 25 sizes and 4 of 5 size-chart rows trimmed):

```json
{
  "country": "us",
  "language": "en",
  "currency": "USD",
  "id": "Q5495005",
  "title": "Jordan Retro 1 High OG - Men's",
  "brand": "Jordan",
  "url": "https://www.footlocker.com/product/~/Q5495005.html",
  "model_number": "190074",
  "description": "A classic remade. Reinventing the King’s style, the Jordan Retro 1 High OG brings a fashion-forward look to the OG sneaker that started it all...",
  "genders": ["Men's"],
  "sports": ["Basketball", "Casual"],
  "category": {
    "product_types": ["Shoes"],
    "styles": ["Performance Basketball Shoes", "Casual Sneakers"],
    "sub_styles": ["Casual Basketball Sneakers"]
  },
  "color": "Black/White/Royal Blue",
  "primary_color": "Black",
  "width": "Width - D - Medium",
  "style_code": "IQ5495-005",
  "images": ["https://images.footlocker.com/is/image/EBFL2/Q5495005"],
  "rating": 4.6,
  "review_count": 1167,
  "price": { "price": 185, "list_price": 185, "percent_off": null, "lowest_price_30d": null },
  "available": true,
  "available_to_ship": true,
  "available_for_pickup": true,
  "launch": { "is_launch": false, "launch_type": "Cool", "launch_date": "2026-10-10T14:00:00.000Z", "web_only": true },
  "flags": {
    "on_sale": false,
    "new": false,
    "discounts_excluded": true,
    "free_shipping": true,
    "ship_to_store": true,
    "member_only_sale": null,
    "member_only_product": null
  },
  "sizes": [
    { "size": "7.0", "dual_size": "M7.0 / W8.5", "available": false, "ship": null, "pickup": null, "stores_available": 0, "upc": null, "store_sku": null, "price": 185, "list_price": 185 },
    { "size": "7.5", "dual_size": "M7.5 / W9.0", "available": true, "ship": true, "pickup": true, "stores_available": 271, "upc": "198967016094", "store_sku": "03-41-07817-0-04", "price": 185, "list_price": 185 },
    { "size": "12.5", "dual_size": "M12.5 / W14.0", "available": false, "ship": false, "pickup": false, "stores_available": 0, "upc": "198967025256", "store_sku": "03-41-07817-0-04", "price": 185, "list_price": 185 },
    { "size": "15.0", "dual_size": "M15.0 / W16.0", "available": true, "ship": true, "pickup": true, "stores_available": 17, "upc": "198967043960", "store_sku": "03-41-07817-0-04", "price": 185, "list_price": 185 }
  ],
  "colorways": [
    { "sku": "Z5485201", "color": "Multi/Shadow Brown", "price": 185, "list_price": 185, "available": true, "url": "https://www.footlocker.com/product/~/Z5485201.html" },
    { "sku": "Q5495005", "color": "Black/White/Royal Blue", "price": 185, "list_price": 185, "available": true, "url": "https://www.footlocker.com/product/~/Q5495005.html" }
  ],
  "size_chart": [
    { "label": "MEN'S SHOE SIZE", "sizes": ["4", "4.5", "5", "5.5", "6", "6.5", "7", "7.5", "8", "8.5", "9", "9.5", "10", "10.5", "11", "11.5", "12", "12.5", "13", "13.5", "14", "15", "16", "17", "18"] }
  ]
}
```

Availability is yes / no per size: Foot Locker publishes no unit counts, so never state how many pairs are left. Here 13 of 25 sizes were available to ship and to pick up; sizes 4.0 to 7.0 and 13.5 were not listed for sale at all (`ship` and `pickup` null, no UPC), while 12.5 and 16.0 to 18.0 were listed but sold out (`false`). `stores_available` is the number of Foot Locker stores showing that size as available (271 for 7.5, 17 for 15.0): it is a store count, not a stock count. `launch` carries Foot Locker's launch record for the colorway (`launch_date` October 10, a `web_only` launch); `discounts_excluded: true` is Foot Locker's flag that the item is excluded from discounts. Each colorway is its own SKU with its own price: pass a `colorways[].sku` back to `/product` for its sizes. The other size-chart rows here were WOMEN'S, EUROPEAN, UK and JAPANESE.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nike dunk"}'
```

Captured `data` (47 of 48 items, 3 of 5 colors, 14 of 17 facets and most facet values trimmed):

```json
{
  "query": "nike dunk",
  "redirected_to": null,
  "country": "us",
  "language": "en",
  "currency": "USD",
  "total": 153,
  "page": 1,
  "page_size": 48,
  "total_pages": 4,
  "sort": "relevance",
  "applied_filters": {},
  "data_as_of": "2026-11-11T09:37:13.295Z",
  "count": 48,
  "items": [
    {
      "id": "D1391100",
      "base_product": "D1391100",
      "title": "Nike Dunk Low Retro - Men's",
      "brand": "Nike",
      "url": "https://www.footlocker.com/product/~/D1391100.html",
      "image": "https://images.footlocker.com/is/image/EBFL2/D1391100",
      "price": 99.99,
      "list_price": 120,
      "percent_off": 17,
      "lowest_price_30d": null,
      "on_sale": true,
      "is_new": false,
      "is_launch": false,
      "member_only_sale": false,
      "rating": 4,
      "review_count": 385,
      "color_count": 12,
      "colors": [
        { "sku": "V4452100", "color": "Sanded Purple/White/Off Noir", "price": 120, "list_price": 120 },
        { "sku": "H1931001", "color": "Black/Brown/White", "price": 130, "list_price": 130 }
      ]
    }
  ],
  "facets": [
    {
      "id": "gender",
      "label": "Gender",
      "values": [
        { "label": "Men's", "value": "Men's", "count": 38, "selected": false },
        { "label": "Women's", "value": "Women's", "count": 30, "selected": false }
      ]
    },
    {
      "id": "price",
      "label": "Price",
      "values": [
        { "label": "$50 to $74.99", "value": "50-75", "count": 49, "selected": false },
        { "label": "$100 to $149.99", "value": "100-150", "count": 47, "selected": false }
      ]
    },
    {
      "id": "eligibleForDiscount",
      "label": "Miscellaneous",
      "values": [
        { "label": "Promo Code Eligible", "value": "True", "count": 71, "selected": false }
      ]
    }
  ]
}
```

The price on a listing is the tile's colorway; `colors[]` lists other colorways with their own prices (they differ: $120 and $130 here against the tile's $99.99) and can be shorter than `color_count`. Take an item's `id` to `/product` for sizes. The other facets on this answer were `ageRange`, `brand`, `mensShoesSize`, `womensShoesSize`, `boysShoesSize`, `girlsShoesSize`, `productType`, `primaryColor`, `style`, `sport`, `rating`, `saleProduct`, `freeShipping` and `newArrival`; any `facets[].id` with one of its `values[].value` works in `filters`, e.g. `{"mensShoesSize": "10.0", "primaryColor": "Black"}`.

`data_as_of` is when Foot Locker built this listing: listing pages (search, category, brand, deals) can be up to a few hours old, so a price or a sale flag on a listing can lag the product page. Say how old a listing is when it matters, and read `/product` before quoting a current price.

A bare brand keyword sends Foot Locker's search to a landing page; the brand's listing is returned instead and `redirected_to` says which (`"query": "hoka"` came back with `"redirected_to": "collection hoka"` and the 342 HOKA products, the same as `/brand`). A keyword whose landing page has no product listing (`clearance`, `samba` in the US) is a 400 that is not charged: use `/brand`, `/category` or `/deals` instead.

### Search on a European storefront

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nike dunk", "country": "de"}'
```

Captured `data` (18 of 19 items, 13 of 15 facets and most facet values trimmed):

```json
{
  "query": "nike dunk",
  "redirected_to": null,
  "country": "de",
  "language": "de",
  "currency": "EUR",
  "total": 19,
  "page": 1,
  "page_size": 48,
  "total_pages": 1,
  "sort": "relevance",
  "applied_filters": {},
  "data_as_of": "2026-11-11T10:01:15.598Z",
  "count": 19,
  "items": [
    {
      "id": "316707025504",
      "base_product": "316707025504",
      "title": "Nike Dunk Low - Grundschule Schuhe",
      "brand": "Nike",
      "url": "https://www.footlocker.de/product/~/316707025504.html",
      "image": "https://images.footlocker.com/is/image/FLEU/316707025504",
      "price": 70,
      "list_price": 94.99,
      "percent_off": 26,
      "lowest_price_30d": 94.99,
      "on_sale": true,
      "is_new": false,
      "is_launch": false,
      "member_only_sale": false,
      "rating": 5,
      "review_count": 222,
      "color_count": 1,
      "colors": [
        { "sku": "316706028004", "color": "White-Lt Smoke Grey-White", "price": 65, "list_price": 94.99 }
      ]
    }
  ],
  "facets": [
    {
      "id": "herrenSchuheSize",
      "label": "Größe - Herren (Schuhe)",
      "values": [
        { "label": "42", "value": "42", "count": 6, "selected": false }
      ]
    },
    {
      "id": "gender",
      "label": "Kategorie",
      "values": [
        { "label": "Herren", "value": "Herren", "count": 10, "selected": false },
        { "label": "Kinder", "value": "Kinder", "count": 6, "selected": false },
        { "label": "Damen", "value": "Damen", "count": 3, "selected": false }
      ]
    }
  ]
}
```

On European storefronts titles, facet labels, facet ids and filter values are in the local language and sizes are EU sizes: the men's shoe size facet is `herrenSchuheSize` on `de`, not `mensShoesSize`, and gender is `"Herren"`. Read the facets of the storefront you filter. `lowest_price_30d` is the lowest price of the last 30 days that European storefronts (the UK and Ireland included) publish, mostly on sale items (94.99 EUR here, against today's 70 EUR); it is null on the US, Canadian, Australian and New Zealand storefronts and on many European items. European SKUs are 12 digits and differ from US SKUs for the same shoe.

### Deals, category and brand

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "sale"}'
```

The captured answer opens with (then the same `items[]` and `facets[]` as search):

```json
{
  "type": "sale",
  "label": "Sale",
  "country": "us",
  "language": "en",
  "currency": "USD",
  "total": 2774,
  "page": 1,
  "page_size": 48,
  "total_pages": 58,
  "sort": "relevance",
  "applied_filters": {},
  "data_as_of": "2026-11-11T09:35:12.632Z",
  "count": 48
}
```

`{"path": "/category/mens/shoes.html"}` on `/footlocker/category` answered 2,601 products with `"category": {"id": "men-s-shoes", "name": "Men's Shoes", "path": "/category/mens/shoes.html", "url": "https://www.footlocker.com/category/mens/shoes.html"}`; pass `"collection_id": "men-s-shoes"` for later pages. `{"brand": "New Balance"}` on `/footlocker/brand` answered `"brand": "New Balance"`, `"brand_id": "new-balance"`, `"matched_by": "collection"` and 637 products; `matched_by` is `brand_filter` when the brand was matched through the Brand filter instead (for example with a `query`). Send `sort: "price_low_to_high"` on deals for the cheapest sale items first; there is no discount sort, so sort by `percent_off` yourself.

### Store availability

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "W2288111", "size": "10.0", "zip": "10001"}'
```

Captured `data` (8 of 10 stores and 5 of 7 days of hours each trimmed):

```json
{
  "country": "us",
  "product": {
    "id": "W2288111",
    "title": "Nike Air Force 1 '07 - Men's",
    "brand": "Nike",
    "url": "https://www.footlocker.com/product/~/W2288111.html",
    "price": 115,
    "list_price": 115,
    "currency": "USD"
  },
  "size": "10.0",
  "location": { "zip": "10001" },
  "radius_miles": 25,
  "count": 10,
  "stores_with_availability": 9,
  "sizes": [
    { "size": "10.0", "available_online": true, "ship": true, "pickup": true, "stores_in_results": 9 }
  ],
  "stores": [
    {
      "store_id": "8747",
      "name": "Foot Locker",
      "name_secondary": "34th St. Herald Square",
      "address": "112 W 34th St",
      "address_2": null,
      "city": "New York",
      "state": "NY",
      "zip": "10120",
      "phone": "(212) 760-2311",
      "lat": 40.7499,
      "lng": -73.9887,
      "distance_miles": 0.6,
      "hours": [
        { "day": "Sunday", "open": "11:00", "close": "20:00" },
        { "day": "Monday", "open": "10:00", "close": "22:00" }
      ],
      "opened_at": "1997-05-08",
      "alert": null,
      "closure": null,
      "url": "https://stores.footlocker.com/ny/newyork/112-w-34th-st-8747.html",
      "available": true,
      "sizes_available": ["10.0"]
    },
    {
      "store_id": "8879",
      "name": "Foot Locker",
      "name_secondary": "SoHo",
      "address": "440 Broadway",
      "address_2": null,
      "city": "New York",
      "state": "NY",
      "zip": "10013",
      "phone": "(212) 343-7461",
      "lat": 40.7200257,
      "lng": -74.0009771,
      "distance_miles": 2.3,
      "hours": [
        { "day": "Sunday", "open": "11:00", "close": "19:00" },
        { "day": "Monday", "open": "10:00", "close": "20:00" }
      ],
      "opened_at": null,
      "alert": null,
      "closure": null,
      "url": "https://stores.footlocker.com/ny/newyork/440-broadway-8879.html",
      "available": false,
      "sizes_available": []
    }
  ]
}
```

9 of the 10 nearest Foot Locker stores showed men's size 10.0 as available; SoHo did not. `available` is yes / no: a store is marked available when Foot Locker lists it among the stores showing that size as available, which is not a held pair or a unit count. Tell the user to confirm with the store (the `phone` is in the answer) before travelling. Only Foot Locker banner stores are covered: Kids Foot Locker and Champs Sports stores are not. Without `size`, `sizes[]` covers every size and each store lists all `sizes_available`. `/footlocker/stores` returns the same store records (address, phone, hours, opening date, `alert` and `closure` notices, store page URL) without a product, by ZIP, city + state or point.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 240 \
  -d '{"product_id": "Q5495005"}'
```

Captured `data` (36 of 38 reviews trimmed; the call took 25 seconds):

```json
{
  "product_id": "Q5495005",
  "country": "us",
  "stats": {
    "total_reviews": 1185,
    "displayed_reviews": 965,
    "average_rating": 4.6,
    "rating_distribution": { "1": 54, "2": 23, "3": 33, "4": 124, "5": 951 },
    "recommended_percent": 92,
    "secondary_ratings_averages": {
      "comfort": { "average": 3.59, "max": 5 },
      "fit": { "average": 3, "max": 5 },
      "quality": { "average": 4.47, "max": 5 }
    },
    "photo_count": 33
  },
  "sort": "most_recent",
  "rating_filter": null,
  "matching_reviews": 965,
  "count": 38,
  "reviews": [
    {
      "id": "273730524",
      "rating": 3,
      "title": "I see why then were sitting online.",
      "text": "Ordered the black/White/Royal Retro 1’s High & The leather style/quality is poor compared to prior releases. My particular ordered shoes have two brown stains on the outsole of the heal. Smh\n\nRetro Jordan’s in my shoe size 15, are never online. I see why these were.",
      "author": "cC899800926",
      "submitted_at": "2026-11-06T15:23:04.000Z",
      "recommended": null,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "verified_purchaser": false,
      "incentivized": false,
      "syndicated": true,
      "syndication_source": "Nike",
      "secondary_ratings": {},
      "photos": [],
      "videos": [],
      "brand_response": null,
      "original_product_name": "Air Jordan 1 High OG 'Royal' Men's Shoes"
    },
    {
      "id": "273660552",
      "rating": 5,
      "title": "Style",
      "text": "These go good dressed down with anything",
      "author": "Micah Morgan",
      "submitted_at": "2026-11-04T13:07:06.000Z",
      "recommended": true,
      "helpful_votes": 0,
      "unhelpful_votes": 0,
      "verified_purchaser": false,
      "incentivized": false,
      "syndicated": false,
      "syndication_source": null,
      "secondary_ratings": {
        "value": { "value": 5, "max": 5 },
        "comfort": { "value": 5, "max": 5 },
        "quality": { "value": 5, "max": 5 },
        "fit": { "value": 3, "max": 5 }
      },
      "photos": [],
      "videos": [],
      "brand_response": null,
      "original_product_name": "Jordan Retro 1 High OG - Men's Basketball Shoes"
    }
  ]
}
```

`total_reviews` (1,185) counts every language; `displayed_reviews` (965) are the English reviews Foot Locker pages through, and `matching_reviews` is how many of those match your `rating` filter. Ask for up to 98 with `limit`; never present them as all reviews. 27 of these 38 were syndicated: `syndication_source` names the site the review was first written on (Nike for 23, champssports.com for 4) and `original_product_name` the product name there. Report `syndicated`, `verified_purchaser` and `incentivized` with any summary. Secondary ratings (fit, comfort, quality, value) come as a value out of `max` with no scale labels: quote them as numbers (fit 3 of 5), not as good or bad. Reviewer age, gender, location and IP are never returned.

### Questions

```bash
curl -X POST https://api.scavio.dev/api/v1/footlocker/questions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  --max-time 240 \
  -d '{"product_id": "Q5495005"}'
```

Captured `data` (9 of 10 questions trimmed; the call took 31 seconds):

```json
{
  "product_id": "Q5495005",
  "country": "us",
  "total_questions": 76,
  "count": 10,
  "questions": [
    {
      "id": "7327803",
      "question": "Do these come with extra Laces?",
      "details": null,
      "author": "Sam Steven",
      "submitted_at": "2023-11-10T17:38:58.000Z",
      "answer_count": 1,
      "helpful_votes": 0,
      "answers": [
        {
          "id": "7109951",
          "text": "These shoes will come with extra laces.",
          "author": "Jesse R",
          "author_type": "retailer",
          "is_best_answer": false,
          "submitted_at": "2023-11-10T21:01:12.000Z",
          "helpful_votes": 0,
          "unhelpful_votes": 0
        }
      ]
    }
  ]
}
```

`author_type` says who answered: `retailer` is Foot Locker staff (all 10 answers here), `brand` the brand, `customer` another shopper. Quote answers with their date: a staff answer about stock or sizes describes the day it was written, not today.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def footlocker(endpoint, body, timeout=90):
    r = requests.post(f"{BASE}/api/v1/footlocker/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

# 1. Upcoming Jordan releases on the US calendar (1 credit)
cal = footlocker("releases", {"status": "upcoming", "brand": "Jordan"})
for rel in cal["releases"]:
    print(rel["launch_at"], rel["sku"], rel["title"], rel["retail_price"], (rel["reservation"] or {}).get("status"))

# 2. Which sizes of one shoe are available, and in how many stores (1 credit)
item = footlocker("product", {"product_id": "Q5495005"})
for s in item["sizes"]:
    if s["available"]:
        print(s["size"], "ship" if s["ship"] else "", "pickup" if s["pickup"] else "", s["stores_available"], "stores")

# 3. Nearby stores showing men's 10.0 (1 credit, US only)
near = footlocker("store-availability", {"product_id": "W2288111", "size": "10.0", "zip": "10001"})
for st in near["stores"]:
    if st["available"]:
        print(st["name_secondary"], st["distance_miles"], "mi", st["phone"])

# 4. Sale items in Germany, men's EU 42, cheapest first (1 credit)
sale = footlocker("deals", {"type": "sale", "country": "de", "sort": "price_low_to_high", "filters": {"herrenSchuheSize": "42"}})
print("listing built at", sale["data_as_of"])
for p in sale["items"][:5]:
    print(p["id"], p["title"], p["price"], sale["currency"], "30-day low", p["lowest_price_30d"])

# 5. Lowest-rated reviews first (1 credit, slow)
rv = footlocker("reviews", {"product_id": "Q5495005", "sort": "lowest_rating", "limit": 20}, timeout=240)
print(rv["stats"]["average_rating"], "average over", rv["stats"]["total_reviews"], "reviews")
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is when the answer was produced; listings also carry `data_as_of`, when Foot Locker built that listing.

- **listing item** (search, category, brand, deals) - `id` (the SKU), `base_product`, `title`, `brand`, `url`, `image`, `price`, `list_price`, `percent_off`, `lowest_price_30d` (European storefronts), `on_sale`, `is_new`, `is_launch`, `member_only_sale`, `rating`, `review_count`, `color_count`, `colors[]` {`sku`, `color`, `price`, `list_price`}.
- **grid** (all four listings) - `country`, `language`, `currency`, `total`, `page`, `page_size`, `total_pages`, `sort`, `applied_filters` {facet id: [values]}, `data_as_of`, `count`, `items[]`, `facets[]` {`id`, `label`, `values[]` {`label`, `value`, `count`, `selected`}}.
- **search** - `query`, `redirected_to` (`"collection <slug>"` or `"brand <name>"` when a bare brand keyword was answered with the brand's listing, else null) and the grid.
- **category** - `category` {`id` (collection id), `name`, `path`, `url`} and the grid.
- **brand** - `brand` (as Foot Locker writes it), `brand_id`, `matched_by` (`collection` or `brand_filter`), `query` and the grid.
- **deals** - `type`, `label` and the grid.
- **product** - `country`, `language`, `currency`, `id`, `title`, `brand`, `url`, `model_number`, `description`, `genders[]`, `sports[]`, `category` {`product_types[]`, `styles[]`, `sub_styles[]`}, `color`, `primary_color`, `width`, `style_code`, `images[]`, `rating`, `review_count`, `price` {`price`, `list_price`, `percent_off`, `lowest_price_30d`}, `available`, `available_to_ship`, `available_for_pickup`, `launch` {`is_launch`, `launch_type`, `launch_date`, `web_only`}, `flags` {`on_sale`, `new`, `discounts_excluded`, `free_shipping`, `ship_to_store`, `member_only_sale`, `member_only_product`}, `sizes[]` {`size`, `dual_size`, `available`, `ship`, `pickup`, `stores_available`, `upc`, `store_sku`, `price`, `list_price`}, `colorways[]` {`sku`, `color`, `price`, `list_price`, `available`, `url`}, `size_chart[]` {`label`, `sizes[]`}.
- **releases** - `country`, `language`, `currency`, `status`, `from`, `to`, `brand`, `total`, `count`, `data_as_of`, `releases[]` {`sku`, `title`, `brand`, `style`, `style_code`, `gender`, `launch_at`, `online_at`, `heat_level`, `in_stock`, `image`, `url`, `retail_price`, `currency`, `reservation` ({`status`, `store_only`, `web_only`, `starts_at`, `ends_at`, `assignment_at`, `awarding_at`, `online_reveal_at`, `store_procedures` {`first_come_first_served`, `reservations`, `sweepstakes`}} or null), `sizes[]` {`us`, `eu`, `uk`, `participating[]`}}.
- **stores** - `country`, `location` ({`zip`}, {`city`, `state`} or {`lat`, `lng`}), `radius_miles`, `count`, `stores[]` {`store_id`, `name`, `name_secondary`, `address`, `address_2`, `city`, `state`, `zip`, `phone`, `lat`, `lng`, `distance_miles`, `hours[]` {`day`, `open`, `close`}, `opened_at`, `alert`, `closure`, `url`}.
- **store-availability** - `country`, `product` {`id`, `title`, `brand`, `url`, `price`, `list_price`, `currency`}, `size`, `location`, `radius_miles`, `count`, `stores_with_availability`, `sizes[]` {`size`, `available_online`, `ship`, `pickup`, `stores_in_results`}, `stores[]` (as in stores, plus `available` and `sizes_available[]`).
- **reviews** - `product_id`, `country`, `stats` {`total_reviews`, `displayed_reviews`, `average_rating`, `rating_distribution` {`1`..`5`}, `recommended_percent`, `secondary_ratings_averages` {name: {`average`, `max`}}, `photo_count`}, `sort`, `rating_filter`, `matching_reviews`, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `author`, `submitted_at`, `recommended`, `helpful_votes`, `unhelpful_votes`, `verified_purchaser`, `incentivized`, `syndicated`, `syndication_source`, `secondary_ratings` {name: {`value`, `max`}}, `photos[]`, `videos[]`, `brand_response`, `original_product_name`}.
- **questions** - `product_id`, `country`, `total_questions`, `count`, `questions[]` {`id`, `question`, `details`, `author`, `submitted_at`, `answer_count`, `helpful_votes`, `answers[]` {`id`, `text`, `author`, `author_type`, `is_best_answer`, `submitted_at`, `helpful_votes`, `unhelpful_votes`}}.

## Guardrails

- Release calendar data is for monitoring: dates, prices, sizes and reservation windows to read, store and report. This API does not enter reservations, raffles or draws, does not add to cart or check out, and does not hold or buy stock. Never present it as a purchasing bot, an entry tool or a way to buy ahead of other shoppers, and never help automate a reservation or checkout.
- Size availability is yes / no. `available`, `ship` and `pickup` say whether a size is offered; `stores_available` and `stores_in_results` count stores, not pairs. Foot Locker publishes no unit counts: never estimate how many pairs are left.
- Store availability means Foot Locker lists the store as showing that size available; it does not reserve a pair. Advise calling the store before going. Kids Foot Locker and Champs Sports stores are not covered.
- Freshness: listings (search, category, brand, deals) can be up to a few hours old; `data_as_of` says when the listing was built. Read `/product` for the current price and sizes before quoting them, and give the time with any availability you report.
- Prices are in the storefront's currency (`currency`: USD, CAD, GBP, EUR, AUD or NZD). Compare storefronts only after converting, and say the prices are each site's own. A listing's `price` is the tile colorway's: colorways are priced separately (`colors[]`, `colorways[]`).
- `percent_off` compares the price with Foot Locker's list price. `lowest_price_30d` is the 30-day lowest price European storefronts publish; report it as that, not as price history. There is no price history: poll and store results yourself.
- `member_only_sale` flags a sale price for Foot Locker members; member (FLX) prices, points and account data are not returned.
- SKUs belong to a storefront: a US SKU will not resolve on `de`, and European SKUs are 12 digits. Use the `id` from a listing on the same storefront.
- A release SKU may have no online product page (store-only, or not launched yet): `/product` answers a charged 404. Check `sizes[].participating` and `url` on the calendar first.
- Reviews: up to 98 per call, English reviews only; `total_reviews` counts every language. Never present the returned reviews as all of them. Report `syndicated` (with `syndication_source`), `verified_purchaser` and `incentivized` with any summary, and quote review text verbatim with its rating and date. Reviewer age, gender, location and IP are never returned.
- Questions: `author_type` `retailer` answers are Foot Locker staff writing on the date shown; they are not today's stock.
- Not covered: search suggestions, unit counts, member (FLX) prices or account data, order status, checkout, raffles or reservation entry, Kids Foot Locker and Champs Sports stores, price history, and the storefronts in Poland, Portugal, Denmark, Sweden, Norway, Switzerland and Asia.
- Foot Locker's terms of use restrict automated monitoring and copying of the site without written permission and allow personal, non-commercial use of its materials. That is Foot Locker's policy, not legal advice; the user is responsible for how they use the data.
- Never fabricate release dates, prices, availability, store counts or ratings. Only return what the API returned, with the product `url` or SKU.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, or a `query` with `:`; a `country` the endpoint does not serve, e.g. `de` on `/releases` or `/reviews`; `language` other than the storefront's; `exclusives` outside `us` / `ca`; `page` outside 1-200; an unknown `sort`, deal `type` or release `status`; `filters` that is not an object of facet id to value(s), more than 20 values for one or 30 in all; none of `path`, `url` and `collection_id`; no `product_id` or `url`; a product `url` on another storefront than `country`; `from` after `to` or not an ISO date; a ZIP that is not 5 digits; `lat` without `lng`; a `radius` outside 1-120 or `limit` outside 1-50; a `rating` outside 1-5 or a review `limit` outside 1-98). A keyword whose landing page has no product listing (`clearance`) is also a 400; it is not charged.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product online (unknown, store-only or not launched yet), category, brand, or size on the product. These not-founds are charged 1 credit: take SKUs, paths and brands from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api).
- `502` means Foot Locker was temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means too many Foot Locker calls are running at once: wait the `Retry-After` seconds (5 for most endpoints, 30 for reviews and questions) and send it again. Not charged.

## SDKs

```bash
pip install scavio==0.48.0
npm install scavio@0.49.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: calendar } = await scavio.footlocker.releases({ status: "upcoming", brand: "Jordan" });
const { data: found } = await scavio.footlocker.search({ query: "nike dunk", filters: { mensShoesSize: "10.0" } });
const { data: de } = await scavio.footlocker.search({ query: "nike dunk", country: "de" });
const { data: sale } = await scavio.footlocker.deals({ type: "sale", sort: "price_low_to_high" });
const { data: shoes } = await scavio.footlocker.category({ path: "/category/mens/shoes.html" });
const { data: nb } = await scavio.footlocker.brand({ brand: "New Balance" });
const { data: item } = await scavio.footlocker.product({ product_id: "Q5495005" });
const { data: near } = await scavio.footlocker.storeAvailability({ product_id: "W2288111", size: "10.0", zip: "10001" });
const { data: stores } = await scavio.footlocker.stores({ zip: "10001" });
// Slow (25-90 s, up to ~3-4 min): the SDK allows a longer timeout for these two
const { data: reviews } = await scavio.footlocker.reviews({ product_id: "Q5495005", sort: "most_helpful" });
const { data: questions } = await scavio.footlocker.questions({ product_id: "Q5495005" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.footlocker.search(...)`, `client.footlocker.product(...)`, `client.footlocker.category(...)`, `client.footlocker.brand(...)`, `client.footlocker.deals(...)`, `client.footlocker.releases(...)` (the date window is `date_from` / `date_to`), `client.footlocker.stores(...)`, `client.footlocker.store_availability(...)`, `client.footlocker.reviews(...)` and `client.footlocker.questions(...)`.

## MCP

The Scavio MCP server exposes all ten endpoints as tools: `search_footlocker`, `get_footlocker_product`, `get_footlocker_category`, `get_footlocker_brand`, `get_footlocker_deals`, `get_footlocker_releases`, `get_footlocker_stores`, `get_footlocker_store_availability`, `get_footlocker_reviews` and `get_footlocker_questions`. Foot Locker is opt-in: add `footlocker` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.46.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,footlocker"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [releases](https://scavio.dev/docs/footlocker-releases?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [search](https://scavio.dev/docs/footlocker-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [product](https://scavio.dev/docs/footlocker-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [category](https://scavio.dev/docs/footlocker-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [brand](https://scavio.dev/docs/footlocker-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [deals](https://scavio.dev/docs/footlocker-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [stores](https://scavio.dev/docs/footlocker-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [store availability](https://scavio.dev/docs/footlocker-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [reviews](https://scavio.dev/docs/footlocker-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api), [questions](https://scavio.dev/docs/footlocker-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api). Overview: [Foot Locker API](https://scavio.dev/footlocker-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=foot-locker-api).
