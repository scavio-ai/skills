---
name: macys-product-data
description: "Macy's product data API: search macys.com or browse any category, brand page or sale section (Sales & Offers, Clearance, Today Only, Last Act, Limited-Time Specials, Black Friday Deals), 60 products per page with current, regular and sale price, percent off, sale end date, deal label, promotions, rating and colors, filtered by brand, color, special offer, any price range, store pickup or any facet, read one product with every variant (UPC, color, size, availability), the rating histogram and fit, or price up to 10 products in one call for a Macy's price tracker, page Macy's own reviews up to 100 at a time, find stores near a ZIP, a point or a city, and check store pickup near you or per size and color at one store. 9 endpoints, 1 credit each. The official Macy's API issues keys only to pre-approved Macy's Partners and has no public catalog search."
version: 1.0.0
tags: macys, macys-api, macys-product-data, macys-scraper, macys-price-tracker, macys-price-drop, macys-sale-alerts, macys-clearance, macys-deals, macys-black-friday, last-act, today-only, macys-in-stock, macys-store-pickup, in-store-availability, store-locator, macys-reviews, department-store, fashion, apparel, clothing-prices, shoes, beauty, home-goods, upc, variant-data, product-search, product-data, product-reviews, review-analysis, category-browse, brand-catalog, batch-products, autocomplete, retail, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/macys-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data
---

# Macy's Product Data API - Search, Prices, Reviews, Store Pickup

Search Macy's (macys.com, US, prices in USD) by keyword, or browse a category by id or URL, a brand's page by its page id or URL, or one of Macy's sale sections (all Sales & Offers, Clearance & Closeout, Today Only, Last Act final-sale markdowns, Limited-Time Specials, Black Friday Deals), 60 organic products per page, sorted by featured, price, top rated, best sellers or newest, filtered by brand, color, special offer, any price range (not only the site's price buckets), items available for pickup at one store, or any other facet the response lists (gender, size, fit, discount range, customer rating...): product id, title, brand, URL, image, current price (and the top of the range when an item sells at a range), regular price, sale price, percent off, price label (`Sale`, `Now`, `Only`, `Your Choice`), on-sale flag, sale end date, deal label (`Black Friday Deal`, `Clearance`, `LAST ACT`, `Limited-Time Special`...), promotions, rating, review count, colors and a sponsored flag, plus the total, total pages, the facets with counts and the filters Macy's applied. Read one product by id or URL with its full title, brand page id, type, description, bullets, category path, the price block with the date the price is valid until, promotions, rating, review count, the written-review count, the star histogram, recommended counts, the fit slider, the AI review summary, the "N customers purchased" line, question and answer counts, images, every color with its own price, sizes, and every variant with UPC, color, size, availability, availability message, low-stock flag and ship days; or price up to 10 products in one call. Page Macy's own reviews up to 100 at a time, sorted or filtered to one star rating or a word. Find Macy's stores near a ZIP, a latitude/longitude or a city and state with today's and tomorrow's hours, curbside hours and the same-day pickup cut-off. Check which stores near you can hand a product over for pickup, or, at one store, which variants can be picked up and which are in the store. Pull the search box's autocomplete. All endpoints return structured JSON, 1 credit each.

See also: for Nordstrom (department-store fashion with per-size stock and units available to ship) use the `nordstrom-product-data` skill; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Build a Macy's price tracker or sale alert: poll a list of products (up to 10 per `/product` call) and detect price drops, new sale prices or a deal label appearing
- Find clothing, shoes, handbags, beauty, home or any product at Macy's by keyword and compare prices, percent off, ratings and brands
- List Macy's clearance, Last Act, Today Only, Limited-Time Special or Black Friday deals, sorted by price or filtered by brand, size or discount range
- Browse a Macy's category or a brand's whole Macy's catalog (Calvin Klein, Levi's...) with prices and sale end dates
- Check whether a Macy's item can be picked up in store near a ZIP code or city, or which sizes and colors can be picked up at one store
- Read the UPC, sizes, colors and per-variant availability of a Macy's product for matching against other retailers
- Find Macy's stores near a ZIP code, a point or a city with today's and tomorrow's hours and the pickup cut-off
- Read what Macy's reviewers say, pull only the 1-star reviews, reviews with photos, or reviews that mention a word, and how a product fits
- Get Macy's search autocomplete suggestions for keyword research

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Product, reviews, stores, store availability and suggestions usually answer in 1-9 seconds. The listing endpoints (search, category, brand, deals) read large pages and are slow: the captured calls took 4 to 62 seconds, so allow a client timeout of at least 90 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/macys/search` | 1 | 60 organic products per page: id, title, brand, URL, image, price, price max, regular price, regular price max, sale price, percent off, percent off max, price label, set value, on-sale flag, sale end date, deal label, currency, rating, review count, colors, promotions, `is_sponsored`. Plus `redirected_to_category`, total, page, total pages, sort, count, `sponsored_dropped`, `applied_filters[]` and `facets[]` with values and counts |
| `POST /api/v1/macys/category` | 1 | One category by `category_id` or URL, the same grid as search, plus the category's id, name and URL |
| `POST /api/v1/macys/brand` | 1 | One brand's Macy's page by `brand_id` (a product's `brand_page_id`) or URL, the same grid as search, plus the brand page's id, name and URL |
| `POST /api/v1/macys/deals` | 1 | A sale section by `type` (`sale`, `clearance`, `today_only`, `last_act`, `limited_time_special`, `black_friday`), the same grid as search plus the section's label |
| `POST /api/v1/macys/product` | 1 | One product by id or URL: title, full title, brand, brand page id and URL, type, description, bullets, categories, the price block, price valid until, promotions, rating, review count, written-review count, rating histogram, recommended and not-recommended counts, fit slider, AI review summary, purchased message, question and answer counts, availability, images, colors (each with its price), sizes, size label, and every variant (UPC, variant id, color, size, available, availability message, low-availability flag, ship days, ship message). Or up to 10 ids in one call (`product_ids`) in Macy's summary view |
| `POST /api/v1/macys/reviews` | 1 | One product's Macy's reviews, newest, highest or lowest rated first or with photos first, 1-100 per page (default 20), optionally one star rating or only reviews mentioning a word: total written reviews, pages and `has_more`. Each review: id, rating, title, text, date, nickname, location, recommended, helpful yes / no votes, incentivized and syndicated flags, the syndication source, badges, fit, slider ratings, photos, brand response |
| `POST /api/v1/macys/stores` | 1 | Macy's stores near a ZIP, a lat/lng point or a city + state, nearest first, up to 15 within the radius (default and maximum 100 miles): store id, name, address, phone, lat, lng, distance in miles, today's and tomorrow's dated hours, curbside hours, the same-day pickup cut-off and store features |
| `POST /api/v1/macys/store-availability` | 1 | Store pickup for one product. Near a location: every store with `available` true / false and Macy's `available_items_count`. At one `store_id`: the store's hours, pickup cut-off, pickup day and pickup options, and per variant (UPC, color, size) `pickup_available`, `in_store_available` and `available_online`. No unit quantities |
| `POST /api/v1/macys/suggestions` | 1 | The macys.com search box's autocomplete for a partial term: up to 7 suggested searches |

## Workflow

1. **Find products:** call `/macys/search` with `query`, `/macys/category` with a `category_id`, `/macys/brand` with a `brand_id`, or `/macys/deals` with a `type`. Each item has an `id` and a `url`.
2. **Narrow the listing:** pass `brand`, `color`, `special_offer` (search, category and brand only), `min_price` / `max_price`, `pickup_store_id`, or any other facet through `filters` as `{"<facets[].name>": "<values[].value>"}`. Check `applied_filters[]` to see what Macy's actually applied.
3. **Drill down:** a product's `categories[]` ids feed `/category`; its `brand_page_id` feeds `/brand`. When a keyword opens a category on the site, search returns that category in `redirected_to_category`.
4. **One product in full:** call `/macys/product` with the item's `id` as `product_id` (or its `url`). Read `variants[]` for UPC, color, size and availability, `colors[]` for each color's price, and `rating_distribution` for the star histogram.
5. **Price tracking:** keep a list of product ids and call `/macys/product` with up to 10 of them in `product_ids` per call (1 credit). Store `price`, `regular_price`, `on_sale`, `sale_ends` and `deal_label` per run and compare runs to detect a drop.
6. **Store pickup:** call `/macys/stores` with the user's `zip` (or `lat` + `lng`, or `city` + `state`) to get `store_id`s, then `/macys/store-availability` with `product_id` and either the same location (which stores can do pickup) or one `store_id` (which variants can be picked up, and which are in the store).
7. **Reviews:** call `/macys/reviews` with the `product_id`; page with `page` and `limit` (up to 100), sort with `sort`, keep one star rating with `rating`, or search the text with `query`. Check `has_more` and `total`.
8. **Keyword research:** `/macys/suggestions` with a partial term returns suggested searches to feed back into `/macys/search`.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-1000). 60 organic items per page |
| `sort` | string | `featured` | `featured`, `price_low_to_high`, `price_high_to_low`, `top_rated`, `best_sellers` or `newest` |
| `brand` | string or array | none | Brands as the `BRAND` facet spells them (`"Levi's"`, `"Calvin Klein"`). A list (up to 20) matches any of them |
| `color` | string or array | none | Colors as the `COLOR_NORMAL` facet lists them (`Black`, `Blue`, `Red`...). A list matches any of them |
| `special_offer` | string or array | none | `limited_time_special`, `gift_with_purchase`, `black_friday_deal`, `clearance`, `last_act`, `our_lowest_price`, `sales_and_discounts`, `special_offer` or `today_only`. A list matches any of them |
| `min_price` | number | none | Minimum price in USD. Any bound works, not only the site's price buckets |
| `max_price` | number | none | Maximum price in USD. Either bound can be sent alone |
| `pickup_store_id` | integer or string | none | Only items available for pickup at this store (a `/stores` `store_id`, e.g. `4592`) |
| `filters` | object | none | Any other facet from a previous response: `facets[].name` to one value or a list of `values[].value` (up to 10 facets), e.g. `{"GENDER": "Women", "CUSTRATINGS": "4 stars & up"}` |
| `include_sponsored` | boolean | `false` | Keep ad-only sponsored tiles. Organic items that also hold a paid slot are always kept, flagged `is_sponsored` |

### Category (`/category`)

Pass `category_id` or `url`, plus any search parameter except `query`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | integer or string | one of | Macy's category id: the `id=` of a macys.com `/shop/` URL, a product's `categories[].id`, or a search's `redirected_to_category.id` (`3763` is Men's Coats & Jackets) |
| `url` | string | one of | A macys.com category URL with its `id=` (`https://www.macys.com/shop/mens/clothing/coats?id=3763`). Filters, page and sort already in the URL are kept |

### Brand (`/brand`)

Pass `brand_id` or `url`, plus any search parameter except `query`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand_id` | integer or string | one of | The brand page id: a product's `brand_page_id`, or the `id=` of a macys.com `/shop/brands/` URL (`337747` is Calvin Klein, `5201` Benefit Cosmetics). A brand name alone is not enough: use search with `brand` for that |
| `url` | string | one of | A macys.com brand page URL with its `id=` |

### Deals (`/deals`)

Any search parameter except `query` and `special_offer`, plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `sale` | `sale` (all Sales & Offers), `clearance` (Clearance & Closeout), `today_only`, `last_act` (final-sale markdowns), `limited_time_special` or `black_friday` |

### Product (`/product`)

Pass exactly one of `product_id`, `url` or `product_ids`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | integer or string | one of | Macy's product id: a listing item's `id`, or the `ID=` number in a macys.com product URL (`25822310`) |
| `url` | string | one of | A macys.com product URL with `ID=` |
| `product_ids` | array or string | one of | Up to 10 product ids in one call, an array or a comma-separated string |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | integer or string | one of | Macy's product id |
| `url` | string | one of | A macys.com product URL with `ID=`, used when `product_id` is not given |
| `sort` | string | `newest` | `newest`, `highest_rated`, `lowest_rated` or `with_photos` |
| `page` | integer | 1 | Page, 1-based (1-500) |
| `limit` | integer | 20 | Reviews per page, 1-100 |
| `rating` | integer | all | Only reviews with this many stars, 1-5 |
| `query` | string | none | Only reviews mentioning this text (1-100 chars) |

### Stores (`/stores`)

Pass one location: `zip`, or `lat` with `lng`, or `city` with `state`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code (`10001` or `10001-1234`) |
| `lat`, `lng` | number | one of | A point, both required together |
| `city`, `state` | string | one of | A US city and its 2-letter state code (`Atlanta`, `GA`), both required together |
| `radius` | integer | 100 | Search radius in miles, 1-100 |

### Store availability (`/store-availability`)

Pass `product_id` or `url`, and exactly one of a location (as `/stores`, with `radius`) or `store_id`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | integer or string | one of | Macy's product id |
| `url` | string | one of | A macys.com product URL with `ID=` |
| `store_id` | integer or string | one of | One store (a `/stores` `store_id`, e.g. `4592` State Street, Chicago) for per-variant flags |
| `zip` / `lat` + `lng` / `city` + `state` | | one of | A location: which stores near it can do pickup |
| `radius` | integer | 100 | With a location: radius in miles, 1-100 |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

## Examples

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 25822310}'
```

Captured `data` (6 of 8 bullets, 1 of 2 categories, 4 of 6 images, 3 of 5 colors, 6 of 8 sizes and 58 of 60 variants trimmed; the description and review summary shortened):

```json
{
  "requested_id": 25822310,
  "id": 25822310,
  "title": "Men's Standard Straight Fit Stretch Denim Jeans",
  "full_title": "Calvin Klein Men's Standard Straight Fit Stretch Denim Jeans",
  "brand": "Calvin Klein",
  "brand_page_id": 337747,
  "brand_url": "https://www.macys.com/shop/brands/calvin-klein?id=337747",
  "type": "JEANS",
  "url": "https://www.macys.com/shop/product/calvin-klein-mens-straight-fit-stretch-denim-jeans?ID=25822310",
  "description": "Crafted from comfort-stretch denim, these Calvin Klein straight-fit jeans offer lasting flexibility and all-day comfort. ...",
  "bullets": ["Approx. inseam: 32\"", "Type of fit: straight fit"],
  "categories": [
    { "id": 11221, "name": "Jeans & Denim", "url": "https://www.macys.com/shop/mens/clothing/jeans?id=11221" }
  ],
  "price": 59.4,
  "price_max": 71.4,
  "regular_price": 99,
  "regular_price_max": 119,
  "sale_price": 59.4,
  "percent_off": 40,
  "percent_off_max": null,
  "price_label": "Sale",
  "set_value": null,
  "on_sale": true,
  "sale_ends": "2026-11-12",
  "deal_label": null,
  "currency": "USD",
  "price_valid_until": "2026-11-12",
  "promotions": [],
  "rating": 4.5,
  "review_count": 55,
  "text_review_count": 32,
  "rating_distribution": { "1": 2, "2": 2, "3": 3, "4": 7, "5": 41 },
  "recommended_count": 14,
  "not_recommended_count": 2,
  "fit": { "value": 4, "scale": 7, "label": "neutral", "min_label": "Runs Small", "max_label": "Runs Large" },
  "review_summary": "* Customers frequently praise the comfortable feel of the denim.\n* Many reviewers find the fit to be accurate and true to size.\n...",
  "purchased_message": "859 customers purchased",
  "questions_count": 0,
  "answers_count": 0,
  "available": true,
  "images": [
    "https://slimages.macysassets.com/is/image/MCY/products/7/optimized/40869767_fpx.tif",
    "https://slimages.macysassets.com/is/image/MCY/products/2/optimized/36091812_fpx.tif"
  ],
  "colors": [
    { "id": 11426969, "name": "WINTER HAZE", "normal_name": "Blue", "swatch": "https://slimages.macysassets.com/is/image/MCY/swatches/8/optimized/39126708_fpx.tif", "image": "https://slimages.macysassets.com/is/image/MCY/products/0/optimized/39142680_fpx.tif", "price": 71.4 },
    { "id": 11000904, "name": "CK Classic Black", "normal_name": "Black", "swatch": "https://slimages.macysassets.com/is/image/MCY/swatches/0/optimized/36091800_fpx.tif", "image": "https://slimages.macysassets.com/is/image/MCY/products/9/optimized/36091809_fpx.tif", "price": 65.4 }
  ],
  "sizes": ["29", "30"],
  "size_label": "Waist",
  "variant_count": 60,
  "variants": [
    { "upc": "198629836923", "variant_id": 57591604, "color": "CK Classic Black", "size": "29x30", "available": true, "availability_message": "Just a few left", "low_availability": true, "ship_days": 2, "ship_message": "Usually ships within 2 business days." },
    { "upc": "198629836978", "variant_id": 57591605, "color": "CK Classic Black", "size": "30x30", "available": true, "availability_message": "In Stock", "low_availability": false, "ship_days": 2, "ship_message": "Usually ships within 2 business days." }
  ]
}
```

Read the price block as: the jeans sell from $59.40 to $71.40 depending on color (`colors[].price`), against a regular $99 to $119, 40% off, and the sale price ends on 2026-11-12. `review_count` (55) counts every rating; `text_review_count` (32) counts the ones with written text, which is all `/reviews` can return.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jeans"}'
```

Captured `data` for `{"query": "jeans"}` (58 of 60 items, 32 of 34 facets and 2 of the Offers facet's 7 values trimmed):

```json
{
  "query": "jeans",
  "redirected_to_category": null,
  "total": 6711,
  "page": 1,
  "total_pages": 112,
  "per_page": 60,
  "sort": "featured",
  "count": 60,
  "sponsored_dropped": 2,
  "items": [
    {
      "id": 25386711,
      "title": "Women's Classic Straight Jeans",
      "brand": "Tommy Hilfiger",
      "url": "https://www.macys.com/shop/product/tommy-hilfiger-womens-classic-straight-jeans?ID=25386711",
      "image": "https://slimages.macysassets.com/is/image/MCY/products/9/optimized/39667019_fpx.tif",
      "price": 45.17,
      "price_max": 51.67,
      "regular_price": 69.5,
      "regular_price_max": 79.5,
      "sale_price": 45.17,
      "percent_off": 35,
      "percent_off_max": null,
      "price_label": "Sale",
      "set_value": null,
      "on_sale": true,
      "sale_ends": "2026-11-12",
      "deal_label": null,
      "currency": "USD",
      "rating": 4.2,
      "review_count": 72,
      "colors": ["Nos Dark Blue", "Nos Mid Blue", "Optic White"],
      "promotions": [],
      "is_sponsored": true
    },
    {
      "id": 25822310,
      "title": "Men's Standard Straight Fit Stretch Denim Jeans",
      "brand": "Calvin Klein",
      "url": "https://www.macys.com/shop/product/calvin-klein-mens-straight-fit-stretch-denim-jeans?ID=25822310",
      "image": "https://slimages.macysassets.com/is/image/MCY/products/7/optimized/40869767_fpx.tif",
      "price": 59.4,
      "price_max": 71.4,
      "regular_price": 99,
      "regular_price_max": 119,
      "sale_price": 59.4,
      "percent_off": 40,
      "percent_off_max": null,
      "price_label": "Sale",
      "set_value": null,
      "on_sale": true,
      "sale_ends": "2026-11-12",
      "deal_label": null,
      "currency": "USD",
      "rating": 4.5,
      "review_count": 55,
      "colors": ["WINTER HAZE", "Klein Blue Black", "CK Classic Rinse", "CK Classic Black", "BLEACHED CLEARWATER"],
      "promotions": [],
      "is_sponsored": false
    }
  ],
  "applied_filters": [],
  "facets": [
    {
      "name": "PRICE",
      "label": "Price",
      "values": [
        { "label": "Under $50", "count": 1839, "value": "0|49.99" },
        { "label": "$50-$100", "count": 3019, "value": "50|100" },
        { "label": "$100-$250", "count": 1597, "value": "100|250" },
        { "label": "$250-$500", "count": 217, "value": "250|500" },
        { "label": "$500 & Above", "count": 34, "value": "500|-1" }
      ]
    },
    {
      "name": "SPECIAL_OFFERS",
      "label": "Offers",
      "values": [
        { "label": "Limited-Time Special", "count": 224, "value": "Limited-Time Special" },
        { "label": "Black Friday Deal", "count": 1124, "value": "Black Friday Deal" },
        { "label": "Clearance", "count": 976, "value": "Clearance" },
        { "label": "Last Act", "count": 439, "value": "Last Act" },
        { "label": "Sales & Discounts", "count": 4319, "value": "Sales & Discounts" }
      ]
    }
  ],
  "currency": "USD"
}
```

The first item is an organic result that also holds a paid slot, so it is kept and flagged `is_sponsored: true` (6 of the 60 captured items carry the flag). `sponsored_dropped: 2` is the ad-only tiles that were left out because `include_sponsored` was not set. For a price range use `min_price` / `max_price` rather than the `PRICE` facet values.

### Category and brand

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": 3763}'
```

The captured page carries `"category": { "id": 3763, "name": "Men's Coats & Jackets", "url": "https://www.macys.com/shop/mens/clothing/coats?id=3763" }`, `total: 4703`, `total_pages: 79`, `count: 60`, `sponsored_dropped: 3` and 14 facets, then the same `items[]` as search. `/brand` with `{"brand_id": 337747}` answered `"brand": { "id": 337747, "name": "Calvin Klein", "url": "https://www.macys.com/shop/brands/calvin-klein?id=337747" }`, `total: 2083`, `total_pages: 35` and `count: 59`: a full page can hold fewer than 60 items.

A brand page item with a gift-set value (captured from `/brand`):

```json
{
  "id": 28229490,
  "title": "4-Piece Fragrance Gift Set",
  "brand": "Calvin Klein",
  "url": "https://www.macys.com/shop/product/calvin-klein-4-piece-fragrance-gift-set?ID=28229490",
  "image": "https://slimages.macysassets.com/is/image/MCY/products/9/optimized/38903209_fpx.tif",
  "price": 25,
  "price_max": null,
  "regular_price": 45,
  "regular_price_max": null,
  "sale_price": 25,
  "percent_off": 44,
  "percent_off_max": null,
  "price_label": "Only",
  "set_value": 123,
  "on_sale": true,
  "sale_ends": "2026-11-30",
  "deal_label": "Black Friday Deal",
  "currency": "USD",
  "rating": 4.6,
  "review_count": 22,
  "colors": [],
  "promotions": [],
  "is_sponsored": false
}
```

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "clearance"}'
```

The captured answer opens with `"type": "clearance"`, `"label": "Clearance & Closeout"`, `total: 23124`, `total_pages: 386`, `count: 60`, `sponsored_dropped: 4` and 44 facets. Its first item:

```json
{
  "id": 13313167,
  "title": "Men's Modern-Fit Wool TH-Flex Stretch Suit Separates Jacket",
  "brand": "Tommy Hilfiger",
  "url": "https://www.macys.com/shop/product/tommy-hilfiger-mens-modern-fit-wool-th-flex-stretch-suit-separates-jacket?ID=13313167",
  "image": "https://slimages.macysassets.com/is/image/MCY/products/8/optimized/36313488_fpx.tif",
  "price": 85,
  "price_max": null,
  "regular_price": 480,
  "regular_price_max": null,
  "sale_price": 85,
  "percent_off": 82,
  "percent_off_max": null,
  "price_label": "Sale",
  "set_value": null,
  "on_sale": true,
  "sale_ends": "2026-11-19",
  "deal_label": null,
  "currency": "USD",
  "rating": 4.2,
  "review_count": 132,
  "colors": ["Blue Sharkskin", "Light Grey", "Charcoal", "Tan", "Navy"],
  "promotions": [],
  "is_sponsored": false
}
```

On the same clearance page most items carry `deal_label` `"Clearance"` or `"LAST ACT"` and `price_label` `"Now"`, and 56 of the 60 have `sale_ends: null`. For the biggest markdowns, add `"filters": {"PRICE_DISCOUNT_RANGE": "70_PERCENT_ off & more"}` (a `values[].value` from that facet; its label reads "70% off & more").

### Store availability at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 25822310, "store_id": 4592}'
```

Captured `data` (5 of 7 store features and 58 of 60 variants trimmed):

```json
{
  "requested_id": 25822310,
  "product_id": 25822310,
  "title": "Men's Standard Straight Fit Stretch Denim Jeans",
  "brand": "Calvin Klein",
  "url": "https://www.macys.com/shop/product/calvin-klein-mens-straight-fit-stretch-denim-jeans?ID=25822310",
  "store": {
    "store_id": 4592,
    "name": "State Street",
    "address": { "line1": "111 N State St", "line2": null, "city": "Chicago", "state": "IL", "zip": "60602", "country": "US" },
    "lat": 41.883886,
    "lng": -87.626278,
    "hours": [
      { "date": "2026-11-09", "open": "10:00 AM", "close": "9:00 PM", "closed": false },
      { "date": "2026-11-10", "open": "10:00 AM", "close": "9:00 PM", "closed": false }
    ],
    "curbside_hours": [
      { "date": "2026-11-09", "open": "10:00 AM", "close": "7:00 PM", "closed": false },
      { "date": "2026-11-10", "open": "10:00 AM", "close": "7:00 PM", "closed": false }
    ],
    "pickup_cutoff": "3:00 PM",
    "pickup_day": "TODAY",
    "pickup_options": ["Curbside", "In Store"],
    "features": ["Furniture Gallery", "Visitor Services"]
  },
  "variant_count": 60,
  "pickup_available_count": 31,
  "in_store_available_count": 43,
  "variants": [
    { "upc": "198629836923", "variant_id": 57591604, "color": "CK Classic Black", "size": "29x30", "pickup_available": false, "in_store_available": false, "available_online": true },
    { "upc": "198629836978", "variant_id": 57591605, "color": "CK Classic Black", "size": "30x30", "pickup_available": true, "in_store_available": true, "available_online": true }
  ]
}
```

`pickup_available` and `in_store_available` are separate answers: 43 variants are in the store but only 31 can be ordered for pickup. Say "available for pickup at State Street" or "in the store", never a number of units.

Near a location instead (`{"product_id": 25822310, "zip": "10001"}`), the answer is `product_id`, `location`, `radius_miles`, `count`, `available_count` and `stores[]`, each store in the `/stores` shape plus `available` (true / false) and `available_items_count`.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10001"}'
```

Captured `data` (14 of 15 stores trimmed):

```json
{
  "location": { "zip": "10001" },
  "radius_miles": 100,
  "count": 15,
  "stores": [
    {
      "store_id": 10,
      "name": "Herald Square",
      "address": { "line1": "151 West 34th Street", "line2": null, "city": "New York", "state": "NY", "zip": "10001", "country": "US" },
      "phone": "212-695-4400",
      "lat": 40.751455,
      "lng": -73.9902,
      "distance_miles": 0.54,
      "hours": [
        { "date": "2026-11-09", "open": "10:00 AM", "close": "9:00 PM", "closed": false },
        { "date": "2026-11-10", "open": "10:00 AM", "close": "9:00 PM", "closed": false }
      ],
      "curbside_hours": [
        { "date": "2026-11-09", "open": null, "close": null, "closed": true },
        { "date": "2026-11-10", "open": null, "close": null, "closed": true }
      ],
      "pickup_cutoff": "4:00 PM",
      "features": []
    }
  ]
}
```

Herald Square has no curbside pickup on either day (`closed: true`), while the Jersey City store in the same answer runs curbside 10:00 AM to 8:00 PM. The 15 stores reach 16.63 miles here: the list stops at 15 well inside the 100-mile radius in a dense area.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 25822310, "limit": 10}'
```

Captured `data` (9 of 10 reviews trimmed):

```json
{
  "product_id": 25822310,
  "product_title": "Calvin Klein Men's Standard Straight Fit Stretch Denim Jeans",
  "product_url": "https://www.macys.com/shop/product/calvin-klein-mens-straight-fit-stretch-denim-jeans?ID=25822310",
  "sort": "newest",
  "rating_filter": null,
  "query": null,
  "total": 32,
  "page": 1,
  "limit": 10,
  "total_pages": 4,
  "has_more": true,
  "count": 10,
  "reviews": [
    {
      "id": 307775755,
      "rating": 5,
      "title": "Great plain pocket jeans.",
      "text": "Love the color and fit. And they feel comfortable when I move around.",
      "date": "2026-10-26",
      "nickname": "Philip",
      "location": "New Jersey",
      "recommended": true,
      "helpful_yes": 0,
      "helpful_no": 0,
      "incentivized": false,
      "syndicated": false,
      "syndicated_from": null,
      "badges": [],
      "fit": "mostly small",
      "slider_ratings": [
        { "id": "OverallSize", "label": "Runs Small/Runs Large", "value": 2, "scale": 7, "value_label": "mostly small", "min_label": "Runs Small", "max_label": "Runs Large" }
      ],
      "photos": [],
      "brand_response": null
    }
  ]
}
```

`total` (32) is the written reviews, the same as the product's `text_review_count`; the product's `review_count` (55) also counts ratings left without text, which no endpoint returns. Use `rating_distribution` on `/product` for the full histogram.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/macys/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jea"}'
```

Captured `data`:

```json
{
  "query": "jea",
  "count": 7,
  "suggestions": ["levi's women jeans", "women jeans", "jean paul gaultier", "men levi's jeans", "mens jeans", "jeans", "jean paul gaultier perfume men"]
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

def macys(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/macys/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Clearance on one brand, lowest price first (1 credit; listing calls can take up to a minute)
found = macys("deals", {"type": "clearance", "brand": "Calvin Klein", "sort": "price_low_to_high"})
for p in found["items"][:5]:
    print(p["id"], p["title"], p["price"], "regular", p["regular_price"], p["deal_label"], p["sale_ends"])

# 2. Price watch list: up to 10 products per call (1 credit)
watch = macys("product", {"product_ids": [25822310, 13313167]})
for p in watch["products"]:
    print(p["requested_id"], p["price"], p["on_sale"], p["sale_ends"], p["deal_label"])
print("not found:", watch["not_found"])

# 3. Which sizes can be picked up at a store near the user (2 calls, 1 credit each)
store = macys("stores", {"zip": "60602"})["stores"][0]
avail = macys("store-availability", {"product_id": 25822310, "store_id": store["store_id"]})
for v in avail["variants"]:
    if v["pickup_available"]:
        print(store["name"], v["color"], v["size"], "pickup by", avail["store"]["pickup_cutoff"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when Macy's answered.

- **listing item** (search, category, brand, deals) - `id`, `title`, `brand`, `url`, `image`, `price`, `price_max`, `regular_price`, `regular_price_max`, `sale_price`, `percent_off`, `percent_off_max`, `price_label`, `set_value`, `on_sale`, `sale_ends`, `deal_label`, `currency`, `rating`, `review_count`, `colors[]` (names), `promotions[]` {`id`, `title`, `description`, `type`}, `is_sponsored`.
- **search** - `query`, `redirected_to_category` ({`id`, `name`, `url`} or null), `total`, `page`, `total_pages`, `per_page` (60), `sort`, `count`, `sponsored_dropped`, `items[]`, `applied_filters[]` {`name`, `values[]`}, `facets[]` {`name`, `label`, `values[]` {`label`, `count`, `value`}}, `currency`.
- **category** - `category` {`id`, `name`, `url`} and the search fields from `total` on.
- **brand** - `brand` {`id`, `name`, `url`} and the search fields from `total` on.
- **deals** - `type`, `label` and the search fields from `total` on.
- **product** - `requested_id`, `id`, `title`, `full_title`, `brand`, `brand_page_id`, `brand_url`, `type`, `url`, `description`, `bullets[]`, `categories[]` {`id`, `name`, `url`}, the listing price fields (`price` to `currency`), `price_valid_until`, `promotions[]`, `rating`, `review_count`, `text_review_count`, `rating_distribution` ({"1".."5": count} or null), `recommended_count`, `not_recommended_count`, `fit` ({`value`, `scale`, `label`, `min_label`, `max_label`} or null), `review_summary`, `purchased_message`, `questions_count`, `answers_count`, `available`, `images[]`, `colors[]` {`id`, `name`, `normal_name`, `swatch`, `image`, `price`}, `sizes[]`, `size_label`, `variant_count`, `variants[]` {`upc`, `variant_id`, `color`, `size`, `available`, `availability_message`, `low_availability`, `ship_days`, `ship_message`}.
- **product batch** (`product_ids`) - `requested`, `count`, `not_found[]` (ids), `products[]` (each in the product shape, Macy's summary view).
- **reviews** - `product_id`, `product_title`, `product_url`, `sort`, `rating_filter`, `query`, `total`, `page`, `limit`, `total_pages`, `has_more`, `count`, `reviews[]` {`id`, `rating`, `title`, `text`, `date`, `nickname`, `location`, `recommended`, `helpful_yes`, `helpful_no`, `incentivized`, `syndicated`, `syndicated_from`, `badges[]`, `fit`, `slider_ratings[]` {`id`, `label`, `value`, `scale`, `value_label`, `min_label`, `max_label`}, `photos[]`, `brand_response`}.
- **stores** - `location` ({`zip`} or {`lat`, `lng`} or {`city`, `state`}), `radius_miles`, `count`, `stores[]` {`store_id`, `name`, `address` {`line1`, `line2`, `city`, `state`, `zip`, `country`}, `phone`, `lat`, `lng`, `distance_miles`, `hours[]` and `curbside_hours[]` {`date`, `open`, `close`, `closed`}, `pickup_cutoff`, `features[]`}.
- **store-availability near a location** - `product_id`, `location`, `radius_miles`, `count`, `available_count`, `stores[]` (the stores shape plus `available` and `available_items_count`).
- **store-availability at a store** - `requested_id`, `product_id`, `title`, `brand`, `url`, `store` {`store_id`, `name`, `address`, `lat`, `lng`, `hours[]`, `curbside_hours[]`, `pickup_cutoff`, `pickup_day`, `pickup_options[]`, `features[]`}, `variant_count`, `pickup_available_count`, `in_store_available_count`, `variants[]` {`upc`, `variant_id`, `color`, `size`, `pickup_available`, `in_store_available`, `available_online`}.
- **suggestions** - `query`, `count`, `suggestions[]` (strings).

## Guardrails

- Prices are US dollars (`currency: "USD"`): `59.4` is $59.40. This is macys.com (US) only. International prices and Bloomingdale's are not covered.
- `price` is the current price. When an item sells at a range (by color or size), `price` is the low end and `price_max` the high end; `regular_price_max` and `percent_off_max` work the same way. Quote a range as a range. On `/product`, `colors[].price` gives each color's own price.
- `percent_off` is measured against `regular_price` as Macy's states it. `sale_ends` (and `price_valid_until` on `/product`) is a date with no time; when it is null, do not say when the price ends.
- `deal_label` is the item's deal badge (`Black Friday Deal`, `Clearance`, `LAST ACT`, `Limited-Time Special`...) and `price_label` the word printed before the price (`Sale`, `Now`, `Only`, `Your Choice`); both are null on full-price items. `set_value` is the value Macy's states for a gift set, not a price.
- `promotions[]` carries Macy's promotion texts as given. A promotion can describe terms (for example "Last Act items are final sale") on an item whose `deal_label` is different; report the text, do not infer the item's deal from it.
- There are no coupon or promo codes, no price history and no Q&A text (only `questions_count` and `answers_count`). To track prices, poll `/product` with `product_ids` on a schedule and store the results yourself.
- Listings return 60 organic items per page; `count` can be below 60 on a full page (59 on the captured brand page). Ad-only tiles are dropped unless `include_sponsored: true`, and `sponsored_dropped` says how many. Organic items that also hold a paid slot are always kept and flagged `is_sponsored: true`; do not treat them as ads to skip.
- `total` changes with the sort, as it does on the site: compare totals only between calls with the same sort and filters.
- A keyword the site maps to a category (for example `handbags`) returns that category in `redirected_to_category`; the filters still apply. Pass its `id` to `/category` to browse it directly.
- Filters take facet VALUES, not labels: `filters` keys are `facets[].name` and values are `values[].value`. They differ on some facets (`PRICE_DISCOUNT_RANGE` value `"50_PERCENT_ off & more"`, label "50% off & more"). `brand` must be spelled as the `BRAND` facet value (`"Levi's"`), which can differ from the product title's spelling. Check `applied_filters[]` before claiming a list is filtered.
- `special_offer` works on search, category and brand; on `/deals` it is a 400, pick the section with `type`.
- `/product` with `product_ids` (up to 10) is Macy's summary view: `rating` and `review_count` but no `rating_distribution`, and a collection without its members' variants (ask for those one by one). Unknown ids are listed in `not_found`; the call is a 404 only when none is found.
- A collection member id (one towel size, say) answers with the collection product: `id` is the collection, `requested_id` echoes the id you asked for. Match on `requested_id` when tracking a list.
- Store availability has NO unit quantities. Near a location, `available` says whether a store can hand the product over and `available_items_count` is Macy's own item count for that store, not a number of units. At a `store_id`, `pickup_available` (can be ordered for pickup) and `in_store_available` (in the store) are per variant and can differ. Never claim a store has N units. On `/product`, `low_availability` and `availability_message` ("Just a few left") are online availability, not store stock.
- A `store_id` comes from `/stores` (or `/store-availability` near a location); the same id feeds `pickup_store_id` on the listings. `/stores` returns at most 15 stores, nearest first, within `radius` (default and maximum 100 miles). Hours cover today and tomorrow only (`hours[].date`); for later days, call again.
- Reviews are Macy's own reviews. `total` counts written reviews only; ratings left without text are counted in the product's `review_count` and `rating_distribution` but are never returned. Reviewers are shown by `nickname` (often `"anonymous"`) and an optional free-text `location`; there is no reviewer id. `has_more: true` means more pages exist; do not claim to have read every review unless it is false.
- `incentivized` and `syndicated` are Macy's flags as given; `badges[]` can repeat them (`"incentivizedReview"`).
- This API reads public product data for research, price monitoring and stock alerts. It does not add to cart, check out or reserve stock; do not present it as a purchasing bot.
- Never fabricate prices, sale dates, deal labels, availability or reviews. Only return what the API returned, with the product `url` or `id`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`; a `page` outside 1-1000 (reviews 1-500); an unknown `sort`, `special_offer` or deal `type`; `special_offer` on `/deals`; `min_price` above `max_price`; a `filters` key that is not a facet name or more than 10 facets; more than 20 values for one facet; a `product_id` that is not a number; a `url` that is not macys.com or has no `ID=` / `id=`; both `product_id` and `url` naming different products; `product_ids` together with `product_id` or `url`, or more than 10 of them; no location, half a location (`lat` without `lng`, `city` without `state`), or both a location and a `store_id`; a ZIP that is not 5 digits; `radius` outside 1-100; `limit` outside 1-100; `rating` outside 1-5).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product, category or brand page, an unknown `store_id` on `/store-availability`, or a batch where none of the ids was found. Not charged. Re-run the search for a fresh `id`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data).
- `502` or `503` means Macy's is temporarily unavailable or returned an unusable page. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.

## SDKs

```bash
pip install scavio==0.42.0
npm install scavio@0.43.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.macys.search({ query: "jeans", brand: "Levi's", sort: "price_low_to_high" });
const { data: item } = await scavio.macys.product({ product_id: found.items[0].id });
const { data: watch } = await scavio.macys.product({ product_ids: [25822310, 13313167] });
const { data: rev } = await scavio.macys.reviews({ product_id: item.id, rating: 1 });
const { data: cat } = await scavio.macys.category({ category_id: 3763 });
const { data: ck } = await scavio.macys.brand({ brand_id: item.brand_page_id });
const { data: clearance } = await scavio.macys.deals({ type: "clearance" });
const { data: near } = await scavio.macys.stores({ zip: "10001" });
const { data: pickup } = await scavio.macys.storeAvailability({ product_id: item.id, store_id: near.stores[0].store_id });
const { data: ideas } = await scavio.macys.suggestions({ query: "jea" });
```

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_macys`, `get_macys_product`, `get_macys_reviews`, `get_macys_category`, `get_macys_brand`, `get_macys_deals`, `get_macys_stores`, `get_macys_store_availability` and `get_macys_suggestions`. Macy's is opt-in: add `macys` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.40.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,macys"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/macys-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [product](https://scavio.dev/docs/macys-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [reviews](https://scavio.dev/docs/macys-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [category](https://scavio.dev/docs/macys-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [brand](https://scavio.dev/docs/macys-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [deals](https://scavio.dev/docs/macys-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [stores](https://scavio.dev/docs/macys-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [store availability](https://scavio.dev/docs/macys-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data), [suggestions](https://scavio.dev/docs/macys-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data). Overview: [Macy's API](https://scavio.dev/macys-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=macys-product-data).
