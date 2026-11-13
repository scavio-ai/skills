# Kroger Grocery Data API - Search, Store Prices, Coupons, QFC + Fred Meyer

Read grocery and general-merchandise data from three Kroger banners: Kroger (kroger.com), QFC (qfc.com, Washington and Oregon) and Fred Meyer (fredmeyer.com, the Pacific Northwest and Alaska, with grocery plus general merchandise, apparel and home). Search by keyword or open a category listing, read one product with nutrition, ingredients and allergens, list this week's digital deals and a store's digital coupons, and find stores near a ZIP code or a city. For one specific store's price, promotion, stock and aisle, pass up to 25 UPCs and a `store_id` to the prices endpoint. Every price is an integer number of cents (`price: 579` is $5.79). All 8 endpoints return structured JSON and cost 1 to 3 credits each.

The same item is priced differently by banner and by store. On 2026-11-13 Simple Truth organic lactose-free 2% milk (UPC `0001111050438`) had a regular price of $5.79 at QFC Seattle, $4.99 at Fred Meyer Portland and $5.99 at Fred Meyer Anchorage. That is why the store matters more than the banner: always say which store a price came from.

Kroger runs a free, self-service developer API (developer.kroger.com) for its public Products and Locations endpoints, with OAuth client credentials and a limit of 10,000 product calls per day; it returns a store's price only when the request passes `filter.locationId`. Its Acceptable Use page lists as prohibited "Comparing products/prices among other retailers" and "Systematically scraping or gathering response data to create a database". This skill reads the public Kroger, QFC and Fred Meyer sites with one Scavio key and adds what the public API has no endpoint for: weekly digital deals, digital coupons and search suggestions.

See also: for other US grocery store prices use `heb-grocery-data`, `aldi-grocery-data`, `whole-foods-grocery-data` or `costco-product-data`; for the cross-retailer view use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Look up Kroger, QFC or Fred Meyer prices for a product, a brand or a category
- Get Fred Meyer or QFC prices by store, or compare one item's price across stores and banners
- Check stock level, available quantity and the aisle, bay and shelf of items at one store
- Find Kroger, QFC or Fred Meyer stores (and fuel centers) near a ZIP code or a city, with hours, departments and pharmacy
- List this week's Kroger, QFC or Fred Meyer weekly digital deals, or a store's digital coupons by department
- Read nutrition facts, ingredients, allergens or dietary flags for a Kroger product
- Build a grocery price basket or a shelf-price monitor across Pacific Northwest stores
- Autocomplete a grocery search the way the store's search box does

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. The endpoints here cost 1 to 3 credits each (search and product 2, prices 3, the rest 1).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Banners

Every endpoint takes `banner`. Only these three are served:

| `banner` | Site | Region | Store ids start with |
|---|---|---|---|
| `kroger` (default) | kroger.com | Kroger stores across the US | anything else |
| `qfc` | qfc.com | QFC: Washington and Oregon | `705` |
| `fred_meyer` | fredmeyer.com | Fred Meyer: the Pacific Northwest and Alaska; grocery plus general merchandise, apparel and home | `701` |

With a `store_id` the banner can be left out: it is read from the id. A banner that contradicts a `store_id` prefix or the host of an absolute URL is a `400`. Other Kroger banners (Ralphs, King Soopers, Fry's, Smith's, Harris Teeter, Dillons, Mariano's and the rest) are not served yet: say so rather than sending their URLs or approximating them with `kroger`.

## Endpoints

Base URL: `https://api.scavio.dev`. Most calls answered in 3 to 11 seconds in testing; a kroger.com search took 35 seconds and a 3-UPC prices call 47 seconds, and prices can take about a minute. Allow a client timeout of at least 90 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/kroger/search` | 2 | Keyword search, first page only (up to 24 products): `banner`, `store`, `total`, `count`, `products[]` |
| `POST /api/v1/kroger/product` | 2 | One product by URL or UPC: the search fields plus description, nutrition (serving size, facts, ingredients, allergens), images, country of origin, dimensions, weight, aisle (`store_location`) and breadcrumbs |
| `POST /api/v1/kroger/prices` | 3 | Price, promotion, stock, available quantity, aisle and fulfillment for 1 to 25 UPCs at one store you choose (`store_id`) |
| `POST /api/v1/kroger/stores` | 1 | Stores near a ZIP or a city / address (up to 50, nearest first), or one store by `store_id`: `location_id`, address, coordinates, phone, hours, departments, pharmacy, fuel center, pickup, delivery, distance |
| `POST /api/v1/kroger/category` | 1 | One category listing by `/pl/` URL or `taxonomy_id`, first page only, in the search shape |
| `POST /api/v1/kroger/deals` | 1 | This week's weekly digital deals (`deals_week` with its end), first page only, in the search shape |
| `POST /api/v1/kroger/coupons` | 1 | The digital coupons at one store, 24 per page, by department or text: savings (amount in cents or percent), terms, tags, where valid, clip-by and expiry dates |
| `POST /api/v1/kroger/suggestions` | 1 | Search box suggestions for a partial query |

## Which store priced it

This is the single most important rule of this skill.

- **search, product, category and deals** return the prices, promotions, stock and aisle of a store the site chooses for the request, given in `store` (`location_id`, `name`, `banner`, `division`, `store_number`, `address`). You cannot pick that store, it can change between calls, and it is often far from the shopper: in the captures a QFC search was priced at Mount Tabor, Portland, Oregon, and a Fred Meyer product at Pocatello, Idaho. Never present those prices as "the Fred Meyer price" or "the QFC price"; name the store.
- **prices** is the only endpoint priced at a store you choose. Get the `location_id` from `/kroger/stores` and send it as `store_id`; every item comes back with `priced_at` equal to that id.
- **coupons** and **suggestions** take a `store_id` too (coupons also take a `zip`, which picks the banner's nearest store).

## Workflow

1. **Pick the banner** from the user's words: Fred Meyer -> `fred_meyer`, QFC -> `qfc`, Kroger -> `kroger`.
2. **Find products:** `/kroger/search` with `query`, `/kroger/category` with a `/pl/` URL or `taxonomy_id`, or `/kroger/deals`. Each product has a 13-digit `upc`.
3. **Find the store:** `/kroger/stores` with the shopper's `zip` or a `query` such as `"Portland, OR"`. Use `stores[].location_id` (skip `type: "fuel_center"` entries for grocery prices).
4. **Price at that store:** `/kroger/prices` with `store_id` and up to 25 `upcs`. To compare stores, call it once per store with the same UPCs.
5. **One product in full:** `/kroger/product` with the `upc` (or the product `url`) for nutrition, ingredients and allergens.
6. **Savings:** `/kroger/coupons` with the same `store_id` (filter with `category` or `query`), and `/kroger/deals` for the week's digital deals.
7. **Monitoring:** poll `/kroger/prices` for a fixed set of stores and UPCs on a schedule and store `price`, `promo_price`, `promo_ends_at`, `stock_level` and the time per run; compare runs yourself. There is no price history.

### Pagination and sort

- **search, category and deals:** only the first page (up to 24 products) is available. `page` above 1 is refused with a `400` before any charge. There is no sort. `total` is the number of matches the site reports (it counts up to 1000). For more specific results narrow the query or open a category.
- **coupons:** real paging, `page` 1-50, 24 coupons per page; `has_more` says whether another page exists and `total_at_store` counts every coupon at the store before filters.
- **stores:** `limit` 1-50 (default 10), no paging.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars) |
| `banner` | string | `kroger` | `kroger`, `qfc` or `fred_meyer` |
| `page` | integer | 1 | Only 1 is accepted; above 1 is a `400`, not charged |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `product_url` | string | one of | Full or relative product URL on kroger.com, qfc.com or fredmeyer.com (`products[].url`, e.g. `/p/simple-truth-organic-lactose-free-2-reduced-fat-milk-half-gallon/0001111050438`). An absolute URL sets the banner |
| `upc` | string | one of | The product's UPC (`products[].upc`, or the digits at the end of a product URL) |
| `slug` | string | - | The readable part of the product URL. Optional with `upc` |
| `banner` | string | `kroger` | As on search |

### Prices (`/prices`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | required | A store's 8-digit `location_id` from `/stores` (e.g. `70500847`) |
| `upcs` | array of strings | required | 1 to 25 13-digit UPCs as the site writes them (`products[].upc`) |
| `banner` | string | from the id | Optional: read from the `store_id` prefix |

### Stores (`/stores`)

Send exactly one of `zip`, `query` or `store_id`.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `zip` | string | one of | A 5-digit US ZIP code |
| `query` | string | one of | A city or address as typed in the site's store finder (2-100 chars), e.g. `Portland, OR` |
| `store_id` | string | one of | One store by its 8-digit `location_id` |
| `banner` | string | `kroger` | Which banner's stores to list |
| `limit` | integer | 10 | Stores to return, 1-50 |
| `include_other_banners` | boolean | false | Also return nearby stores of other Kroger banners (for example Fred Meyer stores near a QFC search, or Fred Meyer Jewelers). Partner fuel stations are never returned |

### Category (`/category`)

Send `url` or `taxonomy_id`, not both.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | A category listing URL (`/pl/<name>/<id>`) on kroger.com, qfc.com or fredmeyer.com. The host sets the banner |
| `taxonomy_id` | string | one of | The digits at the end of a `/pl/` URL (e.g. `08190`). Category ids are shared across banners |
| `slug` | string | - | The name part of a `/pl/` URL (e.g. `Import-Beer`). Optional with `taxonomy_id`; without it `category.name` is null |
| `banner`, `page` | | | As on search |

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `banner` | string | `kroger` | As on search |
| `page` | integer | 1 | Only 1 is accepted |

### Coupons (`/coupons`)

Send `store_id` or `zip`, not both.

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | one of | A store's 8-digit `location_id` |
| `zip` | string | one of | A 5-digit ZIP: the banner's nearest store is used |
| `banner` | string | from the id | Optional with `store_id`; with `zip` it picks which banner's store |
| `page` | integer | 1 | 1-50, 24 coupons per page |
| `category` | string | - | One department from the response's `categories` list (`Dairy`, `Beverages`, `Snacks`, `Health`...) |
| `query` | string | - | Only coupons whose brand or text matches (2-100 chars) |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (2-100 chars) |
| `banner` | string | `kroger` | As on search |
| `store_id` | string | - | Optional: without it the banner's store nearest a representative ZIP is used (Kroger 45202 Cincinnati, QFC 98101 Seattle, Fred Meyer 97201 Portland) |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "coffee", "banner": "qfc"}'
```

Captured `data` (23 of 24 products trimmed):

```json
{
  "query": "coffee",
  "page": 1,
  "banner": "qfc",
  "store": {
    "location_id": "70500205",
    "name": "Mount Tabor",
    "banner": "qfc",
    "division": "705",
    "store_number": "00205",
    "address": { "line1": "5544 E Burnside St", "city": "Portland", "state": "OR", "zip": "97215" }
  },
  "total": 642,
  "count": 24,
  "products": [
    {
      "upc": "0081006334503",
      "name": "Death Wish Coffee Co® Power Surge Ground Coffee",
      "brand": "Death Wish Coffee",
      "url": "/p/death-wish-coffee-co-power-surge-ground-coffee/0081006334503",
      "image": "https://www.kroger.com/product/images/large/front/0081006334503",
      "images": [
        "https://www.kroger.com/product/images/xlarge/front/0081006334503",
        "https://www.kroger.com/product/images/xlarge/back/0081006334503"
      ],
      "price": 1699,
      "list_price": 1699,
      "promo_price": 1099,
      "promo_ends_at": "2026-11-18T04:59:59.999Z",
      "price_display": "$16.99",
      "unit_price_display": "$1.70/oz",
      "nfor": null,
      "nfor_price": null,
      "size": "10 oz",
      "in_stock": null,
      "stock_level": null,
      "is_snap_eligible": true,
      "dietary_info": ["Vegetarian", "Kosher", "Vegan", "Pescatarian"],
      "category": { "department": "Beverages", "commodity": "Coffee", "sub_commodity": "Ground Coffee" },
      "rating": {
        "average": 4.64,
        "count": 148,
        "distribution": { "1": 4, "2": 4, "3": 6, "4": 13, "5": 121 }
      }
    }
  ]
}
```

Read the price fields together:

- `price`, `list_price`, `promo_price` and `nfor_price` are integer cents; `price_display` is the site's own text. `promo_price` (with `promo_ends_at`, an ISO time) is the sale price: $10.99 against a regular $16.99 here.
- `nfor` / `nfor_price` is a multi-buy: `nfor: 2, nfor_price: 400` reads "2 for $4.00". Quote it as a multi-buy, not as the one-item price.
- `unit_price_display` is the site's price per unit (`$1.70/oz`): compare pack sizes with it.
- `in_stock` is `true` or `false` when the store has a stock record for the item and `null` when it has none; `stock_level` is `HIGH`, `LOW` or `TEMPORARILY_OUT_OF_STOCK`. Null means unknown, not out of stock.
- `rating` is the average, the count and the star distribution only. Review text is not available.
- `url` is relative: prefix the banner's site (`https://www.qfc.com`) to show it.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"upc": "0001111050438", "banner": "fred_meyer"}'
```

Captured `data` (description shortened; three images trimmed):

```json
{
  "upc": "0001111050438",
  "name": "Simple Truth Organic® Lactose Free 2% Reduced Fat Milk Half Gallon",
  "brand": "Simple Truth",
  "url": "/p/simple-truth-organic-lactose-free-2-reduced-fat-milk-half-gallon/0001111050438",
  "image": "https://www.kroger.com/product/images/large/front/0001111050438",
  "images": ["https://www.kroger.com/product/images/xlarge/back/0001111050438"],
  "price": 499,
  "list_price": 499,
  "promo_price": 399,
  "promo_ends_at": "2026-12-02T04:59:59.999Z",
  "price_display": "$4.99",
  "unit_price_display": "$0.08/fl oz",
  "nfor": null,
  "nfor_price": null,
  "size": "1/2 gal",
  "in_stock": true,
  "stock_level": "HIGH",
  "is_snap_eligible": true,
  "dietary_info": ["Kosher", "Lactose Free", "Pescatarian", "Vegetarian"],
  "category": { "department": "Natural & Organic", "commodity": "Dairy & Eggs", "sub_commodity": "Milk" },
  "rating": {
    "average": 3.12,
    "count": 17,
    "distribution": { "1": 5, "2": 2, "3": 1, "4": 4, "5": 5 }
  },
  "description": "Simple Truth Organic® Lactose Free 2% Reduced Fat Milk Half Gallon is a USDA organic delight. ...",
  "country_of_origin": "UNITED STATES",
  "temperature": "Refrigerated",
  "dimensions": { "height": "9.5 [in_i]", "width": "4.0 [in_i]", "length": "4.0 [in_i]" },
  "weight": "4.3 [lb_av]",
  "nutrition": null,
  "store_location": { "aisle": "DAIRY", "aisle_number": "100", "side": "R" },
  "breadcrumbs": ["Natural & Organic", "Dairy & Eggs", "Milk"],
  "banner": "fred_meyer",
  "store": {
    "location_id": "70100260",
    "name": "Pocatello",
    "banner": "fred_meyer",
    "division": "701",
    "store_number": "00260",
    "address": { "line1": "800 Yellowstone Ave", "city": "Pocatello", "state": "ID", "zip": "83201" }
  }
}
```

`nutrition` is null when the site shows no nutrition panel for the item (as here). When present it carries `serving_size`, `servings_per_container`, `allergens`, `ingredients` and `facts[]` (`name`, `value`, `unit`, `daily_value`). The $4.99 here is the Pocatello store's price, chosen by the site; the product endpoint cannot be pointed at another store.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "97201", "banner": "fred_meyer"}'
```

Captured `data` (8 of 10 stores trimmed; 40 of 43 departments trimmed):

```json
{
  "banner": "fred_meyer",
  "count": 10,
  "stores": [
    {
      "location_id": "70100360",
      "banner": "fred_meyer",
      "type": "store",
      "name": "Stadium",
      "store_number": "00360",
      "address": { "line1": "100 NW 20Th Pl", "city": "Portland", "state": "OR", "zip": "97209" },
      "coordinates": { "lat": 45.5239565, "lng": -122.6927962 },
      "phone": "(503) 273-2004",
      "timezone": "America/Los_Angeles",
      "hours": [{ "days": "Sun - Sat", "hours": "7:00 AM - 10:00 PM" }],
      "open_24_hours": false,
      "departments": [
        { "name": "Coffee Bar", "phone": null, "hours": [{ "days": "Sun - Sat", "hours": "7:00 AM - 9:00 PM" }] },
        { "name": "Pickup", "phone": "(503) 721-4101", "hours": null },
        { "name": "Deli", "phone": null, "hours": [{ "days": "Sun - Sat", "hours": "7:00 AM - 10:00 PM" }] }
      ],
      "has_pharmacy": true,
      "has_fuel_center": false,
      "pickup": true,
      "delivery": false,
      "distance_miles": 0.83
    },
    {
      "location_id": "70100004",
      "banner": "fred_meyer",
      "type": "fuel_center",
      "name": "Burlingame Fuel",
      "store_number": "00004",
      "address": { "line1": "8420 SW 24th Ave", "city": "Portland", "state": "OR", "zip": "97219" },
      "coordinates": { "lat": 45.463963, "lng": -122.701684 },
      "phone": null,
      "timezone": "America/Los_Angeles",
      "hours": [{ "days": "Sun - Sat", "hours": "24 Hours" }],
      "open_24_hours": false,
      "departments": [{ "name": "Gas Station", "phone": null, "hours": null }],
      "has_pharmacy": false,
      "has_fuel_center": true,
      "pickup": false,
      "delivery": false,
      "distance_miles": 3.47
    }
  ],
  "query": "97201"
}
```

`location_id` is the `store_id` for prices, coupons and suggestions. Fuel centers are their own entries (`type: "fuel_center"`), not linked to a store; fuel prices are not available. `distance_miles` is measured from the ZIP or place searched.

### Prices at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/prices \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "70500847", "upcs": ["0001111050438", "0081006334306", "0003600056535"]}'
```

Captured `data`:

```json
{
  "banner": "qfc",
  "store": {
    "location_id": "70500847",
    "name": "Harvard Market",
    "banner": "qfc",
    "address": { "line1": "1401 Broadway", "city": "Seattle", "state": "WA", "zip": "98122" }
  },
  "count": 3,
  "items": [
    {
      "upc": "0001111050438",
      "name": "Simple Truth Organic® Lactose Free 2% Reduced Fat Milk Half Gallon",
      "brand": "Simple Truth",
      "size": "1/2 gal",
      "url": "/p/simple-truth-organic-lactose-free-2-reduced-fat-milk-half-gallon/0001111050438",
      "image": "https://www.kroger.com/product/images/large/front/0001111050438",
      "price": 579,
      "promo_price": 399,
      "promo_ends_at": "2026-12-02T04:59:59.999Z",
      "on_sale": true,
      "price_display": "$5.79",
      "unit_price_display": "$0.09/fl oz",
      "in_stock": true,
      "stock_level": "LOW",
      "quantity": 5,
      "aisle": { "description": "DAIRY", "number": "100", "side": "L", "bay": "9", "shelf": "4" },
      "fulfillment": { "pickup": true, "delivery": true, "in_store": true, "ship": false },
      "priced_at": "70500847"
    },
    {
      "upc": "0081006334306",
      "name": "Death Wish Coffee Co.® Medium Roast Ground Coffee",
      "brand": "Death Wish Coffee",
      "size": "10 oz",
      "url": "/p/death-wish-coffee-co-medium-roast-ground-coffee/0081006334306",
      "image": "https://www.kroger.com/product/images/large/front/0081006334306",
      "price": 1699,
      "promo_price": 1099,
      "promo_ends_at": "2026-11-18T04:59:59.999Z",
      "on_sale": true,
      "price_display": "$16.99",
      "unit_price_display": "$1.70/oz",
      "in_stock": null,
      "stock_level": null,
      "quantity": null,
      "aisle": { "description": "AISLE 5", "number": "5", "side": "L", "bay": "33", "shelf": "3" },
      "fulfillment": { "pickup": true, "delivery": true, "in_store": true, "ship": false },
      "priced_at": "70500847"
    },
    {
      "upc": "0003600056535",
      "name": "Viva® Signature Cloth™ Paper Towels Double Rolls",
      "brand": "Viva",
      "size": "12 rolls",
      "url": "/p/viva-signature-cloth-paper-towels-double-rolls/0003600056535",
      "image": "https://www.kroger.com/product/images/large/front/0003600056535",
      "price": 2499,
      "promo_price": null,
      "promo_ends_at": null,
      "on_sale": false,
      "price_display": "$24.99",
      "unit_price_display": "$0.05/sq ft",
      "in_stock": false,
      "stock_level": "TEMPORARILY_OUT_OF_STOCK",
      "quantity": 0,
      "aisle": null,
      "fulfillment": { "pickup": false, "delivery": false, "in_store": false, "ship": false },
      "priced_at": "70500847"
    }
  ],
  "not_found": []
}
```

The same milk read $5.79 here at QFC Harvard Market, Seattle, and $4.99 at the Fred Meyer store the site chose for the product call above. `quantity` is the number the site reports as available at the store: an estimate, not a shelf count. `fulfillment.in_store: true` means the store sells the item, not that it is on the shelf. UPCs the site does not know are listed in `not_found` and are not an error.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"taxonomy_id": "08190", "slug": "Import-Beer", "banner": "qfc"}'
```

The captured answer opens with (then `products[]` in the search shape, e.g. Guinness Draught Stout at `price: 1349`, `promo_price: 1099`):

```json
{
  "banner": "qfc",
  "category": { "id": "08190", "name": "Import Beer", "url": "https://www.qfc.com/pl/Import-Beer/08190" },
  "page": 1,
  "store": {
    "location_id": "70500829",
    "name": "North Bend",
    "banner": "qfc",
    "division": "705",
    "store_number": "00829",
    "address": { "line1": "460 E North Bend Way", "city": "North Bend", "state": "WA", "zip": "98045" }
  },
  "total": 65,
  "count": 24
}
```

### Weekly digital deals

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"banner": "qfc"}'
```

The captured answer opens with (then `products[]` in the search shape):

```json
{
  "banner": "qfc",
  "deals_week": { "id": "WDDShopAllProduct26111700s", "ends_at": "2026-11-18T04:59:59.999Z" },
  "page": 1,
  "store": {
    "location_id": "70500847",
    "name": "Harvard Market",
    "banner": "qfc",
    "division": "705",
    "store_number": "00847",
    "address": { "line1": "1401 Broadway", "city": "Seattle", "state": "WA", "zip": "98122" }
  },
  "total": 306,
  "count": 24
}
```

`deals_week.ends_at` is the promotion end most deal items share; there is no start date. Items on a store promotion carry `promo_price` and `promo_ends_at` (Kellogg's Frosted Flakes 28.5 oz at `promo_price: 599` against `price: 799`). Items whose deal is a digital coupon show only the shelf price (Kroger shredded cheese at `price: 249`, `promo_price: null`): the deal price is in the coupon, tag `Weekly Digital Deals`, `savings.type: "price"` (below). The printed weekly ad circular is not available.

### Coupons

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/coupons \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "70100011"}'
```

Captured `data` (22 of 24 coupons and 28 of 32 categories trimmed; terms shortened):

```json
{
  "banner": "fred_meyer",
  "store": {
    "location_id": "70100011",
    "name": "Anchorage",
    "banner": "fred_meyer",
    "address": { "line1": "1000 E Northern Lights Blvd", "city": "Anchorage", "state": "AK", "zip": "99508" }
  },
  "page": 1,
  "page_size": 24,
  "count": 24,
  "total_at_store": 450,
  "has_more": true,
  "categories": ["Health", "Adult Beverage", "Personal Care", "Dairy"],
  "category": null,
  "query": null,
  "coupons": [
    {
      "id": "4250553",
      "brand": "Other",
      "title": "Save $30.00 When You Spend $75.00",
      "description": "$30 off Your First Pickup or Delivery Order of $75 or more",
      "details": "Valid now through November 17, 2026, when you spend $75 or more on pickup and delivery, where available. ...",
      "savings": { "type": "amount_off", "amount": 3000, "percent": null },
      "type": "standard",
      "min_quantity": 1,
      "categories": ["General"],
      "tags": ["Pickup & Delivery Only", "Expiring Soon"],
      "valid_for": ["delivery", "pickup"],
      "max_redemptions": 1,
      "starts_at": "2026-10-20",
      "clip_by": "2026-11-17",
      "expires_at": "2026-11-17",
      "image": "https://krogerws.softcoin.com/mediaCache/ecoupon_6073549.jpg?o=4250553&r=kroger"
    },
    {
      "id": "4259595",
      "brand": "Kroger Brand",
      "title": "$1.49",
      "description": "$1.49 Kroger Cheese",
      "details": "When You Buy ONE (1) Kroger Bars, Shreds or Slices (6-8 oz), Offer Valid at Select Markets. ...",
      "savings": { "type": "price", "amount": 149, "percent": null },
      "type": "standard",
      "min_quantity": 1,
      "categories": ["Dairy", "Pasta"],
      "tags": ["Weekly Digital Deals", "Expiring Soon"],
      "valid_for": ["pickup", "in_store", "delivery"],
      "max_redemptions": null,
      "starts_at": "2026-11-11",
      "clip_by": "2026-11-17",
      "expires_at": "2026-11-17",
      "image": "https://krogerws.softcoin.com/mediaCache/ecoupon_6100969.jpg?o=4259595&r=kroger"
    }
  ]
}
```

`savings.type` is `amount_off` (amount in cents off), `percent_off` (`percent`), `price` (the item costs `amount` cents with the coupon), `free_item` or `other` (points offers and the like: read `title` and `details`). Dates are `YYYY-MM-DD` as the site shows them. Coupons are listed only: nothing is clipped and no shopper account is used, so a coupon still has to be clipped by the shopper to apply.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/kroger/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "almond mi", "banner": "qfc"}'
```

Captured `data` (2 of 5 suggestions trimmed):

```json
{
  "query": "almond mi",
  "banner": "qfc",
  "store": { "location_id": "70500847", "name": null, "banner": "qfc", "address": null },
  "count": 5,
  "suggestions": [
    { "text": "almond milk", "type": "query" },
    { "text": "unsweetened almond milk", "type": "query" },
    { "text": "vanilla almond milk", "type": "query" }
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

def kroger(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/kroger/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. UPCs from a Fred Meyer search (2 credits)
found = kroger("search", {"query": "organic milk", "banner": "fred_meyer"})
upcs = [p["upc"] for p in found["products"][:10]]

# 2. Fred Meyer stores near a ZIP, grocery stores only (1 credit)
stores = kroger("stores", {"zip": "97201", "banner": "fred_meyer", "limit": 5})["stores"]
stores = [s for s in stores if s["type"] == "store"]

# 3. The same UPCs priced at each store (3 credits per store)
for s in stores:
    priced = kroger("prices", {"store_id": s["location_id"], "upcs": upcs})
    for item in priced["items"]:
        promo = item["promo_price"]
        print(s["name"], item["name"], item["price"] / 100, promo / 100 if promo else None, item["stock_level"])

# 4. Dairy coupons at the first store (1 credit)
coupons = kroger("coupons", {"store_id": stores[0]["location_id"], "category": "Dairy"})
for c in coupons["coupons"]:
    print(c["title"], c["savings"], c["expires_at"])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `fetched_at` is the ISO time the data was retrieved; nothing is cached, so it is the age of the data. Key `data` fields:

- **search** - `query`, `page`, `banner`, `store`, `total`, `count`, `products[]`.
- **product item (search, category, deals)** - `upc`, `name`, `brand`, `url`, `image`, `images[]`, `price`, `list_price`, `promo_price`, `promo_ends_at`, `price_display`, `unit_price_display`, `nfor`, `nfor_price`, `size`, `in_stock`, `stock_level`, `is_snap_eligible`, `dietary_info[]`, `category` {`department`, `commodity`, `sub_commodity`}, `rating` {`average`, `count`, `distribution`}.
- **product** - the item fields plus `description`, `country_of_origin`, `temperature`, `dimensions`, `weight`, `nutrition` (null or {`serving_size`, `servings_per_container`, `allergens`, `ingredients`, `facts[]`}), `store_location` {`aisle`, `aisle_number`, `side`}, `breadcrumbs[]`, `banner`, `store`.
- **prices** - `banner`, `store`, `count`, `items[]` {`upc`, `name`, `brand`, `size`, `url`, `image`, `price`, `promo_price`, `promo_ends_at`, `on_sale`, `price_display`, `unit_price_display`, `in_stock`, `stock_level`, `quantity`, `aisle` {`description`, `number`, `side`, `bay`, `shelf`}, `fulfillment` {`pickup`, `delivery`, `in_store`, `ship`}, `priced_at`}, `not_found[]`.
- **stores** - `banner`, `query`, `count`, `stores[]` {`location_id`, `banner`, `type`, `name`, `store_number`, `address`, `coordinates`, `phone`, `timezone`, `hours[]`, `open_24_hours`, `departments[]`, `has_pharmacy`, `has_fuel_center`, `pickup`, `delivery`, `distance_miles`}.
- **category** - `banner`, `category` {`id`, `name`, `url`}, `page`, `store`, `total`, `count`, `products[]`.
- **deals** - `banner`, `deals_week` {`id`, `ends_at`}, `page`, `store`, `total`, `count`, `products[]`.
- **coupons** - `banner`, `store`, `page`, `page_size`, `count`, `total_at_store`, `has_more`, `categories[]`, `category`, `query`, `coupons[]` {`id`, `brand`, `title`, `description`, `details`, `savings` {`type`, `amount`, `percent`}, `type`, `min_quantity`, `categories`, `tags`, `valid_for`, `max_redemptions`, `starts_at`, `clip_by`, `expires_at`, `image`}.
- **suggestions** - `query`, `banner`, `store`, `count`, `suggestions[]` {`text`, `type`}.

## Guardrails

- Cents: every price and every coupon `amount` is an integer number of cents. Divide by 100 before showing dollars, or quote `price_display`.
- Store scope: always name the store a price came from (`store.name` and `store.location_id`, or `priced_at`). Prices on search, product, category and deals belong to a store the site chose; only `/prices` is priced at a store you chose. Never call a site-chosen store's price "the QFC price" or "the Fred Meyer price".
- Online store prices, not register prices: these are the prices the site shows for a store, which can differ from what rings up at checkout.
- Stock: `in_stock: null` means the store has no stock record, not that it is out of stock. `quantity` is an estimate. Never promise an item is on the shelf.
- Promotions: `promo_price` applies until `promo_ends_at`; `nfor` deals are multi-buys. A digital-coupon deal needs the shopper to clip the coupon; say so.
- Ratings are average, count and distribution only. There is no review text: never invent review quotes.
- Banners: only `kroger`, `qfc` and `fred_meyer` are served. Do not claim Ralphs, King Soopers, Fry's, Smith's, Harris Teeter or other Kroger banners are covered.
- Not covered: review text, fuel prices (fuel center locations only), the printed weekly ad circular, coupon clipping, cart and checkout, pharmacy data, price history, more than the first page of search, category or deals results, and sorting.
- Kroger's website terms (Website & App Terms, updated September 9, 2026), which cover fredmeyer.com and qfc.com, license the sites for "personal, non-commercial use" and prohibit using "any automated means, including bots, crawlers, scrapers, or data-mining tools" to collect or monitor information from them. This is not legal advice; the user is responsible for checking the current terms for their use case.
- Never fabricate prices, UPCs, store ids, stock, coupons or nutrition. Only return what the API returned, with the `upc` and the store.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: `page` above 1 on search, category or deals; a banner other than `kroger`, `qfc` or `fred_meyer`; a banner that contradicts the `store_id` prefix or a URL host; a `store_id` that is not 8 digits; `upcs` empty, over 25, or not 13 digits; stores without exactly one of `zip`, `query` or `store_id`; coupons with both or neither of `store_id` and `zip`; category with both or neither of `url` and `taxonomy_id`; a ZIP that is not 5 digits.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means an unknown UPC on product or an unknown `store_id`. Not-founds are charged at the endpoint's cost: take UPCs and store ids from a previous answer rather than guessing them. Unknown UPCs on `/prices` are listed in `not_found` instead.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data).
- `502` means Kroger data was temporarily unavailable or the answer was unusable. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Kroger is busy: wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.54.0
npm install scavio@0.55.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.kroger.search({ query: "coffee", banner: "qfc" });
const { data: item } = await scavio.kroger.product({ upc: "0001111050438", banner: "fred_meyer" });
const { data: stores } = await scavio.kroger.stores({ zip: "97201", banner: "fred_meyer" });
const { data: priced } = await scavio.kroger.prices({ store_id: "70500847", upcs: ["0001111050438"] });
const { data: beer } = await scavio.kroger.category({ taxonomy_id: "08190", slug: "Import-Beer", banner: "qfc" });
const { data: deals } = await scavio.kroger.deals({ banner: "qfc" });
const { data: coupons } = await scavio.kroger.coupons({ store_id: "70100011", category: "Dairy" });
const { data: hints } = await scavio.kroger.suggestions({ query: "almond mi", banner: "qfc" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.kroger.search(...)`, `client.kroger.product(...)`, `client.kroger.prices(...)`, `client.kroger.stores(...)`, `client.kroger.category(...)`, `client.kroger.deals(...)`, `client.kroger.coupons(...)` and `client.kroger.suggestions(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all eight endpoints as tools: `search_kroger`, `get_kroger_product`, `get_kroger_prices`, `find_kroger_stores`, `get_kroger_category`, `get_kroger_deals`, `get_kroger_coupons` and `get_kroger_suggestions`. Kroger is opt-in: add `kroger` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.52.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,kroger"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/kroger-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [product](https://scavio.dev/docs/kroger-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [prices](https://scavio.dev/docs/kroger-prices?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [stores](https://scavio.dev/docs/kroger-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [category](https://scavio.dev/docs/kroger-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [deals](https://scavio.dev/docs/kroger-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [coupons](https://scavio.dev/docs/kroger-coupons?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data), [suggestions](https://scavio.dev/docs/kroger-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data). Overview: [Kroger API](https://scavio.dev/kroger-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=kroger-grocery-data).
