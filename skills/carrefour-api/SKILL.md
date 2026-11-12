---
name: carrefour-api
description: "Carrefour API for carrefour.fr groceries: search by keyword or browse a category (aisle), 30 products per page with price, unit price per kg or litre, the promotion with type, label, loyalty-card flag and start and end dates, Nutri-Score, Eco-Score, rating and marketplace seller, filtered by brand, promotion, Nutri-Score, organic, Carrefour brands or price range and sorted by price, unit price or rating; list items on promotion (catalogue, immediate discounts, loyalty-card offers, festive selection); pass a store ref for that store's shelf price and range instead of the national online price; read one product with ingredients, allergens and nutrition per 100 g and per portion; read verified customer reviews; find stores near a French postal code or a point with a service filter (drive, fuel station), check which nearby stores carry a product (yes / no, no price), and read a store's services, opening and drive hours, next pickup slot and fuel prices per litre. Search and product also serve Carrefour Argentina (ARS, Spanish), Romania (RON, Romanian) and Belgium (EUR, French or Dutch); data comes in the market's language. 9 endpoints, 1 credit each (Belgium search and product 2). No price history, no checkout. Carrefour publishes no public carrefour.fr product or price API."
version: 1.0.0
tags: carrefour, carrefour-api, carrefour-grocery-prices, carrefour-price-data, carrefour-promotions, carrefour-france, carrefour-fr, carrefour-drive, carrefour-black-friday, french-supermarket, french-supermarket-prices, france-grocery, grocery, grocery-prices, supermarket-prices, store-prices, price-per-store, unit-price, nutri-score, eco-score, ingredients, allergens, nutrition, product-reviews, store-locator, store-availability, fuel-prices, carrefour-belgium, carrefour-argentina, carrefour-romania, multi-country, europe, product-search, product-data, category-browse, retail, price-monitoring, catalog-enrichment, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/docs/carrefour-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api
---

# Carrefour API - Grocery Prices by Store, Promotions, Nutri-Score, Stores

Read Carrefour grocery and general-merchandise data from carrefour.fr: search by keyword or browse a category (aisle), 30 products per page with the price, the unit price per kg or litre, the current promotion with its dates and whether it needs the loyalty card, Nutri-Score, Eco-Score, rating and the marketplace seller; list the items on promotion; and read one product with its ingredients, allergens and nutrition table. Prices are carrefour.fr's national online price unless you pass a `store`: then they are that store's shelf price and that store's range. Find stores near a French postal code, check which nearby stores carry a product, and read a store's services, opening and drive hours, next pickup slot and, at stores with a fuel station, fuel prices per litre. Search and product also cover Carrefour Argentina, Romania and Belgium in their own language and currency. All 9 endpoints return structured JSON and cost 1 credit each; Belgium search and product cost 2.

Product data comes in the market's language exactly as the site writes it: French titles, categories, promotion labels, ingredients and nutrient names on carrefour.fr ("Pâte à Tartiner Noisettes Cacao NUTELLA", "Le 2ème à -50%", "matières grasses"), Spanish on Argentina, Romanian on Romania, French or Dutch on Belgium. Quote those values as written; translate them for the user only in your own words around the data, and never rewrite them into the data.

Carrefour does not publish a public product, price or store API for carrefour.fr. Its developer portal serves Carrefour Italia partners, Carrefour Links serves brands and suppliers, and marketplace sellers sync their own offers through Mirakl. The France developer portal some AI answers link does not resolve as of November 12, 2026. None of these is a public endpoint for searching carrefour.fr or reading live prices. This skill reads public Carrefour pages with one Scavio key.

See also: for US grocery store prices use `kroger-grocery-data`, `heb-grocery-data`, `aldi-grocery-data` or `whole-foods-grocery-data`; for the cross-retailer price view use `google-shopping-api`; for French products sold on Amazon use `amazon-product-data` with the `fr` marketplace.

## When to trigger

Use this skill when the user asks to:
- Look up Carrefour grocery prices on carrefour.fr, with the unit price per kg or litre, for a product, a brand or a category
- Compare one product's price across Carrefour stores, or a store's shelf price against the national online price
- List Carrefour promotions: catalogue offers, immediate discounts, loyalty-card (Club / Avantage Fidélité) offers or the festive selection, with start and end dates, for example ahead of Black Friday
- Build a French supermarket price basket or a shelf-price monitor for a CPG brand, polling prices and promotions per store
- Read a product's Nutri-Score, Eco-Score, ingredients, allergens and nutrition per 100 g or per portion
- Read what Carrefour customers say about a product (verified reviews with purchase dates)
- Find Carrefour stores near a French postal code or a point, only those with a drive or a fuel station, and check which nearby stores carry a product
- Read a Carrefour store's services, opening and drive hours, next pickup slot, or its fuel prices per litre
- Search Carrefour Argentina, Romania or Belgium products in pesos, lei or euros

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit (Belgium search and product 2), so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
On Growth, 1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. Calls answered in 0.4 to 10 seconds in testing, with store-scoped calls and store pages at the slow end, and a call can take longer when it is retried for you. Allow a client timeout of at least 60 seconds.

| Endpoint | Credits | Markets | What it returns |
|---|---|---|---|
| `POST /api/v1/carrefour/search` | 1 (be 2) | fr, ar, ro, be | A keyword search page (fr 30 items, ar and ro 24, be 36): per item `ean`, `title`, `brand`, `url`, `image`, `type`, `sponsored`, `price`, `unit_price`, `unit_price_label`, `unit`, `packaging`, `format`, `nutriscore`, `ecoscore`, `rating`, `review_count`, `available`, `low_stock`, `promotion`, `seller`, `flags`, `category`. Plus `query`, `corrected_query`, `results_type`, `total`, `total_pages`, `facets[]`, `store`, `price_scope`, `country`, `language`, `currency` |
| `POST /api/v1/carrefour/product` | 1 (be 2) | fr, ar, ro, be | One product by `ean` or `url`: on fr the description, breadcrumb, packaging, origin, Nutri-Score, Eco-Score, regulated name, ingredients, allergens, nutrition per 100 g / ml and per portion, storage, characteristics, the price block, availability, marketplace seller and every offer, and the rating |
| `POST /api/v1/carrefour/reviews` | 1 | fr | 1-50 customer reviews (default 10) of one product with four sorts, a star filter and offset paging: `author`, `rating`, `title`, `text`, `reviewed_at`, `purchased_at`, `source` |
| `POST /api/v1/carrefour/category` | 1 | fr | One category (aisle) grid by `url` or `path` (`/r/cremerie`): the same grid, filters and sorts as search plus the category's label and breadcrumb |
| `POST /api/v1/carrefour/promotions` | 1 | fr | Items on promotion by `type`: `all`, `catalogue`, `immediate`, `loyalty` or `festive`, optionally for one aisle; the same grid as search |
| `POST /api/v1/carrefour/suggestions` | 1 | fr | Search box suggestions for a partial query, plus suggestions scoped to a category |
| `POST /api/v1/carrefour/stores` | 1 | fr | Stores near a French postal code or a point, nearest first (up to 20 per page), optionally with one service: `id`, `store_ref`, `pickup_refs[]`, name, banner, format, `distance_km`, address, today's hours, `slug` |
| `POST /api/v1/carrefour/store-availability` | 1 | fr | Whether the stores around a French postal code carry one product: per store `available` yes / no, `distance_km` and the store (ref, address, phone, weekly and drive hours). No price |
| `POST /api/v1/carrefour/store` | 1 | fr | One store page: services, weekly opening and drive hours, the next pickup slot as shown, delivery flags, nearby stores and, at stores with a fuel station, `fuel` prices per litre with update times |

## Markets

Every endpoint takes `country` (default `fr`). carrefour.fr has every endpoint and every filter; Argentina, Romania and Belgium have search and product only.

| `country` | Site | Currency | Language | Endpoints | Notes |
|---|---|---|---|---|---|
| `fr` | carrefour.fr | EUR | fr | all 9 | Every filter, every sort, `store` scope |
| `ar` | carrefour.com.ar | ARS | es | search, product | Product by `ean` or `url`. Sorts: relevance and the two price sorts |
| `ro` | carrefour.ro | RON | ro | search, product | Product by `url` only. Sorts: relevance and the two price sorts |
| `be` | carrefour.be | EUR | `language`: `fr` (default) or `nl` | search, product | 2 credits each. Product by `url` only. Sort: relevance only |

On ar, ro and be the response has `facets: []`, `store: null` and `price_scope: "online price"`, and items carry the fields their site gives (`product_id`, `list_price`; `card_offers` on ar; `packaging` and `nutriscore` on be). The brand, promotion, Nutri-Score, organic, Carrefour-brands and price filters and `store` are carrefour.fr only and return `400` elsewhere. Carrefour Spain, Italy, Poland, Brazil and Taiwan and the Middle East sites (run by a franchise partner) are not served.

## Workflow

1. **Find products:** call `/carrefour/search` with `query`, `/carrefour/category` with a category `path` (a product's `breadcrumb[].url`) or `/carrefour/promotions` with a `type`. Each item has an `ean` on carrefour.fr; use it for `/product`, `/reviews` and `/store-availability`.
2. **Decide the price scope first.** Without `store` every price is carrefour.fr's national online price. For one store's shelf price and range, call `/carrefour/stores` with the shopper's `postal_code`, take a `store_ref` or a `pickup_refs[].ref`, and pass it as `store` on search, product, category or promotions. `/carrefour/store-availability` also gives refs (`stores[].store.ref`) for stores that carry a given product. Every answer says which scope it used in `store` (`"national"` or the ref) and `price_scope`.
3. **One product in full:** call `/carrefour/product` with the `ean` (or the item `url`) and the same `store`. Read `ingredients`, `allergens`, `nutrition`, `nutriscore`, `ecoscore` and the price block.
4. **Shelf-price watch:** poll search, category, promotions or product for a fixed list of stores on a schedule and store `price`, `unit_price`, the whole `promotion` object and the time per run; compare runs yourself. There is no price history.
5. **Stores:** `/carrefour/stores` for the locator (filter with `service`, e.g. `station_service` for fuel stations or `drive`), then `/carrefour/store` with the store's `slug` for services, hours, the next pickup slot and fuel prices.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Search keywords (1-200 chars). On fr the site corrects spelling: see `corrected_query` |
| `country` | string | `fr` | `fr`, `ar`, `ro` or `be` |
| `language` | string | - | `be` only: `fr` (default) or `nl` |
| `store` | string or integer | national | fr only: a `store_ref` or `pickup_refs[].ref` from `/stores`, or `stores[].store.ref` from `/store-availability` (digits). That store's prices and range |
| `page` | integer | 1 | Results page, 1-500 |
| `sort` | string | `relevance` | `relevance`, `price_low_to_high`, `price_high_to_low`, `unit_price_low_to_high`, `unit_price_high_to_low` or `top_rated`. ar and ro: relevance and the two price sorts; be: relevance only |
| `brand` | string | - | fr: one brand as the Marque facet lists it (`facets[id=facet_marque].values[].label`, e.g. `NUTELLA`, `CARREFOUR BIO`) |
| `promotion` | string | - | fr: one value of the Promotions facet (`facets[id=facet_promotions]`): `Toutes les promotions`, `Remises immédiates`, `Vu en catalogue`, `Avantage Fidélité`... |
| `nutriscore` | string | - | fr: `A`, `B`, `C`, `D` or `E` |
| `organic` | boolean | - | fr: only organic products |
| `carrefour_brands` | boolean | - | fr: only Carrefour's own brands |
| `min_price`, `max_price` | number | - | fr: price range in EUR |

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ean` | string | one of | The barcode (EAN / GTIN, 8-14 digits): `items[].ean`. fr and ar |
| `url` | string | one of | A product URL (`items[].url`) on the `country`'s site. Required on ro and be |
| `country`, `language`, `store` | | | As on search (`store` fr only) |
| `seller` | string or integer | - | fr: a marketplace seller id (`items[].seller.id`) to read that seller's offer |

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ean` | string | required | The product barcode |
| `sort` | string | `most_recent` | `most_recent`, `oldest`, `highest_rated` or `lowest_rated` |
| `rating` | integer | - | Only reviews with this many stars (1-5) |
| `limit` | integer | 10 | Reviews to return, 1-50 |
| `offset` | integer | 0 | Reviews to skip, for paging (0-10000) |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | one of | A carrefour.fr category URL (`https://www.carrefour.fr/r/...`) |
| `path` | string | one of | The category path (`/r/cremerie`, `/r/epicerie-sucree/petit-dejeuner`) or its slug (`cremerie`): a product's `breadcrumb[].url` |
| `store`, `page`, `sort` and the fr filters | | | As on search |

### Promotions (`/promotions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | `all` | `all`, `catalogue` (seen in the printed catalogue: "Vu en catalogue"), `immediate` ("Remises immédiates"), `loyalty` ("Avantage Fidélité": loyalty-card offers) or `festive` (the site's seasonal "Sélection festive") |
| `category` | string | - | Only one aisle: a value of the Rayon facet (`facets[id=product.categories.name].values[].label`, e.g. `Boissons`) |
| `store`, `page`, `sort`, `brand`, `nutriscore`, `organic`, `carrefour_brands`, `min_price`, `max_price` | | | As on search. `promotion` is not taken here: use `type` |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the shopper has typed so far (1-200 chars) |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `postal_code` | string | one of | A French postal code (5 digits) |
| `lat`, `lng` | number | one of | A point in metropolitan France (lat 41-51.5, lng -5.5-10), sent together |
| `service` | string | - | Only stores with this service: `drive`, `lad` (home delivery), `Retrait2h-drive`, `station_service` (fuel station), `banque_assurance`, `spectacles`, `voyages`, `location_vehicule`, `traiteur`, `Parapharmacie` or `pro` |
| `page` | integer | 1 | Page of stores, 1-50 |
| `limit` | integer | 10 | Stores per page, 1-20 |

There is no banner filter (Hypermarché, Market, City, Express): filter on `banner` / `format` in the answer.

### Store availability (`/store-availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ean` | string | required | The product barcode |
| `postal_code` | string | required | A French postal code: the stores around it are checked |

### Store (`/store`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `slug` | string | one of | A store page slug: `stores[].slug` (e.g. `venissieux`, `lyon-part-dieu`) |
| `url` | string | one of | A `https://www.carrefour.fr/magasin/...` store page URL |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nutella"}'
```

Captured `data` (27 of 30 items and 11 of 13 facets trimmed):

```json
{
  "query": "nutella",
  "corrected_query": null,
  "results_type": "match",
  "sort": "relevance",
  "applied_filters": {},
  "total": 49,
  "total_pages": 2,
  "page": 1,
  "page_size": 30,
  "count": 30,
  "items": [
    {
      "ean": "3017620422003",
      "title": "Pâte à Tartiner Noisettes Cacao NUTELLA",
      "brand": "NUTELLA",
      "url": "https://www.carrefour.fr/p/pate-a-tartiner-noisettes-cacao-nutella-3017620422003",
      "image": "https://media.carrefour.fr/media/referential/media/05c71277c9f94c388a282e78457e0879/p_540x540/03017620422003_C1R1_s37.png",
      "type": "product",
      "sponsored": false,
      "price": 3.99,
      "unit_price": 9.98,
      "unit_price_label": "9.98 € / KG",
      "unit": "KG",
      "packaging": "le pot de 400g",
      "format": "400g",
      "nutriscore": null,
      "ecoscore": null,
      "rating": 4.36,
      "review_count": 14,
      "available": true,
      "low_stock": false,
      "promotion": {
        "type": "ri",
        "label": "Le 2ème à -50%",
        "loyalty_only": false,
        "seen_in_catalogue": false,
        "discounted_price": 5.98,
        "initial_price": 7.98,
        "discount_amount": 2,
        "quantity": 2,
        "starts_at": "2026-11-02T00:00:00+01:00",
        "ends_at": "2026-11-17T23:59:00+01:00"
      },
      "seller": null,
      "flags": [],
      "category": "Epicerie sucrée"
    },
    {
      "ean": "3560071507480",
      "title": "Pâte à Tartiner Noisettes Bio CARREFOUR BIO",
      "brand": "CARREFOUR BIO",
      "url": "https://www.carrefour.fr/p/pate-a-tartiner-noisettes-bio-carrefour-bio-3560071507480",
      "image": "https://media.carrefour.fr/medias/7a86009b42643bc78bc0185ea7ae4b02/p_540x540/3560071507480-0.jpg",
      "type": "product",
      "sponsored": false,
      "price": 2.65,
      "unit_price": 7.57,
      "unit_price_label": "7.57 € / KG",
      "unit": "KG",
      "packaging": "le pot de 350g",
      "format": "350g",
      "nutriscore": null,
      "ecoscore": null,
      "rating": 4.44,
      "review_count": 403,
      "available": true,
      "low_stock": false,
      "promotion": {
        "type": "rd_fid_market",
        "label": "-10% Club",
        "loyalty_only": true,
        "seen_in_catalogue": false,
        "discounted_price": null,
        "initial_price": 2.65,
        "discount_amount": 0.27,
        "quantity": 1,
        "starts_at": "2025-01-01T00:00:00+01:00",
        "ends_at": "2026-12-31T23:59:00+01:00"
      },
      "seller": null,
      "flags": ["organic"],
      "category": "Epicerie sucrée"
    },
    {
      "ean": "4008400404127",
      "title": "Pâte À Tartiner Noisettes/cacao Nutella (750g) FERRERO",
      "brand": "FERRERO",
      "url": "https://www.carrefour.fr/p/pate-a-tartiner-noisettes-cacao-nutella-750g-4008400404127?s=3155",
      "image": "https://media.carrefour.fr/medias/378f624c67933d0eb57d7a50270753af/p_540x540/ab08465e8bee47fbb20bb18336ba5240-image.jpg",
      "type": "marketplace",
      "sponsored": false,
      "price": 56.95,
      "unit_price": null,
      "unit_price_label": null,
      "unit": null,
      "packaging": null,
      "format": null,
      "nutriscore": null,
      "ecoscore": null,
      "rating": null,
      "review_count": null,
      "available": true,
      "low_stock": false,
      "promotion": null,
      "seller": {
        "id": "3155",
        "name": "Tormino FR",
        "rating": null,
        "review_count": null,
        "shipping_days_min": null,
        "shipping_days_max": null,
        "free_shipping": null
      },
      "flags": [],
      "category": "Epicerie sucrée"
    }
  ],
  "facets": [
    {
      "id": "facet_promotions",
      "label": "Promotions",
      "type": "checkbox",
      "values": [
        { "label": "Toutes les promotions", "count": 18, "selected": false },
        { "label": "Remises immédiates", "count": 11, "selected": false },
        { "label": "Avantage Fidélité", "count": 5, "selected": false },
        { "label": "Avantage Carrefour Bio", "count": 2, "selected": false },
        { "label": "Mardi PASS", "count": 5, "selected": false }
      ]
    },
    {
      "id": "facet_price",
      "label": "Prix",
      "type": "slider",
      "values": [],
      "ranges": [
        { "min": 0, "max": 2.03 },
        { "min": 2.03, "max": 4.06 },
        { "min": 18.28, "max": 173.38 }
      ]
    }
  ],
  "store": "national",
  "price_scope": "national online price; prices and assortment differ by store (pass store for one store's prices)",
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

Read the price fields together:

- `price` is the regular price of one item, even when a promotion runs (3.99 for the 400 g jar). `unit_price` is the site's price per `unit` (`KG` or `L`), with the site's own `unit_price_label`: compare pack sizes with it (9.98 EUR / kg for the 400 g jar, 7.57 for the 350 g Carrefour Bio jar).
- `promotion.discounted_price` and `initial_price` are for `quantity` items, not one: "Le 2ème à -50%" (second at half price) reads 5.98 for 2 against 7.98 for 2, so one jar works out at 2.99 only when bought in twos. Divide by `quantity` before comparing with `price`, and say it is a multi-buy.
- `discounted_price` is null whenever the site does not price the deal: often on multi-buys (the same "Le 2ème à -50%" at a store, below), on "Vu en catalogue" tiles and on loyalty offers. Never compute a price the site did not give; quote the `label`, `discount_amount` when set, and the dates.
- `loyalty_only: true` means the offer needs the Carrefour loyalty card (the Club / Avantage Fidélité): the "-10% Club" deal takes 0.27 off 2.65 for card holders only. Never present it as the price everyone pays. `seen_in_catalogue` flags offers from the printed catalogue; `starts_at` / `ends_at` bound every promotion.
- `type: "marketplace"` items are sold by a third-party seller (`seller.name`), not by Carrefour, usually without a unit price: the 750 g Nutella from "Tormino FR" at 56.95 is a marketplace listing. Keep marketplace offers apart from Carrefour's own prices.

`nutriscore` and `ecoscore` are `A`-`E` or null when the site shows none (null on most tiles of this search; the product page can still carry one: Eco-Score `D` on the Nutella jar). `flags` lists badges such as `organic`. `sponsored` marks paid placements. Facets carry the exact labels the filters take: send `brand` and `promotion` values from `facet_marque` and `facet_promotions`, and use the `facet_price` bands to pick a `min_price` / `max_price`. `results_type: "fallback"` means nothing matched and the site returned loosely related items: say so rather than presenting them as matches. `corrected_query` is the site's spelling correction.

### Search at one store

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nutella", "store": "840093"}'
```

The captured answer opens with (then `items[]` and `facets[]`):

```json
{
  "query": "nutella",
  "results_type": "match",
  "total": 36,
  "total_pages": 2,
  "page": 1,
  "page_size": 30,
  "count": 30,
  "store": "840093",
  "price_scope": "store",
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

and the same 400 g jar reads:

```json
{
  "ean": "3017620422003",
  "title": "Pâte à Tartiner Noisettes Cacao NUTELLA",
  "price": 3.69,
  "unit_price": 9.22,
  "unit_price_label": "9.22 € / KG",
  "promotion": {
    "type": "ri",
    "label": "Le 2ème à -50%",
    "loyalty_only": false,
    "seen_in_catalogue": false,
    "discounted_price": null,
    "initial_price": 7.38,
    "discount_amount": null,
    "quantity": 2,
    "starts_at": "2026-11-02T00:00:00+01:00",
    "ends_at": "2026-11-17T23:59:00+01:00"
  }
}
```

Prices and assortment differ by store. Measured on 2026-11-12, the Nutella 400 g jar was 3.99 national, 3.69 at store 840093 and at Market Lyon Frères Lumière (ref 281), and 4.61 at Lyon Part Dieu (store_ref 810936); "nutella" matched 49 products nationally and 36 at store 840093, and "lait" about 599 nationally against 147 at store 281. A hypermarket's `store_ref` and its drive `pickup_refs[].ref` are separate refs and can price differently (Lyon Part Dieu's drive ref 840116 returned 3.99 on product): record which ref you used, quote the store's name with every store price, and never present the national price as a store's shelf price or the other way round. A ref that is not a Carrefour store returns a charged `404`, so take refs from `/stores` or `/store-availability`.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ean": "3017620422003"}'
```

Captured `data` (2 of 4 breadcrumb entries, 5 of 8 nutrients per table and the description trimmed; `offers[0]` repeats the price block):

```json
{
  "ean": "3017620422003",
  "title": "Pâte à Tartiner Noisettes Cacao NUTELLA",
  "brand": "NUTELLA",
  "url": "https://www.carrefour.fr/p/pate-a-tartiner-noisettes-cacao-nutella-3017620422003",
  "type": "product",
  "key_features": [],
  "breadcrumb": [
    { "label": "Epicerie sucrée", "url": "https://www.carrefour.fr/r/epicerie-sucree" },
    { "label": "Petit déjeuner", "url": "https://www.carrefour.fr/r/epicerie-sucree/petit-dejeuner" }
  ],
  "categories": ["Epicerie sucrée", "Petit déjeuner", "Pâtes à tartiner et Miels", "Pâtes à tartiner et Crèmes"],
  "packaging": "le pot de 400g",
  "format": "400g",
  "origin": null,
  "nutriscore": null,
  "ecoscore": "D",
  "regulated_name": "Pâte à tartiner aux noisettes",
  "ingredients": "sucre, huile de palme, NOISETTES 13%, LAIT écrémé en poudre 8,7%, cacao maigre 7,4%, émulsifiants : lécithines SOJA vanilline",
  "allergens": ["NOISETTES", "LAIT", "SOJA"],
  "nutrition": {
    "per_100": {
      "label": "100 g",
      "values": [
        { "nutrient": "valeur énergétique (kcal)", "quantity": "539 kcal", "daily_value_pct": null },
        { "nutrient": "matières grasses", "quantity": "30.9 g", "daily_value_pct": null },
        { "nutrient": "sucres", "quantity": "56.3 g", "daily_value_pct": null }
      ]
    },
    "per_portion": {
      "label": "15 g",
      "values": [
        { "nutrient": "valeur énergétique (kcal)", "quantity": "80 kcal", "daily_value_pct": null },
        { "nutrient": "matières grasses", "quantity": "4.6 g", "daily_value_pct": null },
        { "nutrient": "sucres", "quantity": "8.4 g", "daily_value_pct": null }
      ]
    }
  },
  "storage": "A conserver au sec et à l'abri de la chaleur. Ne pas mettre au réfrigérateur.",
  "advice": null,
  "characteristics": [],
  "weights": [],
  "flags": [],
  "price": 3.99,
  "unit_price": 9.98,
  "unit_price_label": "9.98 € / KG",
  "unit": "KG",
  "tax_note": null,
  "available": true,
  "low_stock": false,
  "max_quantity": 50,
  "promotion": {
    "type": "ri",
    "label": "Le 2ème à -50%",
    "loyalty_only": false,
    "seen_in_catalogue": false,
    "discounted_price": 5.98,
    "initial_price": 7.98,
    "discount_amount": 2,
    "quantity": 2,
    "starts_at": "2026-11-02T00:00:00+01:00",
    "ends_at": "2026-11-17T23:59:00+01:00"
  },
  "seller": null,
  "more_offers_count": 0,
  "rating": {
    "average": 4.36,
    "count": 14,
    "distribution": { "1": 7, "2": 0, "3": 0, "4": 36, "5": 57 }
  },
  "store": "national",
  "price_scope": "national online price; prices and assortment differ by store (pass store for one store's prices)",
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

`allergens` are the words the ingredient list writes in capitals, exactly as written there (`NOISETTES`, `LAIT`, `SOJA`): they come from the label text, so for an allergy question quote the `ingredients` line too and tell the user to check the pack. Nutrient names and quantities are French strings with their unit (`"matières grasses"`, `"30.9 g"`); `per_portion.label` gives the portion size (15 g). `regulated_name` is the legal product name. `rating.distribution` is the percentage of ratings per star (7 / 0 / 0 / 36 / 57 adds up to 100 over `count` 14), not a count. Non-food items carry `characteristics[]` (`name`, `values`) and `key_features` instead of nutrition. `max_quantity` is the most units of the item one order can take on the site.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ean": "8006530256179"}'
```

Captured `data` (8 of 10 reviews trimmed):

```json
{
  "ean": "8006530256179",
  "sort": "most_recent",
  "rating": null,
  "limit": 10,
  "offset": 0,
  "total": 76,
  "reviews": [
    {
      "author": "REGINE D.",
      "rating": 4,
      "title": "Excellent",
      "text": "Tres absorbant\nEt tres doux",
      "reviewed_at": "2026-10-16",
      "purchased_at": "2026-10-15",
      "source": "SHOP_ADVIZOR"
    },
    {
      "author": "JEAN S.",
      "rating": 5,
      "title": "Tres bonnes couches",
      "text": "Tres bonnes couches bonne qualite",
      "reviewed_at": "2026-10-16",
      "purchased_at": "2026-10-14",
      "source": "SHOP_ADVIZOR"
    }
  ],
  "count": 10,
  "has_more": true,
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

Reviews are verified-purchase reviews: each carries `purchased_at` (the purchase date) and `source` (the review provider). `author` is the public first name and last initial as Carrefour publishes it: never try to identify a reviewer. Review text is in French as written. Page with `offset` while `has_more` is true; `total` counts every review (after the `rating` filter).

### Category and promotions

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/promotions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type": "catalogue"}'
```

The captured answer opens with (then `items[]` and `facets[]` as on search):

```json
{
  "type": "catalogue",
  "label": "Vu en catalogue",
  "category": null,
  "sort": "relevance",
  "applied_filters": {},
  "total": 5427,
  "total_pages": 181,
  "page": 1,
  "page_size": 30,
  "count": 30,
  "store": "national",
  "price_scope": "national online price; prices and assortment differ by store (pass store for one store's prices)",
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

Its first item was a "Panettone classique CARREFOUR EXTRA" at 5.49 (Nutri-Score `E`) with `promotion` {`type`: `"ta"`, `label`: `"Vu en catalogue"`, `seen_in_catalogue`: true, `discounted_price`: null, `starts_at` 2026-11-10, `ends_at` 2026-11-23}: a catalogue offer flags the item without giving a promotional price, so quote the tile `price` and the dates. `label` is the site's own name for the list; `festive` returns the site's current "Sélection festive" (panettone, advent calendars, champagne in November). `/carrefour/category` with `{"path": "/r/cremerie"}` returns the same grid with `category` {`label`: `"Crèmerie et Produits laitiers"`, `path`, `url`, `breadcrumb[]`} and `total` 5683. This is carrefour.fr's online promotions list, not the printed leaflet itself.

Black Friday 2026 is November 27; carrefour.fr's Black Friday page reads "Jusqu'au 30 novembre". Poll `/promotions` (and `type: "loyalty"` for card offers) daily through the season and store what you see.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "nutel"}'
```

Captured `data` (7 of 10 suggestions and 1 of 3 categories trimmed):

```json
{
  "query": "nutel",
  "suggestions": [
    { "text": "nutella", "url": "https://www.carrefour.fr/s?q=nutella" },
    { "text": "cacao nutella", "url": "https://www.carrefour.fr/s?q=cacao%20nutella" },
    { "text": "nutella b ready", "url": "https://www.carrefour.fr/s?q=nutella%20b%20ready" }
  ],
  "categories": [
    { "category": "Epicerie sucrée", "text": "nutella", "url": "https://www.carrefour.fr/s?q=nutella&filters%5Bproduct.categories.name%5D=Epicerie%20sucr%C3%A9e" },
    { "category": "Surgelés", "text": "nutella", "url": "https://www.carrefour.fr/s?q=nutella&filters%5Bproduct.categories.name%5D=Surgel%C3%A9s" }
  ],
  "count": 10,
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

### Stores

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"postal_code": "69003"}'
```

Captured `data` (8 of 10 stores trimmed):

```json
{
  "postal_code": "69003",
  "lat": 45.7549,
  "lng": 4.8492,
  "page": 1,
  "limit": 10,
  "service": null,
  "count": 10,
  "stores": [
    {
      "id": "6619",
      "store_ref": "810929",
      "pickup_refs": [{ "ref": "800294", "name": "Drive Pieton", "type": "pieton", "status": "OPEN" }],
      "name": "Express Lyon Saxe 163",
      "banner": "CARREFOUR EXPRESS",
      "format": "PROXIMITE",
      "distance_km": 0.11,
      "address": {
        "line1": "163b Avenue Du Marechal De Saxe",
        "line2": null,
        "postal_code": "69003",
        "city": "Lyon",
        "region": "Auvergne-Rhône-Alpes",
        "country_code": "FR"
      },
      "lat": 45.754135,
      "lng": 4.847231,
      "open_today": true,
      "opening_today": [{ "opens": "2026-11-12T07:00:00+01:00", "closes": "2026-11-12T22:00:00+01:00" }],
      "slug": "express-lyon-saxe-163",
      "store_url": "https://www.carrefour.fr/magasin/express-lyon-saxe-163"
    },
    {
      "id": "A5LX",
      "store_ref": null,
      "pickup_refs": [],
      "name": "Lyon -Gambetta 10",
      "banner": "PROXI",
      "format": "PROXIMITE",
      "distance_km": 0.36,
      "address": {
        "line1": "10 Cr Gambetta",
        "line2": null,
        "postal_code": "69007",
        "city": "Lyon",
        "region": "Auvergne-Rhône-Alpes",
        "country_code": "FR"
      },
      "lat": 45.75540119851401,
      "lng": 4.841773499883083,
      "open_today": false,
      "opening_today": [],
      "slug": null,
      "store_url": null
    }
  ],
  "filters": {
    "services": ["drive", "lad", "Retrait2h-drive", "station_service", "banque_assurance", "spectacles", "voyages", "location_vehicule", "traiteur", "Parapharmacie", "pro"]
  },
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

Only stores with a `store_ref` or a `pickup_refs[].ref` can scope prices: 8 of the 10 stores near 69003 (the Carrefour City and Proxi convenience stores) had `store_ref: null` and no pickup refs, so there are no store prices for them; the Proxi stores also had no `slug`, so no store page. Use the nearest store that has a ref, and say which one. Lyon Part Dieu (`format` "HYPERMARCHES FRANCE") had `store_ref` 810936 and a drive pickup ref 840116. `distance_km` is the distance from the searched postal code or point.

### Store availability

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/store-availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"ean": "3017620422003", "postal_code": "69003"}'
```

Captured `data` (19 of 20 stores and 5 days of each week trimmed):

```json
{
  "ean": "3017620422003",
  "postal_code": "69003",
  "count": 20,
  "available_count": 20,
  "note": "availability only, no price: for a store's price call search or product with store set to stores[].store.ref",
  "stores": [
    {
      "available": true,
      "distance_km": 0.96053,
      "store": {
        "id": "8424",
        "ref": "281",
        "pickup_refs": [{ "ref": "281", "name": "Drive Retrait Parking", "type": "drive", "status": "OPEN" }],
        "name": "Market Lyon Frères Lumière",
        "banner": "MARKET",
        "format": "SUPERMARCHES FRANCE",
        "address": {
          "line1": "68 Avenue Des Freres Lumiere",
          "line2": null,
          "postal_code": "69008",
          "city": "Lyon",
          "region": "Auvergne-Rhône-Alpes",
          "country_code": "FR"
        },
        "lat": 45.7451,
        "lng": 4.86554,
        "phone": "04 72 78 52 10",
        "opening_hours": {
          "saturday": [{ "opens": "08:30", "closes": "21:00" }],
          "sunday": [{ "opens": "09:00", "closes": "12:30" }]
        },
        "drive_hours": {
          "saturday": [{ "opens": "08:00", "closes": "20:30" }],
          "sunday": [{ "opens": "09:30", "closes": "12:00" }]
        },
        "slug": "market-lyon-freres-lumiere",
        "store_url": "https://www.carrefour.fr/magasin/market-lyon-freres-lumiere"
      }
    }
  ],
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

This is availability only: yes / no per store, never a price and never a unit count. For a store's price, pass its `store.ref` as `store` to `/search` or `/product` (ref 281 returned 3.69 for this jar). Stores come nearest first (20 here, the farthest 14.7 km away).

### Store and fuel prices

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/store \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "venissieux"}'
```

Captured `data` (24 of 27 services, 5 days of each week, 3 of 5 nearby stores and 2 of 5 fuels trimmed):

```json
{
  "store": {
    "id": "0016",
    "store_ref": "810893",
    "pickup_refs": [{ "ref": "168", "name": "Drive Retrait Parking", "type": "drive", "status": "OPEN" }],
    "name": "Vénissieux",
    "banner": "CARREFOUR",
    "format": "HYPERMARCHES FRANCE",
    "type": "Hypermarché",
    "status": "Actif",
    "address": {
      "line1": "136 Boulevard Joliot Curie",
      "line2": null,
      "postal_code": "69200",
      "city": "Vénissieux",
      "region": "Auvergne-Rhône-Alpes",
      "country_code": "FR"
    },
    "lat": 45.71656,
    "lng": 4.87515,
    "phone": "04 37 90 49 79",
    "services": [
      { "category": "facilite", "name": "Point Retrait Colis" },
      { "category": "commercial_service", "name": "Drive Retrait Parking" },
      { "category": "commercial_service", "name": "Station Service 24h/24 et/ou Bornes de recharges électriques" }
    ],
    "open_today": true,
    "opening_hours": {
      "saturday": [{ "opens": "08:30", "closes": "21:00" }],
      "sunday": [{ "opens": "08:00", "closes": "12:00" }]
    },
    "drive_hours": {
      "saturday": [{ "opens": "08:00", "closes": "20:30" }],
      "sunday": [{ "opens": "08:00", "closes": "12:00" }]
    },
    "has_delivery": false,
    "has_express_delivery": true,
    "next_slots": [{ "pickup_ref": "168", "starts_at": "2026-11-12T11:00:00+01:00", "ends_at": "2026-11-12T11:30:00+01:00" }],
    "nearest_stores": [
      { "id": "4727", "name": "City Venissieux Sembat", "banner": "CARREFOUR CITY", "slug": "city-venissieux-sembat", "store_url": "https://www.carrefour.fr/magasin/city-venissieux-sembat" },
      { "id": "8057", "name": "Market Saint-Fons", "banner": "CARREFOUR MARKET", "slug": "market-saint-fons", "store_url": "https://www.carrefour.fr/magasin/market-saint-fons" }
    ],
    "slug": "venissieux",
    "store_url": "https://www.carrefour.fr/magasin/venissieux"
  },
  "fuel": {
    "updated_at": "2026-11-12T01:15:09+01:00",
    "prices": [
      { "fuel": "SP95-E10", "code": "E10", "price_per_litre": 1.972, "updated_at": "2026-11-11T19:41:00+01:00" },
      { "fuel": "SP98", "code": "SP98", "price_per_litre": 2.033, "updated_at": "2026-11-11T19:41:00+01:00" },
      { "fuel": "Gazole", "code": "GAZOLE", "price_per_litre": 2.073, "updated_at": "2026-11-11T19:41:00+01:00" }
    ]
  },
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

`fuel` is set only at stores with a fuel station and is null elsewhere: find them with `/stores` and `service: "station_service"`. Prices are EUR per litre, each with its own `updated_at`: quote the time with the price. Fuels the station sells can include Gazole, SP95, SP95-E10, SP98, E85 and GPLc. `next_slots` is the next pickup slot the store page shows, per pickup ref: it is not a booking and can be gone by the time a shopper looks. Service names and `type` / `status` are in French as the page writes them.

### Argentina, Romania and Belgium

```bash
curl -X POST https://api.scavio.dev/api/v1/carrefour/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "yerba", "country": "ar"}'
```

A captured Argentina item (`image` trimmed), from a search with `total` 261 and `page_size` 24:

```json
{
  "ean": "7791720046135",
  "product_id": "765528",
  "title": "Yerba mate serrana Carrefour Classic 500 grs",
  "brand": "Carrefour",
  "url": "https://www.carrefour.com.ar/yerba-mate-serrana-carrefour-classic-500-grs-765528/p",
  "price": 2151,
  "list_price": 2390,
  "unit_price": 4780,
  "unit_price_label": "$4,780.00 x 1 K.",
  "unit": "1 K.",
  "packaging": null,
  "nutriscore": null,
  "available": true,
  "promotion": { "type": "price_cut", "label": null, "loyalty_only": false, "seen_in_catalogue": false, "discounted_price": 2151, "initial_price": 2390, "discount_amount": 239, "quantity": 1, "starts_at": null, "ends_at": null },
  "category": "Yerba",
  "card_offers": []
}
```

On Argentina `price` is the current price in ARS and `list_price` the price before a markdown; `unit_price` is the site's own per-unit field and can refer to the list price on a marked-down item, so recompute from `price` if you need it exact. A Romania product (`{"country": "ro", "url": "https://carrefour.ro/produse/cafea-boabe-prajita-davidoff-cafe-creme-500g-19-14515950"}`) read "Cafea boabe, prajita, Davidoff Cafe Creme 500g" at 72.29 RON with `unit_price` 144.58 and `unit_price_label` "144.58 LEI / kg", `brand` null and `ean` null (Romania and Belgium use their own `product_id`, so look products up by `url`; Romania search tiles can lack the unit price the product page has). A Belgium search for "chocolat" (2 credits) returned 36 items per page in French; its first item, "Classic' Les Barquettes Fraise Biscuits 3 x 6 Pièces 120 g" at 1.35 EUR, had Nutri-Score `D`, `unit_price_label` "11,25 €/kg" (the site's comma decimals; `unit_price` is the number 11.25) and a multi-buy `promotion` labelled "5 achetés = 5€" with no prices. Send `"language": "nl"` for the Dutch site.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def carrefour(endpoint, body, timeout=60):
    r = requests.post(f"{BASE}/api/v1/carrefour/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    r.raise_for_status()
    return r.json()["data"]

# 1. Stores near a postal code that can scope prices (1 credit)
stores = carrefour("stores", {"postal_code": "69003", "limit": 20})
refs = [(s["name"], s["store_ref"] or s["pickup_refs"][0]["ref"])
        for s in stores["stores"] if s["store_ref"] or s["pickup_refs"]]

# 2. National price vs each store's shelf price for one product (1 credit each)
ean = "3017620422003"
national = carrefour("product", {"ean": ean})
print("national", national["price"], national["unit_price_label"])
for name, ref in refs[:3]:
    p = carrefour("product", {"ean": ean, "store": ref})
    promo = p["promotion"] or {}
    print(name, ref, p["price"], promo.get("label"), "card only" if promo.get("loyalty_only") else "")

# 3. Loyalty-card offers in one aisle, cheapest per kg first (1 credit)
deals = carrefour("promotions", {"type": "loyalty", "category": "Boissons", "sort": "unit_price_low_to_high"})
for it in deals["items"][:5]:
    pr = it["promotion"]
    print(it["title"], it["price"], pr["label"], pr["discount_amount"], pr["ends_at"])

# 4. Fuel prices at stations near a postal code (1 + 1 per station)
stations = carrefour("stores", {"postal_code": "75011", "service": "station_service", "limit": 5})
for s in stations["stores"]:
    if s["slug"]:
        fuel = carrefour("store", {"slug": s["slug"]})["fuel"]
        if fuel:
            print(s["name"], [(f["fuel"], f["price_per_litre"]) for f in fuel["prices"]])
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. `credits_used` is 2 on Belgium search and product.

- **grid item** (fr search, category, promotions) - `ean`, `title`, `brand`, `url`, `image`, `type` (`product` or `marketplace`), `sponsored`, `price`, `unit_price`, `unit_price_label`, `unit`, `packaging`, `format`, `nutriscore`, `ecoscore`, `rating`, `review_count`, `available`, `low_stock`, `promotion`, `seller`, `flags[]`, `category`.
- **promotion** - `type`, `label`, `loyalty_only`, `seen_in_catalogue`, `discounted_price` (for `quantity` items, or null), `initial_price`, `discount_amount`, `quantity`, `starts_at`, `ends_at`.
- **seller** (marketplace) - `id`, `name`, `rating`, `review_count`, `shipping_days_min`, `shipping_days_max`, `free_shipping`.
- **grid** - `sort`, `applied_filters`, `total`, `total_pages`, `page`, `page_size`, `count`, `items[]`, `facets[]` {`id`, `label`, `type`, `values[]` {`label`, `count`, `selected`}, `ranges[]` {`min`, `max`} on the price facet}, `store`, `price_scope`, `country`, `language`, `currency`.
- **search** - `query`, `corrected_query`, `results_type` (`match` or `fallback`) and the grid. **category** - `category` {`label`, `path`, `url`, `breadcrumb[]`} and the grid. **promotions** - `type`, `label`, `category` and the grid.
- **market item** (ar, ro, be search) - `ean` (ar), `product_id`, `title`, `brand`, `url`, `image`, `price`, `list_price`, `unit_price`, `unit_price_label`, `unit`, `packaging`, `nutriscore`, `available`, `promotion`, `category`, `card_offers` (ar). Envelope as search with `facets: []`, `store: null`.
- **product** (fr) - `ean`, `title`, `brand`, `url`, `type`, `description`, `key_features`, `breadcrumb[]` {`label`, `url`}, `categories[]`, `images[]`, `packaging`, `format`, `origin`, `nutriscore`, `ecoscore`, `regulated_name`, `ingredients`, `allergens[]`, `nutrition` {`per_100`, `per_portion`: {`label`, `values[]` {`nutrient`, `quantity`, `daily_value_pct`}}}, `storage`, `advice`, `characteristics[]` {`name`, `values`}, `weights[]` {`type`, `value`, `unit`}, `flags`, `price`, `unit_price`, `unit_price_label`, `unit`, `tax_note`, `available`, `low_stock`, `max_quantity`, `promotion`, `seller`, `offers[]`, `more_offers_count`, `rating` {`average`, `count`, `distribution` (percent per star)}, `store`, `price_scope`, `country`, `language`, `currency`. On ar the market item plus `description`, `categories`, `images`, `measurement_unit`, `product_type`, `origin`, `price_valid_until`; on ro and be plus `description`, `breadcrumb`, `images`.
- **reviews** - `ean`, `sort`, `rating`, `limit`, `offset`, `total`, `reviews[]` {`author`, `rating`, `title`, `text`, `reviewed_at`, `purchased_at`, `source`}, `count`, `has_more`.
- **suggestions** - `query`, `suggestions[]` {`text`, `url`}, `categories[]` {`category`, `text`, `url`}, `count`.
- **stores** - `postal_code`, `lat`, `lng`, `page`, `limit`, `service`, `count`, `stores[]` {`id`, `store_ref`, `pickup_refs[]` {`ref`, `name`, `type`, `status`}, `name`, `banner`, `format`, `distance_km`, `address` {`line1`, `line2`, `postal_code`, `city`, `region`, `country_code`}, `lat`, `lng`, `open_today`, `opening_today[]` {`opens`, `closes`}, `slug`, `store_url`}, `filters` {`services[]`}.
- **store-availability** - `ean`, `postal_code`, `count`, `available_count`, `note`, `stores[]` {`available`, `distance_km`, `store` {`id`, `ref`, `pickup_refs`, `name`, `banner`, `format`, `address`, `lat`, `lng`, `phone`, `opening_hours`, `drive_hours`, `slug`, `store_url`}}.
- **store** - `store` {`id`, `store_ref`, `pickup_refs`, `name`, `banner`, `format`, `type`, `status`, `address`, `lat`, `lng`, `phone`, `services[]` {`category`, `name`}, `open_today`, `opening_hours`, `drive_hours` (per weekday: [{`opens`, `closes`}]), `has_delivery`, `has_express_delivery`, `next_slots[]` {`pickup_ref`, `starts_at`, `ends_at`}, `nearest_stores[]` {`id`, `name`, `banner`, `slug`, `store_url`}, `slug`, `store_url`}, `fuel` ({`updated_at`, `prices[]` {`fuel`, `code`, `price_per_litre`, `updated_at`}} or null).

## Guardrails

- Price scope: always say whether a price is carrefour.fr's national online price (`store: "national"`) or one store's shelf price (`store` set to a ref), and name the store. Prices and assortment differ by store.
- Promotions: `price` is the regular one-item price. `discounted_price` and `initial_price` cover `quantity` items; null means the site did not price the deal (multi-buys such as "Le 2ème à -50%", catalogue offers, many card offers): quote the label and dates and do not compute a price. `loyalty_only: true` offers need the Carrefour loyalty card; never present them as the price for everyone.
- Unit price: compare products with `unit_price` and its `unit`, not with `price`. Marketplace items (`type: "marketplace"`) are third-party offers, usually with no unit price; keep them out of Carrefour price comparisons unless the user asks.
- Language: product data is in the market's language as the site writes it. Translate in your answer if the user wants, but quote titles, labels, ingredients and allergens as returned.
- Allergens and nutrition come from the label text on the site: quote them as written and tell the user to check the pack for an allergy decision. Never infer an allergen that is not listed.
- Store availability is yes / no only, with no price and no unit count. Never estimate stock.
- Fuel prices exist only at stores with a fuel station; give each price with its `updated_at`.
- Reviews: quote text verbatim in French with its rating and date; the author is a public first name and initial, never try to identify them.
- There is no price history: poll and store results yourself.
- Not covered: product Q&A, the printed leaflet / catalogue as a document, delivery or drive slot booking, cart and checkout, loyalty account data (Carte Carrefour, Club or PASS balances), price history, and Carrefour Spain, Italy, Poland, Brazil, Taiwan and the Middle East sites.
- carrefour.fr's terms of use (updated March 6, 2020) prohibit extracting or reusing its databases "without the prior express authorization of Carrefour France" (Art. 49), and product photographs belong to Carrefour France or its licensors (Art. 44). This is not legal advice; the user is responsible for checking the terms for their use case.
- Never fabricate prices, promotions, Nutri-Scores, ingredients, stock or reviews. Only return what the API returned, with the product `url` or `ean`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no `query`; an endpoint other than search or product with `country` `ar`, `ro` or `be`; `language` on a market other than `be`; `store`, `seller` or a carrefour.fr filter (`brand`, `promotion`, `nutriscore`, `organic`, `carrefour_brands`, `min_price`, `max_price`) on ar, ro or be; a sort the market does not honor (anything but relevance on be); `ean` on ro or be (use `url`); a product URL from another Carrefour site than `country`; a `store` that is not digits; an `ean` that is not 8-14 digits; a postal code that is not 5 digits or is unknown (send a nearby code, or `lat` and `lng`); `lat` without `lng`; an unknown `service`; `promotion` on `/promotions` (use `type`); `limit` outside 1-50 on reviews or 1-20 on stores; a `page` outside its range.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such product, store ref or store page. Not-founds are charged (1 credit, 2 on Belgium search and product): take EANs, URLs, refs and slugs from a previous answer rather than guessing them. A keyword with no match is a normal `200` (`results_type: "fallback"` or `total: 0`).
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api).
- `502` means Carrefour was temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Carrefour is busy: wait the `Retry-After` seconds (5) and send it again. Not charged.

## SDKs

```bash
pip install scavio==0.50.0
npm install scavio@0.51.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.carrefour.search({ query: "nutella", sort: "unit_price_low_to_high" });
const { data: atStore } = await scavio.carrefour.search({ query: "nutella", store: "840093" });
const { data: item } = await scavio.carrefour.product({ ean: "3017620422003" });
const { data: reviews } = await scavio.carrefour.reviews({ ean: "8006530256179", sort: "lowest_rated" });
const { data: dairy } = await scavio.carrefour.category({ path: "/r/cremerie" });
const { data: deals } = await scavio.carrefour.promotions({ type: "loyalty" });
const { data: stores } = await scavio.carrefour.stores({ postal_code: "69003" });
const { data: avail } = await scavio.carrefour.storeAvailability({ ean: "3017620422003", postal_code: "69003" });
const { data: store } = await scavio.carrefour.store({ slug: "venissieux" });
const { data: be } = await scavio.carrefour.search({ query: "melk", country: "be", language: "nl" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.carrefour.search(...)`, `client.carrefour.product(...)`, `client.carrefour.reviews(...)`, `client.carrefour.category(...)`, `client.carrefour.promotions(...)`, `client.carrefour.suggestions(...)`, `client.carrefour.stores(...)`, `client.carrefour.store_availability(...)` and `client.carrefour.store(...)`.

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_carrefour`, `get_carrefour_product`, `get_carrefour_reviews`, `get_carrefour_category`, `get_carrefour_promotions`, `get_carrefour_suggestions`, `find_carrefour_stores`, `get_carrefour_store_availability` and `get_carrefour_store`. Carrefour is opt-in: add `carrefour` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.48.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,carrefour"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/carrefour-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [product](https://scavio.dev/docs/carrefour-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [reviews](https://scavio.dev/docs/carrefour-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [category](https://scavio.dev/docs/carrefour-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [promotions](https://scavio.dev/docs/carrefour-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [suggestions](https://scavio.dev/docs/carrefour-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [stores](https://scavio.dev/docs/carrefour-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [store availability](https://scavio.dev/docs/carrefour-store-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api), [store](https://scavio.dev/docs/carrefour-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api). Overview: [Carrefour API](https://scavio.dev/carrefour-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=carrefour-api).
