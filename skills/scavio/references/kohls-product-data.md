# Kohl's Product Data API - Clearance, Kohl's Cash, Store Pickup Stock

Search Kohl's (kohls.com, US, prices in USD) by keyword, or browse a catalog page by its path or URL, one brand by name, or one of the deal lists (Clearance, Sale, items that earn Kohl's Cash right now, Sephora at Kohl's), 120 products per page plus any sponsored items, which stay in the list flagged `is_sponsored`. Sort by featured, new arrivals, best sellers, price, highest rated or percent off; filter by brand, color, size, on sale, clearance, or any facet value the response lists (price buckets, discount, customer rating, store pickup, gender, department...). Each item carries the id, title, URL, image, current price (and the top of the range), regular price, sale price, `price_label` (`sale`, `clearance`, `sale+regular`...), on-sale and clearance flags, percent off, the price after a public offer code (`with_code_price`) with the code, a cart-only price flag, BOGO promotions, the average rating, review count, badges, colors, Sephora and coupon-eligible flags, and online, pickup and ship-to-store availability. Read one product by id or URL with its department code, breadcrumbs, rating, review count and recommended percent, description, images, return policy, the price block, Kohl's Cash earn and redeem windows, the offers that apply (code, terms, dates), online units and every variant (SKU, UPC, color, size, availability, online units, max per order, price, with-code price, Kohl's Cash earned); add a `store_id` for that store's availability and in-store price per variant. Check one SKU's pickup stock at every Kohl's store within about 50 miles of a ZIP, with a real unit count per store. Find stores with weekly hours, store badges (Sephora...) and services, pull the search box's suggestions and today's public coupon codes. All endpoints return structured JSON, 2 credits each; stores costs 1.

See also: for Macy's sale, clearance and store pickup use the `macys-product-data` skill; for Target use `target-product-data`; for the cross-retailer price view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Track Kohl's clearance: list the Clearance page (optionally one brand, size or discount band, sorted by percent off) and detect new markdowns between runs
- Build a Kohl's price tracker or sale alert: poll products or listings and detect a price drop, a new sale or clearance label, or a better price with a coupon code
- Find which items earn Kohl's Cash right now, and read a product's Kohl's Cash earn and redeem dates
- Get today's Kohl's coupon codes, or the price of an item after the code applies
- Check whether a Kohl's item (one color and size) is in stock for pickup at a store near a ZIP code, and how many units that store has
- Search Kohl's for a product and compare prices, percent off, ratings and brands, or browse a category (small appliances, women's clothing...) or a brand's whole Kohl's catalog
- Browse Sephora at Kohl's
- Find Kohl's stores near a ZIP, a city or a point, with hours, Sephora shops and services like In-Store Pickup or Amazon Returns
- Prepare a Kohl's Black Friday watch list
- Get Kohl's search suggestions for keyword research

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 2 credits except stores (1), so the free credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Stores, store availability and suggestions usually answer in 3-5 seconds, product in about 5. The listing endpoints (search, category, brand, deals) read 120-product pages and took 9 to 11 seconds in the captures; coupons took 40 seconds. Allow a client timeout of at least 90 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/kohls/search` | 2 | 120 products per page plus sponsored items: id, title, URL, image, price, price max, regular price (and max), sale price (and max), `price_label`, `on_sale`, `is_clearance`, `percent_off`, `price_suppressed`, `price_note`, `with_code_price` (and max), `with_code_offer_codes`, promotions, rating, review count, badges, colors, `is_sephora`, `coupon_eligible`, `available_online`, `available_pickup`, `available_ship_to_store`, `is_sponsored`. Plus `corrected_query`, `redirected_to`, total, page, total pages, per page, sort, count, `sponsored_count`, `applied_filters`, `facets[]` with value ids and counts |
| `POST /api/v1/kohls/category` | 2 | One catalog listing by `path` or `url` (it must carry its `CN=` facets), the same grid as search, plus the category's name, breadcrumbs, path, URL and the facet ids that define it |
| `POST /api/v1/kohls/brand` | 2 | One brand by name as Kohl's lists it (`"Hamilton Beach"`, `"Levi's"`) or by URL, the same grid as search, plus the brand's name, facet value and URL |
| `POST /api/v1/kohls/deals` | 2 | A deal list by `type`: `clearance` (default), `sale`, `kohls_cash` (items that earn Kohl's Cash now) or `sephora` (Sephora at Kohl's), the same grid as search plus the list's label |
| `POST /api/v1/kohls/product` | 2 | One product by id or URL: brand, status, `dept`, breadcrumbs, `is_sephora`, rating, review count, recommended percent, new / best seller / top rated, badges, description, details, ingredients (beauty), images, videos, return policy, the price block (incl. `lowest_applicable_price`, `with_code_price`, `price_suppressed`), `kohls_cash` windows, `offers[]`, pickup / ship-to-store / Kohl's Cash eligibility, marketplace flag, online units, colors, sizes, and every variant (sku, UPC, color, size, availability, online units, max per order, prices, Kohl's Cash earned, pickup eligibility, beauty attributes). Add `store_id` for one store's availability and price per variant |
| `POST /api/v1/kohls/stores` | 1 | Kohl's stores near a ZIP, a city + state or a lat/lng point within 1-100 miles (default 25): store id, name, address, city, state, ZIP, phone, lat, lng, distance, weekly hours with the UTC offset, store badges (Sephora, Fine Jewelry, Lands' End...), services (In-Store Pickup, Amazon Returns Outpost...) and the store page URL |
| `POST /api/v1/kohls/store-availability` | 2 | One SKU at every store within about 50 miles of a ZIP: per store `pickup_units` (a unit count), `stock_level` (`In Stock`, `Low Stock`, `Out of Stock`), `in_stock`, ship-to-store units and pickup window, pickup and ship-to-store eligibility, clearance and Sephora flags, address, phone, distance and the week's hours. Plus `count`, `in_stock_count`, `total_pickup_units` |
| `POST /api/v1/kohls/suggestions` | 2 | The search box's suggestions for a partial term: keyword completions (`type: "terms"`, default) or matching products with id, title, URL and image (`type: "products"`) |
| `POST /api/v1/kohls/coupons` | 2 | Today's public Kohl's coupon codes: code, description (offer, minimum and exclusions as stated), end date, whether it needs a Kohl's Card, the terms page and the eligible-products URL |

## Workflow

1. **Find products:** call `/kohls/search` with `query`, `/kohls/deals` with a `type`, `/kohls/brand` with a `brand` name, or `/kohls/category` with a catalog `path`. Each item has an `id` and a `url`.
2. **Narrow the listing:** pass `brand` (search, category, deals), `color`, `size`, `on_sale`, `clearance`, or any facet through `filters` as a list of `facets[].values[].value` ids (`["Price:%2425%20to%20%2450", "TopRated:4"]`). Price is a facet bucket like `$25 to $50`, not a free range.
3. **Page through:** `page` 1, 2, 3... up to `total_pages`. A page holds 120 products plus the sponsored items.
4. **One product in full:** call `/kohls/product` with the item's `id` as `product_id` (or its `url`). Read `variants[]` for each SKU's color, size, stock and price, `kohls_cash` for the earn and redeem dates, and `offers[]` for the codes that apply.
5. **Store stock:** call `/kohls/store-availability` with a `variants[].sku`, the product's `dept` and the user's `zip`. Each store gives `pickup_units`, a real count.
6. **One store's price:** call `/kohls/product` again with a `store_id` from `/kohls/stores` (or from store availability): each variant gains a `store` block with that store's availability and price.
7. **Clearance tracking:** call `/kohls/deals` with `type: "clearance"`, `sort: "percent_off"` and the user's brand, size or a `Discount:` facet, walk the pages, and store `id`, `price`, `regular_price`, `percent_off`, `with_code_price` per run. Compare runs yourself: there is no price history.
8. **Coupons:** `/kohls/coupons` lists today's public codes. A listing item's `with_code_price` and `with_code_offer_codes` already show what a code does to that item.
9. **Keyword research:** `/kohls/suggestions` with a partial term returns completions; `type: "products"` returns matching products.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `page` | integer | 1 | Results page, 1-based (1-500). 120 products per page |
| `sort` | string | `featured` | `featured`, `new_arrivals`, `best_sellers`, `price_low_to_high`, `price_high_to_low`, `highest_rated` or `percent_off` |
| `brand` | string | none | One brand as the `Brand` facet lists it (`"Levi's"`, `"Hamilton Beach"`, `"BLACK+DECKER"`) |
| `color` | string | none | One color as the `Color` facet lists it (`Black`, `Blue`, `Beig/khaki`...) |
| `size` | string | none | One size as the `Size` facet lists it (`M`, `32X30`, `10`...) |
| `on_sale` | boolean | `false` | Only items on sale (`Promotions:Sale`) |
| `clearance` | boolean | `false` | Only clearance items (`Promotions:Clearance`) |
| `filters` | string or array | none | Facet value ids from a previous answer's `facets[].values[].value` (up to 10): `"Gender:Womens"`, `"Price:%2425%20to%20%2450"`, `"TopRated:4"`, `"InStoreOnline:Pick%20Up%20in%20Store"`, `"Discount:50%25%20off%20or%20more"`. Several facets combine (AND). Unencoded values work too (`"Price:$25 to $50"`) |

`brand`, `color` and `size` take one value each; for more values of one facet, send their ids through `filters`.

### Category (`/category`)

Pass `path` or `url` (not both), plus any search parameter except `query`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `path` | string | one of | A Kohl's catalog path WITH its `CN=` part: `/catalog/small-appliances-kitchen-dining.jsp?CN=Category:Small%20Appliances+Department:Kitchen%20%26%20Dining`. Take it from a kohls.com category link or a product's `breadcrumbs[].url` |
| `url` | string | one of | A kohls.com catalog URL with its `CN=` part. A sort or page in the URL is kept |

### Brand (`/brand`)

Pass `brand` or `url` (not both), plus any search parameter except `query` and the `brand` filter.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `brand` | string | one of | A brand name as the `Brand` facet lists it (`"Nike"`, `"Hamilton Beach"`, `"Levi's"`). An unknown brand is a 404 |
| `url` | string | one of | A kohls.com brand page URL whose `CN` carries `Brand:...` |

### Deals (`/deals`)

Any search parameter except `query`, plus:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `clearance` | `clearance`, `sale`, `kohls_cash` (items that earn Kohl's Cash right now) or `sephora` (Sephora at Kohl's) |

### Product (`/product`)

Pass `product_id` or `url`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_id` | string or integer | one of | Kohl's product id (4-10 digits): a listing item's `id`, the number after `prd-` in a product URL (`"6251213"`) |
| `url` | string | one of | A kohls.com product URL with `prd-<id>` in its path |
| `store_id` | string or integer | none | A Kohl's store number (`stores[].store_id`, e.g. `"725"`): adds that store's availability and price to every variant |

### Stores (`/stores`)

Pass one of `zip`, `city` + `state`, or `lat` + `lng`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | US ZIP code (`60601` or `60601-1234`) |
| `city`, `state` | string | one of | A US city and its 2-letter state code (`Austin`, `TX`), both required together |
| `lat`, `lng` | number | one of | A point, both required together |
| `radius` | integer | 25 | Radius in miles, 1-100 |

### Store availability (`/store-availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `sku` | string or integer | required | A Kohl's SKU code (5-12 digits): a product's `variants[].sku` (`"73519108"`). A product id is not a SKU |
| `dept` | string | none | The product's department code (`product.dept`, e.g. `"063"`). Optional; send it when you have it |
| `zip` | string | required | US ZIP code. Stores within about 50 miles are listed; there is no radius parameter |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-100 chars, no `/ \ ? #`) |
| `type` | string | `terms` | `terms` (keyword completions) or `products` (matching products) |

### Coupons (`/coupons`)

No parameters: send `{}`.

## Examples

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_id": "6251213"}'
```

Captured `data` (description and details shortened, the offer terms shortened, 2 of 4 breadcrumbs and 6 of 8 images trimmed):

```json
{
  "id": "6251213",
  "title": "Hamilton Beach 1.7-Liter Black Electric Kettle",
  "brand": "Hamilton Beach",
  "brand_url": "https://www.kohls.com/catalog/hamilton-beach.jsp?CN=Brand:Hamilton%20Beach",
  "url": "https://www.kohls.com/product/prd-6251213/hamilton-beach-17-liter-black-electric-kettle.jsp",
  "status": "In Stock",
  "dept": "063",
  "breadcrumbs": [
    { "name": "Kitchen & Dining", "url": "https://www.kohls.com/catalog/kitchen-dining.jsp?CN=Department:Kitchen%20%26%20Dining" },
    { "name": "Small Appliances", "url": "https://www.kohls.com/catalog/small-appliances-kitchen-dining.jsp?CN=Category:Small%20Appliances+Department:Kitchen%20%26%20Dining" }
  ],
  "partnership": null,
  "is_sephora": false,
  "rating": 4.3,
  "review_count": 188,
  "recommended_percent": 49,
  "is_new": false,
  "best_seller": true,
  "top_rated": false,
  "badges": ["Best Seller"],
  "description": "Bring style and performance to your kitchen with the Hamilton Beach 1.7-Liter Electric Kettle. ...",
  "details": "Bring style and performance to your kitchen with the Hamilton Beach 1.7-Liter Electric Kettle. ...",
  "ingredients": null,
  "images": [
    "https://media.kohlsimg.com/is/image/kohls/6251213?wid=350&hei=350&op_sharpen=1",
    "https://media.kohlsimg.com/is/image/kohls/6251213_ALT?wid=50&hei=50&op_sharpen=1"
  ],
  "videos": [],
  "return_policy": "Free in-store returns for 90 days or 120 for Kohl's Card Holders",
  "price": 29.99,
  "regular_price": 39.99,
  "regular_price_max": null,
  "sale_price": 29.99,
  "sale_price_max": null,
  "sale_status": "Sale",
  "percent_off": 25,
  "lowest_applicable_price": 23.99,
  "price_suppressed": false,
  "price_note": null,
  "with_code_price": null,
  "with_code_price_max": null,
  "with_code_savings": null,
  "with_code_offer_codes": [],
  "kohls_cash": null,
  "offers": [
    {
      "id": "58452",
      "code": "LOVE2SAVE",
      "description": "Save an extra 20% in store & online!",
      "terms": "20% COUPON IS VALID ON QUALIFYING PURCHASES 11/09-11/21, 2026. Must present coupon in store or enter code at Kohls.com. ...",
      "discount_type": "percentOff",
      "discount_amount": 20,
      "starts": "2026-11-08T23:00:00",
      "ends": "2026-11-22T02:00:00"
    }
  ],
  "pickup_eligible": true,
  "ship_to_store_eligible": true,
  "kohls_cash_eligible": true,
  "is_marketplace": false,
  "online_units": 376,
  "colors": ["Black"],
  "sizes": [],
  "variant_count": 1,
  "variants": [
    {
      "sku": "73519108",
      "upc": "000040094410385",
      "color": "Black",
      "size": null,
      "availability": "In Stock",
      "online_units": 376,
      "max_per_order": 3,
      "price": 29.99,
      "regular_price": 39.99,
      "sale_price": 29.99,
      "sale_status": "Sale",
      "lowest_applicable_price": 23.99,
      "with_code_price": null,
      "with_code_savings": null,
      "with_code_offer_codes": [],
      "percent_off": 25,
      "price_suppressed": false,
      "kohls_cash_earned": null,
      "pickup_eligible": true,
      "ship_to_store_eligible": true,
      "in_store": true,
      "image": "https://media.kohlsimg.com/is/image/kohls/6251213",
      "attributes": {}
    }
  ],
  "store_id": null,
  "currency": "USD"
}
```

`lowest_applicable_price` (23.99) is the $29.99 sale price less the 20% `LOVE2SAVE` offer in `offers[]`. On this product `with_code_price` was null, while the same kettle on the brand listing showed `with_code_price: 23.99` with `["LOVE2SAVE"]`: on `/product`, read `lowest_applicable_price` and `offers[]`, not only `with_code_price`. `kohls_cash` is null here because the kettle had no Kohl's Cash window that day; when it has one it is `{earn_start, earn_end, redeem_start, redeem_end, earned_min, earned_max, exclusions_url}`. `rating` (4.3), `review_count` (188) and `recommended_percent` (49) are all Kohl's gives about reviews: review text is not available. Pass `variants[0].sku` (`"73519108"`) and `dept` (`"063"`) to `/store-availability`.

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jeans"}'
```

Captured `data` for `{"query": "jeans"}` (126 of 128 items, 7 colors of the first item, 10 of 12 facets and some facet values trimmed):

```json
{
  "query": "jeans",
  "corrected_query": null,
  "redirected_to": null,
  "total": 5796,
  "page": 1,
  "total_pages": 49,
  "per_page": 120,
  "sort": "featured",
  "count": 128,
  "sponsored_count": 8,
  "items": [
    {
      "id": "2982007",
      "title": "Juniors' WallFlower Insta Stretch® Luscious Curvy Bootcut Jeans",
      "url": "https://www.kohls.com/product/prd-2982007/juniors-wallflower-luscious-curvy-bootcut-jeans.jsp",
      "image": "https://media.kohlsimg.com/is/image/kohls/2982007_Jenna?wid=180&hei=180&op_sharpen=1",
      "price": 24,
      "price_max": 40,
      "regular_price": 40,
      "regular_price_max": null,
      "sale_price": 24,
      "sale_price_max": 40,
      "price_label": "clearance+regular",
      "on_sale": true,
      "is_clearance": true,
      "percent_off": 40,
      "price_suppressed": false,
      "price_note": null,
      "with_code_price": 19.2,
      "with_code_price_max": 32,
      "with_code_offer_codes": ["LOVE2SAVE"],
      "promotions": [],
      "rating": 4.4,
      "review_count": 4477,
      "badges": ["best_seller"],
      "colors": ["Delilah", "Davey"],
      "is_sephora": false,
      "coupon_eligible": true,
      "available_online": true,
      "available_pickup": true,
      "available_ship_to_store": true,
      "is_sponsored": false,
      "currency": "USD"
    },
    {
      "id": "1070694",
      "title": "Men's Lee® Relaxed Fit Jeans",
      "url": "https://www.kohls.com/product/prd-1070694/mens-lee-relaxed-fit-jeans.jsp",
      "image": "https://media.kohlsimg.com/is/image/kohls/1070694_Medium_Stone",
      "price": 39.99,
      "price_max": 50,
      "regular_price": 50,
      "regular_price_max": null,
      "sale_price": 39.99,
      "sale_price_max": 50,
      "price_label": "sale",
      "on_sale": true,
      "is_clearance": false,
      "percent_off": 20,
      "price_suppressed": false,
      "price_note": null,
      "with_code_price": null,
      "with_code_price_max": null,
      "with_code_offer_codes": [],
      "promotions": [],
      "rating": 4.3925,
      "review_count": 3192,
      "badges": [],
      "colors": ["Medium Stone", "Newman"],
      "is_sephora": false,
      "coupon_eligible": false,
      "available_online": null,
      "available_pickup": null,
      "available_ship_to_store": null,
      "is_sponsored": true,
      "currency": "USD"
    }
  ],
  "applied_filters": [],
  "facets": [
    {
      "id": "InStoreOnline",
      "label": "Pickup & Shipping",
      "values": [
        { "label": "Store Pickup Today", "value": "InStoreOnline:Pick%20Up%20in%20Store", "count": 1364, "selected": false },
        { "label": "Ship to Store", "value": "InStoreOnline:Ship%20to%20Store", "count": 2214, "selected": false },
        { "label": "Ship to Me", "value": "InStoreOnline:Online%20Only", "count": 5768, "selected": false }
      ]
    },
    {
      "id": "Price",
      "label": "Price",
      "values": [
        { "label": "$10 to $25", "value": "Price:%2410%20to%20%2425", "count": 1154, "selected": false },
        { "label": "$25 to $50", "value": "Price:%2425%20to%20%2450", "count": 2879, "selected": false }
      ]
    }
  ],
  "currency": "USD"
}
```

`count` is 128 because 8 sponsored items sit among the 120 (positions 2, 5, 8 ... 23 here): drop `is_sponsored: true` items when you want only the organic grid, and dedupe by `id` across pages. All 8 sponsored items repeated products already in the organic grid and came back with `available_*` null. The WallFlower jeans sell from $24 to $40 by color and size, so quote a range; with `LOVE2SAVE` the range is $19.20 to $32. The other facets on this answer were `Gender`, `SizeRange`, `Fit`, `LegOpening`, `Size` (499 values), `Rise`, `Brand` (290), `Color`, `TopRated` and `Material`.

### Deals (clearance)

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "clearance"}'
```

The captured answer opens with `"type": "clearance"`, `"label": "Clearance"`, `total: 4282`, `total_pages: 36`, `count: 120`, `sponsored_count: 0` and 15 facets, including `Discount` (`"Discount:50%25%20off%20or%20more"`, 30% to 80% off or more). Its first item:

```json
{
  "id": "3836990",
  "title": "Women's Croft & Barrow® Essential Long-Sleeve Classic Crewneck Tee",
  "url": "https://www.kohls.com/product/prd-3836990/womens-croft-barrow-essential-long-sleeve-classic-crewneck-tee.jsp",
  "image": "https://media.kohlsimg.com/is/image/kohls/3836990_Ivory_Autumn_Tile?wid=180&hei=180&op_sharpen=1",
  "price": 8.99,
  "price_max": null,
  "regular_price": 14.99,
  "regular_price_max": null,
  "sale_price": 8.99,
  "sale_price_max": null,
  "price_label": "clearance",
  "on_sale": true,
  "is_clearance": true,
  "percent_off": 40,
  "price_suppressed": false,
  "price_note": null,
  "with_code_price": 7.19,
  "with_code_price_max": null,
  "with_code_offer_codes": ["LOVE2SAVE"],
  "promotions": [],
  "rating": 4.5,
  "review_count": 15468,
  "badges": ["best_seller"],
  "colors": ["Maroon Rose", "Navy Nice Flowers", "Ivory Autumn Tile", "Red Small Paisley", "Red Nice Flowers"],
  "is_sephora": false,
  "coupon_eligible": true,
  "available_online": true,
  "available_pickup": false,
  "available_ship_to_store": true,
  "is_sponsored": false,
  "currency": "USD"
}
```

The same page also held "add to cart for price" items, for example a Nike toddler shoe with `"price": null`, `"regular_price": 40`, `"price_suppressed": true`, `"price_note": "FOR PRICE,ADD TO CART"`, `"price_label": null` and `"is_clearance": false`: Kohl's shows that price only in the cart, so report the regular price and the note, never a guessed sale price.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/catalog/small-appliances-kitchen-dining.jsp?CN=Category:Small%20Appliances+Department:Kitchen%20%26%20Dining"}'
```

The captured page opens with:

```json
{
  "category": {
    "name": "Small Appliances",
    "breadcrumbs": ["Kitchen & Dining", "Small Appliances"],
    "path": "/catalog/small-appliances-kitchen-dining.jsp?CN=Category:Small%20Appliances+Department:Kitchen%20%26%20Dining",
    "url": "https://www.kohls.com/catalog/small-appliances-kitchen-dining.jsp?CN=Category:Small%20Appliances+Department:Kitchen%20%26%20Dining",
    "facets": ["Category:Small%20Appliances", "Department:Kitchen%20%26%20Dining"]
  },
  "total": 2486,
  "page": 1,
  "total_pages": 21,
  "per_page": 120,
  "sort": "featured",
  "count": 126,
  "sponsored_count": 6
}
```

then 126 items in the search shape, `applied_filters` with the two facets that define the page, and 10 facets (`Department`, `InStoreOnline`, `CouponEligible`, `Category`, `Product`, `Brand` with 213 values, `Promotions`, `Price`, `Color`, `TopRated`). The path is the whole thing: `/catalog/small-appliances-kitchen-dining.jsp` alone is a 400, because the `CN=` facets define the listing, not the file name.

### Brand

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/brand \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"brand": "Hamilton Beach"}'
```

The captured answer opens with `"brand": { "name": "Hamilton Beach", "value": "Brand:Hamilton%20Beach", "url": "https://www.kohls.com/catalog/hamilton-beach.jsp?CN=Brand:Hamilton%20Beach" }`, `total: 159`, `total_pages: 2`, `count: 120`, `sponsored_count: 0`, then the same `items[]` as search (118 of the 120 carried a `with_code_price`).

### Store availability

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sku": "73519108", "dept": "063", "zip": "10001"}'
```

Captured `data` (43 of 44 stores trimmed; the kept one is the nearest store with stock):

```json
{
  "sku": "73519108",
  "zip": "10001",
  "dept": "063",
  "count": 44,
  "in_stock_count": 23,
  "total_pickup_units": 45,
  "stores": [
    {
      "store_id": "541",
      "name": "CLIFTON",
      "pickup_units": 1,
      "stock_level": "Low Stock",
      "in_stock": true,
      "ship_to_store_units": 200,
      "pickup_eligible": true,
      "ship_to_store_eligible": true,
      "ship_to_store_window": "Thu, Nov 12 - Tue, Nov 17",
      "ship_to_store_from": "2026-11-12T03:22:11-06:00",
      "ship_to_store_to": "2026-11-17T03:22:11-06:00",
      "is_clearance": false,
      "has_sephora": true,
      "distance_miles": 9.17,
      "address": "14 MAIN AVE",
      "address_2": null,
      "city": "CLIFTON",
      "state": "NJ",
      "zip": "07014",
      "phone": "(973) 661-9470",
      "lat": 40.829582,
      "lng": -74.142972,
      "hours": [
        { "day": "Sunday", "date": "2026-11-15", "open": "09:00", "close": "22:00" },
        { "day": "Tuesday", "date": "2026-11-10", "open": "09:00", "close": "22:00" },
        { "day": "Friday", "date": "2026-11-13", "open": "09:00", "close": "23:00" }
      ]
    }
  ]
}
```

Stores come nearest first, out to 49.88 miles here. The two nearest (Jersey City, Secaucus) had `pickup_units: 0` and `Out of Stock`; per-store counts ran from 0 to 5 (`Low Stock` at 1-2 units, `In Stock` at 3-5). `pickup_units` is Kohl's own unit count for that store. `ship_to_store_units` read 200 at every store: it is what can be shipped to the store for pickup in `ship_to_store_window`, not stock on the shelf. `hours` holds the next seven days (4 of 7 trimmed above), listed Sunday first: match on `date`.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "60601"}'
```

Captured `data` (18 of 19 stores and 4 of 7 days trimmed):

```json
{
  "location": { "zip": "60601" },
  "radius_miles": 25,
  "count": 19,
  "stores": [
    {
      "store_id": "725",
      "name": "Kohl's Bucktown",
      "address": "2140 N ELSTON AVE",
      "address_2": null,
      "city": "CHICAGO",
      "state": "IL",
      "zip": "60614",
      "phone": "(773) 342-9032",
      "lat": 41.9204591,
      "lng": -87.6718313,
      "distance_miles": 3.7,
      "hours": [
        { "day": "Sunday", "open": "09:00", "close": "22:00" },
        { "day": "Monday", "open": "09:00", "close": "22:00" },
        { "day": "Friday", "open": "09:00", "close": "23:00" }
      ],
      "utc_offset": -6,
      "observes_dst": true,
      "badges": ["Sephora", "Babies'R'Us", "Indochino", "Fine Jewelry", "Lands' End", "Little Co.", "FLX", "Kids Room Shop"],
      "services": ["In-Store Pickup", "Wifi Enabled", "Amazon Returns Outpost", "Energy Star"],
      "url": "https://www.kohls.com/stores/il/chicago-725.shtml"
    }
  ]
}
```

`store_id` ("725") is what `/product` takes as `store_id`. A store with Sephora at Kohl's lists `"Sephora"` in `badges`. `utc_offset` (with `observes_dst`) is the store's offset from UTC.

### Coupons

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/coupons \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (3 of 5 offers trimmed: HOME10, TOYS10 and SHOP10):

```json
{
  "count": 5,
  "offers": [
    {
      "code": "LOVE2SAVE",
      "description": "Take an extra 20% off. Ends November 21.",
      "ends": "2026-11-21",
      "requires_kohls_card": false,
      "details_url": "https://www.kohls.com/ecom/PrintPass/LOVE2SAVE/20261109.html",
      "shop_url": "https://www.kohls.com/catalog.jsp?CN=CouponEligible:Eligible"
    },
    {
      "code": "NOV30",
      "description": "Take an extra 30% off with a Kohl's Card. Ends November 21.",
      "ends": "2026-11-21",
      "requires_kohls_card": true,
      "details_url": "https://www.kohls.com/ecom/PrintPass/NOV30/20261109.html",
      "shop_url": "https://www.kohls.com/catalog.jsp?CN=CouponEligible:Eligible&BL=y"
    }
  ]
}
```

These are the public codes on Kohl's today's-deals page, with the description as Kohl's states it (minimum purchase and exclusions included). `details_url` can be null. Account-specific offers and Kohl's Rewards balances are not covered.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/kohls/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "coff"}'
```

Captured `data`:

```json
{
  "query": "coff",
  "type": "terms",
  "count": 8,
  "suggestions": ["coffee makers", "keurig coffee makers", "ninja coffee makers", "coffee mugs", "cuisinart coffee makers", "coffee", "coffee grinder", "keurig single serve coffee maker"]
}
```

With `"type": "products"` the answer carries `products[]` {`id`, `title`, `url`, `image`} instead of `suggestions[]`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def kohls(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/kohls/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Clearance for one brand, biggest markdown first, organic items only (2 credits per page)
page = kohls("deals", {"type": "clearance", "brand": "Nike", "sort": "percent_off"})
for p in [i for i in page["items"] if not i["is_sponsored"]][:5]:
    print(p["id"], p["title"], p["price"], "was", p["regular_price"], p["percent_off"], "with code", p["with_code_price"])

# 2. One product, then pickup stock near the user (2 calls, 2 credits each)
item = kohls("product", {"product_id": "6251213"})
v = item["variants"][0]
near = kohls("store-availability", {"sku": v["sku"], "dept": item["dept"], "zip": "10001"})
for s in near["stores"]:
    if s["in_stock"]:
        print(s["name"], s["distance_miles"], "mi", s["pickup_units"], "units", s["stock_level"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Nothing is cached; `fetched_at` is when the answer was produced.

- **listing item** (search, category, brand, deals) - `id`, `title`, `url`, `image`, `price`, `price_max`, `regular_price`, `regular_price_max`, `sale_price`, `sale_price_max`, `price_label`, `on_sale`, `is_clearance`, `percent_off`, `price_suppressed`, `price_note`, `with_code_price`, `with_code_price_max`, `with_code_offer_codes[]`, `promotions[]` (BOGO texts), `rating`, `review_count`, `badges[]` (`best_seller`, `kohlsexclusive_badge`, `bogo_1_1_p_50`...), `colors[]`, `is_sephora`, `coupon_eligible`, `available_online`, `available_pickup`, `available_ship_to_store`, `is_sponsored`, `currency`.
- **grid** (all four listings) - `total`, `page`, `total_pages`, `per_page` (120), `sort`, `count`, `sponsored_count`, `items[]`, `applied_filters[]` {`facet`, `label`, `value`}, `facets[]` {`id`, `label`, `values[]` {`label`, `value`, `count`, `selected`}}, `currency`.
- **search** - `query`, `corrected_query` (the keyword the site searched instead, or null), `redirected_to` ({`url`} or null) and the grid.
- **category** - `category` {`name`, `breadcrumbs[]`, `path`, `url`, `facets[]`} and the grid.
- **brand** - `brand` {`name`, `value`, `url`} and the grid.
- **deals** - `type`, `label` and the grid.
- **product** - `id`, `title`, `brand`, `brand_url`, `url`, `status`, `dept`, `breadcrumbs[]` {`name`, `url`}, `partnership`, `is_sephora`, `rating`, `review_count`, `recommended_percent`, `is_new`, `best_seller`, `top_rated`, `badges[]`, `description`, `details`, `ingredients`, `images[]`, `videos[]`, `return_policy`, `price`, `regular_price`, `regular_price_max`, `sale_price`, `sale_price_max`, `sale_status`, `percent_off`, `lowest_applicable_price`, `price_suppressed`, `price_note`, `with_code_price`, `with_code_price_max`, `with_code_savings`, `with_code_offer_codes[]`, `kohls_cash` ({`earn_start`, `earn_end`, `redeem_start`, `redeem_end`, `earned_min`, `earned_max`, `exclusions_url`} or null), `offers[]` {`id`, `code`, `description`, `terms`, `discount_type`, `discount_amount`, `starts`, `ends`}, `pickup_eligible`, `ship_to_store_eligible`, `kohls_cash_eligible`, `is_marketplace`, `online_units`, `colors[]`, `sizes[]`, `variant_count`, `variants[]` {`sku`, `upc`, `color`, `size`, `availability`, `online_units`, `max_per_order`, `price`, `regular_price`, `sale_price`, `sale_status`, `lowest_applicable_price`, `with_code_price`, `with_code_savings`, `with_code_offer_codes[]`, `percent_off`, `price_suppressed`, `kohls_cash_earned`, `pickup_eligible`, `ship_to_store_eligible`, `in_store`, `image`, `attributes`, and with `store_id` a `store` {`store_id`, `availability`, `price`, `regular_price`, `sale_price`, `sale_status`} or null}, `store_id`, `currency`.
- **stores** - `location` ({`zip`}, {`city`, `state`} or {`lat`, `lng`}), `radius_miles`, `count`, `stores[]` {`store_id`, `name`, `address`, `address_2`, `city`, `state`, `zip`, `phone`, `lat`, `lng`, `distance_miles`, `hours[]` {`day`, `open`, `close`}, `utc_offset`, `observes_dst`, `badges[]`, `services[]`, `url`}.
- **store-availability** - `sku`, `zip`, `dept`, `count`, `in_stock_count`, `total_pickup_units`, `stores[]` {`store_id`, `name`, `pickup_units`, `stock_level`, `in_stock`, `ship_to_store_units`, `pickup_eligible`, `ship_to_store_eligible`, `ship_to_store_window`, `ship_to_store_from`, `ship_to_store_to`, `is_clearance`, `has_sephora`, `distance_miles`, `address`, `address_2`, `city`, `state`, `zip`, `phone`, `lat`, `lng`, `hours[]` {`day`, `date`, `open`, `close`}}.
- **suggestions** - `query`, `type`, `count`, and `suggestions[]` (strings) for `terms` or `products[]` {`id`, `title`, `url`, `image`} for `products`.
- **coupons** - `count`, `offers[]` {`code`, `description`, `ends`, `requires_kohls_card`, `details_url`, `shop_url`}.

## Guardrails

- Prices are US dollars (`currency: "USD"`): `29.99` is $29.99. This is kohls.com (US) only; there is no international site.
- `price` is the current price. When an item sells at a range (by color or size), `price` is the low end and `price_max` the high end; `with_code_price_max` works the same way. Quote a range as a range. `percent_off` compares the low end of the sale price with the low end of the regular price, so on a range item it is not every variant's discount. For one variant's price, read `variants[]` on `/product`.
- `percent_off` is measured against Kohl's own `regular_price`. Kohl's terms say a "Regular" or "Original" price is a former or future offered price and actual sales may not have been made at it; report it as Kohl's regular price, not as proof of a past price.
- `price_label` combines labels when variants differ: `clearance+regular` means some colors or sizes are on clearance and others at regular price. `is_clearance` is true when any part is clearance.
- `price_suppressed: true` means Kohl's shows the price only in the cart: `price`, `sale_price` and `percent_off` are null and `price_note` carries Kohl's text (`"FOR PRICE,ADD TO CART"`). Report the regular price and the note; never guess the cart price. Such items can appear on the Clearance list without a clearance label.
- `with_code_price` is the price after the public offer code(s) in `with_code_offer_codes`, as Kohl's computes it. It is not applied at checkout by this API, and codes have end dates (see `/coupons` or `offers[]`). On `/product`, also read `lowest_applicable_price`: in the capture it held the after-code price while `with_code_price` was null.
- Kohl's Cash: `kohls_cash` on `/product` gives the earn and redeem dates and the amount range when the product earns it; `variants[].kohls_cash_earned` per SKU. Kohl's Cash balances and Kohl's Rewards accounts are not covered. `type: "kohls_cash"` on `/deals` lists items that earn Kohl's Cash now.
- Reviews: listing items carry `rating` and `review_count`; `/product` adds `recommended_percent`. Review text is not available from any endpoint, so never summarize or quote what reviewers say.
- Sponsored items: a page carries up to about 8 sponsored products among the 120, flagged `is_sponsored: true` and counted in `sponsored_count`; they can repeat organic items and come with `available_*` null. Filter them out for organic rankings and dedupe by `id`.
- Filters take facet value ids: `filters` entries are `facets[].values[].value` (`"Color:Black"`, `"Price:%2425%20to%20%2450"`). Price is a bucket from the `Price` facet; there is no free `min_price` / `max_price`. A filter that matches nothing returns a 200 with `total: 0`; check `total` and the `selected` flags before claiming a list is filtered. At most 10 facets per call, counting the ones that define a category, brand or deal page.
- `brand`, `color` and `size` take the facet's own spelling and one value each. `size: "M"` works on Kohl's. A `brand` filter on `/brand` is a 400.
- A keyword the site autocorrects comes back with `corrected_query` (the term actually searched): say so. A keyword the site sends to a catalog page gives `redirected_to.url`; one it sends to a landing page with no product grid gives `total: 0` and that `redirected_to`.
- `/category` needs the catalog path or URL with its `CN=` facets; take it from a kohls.com link or a product's `breadcrumbs[].url`.
- Store stock: `/store-availability` takes a variant `sku`, never a product id, and covers stores within about 50 miles of the ZIP. `pickup_units` is the store's unit count for pickup; `stock_level` is Kohl's band (`Low Stock` was 1-2 units and `In Stock` 3-5 in the capture). `ship_to_store_units` is not shelf stock. Stock changes through the day: give the `fetched_at` time with any count.
- `online_units` (product and variants) is online stock, not store stock. `max_per_order` is Kohl's per-order limit.
- There is no price history. To track clearance or prices, poll the listings or `/product` on a schedule and store the results yourself.
- Coupons: `/coupons` returns the public codes on Kohl's today's-deals page only. `requires_kohls_card: true` codes need a Kohl's Card. Report codes with their `description` and `ends`; do not promise a code works on a given item beyond what `with_code_offer_codes` or `coupon_eligible` says.
- Kohl's publishes no public developer or catalog API: marketplace sellers get API access through the Mirakl seller portal, and the Kohl's Creators affiliate program gives links, not data. This API reads public product data for research, price monitoring and stock alerts. It does not add to cart, check out or reserve stock; do not present it as a purchasing bot.
- Never fabricate prices, sale or clearance status, Kohl's Cash dates, coupon codes, stock, unit counts or ratings. Only return what the API returned, with the product `url` or `id`.

## Failure handling

- `400` means a missing or invalid parameter (no `query`; `page` outside 1-500; an unknown `sort`, deal `type` or suggestions `type`; a `filters` entry that is not a facet id like `"Color:Black"`, or more than 10 facets; more than one value in `brand`, `color` or `size`; a `brand` filter on `/brand`; both `path` and `url`, or both `brand` and `url`; a catalog path or URL without its `CN=` part; a brand URL whose `CN` has no `Brand:`; a `product_id` that is not 4-10 digits; a product `url` without `prd-<id>`; `product_id` and `url` naming different products; a `store_id` that is not 1-5 digits; a `sku` that is not 5-12 digits; a `dept` that is not 1-4 digits; a ZIP that is not 5 digits; more than one of `zip`, `city` + `state` and `lat` + `lng`, `city` without `state` or `lat` without `lng`; a `radius` outside 1-100; a suggestions `query` with `/ \ ? #`).
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product (it can take about 20 seconds), no products under that catalog path, or no such brand. Not charged. Re-run the search for a fresh `id`, or use a brand as the `Brand` facet of a search lists it.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data).
- `502` or `503` means Kohl's is temporarily unavailable or returned an unusable page. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.

## SDKs

```bash
pip install scavio==0.44.0
npm install scavio@0.45.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.kohls.search({ query: "jeans", size: "32X30", sort: "percent_off" });
const { data: item } = await scavio.kohls.product({ product_id: found.items[0].id });
const { data: near } = await scavio.kohls.storeAvailability({ sku: item.variants[0].sku, dept: item.dept, zip: "10001" });
const { data: next } = await scavio.kohls.search({ query: "jeans", page: 2 });
const { data: clearance } = await scavio.kohls.deals({ type: "clearance", brand: "Nike", sort: "percent_off" });
const { data: kitchen } = await scavio.kohls.category({ path: "/catalog/small-appliances-kitchen-dining.jsp?CN=Category:Small%20Appliances+Department:Kitchen%20%26%20Dining" });
const { data: brand } = await scavio.kohls.brand({ brand: "Hamilton Beach" });
const { data: stores } = await scavio.kohls.stores({ zip: "60601" });
const { data: atStore } = await scavio.kohls.product({ product_id: "6251213", store_id: stores.stores[0].store_id });
const { data: ideas } = await scavio.kohls.suggestions({ query: "coff" });
const { data: codes } = await scavio.kohls.coupons();
```

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_kohls`, `get_kohls_product`, `get_kohls_category`, `get_kohls_brand`, `get_kohls_deals`, `get_kohls_stores`, `get_kohls_store_availability`, `get_kohls_suggestions` and `get_kohls_coupons`. Kohl's is opt-in: add `kohls` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.42.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,kohls"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/kohls-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [product](https://scavio.dev/docs/kohls-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [category](https://scavio.dev/docs/kohls-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [brand](https://scavio.dev/docs/kohls-brand?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [deals](https://scavio.dev/docs/kohls-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [stores](https://scavio.dev/docs/kohls-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [store availability](https://scavio.dev/docs/kohls-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [suggestions](https://scavio.dev/docs/kohls-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data), [coupons](https://scavio.dev/docs/kohls-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data). Overview: [Kohl's API](https://scavio.dev/kohls-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=kohls-product-data).
