# Maisons du Monde API - Promo Prices, Product Data, Reviews, Store Stock

Read Maisons du Monde (furniture and home decor) product data on maisonsdumonde.com, market by market: keyword search and category grids with the site's own sorts and filters, one product in full by reference or link, sale events (Black Friday, Seconde Chance) and any category's discounted items, customer reviews with a star histogram, stores near a postcode, one store's phone, hours and services, one item's stock at one store with the delivery options, and marketplace sellers with their catalogs. All 9 endpoints return structured JSON and cost 1 credit per call.

**The job this skill is for: Maisons du Monde promo prices.** Every item carries `price` (what the site charges now) next to `was_price` (the crossed-out price shown next to a discount) and `discount_percent` (the page's own percent off), plus `sold_by`: `mdm` for items Maisons du Monde sells itself, `marketplace` for third-party sellers (France, Germany, Spain and Italy). Maisons du Monde shows no 30-day lowest price and no price history, so neither is returned: to see whether a price really moved, read the same items on a schedule and store each reading with its time and market. Black Friday 2026 is November 27; the French winter soldes run from 2027-01-06 to 2027-02-02.

**Prices by country: the euro markets shared one price, Switzerland is priced separately in CHF.** The same product reference serves every market. Measured on 2026-11-14 on 6 products, every euro market we read gave the same price for the same product, and Switzerland had its own CHF price:

| Product | Euro markets read | EUR price (was) | Switzerland |
|---|---|---|---|
| 204172 round gilded mirror | all euro markets | 37.45 (74.99) | CHF 45.95 (91.90) |
| 254909 compressed 3-seat sofa | all euro markets | 479.20 (599) | CHF 527.20 (659) |
| 186339 Nio 2-seat sofa bed | all euro markets | 339 | CHF 339 |
| 129991 coffee table | all euro markets | 271.20 (339) | not sold in Switzerland |
| 230448 corner sofa | `be`, `lu` | 1699 | CHF 1699 |
| 166180 3/4-seat corner sofa | `es`, `it`, `pt` | 199.50 (399) | not read |

That is 6 products on one day, not a rule: read each market you care about and compare. In Switzerland the number is sometimes the same as the euro price and sometimes not, but it is always in CHF: never compare a CHF price with a EUR price without converting it yourself, with the rate and its date.

Maisons du Monde publishes no public product or price API. Its marketplace runs a seller API for approved third-party sellers, who use it to publish and update their own products, offers and stock; product feeds go to approved affiliates through affiliate networks.

See also: for IKEA prices by country use `ikea-api`; for Wayfair prices and the was price use `wayfair-api`; for Ashley Furniture sale prices use `ashley-furniture-api`; for Carrefour France grocery prices use `carrefour-api`; for the cross-retailer view of one product use `google-shopping-api`.

## When to trigger

Use this skill when the user asks to:
- Check Maisons du Monde promo prices: the current price next to the crossed-out price and the discount, per market
- Track Maisons du Monde prices through Black Friday and the soldes (poll and store price, was price, discount, badges and market)
- Compare one Maisons du Monde product's price across countries (France, Belgium, Luxembourg, the Netherlands, Germany, Spain, Italy, Portugal, Switzerland)
- Split Maisons du Monde's own items from marketplace sellers' items, or read a marketplace seller's profile and catalog
- Search Maisons du Monde by keyword, sorted by price or customer rating, filtered by price range, discount, stock, rating, color, material, style or brand
- Browse a Maisons du Monde category, or list the Black Friday, Seconde Chance (used and returned items) or a category's discounted items
- Read one Maisons du Monde product in full: exact online stock, variants, dimensions, materials, made-in country, assembly and dimension PDFs, review summary, Q&A
- Read Maisons du Monde customer reviews with the star histogram and per-criterion scores (style, value for money, comfort)
- Find Maisons du Monde stores near a postcode with hours, read a store's phone and services, or check an item's stock at one store
- Read the home delivery from-price and the click and collect status for an item

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits: 50 calls, since every endpoint here costs 1 credit.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In build testing calls took 2.1 to 21 seconds; in the captures stores took 24 seconds, availability 37 seconds and one store call 72 seconds. A failed attempt is retried once, so a slow call can take up to about 2 minutes. Set a client timeout of at least 150 seconds and do not fire many calls at once (a busy moment answers `503` with `Retry-After`).

| Endpoint | Markets | Credits | What it returns |
|---|---|---|---|
| `POST /api/v1/maisonsdumonde/search` | all 9 | 1 | 40 items per page for a keyword, with the exact total, sorts, facets and the applied filters; a keyword that names a category answers that category and says so in `redirected_to` |
| `POST /api/v1/maisonsdumonde/product` | all 9 | 1 | One product by `id` or `url`: prices, stock with the exact online quantity, seller (marketplace items), variants, dimensions, weight, materials, made-in, composition, assembly, documents, images, breadcrumbs, description, rating, review summary, Q&A and `markets` (the same product on every other market) |
| `POST /api/v1/maisonsdumonde/category` | all 9 | 1 | One category's grid by `category` hash or `category_url`, with the search sorts and filters, plus `category` {`id`, `name`, `url`, `breadcrumbs`} |
| `POST /api/v1/maisonsdumonde/deals` | all 9 | 1 | A sale event's grid: `black_friday` (default, every market while it runs), `second_chance` (`fr`, used and returned items with their condition), or a category's discounted items |
| `POST /api/v1/maisonsdumonde/reviews` | all 9 | 1 | A product's rating, review count, star histogram and reviews (rating, text, date, author, source market, criteria scores, brand reply, images), with `next_cursor` |
| `POST /api/v1/maisonsdumonde/stores` | `fr`, `be`, `de`, `es`, `it`, `pt`, `ch` | 1 | Up to 10 stores nearest a postcode with address, coordinates, distance, open now, hours per day and click and collect level |
| `POST /api/v1/maisonsdumonde/store` | `fr`, `be`, `de`, `es`, `it`, `pt`, `ch` | 1 | One store by `store_id` or `url`: address, phone, coordinates, hours, services, click and collect level, today's hours |
| `POST /api/v1/maisonsdumonde/availability` | `fr`, `be`, `de`, `es`, `it`, `pt`, `ch` | 1 | One Maisons du Monde item at one store: in stock, quantity, the site's stock text, display model, click and collect, on shelf, and the market's delivery options with the home delivery from-price |
| `POST /api/v1/maisonsdumonde/seller` | `fr`, `de`, `es`, `it` | 1 | One marketplace seller by `seller_id` or `url`: rating, review count, orders, member since, order approval, shipping, returns, description, plus the seller's catalog as a grid |

## Markets

Every endpoint takes `country` (lowercase, default `fr`) and `language` (default the market's first language). Data comes in the market's language and currency: French names on `fr`, Dutch on `nl`, German on `de`, Italian on `it` and on `ch` with `language: "it"`. Quote names and labels as returned; translate them for the user only in your own words around the data. Every `data` echoes `country`, `language` and `currency`.

| `country` | Languages | Currency | Marketplace sellers | Stores, store, availability |
|---|---|---|---|---|
| `fr` France | `fr` | EUR | yes | yes |
| `be` Belgium | `fr`, `nl` | EUR | no | yes |
| `lu` Luxembourg | `fr` | EUR | no | no |
| `nl` Netherlands | `nl` | EUR | no | no |
| `de` Germany | `de` | EUR | yes | yes |
| `es` Spain | `es` | EUR | yes | yes |
| `it` Italy | `it` | EUR | yes | yes |
| `pt` Portugal | `pt` | EUR | no | yes |
| `ch` Switzerland | `fr`, `de`, `it` | CHF | no | yes |

- Search, product, category, deals and reviews: all 9 markets (12 market-languages).
- Stores, store and availability: `fr`, `be`, `de`, `es`, `it`, `pt`, `ch`. The store finder has no results on `nl` and `lu`.
- Seller, and the `seller` / `sold_by` filters: `fr`, `de`, `es`, `it`. On the other markets every item is sold by Maisons du Monde.
- A market outside an endpoint's list, or a `language` the market does not serve, answers `400` before anything is charged. Maisons du Monde closed its Austrian store in 2026 and its UK business in 2023: `at`, `gb` and `uk` answer `400`.
- The catalog is much deeper on the four marketplace markets: the sofas and armchairs category held about 9,000 to 13,000 items there against about 690 on `be`, `nl`, `lu`, `pt` and `ch` in testing.

## Workflow

1. **Find products:** `/search` with `query` in the market's language (`table`, `canapé` on `fr`; `sofa` on `de`; `divano` on `it`). Read `items[].id` for `/product`, `/reviews` and `/availability`. If `redirected_to` is set, the keyword named a category: its `category_id` works on `/category`.
2. **Browse and filter:** `/category` with `category` (the hash at the end of a `/c/` URL, optionally with its name: `canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f`) or `category_url`. The hash is the same on every market, so a category from `fr` works on `de`. Filter with `price_min` / `price_max`, `on_sale`, `min_discount`, `in_stock`, `min_rating`, `color`, `material`, `style`, `brand` (option ids from `facets`), and any other facet through `filters`.
3. **One product in full:** `/product` with `id` (digits for Maisons du Monde items, `M` + digits for marketplace items) or the product `url`. `markets[]` lists the same product's page on every other market and language.
4. **Prices by country:** call `/product` with the same `id` and a different `country` (and `language`). A product not sold in a market answers `404` (charged), so read `markets[]` first and call only the markets listed there.
5. **Deals:** `/deals` with `event` `black_friday` or `second_chance` (`fr`), or with `category` / `category_url` for that category's discounted items (add `min_discount` for a deeper cut). The grid takes the same sorts and filters.
6. **Reviews:** `/reviews` with `id`, `sort` and `limit` (up to 30); pass `next_cursor` back as `cursor` with the same `sort` for the next page.
7. **Store stock:** `/stores` with a `postcode`, then `/availability` with the item `id` and a `stores[].id` as `store_id`. `/store` with a `stores[].id` adds the phone and services.
8. **Marketplace:** `/product` on a marketplace item returns `seller.id`; `/seller` with that `seller_id` returns the seller's profile, `seller.code` and its catalog. Pass `seller.code` as `seller` on search, category or deals for that seller's items, or `sold_by: "mdm"` for Maisons du Monde's own items.
9. **Promo-price monitoring:** poll `/search`, `/category` or `/deals` (40 items per call) or `/product` on a schedule. Store `id`, `country`, `language`, the time, `price`, `was_price`, `discount_percent`, `currency`, `badges` and `sold_by` per run. There is no price history endpoint.

## Parameters

### Shared by search, category, deals and the seller catalog

| Parameter | Type | Default | Description |
|---|---|---|---|
| `country` | string | `fr` | See Markets |
| `language` | string | the market's first | `fr`, `nl`, `de`, `es`, `it` or `pt`, among the market's languages |
| `page` | integer | 1 | 1-based, 40 items per page, up to 250. A page past the last returns no items and a note |
| `sort` | string | `relevance` | `relevance`, `price_asc`, `price_desc` or `rating` (customer rating). The site has no newest, best-seller or discount sort |
| `price_min` / `price_max` | number | none | Price range in the market's currency |
| `on_sale` | boolean | none | Only discounted items |
| `min_discount` | integer | none | `20`, `30`, `40` or `50`: at least that percent off |
| `in_stock` | boolean | none | Only items in stock online |
| `min_rating` | integer | none | `5` (five stars), `4` or `3` (that many stars and up) |
| `color`, `material`, `style`, `brand` | string or list | none | 1 to 5 option ids from that facet's `options[].id` (facets `c`, `f`, `st`, `bra`), for example `brand: "BRAND_MAISONS_DU_MONDE"` |
| `seller` | string | none | One marketplace seller's items: `seller.code` from `/seller` or a Seller facet (`se`) option id, for example `BESTMOBILIER`. `fr`, `de`, `es`, `it` |
| `sold_by` | string | none | `mdm`: only items Maisons du Monde sells itself. `fr`, `de`, `es`, `it`. Not with `seller` |
| `filters` | object | none | Any other facet: `{"<facets[].id>": ["<options[].id>"]}`, for example `{"nbs": ["CAPACITY_2_places"]}`; dimension ranges `dd`, `dh`, `dw` as `"min-max"` in cm. Up to 10 keys, 5 values each. A facet with a named parameter above must use that parameter |

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | Keywords in the market's language (1-200 chars) |

Plus the shared parameters. On `de`, keyword results are not sorted: the German site answers none when sorted, so a sorted `de` search comes back in relevance order with a note (sorting works on `de` category and deals).

### Product (`/product`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `id` | string | one of | A product reference (`items[].id`): `186339`, or `M24132196` for a marketplace item |
| `url` | string | one of | A product page of any market; its market and language are used unless `country` / `language` are sent |
| `country`, `language` | string | `fr` | As above |

### Category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category` | string | one of | A category hash (`n` + 39 hex characters, or 32 hex), optionally with its name: `canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f`, or `redirected_to.category_id` of a search |
| `category_url` | string | one of | A `/c/` category page of any market; filters in it are kept. A themed page (`/vc/`) answers `400` |

Plus the shared parameters.

### Deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `event` | string | `black_friday` | `black_friday` (every market while it runs) or `second_chance` (`fr`: used and returned items) |
| `category` / `category_url` | string | none | Instead of `event`: that category's discounted items (on sale, or `min_discount` when sent) |

Plus the shared parameters. An event that is not running answers `404`.

### Reviews (`/reviews`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `id` | string | required | A Maisons du Monde product reference (digits) |
| `sort` | string | `newest` | `newest`, `rating_desc` or `rating_asc`. There is no star filter |
| `limit` | integer | 10 | Reviews per page, 1 to 30 |
| `cursor` | string | none | `next_cursor` of the previous answer (keep the same `sort`) |
| `country`, `language` | string | `fr` | The language the reviews are shown in |

### Stores (`/stores`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `postcode` | string | required | A postcode of the market: 5 digits on `fr`, `de`, `es`, `it`; 4 on `be`, `ch`; `1000-001` on `pt` |
| `limit` | integer | 10 | Stores to return, nearest first, 1 to 10 |
| `country`, `language` | string | `fr` | Stores markets only |

### Store (`/store`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `store_id` | string | one of | `stores[].id`, for example `41` |
| `url` | string | one of | A store page (`stores[].url`) |
| `country`, `language` | string | `fr` | The store's market |

### Availability (`/availability`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `id` | string | required | A Maisons du Monde item reference (digits). Marketplace items (`M...`) answer `400`: they ship from their seller and are not stocked in stores |
| `store_id` | string | required | `stores[].id` from `/stores` on the same market |
| `country`, `language` | string | `fr` | Stores markets only |

### Seller (`/seller`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `seller_id` | string | one of | A marketplace seller id (a product's `seller.id`), for example `2066` |
| `url` | string | one of | A seller page (`seller.url`) |
| `page`, `sort` | | | As on search, for the catalog |
| `country`, `language` | string | `fr` | `fr`, `de`, `es`, `it` |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "table"}'
```

Captured `data` (France, 2026-11-14; 1 of 40 items and 3 of 28 facets shown, facet options trimmed to 2):

```json
{
  "query": "table",
  "items": [
    {
      "position": 1,
      "id": "166560",
      "name": "Table à manger extensible, L160/230 cm",
      "collection": "Bronx",
      "brand": "Maisons du Monde",
      "url": "https://www.maisonsdumonde.com/FR/fr/p/table-a-manger-extensible-l160-230-cm-bronx-166560.htm",
      "image": "https://medias.maisonsdumonde.com/images/f_auto,q_auto,w_350/v1/img/166560_0/table-a-manger-extensible-l160-230-cm-bronx.jpg",
      "price": 319.2,
      "was_price": 399,
      "discount_percent": 20,
      "currency": "EUR",
      "badges": ["BLACK FRIDAY"],
      "rating": 4.08,
      "review_count": 304,
      "color_count": null,
      "sold_by": "mdm",
      "offer_id": null,
      "sponsored": false,
      "condition": null,
      "store_only": false,
      "purchase_status": "purchasable"
    }
  ],
  "count": 40,
  "sponsored_count": 0,
  "total": 51822,
  "page": 1,
  "page_size": 40,
  "total_pages": 75,
  "sort": "relevance",
  "sorts_offered": [
    {"sort": "relevance", "label": "Notre recommandation"},
    {"sort": "price_asc", "label": "Prix croissant"},
    {"sort": "price_desc", "label": "Prix décroissant"},
    {"sort": "rating", "label": "Avis client"}
  ],
  "requested_filters": {},
  "applied_filters": [],
  "facets": [
    {"id": "p", "name": "Prix", "type": "range", "min": 2, "max": 1299},
    {"id": "disc", "name": "Taux de réduction", "type": "options", "options": [{"id": "all", "label": "Toutes les promotions", "count": 22698}, {"id": "20-100", "label": "-20% et plus", "count": 14970}], "option_count": 5},
    {"id": "se", "name": "Vendeur", "type": "options", "options": [{"id": "MAISONS-DU-MONDE", "label": "Maisons du Monde", "count": 2614}, {"id": "HOME-PARTNERS-FRANCE", "label": "Home Partners France", "count": 1680}], "option_count": 286}
  ],
  "redirected_to": null,
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

`count` is the organic items on the page; sponsored marketplace tiles sit inside `items[]` with `sponsored: true` and are counted in `sponsored_count` (the captured France sofas category and Black Friday pages carried 16 each, so `items[]` held 56). Drop `sponsored: true` items when you rank or count results. A marketplace tile in the German "sofa" search, same day:

```json
{"position": 4, "id": "M23165516", "name": "Sofa 3 Sitzer, mit Schlaffunktion, in Pet Friendly Cord-Stoff, Beige", "collection": "Napi", "brand": "KONSIMO", "price": 899, "was_price": 1499, "discount_percent": 40, "currency": "EUR", "sold_by": "marketplace", "offer_id": "8400766", "sponsored": true}
```

(`url`, `image` and the remaining fields omitted.) Grid tiles say `sold_by` but not the seller's name: call `/product` for `seller`.

### Product

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/product \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "186339"}'
```

Captured `data` (France, 2026-11-14; 2 of 8 variants, 2 of 5 dimensions, 1 of 12 images, 2 of 5 breadcrumbs, 1 of 3 review summary sections, 1 of 4 questions and 3 of 12 markets shown; description, composition, review summary and answer text shortened; `characteristics`, `wood_and_finishes`, `assembly`, `categories` and `short_description` omitted):

```json
{
  "id": "186339",
  "gtin13": "3611871863396",
  "name": "Canapé convertible 2 places vert d'eau",
  "collection": "Nio",
  "brand": "Maisons du Monde",
  "url": "https://www.maisonsdumonde.com/FR/fr/p/canape-convertible-2-places-vert-d-eau-nio-186339.htm",
  "price": 339,
  "was_price": null,
  "discount_percent": null,
  "currency": "EUR",
  "eco_participation": 8.5,
  "badges": [],
  "stock": {"status": "purchasable", "quantity": 117},
  "store_only": false,
  "sold_by": "mdm",
  "seller": null,
  "offer_id": null,
  "condition": null,
  "variants": [
    {"dimension": "color", "value": "Gris anthracite", "name": "Canapé convertible 2 places gris anthracite", "id": "186366", "url": "https://www.maisonsdumonde.com/FR/fr/p/canape-convertible-2-places-gris-anthracite-nio-186366.htm", "price_difference": null},
    {"dimension": "model", "value": "1 place 109 cm", "name": "1 place 109 cm", "id": "175580", "url": "https://www.maisonsdumonde.com/FR/fr/p/canape-convertible-1-place-vert-d-eau-nio-175580.htm", "price_difference": -110}
  ],
  "dimensions": [{"label": "Longueur", "value": "150", "unit": "cm"}, {"label": "Dimensions du colis", "value": "152 x 134.5 x 28", "unit": "cm"}],
  "weight": {"value": 34.4, "unit": "kg"},
  "materials": {"main": "Bois", "other": "PU - Polyuréthane, PES - Polyester"},
  "made_in": "Chine",
  "composition": "Revêtement : tissu 100% polyester, coloris vert d'eau, non déhoussable\nStructure : pin massif et contreplaqué\n...",
  "attributes": [],
  "care": null,
  "documents": [
    {"type": "dimensions", "label": "Fiche des dimensions", "url": "https://assets.maisonsdumonde.com/technical-docs/186331-186336-186337-186338-186339-186366-186367-209539-216177-216178-219563-221261_fiche-technique.pdf"},
    {"type": "assembly", "label": "Notice de montage", "url": "https://assets.maisonsdumonde.com/technical-docs/186339-186366-186367-186331-186336-186337-186338-221261_fiche-de-montage.pdf"}
  ],
  "images": ["https://medias.maisonsdumonde.com/images/ar_1:1,c_fill,f_auto,q_auto,w_1920/v1/img/186339_0/canape-convertible-2-places-vert-d-eau.jpg"],
  "breadcrumbs": [
    {"name": "Canapés", "url": "https://www.maisonsdumonde.com/FR/fr/c/canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f"},
    {"name": "Canapés droits", "url": "https://www.maisonsdumonde.com/FR/fr/c/canapes-droits-nb37d60b470cf6361801035497c9b0fdd2481361"}
  ],
  "description": "Le canapé convertible Nio en tissu vert clair apporte une touche de fraîcheur à votre intérieur tout en offrant une solution de couchage ponctuel. ...",
  "rating": 4,
  "review_count": 830,
  "review_summary": {"title": "L'avis de nos clients", "sections": [{"key": "positivePoints", "title": "Points positifs", "text": "Les clients sont particulièrement séduits par plusieurs aspects de ce canapé. ..."}]},
  "questions": [{"question": "Les pieds de support pour le mode lit sont-ils intégrés au canapé convertible NIO ?", "answer": "Oui, des pieds de support supplémentaires sont directement intégrés à la structure du canapé NIO. ..."}],
  "markets": [
    {"country": "ch", "language": "fr", "url": "https://www.maisonsdumonde.com/CH/fr/p/canape-convertible-2-places-vert-d-eau-nio-186339.htm"},
    {"country": "es", "language": "es", "url": "https://www.maisonsdumonde.com/ES/es/p/sofa-cama-de-2-plazas-de-tela-verde-agua-nio-186339.htm"},
    {"country": "be", "language": "nl", "url": "https://www.maisonsdumonde.com/BE/nl/p/tweepersoons-slaapbank-in-aquagroen-nio-186339.htm"}
  ],
  "notes": [
    "Maisons du Monde shows no 30-day lowest price, so none is returned; was_price is the site's crossed-out price. No price history: poll for changes.",
    "Home delivery is a from-price per product and market: call availability (delivery). Reviews (pooled across markets, translated): call reviews.",
    "eco_participation is the French furniture recycling fee included in price (shown on fr only)."
  ],
  "country": "fr",
  "language": "fr"
}
```

`stock.quantity` is the exact online stock. `price_difference` is a variant's price against this item in the market's currency (the 1-seat model is 110 less); `null` means the same price. This product's `markets` listed 12 market-languages. `eco_participation` is part of `price`, not added to it. A marketplace product (`M24132196` on `fr`, same day) carried `sold_by: "marketplace"`, an `offer_id`, and `seller` {`id`: `2066`, `name`: `BESTMOBILIER`, `url`, `rating`: 4.06, `orders`: 61386, `member_since`: `2020-04-02`} at EUR 1099 with `was_price` 1399.

### Category

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category": "canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f"}'
```

Captured `data` (France, 2026-11-14; 1 of 56 items shown, `sorts_offered` and facets omitted):

```json
{
  "category": {
    "id": "n4dc562d7bb509362a3a2102db4cbf90b6454f1f",
    "name": "Canapés",
    "url": "https://www.maisonsdumonde.com/FR/fr/c/canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f",
    "breadcrumbs": [
      {"name": "Accueil", "url": "https://www.maisonsdumonde.com/FR/fr"},
      {"name": "Canapés et fauteuils", "url": "https://www.maisonsdumonde.com/FR/fr/c/canapes-et-fauteuils-ncf50f4ed873ed30c5529ea40ee5951ea0b09e3e"},
      {"name": "Canapés", "url": "https://www.maisonsdumonde.com/FR/fr/c/canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f"}
    ]
  },
  "items": [
    {
      "position": 1,
      "id": "254909",
      "name": "Canapé compressé 3 places vert kaki",
      "collection": "Open",
      "brand": "Maisons du Monde",
      "url": "https://www.maisonsdumonde.com/FR/fr/p/canape-compresse-3-places-vert-kaki-open-254909.htm",
      "image": "https://medias.maisonsdumonde.com/images/f_auto,q_auto,w_350/v1/img/254909_0/canape-compresse-3-places-vert-kaki.jpg",
      "price": 479.2,
      "was_price": 599,
      "discount_percent": 20,
      "currency": "EUR",
      "eco_participation": 18.5,
      "badges": ["Nouveau"],
      "rating": null,
      "review_count": null,
      "color_count": null,
      "sold_by": "mdm",
      "offer_id": null,
      "sponsored": false,
      "condition": null,
      "store_only": false,
      "purchase_status": "purchasable"
    }
  ],
  "count": 40,
  "sponsored_count": 16,
  "total": 18337,
  "page": 1,
  "page_size": 40,
  "total_pages": 250,
  "sort": "relevance",
  "requested_filters": {},
  "applied_filters": [],
  "notes": ["Marketplace items (sold_by marketplace) are sold by third-party sellers; grid tiles do not name the seller: call product for seller."],
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

`total_pages` stops at 250 (10,000 items) even when `total` is larger: narrow with filters to reach the rest. To keep Maisons du Monde's own items, send `"sold_by": "mdm"`.

### Deals

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/deals \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"event": "black_friday"}'
```

Captured `data` (France, 2026-11-14; 1 of 56 items shown, `sorts_offered` and facets omitted):

```json
{
  "event": {"type": "black_friday", "name": "Black Friday", "url": "https://www.maisonsdumonde.com/FR/fr/c/black-friday-n4b664e720704d0157d72e4afb6be43ac6fb9563", "category_id": "n4b664e720704d0157d72e4afb6be43ac6fb9563"},
  "items": [
    {
      "position": 1,
      "id": "209577",
      "name": "Table de chevet en bois de paulownia et tiroir blanc, L42 cm",
      "collection": "Spring",
      "brand": "Maisons du Monde",
      "url": "https://www.maisonsdumonde.com/FR/fr/p/table-de-chevet-en-bois-de-paulownia-et-tiroir-blanc-l42-cm-spring-209577.htm",
      "price": 31.95,
      "was_price": 39.99,
      "discount_percent": 20,
      "currency": "EUR",
      "eco_participation": 0.32,
      "badges": ["BLACK FRIDAY"],
      "rating": 3.71,
      "review_count": 156,
      "color_count": null,
      "sold_by": "mdm",
      "offer_id": null,
      "sponsored": false,
      "condition": null,
      "store_only": false,
      "purchase_status": "purchasable"
    }
  ],
  "count": 40,
  "sponsored_count": 16,
  "total": 107344,
  "page": 1,
  "page_size": 40,
  "total_pages": 250,
  "sort": "relevance",
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

(`image`, `requested_filters`, `applied_filters` and `notes` omitted.) Black Friday on `fr` counted 107,344 items, marketplace included; on `de` it counted 996 and on `ch` 998 in build testing. `second_chance` on `fr` counted 307 used and returned items, each with a `condition` grade (for example `satisfying`) and the `Seconde Chance` badge.

### Reviews

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/reviews \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "186339"}'
```

Captured `data` (France, 2026-11-14; 1 of 10 reviews shown):

```json
{
  "product_id": "186339",
  "sort": "newest",
  "rating": 4.07,
  "review_count": 830,
  "rating_histogram": {"1": 44, "2": 55, "3": 102, "4": 223, "5": 406},
  "criteria": null,
  "reviews": [
    {
      "rating": 5,
      "text": "confortable, simple à monter (il n'y a que deux pieds à fixer), design agréable, excellent rapport qualité-prix, le support à l'achat est précis",
      "date": "2026-11-02",
      "author": "Lucia V.",
      "country": "Italie",
      "source_market": "it",
      "syndicated": true,
      "criteria": [{"label": "Style", "rating": 5}, {"label": "Rapport qualité / prix", "rating": 4}, {"label": "Confort", "rating": 5}],
      "brand_reply": null,
      "images": []
    }
  ],
  "next_cursor": "eyJzb3J0IjpbMTc5MTYyNTYxNjAwMCwiYjM4YjMyN2UtZWVkMy00NzEwLThjOGMtODYwNjdkN2NlNTg1Il0sImhhc2giOiI3ZjBiYTUzZSJ9",
  "notes": [
    "Reviews are pooled across every Maisons du Monde market and shown translated into the request language; source_market is where a review was written (syndicated true). rating is computed from rating_histogram.",
    "Authors are the display names the site shows; e-mail addresses and long numbers in review text are removed."
  ],
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

This review was written in Italy and is shown in French. The same product read on `de` and on `ch` in Italian returned the same 830 reviews in German and Italian. Reviews carry no id, no title and no verified-buyer flag.

### Stores, store and store stock

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/stores \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"postcode": "75011"}'
```

Captured `data` (France, 2026-11-14; 1 of 10 stores and 2 of 7 days shown):

```json
{
  "postcode": "75011",
  "stores": [
    {
      "id": "125",
      "name": "Paris - Faubourg St Antoine (12ème)",
      "address": "32 Rue du Faubourg Saint-Antoine",
      "postcode": "75012",
      "city": "Paris",
      "country": "fr",
      "lat": 48.8523423,
      "lng": 2.3716431,
      "distance_km": 1,
      "url": "https://www.maisonsdumonde.com/FR/fr/s/paris-faubourg-st-antoine-12eme-125",
      "open_now": true,
      "hours_today": null,
      "hours": [{"day": "saturday", "slots": [{"open": "10:00", "close": "19:30"}]}, {"day": "sunday", "slots": []}],
      "click_collect": "standard"
    }
  ],
  "count": 10,
  "notes": ["Phone numbers and in-store services are on each store's page: call store with stores[].id or stores[].url."],
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

Then the stock of item 204172 at store 125:

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/availability \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "204172", "store_id": "125"}'
```

Captured `data` (France, 2026-11-14, complete):

```json
{
  "product_id": "204172",
  "store": {"id": "125", "name": "Paris - Faubourg St Antoine (12ème)", "postcode": "75012", "city": "Paris"},
  "in_stock": false,
  "quantity": 0,
  "stock_text": "Stock indisponible",
  "display_model": false,
  "click_collect": {"available": false, "text": ["Stock indisponible", "Retrait indisponible"]},
  "on_shelf": {"available": false, "text": ["Stock indisponible", "Retrait indisponible"]},
  "delivery": [
    {"type": "home", "title": "Livraison à domicile", "available": true, "availability_text": "Disponible", "from_price": 6.9, "currency": "EUR", "price_text": "à partir de 6,90 €"},
    {"type": "store_pickup", "title": "Retrait en magasin", "available": false, "availability_text": "Indisponible", "from_price": null, "currency": null, "price_text": null},
    {"type": "in_store", "title": "En rayon en magasin", "available": null, "availability_text": null, "from_price": null, "currency": null, "price_text": null}
  ],
  "notes": ["Home delivery is a from-price per product and market (the site's own wording in price_text); the exact cost for a postcode is only shown in the cart and is not returned."],
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

In build testing the Nio sofa bed 186339 at the Marseille store (41) answered `quantity` 1 with `stock_text` "Modèle exposé en magasin" (`display_model: true`: the display piece only). The home delivery from-price differs by market for the same item: 6.90 EUR on `fr` and 7.90 EUR on `es` for the mirror 204172.

And one store:

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/store \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"store_id": "41"}'
```

Captured `data` (France, 2026-11-14; 2 of 7 days shown):

```json
{
  "id": "41",
  "name": "Maisons du Monde - Marseille",
  "address": "54-56 Rue Paradis",
  "postcode": "13006",
  "city": "Marseille",
  "country": "fr",
  "phone": "+33491540555",
  "lat": 43.29180931,
  "lng": 5.37733498,
  "url": "https://store.maisonsdumonde.com/fr/fr/provence-alpes-cote-d-azur/bouches-du-rhone/marseille/maisons-du-monde-marseille-201",
  "hours": [{"day": "saturday", "slots": [{"open": "10:00", "close": "19:00"}]}, {"day": "sunday", "slots": []}],
  "services": ["CLICK & COLLECT 2H - GRATUIT", "NOS SERVICES DÉCO", "MONTAGE DE MEUBLES", "SERVICES PROFESSIONNELS", "CARTES CADEAUX", "HÔTEL MAISONS DU MONDE"],
  "click_collect": "express",
  "hours_today": "Ouvre lundi à 10:00",
  "language": "fr",
  "currency": "EUR"
}
```

### Marketplace seller

```bash
curl -X POST https://api.scavio.dev/api/v1/maisonsdumonde/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_id": "2066"}'
```

Captured `data` (France, 2026-11-14; 1 of 40 catalog items shown; `shipping.types`, `shipping.policy`, `shipping.trade_in`, `returns.how_to_return` and `description` omitted; `sorts_offered`, `requested_filters` and facets omitted):

```json
{
  "seller": {
    "id": "2066",
    "name": "BESTMOBILIER",
    "code": "BESTMOBILIER",
    "url": "https://www.maisonsdumonde.com/FR/fr/m/bestmobilier-2066",
    "rating": 4.06,
    "review_count": 3059,
    "orders": 61393,
    "member_since": "2020-04-02",
    "order_approval": {"delay": "1 heure", "rate_percent": 99.98},
    "shipping": {"label": "Livraison à domicile", "zone": "France (hors îles)", "ships_within_days": 4},
    "returns": {"withdrawal_days": 14},
    "company_city": "Neuilly sur Seine"
  },
  "items": [
    {
      "position": 1,
      "id": "M26104910",
      "name": "Lot de 2 chaises cannage   en tissu bouclette  vert kaki",
      "collection": "Luciano",
      "brand": "Best Mobilier",
      "url": "https://www.maisonsdumonde.com/FR/fr/p/lot-de-2-chaises-cannage-en-tissu-bouclette-vert-kaki-luciano-M26104910.htm",
      "price": 98,
      "was_price": 142,
      "discount_percent": 30,
      "currency": "EUR",
      "eco_participation": 2.42,
      "badges": ["BLACK FRIDAY"],
      "rating": null,
      "review_count": null,
      "color_count": 4,
      "sold_by": "marketplace",
      "offer_id": "24271517",
      "sponsored": false,
      "condition": null,
      "store_only": false,
      "purchase_status": "purchasable"
    }
  ],
  "count": 40,
  "sponsored_count": 0,
  "total": 1494,
  "page": 1,
  "page_size": 40,
  "total_pages": 38,
  "sort": "relevance",
  "applied_filters": [{"id": "se", "value": "BESTMOBILIER", "label": "BESTMOBILIER"}],
  "country": "fr",
  "language": "fr",
  "currency": "EUR"
}
```

(`image` and `notes` omitted.) The same seller read on `de` listed 35 items: a seller's catalog is per market.

### Python

```python
import time
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def mdm(endpoint, body, timeout=180):
    r = requests.post(f"{BASE}/api/v1/maisonsdumonde/{endpoint}", headers=HEADERS, json=body, timeout=timeout)
    if r.status_code == 404:
        return None  # not sold in that market (charged)
    r.raise_for_status()
    return r.json()["data"]

# One product's promo price on each market that lists it (1 credit per market).
first = mdm("product", {"id": "204172"})
markets = [(first["country"], first["language"])] + [(m["country"], m["language"]) for m in first["markets"]]
seen, readings = set(), []
for country, language in markets:
    if country in seen:  # one language per market is enough for the price
        continue
    seen.add(country)
    p = first if country == first["country"] else mdm("product", {"id": "204172", "country": country, "language": language})
    if p is None:
        continue
    readings.append({
        "id": p["id"],
        "country": p["country"],
        "captured_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "price": p["price"],
        "was_price": p["was_price"],
        "discount_percent": p["discount_percent"],
        "currency": p["currency"],
        "sold_by": p["sold_by"],
    })

# Store `readings` and run this on a schedule. Compare a price only with
# readings in the same currency; never compare CHF with EUR without converting.
for row in readings:
    print(row)
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live; nothing is cached. Every `data` echoes `country`, `language` and `currency`. Prices are numbers in the market's currency, never converted. `notes` appears when there is something to say.

- **Grid item** (search, category, deals, seller catalog) - `position`, `id` (digits for Maisons du Monde items, `M` + digits for marketplace items), `name`, `collection`, `brand`, `url`, `image`, `price`, `was_price`, `discount_percent`, `currency`, `eco_participation` (`fr`, when the page shows one), `badges[]` (the page's own badges: `BLACK FRIDAY`, `Nouveau`, `Seconde Chance`), `rating`, `review_count`, `color_count`, `sold_by` (`mdm` or `marketplace`), `offer_id` (marketplace), `sponsored`, `condition` (Seconde Chance items), `store_only`, `purchase_status`.
- **Grid** - `items[]`, `count` (organic items on the page), `sponsored_count`, `total` (exact), `page`, `page_size` (40), `total_pages` (at most 250), `sort`, `sorts_offered[]` {`sort`, `label`}, `requested_filters`, `applied_filters[]` {`id`, `value`, `label`}, `facets[]` {`id`, `name`, `type` (`options` or `range`), `options[]` {`id`, `label`, `count`} and `option_count` (at most 100 options per facet are returned), or `min` / `max`}. Search adds `query` and `redirected_to` {`type`, `category_id`, `name`, `url`} or `null`; category adds `category` {`id`, `name`, `url`, `breadcrumbs[]`}; deals adds `event` {`type`, `name`, `url`, `category_id`}.
- **product** - `id`, `gtin13`, `name`, `collection`, `brand`, `url`, `price`, `was_price`, `discount_percent`, `currency`, `eco_participation` (`fr`), `badges[]`, `stock` {`status`, `quantity`}, `store_only`, `sold_by`, `seller` {`id`, `name`, `url`, `rating`, `orders`, `member_since`} or `null`, `offer_id`, `condition`, `variants[]` {`dimension` (`color`, `model` or `package`), `value`, `name`, `id`, `url`, `price_difference`}, `dimensions[]` {`label`, `value`, `unit`}, `weight` {`value`, `unit`}, `materials` {`main`, `other`}, `made_in`, `characteristics[]` {`label`, `value`, `unit`}, `composition`, `attributes[]`, `wood_and_finishes[]` {`label`, `value`}, `assembly[]` {`label`, `value`, `unit`}, `care`, `documents[]` {`type`, `label`, `url`}, `images[]`, `breadcrumbs[]` {`name`, `url`}, `categories[]` {`id`, `name`}, `short_description`, `description`, `rating`, `review_count`, `review_summary` {`title`, `sections[]` {`key`, `title`, `text`}}, `questions[]` {`question`, `answer`}, `markets[]` {`country`, `language`, `url`}, `notes[]`; `requested_id` when the site answers a different reference than the one sent.
- **reviews** - `product_id`, `sort`, `rating`, `review_count`, `rating_histogram` {`1` to `5`}, `criteria` (average per criterion when the site shows one, else `null`), `reviews[]` {`rating`, `text`, `date`, `author`, `country` (the reviewer's country name, in the request language), `source_market`, `syndicated`, `criteria[]` {`label`, `rating`}, `brand_reply`, `images[]`}, `next_cursor`, `notes[]`.
- **stores** - `postcode`, `stores[]` {`id`, `name`, `address`, `postcode`, `city`, `country`, `lat`, `lng`, `distance_km`, `url`, `open_now`, `hours_today`, `hours[]` {`day`, `slots[]` {`open`, `close`}}, `click_collect`}, `count`, `notes[]`.
- **store** - `id`, `name`, `address`, `postcode`, `city`, `country`, `phone`, `lat`, `lng`, `url`, `hours[]`, `services[]` (as the store page lists them, in the market's language), `click_collect`, `hours_today`.
- **availability** - `product_id`, `store` {`id`, `name`, `postcode`, `city`}, `in_stock`, `quantity`, `stock_text`, `display_model`, `click_collect` {`available`, `text[]`}, `on_shelf` {`available`, `text[]`}, `delivery[]` {`type` (`home`, `store_pickup`, `in_store`), `title`, `available`, `availability_text`, `from_price`, `currency`, `price_text`}, `notes[]`.
- **seller** - `seller` {`id`, `name`, `code`, `url`, `rating`, `review_count`, `orders`, `member_since`, `order_approval` {`delay`, `rate_percent`}, `shipping` {`label`, `zone`, `ships_within_days`, `types[]`, `policy`, `trade_in`}, `returns` {`withdrawal_days`, `how_to_return`}, `company_city`, `description`} plus the grid of the seller's catalog.

## Guardrails

- Crossed-out price: `was_price` is the crossed-out price the page shows next to a discount, and `discount_percent` is the page's own percent off. Maisons du Monde shows no 30-day lowest price, so none is returned: never call `was_price` the 30-day lowest price, the previous price or yesterday's price, and never present `discount_percent` as a measured price drop. For a measured change, compare your own stored readings.
- Prices by country: the euro markets shared one price per product on the 6 products measured on 2026-11-14; that is a measurement, not a guarantee. Read each market you report. Switzerland is priced separately in CHF. Never compare CHF with EUR without converting explicitly, with the rate and its date.
- Marketplace: on `fr`, `de`, `es` and `it` some items are sold by third-party sellers (`sold_by: "marketplace"`, `id` starting with `M`), who set their own prices. Keep them apart from Maisons du Monde's own items in any statistic (`sold_by: "mdm"` filters them out). Grid tiles carry `sold_by` but not the seller's name: `/product` has `seller`.
- Sponsored tiles: `items[]` can hold sponsored marketplace tiles (`sponsored: true`, up to 16 on page 1); `count` excludes them. Drop them before ranking or counting.
- `eco_participation` (`fr`) is the French furniture recycling fee, included in `price`. Do not add it to the price.
- German search: sorted keyword searches on `de` come back in relevance order with a note. Use `/category` to sort on `de`.
- Paging: 40 per page, at most 250 pages; narrow with filters past that.
- Reviews are pooled across every Maisons du Monde market and shown translated into the request language. Say so when quoting one, and say where it was written (`source_market`). The site has no star filter; `rating_histogram` covers every review. Reviews carry no verified-buyer flag, id or title. Quote short excerpts, and never more than the `author` display name of a reviewer.
- A product with no reviews, and a marketplace item (whose reviews the site does not list), answers `404` on `/reviews`.
- Delivery: home delivery is a from-price per product and market (`delivery[].from_price`, the site's "à partir de" wording). There is no postcode-exact delivery cost: never present the from-price as the user's delivery cost.
- Store stock: `/availability` is per item and per store, Maisons du Monde items only. `display_model: true` means the display piece is the stock. Stores, store and availability are not available on `nl` and `lu`.
- Markets: Austria (closed 2026) and the UK (closed 2023) are not served.
- Not available: price history, the 30-day lowest price, search suggestions, a postcode-exact delivery cost, review star filter, cart, checkout, private sales and professional (B2B) prices.
- Terms: Maisons du Monde's terms reserve its rights over the site's content, including database rights, and prohibit reproducing or using it without its prior consent; they allow downloading copies for personal, non-commercial use. We do not interpret them. This is not legal advice; the user is responsible for their own compliance. Do not republish Maisons du Monde product photos or room scenes; link product pages instead.
- Never fabricate prices, references, category hashes, store ids, seller ids, reviews or ratings. Only return what the API returned, with the market, the currency and the product `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: a `country` outside the endpoint's markets (stores, store and availability on `nl` or `lu`; seller, `seller` or `sold_by` outside `fr`, `de`, `es`, `it`; `at`, `gb`, `uk`); a `language` the market does not serve; a reference that is not digits or `M` + digits; a marketplace `M` reference on `/availability`; a `url` that is not a Maisons du Monde product, category, store or seller page; a themed `/vc/` page as `category_url`; a `sort`, `event`, `min_discount` or `min_rating` outside its list; `second_chance` outside `fr`; `price_min` not below `price_max`; `seller` together with `sold_by`; a `filters` key that has a named parameter; a postcode in the wrong format for the market; a `cursor` that is not a `next_cursor`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Maisons du Monde has no product ... on ... (unknown, or not sold in that market).", "Maisons du Monde found nothing for this query.", "Maisons du Monde has no reviews for product ...", "Maisons du Monde has no store ...", "Maisons du Monde has no marketplace seller ...", or an event that is not running. Take references, hashes and ids from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api).
- `502` means Maisons du Monde data was temporarily unavailable ("Maisons du Monde is temporarily unavailable. Please try again."). It is retried automatically and not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means Maisons du Monde is busy ("Maisons du Monde is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds (5) and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.59.0
npm install scavio@0.60.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.maisonsdumonde.search({ query: "table", sort: "price_asc", on_sale: true });
const { data: sofa } = await scavio.maisonsdumonde.product({ id: "186339", country: "de" });
const { data: sofas } = await scavio.maisonsdumonde.category({ category: "canapes-n4dc562d7bb509362a3a2102db4cbf90b6454f1f", sold_by: "mdm" });
const { data: blackFriday } = await scavio.maisonsdumonde.deals({ event: "black_friday", country: "es" });
const { data: reviews } = await scavio.maisonsdumonde.reviews({ id: "186339", language: "fr", limit: 30 });
const { data: near } = await scavio.maisonsdumonde.stores({ postcode: "75011" });
const { data: store } = await scavio.maisonsdumonde.store({ store_id: "41" });
const { data: stock } = await scavio.maisonsdumonde.availability({ id: "204172", store_id: "125" });
const { data: seller } = await scavio.maisonsdumonde.seller({ seller_id: "2066" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.maisonsdumonde.search(...)`, `client.maisonsdumonde.product(...)`, `client.maisonsdumonde.category(...)`, `client.maisonsdumonde.deals(...)`, `client.maisonsdumonde.reviews(...)`, `client.maisonsdumonde.stores(...)`, `client.maisonsdumonde.store(...)`, `client.maisonsdumonde.availability(...)` and `client.maisonsdumonde.seller(...)`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_maisonsdumonde`, `get_maisonsdumonde_product`, `get_maisonsdumonde_category`, `get_maisonsdumonde_deals`, `get_maisonsdumonde_reviews`, `get_maisonsdumonde_stores`, `get_maisonsdumonde_store`, `get_maisonsdumonde_availability` and `get_maisonsdumonde_seller`. Maisons du Monde is opt-in: add `maisonsdumonde` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.57.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,maisonsdumonde"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/maisonsdumonde-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [product](https://scavio.dev/docs/maisonsdumonde-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [category](https://scavio.dev/docs/maisonsdumonde-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [deals](https://scavio.dev/docs/maisonsdumonde-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [reviews](https://scavio.dev/docs/maisonsdumonde-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [stores](https://scavio.dev/docs/maisonsdumonde-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [store](https://scavio.dev/docs/maisonsdumonde-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [availability](https://scavio.dev/docs/maisonsdumonde-availability?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api), [seller](https://scavio.dev/docs/maisonsdumonde-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api). Overview: [Maisons du Monde API](https://scavio.dev/maisonsdumonde-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=maisons-du-monde-api).
