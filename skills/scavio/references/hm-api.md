# H&M API - Prices by Country, Product Data, Stock by Size, Stores

Read H&M's own online store (hm.com) in 47 countries: keyword search, one article in full, online stock per size, H&M stores with opening hours, category grids, the sale grid, new arrivals, search suggestions and where an article is made. All 9 endpoints return structured JSON. Product costs 2 credits per call; the other 8 cost 1.

**The job this skill is for: H&M prices by country.** One article's price, sale price, member price and online stock by size in each H&M market, in that market's currency. **Article codes are global**: the same 10-digit code (7-digit product code + 3-digit colour) names the same colourway in every market. So "this item in every country" is one code and one call per `country`.

Captured on 2026-11-15, article `1372161001` (the women's bow-detail blazer dress) from the search endpoint in each market:

| `country` | `language` | `title` | `price` | `regular_price` | `sale_price` | `member_price` | `currency` |
|---|---|---|---|---|---|---|---|
| `gb` | `en` | Bow-detail blazer dress | 64.99 | 64.99 | null | null | GBP |
| `de` | `de` | Blazer-Kleid mit Zierschleife | 69.99 | 69.99 | null | null | EUR |
| `fr` | `fr` | Robe blazer avec nœud | 59.99 | 59.99 | null | null | EUR |
| `ch` | `it` | Abito a blazer con fiocco decorativo | 84.95 | 84.95 | null | null | CHF |
| `se` | `sv` | Kavajklänning med rosett | 799 | 799 | null | null | SEK |
| `pl` | `pl` | Żakietowa sukienka z kokardą | 299.99 | 299.99 | null | null | PLN |
| `ca` | `fr` | Robe veston avec boucle | 99 | 99 | null | 78.99 | CAD |
| `mx` | `es` | Vestido blazer con moño | 1049 | 1499 | 1049 | null | MXN |

The same article was on sale in Mexico, carried a member price in Canada and was at its regular price in the six other markets on the same day. Prices are never converted: to compare countries, convert explicitly and state the rate and its date.

**The price fields.** `price` is what a non-member pays now (`sale_price` when on sale, else `regular_price`). `sale_price` is a markdown. `member_price` is H&M's member price as H&M displays it to signed-in members; we do not sign in, so it is the displayed figure, not a checkout price. `discount_percent` is H&M's own markdown figure. `prior_price` is the earlier price H&M shows next to a markdown in the EU (captured on `pl`: `price` 19.99, `regular_price` 29.99, `prior_price` 29.99 PLN). `price_disclosure` (product only) is H&M's own note where it shows one, e.g. `"Sale price in effect for 90+ days"`.

**Price history.** H&M shows none and none is returned. To build one, call search or product on a schedule and store each reading with its time, country and currency. H&M's US Black Friday page says Black Friday 2026 starts at hm.com on November 26 and in stores on November 27.

H&M has no public product data API. H&M Group runs integration portals for its business partners behind a sign-in; they are not open to developers who want store prices or stock.

See also: for Nordstrom fashion prices, markdowns and per-size stock use `nordstrom-product-data`; for second-hand fashion use `vinted-api`; for Macy's, Kohl's and JCPenney use `macys-product-data`, `kohls-product-data` and `jcpenney-product-data`; for the cross-merchant view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Compare one H&M item's price across countries, each in its own currency (one article code, one call per country)
- Check whether an H&M item is on sale in a market, its sale price, discount, member price or EU prior price
- Track H&M prices or markdowns over time (Black Friday, end-of-season sales) by polling and storing prices
- Check which sizes of an H&M item are in stock online in a market, per colour, with H&M's low-stock flag
- Search H&M's catalog by keyword in a market, sorted by relevance, newest or price, filtered by colour, size, material, fit, product type, department or on sale
- Read one H&M article in full: description, composition, materials, care, fit and length attributes, every colourway with its own prices, rating and the latest reviews with fit feedback
- List H&M stores in a country, a city, a postal code or around a point, with opening hours, departments and campaigns; list one store's assortment
- Browse an H&M category, the sale grid or new arrivals of a department (women, men, kids, baby, home)
- Find where an H&M article is made: countries of production, suppliers and factories as H&M publishes them

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=hm-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=hm-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 50 calls on every endpoint here except product, which costs 2 (25 product calls).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures search, stock, category, deals, new arrivals, suggestions and production took 0.7 to 9.5 seconds, stores 8.6 seconds, and **product 3.7 to 75 seconds**. Set a client timeout of at least 180 seconds and do not fire many calls at once (a busy moment answers `503` with `Retry-After`).

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/hm/search` | all 47 | 1 | Items for a keyword (or an article or product code), with prices, colours, sizes, facets and totals |
| `POST /api/v1/hm/product` | 38 | 2 | One article in full by `article_code` or `url`: composition, every colourway's prices, online stock per size, rating, the latest reviews |
| `POST /api/v1/hm/stock` | all 47 | 1 | Online stock per size for every colour of a product |
| `POST /api/v1/hm/stores` | 46 | 1 | H&M stores of a country with address, coordinates, phone, opening hours, departments |
| `POST /api/v1/hm/category` | all 47 | 1 | One category grid by H&M's category id (the same ids in every market) |
| `POST /api/v1/hm/deals` | all 47 | 1 | The sale grid of a department: every marked-down item |
| `POST /api/v1/hm/new-arrivals` | all 47 | 1 | The new-arrivals grid of a department |
| `POST /api/v1/hm/suggestions` | all 47 | 1 | Search suggestions for what a shopper has typed |
| `POST /api/v1/hm/production` | all 47 | 1 | Countries of production, suppliers and factories for one article |

## Markets

Every endpoint takes `country` (lowercase ISO-2, default `us`) and, except stores and production, `language` (default the market's first). Titles, descriptions, colours and facet values come back in that language and prices in the market's currency, never converted. Every `data` echoes `country`, `language`, `currency`, `locale` and `store`.

| `country` | Languages | Currency |
|---|---|---|
| `us` | `en` | USD |
| `ca` | `en`, `fr` | CAD |
| `mx` | `es` | MXN |
| `gb` | `en` | GBP |
| `ie` | `en` | EUR |
| `de`, `at` | `de` | EUR |
| `ch` | `de`, `fr`, `it` | CHF |
| `fr` | `fr` | EUR |
| `be` | `nl`, `fr` | EUR |
| `nl` | `nl` | EUR |
| `it` | `it` | EUR |
| `es` | `es` | EUR |
| `pt` | `pt` | EUR |
| `se` | `sv` | SEK |
| `fi` | `fi`, `sv` | EUR |
| `dk` | `da` | DKK |
| `no` | `no` | NOK |
| `pl` | `pl` | PLN |
| `cz` | `cs` | CZK |
| `sk` | `sk` | EUR |
| `hu` | `hu` | HUF |
| `ro` | `ro` | RON |
| `bg` | `bg` | EUR |
| `gr` | `el` | EUR |
| `rs` | `sr` | RSD |
| `tr` | `tr` | TRY |
| `ua` | `uk` | UAH |
| `il` | `he` | ILS |
| `hk`, `mo` | `zh`, `en` | HKD |
| `tw` | `zh`, `en` | TWD |
| `jp` | `ja` | JPY |
| `kr` | `ko` | KRW |
| `in` | `en` | INR |
| `my` | `en` | MYR |
| `ph` | `en` | PHP |
| `sg` | `en` | SGD |
| `vn` | `vi` | VND |
| `au` | `en` | AUD |
| `hr`, `cy`, `ee`, `lv`, `lt`, `lu`, `si` | `en` | EUR (H&M's shared English EUR store) |

- Search, stock, category, deals, new arrivals, suggestions and production: all 47. Product: 38 (not `mo`, `tw` or the 7 shared-store countries; use search or stock there, which carry prices, colours and sizes). Stores: 46 (not `mo`: H&M lists no stores there).
- `hr`, `cy`, `ee`, `lv`, `lt`, `lu` and `si` are served by H&M's shared English EUR store: the answer says `"store": "eu"`, and all seven get the same catalog and prices.
- Countries where H&M runs a separate site (`ae`, `eg`, `id`, `th`, `br`, `cn`), countries with no H&M online store (`al`, `az`, `ba`, `by`, `cl`, `co`, `cr`, `ge`, `is`, `kh`, `kz`, `mk`, `nz`, `pe`, `xk`, `za`), `ru`, and `uk` (use `gb`) answer `400` before anything is charged.
- Assortments differ by market: an article sold in one market can be missing in another (product answers `404`, search returns no item with that code).

## Workflow

1. **One item, every country:** take the 10-digit `article_code` (from any answer, or from a link: `productpage.<article code>.html`). For each market call `/search` with `query` set to the code (1 credit) and keep the item whose `article_code` equals it; or call `/product` (2 credits, slower) for the full record. Store `price`, `regular_price`, `sale_price`, `member_price`, `prior_price`, `currency` and the time per market.
2. **Is it on sale:** `sale_price` is set, with `discount_percent`; in the EU `prior_price` shows the earlier price H&M displays. Product adds `price_disclosure` where H&M shows one.
3. **Sizes in stock online:** `/stock` with `article_code` or the 7-digit `product_code` (every colour in one call, 1 credit). `few_left` is H&M's low-stock flag. This is online stock, not store stock.
4. **Price tracking:** poll search by code (or product) on a schedule and store each reading. There is no price history endpoint.
5. **Browse:** `/search` with `query`, `/category` with a category id, `/deals` or `/new-arrivals` with `department`. Read `facets` from the first answer, then filter with those exact `value`s in the same market and language.
6. **A store's assortment:** `/stores` for the country (or a city, postal code or lat / lng), then `/search` with `store` set to a `store_code` to list only items in that store's assortment. Per-size stock in a store is not available.
7. **Where it is made:** `/production` with the `article_code`: the same answer in every market.

## Parameters

### Shared

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `us` | See Markets |
| `language` | string | the market's first | One of the market's languages (not on stores or production) |
| `page` | integer | 1 | 1-based, up to 200 (stores up to 100) |
| `page_size` | integer | 36 | 1 to 72 on grids; 1 to 100 on stores (default 20) |
| `sort` | string | `relevance` | `relevance`, `newest`, `price_asc` or `price_desc` (search, category, deals, new arrivals) |
| `color` | string or array | none | Values of the `color` facet of an earlier answer in the same market (`black_000000` on `us`, `schwarz_000000` on `de`); up to 10, ORed |
| `size` | string or array | none | Values of the `size` facet (`womenswear;NO_FORMAT[Numeric];8`) |
| `material` | string or array | none | Values of the `material` facet, in the market's language (`Cotton`, `Baumwolle`) |
| `fit` | string or array | none | Values of the `fit` facet (`Slim fit`, `Loose fit`) |
| `product_type` | string or array | none | Values of the `product_type` facet (`Jeans`) |
| `on_sale` | boolean | false | Only marked-down items (search, category, new arrivals; deals is the sale already) |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords, 1-200 chars, any language; an article or product code finds that item |
| `department` | string | none | `women`, `men`, `kids`, `baby` or `home` |
| `store` | string | none | A `store_code` from `/stores` (`US0098`): only items in that store's assortment |

### Product (`/product`) and production (`/production`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `article_code` | string | one of | 10 digits (`1310382004`) |
| `url` | string | one of | An hm.com product link (`https://www2.hm.com/<locale>/productpage.<article code>.html`); its market is used unless `country` is sent |

### Stock (`/stock`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `article_code` | string | one of | 10 digits |
| `product_code` | string | one of | 7 digits (the first 7 of an article code, `1310382`) |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `city` | string | none | Stores whose city or address contains this (case and accents ignored) |
| `postal_code` | string | none | Stores whose postal code starts with this |
| `lat` / `lng` | number | none | Stores within `radius_km`, nearest first, with `distance_km` |
| `radius_km` | number | 25 | 0.1 to 1000 |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | required | An H&M category id, the same in every market: `ladies_dresses`, `ladies_tops`, `ladies_jeans`, `ladies_knitwear`, `men_jeans`, `men_hoodiessweatshirts`, `men_tshirtstanks`, `kids_all`, `ladies_all`, `men_all`, or `items[].category` of any answer |

### Deals (`/deals`) and new arrivals (`/new-arrivals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `department` | string | `women` | `women`, `men`, `kids`, `baby` or `home` |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far, 1-100 chars |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "jeans"}'
```

Captured `data` (US, 2026-11-15; 1 of 36 items, 2 of 5 facets and 2 of 6 departments shown, lists trimmed):

```json
{
  "query": "jeans",
  "items": [
    {
      "article_code": "1359271004",
      "product_code": "1359271",
      "title": "Barrel-Leg High-Waist Jeans",
      "brand": "H&M",
      "url": "https://www2.hm.com/en_us/productpage.1359271004.html",
      "price": 49.99,
      "regular_price": 49.99,
      "sale_price": null,
      "member_price": 39.99,
      "discount_percent": null,
      "prior_price": null,
      "currency": "USD",
      "promo_text": null,
      "promo_terms": null,
      "multipack": null,
      "color": "Cream",
      "colors": [
        {"article_code": "1359271004", "name": "Cream", "hex": "#F0EEED"},
        {"article_code": "1359271001", "name": "Dark brown", "hex": "#3D3B3D"}
      ],
      "sizes": [
        {"size_code": "1359271004002", "label": "2", "in_stock": true},
        {"size_code": "1359271004003", "label": "4", "in_stock": true}
      ],
      "in_stock": true,
      "coming_soon": false,
      "new_arrival": false,
      "markers": [],
      "category": "ladies_jeans_barrel",
      "image": "https://image.hm.com/assets/hm/53/50/53504aa4e9919677e29bf2fc087a5380395c99ce.jpg",
      "model_image": "https://image.hm.com/assets/hm/28/64/28646d84584153bd69183167a2cb3989ba42b455.jpg"
    }
  ],
  "count": 36,
  "total": 1329,
  "page": 1,
  "page_size": 36,
  "total_pages": 37,
  "sort": "relevance",
  "sorts_offered": ["relevance", "newest", "price_asc", "price_desc"],
  "filters": {},
  "facets": [
    {"filter": "color", "name": "ColorWithNames", "values": [{"value": "beige_f5f5dc", "label": "beige", "count": 31, "hex": "#F5F5DC"}]},
    {"filter": "size", "name": "Size", "values": [{"value": "womenswear;NO_FORMAT[Numeric];0", "label": "0", "count": 191}]}
  ],
  "on_sale_count": 60,
  "price_range": {"min": 9.99, "max": 269},
  "department": null,
  "store_code": null,
  "departments": [
    {"department": "women", "id": "ladies_all", "label": "Women", "count": 720},
    {"department": "men", "id": "men_all", "label": "Men", "count": 169}
  ],
  "did_you_mean": [],
  "related_searches": [],
  "country": "us",
  "language": "en",
  "currency": "USD",
  "locale": "en_us",
  "store": "us",
  "notes": [
    "member_price is H&M's member (club) price, shown to signed-in H&M members; price is what a non-member pays now (sale_price when on sale, else regular_price).",
    "sizes[].in_stock is online stock (not store stock)."
  ]
}
```

The facets are `color`, `size`, `material`, `fit` and `product_type`; pass a facet `value` back as that filter.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"article_code": "1310382004"}'
```

Captured `data` (US, 2026-11-15; lists trimmed to 2, 2 of 10 reviews shown):

```json
{
  "article_code": "1310382004",
  "product_code": "1310382",
  "title": "Bow-Detail One-Shoulder Top",
  "brand": "H&M",
  "category": "Peplum",
  "category_code": "ladies_tops_peplum",
  "breadcrumbs": [
    {"name": "Women", "url": "https://www2.hm.com/en_us/women.html"},
    {"name": "Tops & T-Shirts", "url": "https://www2.hm.com/en_us/women/products/tops.html"}
  ],
  "url": "https://www2.hm.com/en_us/productpage.1310382004.html",
  "color": "White/black",
  "description": "Fitted, one-shoulder top in woven fabric with an asymmetric neckline. Large bow on one shoulder, concealed zipper at one side with hook-and-eye fastener, and shaping darts at waist. Flared peplum.",
  "composition": [
    {"part": "Shell", "materials": [{"name": "Polyester", "percent": 100}]},
    {"part": "Details", "materials": [{"name": "Polyester", "percent": 95}, {"name": "Spandex", "percent": 5}]}
  ],
  "materials": [
    {"name": "Spandex", "description": "Elastane is an elastic synthetic fibre made from oil (a fossil resource)."}
  ],
  "care": ["Only non-chlorine bleach when needed", "Line dry"],
  "attributes": {"weight": ["150 g"], "length": ["Regular length"], "rise": ["Low waist"], "sleeve_length": ["Sleeveless"], "fit": ["Slim fit"], "style": ["One-shoulder", "Peplum"], "neckline": ["Asymmetric Neckline"], "imported": ["Yes"]},
  "price": 29.99,
  "regular_price": 29.99,
  "sale_price": null,
  "member_price": 23.99,
  "discount_percent": null,
  "price_disclosure": null,
  "currency": "USD",
  "colors": [
    {"article_code": "1310382001", "name": "Dark green", "rgb": "#383F3D", "price": 29.99, "regular_price": 29.99, "sale_price": null, "member_price": null, "discount_percent": null, "price_disclosure": null, "url": "https://www2.hm.com/en_us/productpage.1310382001.html", "image": "https://image.hm.com/assets/hm/19/f7/19f7a51b4cc20700f0641e6359af0fa3a92020ef.jpg"},
    {"article_code": "1310382002", "name": "Red", "rgb": "#B91623", "price": 17.99, "regular_price": 29.99, "sale_price": 17.99, "member_price": null, "discount_percent": 40, "price_disclosure": "Sale price in effect for 90+ days", "url": "https://www2.hm.com/en_us/productpage.1310382002.html", "image": "https://image.hm.com/assets/hm/71/51/7151b2a57b03e505cce2f8da8e1cb542909af41f.jpg"}
  ],
  "sizes": [
    {"size_code": "1310382004002", "label": "XS", "in_stock": true, "few_left": false},
    {"size_code": "1310382004003", "label": "S", "in_stock": true, "few_left": false}
  ],
  "new_arrival": true,
  "coming_soon": false,
  "sold_in_stores": true,
  "images": [
    {"url": "https://image.hm.com/assets/hm/2c/01/2c013149f77f0ee2f1ac24941214bffd9fbe8756.jpg", "type": "LOOKBOOK"}
  ],
  "rating": {"average": 4.4, "count": 22},
  "reviews": [
    {"rating": 5, "text": "Top was very nice and high quality, fit was TTS but if you have a bigger bust I recommend you size up. This was a great Christmas outfit.", "date": "2025-11-04T02:43:20.000Z", "fit": []},
    {"rating": 3, "text": "Runs super large, usually M but shouldve gotten the small, bow looks really nice. Didnot return but got it altered", "date": "2025-12-23T16:19:10.000Z", "fit": [{"label": "True to Size", "value": "Runs Large"}, {"label": "Length", "value": "True to Size"}]}
  ],
  "country": "us",
  "language": "en",
  "locale": "en_us",
  "store": "us",
  "notes": [
    "member_price is H&M's member (club) price, shown to signed-in H&M members; price is what a non-member pays now (sale_price when on sale, else regular_price).",
    "sizes[].in_stock / few_left are online stock (not store stock).",
    "reviews are the latest reviews H&M shows on the product page (up to 10; H&M publishes no full review list without a session), with each reviewer's fit feedback; reviewer names are left out. rating is the product's average and count."
  ]
}
```

Prices are per colourway: in this capture the red colourway was on sale at 17.99 while the others were 29.99. `rating.count` (22) is the product's total; `reviews` holds at most the 10 latest.

### Stock

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/stock \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"article_code": "1310382004"}'
```

Captured `data` (US, 2026-11-15; 1 of 5 colours, 2 of 5 sizes shown):

```json
{
  "product_code": "1310382",
  "article_code": "1310382004",
  "title": "Bow-Detail One-Shoulder Top",
  "colors": [
    {
      "article_code": "1310382004",
      "name": "White/black",
      "sizes": [
        {"size_code": "1310382004002", "label": "XS", "in_stock": true, "few_left": false},
        {"size_code": "1310382004003", "label": "S", "in_stock": true, "few_left": false}
      ]
    }
  ],
  "sizes_total": 31,
  "sizes_in_stock": 10,
  "country": "us",
  "language": "en",
  "currency": "USD",
  "locale": "en_us",
  "store": "us",
  "notes": [
    "Online stock, not store stock (H&M publishes no per-size store stock).",
    "few_left is H&M's low-stock flag for that size."
  ]
}
```

On `mo`, `tw` and the shared EU store, stock comes from the listing and `few_left` is `null`.

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "us", "city": "New York"}'
```

Captured `data` (US, 2026-11-15; 1 of 10 stores, 2 of 7 days, 1 of 4 departments shown):

```json
{
  "stores": [
    {
      "store_code": "US0098",
      "name": "5th Ave at 18th Street",
      "status": "open",
      "store_class": "Flagship",
      "address": "111 5th Ave",
      "city": "New York City",
      "state": "New York",
      "postal_code": "10003",
      "country": "US",
      "lat": 40.73857149,
      "lng": -73.99152786,
      "phone": "+1-855-466-7467",
      "opening_hours": [
        {"day": "monday", "open": "10:00", "close": "21:00"},
        {"day": "sunday", "open": "11:00", "close": "20:00"}
      ],
      "opening_hour_exceptions": [],
      "departments": [
        {"name": "Ladies", "concepts": ["H&M Womenswear", "H&M Denim", "H&M Tailoring", "Womens Accessories", "H&M Edition", "H&M Move", "Womens Shoes"]}
      ],
      "campaigns": []
    }
  ],
  "count": 10,
  "total": 10,
  "country_total": 478,
  "page": 1,
  "page_size": 20,
  "total_pages": 1,
  "filters": {"city": "New York"},
  "country": "us",
  "language": "en",
  "currency": "USD",
  "locale": "en_us",
  "store": "us",
  "notes": ["Pass a store_code as search store to list that store's assortment. Store names and addresses come in the country's language."]
}
```

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "ladies_dresses", "country": "gb"}'
```

Captured `data` (UK, 2026-11-15; grid fields only, items have the search item shape):

```json
{
  "category": "ladies_dresses",
  "count": 36,
  "total": 3440,
  "page": 1,
  "page_size": 36,
  "total_pages": 96,
  "sort": "relevance",
  "sorts_offered": ["relevance", "newest", "price_asc", "price_desc"],
  "filters": {},
  "on_sale_count": 717,
  "price_range": {"min": 4, "max": 549.99},
  "country": "gb",
  "language": "en",
  "currency": "GBP",
  "locale": "en_gb",
  "store": "gb"
}
```

A category returns everything H&M files under that id, which can be more than the site's curated page; items carry their own, more specific `category` (here the first item was `ladies_occasion_partywear_dresses`).

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "gb", "department": "men"}'
```

Captured `data` (UK men, 2026-11-15; 1 of 36 items shown, `sizes` trimmed; `sorts_offered`, `filters`, `facets`, `notes` and the `language` / `locale` / `store` echo dropped):

```json
{
  "department": "men",
  "items": [
    {
      "article_code": "1285527001",
      "product_code": "1285527",
      "title": "2-pack sports trunks with DryMove™",
      "brand": "H&M",
      "url": "https://www2.hm.com/en_gb/productpage.1285527001.html",
      "price": 10,
      "regular_price": 19.99,
      "sale_price": 10,
      "member_price": null,
      "discount_percent": 50,
      "prior_price": null,
      "currency": "GBP",
      "promo_text": null,
      "promo_terms": null,
      "multipack": {"quantity": 2, "unit_price": 5},
      "color": "Black",
      "colors": [{"article_code": "1285527001", "name": "Black", "hex": "#272627"}, {"article_code": "1285527004", "name": "Beige", "hex": "#8C867E"}],
      "sizes": [{"size_code": "1285527001002", "label": "S", "in_stock": false}, {"size_code": "1285527001003", "label": "M", "in_stock": true}],
      "in_stock": true,
      "coming_soon": false,
      "new_arrival": false,
      "markers": ["H&M Move"],
      "category": "sportswear_men_clothing_socks",
      "image": "https://image.hm.com/assets/hm/6f/e0/6fe01d42afc290c5ee53cae974058cf053a88a99.jpg",
      "model_image": "https://image.hm.com/assets/hm/6f/e0/6fe01d42afc290c5ee53cae974058cf053a88a99.jpg"
    }
  ],
  "count": 36,
  "total": 414,
  "page": 1,
  "page_size": 36,
  "total_pages": 12,
  "sort": "relevance",
  "on_sale_count": 414,
  "price_range": {"min": 3, "max": 179},
  "country": "gb",
  "currency": "GBP"
}
```

H&M runs sales in seasons. A market with no sale running answers an empty grid (`total: 0`, a note says so) and the call is charged as normal: on 2026-11-15, 25 of the 47 markets had an empty women's sale grid.

### New arrivals

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/new-arrivals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"country": "se"}'
```

Captured on `se` (Swedish, women by default, 2026-11-15): `total` 1733, `price_range` {`min`: 39.99, `max`: 5490} SEK, first item `1363167003` "Ribbstickad topp med spetskant" at 179 SEK, colour `Svart`. Items have the search item shape, in Swedish.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "hoodie"}'
```

Captured `data` (US, 2026-11-15; 3 of 5 shown):

```json
{
  "query": "hoodie",
  "suggestions": [
    {"text": "hoodie", "type": "query", "url": null},
    {"text": "hoodie men", "type": "query", "url": null},
    {"text": "hoodie women", "type": "query", "url": null}
  ],
  "count": 5,
  "country": "us",
  "language": "en",
  "currency": "USD",
  "locale": "en_us",
  "store": "us"
}
```

### Production

```bash
curl -X POST https://api.scavio.dev/api/v1/hm/production \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"article_code": "1310382004"}'
```

Captured `data` (2026-11-15):

```json
{
  "article_code": "1310382004",
  "product_code": "1310382",
  "production_countries": ["Indonesia"],
  "countries": [
    {
      "country": "Indonesia",
      "suppliers": [
        {
          "supplier_id": "108363",
          "name": "D & J TRADING CO.,LTD",
          "factories": [{"factory_id": "108295", "name": "PT. Doo San Jaya Sukabumi", "city": "Sukabumi", "workers": "3001-3500"}]
        }
      ]
    }
  ],
  "country": "us",
  "language": "en",
  "currency": "USD",
  "locale": "en_us",
  "store": "us",
  "notes": ["H&M's own supplier disclosure for this article: the same in every market. Factory street addresses and contacts are left out (city only)."]
}
```

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def hm(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/hm/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    if r.status_code == 404:
        return None  # not sold in that market (charged)
    r.raise_for_status()
    return r.json()["data"]

ARTICLE = "1372161001"  # article codes are the same in every market
MARKETS = [("gb", "en"), ("de", "de"), ("fr", "fr"), ("se", "sv"), ("pl", "pl"), ("ca", "fr"), ("mx", "es")]

captured_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
rows = []
for cc, lang in MARKETS:  # 1 credit per market
    d = hm("search", {"query": ARTICLE, "country": cc, "language": lang})
    item = next((i for i in (d or {}).get("items", []) if i["article_code"] == ARTICLE), None)
    if item is None:
        print(cc, "not listed")
        continue
    rows.append({"country": cc, "currency": item["currency"], "price": item["price"],
                 "regular_price": item["regular_price"], "sale_price": item["sale_price"],
                 "member_price": item["member_price"]})

for r in rows:
    print(captured_at, r["country"], r["price"], r["currency"],
          "sale" if r["sale_price"] else "", "member " + str(r["member_price"]) if r["member_price"] else "")

# Store rows with captured_at and run this on a schedule: that stored series is
# your price history (H&M publishes none). Currencies differ: convert explicitly,
# with the rate and its date, before comparing countries.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Every `data` echoes `country`, `language`, `currency` (except product, which carries it with the prices), `locale` and `store` (`eu` on the shared store). Prices are numbers in the market's currency, never converted. `notes` appears when there is something to say.

- **Grid item** (search, category, deals, new arrivals) - `article_code`, `product_code`, `title` (in the request language), `brand`, `url`, `price`, `regular_price`, `sale_price`, `member_price`, `discount_percent`, `prior_price`, `currency`, `promo_text`, `promo_terms`, `multipack` {`quantity`, `unit_price`}, `color`, `colors[]` {`article_code`, `name`, `hex`}, `sizes[]` {`size_code`, `label`, `in_stock`}, `in_stock`, `coming_soon`, `new_arrival`, `markers`, `category` (H&M's category id), `image`, `model_image`.
- **Grid** - `items[]`, `count`, `total`, `page`, `page_size`, `total_pages`, `sort`, `sorts_offered`, `filters`, `facets[]` {`filter`, `name`, `values[]` {`value`, `label`, `count`, `hex` on colours}}, `on_sale_count`, `price_range` {`min`, `max`}. Search adds `query`, `department`, `store_code`, `departments[]` {`department`, `id`, `label`, `count`}, `did_you_mean`, `related_searches`; category adds `category`; deals and new arrivals add `department`.
- **product** - `article_code`, `product_code`, `title`, `brand`, `category`, `category_code`, `breadcrumbs[]` {`name`, `url`}, `url`, `color`, `description`, `composition[]` {`part`, `materials[]` {`name`, `percent`}}, `materials[]` {`name`, `description`}, `care[]`, `attributes` {`fit`, `length`, `rise`, `sleeve_length`, `style`, `neckline`, `weight`, ... as H&M lists them}, the price fields with `price_disclosure`, `currency`, `colors[]` {`article_code`, `name`, `rgb`, the price fields, `price_disclosure`, `url`, `image`}, `sizes[]` {`size_code`, `label`, `in_stock`, `few_left`}, `new_arrival`, `coming_soon`, `sold_in_stores`, `images[]` {`url`, `type`}, `rating` {`average`, `count`}, `reviews[]` {`rating`, `text`, `date`, `fit[]` {`label`, `value`}}.
- **stock** - `product_code`, `article_code`, `title`, `colors[]` {`article_code`, `name`, `sizes[]` {`size_code`, `label`, `in_stock`, `few_left`}}, `sizes_total`, `sizes_in_stock`.
- **stores** - `stores[]` {`store_code`, `name`, `status`, `store_class`, `address`, `city`, `state`, `postal_code`, `country`, `lat`, `lng`, `phone`, `opening_hours[]` {`day`, `open`, `close`}, `opening_hour_exceptions[]` {`date`, `closed`, `open`, `close`}, `departments[]` {`name`, `concepts`}, `campaigns`, `distance_km` with lat / lng}, `count`, `total`, `country_total`, `page`, `page_size`, `total_pages`, `filters`.
- **suggestions** - `query`, `suggestions[]` {`text`, `type` (`query` or `content`), `url` for content pages}, `count`.
- **production** - `article_code`, `product_code`, `production_countries[]`, `countries[]` {`country`, `suppliers[]` {`supplier_id`, `name`, `factories[]` {`factory_id`, `name`, `city`, `workers`}}}.

## Guardrails

- Article codes are global; product codes are the first 7 digits of an article code and cover every colourway. Prices are per colourway (article), not per product: quote the price of the article the user asked about.
- To price one item in many markets, search by the article code (1 credit) and keep the item whose `article_code` matches exactly; product (2 credits; 4 to 75 seconds in the captures) is for the full record. Product is not served on `mo`, `tw` or the shared EU store.
- `member_price` is the member price H&M displays; we do not sign in, so never present it as what a member pays at checkout, and never present member-only cart prices or app-only offers as available.
- `sizes[].in_stock` and `few_left` are ONLINE stock in that market. H&M publishes no per-size stock by store: never say a size is in stock at a store. Search with `store` lists a store's assortment, not its stock.
- `reviews` are at most the 10 latest reviews H&M shows; there is no endpoint for the full review list. Never say you read all reviews; summarize the ones returned and give `rating.count` as the total. Reviewer names are not returned.
- Category ids are the same in every market. A category returns everything H&M files under that id, which can be more than the site's curated page.
- The sale grid is seasonal and can be empty between sales in any market: an empty `/deals` answer is not an error, and never claim every market has a sale running.
- The 7 shared-store countries (`hr`, `cy`, `ee`, `lv`, `lt`, `lu`, `si`) get one English EUR catalog with the same prices; do not present them as separate national prices.
- Production lists countries, supplier and factory names and cities as H&M publishes them; no street addresses or contacts.
- Not available: price history (poll and store), per-size store stock, the full review list, checkout or member-only cart prices, and H&M Group's other brands (COS, Weekday, & Other Stories, Monki, ARKET).
- Terms: H&M's US Terms of Use (last updated 28/06/2024) ask users not to use spiders, bots, crawlers or other automated tools to navigate or search hm.com or copy its content, and say site content is for personal, non-commercial use. We do not interpret them. This is not legal advice; the user is responsible for checking the current terms for their market and use case. Do not republish H&M product photos, campaign images or logos; link product pages instead.
- Never fabricate prices, article codes, sizes, stock, store details or reviews. Only return what the API returned, with the country, the currency and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` the endpoint does not serve (product on `mo`, `tw` or a shared-store country; stores on `mo`; a held-back country; `uk`); a `language` the market does not serve; no `query` on search or suggestions; neither `article_code` nor `url` on product or production; neither `article_code` nor `product_code` on stock; an `article_code` that is not 10 digits or a `product_code` that is not 7; a `url` that is not an hm.com product link; a `store` that is not a store code; a `category` that is not an H&M category id; a `sort` or `department` outside the lists above; a filter value containing `|` or `:`; more than 10 values for a filter.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "H&M has no article ... on ... (unknown code or not sold there).", "H&M has no product ... on ... (unknown code or not sold online there).", "H&M has no category ... on ... (or it is empty there). Use the category of an item from search.", "H&M publishes no production details for article ... (unknown code)." Take codes and category ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=hm-api).
- `502` means H&M data was temporarily unavailable ("H&M is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means H&M is busy ("H&M is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.62.0
npm install scavio@0.63.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.hm.search({ query: "1372161001", country: "de", language: "de" });
const { data: item } = await scavio.hm.product({ article_code: "1310382004" });
const { data: stock } = await scavio.hm.stock({ product_code: "1310382", country: "gb" });
const { data: stores } = await scavio.hm.stores({ country: "us", city: "New York" });
const { data: dresses } = await scavio.hm.category({ category: "ladies_dresses", country: "gb", sort: "price_asc" });
const { data: sale } = await scavio.hm.deals({ country: "gb", department: "men" });
const { data: fresh } = await scavio.hm.newArrivals({ country: "se" });
const { data: typed } = await scavio.hm.suggestions({ query: "hoodie" });
const { data: made } = await scavio.hm.production({ article_code: "1310382004" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.hm.search(...)`, `client.hm.product(...)`, `client.hm.stock(...)`, `client.hm.stores(...)`, `client.hm.category(...)`, `client.hm.deals(...)`, `client.hm.new_arrivals(...)`, `client.hm.suggestions(...)` and `client.hm.production(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_hm`, `get_hm_product`, `get_hm_stock`, `get_hm_stores`, `get_hm_category`, `get_hm_deals`, `get_hm_new_arrivals`, `get_hm_suggestions` and `get_hm_production`. H&M is opt-in: add `hm` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.60.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,hm"
      }
    }
  }
}
```
