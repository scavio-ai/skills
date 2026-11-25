# Best Buy Product Data API - US and Canada Prices, Open-Box, Store Stock, Deals

Two markets on the same endpoints, chosen with `country`:

- `country: "us"` (the default) - bestbuy.com, in USD. Unchanged by Canada: a body without `country` works exactly as before.
- `country: "ca"` - Best Buy Canada (bestbuy.ca, Best Buy's Canadian store: 142 stores across Canada per Best Buy's FY2026 10-K, plus a marketplace of third-party sellers), in CAD, in English or French, 1 credit per call. All nine endpoints take it, and Canada adds one endpoint of its own: product questions. See [Best Buy Canada](#best-buy-canada-country-ca) below.

Best Buy's developer API (developer.bestbuy.com) covers bestbuy.com only; nothing there covers bestbuy.ca. Scavio fetches the public bestbuy.ca page data on request.

The rest of this section and the US sections below describe bestbuy.com. Search Best Buy (bestbuy.com, US) by keyword, or browse a category or deals page by category id or URL (catalogue categories such as `abcat0101001` All Flat-Screen TVs, and merchandised pages such as `pcmcat1674241939957` All Electronics on Sale), 18 organic products per page, sorted by best match, best selling, best discount, price, rating or newest, filtered by brand, on sale, clearance, open box or a price range: SKU, BSIN, name, brand, model number, URL, image, current price, regular price, savings in dollars and percent, on-sale flag, the deal badge (`Holiday Deal`, `BlackFriday`, `Doorbuster`...) and deal end time, condition, rating, review count, seller type (`best_buy` or `marketplace`), product type, badges and release date, plus the total result count, the filter sidebar with product counts, the sort options and related searches. Read one product by SKU or URL with its UPC, model, status, category path, price block, financing offer, every open-box offer by condition (fair, good, excellent) with its price and its savings against new and against the regular price, other conditions and sellers of the same product, the AI review summary and what customers love, description, features, what is included, the full specification table by group, dimensions, images and manuals. Check one SKU's store pickup status at up to 8 Best Buy stores (the stores nearest a ZIP, or store ids you pass): in stock, limited (with the real count when Best Buy shows "only N left"), ship to store, out of stock, not available for pickup, or unknown with a reason, plus the pickup date. Find the stores near a ZIP with 35 days of dated opening hours, get today's Deal of the Day and the more-deals row with live prices, price up to 15 SKUs in one call, page Best Buy's own customer reviews 20 at a time with the star histogram, recommended percent and the most mentioned pros and cons, and pull the search box's autocomplete. All endpoints return structured JSON.

See also: for PC parts with per-store stock counts and open-box units at Micro Center use the `micro-center-api` skill; for the cross-retailer price view use `google-shopping-api`. For Canadian electronics prices at other retailers, see [Pairs well with](#pairs-well-with).

## When to trigger

Use this skill when the user asks to:
- Find TVs, laptops, phones, gaming, appliances or any product at Best Buy by keyword, and compare prices, savings, ratings and brands
- Track Best Buy prices or price drops on a list of SKUs, or build a Best Buy price tracker (one `/prices` call covers up to 15 SKUs)
- Get Best Buy open-box prices by condition (fair, good, excellent) and how much each saves against new and against the regular price
- Check whether a Best Buy item is in stock for store pickup near a ZIP code, or at specific stores, for an in-stock tracker or restock monitor
- Get today's Best Buy Deal of the Day and the other deals on that page with live prices
- List a Best Buy category or deals page (All Electronics on Sale, clearance, open-box only) sorted by best discount or price
- Read the UPC, model number and full specification table of a Best Buy product
- Find Best Buy stores near a ZIP code with their hours, including holiday hours and closed days
- Read what Best Buy reviewers say, pull only the 1-star reviews, the newest reviews, or the most mentioned pros and cons
- Get Best Buy search autocomplete suggestions for keyword research
- Get Best Buy Canada (bestbuy.ca) prices in CAD for TVs, laptops, consoles or Apple products, with the sale start and end dates and the environmental handling fee by province
- Check how many units of an item each Best Buy Canada store near a postal code has, or compare the units at stores in different provinces
- List Best Buy Canada's Black Friday, top deals, clearance, open box or refurbished collection
- Read Best Buy Canada open-box and refurbished SKUs with their own prices, or the questions shoppers asked about a product with the top answer
- Compare one product's Best Buy Canada price with Amazon.ca, Walmart.ca, Costco Canada or Canadian Tire

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Most US calls cost 2 credits (stores and suggestions 1, deals and pcmcat category pages 3), so the free credits cover about 25 US calls; every Best Buy Canada call costs 1 credit, so they cover 50 Canada calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off (Hobby is $15 a
month for 3,000 credits; Growth works out to $1 per 1,000 credits).

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. The cost depends on `country`: the **US** costs below are unchanged, and every **Best Buy Canada** call (`country: "ca"`, and `/questions`) costs **1 credit**. US calls take 2-6 seconds; US `/availability` takes 5-20 seconds (it checks each store in turn); Canada calls take 1-20 seconds (a collection page can take about 12). Allow a client timeout of at least 60 seconds.

| Endpoint | US credits | Canada credits | What it returns |
|---|---|---|---|
| `POST /api/v1/bestbuy/search` | 2 | 1 | US: 18 organic products per page: position, SKU, BSIN, name, brand, model, URL, image, price, regular price, savings and savings percent, on-sale flag, deal badge, deal end time, condition, rating, review count, seller type, product type, badges, release date. Plus total results and pages, the applied sort and filters, the category, the filter sidebar (`facets[]` with values and counts), sort options, related searches and any spelling correction. Canada: 1-100 per page (default 24) with sale end date, EHF and the marketplace seller |
| `POST /api/v1/bestbuy/category` | 2 for an `abcat` id, 3 for a `pcmcat` page | 1 | One category or deals page by `category_id` or URL, in the same shape as search, with the same filters and sorts (no `best_match` in the US). Canada adds the category's parents and subcategories with product counts |
| `POST /api/v1/bestbuy/product` | 2 | 1 | One product by SKU or URL: SKU, BSIN, name, brand, model, UPC, URL, status, condition, product type, category path, price block, financing, `open_box[]` per condition (fair, good, excellent) with price, savings vs new, savings vs regular, savings percent and URL, seller type, other offers, rating, review count, AI review summary, what customers love, description, features, included items, specifications, dimensions, images, manuals, badges, release date. Canada: UPC, sale start and end (UTC), EHF by province, online units, open-box and refurbished SKUs with their own prices, warranty; `rating` is null |
| `POST /api/v1/bestbuy/reviews` | 2 | 1 | One product's Best Buy reviews, 20 per page, sorted or filtered to one star rating: average rating, review count, recommended percent, star distribution, pros and cons with mention counts, total results for the filter, page count and `has_more`. Each review: id, title, text, rating, author, date, recommended, verified-purchase and incentivized flags, days of ownership, helpful and not-helpful votes, badges, photos, syndication source, the SKU reviewed when it is a sibling SKU, and the brand's response. Canada: 1-100 per page, a summary with Best Buy Canada's AI summary, verified-only and with-photos filters, no reviewer names |
| `POST /api/v1/bestbuy/availability` | 2 | 1 | US: store pickup status of one SKU at up to 8 stores (nearest a ZIP, default 5, or the `store_ids` you pass): status, quantity (only for `limited`), pickup date, minimum hours until pickup, the nearby store Best Buy suggests when this one cannot fill it, and a reason when the status is `unknown`. Plus store and in-stock counts and a count per status. Canada: **exact units** of 1-20 SKUs at up to 50 stores near a postal code (default 10) or at `store_ids`, with online units and order limit; no prices |
| `POST /api/v1/bestbuy/stores` | 1 | 1 | US: Best Buy stores near a US ZIP, nearest first, up to 15: store id, name, address, city, state, ZIP, country, phone, open status, store type, distance in miles, and dated hours for the next 35 days (holiday hours and closed days included). Canada: stores near a postal code, in a city or near latitude / longitude (1-100, default 20) with address, phone, distance in km, 7 dated days of hours, services and pickup options |
| `POST /api/v1/bestbuy/deals` | 3 | 1 | US: today's Deal of the Day and the more-deals row under it, up to 15 products with live prices: SKU, name, URL, image, rating, review count, price, regular price, savings, savings percent, on-sale flag, badge, deal end time, plus the page's countdown end. No parameters. Canada: one deal collection (`black_friday`, `top_deals`, `clearance`, `open_box`, `refurbished`) as a listing, with the collection's own dates text; bestbuy.ca has no Deal of the Day |
| `POST /api/v1/bestbuy/prices` | 2 per call | 1 per call | US: current prices for 1-15 SKUs in one call: price, regular price, savings, savings percent, on-sale flag and deal badge per SKU (`deal_ends_at` is usually null here; read the end time from `/product`), `found: false` for a SKU Best Buy does not know. Canada: 1-20 SKUs with sale end date, EHF by province, rating and seller type |
| `POST /api/v1/bestbuy/suggestions` | 1 | 1 | US: the search box's autocomplete for a partial term: each suggested term with the categories (id and name) and SKUs Best Buy shows for it, plus any spelling correction. Canada: terms only, each flagged when it is a brand |
| `POST /api/v1/bestbuy/questions` | -- | 1 | Canada only: customer questions about one product, 1-50 per page (default 10), most answered or newest, each with its answer count and the top answer |

## Workflow (US)

1. **Find products:** call `/bestbuy/search` with `query`, or `/bestbuy/category` with a `category_id` (or a category page `url`). Each row has a `sku` and a `url`. To drill down, take a `category_id` from the `category_facet` values in `facets[]`, or a category id from a product's `category_path[]`.
2. **Narrow the listing:** pass `filters` (`brand`, `on_sale`, `clearance`, `open_box`, and `min_price` with `max_price`) and a `sort` such as `best_discount` or `price_low`. `applied_filters[]` echoes what Best Buy applied. The `brand` value must be spelled as in the Brand filter (a `brand_facet` value).
3. **One product in full:** call `/bestbuy/product` with the row's `sku` (or its `url`). Read `open_box[]` for each open-box condition's price, `specifications[]` for the spec table, and `upc` and `model` for matching against other retailers.
4. **Store pickup:** call `/bestbuy/availability` with the `sku` and the user's `zip` (and `max_stores`, up to 8), or with `store_ids` from a `/bestbuy/stores` answer. Read each store's `status` and `pickup_date`.
5. **Store hours:** call `/bestbuy/stores` with the `zip` for addresses, phone numbers and dated hours; a store's `store_id` feeds `store_ids` on `/availability`.
6. **Price tracking:** keep a list of SKUs and call `/bestbuy/prices` with up to 15 at a time. Compare `price` across runs to detect a drop; `badge` and `deal_ends_at` say which deal applies and when it ends when Best Buy publishes it.
7. **Daily deals:** call `/bestbuy/deals` once a day for the Deal of the Day (`deal_of_the_day`) and the rest of the row (`deals[]`).
8. **Reviews:** call `/bestbuy/reviews` with the `sku`; page with `page`, sort with `sort` (`newest`, `lowest_rated`...) or keep one star rating with `rating`. Check `has_more` and `total_results`.
9. **Keyword research:** `/bestbuy/suggestions` with a partial term returns the suggested terms with category ids and SKUs; feed a term back into `/bestbuy/search` or a SKU into `/bestbuy/product`.

## Parameters (US)

Every US endpoint also takes `country` (`us`, the default, or `ca`: see [Best Buy Canada](#best-buy-canada-country-ca) for the Canada parameters).

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-100). 18 products per page |
| `sort` | string | `best_match` | `best_match`, `best_selling`, `best_discount`, `price_low`, `price_high`, `rating` or `newest` |
| `filters` | object | none | `brand` (string, as spelled in the Brand filter), `on_sale` (boolean), `clearance` (boolean), `open_box` (boolean), `min_price` and `max_price` (dollars, pass both, `min_price` below `max_price`). Combine freely |
| `include_sponsored` | boolean | `false` | Also return the sponsored tiles Best Buy mixes into the grid, flagged `sponsored: true` with `position: null` |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string | one of | Best Buy category id: `abcat` plus 7 digits (catalogue categories, e.g. `abcat0101001` All Flat-Screen TVs), `pcmcat` plus digits (merchandised pages, e.g. `pcmcat1674241939957` All Electronics on Sale), or `cat` plus digits |
| `url` | string | one of | A bestbuy.com category page URL (`.../<id>.c?id=<id>`), used when `category_id` is not given. Filters in the URL (`qp=...`) are kept; its sort is not, use `sort` |
| `page` | integer | 1 | Results page, 1-based (1-100). 18 products per page |
| `sort` | string | page default | `best_selling` (the default on most pages), `best_discount`, `price_low`, `price_high`, `rating` or `newest`. `best_match` is search-only |
| `filters` | object | none | The same as search |
| `include_sponsored` | boolean | `false` | The same as search |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | Best Buy SKU, the 6-9 digit number after `/sku/` in a product URL (a result's `sku`, e.g. `6607832`) |
| `url` | string | one of | bestbuy.com product URL that names a SKU: `/product/<name>/<id>/sku/<sku>` or `/site/<name>/<sku>.p?skuId=<sku>`. Used when `sku` is not given |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | Best Buy SKU |
| `url` | string | one of | bestbuy.com product URL that names a SKU, used when `sku` is not given |
| `page` | integer | 1 | Reviews page, 1-based (1-500). 20 reviews per page |
| `sort` | string | `most_relevant` | `most_relevant`, `most_helpful`, `newest`, `oldest`, `highest_rated` or `lowest_rated` |
| `rating` | integer | all | Only reviews with this many stars, 1-5 |

### Availability (`/availability`)

Pass `sku` or `url`, and exactly one of `zip` or `store_ids`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string | one of | Best Buy SKU |
| `url` | string | one of | bestbuy.com product URL that names a SKU, used when `sku` is not given |
| `zip` | string | one of | US ZIP code: check the stores nearest it (`94103` or `94103-1234`) |
| `max_stores` | integer | 5 | With `zip`: how many of the nearest stores to check, 1-8 |
| `store_ids` | array or string | one of | Check these stores instead: Best Buy store numbers (a `/stores` result's `store_id`), an array or a comma-separated string, up to 8 |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | required | US ZIP code (`94103` or `94103-1234`). There is no latitude/longitude or radius parameter |

### Deals (`/deals`)

No parameters: send `{}`.

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `skus` | array or string | required | 1-15 Best Buy SKUs, an array (`["6607832", "6673112"]`) or a comma-separated string |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

## Best Buy Canada (`country: "ca"`)

Send `country: "ca"` on any of the nine endpoints, or call `/questions` (Canada only, `country` defaults to `ca` there). Best Buy Canada is bestbuy.ca, Best Buy's Canadian store: 142 stores across Canada per Best Buy's FY2026 10-K, plus a marketplace of third-party sellers. Every Canada call costs **1 credit**. Prices are in Canadian dollars (CAD), as Best Buy Canada gives them. `language` is `en` (default) or `fr`: SKUs and prices are the same, names, specifications, facet values and links come back in French. SKUs are Best Buy Canada's own numbers (usually 8 digits, e.g. `19791103`), not bestbuy.com's; a `bestbuy.ca/en-ca/product/<name>/<sku>` or `/fr-ca/produit/<name>/<sku>` link works too. Store numbers come from `/stores` with `country: "ca"` (e.g. `651`).

### Price is national, the EHF is not

- **The price is the same in every province and store.** Only the environmental handling fee (`ehf`) changes by province. Pass `province` (default `ON`) to get `ehf` for that province; `ehf_by_province[]` lists the fee per province where Best Buy Canada gives one. The captured TCL 55" TV had `ehf` 0 for Ontario and 16.75 in Quebec. There are no per-store prices to ask for.
- **Units are exact counts per store.** `/availability` returns `units` on hand at each store: the MacBook Air (SKU `19791103`) had 35 units at the Centreville store in Montreal (captured below) and 20 at a Vancouver store on Nov 25, 2026.
- **Sales carry dates.** `/product` returns `sale_starts_at` and `sale_ends_at` in UTC (ISO 8601); listings and `/prices` return `sale_ends_at`.
- **Open-box and refurbished are their own SKUs.** `/product` lists them in `open_box[]` (Geek Squad Open Box, Open Box, Refurbished) with their own SKU, price, regular price and seller; pass that SKU to `/prices` or `/availability`.

### Canada parameters

| Endpoint | Parameters |
|---|---|
| `/search` | `query` (required, 1-200 chars), `page` (1-based), `page_size` (1-100, default 24), `sort` (`best_match`, `price_low`, `price_high`, `rating`), `filters`, `include_sponsored`, `province`, `language` |
| `/category` | `category_id` (numeric, e.g. `21344` Televisions, a slug id such as `homegardentools`, or `departments` for the top level) or a bestbuy.ca category `url`, plus every listing parameter of search |
| `/deals` | `collection` (`black_friday`, `top_deals` (default), `clearance`, `open_box`, `refurbished`), plus every listing parameter of search |
| `/product` | `sku` or `url`, `province`, `language` |
| `/reviews` | `sku` or `url`, `page`, `page_size` (1-100, default 20), `sort` (`most_relevant`, `most_helpful`, `newest`, `oldest`, `highest_rated`, `lowest_rated`), `rating` (1-5), `verified_only`, `with_photos`, `language` (`fr`: French-language reviews only) |
| `/availability` | `sku` or `url`, or `skus` (1-20); and exactly one of `postal_code` (with `max_stores` 1-50, default 10) or `store_ids` (up to 50); `language` |
| `/stores` | `postal_code` (e.g. `M5V 3L9`, with `radius_km` 1-100, default 25), or `city` (e.g. `Winnipeg`), or `latitude` + `longitude`; `limit` (1-100, default 20); `language` |
| `/prices` | `skus` (1-20, an array or a comma-separated string), `province`, `language` |
| `/suggestions` | `query` (required, 1-100 chars), `language` |
| `/questions` | `sku` or `url`, `page`, `page_size` (1-50, default 10), `sort` (`most_answered` (default), `newest`), `language` |

`filters` on search, category and deals: `brand`, `on_sale`, `clearance`, `open_box`, `min_price` and `max_price` (CAD), `rating` (3, 4 or 5: that many stars and up), `sold_by` (`best_buy` or `marketplace`), `seller`, `in_stock_online`, and `facets` (up to 10 `{facet, value}` pairs taken from a response's `facets[]`). `on_sale` and `clearance` together match either one (the site's Current Offers filter). `province` is one of `AB`, `BC`, `MB`, `NB`, `NL`, `NS`, `NT`, `NU`, `ON`, `PE`, `QC`, `SK`, `YT`.

### Canada workflow

1. **Find products:** `/search` with `country: "ca"` and `query`, `/category` with a `category_id` (walk the tree from `departments` through `category.subcategories[]`), or `/deals` with a `collection`. Read `products[].sku`, `price`, `sale_ends_at`, `seller_type`.
2. **One product in full:** `/product` with the `sku` for UPC, model, sale start and end, `ehf_by_province`, online units and the open-box / refurbished SKUs.
3. **Store stock:** `/stores` with a postal code or city for store numbers, then `/availability` with the SKU (or up to 20 `skus`) and `postal_code` or `store_ids` for the exact units at each store.
4. **Price tracking:** `/prices` with up to 20 SKUs per call; compare `price` across runs and read `sale_ends_at` for when the current sale price ends.
5. **Rating and shopper questions:** `/reviews` for the rating summary and review text, `/questions` for what shoppers asked and the top answer.

### Canada traps

- **`unknown` is never out of stock.** On `/availability`, a store Best Buy Canada returned no stock record for comes back `status: "unknown"` with `units: null`. Say "could not confirm" for it. `out_of_stock` means the store reported 0 units.
- **No per-store prices.** The price is national; `/availability` returns units only. Read the price from `/product` or `/prices` and do not present a store as cheaper than another.
- **`rating` and `review_count` are null on `/product`.** Read them from `/reviews` (`summary`) or from `/prices` and the listing rows, where they are null when Best Buy Canada has no rating for the item (the captured TCL TV).
- **Results stop at 2,000.** Best Buy Canada serves at most the first 2,000 results of a query (`results_cap: 2000`, `results_capped: true` when the total is larger). A `page` that starts past it is a `400`, not charged. Narrow with filters or a category instead.
- **Sorts.** Canada offers `best_match`, `price_low`, `price_high` and `rating` only; `best_selling`, `best_discount` and `newest` are a `400` for Canada.
- **Deals are collections.** `/deals` with `country: "ca"` reads one named collection, not a Deal of the Day (bestbuy.ca has none). `dates_text` is the collection's own text when its page states dates, and it comes in English only (`collection_text_language: "en"`); the products follow `language`.
- **EHF on listings.** Search, category and deals rows carry `ehf` for `province` but `ehf_by_province: null`; read the fee per province from `/product` or `/prices`.
- **Brand on listings.** Canada listing rows carry no brand field: `brand` is null unless a brand filter is applied. `model` is read from the name when it carries one in parentheses.
- **Marketplace sellers.** `seller_type: "marketplace"` rows are sold by a third-party seller; name the seller exactly as `seller.name` gives it (e.g. `TVOUTLET`), never as Best Buy.
- **Reviews.** No reviewer names, nicknames or locations are returned. `syndicated_from` names the site a review was first posted on (often `bestbuy.com`). Review photos hosted off Best Buy are counted in `photo_count` but not linked.
- **Not-found is charged for Canada.** An unknown SKU or category is a charged `404` (in the US it is not charged). A refused input (`400`) and an upstream failure (`502`) are not charged.
- Not available for Canada: per-store prices (the price is national), a Deal of the Day, results past 2,000, review photos hosted off Best Buy, cart / checkout, price history (poll `/prices` and store it yourself).

### Pairs well with

For Canadian electronics prices across retailers: `amazon-product-data` with `country: "ca"` (Amazon.ca), `walmart-product-data` with `domain: "ca"` (Walmart.ca), `costco-product-data` with `country: "ca"` (Costco Canada) and `canadian-tire-api` (Canadian Tire). Match products by UPC or model number. Each reads the retailer's own site.

### Canada examples

#### Exact units per store

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "ca", "sku": "19791103", "postal_code": "H3B 4W8", "max_stores": 5}'
```

Captured `data`:

```json
{
  "postal_code": "H3B4W8",
  "language": "en",
  "store_count": 5,
  "product_count": 1,
  "requested": 1,
  "products": [
    {
      "sku": "19791103",
      "found": true,
      "name": "Apple MacBook Air 13.6\" w/ Touch ID (2026) - Midnight (Apple M5 / 16GB RAM / 512GB SSD) - English",
      "url": "https://www.bestbuy.ca/en-CA/product/apple-macbook-air-13-6-w-touch-id-2026-midnight-apple-m5-16gb-ram-512gb-ssd-english/19791103",
      "seller_type": "best_buy",
      "online": {
        "status": "InStock",
        "units": 395,
        "purchasable": true,
        "order_limit": 1
      },
      "pickup_status": "InStock",
      "sale_channel": "InStoreAndOnline",
      "in_stock_store_count": 1,
      "stores": [
        { "store_id": "286", "name": "Best Buy Express Plc Montreal Trust", "city": "Montreal", "province": "QC", "type": "SmallFormat", "units": 0, "status": "out_of_stock", "reservable": false },
        { "store_id": "252", "name": "Best Buy Mobile Montreal Eaton Centre", "city": "Montreal", "province": "QC", "type": "Mobile", "units": 0, "status": "out_of_stock", "reservable": false },
        { "store_id": "288", "name": "Best Buy Express Montreal Eaton Centre", "city": "Montreal", "province": "QC", "type": "SmallFormat", "units": 0, "status": "out_of_stock", "reservable": false },
        { "store_id": "651", "name": "Centreville", "city": "Montreal", "province": "QC", "type": "BigBox", "units": 35, "status": "in_stock", "reservable": true },
        { "store_id": "270", "name": "Best Buy Express Alexis Nihon Plaza", "city": "Montreal", "province": "QC", "type": "SmallFormat", "units": 0, "status": "out_of_stock", "reservable": false }
      ]
    }
  ],
  "note": "units are the exact on-hand counts Best Buy Canada publishes per store. status unknown (units null) means Best Buy Canada returned no stock record for that store, not that it is out of stock. Prices are national: read them from product or prices."
}
```

`units` is the exact count each store reported; `in_stock_store_count` counts the stores with `status: "in_stock"`. `online.units` is the online stock.

#### Product with sale dates, EHF and open box

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "ca", "sku": "19791103"}'
```

Captured `data` (warranty, description, long description, what's in the box, 25 specifications, 15 images and the URL map trimmed; the rest kept):

```json
{
  "sku": "19791103",
  "name": "Apple MacBook Air 13.6\" w/ Touch ID (2026) - Midnight (Apple M5 / 16GB RAM / 512GB SSD) - English",
  "brand": "APPLE",
  "model": "MDHE4LL/A",
  "upc": "195950690200",
  "url": "https://www.bestbuy.ca/en-ca/product/apple-macbook-air-13-6-w-touch-id-2026-midnight-apple-m5-16gb-ram-512gb-ssd-english/19791103",
  "language": "en",
  "condition": "Brand New",
  "product_type": "Hardgood",
  "category": {
    "id": "12746017",
    "name": "Apple MacBook Air"
  },
  "price": 1589.99,
  "regular_price": 1789.99,
  "savings": 200,
  "savings_percent": 11.2,
  "on_sale": true,
  "savings_hidden": false,
  "clearance": false,
  "sale_starts_at": "2026-11-19T04:30:00Z",
  "sale_ends_at": "2026-12-03T07:00:00Z",
  "province": "ON",
  "ehf": 0,
  "ehf_by_province": [
    { "province": "NL", "amount": 0.6 },
    { "province": "PE", "amount": 0.4 },
    { "province": "BC", "amount": 0.5 },
    { "province": "SK", "amount": 0.45 },
    { "province": "MB", "amount": 0.45 },
    { "province": "QC", "amount": 0.6 },
    { "province": "NB", "amount": 0.65 },
    { "province": "YT", "amount": 2 },
    { "province": "NS", "amount": 0.4 },
    { "province": "AB", "amount": 0.3 },
    { "province": "NT", "amount": 3 }
  ],
  "seller_type": "best_buy",
  "seller": {
    "id": "bbyca",
    "name": "Best Buy Canada"
  },
  "online": {
    "status": "InStock",
    "units": 408,
    "available": true,
    "button": "AddToCart"
  },
  "in_store_status": "Available",
  "purchasable": true,
  "preorder": {
    "preorderable": false,
    "release_date": "2026-03-11 03:30:00 AM"
  },
  "open_box": [
    {
      "sku": "19833113",
      "condition": "Geek Squad Open Box",
      "name": "Open Box - Apple MacBook Air 13.6\" w/ Touch ID (2026) - Midnight (Apple M5 / 16GB RAM / 512GB SSD) - English",
      "price": 1429.99,
      "regular_price": 1474.99,
      "savings": 45,
      "savings_percent": 3.1,
      "on_sale": true,
      "savings_hidden": false,
      "seller_type": "best_buy",
      "seller": {
        "id": "bbyca",
        "name": "Best Buy Canada"
      },
      "url": "https://www.bestbuy.ca/en-CA/product/open-box-apple-macbook-air-13-6-w-touch-id-2026-midnight-apple-m5-16gb-ram-512gb-ssd-english/19833113"
    }
  ],
  "rating": null,
  "review_count": null,
  "machine_translated": false,
  "has_french_content": true,
  "notes": ["rating and review_count are not part of Best Buy Canada's product data: read them from reviews (summary) or prices."],
  "market": {
    "country": "ca",
    "currency": "CAD",
    "language": "en"
  }
}
```

Read it as: CAD 1,589.99 on sale (regular 1,789.99) from 2026-11-19T04:30:00Z to 2026-12-03T07:00:00Z, the same price in every province; the EHF for Ontario (`province: "ON"`) is 0 and Quebec's is 0.60. The Geek Squad Open Box unit is its own SKU, `19833113`, at 1,429.99.

#### Black Friday collection

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "ca", "collection": "black_friday"}'
```

Captured `data` (23 of 24 products and the 22 facets trimmed):

```json
{
  "collection": "black_friday",
  "collection_id": "413517",
  "name": "Black Friday Deals",
  "header_title": "Black Friday Deals 2026",
  "dates_text": "Black Friday is Friday, November 27 in 2026, but you can get a head start at Best Buy Canada. Black Friday VIP starts November 18, with the Black Friday Sale kicking off November 19 and running until December 3.",
  "collection_text_language": "en",
  "language": "en",
  "province": "ON",
  "page": 1,
  "page_size": 24,
  "total_results": 6754,
  "results_cap": 2000,
  "results_capped": true,
  "total_pages": 84,
  "has_more": true,
  "sort": "best_match",
  "filters_applied": [],
  "redirect_url": null,
  "related_queries": [],
  "count": 24,
  "products": [
    {
      "position": 1,
      "sku": "20122735",
      "name": "Nintendo Switch 2 Console Bundle with Mario Kart World Digital Download & 3-Month Nintendo Switch Online Individual Membership",
      "brand": null,
      "model": null,
      "url": "https://www.bestbuy.ca/en-ca/product/nintendo-switch-2-console-bundle-with-mario-kart-world-digital-download-3-month-nintendo-switch-online-individual-membership/20122735",
      "image": "https://multimedia.bbycastatic.ca/multimedia/products/1500x1500/201/20122/20122735.jpg",
      "price": 679.99,
      "regular_price": 749.99,
      "savings": 70,
      "savings_percent": 9.3,
      "on_sale": true,
      "savings_hidden": false,
      "sale_ends_at": "2026-12-03T07:00:00Z",
      "clearance": false,
      "ehf": 0,
      "ehf_by_province": null,
      "rating": 4,
      "rating_count": 5,
      "review_count": 5,
      "seller_type": "best_buy",
      "seller": null,
      "online_only": false,
      "in_store_only": false,
      "preorderable": false,
      "category": {
        "id": "25813239",
        "name": "Nintendo Switch 2 Consoles"
      }
    }
  ],
  "market": {
    "country": "ca",
    "currency": "CAD",
    "language": "en"
  }
}
```

Quote `dates_text` as given; it is Best Buy Canada's own text.

#### Prices with EHF by province

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "ca", "skus": ["19791103", "19296507", "19997813"]}'
```

Captured `data` (the first 2 of 3 rows trimmed; the row kept is the TV, whose EHF varies most):

```json
{
  "province": "ON",
  "language": "en",
  "requested": 3,
  "count": 3,
  "prices": [
    {
      "found": true,
      "sku": "19997813",
      "name": "TCL 55\" S4CF 4K UHD HDR Dolby Atmos LED Fire TV Smart TV (55S4CF) - 2026 - Great for Movies & Gaming",
      "url": "https://www.bestbuy.ca/en-CA/product/tcl-55-s4cf-4k-uhd-hdr-dolby-atmos-led-fire-tv-smart-tv-55s4cf-2026-great-for-movies-gaming/19997813",
      "image": "https://multimedia.bbycastatic.ca/multimedia/products/1500x1500/199/19997/19997813.jpg",
      "price": 349.99,
      "regular_price": 499.99,
      "savings": 150,
      "savings_percent": 30,
      "on_sale": true,
      "savings_hidden": false,
      "sale_ends_at": "2026-11-27T07:00:00Z",
      "clearance": false,
      "ehf": 0,
      "ehf_by_province": [
        { "province": "NL", "amount": 17.1 },
        { "province": "PE", "amount": 10.5 },
        { "province": "BC", "amount": 11 },
        { "province": "SK", "amount": 7 },
        { "province": "MB", "amount": 7 },
        { "province": "QC", "amount": 16.75 },
        { "province": "NB", "amount": 14.25 },
        { "province": "YT", "amount": 56 },
        { "province": "NS", "amount": 10.5 },
        { "province": "AB", "amount": 2.75 },
        { "province": "NT", "amount": 40 }
      ],
      "rating": null,
      "rating_count": null,
      "review_count": null,
      "seller_type": "best_buy",
      "seller": null,
      "online_only": false,
      "in_store_only": false,
      "preorderable": false,
      "category": {
        "id": "329719",
        "name": "55 - 59 Inch TVs"
      }
    }
  ],
  "market": {
    "country": "ca",
    "currency": "CAD",
    "language": "en"
  }
}
```

#### Questions (Canada only)

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/questions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "19296507"}'
```

Captured `data` (9 of 10 questions trimmed):

```json
{
  "sku": "19296507",
  "language": "en",
  "page": 1,
  "page_size": 10,
  "sort": "most_answered",
  "total_questions": 96,
  "total_pages": 10,
  "has_more": true,
  "count": 10,
  "questions": [
    { "id": "10868533", "question": "How many scalpers do I have to fight to get one?", "submitted_at": "2025-04-02T19:01:28Z", "answer_count": 18, "syndicated": true, "syndicated_from": "bestbuy.com", "top_answer": { "id": "12070667", "text": "None anymore Scalpers are dumb to buy it now", "submitted_at": "2025-07-24T00:09:09Z", "verified_purchase": false, "helpful_count": 0, "not_helpful_count": 0 } }
  ],
  "note": "Best Buy Canada shows the top answer of each question; answer_count is the total."
}
```

`answer_count` is every answer; Best Buy Canada shows the top answer of each question, so `top_answer` is the only one returned. No asker or answerer names.

## Examples (US)

### Product with open-box prices

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "6607832"}'
```

Captured `data` (13 of 14 features, 4 of 7 included items, 92 of 95 specifications, 15 of 16 images, 6 of 7 manuals and 2 of 4 "what customers love" lines trimmed; the description shortened):

```json
{
  "sku": "6607832",
  "bsin": "J2FPJKSV76",
  "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
  "brand": "Insignia™",
  "model": "NS-55F501NA26",
  "upc": "600603311888",
  "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832",
  "status": "active",
  "condition": "new",
  "product_type": "Televisions",
  "category_path": [
    { "id": "abcat0100000", "name": "TV & Home Theater", "url": "https://www.bestbuy.com/site/electronics/tv-home-theater/abcat0100000.c?id=abcat0100000" },
    { "id": "abcat0101000", "name": "TVs", "url": "https://www.bestbuy.com/site/tv-home-theater/tvs/abcat0101000.c?id=abcat0101000" },
    { "id": "abcat0101001", "name": "All Flat-Screen TVs", "url": "https://www.bestbuy.com/site/tvs/all-flat-screen-tvs/abcat0101001.c?id=abcat0101001" }
  ],
  "price": 189.99,
  "regular_price": 349.99,
  "savings": 160,
  "savings_percent": 45,
  "on_sale": true,
  "badge": "Holiday Deal",
  "deal_ends_at": "2026-11-08T23:59:59 CST",
  "financing": null,
  "open_box": [
    { "condition": "fair", "price": 165.99, "savings_vs_new": 24, "savings_vs_regular": 184, "savings_percent": 52, "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832/openbox?condition=fair" },
    { "condition": "good", "price": 171.99, "savings_vs_new": 18, "savings_vs_regular": 178, "savings_percent": 50, "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832/openbox?condition=good" },
    { "condition": "excellent", "price": 176.99, "savings_vs_new": 13, "savings_vs_regular": 173, "savings_percent": 49, "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832/openbox?condition=excellent" }
  ],
  "seller_type": "best_buy",
  "other_offers": [],
  "rating": 4.6,
  "review_count": 4031,
  "review_summary": "Customers admire the excellent picture quality, ease of setup, and ideal size of the 55\" Class F50 Series LED 4K UHD Smart Fire TV. The lightweight design is also appreciated by some users. However, a few customers have noted that the button layout could be more user-friendly and the volume could be improved.",
  "what_customers_love": ["Picture quality looks vibrant and impressive", "Sets up quickly right out of the box"],
  "description": "This 55-inch screen uses 4K Ultra HD technology for vibrant, true-to-life images. HDR10 contrasts bright highlights with dark shadows, so you can catch subtle details. ...",
  "features": [
    { "title": "4k Ultra HD (2160p resolution)", "description": "Enjoy breathtaking HDR10 4K movies and TV shows at 4 times the resolution of Full HD, and upscale your current content to Ultra HD-level picture quality." }
  ],
  "included_items": ["Insignia 55\" Class F50 Series LED 4K UHD Smart Fire TV", "Voice Remote with Alexa", "Batteries (AAA*2)"],
  "specifications": [
    { "group": "Key Specs", "name": "Display Type", "value": "LED" },
    { "group": "Key Specs", "name": "Resolution", "value": "4K (2160p)" },
    { "group": "Key Specs", "name": "Screen Size Class", "value": "55 inches" }
  ],
  "dimensions": { "height": null, "width": "48.4 inches", "depth": null, "weight": null },
  "images": ["https://pisces.bbystatic.com/image2/BestBuy_US/images/products/2c3f0bff-9d72-4850-97ac-879cc3cd8162.jpg"],
  "manuals": [
    { "type": "Warranty Manual", "url": "https://files.bbystatic.com/xR%2BLqpEeZ1WAOL8A%2FGIPkQ%3D%3D/b6e4c80f-2b83-4f4b-b780-e87ba5bd3091" }
  ],
  "badges": ["Best Selling", "Trending Deal", "A Best Buy brand", "A Best Buy Brand"],
  "release_date": "2025-05-01"
}
```

Read the open-box rows as: new is $189.99 on sale (regular $349.99); open-box fair is $165.99, which is $24 below the new sale price and $184 below the regular price (52% off regular). `open_box[]` is sorted by price, cheapest first, and lists only the conditions Best Buy offers right now; it is an empty list when there is no open-box offer.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "tv"}'
```

Captured `data` for `{"query": "tv"}` (17 of 18 products, 26 of 28 facets and 2 of the category facet's 4 values trimmed):

```json
{
  "query": "tv",
  "page": 1,
  "page_size": 18,
  "total_results": 1417,
  "total_pages": 79,
  "sort": "best_match",
  "category": { "id": "abcat0101000", "name": "TVs" },
  "applied_filters": [],
  "corrected_query": null,
  "redirect_url": null,
  "count": 18,
  "sponsored_count": 6,
  "products": [
    {
      "position": 2,
      "sponsored": false,
      "sku": "6607832",
      "bsin": "J2FPJKSV76",
      "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
      "brand": "Insignia",
      "model": "NS-55F501NA26",
      "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832",
      "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/2c3f0bff-9d72-4850-97ac-879cc3cd8162.jpg",
      "price": 189.99,
      "regular_price": 349.99,
      "savings": 160,
      "savings_percent": 45,
      "on_sale": true,
      "badge": "Holiday Deal",
      "deal_ends_at": "2026-11-08T23:59:59 CST",
      "condition": "new",
      "rating": 4.6,
      "review_count": 4031,
      "seller_type": "best_buy",
      "product_type": "Television",
      "badges": ["Best Selling", "Trending Deal", "A Best Buy brand", "A Best Buy Brand"],
      "release_date": "2025-05-01"
    }
  ],
  "facets": [
    {
      "field": "category_facet",
      "name": "Category",
      "value_count": 4,
      "values": [
        { "value": "All Flat-Screen TVs", "count": null, "category_id": "abcat0101001" },
        { "value": "Frame TVs", "count": null, "category_id": "pcmcat1769545828021" }
      ]
    },
    {
      "field": "condition_facet",
      "name": "Condition",
      "value_count": 3,
      "values": [
        { "value": "New", "count": 1937 },
        { "value": "Open-Box", "count": 80 },
        { "value": "Refurbished", "count": 54 }
      ]
    }
  ],
  "sort_options": ["best_match", "best_selling", "best_discount", "price_low", "price_high", "rating", "newest"],
  "related_searches": ["laptop", "monitor", "ps5", "ipad", "xbox"]
}
```

`count: 18` is the organic products on the page; the 6 sponsored tiles on the same page (`sponsored_count: 6`) were left out because `include_sponsored` was not set. The category facet's values carry `category_id`s to pass to `/category`, and `count: null` there because the site shows no count for them.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "abcat0101001"}'
```

The captured page for All Flat-Screen TVs (`total_results: 1329`, `total_pages: 74`, `sort: "best_selling"`, `sponsored_count: 0`, 31 facets) has the same envelope as search with `category_id` in place of `query`. Its first row:

```json
{
  "position": 1,
  "sponsored": false,
  "sku": "6685581",
  "bsin": "J3Z9Z424FK",
  "name": "Hisense - 55\" Class QD5 Hi-QLED Series 4K UHD Smart Roku TV (2026)",
  "brand": "Hisense",
  "model": "55QD5SR",
  "url": "https://www.bestbuy.com/product/hisense-55-class-qd5-hi-qled-series-4k-uhd-smart-roku-tv-2026/J3Z9Z424FK/sku/6685581",
  "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/4044db39-586f-4074-8410-d8deefe260d7.png",
  "price": 179.99,
  "regular_price": 379.99,
  "savings": 200,
  "savings_percent": 52,
  "on_sale": true,
  "badge": "BlackFriday",
  "deal_ends_at": "2026-11-08T23:59:59 CST",
  "condition": "new",
  "rating": 4.1,
  "review_count": 12,
  "seller_type": "best_buy",
  "product_type": "Television",
  "badges": ["Best Selling", "Trending Deal", "Only at Best Buy"],
  "release_date": null
}
```

For open-box listings, add `"filters": {"open_box": true}`; for the biggest markdowns first, `"sort": "best_discount"`.

### Availability

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "6607832", "zip": "94103", "max_stores": 3}'
```

Captured `data`:

```json
{
  "sku": "6607832",
  "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
  "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76",
  "zip": "94103",
  "store_count": 3,
  "in_stock_count": 3,
  "status_counts": { "in_stock": 3 },
  "stores": [
    { "store_id": "187", "name": "San Francisco (13th and Harrison St.)", "zip": "94103", "distance_miles": 0.4, "status": "in_stock", "quantity": null, "pickup_date": "2026-11-08", "min_pickup_hours": 1, "nearby_alternative": null, "reason": null },
    { "store_id": "873", "name": "Colma", "zip": "94014", "distance_miles": 7.3, "status": "in_stock", "quantity": null, "pickup_date": "2026-11-08", "min_pickup_hours": 1, "nearby_alternative": null, "reason": null },
    { "store_id": "499", "name": "Emeryville", "zip": "94608", "distance_miles": 7.9, "status": "in_stock", "quantity": null, "pickup_date": "2026-11-08", "min_pickup_hours": 1, "nearby_alternative": null, "reason": null }
  ]
}
```

`quantity: null` on `in_stock` is expected: Best Buy publishes no unit count for a well-stocked item, so say "in stock for pickup today", never a number of units. The `url` here is a product-family URL (no `/sku/`), so pass `sku`, not this `url`, to the other endpoints.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "94103"}'
```

Captured `data` (14 of 15 stores and 32 of the first store's 35 days of hours trimmed; the closed day kept):

```json
{
  "zip": "94103",
  "count": 15,
  "stores": [
    {
      "store_id": "187",
      "name": "San Francisco (13th and Harrison St.)",
      "address": "1717 Harrison St",
      "address2": null,
      "city": "San Francisco",
      "state": "CA",
      "zip": "94103",
      "country": "US",
      "phone": "415-626-9682",
      "status": "Open",
      "store_type": "Big Box",
      "distance_miles": 0.4,
      "hours": [
        { "date": "2026-11-08", "open": "10:00", "close": "20:00", "closed": false },
        { "date": "2026-11-09", "open": "10:00", "close": "21:00", "closed": false },
        { "date": "2026-11-26", "open": null, "close": null, "closed": true }
      ]
    }
  ]
}
```

The hours are dated, so holiday changes show up on their own day: the same store opens 06:00-22:00 on 2026-11-27 and is closed on 2026-11-26.

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (13 of 14 more-deals rows trimmed):

```json
{
  "countdown_ends": "2026-11-09 00:00",
  "deal_of_the_day": {
    "sku": "6583282",
    "name": "Greenworks - 80-Volt 750 CFM Cordless Handheld Blower (1 x 2.5Ah Battery and 1 x Charger) - Green",
    "url": "https://www.bestbuy.com/product/greenworks-80-volt-750-cfm-cordless-handheld-blower-1-x-2-5ah-battery-and-1-x-charger-green/JJG744553Y",
    "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/c41493e7-fd16-42dc-976e-9d08e4e2defa.jpg",
    "rating": 4.4,
    "review_count": 167,
    "price": 99.99,
    "regular_price": 299.99,
    "savings": 200,
    "savings_percent": 66,
    "on_sale": true,
    "badge": null,
    "deal_ends_at": null
  },
  "count": 15,
  "deals": [
    {
      "sku": "6667482",
      "name": "HP - 14\" Laptop - Intel Processor N150 2025 - 4GB Memory - 128GB Storage - Willow Green",
      "url": "https://www.bestbuy.com/product/hp-14-laptop-intel-processor-n150-2025-4gb-memory-128gb-storage-willow-green/JJGW3FGF97",
      "image": "https://pisces.bbystatic.com/image2/BestBuy_US/images/products/d7fd5894-07b3-4182-bf0d-8332b09021ea.jpg",
      "rating": 4.3,
      "review_count": 47,
      "price": 204.99,
      "regular_price": 349.99,
      "savings": 145,
      "savings_percent": 41,
      "on_sale": true,
      "badge": null,
      "deal_ends_at": null
    }
  ]
}
```

`count: 15` includes the Deal of the Day: `deals[]` holds the other 14. `countdown_ends` is the countdown as the page shows it, with no time zone.

### Prices

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"skus": ["6607832", "6673112", "6679316"]}'
```

Captured `data`:

```json
{
  "count": 3,
  "requested": 3,
  "prices": [
    { "sku": "6607832", "found": true, "price": 189.99, "regular_price": 349.99, "savings": 160, "savings_percent": 45, "on_sale": true, "badge": "Holiday Deal", "deal_ends_at": null },
    { "sku": "6673112", "found": true, "price": 1399.99, "regular_price": 2699.99, "savings": 1300, "savings_percent": 48, "on_sale": true, "badge": "Holiday Deal", "deal_ends_at": null },
    { "sku": "6679316", "found": true, "price": 399.99, "regular_price": 599.99, "savings": 200, "savings_percent": 33, "on_sale": true, "badge": "BlackFriday", "deal_ends_at": null }
  ]
}
```

`count` is the SKUs found, `requested` the SKUs asked for. A SKU Best Buy does not know comes back `"found": false` with every price field null; the call is 2 credits whether it carries 1 SKU or 15.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "6607832", "sort": "newest"}'
```

Captured `data` (19 of 20 reviews trimmed; the review kept is one with a photo):

```json
{
  "sku": "6607832",
  "name": "Insignia™ - 55\" Class F50 Series LED 4K UHD Smart Fire TV",
  "url": "https://www.bestbuy.com/product/insignia-55-class-f50-series-led-4k-uhd-smart-fire-tv/J2FPJKSV76/sku/6607832",
  "page": 1,
  "page_size": 20,
  "sort": "newest",
  "rating_filter": null,
  "average_rating": 4.6,
  "review_count": 4031,
  "recommended_percent": 93,
  "star_distribution": [
    { "stars": 5, "count": 3256, "percent": 81 },
    { "stars": 4, "count": 468, "percent": 12 },
    { "stars": 3, "count": 109, "percent": 3 },
    { "stars": 2, "count": 55, "percent": 1 },
    { "stars": 1, "count": 143, "percent": 3 }
  ],
  "pros": [
    { "feature": "Picture Quality", "mentions": 1917 },
    { "feature": "Setup Ease", "mentions": 245 },
    { "feature": "Size", "mentions": 119 },
    { "feature": "Weight", "mentions": 54 },
    { "feature": "Features", "mentions": 25 }
  ],
  "cons": [
    { "feature": "Volume", "mentions": 7 }
  ],
  "total_results": 4029,
  "total_pages": 202,
  "has_more": true,
  "count": 20,
  "reviews": [
    {
      "id": "91cb7bf0-99ed-35de-b712-95344c256523",
      "title": "Great picture, and color is perfect",
      "text": "I love my 55 inch tv. It shows good quality and sound",
      "rating": 5,
      "author": "SharonM",
      "submitted_at": "2026-11-06T21:34:48.000-06:00",
      "recommended": true,
      "verified_purchase": true,
      "incentivized": false,
      "days_of_ownership": 31,
      "helpful_count": 0,
      "not_helpful_count": 0,
      "badges": ["Incentivized", "Verified Purchaser"],
      "images": ["https://pisces.bbystatic.com/image2/BestBuy_US/ugc/photos/thumbnail/9646250637e1e3ca8f1bfa2a04e8c44a.jpg"],
      "syndicated_from": null,
      "reviewed_sku": null,
      "brand_response": null
    }
  ]
}
```

`review_count` (4,031) is the product's total; `total_results` (4,029) is what the review list returns for this request, so the two can differ slightly. In this capture every review carries an `"Incentivized"` badge while its `incentivized` flag is `false`: report the two as Best Buy gives them and do not infer one from the other.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/bestbuy/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "ps5 con"}'
```

Captured `data` (11 of 13 suggestions trimmed):

```json
{
  "query": "ps5 con",
  "corrected_query": null,
  "count": 13,
  "suggestions": [
    {
      "term": "ps5 controller",
      "categories": [{ "id": "pcmcat1546550106595", "name": "Gaming Controllers" }],
      "skus": ["6601464", "6430163", "6522931", "6497953", "6492317", "6464307", "6464309", "6669065", "6669064"]
    },
    {
      "term": "ps5 console disc",
      "categories": [],
      "skus": ["6646419", "6646420", "10413388", "12906125", "6601553", "12224139", "11939512", "6565695", "12348331"]
    }
  ]
}
```

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def bestbuy(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/bestbuy/{endpoint}", headers=HEADERS, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["data"]

# 1. Biggest open-box markdowns in a category (2 credits)
found = bestbuy("category", {"category_id": "abcat0101001", "sort": "best_discount", "filters": {"open_box": True}})
for p in found["products"][:5]:
    print(p["sku"], p["name"], p["condition"], p["price"], "regular", p["regular_price"], p["badge"])

# 2. One product: open-box price per condition (2 credits)
item = bestbuy("product", {"sku": found["products"][0]["sku"]})
for ob in item["open_box"]:
    print(ob["condition"], ob["price"], "saves", ob["savings_vs_new"], "vs new,", ob["savings_vs_regular"], "vs regular")

# 3. Store pickup near the user (2 credits, 5-20 s)
avail = bestbuy("availability", {"sku": item["sku"], "zip": "94103", "max_stores": 5})
for s in avail["stores"]:
    qty = f' (only {s["quantity"]} left)' if s["status"] == "limited" else ""
    print(s["name"], s["distance_miles"], "mi:", s["status"] + qty, "pickup", s["pickup_date"], s["reason"] or "")

# 4. Price check for a watch list, up to 15 SKUs per call (2 credits)
watch = bestbuy("prices", {"skus": ["6607832", "6673112", "6679316"]})
for p in watch["prices"]:
    print(p["sku"], p["price"] if p["found"] else "not found", p["badge"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Best Buy answered.

- **search** - `query`, `page`, `page_size` (18), `total_results`, `total_pages`, `sort`, `category` ({`id`, `name`} or null), `applied_filters[]` {`field`, `values[]`}, `corrected_query`, `redirect_url`, `count`, `sponsored_count`, `products[]` (`position`, `sponsored`, `sku`, `bsin`, `name`, `brand`, `model`, `url`, `image`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`, `condition`, `rating`, `review_count`, `seller_type`, `product_type`, `badges[]`, `release_date`), `facets[]` {`field`, `name`, `value_count`, `values[]` {`value`, `count`, `category_id` on category values}}, `sort_options[]`, `related_searches[]`.
- **category** - the same as search with `category_id` in place of `query`.
- **product** - `sku`, `bsin`, `name`, `brand`, `model`, `upc`, `url`, `status`, `condition`, `product_type`, `category_path[]` {`id`, `name`, `url`}, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`, `financing` ({`months`, `monthly_payment`, `rate`, `plan_type`} or null), `open_box[]` {`condition`, `price`, `savings_vs_new`, `savings_vs_regular`, `savings_percent`, `url`}, `seller_type`, `other_offers[]` {`sku`, `condition`, `seller_type`}, `rating`, `review_count`, `review_summary`, `what_customers_love[]`, `description`, `features[]` {`title`, `description`}, `included_items[]`, `specifications[]` {`group`, `name`, `value`}, `dimensions` {`height`, `width`, `depth`, `weight`}, `images[]`, `manuals[]` {`type`, `url`}, `badges[]`, `release_date`.
- **reviews** - `sku`, `name`, `url`, `page`, `page_size` (20), `sort`, `rating_filter`, `average_rating`, `review_count`, `recommended_percent`, `star_distribution[]` {`stars`, `count`, `percent`}, `pros[]` and `cons[]` {`feature`, `mentions`}, `total_results`, `total_pages`, `has_more`, `count`, `reviews[]` {`id`, `title`, `text`, `rating`, `author`, `submitted_at`, `recommended`, `verified_purchase`, `incentivized`, `days_of_ownership`, `helpful_count`, `not_helpful_count`, `badges[]`, `images[]`, `syndicated_from`, `reviewed_sku`, `brand_response` ({`text`, `responded_at`, `department`} or null)}.
- **availability** - `sku`, `name`, `url`, `zip` (null with `store_ids`), `store_count`, `in_stock_count` (stores with `in_stock` or `limited`), `status_counts` {status: number of stores}, `stores[]` {`store_id`, `name`, `zip`, `distance_miles`, `status`, `quantity`, `pickup_date`, `min_pickup_hours`, `nearby_alternative` ({`store_id`, `name`, `zip`, `distance_miles`, `pickup_date`, `quantity`} or null), `reason`}.
- **stores** - `zip`, `count`, `stores[]` {`store_id`, `name`, `address`, `address2`, `city`, `state`, `zip`, `country`, `phone`, `status`, `store_type`, `distance_miles`, `hours[]` {`date`, `open`, `close`, `closed`}}.
- **deals** - `countdown_ends`, `deal_of_the_day` (one deal or null), `count`, `deals[]` {`sku`, `name`, `url`, `image`, `rating`, `review_count`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`}.
- **prices** - `count` (SKUs found), `requested`, `prices[]` {`sku`, `found`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `badge`, `deal_ends_at`}.
- **suggestions** - `query`, `corrected_query`, `count`, `suggestions[]` {`term`, `categories[]` {`id`, `name`}, `skus[]`}.

Best Buy Canada (`country: "ca"`) answers in its own shapes; every Canada `data` carries `market` {`country`, `currency`, `language`}:

- **search / category / deals (ca)** - `language`, `province`, `page`, `page_size`, `total_results`, `results_cap` (2000), `results_capped`, `total_pages`, `has_more`, `sort`, `filters_applied`, `redirect_url`, `related_queries`, `count`, `products[]` (`position`, `sku`, `name`, `brand`, `model`, `url`, `image`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `savings_hidden`, `sale_ends_at`, `clearance`, `ehf`, `ehf_by_province`, `rating`, `rating_count`, `review_count`, `seller_type`, `seller` {`id`, `name`}, `online_only`, `in_store_only`, `preorderable`, `category` {`id`, `name`}), `facets[]` {`facet`, `name`, `values[]` {`value`, `count`, `selected`}}. Search adds `query`; category adds `category_id` and `category` {`id`, `name`, `product_count`, `url`, `parents[]`, `subcategories[]` {`id`, `name`, `product_count`, `has_subcategories`}}; deals adds `collection`, `collection_id`, `name`, `header_title`, `dates_text`, `collection_text_language`.
- **product (ca)** - `sku`, `name`, `brand`, `model`, `upc`, `url`, `urls` {`en`, `fr`}, `language`, `condition`, `product_type`, `category`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `savings_hidden`, `clearance`, `sale_starts_at`, `sale_ends_at`, `province`, `ehf`, `ehf_by_province[]` {`province`, `amount`}, `seller_type`, `seller`, `online` {`status`, `units`, `available`, `button`}, `in_store_status`, `purchasable`, `preorder` {`preorderable`, `release_date`}, `open_box[]` {`sku`, `condition`, `name`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `savings_hidden`, `seller_type`, `seller`, `url`}, `warranty`, `rating` (null), `review_count` (null), `description`, `long_description`, `whats_in_the_box[]`, `specifications[]` {`group`, `name`, `value`}, `images[]`, `machine_translated`, `has_french_content`, `notes[]`.
- **reviews (ca)** - `sku`, `language`, `page`, `page_size`, `sort`, `rating_filter`, `verified_only`, `with_photos`, `summary` {`average_rating`, `rating_count`, `review_count`, `star_distribution[]` {`stars`, `count`}, `recommended` {`yes`, `no`, `percent`}, `key_considerations`, `english_review_count`, `french_review_count`, `ai_summary`}, `total_results`, `total_pages`, `has_more`, `count`, `reviews[]` {`id`, `title`, `text`, `rating`, `submitted_at`, `recommended`, `verified_purchase`, `incentivized`, `helpful_count`, `not_helpful_count`, `key_considerations`, `photo_count`, `photos[]`, `syndicated`, `syndicated_from`}.
- **availability (ca)** - `postal_code`, `language`, `store_count`, `product_count`, `requested`, `products[]` {`sku`, `found`, `name`, `url`, `seller_type`, `online` {`status`, `units`, `purchasable`, `order_limit`}, `pickup_status`, `sale_channel`, `in_stock_store_count`, `stores[]` {`store_id`, `name`, `city`, `province`, `type`, `units`, `status` (`in_stock`, `out_of_stock`, `unknown`), `reservable`}}, `note`.
- **stores (ca)** - `postal_code`, `city`, `latitude`, `longitude`, `located`, `radius_km`, `language`, `total_results`, `count`, `stores[]` {`store_id`, `name`, `type` (`BigBox`, `SmallFormat`, `Mobile`, `ExpressKiosk`), `format`, `address`, `address2`, `landmark`, `city`, `province`, `postal_code`, `phone`, `latitude`, `longitude`, `distance_km`, `utc_offset`, `hours[]` (7 dated strings as the site shows them, e.g. `"Friday   Nov 27 8 AM - 10 PM"`), `services[]`, `pickup_options[]`, `hold_days`}.
- **prices (ca)** - `province`, `language`, `requested`, `count`, `prices[]` {`found`, `sku`, `name`, `url`, `image`, `price`, `regular_price`, `savings`, `savings_percent`, `on_sale`, `savings_hidden`, `sale_ends_at`, `clearance`, `ehf`, `ehf_by_province`, `rating`, `rating_count`, `review_count`, `seller_type`, `seller`, `online_only`, `in_store_only`, `preorderable`, `category`}.
- **suggestions (ca)** - `query`, `sent_query` (accents removed before asking), `language`, `count`, `suggestions[]` {`term`, `is_brand`}.
- **questions (ca only)** - `sku`, `language`, `page`, `page_size`, `sort`, `total_questions`, `total_pages`, `has_more`, `count`, `questions[]` {`id`, `question`, `submitted_at`, `answer_count`, `syndicated`, `syndicated_from`, `top_answer` {`id`, `text`, `submitted_at`, `verified_purchase`, `helpful_count`, `not_helpful_count`}}, `note`.

## Guardrails

- These guardrails are for bestbuy.com unless they say Canada; the Canada-specific ones are in [Canada traps](#canada-traps). Never mix the two markets: a bestbuy.com SKU is not a bestbuy.ca SKU.
- US prices are in US dollars: `189.99` is $189.99. With `country: "ca"` prices are in Canadian dollars as Best Buy Canada gives them; say CAD.
- Report prices, savings and labels as Best Buy gives them. Do not call a price the lowest or a deal good or bad; `regular_price` is Best Buy's own regular price, so describe it as that.
- `savings` and `savings_percent` are measured against `regular_price`. On an open-box offer, `savings_vs_new` is against the current new price (the sale price when the item is on sale) and `savings_vs_regular` against the regular price; `savings_percent` on an open-box offer is against the regular price.
- `open_box[]` lists only the conditions Best Buy offers right now, cheapest first, and is empty when there is none. Never quote an open-box price for a condition that is not in the list, and never claim a number of open-box units: the response has none.
- `deal_ends_at` is the deal's end time as Best Buy gives it (`"2026-11-08T23:59:59 CST"`), and is null on many items, including all of the captured `/prices` and `/deals` rows. When it is null, do not state when the price ends. `countdown_ends` on `/deals` carries no time zone.
- Availability is store PICKUP status, not a shelf count. `quantity` is set only on `limited` (Best Buy shows "only N left"); on `in_stock` it is null because Best Buy publishes no unit count for well-stocked items. Never claim a store has a number of units unless `status` is `limited`, and then quote exactly that `quantity`.
- The statuses: `in_stock` (in the store now), `limited` (in the store now, `quantity` units), `ship_to_store` (not on the shelf; Best Buy can ship it to the store for pickup by `pickup_date`), `out_of_stock` (pickup-eligible but none in the store), `not_available_for_pickup` (the item cannot be picked up at this store), and `unknown`. `unknown` is never out of stock: `reason` says why the store's answer was missing (`store_check_failed`, `sku_not_in_store_results`, `store_not_applied`). Say "could not confirm" for `unknown`, or retry.
- `in_stock_count` counts stores with `in_stock` or `limited`. `pickup_date` is null for `out_of_stock` and `not_available_for_pickup`; `min_pickup_hours` is set only for `in_stock` and `limited`.
- With `store_ids` instead of `zip`, `distance_miles` is null (there is no point to measure from) and `zip` at the top level is null.
- `/availability` checks at most 8 stores per call (default 5 nearest the ZIP). For more stores, call again with the next `store_ids` from `/stores`.
- `/stores` takes a US ZIP only: no latitude/longitude, no radius, and no lookup by store id. It returns up to 15 stores, nearest first. The hours are dated for 35 days: read the entry for the day the user asks about rather than assuming a weekly pattern.
- Search and category return 18 organic products per page; `position` counts organic products only. Sponsored tiles are left out unless `include_sponsored: true`, and then carry `sponsored: true` and `position: null`. `sponsored_count` is how many sponsored tiles the page had either way.
- `min_price` and `max_price` go together: one without the other is a 400. `brand` must match the site's Brand filter spelling (a `brand_facet` value); `applied_filters[]` shows what Best Buy actually applied, so check it before claiming a list is filtered.
- `best_match` is a search sort only; on `/category` it is a 400. A category's default sort is the page's own, usually `best_selling`.
- A `pcmcat` category page costs 3 credits (the page is read first for its built-in filters); an `abcat` id costs 2. A page with no product grid is a 404: pick one of its subcategories from `facets[]` (`category_facet`) instead.
- The `url` on `/availability` and `/deals` rows can be a product-family URL without `/sku/` (every captured one is); passing such a URL as `url` is a 400. Use the row's `sku`.
- `brand` can be spelled differently on a listing row and the product answer (`"Insignia"` in search, `"Insignia™"` on `/product`), and `badges[]` can repeat with different capitalization (`"A Best Buy brand"`, `"A Best Buy Brand"`). Match on `sku`, not on brand or name text.
- `dimensions` fields are null when Best Buy does not list them (the captured TV gives only `width`); read `specifications[]` for the full set.
- `/prices` is 2 credits per call for 1 to 15 SKUs; batch SKUs instead of calling `/product` per SKU when only the price is needed. If every SKU is unknown, the call is a 404.
- Reviews are Best Buy's own first-party reviews. `has_more: true` means more pages exist; do not claim to have read every review unless `has_more` is false. `total_results` counts the reviews matching the request (with `rating` set, only that star rating); `review_count` is the product's total.
- `reviewed_sku` is set when a review was written for a sibling SKU of the same product (another color or size); `syndicated_from` names the site a review was first posted on. `brand_response` is the manufacturer's reply when there is one.
- `/suggestions` returns suggested terms with category ids and SKUs only, no prices or search volumes.
- There is no price history and no price-match data, and the questions endpoint is Best Buy Canada only (`/questions` with a US SKU is not a bestbuy.com Q&A): track prices by calling `/prices` on a schedule and storing the results yourself.
- This API reads public product data for research, price monitoring and stock alerts. It does not add to cart, check out or reserve stock; do not present it as a purchasing bot.
- Never fabricate prices, open-box offers, stock, units, pickup dates, deal end times, EHF amounts or reviews. Only return what the API returned, with the product `url` or `sku`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`, a `page` outside 1-100 (reviews 1-500), an unknown `sort` or `best_match` on `/category`, `min_price` without `max_price` or `min_price` not below `max_price`, a `sku` that is not 6-9 digits, a `url` that is not bestbuy.com or names no SKU, a `category_id` that is not `abcat`/`pcmcat`/`cat` plus digits, neither `sku` nor `url`, both or neither of `zip` and `store_ids`, `max_stores` outside 1-8, more than 8 `store_ids`, a ZIP that is not 5 digits, `rating` outside 1-5, or more than 15 `skus`).
- For Canada, `400` also covers a `best_selling`, `best_discount` or `newest` sort, a `page` that starts past the first 2,000 results, a `province` that is not a Canadian province or territory code, a `sku` that is not a Best Buy Canada SKU, a `url` that is not a bestbuy.ca link, a `postal_code` that is not a Canadian postal code, both or neither of `postal_code` and `store_ids`, more than 20 `skus` or 50 `store_ids`, an unknown `collection`, and `/questions` with a `country` other than `ca`. Not charged.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product (unknown SKU), no such category or a page without a product grid, or a `/prices` call where every SKU is unknown. Not charged in the US; **charged (1 credit) for Canada**. Re-run the search for a fresh `sku` rather than retrying the same one.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data).
- `502` or `503` means Best Buy is temporarily unavailable or returned an unusable page (on `/availability`, when no store could be checked at all). Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds. A single store that could not be checked comes back as `status: "unknown"` with `reason: "store_check_failed"` instead of failing the call.

## SDKs

```bash
pip install scavio==0.92.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

found = client.best_buy.search("tv", sort="best_discount", filters={"open_box": True})
item = client.best_buy.product(sku=found["data"]["products"][0]["sku"])

# Best Buy Canada: the same methods with country="ca" (1 credit per call)
ca = client.best_buy.search("4k tv", country="ca", sort="price_low")
units = client.best_buy.availability(sku="19791103", postal_code="H3B 4W8", country="ca")
prices = client.best_buy.prices(["19791103", "19296507"], country="ca", province="QC")
questions = client.best_buy.questions(sku="19296507")  # Canada only
```

```bash
npm install scavio@0.93.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.bestBuy.search({ query: "tv", sort: "best_discount", filters: { open_box: true } });
const { data: item } = await scavio.bestBuy.product({ sku: found.products[0].sku });
const { data: pickup } = await scavio.bestBuy.availability({ sku: item.sku, zip: "94103" });
const { data: near } = await scavio.bestBuy.stores({ zip: "94103" });
const { data: prices } = await scavio.bestBuy.prices({ skus: ["6607832", "6673112"] });
const { data: today } = await scavio.bestBuy.deals();
const { data: cat } = await scavio.bestBuy.category({ category_id: "abcat0101001" });
const { data: rev } = await scavio.bestBuy.reviews({ sku: item.sku, rating: 1, sort: "newest" });
const { data: ideas } = await scavio.bestBuy.suggestions({ query: "ps5 con" });

// Best Buy Canada
const { data: caUnits } = await scavio.bestBuy.availability({ country: "ca", sku: "19791103", postal_code: "H3B 4W8" });
const { data: blackFriday } = await scavio.bestBuy.deals({ country: "ca", collection: "black_friday" });
const { data: qa } = await scavio.bestBuy.questions({ sku: "19296507" });
```

## MCP

The Scavio MCP server exposes all ten endpoints as tools: `search_bestbuy`, `get_bestbuy_product`, `get_bestbuy_reviews`, `get_bestbuy_category`, `get_bestbuy_deals`, `get_bestbuy_stores`, `get_bestbuy_availability`, `get_bestbuy_suggestions`, `get_bestbuy_prices` and `get_bestbuy_questions` (Best Buy Canada only). Pass `country: "ca"` to the first nine for Best Buy Canada. Best Buy is opt-in: add `bestbuy` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.92.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,bestbuy"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/bestbuy-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [product](https://scavio.dev/docs/bestbuy-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [reviews](https://scavio.dev/docs/bestbuy-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [category](https://scavio.dev/docs/bestbuy-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [deals](https://scavio.dev/docs/bestbuy-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [stores](https://scavio.dev/docs/bestbuy-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [availability](https://scavio.dev/docs/bestbuy-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [suggestions](https://scavio.dev/docs/bestbuy-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [prices](https://scavio.dev/docs/bestbuy-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data), [questions](https://scavio.dev/docs/bestbuy-questions?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data) (Best Buy Canada only). Each page covers both `country: "us"` and `country: "ca"`. Overview: [Best Buy API](https://scavio.dev/bestbuy-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=best-buy-product-data).
