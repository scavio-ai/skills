---
name: saks-fifth-avenue-api
description: "Saks Fifth Avenue API: search saksfifthavenue.com, browse any category, a designer's page or the Sale, Women's Clothing Sale, Men's Sale and New Arrivals lists, 24 grid positions per page with price, regular and sale price, percent off, badge, final-sale, clearance and returnable flags, promotions and colors, filtered by designer, color, size, any price range, on sale, new arrivals or any facet, for designer sale tracking and Saks price alerts; read one product with every color and size, per-SKU online units, restock date and the average rating (review text is not available), check a variant's stock at the Saks stores near a ZIP with the store's unit count where the site shows it, find stores, pull search suggestions and the full A-Z designer index of about 1,200 designers. 9 endpoints, 2 credits each. Saks publishes no public developer or catalog API."
version: 1.0.0
tags: saks, saks-api, saks-fifth-avenue, saks-fifth-avenue-api, saks-scraper, saks-price-tracker, saks-designer-sale, saks-sale, saks-sale-alerts, saks-black-friday, saks-new-arrivals, saks-in-stock, saks-store-pickup, store-availability, store-locator, designer-sale, designer-price-tracker, designer-directory, luxury-fashion, designer-fashion, department-store, luxury, fashion, apparel, shoes, handbags, beauty, variant-data, inventory, product-search, product-data, category-browse, brand-catalog, autocomplete, retail, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/saks-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api
---

# Saks Fifth Avenue API - Designer Sale Prices, Stock, Stores

Search Saks Fifth Avenue (saksfifthavenue.com, US, prices in USD) by keyword, or browse a category by its `/c/` path or URL, one designer's page by slug, or one of the Sale and New Arrivals lists (all Sale, Women's Clothing Sale, Men's Sale, Women's New Arrivals, Men's New Arrivals), 24 grid positions per page, sorted by featured, best sellers, newest, price, sale first or designer A-Z, filtered by designer, color, size, any price range (not only the site's price buckets), on sale, new arrivals, or any other facet the response lists (department, type, gender, material, length, neckline...): product id, title, brand, URL, image, current price (and the top of the range when an item sells at a range), regular price, sale price, percent off, on-sale flag, review count, badge (`Best Seller`...), final-sale, clearance and returnable flags, limited-inventory flag, promotions and colors, plus the total, total pages, `start` / `next_start` offsets, the facets with counts and the price ranges. Read one product by id or URL with its type (master or variant), UPC (for a variant), the price block, new / sale / clearance / final-sale flags, badge, returnable, promotions, description, style code, images, every color and size with its availability, every SKU with its online warehouse unit count, in-stock and available counts, availability with the restock date, store availability, marketplace, drop-ship and preorder flags, merchandising attributes, the average star rating and the review count; add a color and a size to resolve one variant. Check one variant's stock at the Saks pickup stores near a ZIP or a point, with Saks' own unit count for a store when the site gives one. Find Saks stores near a ZIP or a point, pull the search box's suggestions and the full A-Z designer index (about 1,200 designers). All endpoints return structured JSON, 2 credits each.

See also: for Macy's sale, clearance and store pickup use the `macys-product-data` skill; for Nordstrom (per-size stock and reviews) use `nordstrom-product-data`; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Track a Saks designer sale: list the Sale, Women's Clothing Sale or Men's Sale pages for one designer, sorted by price, and detect new markdowns between runs
- Build a Saks price tracker or sale alert: poll a list of products and detect a price drop, a new sale price or an item going final sale
- Find designer clothing, shoes, handbags, jewelry or beauty at Saks by keyword and compare prices, percent off and designers
- Browse a Saks category (women's dresses, men's sweaters...) or a designer's whole Saks catalog (Gucci, Prada, ALICE + OLIVIA...) with prices
- Check which sizes and colors of a Saks item are in stock online, how many units Saks shows per SKU, and when a sold-out item restocks
- Check whether a Saks item in one color and size is in stock at a Saks store near a ZIP code
- Find Saks Fifth Avenue stores near a ZIP code with today's hours and whether they offer pickup
- List every designer Saks carries, or every designer under one letter
- Get Saks search suggestions (designers, categories, featured products, popular searches) for keyword research
- Watch the Saks new arrivals for one designer or category

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 2 credits, so the free credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Product, stores, store availability and suggestions usually answer in 1-3 seconds. The listing endpoints (search, category, brand, deals) and designers read large pages: the captured calls took 5 to 9 seconds and a slow page can take more than 20, so allow a client timeout of at least 90 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/saks/search` | 2 | 24 grid positions per page: id, variant id, title, brand, URL, image, price, price max, regular price, regular price max, sale price, on-sale flag, percent off, currency, review count, badge, `is_final_sale`, `is_clearance`, `returnable`, `limited_inventory`, promotions, product type, colors. Plus `redirected_to`, total, page, total pages, per page, `start`, `next_start`, sort, count, `applied_filters`, `facets[]` with values and counts, `price_ranges[]` |
| `POST /api/v1/saks/category` | 2 | One category by `/c/` `path` or URL, the same grid as search, plus the category's name, path, URL and breadcrumbs |
| `POST /api/v1/saks/brand` | 2 | One designer's page by slug (from `/designers`) or URL, the same grid as search, plus the brand's name, slug and URL |
| `POST /api/v1/saks/deals` | 2 | A list by `type` (`sale`, `womens_sale`, `mens_sale`, `womens_new_arrivals`, `mens_new_arrivals`), the same grid as search plus the list's label. There is no clearance or final-sale list |
| `POST /api/v1/saks/product` | 2 | One product by id (master or variant) or URL: type, master id, title, brand, UPC, URL, the price block, `is_new`, `is_sale`, `is_clearance`, `is_final_sale`, badge, returnable, promotions, description, style code, images, selected color and size, colors and sizes (each with availability, selectable, waitlist), other options, every SKU with `warehouse_units`, in-stock and available counts, availability (units available to sell, message, restock date), available in store, marketplace, drop ship, preorder, purchase limit, attributes, rating, review count. Add `color` + `size` for one variant |
| `POST /api/v1/saks/stores` | 2 | Saks stores near a ZIP or a lat/lng point within 15, 30, 50, 100 or 300 miles (default 50): store id, name, address, city, state, ZIP, lat, lng, distance in miles, today's opening and closing time, hours as listed, closed flag and `pickup` (true for stores that offer in-store pickup) |
| `POST /api/v1/saks/store-availability` | 2 | One variant `sku` at the pickup stores near a ZIP or a point: per store the availability message (`In Stock`, `Limited Inventory`, `Not Available`), `in_stock`, `limited` and `units_at_store` when the site gives a count, plus the store fields |
| `POST /api/v1/saks/suggestions` | 2 | The search box's suggestions for a partial term: the result count, matching designers, suggested categories (name, parent, path), up to 5 featured products and the site's popular searches |
| `POST /api/v1/saks/designers` | 2 | The A-Z designer index, about 1,200 designers: name, slug (what `/brand` takes), URL and letter, optionally one letter only |

## Workflow

1. **Find products:** call `/saks/search` with `query`, `/saks/category` with a `path`, `/saks/brand` with a designer `brand` slug, or `/saks/deals` with a `type`. Each item has an `id` and a `url`.
2. **Narrow the listing:** pass `brand` (search, category and deals), `color`, `size`, `min_price` / `max_price`, `on_sale`, `new_arrivals`, or any other facet through `filters` as `{"<facets[].id>": "<values[].value>"}`. A value that matches nothing returns an empty page, not an error: check `total` and the `selected` flags in `facets[]`.
3. **Page through:** pass the previous answer's `next_start` as `start` until `next_start` is null. `page` works too, but a page can carry fewer than 24 products, so offsets of 24 can skip items.
4. **Find a designer:** call `/saks/designers` (optionally with `letter`) and pass a `slug` to `/saks/brand`. To filter a search or a sale list by designer instead, use the `brand` facet value (`"ALICE + OLIVIA"`), not the slug.
5. **One product in full:** call `/saks/product` with the item's `id` as `product_id` (or its `url`). Read `colors[]` and `sizes[]` for availability, `variants[]` for every SKU and its online units, and `rating` / `review_count`.
6. **One variant:** call `/saks/product` again with `color` (a `colors[].value`) and `size` (a `sizes[].value`). The answer is the variant: its `id` is the variant sku, with its `upc` and stock.
7. **Store stock:** call `/saks/store-availability` with that variant `sku` and the user's `zip` (or `lat` + `lng`). Use `/saks/stores` for the store list with hours and the `pickup` flag.
8. **Designer sale tracking:** call `/saks/deals` with `type: "sale"` (or `womens_sale` / `mens_sale`), `brand` and `sort: "price_low_to_high"`, walk `next_start`, and store `id`, `price`, `regular_price`, `percent_off` per run. Compare runs yourself: there is no price history.
9. **Keyword research:** `/saks/suggestions` with a partial term returns designers, categories (whose `path` feeds `/category`), featured products and popular searches.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-500). 24 grid positions per page |
| `start` | integer | 0 | Item offset instead of `page` (0-12000): pass a previous answer's `next_start`. Send `page` or `start`, not both |
| `sort` | string | `featured` | `featured` (the site's own order), `best_sellers`, `newest`, `price_high_to_low`, `price_low_to_high`, `sale_first` or `brand_az` |
| `brand` | string or array | none | Designers as the `brand` facet spells them (`"Prada"`, `"ALICE + OLIVIA"`). A list (up to 20) matches any of them |
| `color` | string or array | none | Colors as the `colorRefinement` facet lists them (`Black`, `Blue`, `Red`...). A list matches any of them |
| `size` | string or array | none | Sizes as the `sizeRefinement` facet LABEL lists them (`"Medium"`, `"X-Small"`, `"4"`). `"M"` matches nothing. A list matches any of them |
| `min_price` | number | none | Minimum price in USD. Any bound works, not only the site's price ranges |
| `max_price` | number | none | Maximum price in USD. Either bound can be sent alone |
| `on_sale` | boolean | `false` | Only items on sale (the `isSale` facet) |
| `new_arrivals` | boolean | `false` | Only new arrivals (the `isNew` facet) |
| `filters` | object | none | Any other facet from a previous answer: `facets[].id` to one value or a list of `values[].value` (up to 10 facets), e.g. `{"refGender": "Women's", "refMaterial": "Cashmere"}`. Price goes in `min_price` / `max_price`, not here |

### Category (`/category`)

Pass `path` or `url` (not both), plus any search parameter except `query`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | one of | A Saks category path (`/c/women-s-apparel/dresses`): from a category URL, a suggestions `categories[].path` or a search's `redirected_to.path` |
| `url` | string | one of | A saksfifthavenue.com category URL. Filters, sort and page already in the URL are kept |

### Brand (`/brand`)

Pass `brand` or `url` (not both), plus any search parameter except `query` and `brand` filters.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | one of | A designer slug from `/designers` (`gucci`, `chloé`, `alice-olivia`). A plain name is slugified; when that is not a Saks slug the call is a 404, so use the slug |
| `url` | string | one of | A saksfifthavenue.com `/brand/` URL. Filters, sort and page already in the URL are kept |

### Deals (`/deals`)

Any search parameter except `query`, plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `sale` | `sale` (all Sale), `womens_sale` (Women's Clothing Sale), `mens_sale`, `womens_new_arrivals` or `mens_new_arrivals`. Saks lists no clearance or final-sale page |

### Product (`/product`)

Pass `product_id` or `url`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string or integer | one of | Saks product id: a listing item's `id` (the number at the end of a product URL, `"0400019127312"`), or a variant sku. Send it as a string: ids start with `0` |
| `url` | string | one of | A saksfifthavenue.com product URL ending in `-<id>.html`. A color or size the link selects is kept |
| `color` | string | none | One color, a `colors[].value` (`"BLUE OPAL"`) |
| `size` | string | none | One size, a `sizes[].value` (`"4"`). With `color`, the answer is that variant |

### Stores (`/stores`)

Pass `zip`, or `lat` with `lng` (not both).

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code (`10022` or `10022-1234`) |
| `lat`, `lng` | number | one of | A point, both required together |
| `radius` | integer | 50 | Radius in miles: `15`, `30`, `50`, `100` or `300` |

### Store availability (`/store-availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | required | A variant sku (`"10781654"`): a product's `variants[].sku`, or a product's `id` after a `color` + `size` pick. A master product id is not a sku |
| `zip` / `lat` + `lng` | | required | The location, as `/stores` |
| `radius` | integer | 50 | `15`, `30`, `50`, `100` or `300` miles |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars) |

### Designers (`/designers`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `letter` | string | all | Only designers under this letter: `A`-`Z`, or `#` for names starting with a digit |

## Examples

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "0400019127312"}'
```

Captured `data` (the description shortened; 4 of 6 colors, 7 of 10 sizes, 57 of 60 variants and 8 of 14 attribute keys trimmed):

```json
{
  "requested_id": "0400019127312",
  "id": "0400019127312",
  "master_id": "0400019127312",
  "type": "master",
  "title": "Mariah Jacquard Textured Gown",
  "brand": "Kay Unger",
  "upc": null,
  "url": "https://www.saksfifthavenue.com/product/kay-unger-mariah-jacquard-textured-gown-0400019127312.html",
  "price": 348,
  "price_max": null,
  "regular_price": 348,
  "regular_price_max": null,
  "sale_price": null,
  "on_sale": false,
  "percent_off": null,
  "currency": "USD",
  "is_new": false,
  "is_sale": false,
  "is_clearance": false,
  "is_final_sale": false,
  "badge": "BEST SELLER",
  "returnable": true,
  "promotions": [
    { "id": "29149600", "name": "Gift Card Event", "message": "Earn a $50-$500 Gift Card with Code NOVGC" }
  ],
  "description": "Kay Unger's Mariah gown spotlights a tonal textured jacquard design and pleated A-line skirt. ...",
  "style_code": "0400019127312",
  "images": [
    "https://cdn.saksfifthavenue.com/is/image/saks/0400019127312?wid=968&hei=1292&qlt=90&resMode=sharp2&op_usm=0.9,1.0,8,0"
  ],
  "selected": { "color": null, "size": null },
  "colors": [
    { "value": "BLUE OPAL", "label": "BLUE OPAL", "selected": false, "selectable": true, "availability": "IN_STOCK", "waitlist": true, "image": "https://cdn.saksfifthavenue.com/is/image/saks/0400019127312_BLUEOPAL?wid=510&hei=680&qlt=70&resMode=sharp2&op_usm=1.2,1,6,0" },
    { "value": "CHOCOLATE", "label": "CHOCOLATE", "selected": false, "selectable": true, "availability": "IN_STOCK", "waitlist": true, "image": "https://cdn.saksfifthavenue.com/is/image/saks/0400019127312_CHOCOLATE?wid=510&hei=680&qlt=70&resMode=sharp2&op_usm=1.2,1,6,0" }
  ],
  "sizes": [
    { "value": "0", "label": "0", "selected": false, "selectable": true, "availability": "IN_STOCK", "waitlist": true },
    { "value": "2", "label": "2", "selected": false, "selectable": true, "availability": "IN_STOCK", "waitlist": true },
    { "value": "4", "label": "4", "selected": false, "selectable": true, "availability": "IN_STOCK", "waitlist": true }
  ],
  "options": [],
  "variant_count": 60,
  "variants": [
    { "sku": "20789682", "warehouse_units": 11 },
    { "sku": "20900907", "warehouse_units": 46 },
    { "sku": "22834800", "warehouse_units": 0 }
  ],
  "in_stock_count": 39,
  "available_count": 44,
  "available": true,
  "ready_to_order": false,
  "availability": { "ats": 0, "message": null, "in_stock_date": null },
  "available_in_store": true,
  "marketplace": false,
  "drop_ship": true,
  "preorder": false,
  "purchase_limit": null,
  "attributes": {
    "signature_required": false,
    "gift_wrap_eligible": false,
    "country_of_origin": "CN",
    "published_date": "2026-08-28",
    "category": ["Women's Apparel"],
    "type": ["Dresses"]
  },
  "rating": 5,
  "review_count": 1
}
```

This is the master: `type: "master"`, no `upc`, and `ready_to_order: false` until a color and a size are picked. `variants[]` lists all 60 SKUs with Saks' online warehouse units each (0 to 46 here), but not which color and size each SKU is: to get one variant, call again with `"color": "BLUE OPAL", "size": "4"`, and read the variant's `id` (its sku), `upc` and `availability`. `availability.ats` read 0 on this master while 39 SKUs were in stock, so read it on a variant, not on a master. `rating` (5) and `review_count` (1) are all Saks gives about reviews: review text is not available.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "coat"}'
```

Captured `data` for `{"query": "coat"}` (22 of 24 items, 6 of 8 facets, 79 of the size facet's 82 values and 6 of 8 price ranges trimmed):

```json
{
  "query": "coat",
  "redirected_to": null,
  "total": 2328,
  "page": 1,
  "total_pages": 97,
  "per_page": 24,
  "start": 0,
  "next_start": 24,
  "sort": "featured",
  "count": 24,
  "items": [
    {
      "id": "0400027024616",
      "variant_id": null,
      "title": "Maire Puffer Jacket",
      "brand": "Moncler",
      "url": "https://www.saksfifthavenue.com/product/moncler-maire-puffer-jacket-0400027024616.html",
      "image": "https://cdn.saksfifthavenue.com/is/image/saks/0400027024616_BLACK?wid=380&hei=506&qlt=70&resMode=sharp2&op_usm=1.2,1,6,0",
      "price": 2040,
      "price_max": null,
      "regular_price": 2040,
      "regular_price_max": null,
      "sale_price": null,
      "on_sale": false,
      "percent_off": null,
      "currency": "USD",
      "review_count": null,
      "badge": null,
      "is_final_sale": null,
      "is_clearance": false,
      "returnable": true,
      "limited_inventory": false,
      "promotions": ["Earn a $50-$500 Gift Card with Code NOVGC"],
      "product_type": "master",
      "colors": ["BLACK", "OFF WHITE"]
    },
    {
      "id": "0400017320514",
      "variant_id": null,
      "title": "Freestyle Down Puffer Jacket",
      "brand": "SAM.",
      "url": "https://www.saksfifthavenue.com/product/sam.-freestyle-down-puffer-jacket-0400017320514.html",
      "image": "https://cdn.saksfifthavenue.com/is/image/saks/0400017320514_JET?wid=380&hei=506&qlt=70&resMode=sharp2&op_usm=1.2,1,6,0",
      "price": 213.74,
      "price_max": 395,
      "regular_price": 395,
      "regular_price_max": 475,
      "sale_price": 213.74,
      "on_sale": true,
      "percent_off": 46,
      "currency": "USD",
      "review_count": 10,
      "badge": "Best Seller",
      "is_final_sale": null,
      "is_clearance": false,
      "returnable": true,
      "limited_inventory": false,
      "promotions": ["Earn a $50-$500 Gift Card with Code NOVGC"],
      "product_type": "master",
      "colors": ["JET", "DARK MARINE", "COTTON CANDY"]
    }
  ],
  "applied_filters": {},
  "facets": [
    {
      "id": "sizeRefinement",
      "label": "Size",
      "values": [
        { "label": "Medium", "value": "Medium", "count": 941, "selected": false },
        { "label": "Small", "value": "Small", "count": 932, "selected": false },
        { "label": "Large", "value": "Large", "count": 898, "selected": false }
      ]
    },
    {
      "id": "isSale",
      "label": "Sale",
      "values": [
        { "label": "Sale", "value": "Sale", "count": 371, "selected": false },
        { "label": "Not Sale", "value": "Not Sale", "count": 1929, "selected": false }
      ]
    }
  ],
  "price_ranges": [
    { "label": "$500 - $1000", "min_price": 500, "max_price": 1000, "selected": false },
    { "label": "$1000 - $2000", "min_price": 1000, "max_price": 2000, "selected": false }
  ],
  "currency": "USD"
}
```

The SAM. jacket sells from $213.74 to $395 across its colors and sizes against a regular $395 to $475: quote it as a range. Listing items carry `review_count` but never a rating (the product endpoint adds the average). The other facets on this answer were `refCategory` (Department), `brand` (Designer, 218 values), `colorRefinement`, `refinementProductType` (Type), `isNew` and `refGender`. A `price_ranges[]` entry's `min_price` and `max_price` feed the same-named parameters.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/c/women-s-apparel/dresses"}'
```

The captured page opens with:

```json
{
  "category": {
    "name": "Women’s Designer Dresses",
    "path": "/c/women-s-apparel/dresses",
    "url": "https://www.saksfifthavenue.com/c/women-s-apparel/dresses",
    "breadcrumbs": ["Women's Clothing", "Dresses"]
  },
  "total": 11341,
  "page": 1,
  "total_pages": 473,
  "per_page": 24,
  "start": 0,
  "next_start": 22,
  "sort": "featured",
  "count": 22
}
```

then 22 items in the search shape and 12 facets (`brand` with 331 designers, `sizeRefinement`, `colorRefinement`, `refLength`, `refSleeveLength`, `refNeckline`, `refinementStyle`, `refMaterial`, `isSale`, `isNew`, `refLifestyle`, `featuredType`). Editorial tiles took 2 of the 24 grid positions, so the page holds 22 products and `next_start` is 22, not 24: walk the list with `start: next_start`, or page 2 would skip two dresses.

### Brand and designers

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/designers \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (1,193 of 1,196 designers trimmed, three kept from different letters):

```json
{
  "letter": null,
  "total": 1196,
  "count": 1196,
  "designers": [
    { "name": "A.L.C.", "slug": "a.l.c.", "url": "https://www.saksfifthavenue.com/brand/a.l.c.", "letter": "A" },
    { "name": "ALICE + OLIVIA", "slug": "alice-olivia", "url": "https://www.saksfifthavenue.com/brand/alice-olivia", "letter": "A" },
    { "name": "Chloé", "slug": "chloé", "url": "https://www.saksfifthavenue.com/brand/chlo%C3%A9", "letter": "C" }
  ]
}
```

Pass a `slug` exactly as given (dots and accents included) to `/brand`. `/brand` with `{"brand": "gucci"}` answered `"brand": { "name": "Gucci", "slug": "gucci", "url": "https://www.saksfifthavenue.com/brand/gucci" }`, `total: 682`, `total_pages: 29`, `count: 24`, `next_start: 24` and 7 facets, then the same `items[]` as search.

### Deals (designer sale)

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "sale"}'
```

The captured answer opens with `"type": "sale"`, `"label": "Sale"`, `total: 15390`, `total_pages: 642`, `count: 24`, `next_start: 24` and 7 facets. One of its items:

```json
{
  "id": "0400018925848",
  "variant_id": null,
  "title": "MA-1 Low-Top Sneakers",
  "brand": "Amiri",
  "url": "https://www.saksfifthavenue.com/product/amiri-ma-1-low-top-sneakers-0400018925848.html",
  "image": "https://cdn.saksfifthavenue.com/is/image/saks/0400018925848_BLACKWHITE?wid=380&hei=506&qlt=70&resMode=sharp2&op_usm=1.2,1,6,0",
  "price": 510,
  "price_max": 850,
  "regular_price": 850,
  "regular_price_max": null,
  "sale_price": 510,
  "on_sale": true,
  "percent_off": 40,
  "currency": "USD",
  "review_count": null,
  "badge": "BEST SELLER",
  "is_final_sale": null,
  "is_clearance": false,
  "returnable": true,
  "limited_inventory": false,
  "promotions": ["Earn a $50-$500 Gift Card with Code NOVGC"],
  "product_type": "master",
  "colors": ["BLACK WHITE", "ALABASTER", "BLACK", "WHITE BLACK"]
}
```

`price_max` (850) equals `regular_price` here: some colors or sizes are marked down to $510 and others still sell at full price, so "40% off" applies to the low end only. Open the product with a `color` + `size` before quoting one variant's sale price. For one designer's sale, add `"brand": "Amiri"` (the `brand` facet value) and `"sort": "price_low_to_high"`.

### Store availability

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "10781654", "zip": "10022"}'
```

Captured `data` (one of the two stores trimmed):

```json
{
  "sku": "10781654",
  "location": { "zip": "10022" },
  "radius_miles": 50,
  "count": 2,
  "in_stock_count": 2,
  "stores": [
    {
      "store_id": "8601",
      "name": "New York",
      "address": "611 Fifth Avenue",
      "city": "New York",
      "state": "NY",
      "zip": "10022-6899",
      "country": "US",
      "lat": 40.756416,
      "lng": -73.970295,
      "distance_miles": 0.21,
      "open_today": "11:00AM",
      "close_today": "7:00PM",
      "hours": "9AM - 6PM",
      "closed": false,
      "pickup": true,
      "availability_message": "In Stock",
      "in_stock": true,
      "limited": false,
      "units_at_store": 141
    }
  ]
}
```

The other store, Greenwich (26.08 miles), answered `In Stock` with `units_at_store: 15`. Only pickup stores are listed (2 of the 4 Saks locations `/stores` returns for the same ZIP). `units_at_store` is Saks' own figure for that store as the site gives it; when it is null, say "in stock" or "limited", never a number.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10022"}'
```

Captured `data` (2 of 4 stores trimmed):

```json
{
  "location": { "zip": "10022" },
  "radius_miles": 50,
  "count": 4,
  "pickup_count": 2,
  "stores": [
    {
      "store_id": "8601",
      "name": "New York",
      "address": "611 Fifth Avenue",
      "city": "New York",
      "state": "NY",
      "zip": "10022-6899",
      "country": "US",
      "lat": 40.756416,
      "lng": -73.970295,
      "distance_miles": 0.21,
      "open_today": "11:00AM",
      "close_today": "7:00PM",
      "hours": "9AM - 6PM",
      "closed": false,
      "pickup": true
    },
    {
      "store_id": "8681",
      "name": "New Jersey",
      "address": "1 American Dream Way Suite F140",
      "city": "East Rutherford",
      "state": "NJ",
      "zip": "07073",
      "country": "US",
      "lat": 40.8091,
      "lng": -74.0698,
      "distance_miles": null,
      "open_today": "11:00AM",
      "close_today": "7:00PM",
      "hours": null,
      "closed": null,
      "pickup": false
    }
  ]
}
```

Stores with `pickup: false` are the other Saks locations on the site's map: they come without a distance, a listed-hours line or a closed flag. For today's hours use `open_today` and `close_today`; `hours` is a separate line as the site lists it and can differ from them (New York above).

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/saks/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "gucci"}'
```

Captured `data` (4 of 5 products trimmed):

```json
{
  "query": "gucci",
  "result_count": 682,
  "designers": ["Gucci"],
  "categories": [],
  "products": [
    {
      "id": "0400021245588",
      "title": "Jordaan Horsebit Leather Loafers",
      "brand": "Gucci",
      "url": "https://www.saksfifthavenue.com/product/gucci-jordaan-horsebit-leather-loafers-0400021245588.html",
      "image": "https://cdn.saksfifthavenue.com/is/image/saks/0400021245588?wid=380&hei=506&qlt=70&resMode=sharp2&op_usm=1.2,1,6,0"
    }
  ],
  "popular_searches": ["prada", "ralph lauren", "balenciaga", "coach", "burberry"]
}
```

`designers[]` are display names, not slugs: look the slug up in `/designers` before calling `/brand`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def saks(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/saks/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. One designer's sale, lowest price first, every page (2 credits per page)
items, start = [], 0
while start is not None and len(items) < 96:
    page = saks("deals", {"type": "sale", "brand": "Amiri", "sort": "price_low_to_high", "start": start})
    items += page["items"]
    start = page["next_start"]
for p in items[:5]:
    print(p["id"], p["title"], p["price"], "regular", p["regular_price"], p["percent_off"], p["is_final_sale"])

# 2. One variant of a product, then its stock at stores near the user (2 calls, 2 credits each)
variant = saks("product", {"product_id": "0400019127312", "color": "BLUE OPAL", "size": "4"})
near = saks("store-availability", {"sku": variant["id"], "zip": "10022"})
for s in near["stores"]:
    units = s["units_at_store"]
    print(s["name"], s["availability_message"], f"{units} units" if units is not None else "")
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached except the designer index, which can be up to 12 hours old; `fetched_at` is when the answer was produced.

- **listing item** (search, category, brand, deals) - `id`, `variant_id` (when the tile shows one variant, else null), `title`, `brand`, `url`, `image`, `price`, `price_max`, `regular_price`, `regular_price_max`, `sale_price`, `on_sale`, `percent_off`, `currency`, `review_count`, `badge`, `is_final_sale`, `is_clearance`, `returnable`, `limited_inventory`, `promotions[]` (strings), `product_type`, `colors[]` (names).
- **search** - `query`, `redirected_to` ({`type`: `category`, `brand` or `page`, `path`} or null), `total`, `page`, `total_pages`, `per_page` (24), `start`, `next_start`, `sort`, `count`, `items[]`, `applied_filters` (the facet ids and values you sent, plus `min_price` / `max_price`), `facets[]` {`id`, `label`, `values[]` {`label`, `value`, `count`, `selected`}}, `price_ranges[]` {`label`, `min_price`, `max_price`, `selected`}, `currency`.
- **category** - `category` {`name`, `path`, `url`, `breadcrumbs[]`} and the search fields from `total` on.
- **brand** - `brand` {`name`, `slug`, `url`} and the search fields from `total` on.
- **deals** - `type`, `label` and the search fields from `total` on.
- **product** - `requested_id`, `id`, `master_id`, `type` (`master` or `variant`), `title`, `brand`, `upc`, `url`, the price fields (`price` to `currency`), `is_new`, `is_sale`, `is_clearance`, `is_final_sale`, `badge`, `returnable`, `promotions[]` {`id`, `name`, `message`}, `description`, `style_code`, `images[]`, `selected` {`color`, `size`}, `colors[]` {`value`, `label`, `selected`, `selectable`, `availability`, `waitlist`, `image`}, `sizes[]` {`value`, `label`, `selected`, `selectable`, `availability`, `waitlist`}, `options[]` {`id`, `name`, `values[]`}, `variant_count`, `variants[]` {`sku`, `warehouse_units`}, `in_stock_count`, `available_count`, `available`, `ready_to_order`, `availability` {`ats`, `message`, `in_stock_date`}, `available_in_store`, `marketplace`, `drop_ship`, `preorder`, `purchase_limit`, `attributes` (object), `rating`, `review_count`.
- **stores** - `location` ({`zip`} or {`lat`, `lng`}), `radius_miles`, `count`, `pickup_count`, `stores[]` {`store_id`, `name`, `address`, `city`, `state`, `zip`, `country`, `lat`, `lng`, `distance_miles`, `open_today`, `close_today`, `hours`, `closed`, `pickup`}.
- **store-availability** - `sku`, `location`, `radius_miles`, `count`, `in_stock_count`, `stores[]` (the store fields plus `availability_message`, `in_stock`, `limited`, `units_at_store`).
- **suggestions** - `query`, `result_count`, `designers[]` (names), `categories[]` {`name`, `parent`, `path`}, `products[]` {`id`, `title`, `brand`, `url`, `image`}, `popular_searches[]`.
- **designers** - `letter`, `total` (the whole index), `count` (after the letter filter), `designers[]` {`name`, `slug`, `url`, `letter`}.

## Guardrails

- Prices are US dollars (`currency: "USD"`): `213.74` is $213.74. This is saksfifthavenue.com (US) only. International prices are not covered, and neither is Saks OFF 5TH: the saksoff5th.com site has shut down.
- `price` is the current price. When an item sells at a range (by color or size), `price` is the low end and `price_max` the high end; `regular_price_max` works the same way. Quote a range as a range. `percent_off` compares the low end of `price` with the low end of `regular_price`, so on a range item it is not every variant's discount (`price_max` equal to `regular_price` means some variants are at full price). For one variant's price, call `/product` with `color` + `size`.
- On full-price items `regular_price` equals `price` and `sale_price` and `percent_off` are null.
- Reviews: listing items carry `review_count` only; `/product` adds the average `rating` (null when there are no reviews). Review text is not available from any endpoint, so never summarize or quote what reviewers say.
- There is no clearance or final-sale list: `/deals` covers Sale, Women's Clothing Sale, Men's Sale and the two New Arrivals lists. Items carry `is_clearance` and `is_final_sale` flags instead. On listings `is_final_sale` is often null (the tile leaves it blank); `/product` is authoritative for `is_final_sale` and `returnable`.
- There are no coupons, no price history and no Q&A. `promotions[]` carries Saks' promotion texts as given (for example a gift-card event with its code); report them as text, do not apply them to the price. To track prices, poll the listings or `/product` on a schedule and store the results yourself.
- A page has 24 grid positions, but editorial tiles can take some on category and sale pages, so `count` can be 22 or 23 on a full page. Always walk with `start: next_start`; `next_start` is null on the last page. `total_pages` is `total` / 24 rounded up.
- `total` changes with the sort and filters, as it does on the site: compare totals only between calls with the same sort and filters.
- A keyword the site maps to a designer or category page returns that page's grid with `redirected_to` naming it (`type` and `path`); a `category` path feeds `/category`. Say the results come from that page.
- Filters take facet VALUES: `filters` keys are `facets[].id` and values are `values[].value`. `size` must be the size facet's label (`"Medium"`; `"M"` matches nothing). A value that matches nothing is not an error: the answer is a 200 with `total: 0`. `applied_filters` echoes what you sent, not what matched: check `total` and the `selected` flags in `facets[]` before claiming a list is filtered.
- Two designer spellings: the `brand` filter (search, category, deals) takes the `brand` facet value (`"ALICE + OLIVIA"`); `/brand` takes a slug from `/designers` (`alice-olivia`). A `brand` filter on `/brand` is a 400.
- Badges come in the site's own casing (`"Best Seller"` and `"BEST SELLER"` both appear): compare them case-insensitively.
- Product ids are digit strings that start with `0` (`"0400019127312"`): send and store them as strings. A variant sku (`"10781654"`) is a different id from the master.
- `variants[]` on a master gives each SKU's `warehouse_units` (Saks' online warehouse units) but no color or size. To know which SKU is which color and size, call `/product` with `color` + `size`; that answer's `id` is the variant sku. `colors[].availability` and `sizes[].availability` (`IN_STOCK`, `NOT_AVAILABLE`) are online availability, not store stock.
- `availability.ats` is the units available to sell and `availability.in_stock_date` the restock date when Saks gives one; read both on a variant. Never present `warehouse_units` or `ats` as store stock.
- `/store-availability` needs a variant sku, never a master id. It lists only the pickup stores near the location. `units_at_store` is Saks' own count for that store when the site gives one, and null otherwise: then report `availability_message` (`In Stock`, `Limited Inventory`) and never a number.
- `/stores` lists pickup stores (`pickup: true`, with a distance) and the other Saks locations on the site's map (`pickup: false`, `distance_miles`, `hours` and `closed` null). `radius` accepts only 15, 30, 50, 100 or 300.
- `marketplace` and `drop_ship` are Saks' own flags on the product. Report them as given; do not infer the seller or where an order ships from beyond them.
- Saks publishes no public developer or catalog API (marketplace sellers connect through Mirakl, publishers through affiliate networks). This API reads public product data for research, price monitoring and stock alerts. It does not add to cart, check out or reserve stock; do not present it as a purchasing bot.
- Never fabricate prices, sale status, stock, unit counts, ratings or reviews. Only return what the API returned, with the product `url` or `id`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`; `page` outside 1-500 or `start` outside 0-12000, or both sent; an unknown `sort` or deal `type`; a `filters` key that is not a facet id, `price` in `filters`, more than 10 facets or more than 20 values for one; `min_price` above `max_price`; a `brand` filter on `/brand`; both `path` and `url`, or both `brand` and `url`; a `product_id` or `sku` that is not 6-14 digits; a `url` that is not saksfifthavenue.com or has no product id; `product_id` and `url` naming different products; a `color` or `size` that is not one of the product's, with the valid list in the message; no location, `zip` together with `lat` / `lng`, or `lat` without `lng`; a ZIP that is not 5 digits; a `radius` that is not 15, 30, 50, 100 or 300; a `letter` that is not A-Z or `#`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product, category path or brand slug. Not charged. Re-run the search for a fresh `id`, or look the slug up in `/designers`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api).
- `502` or `503` means Saks is temporarily unavailable or returned an unusable page. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.

## SDKs

```bash
pip install scavio==0.43.0
npm install scavio@0.44.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.saks.search({ query: "coat", size: "Medium", sort: "price_low_to_high" });
const { data: item } = await scavio.saks.product({ product_id: found.items[0].id });
const { data: variant } = await scavio.saks.product({ product_id: item.id, color: item.colors[0].value, size: item.sizes[0].value });
const { data: near } = await scavio.saks.storeAvailability({ sku: variant.id, zip: "10022" });
const { data: next } = await scavio.saks.search({ query: "coat", start: found.next_start });
const { data: dresses } = await scavio.saks.category({ path: "/c/women-s-apparel/dresses" });
const { data: index } = await scavio.saks.designers({ letter: "G" });
const { data: gucci } = await scavio.saks.brand({ brand: "gucci" });
const { data: sale } = await scavio.saks.deals({ type: "womens_sale", brand: "Gucci" });
const { data: stores } = await scavio.saks.stores({ zip: "10022" });
const { data: ideas } = await scavio.saks.suggestions({ query: "gucci" });
```

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_saks`, `get_saks_product`, `get_saks_category`, `get_saks_brand`, `get_saks_deals`, `get_saks_stores`, `get_saks_store_availability`, `get_saks_suggestions` and `get_saks_designers`. Saks Fifth Avenue is opt-in: add `saks` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.41.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,saks"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/saks-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [product](https://scavio.dev/docs/saks-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [category](https://scavio.dev/docs/saks-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [brand](https://scavio.dev/docs/saks-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [deals](https://scavio.dev/docs/saks-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [stores](https://scavio.dev/docs/saks-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [store availability](https://scavio.dev/docs/saks-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [suggestions](https://scavio.dev/docs/saks-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api), [designers](https://scavio.dev/docs/saks-designers?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api). Overview: [Saks Fifth Avenue API](https://scavio.dev/saks-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=saks-fifth-avenue-api).
