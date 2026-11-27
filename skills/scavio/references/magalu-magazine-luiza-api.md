# Magalu (Magazine Luiza) API - Prices, Pix Price, Coupons, Deals, Stores

Read Magazine Luiza (magazineluiza.com.br, Magalu, the Brazilian retailer): keyword search, category listings, deal selections (Ofertas do Dia and the Black Friday 2026 selections), one product with its payment plans, variants, seller and spec sheet, a product's reviews, search suggestions, Magalu's physical stores in a state or city, and one store. www.magazineluiza.com.br only (Brazil, BRL, Portuguese text), as shown to a visitor who is not signed in. Every endpoint returns structured JSON and costs 2 credits.

**The job this skill is for: what an item costs at Magalu today, by card, in installments and by Pix, and who sells it.** Magalu shows several prices for one item and this skill returns each one as the site shows it, never computed. On 2026-11-27 the LG Frost Free Smart Inverse 462L refrigerator (product `238058800`) read `price` R$ 3,893.68 (10 installments of R$ 389.37 "sem juros", interest-free), `pix_price` R$ 3,699 with `pix_discount_percent` 5, sold by Magalu (`seller.is_magalu` true, legal name Magazine Luiza SA), rating 4.8 over 1,240 reviews. Its payment plans ran from 1 to 30 installments on `luiza_ouro`, where 30 installments totalled R$ 6,232.34 with R$ 2,338.66 interest as the site states it. A Brastemp 415-litre refrigerator in the best-selling refrigerators sold by the Brastemp marketplace store read R$ 2,699 against a R$ 3,288 list price (17.9 percent off), R$ 2,564.05 by Pix, with a R$ 150 coupon.

Seven limits shape every answer, so say them plainly:
- **2 credits on every call.** Search, category, deals, product, reviews, suggestions, stores and store are each 2 credits. `credits_used` in the response is the truth. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Pages are slow.** Search, category, deals and product usually take 10-60 seconds; deal pages took 127-161 seconds on Black Friday 2026. Reviews, suggestions, stores and store usually take 3-15 seconds. Set a client timeout of at least 180 seconds.
- **40 per page, page 1-25.** Sponsored cards are mixed in by the site and flagged (`sponsored`, `sponsored_count`), so `count` can exceed 40 (49 on the refrigerator search). On page 1 `total` is the site's count capped at 1000; deeper pages show the real count.
- **Available, not units.** `available` is the site's flag; Magalu does not show stock units. No GTIN is published on the page and the marketing description is not returned.
- **No shipping and no Full filter.** Shipping by CEP (Brazilian postal code), store pickup and store stock are not available. The Full delivery filter is refused (`400`): Magazine Luiza lists no products for it on the page.
- **Stores are a directory.** Stores come by state (UF), optionally one city: number, name, city and neighbourhood. One store adds address, CEP and phone. Coordinates, search by CEP, store pickup and store stock are not published.
- **No history.** Everything is the page at the moment of the call; Scavio keeps nothing. Poll and store your own series.

Magazine Luiza has no public product API (it runs an affiliate program). Prices are shown on magazineluiza.com.br for each item, and this skill reads those public pages with one Scavio key.

See also: KaBuM! `kabum-api` (the Brazilian computer and electronics retailer, part of Magalu), Mercado Libre `mercadolibre-product-data`; the same item on Amazon Brazil `amazon-product-data`.

## When to trigger

Use this skill when the user asks to:
- Price an item at Magalu or Magazine Luiza: price, list price, discount, Pix price, installments ("10x sem juros"), coupons
- Search magazineluiza.com.br by keyword (Portuguese, as a shopper types it), sorted by relevance, fastest delivery, price with shipping, price, best sellers, top rated or newest
- Filter Magalu listings by brand, seller (Magalu's own offers or a marketplace seller), price range in BRL, minimum rating, the Black Friday promotion (Ofertas Black) or attributes such as voltage (110V, 220V), colour or capacity
- Browse one Magalu department or subcategory (Eletrodomesticos, Geladeira / Refrigerador)
- List Magalu's daily deals (Ofertas do Dia) or a Black Friday 2026 selection, with each card's deal timer
- Read one Magalu product: every payment method's installment plans, variants (colour, voltage), the seller's business name, CNPJ and stats, spec sheet, questions and answers
- Read Magalu customer reviews of a product with star distribution, aspect ratings and Magalu's own summary
- Get Magalu search suggestions for the start of a search
- List Magazine Luiza physical stores in a Brazilian state or city, or read one store's address, CEP and phone

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 2 credits, so 50 credits cover 25 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures of 2026-11-27: reviews 2.1 s, suggestions 3.2 s, store 3.6 s, stores 12.5 s, deals 14.8 s, search 44.4 s, category 55.1 s, product 55.1 s. Allow a client timeout of at least 180 seconds: deal pages took 127-161 seconds on Black Friday 2026.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/magalu/search` | Keywords: 40 per page with total, prices, Pix price, installment, seller, rating, coupon, deal timer, badges, variants; facets, price range | 2 |
| `POST /api/v1/magalu/category` | One department or subcategory by path or link, same cards, sorts, filters and facets as search, with breadcrumbs | 2 |
| `POST /api/v1/magalu/deals` | A deal selection: Ofertas do Dia (default) or a campaign selection (`blackfriday2026`, `blackfriday2026_celulares` ...), each card with its deal timer | 2 |
| `POST /api/v1/magalu/product` | One product: prices, Pix price, payment methods with installment plans, coupons, deal timer, seller with CNPJ and stats, variants, images, spec sheet, questions | 2 |
| `POST /api/v1/magalu/reviews` | Reviews of one product in 4 sorts, up to 50 per page, with star distribution, aspect ratings and Magalu's summary (no reviewer names) | 2 |
| `POST /api/v1/magalu/suggestions` | Up to 10 search suggestions for the start of a search | 2 |
| `POST /api/v1/magalu/stores` | Magalu's physical stores in one state (UF), optionally one city | 2 |
| `POST /api/v1/magalu/store` | One store: address, city, state, CEP, phone, opening hours when the page carries them | 2 |

Brazil only: there is no `country` parameter. Every answer carries `store` (magalu), `host`, `country` (br), `currency` (BRL) and `language` (pt-BR). Text (titles, specs, reviews, facet labels) is in Portuguese as the site writes it.

## Prices: price, Pix, installments, coupons and deal timers

Every listing card and product carries Magalu's price layers as magazineluiza.com.br shows them to a visitor who is not signed in:

| Field | Meaning |
|---|---|
| `price` | Magalu's price (the card and installment price) |
| `list_price`, `discount_percent` | The struck-through list price and the site's discount percent, when shown (null otherwise) |
| `pix_price`, `pix_discount_percent` | The price paid by Pix and its discount against `price` (R$ 3,699 and 5 on the LG refrigerator) |
| `installment` (cards), `best_installment` (product) | `{count, amount, total, interest, description}`: the plan the site headlines ("sem juros", interest-free) |
| `payment_methods[]` (product) | `{method, plans[]}` per method (`luiza_ouro`, a card brand such as `mastercard`, `pix`), each plan `{count, amount, total, interest, discount_percent}` with interest as the site states it |
| `coupon` (cards), `coupons[]` (product) | `{code, message, discount_type (absolute or percentage), discount_value, starts_at, ends_at}` as given; `code` can be null when the site applies the coupon without one |
| `deal_starts_at`, `deal_ends_at` | The card's own deal timer, where the site shows one (2 of 40 daily-deal cards on 2026-11-27) |
| `badges`, `tags` | The site's badges (`novoselorelampago`, `ofertablack2024`) and tags (`is_magalu_indica`) as given |
| `seller` | `{id, name, is_magalu}` on cards; on product also `legal_name`, `cnpj`, `seller_since`, `score`, `total_sales`, `delivery_rate`, `answer_rate`, `city`, `state` |

- Quote "LG Frost Free Smart Inverse 462L: R$ 3,893.68 or R$ 3,699 by Pix at magazineluiza.com.br on 2026-11-27 (10x R$ 389.37 interest-free, sold by Magalu)", with the date.
- A coupon is "Magalu shows a R$ 150 coupon" (absolute) or "a 5 percent coupon" (percentage). Never compute an after-coupon price, never stack a coupon on the Pix price, and never apply a coupon the site did not attach to that card or product.
- Installments: quote `count`, `amount`, `total` and `interest` exactly as given. A plan with interest costs more than `price`; say so with the site's `total`.
- Variants (colour, voltage) are separate product ids with their own prices: read `/product` with the `variation_id` you mean before quoting.
- The price-range filter is the site's own: a card's `price` can sit above `max_price` when its Pix price is inside the range.
- Report Magalu's prices, labels and dates and the arithmetic only. Never judge a price as a good deal and never describe how often an item goes on sale.

## Workflow

1. **Find the item.** `/search` with `query` (`geladeira frost free`), `/category` with a `path` (`/geladeira-refrigerador/eletrodomesticos/s/ed/refr/`), or `/deals` with a `selection` (`ofertasdodia`, `blackfriday2026`). Each card's `product_id` is the input of product and reviews.
2. **Narrow it.** Read `facets[]` from the first answer and pass `brand`, `seller`, `promotion` or `attributes` with the `values[].value` slugs (`{"voltagem": "220v"}`).
3. **One product.** `/product` with `product_id` or `url`: `payment_methods` for every installment plan, `seller` for the business behind the offer, `variants[].options[].variation_id` for the other colours and voltages.
4. **Reviews.** `/reviews` with `product_id`, a `sort` and `page_size` up to 50.
5. **Stores.** `/stores` with a `state` (`sp`) and optionally `city`; `/store` with a `store_id` for address, CEP and phone.
6. **Watching prices:** there is no history. Poll the same products on a schedule and store each answer with its `fetched_at`; that stored series is the history.

## Parameters

### Search (`/search`), category (`/category`) and deals (`/deals`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required on search | Keywords, 1-200 chars, in Portuguese as a shopper types them (`geladeira frost free`) |
| `path` | string | required on category | A department (`/eletrodomesticos/l/ed/`), a subcategory (`/geladeira-refrigerador/eletrodomesticos/s/ed/refr/`) or a magazineluiza.com.br category link |
| `selection` | string | `ofertasdodia` | Deals only: a selection id or `/selecao/` link (`ofertasdodia`, `blackfriday2026`, `blackfriday2026_celulares`, `blackfriday2026_eletro`, `blackfriday2026_games`, `blackfriday2026_info`) |
| `sort` | string | `relevance` | `relevance`, `fastest_delivery`, `price_with_shipping`, `price_asc`, `price_desc`, `best_sellers`, `top_rated`, `newest` (the site's 8 sorts) |
| `page` | integer | 1 | 1-25, 40 per page |
| `brand` | string or array | none | Brand slug(s) from `facets` brand `values[].value` (`brastemp`, `consul`, `lg`) |
| `seller` | string or array | none | `magalu` (Magalu's own offers) or marketplace seller id(s) from the seller facet (`mideacarrier`) |
| `min_price`, `max_price` | number | none | BRL, the site's price filter (`2000`, `3000`) |
| `min_rating` | integer | none | Minimum star rating, 1-5 |
| `black_friday` | boolean | none | `true`: items in the site's Black Friday promotion (Ofertas Black) |
| `promotion` | string or array | none | Promotion id(s) from the promotion facet (`promocao_sazonal_3`, Ofertas do Dia) |
| `attributes` | object | none | Attribute facets: facet slug to value slug(s), `{"voltagem": "220v", "cor": ["branco", "inox"]}` (`facets[].slug`, `values[].value`), up to 10 facets |

Up to 10 values per list. Values are lowercase slugs as the site writes them in its filters. The Full delivery facet (`delivery_magalu`) is refused, and `brand`, `seller`, `promotion` and the rating go in their own fields, not in `attributes`.

### Product (`/product`) and reviews (`/reviews`)

`product_id` (`238058800` or `ffh7ah372g`: a card's `product_id` or a `variation_id`) or `url` (a magazineluiza.com.br product link of the form `https://www.magazineluiza.com.br/<name>/p/<id>/<dept>/<sub>/`), not both. Reviews also take `sort` (`most_relevant` default, `most_recent`, `most_positive`, `most_negative`; `most_negative` is the site's order, not strictly by stars), `page` (1-500) and `page_size` (1-50, default 10). A star filter is not available.

### Suggestions (`/suggestions`)

`query` (required, 1-100 chars): the start of a search (`geladeira`). The site can answer an empty list for a term (the `geladeira` capture returned 0).

### Stores (`/stores`) and store (`/store`)

`/stores` takes `state` (required, a Brazilian state code: ac, al, am, ap, ba, ce, df, es, go, ma, mg, ms, mt, pa, pb, pe, pi, pr, rj, rn, ro, rr, rs, sc, se, sp, to) and optional `city` (accents and case ignored; cities are written as the site writes them, `SAO PAULO`). `/store` takes `store_id` (`1000`, a `stores[].store_id`) or `url` (a lojas.magazineluiza.com.br store link), not both.

## Examples

### One listing card with a marketplace seller and a coupon

```bash
curl -X POST https://api.scavio.dev/api/v1/magalu/category \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/geladeira-refrigerador/eletrodomesticos/s/ed/refr/", "sort": "best_sellers"}'
```

Captured `data` (2026-11-27; `total` 616, 16 pages, `site_sort` "Mais Vendidos"; one card, `image`, `url` and `variants` dropped):

```json
{
  "category": {
    "name": "Geladeira Refrigerador",
    "breadcrumbs": [
      { "name": "Eletrodomésticos", "url": "https://www.magazineluiza.com.br/eletrodomesticos/l/ed/" },
      { "name": "Geladeira Refrigerador", "url": "https://www.magazineluiza.com.br/geladeira-refrigerador/eletrodomesticos/s/ed/refr/" }
    ]
  },
  "page": 1,
  "page_size": 40,
  "total": 616,
  "total_pages": 16,
  "count": 39,
  "sponsored_count": 0,
  "sort": "best_sellers",
  "items": [
    {
      "product_id": "ed0jh99343",
      "title": "Geladeira Frost Free Duplex 415 Litros Branca Brastemp - BRM51MB",
      "available": true,
      "sponsored": false,
      "price": 2699,
      "list_price": 3288,
      "discount_percent": 17.9,
      "pix_price": 2564.05,
      "pix_discount_percent": 5,
      "currency": "BRL",
      "seller": { "id": "whirlpool", "name": "Brastemp", "is_magalu": false },
      "coupon": {
        "code": null,
        "message": null,
        "discount_type": "absolute",
        "discount_value": 150,
        "starts_at": null,
        "ends_at": null
      },
      "deal_starts_at": null,
      "deal_ends_at": null,
      "badges": []
    }
  ]
}
```

### A daily deal with its timer

`{"selection": "ofertasdodia"}` (2 credits) answered `total` 353 over 9 pages, `selection_info` {`label` null, `description` "Aproveite!", `ends_at` null}. One card (trimmed):

```json
{
  "product_id": "jfjg127c7f",
  "title": "Chuveiro Eletrônico Lorenzetti Acqua Duo Ultra Preto Cromado 5500w 127",
  "price": 599.65,
  "list_price": 685.37,
  "discount_percent": 12.5,
  "pix_price": 557.67,
  "pix_discount_percent": 7,
  "seller": { "id": "uaiexpress1", "name": "Uai Express", "is_magalu": false },
  "coupon": { "code": null, "discount_type": "absolute", "discount_value": 30 },
  "deal_starts_at": "2026-11-27T00:00:00-03:00",
  "deal_ends_at": "2026-11-30T09:59:59-03:00",
  "badges": ["novoselorelampago"]
}
```

The answer's `notes` say how many cards on the page carry a timer ("2 of 40 cards on this page carry one").

### One product with its payment plans and seller

`{"product_id": "238058800"}` (2 credits), trimmed:

```json
{
  "product_id": "238058800",
  "title": "Geladeira/Refrigerador LG Frost Free Smart Inverse",
  "reference": "Prata 462L Inox Look GC-B569NLLM.APZFSBS",
  "brand": "LG",
  "available": true,
  "price": 3893.68,
  "list_price": null,
  "pix_price": 3699,
  "pix_discount_percent": 5,
  "best_installment": { "count": 10, "amount": 389.37, "total": 3893.68, "interest": 0, "description": "sem juros" },
  "payment_methods": [
    { "method": "luiza_ouro", "plans": [
      { "count": 1, "amount": 3699, "total": 3699, "interest": 0, "discount_percent": 5 },
      { "count": 30, "amount": 207.74, "total": 6232.34, "interest": 2338.66, "discount_percent": 0 }
    ] },
    { "method": "mastercard", "plans": [
      { "count": 12, "amount": 367.96, "total": 4415.5, "interest": 521.82, "discount_percent": 0 }
    ] },
    { "method": "pix", "plans": [
      { "count": 1, "amount": 3699, "total": 3699, "interest": 0, "discount_percent": 5 }
    ] }
  ],
  "coupons": [],
  "minimum_order_quantity": 1,
  "seller": {
    "id": "magazineluiza",
    "name": "Magalu",
    "legal_name": "Magazine Luiza SA",
    "cnpj": "47960950000121",
    "is_magalu": true,
    "seller_since": "2016-06-01T00:00:00.000+00:00",
    "score": 5,
    "total_sales": 249556925,
    "answer_rate": "Responde rápido",
    "city": "Franca",
    "state": "SP"
  },
  "rating": 4.8,
  "review_count": 1240
}
```

Plans shown are 2 of 30 on `luiza_ouro` and 1 of 12 on `mastercard`. The product also carries `variants` (Cor, Voltagem with each `variation_id`), `images`, 27 `specs` rows {`group`, `name`, `value`} ("Tipo de Degelo": "Frost Free") and `questions` {`total`, `count`, `items`}.

### Reviews, suggestions, stores and store

- `/reviews` `{"product_id": "238058800", "sort": "most_recent"}`: `rating` 4.8, `review_count` 1240, `comment_count` 770, `star_distribution` 5 stars 1132, 4 stars 58, 3 stars 2, 2 stars 4, 1 star 44; `aspect_ratings` (Boa qualidade, Baixo consumo de energia, Silencioso ... each 5); `summary` (Magalu's own summary of the reviews, as given); `total` 620, 62 pages of 10; each review {`review_id`, `rating`, `title`, `text` ("Linda grande"), `submitted_at` (2026-11-23T22:58:09.777Z), `variant` [{`label` color, `value` Prata}, {`label` voltage, `value` 220V}], `aspects`, `sku`, `images`, `videos`}. No reviewer names.
- `/suggestions` `{"query": "geladeira"}`: `count` 0, `suggestions` [] in the capture; other terms answer up to 10 {`position`, `term`}.
- `/stores` `{"state": "sp", "city": "Sao Paulo"}`: `state_total` 513 stores in Sao Paulo state across `city_count` 235 cities, `count` 98 in the city, each {`store_id` ("527"), `name` ("Loja Sao Miguel Paulista - Sao Paulo"), `city` SAO PAULO, `neighborhood`, `state`, `url`}.
- `/store` `{"store_id": "1000"}`: `name` "Magazine Luiza - Loja Itaberaba/Sao Paulo", `street_address` "ITABERABA 2023", `city` SAO PAULO, `state` SP, `cep` 02739000, `phone` +551139907500, `opening_hours` (the capture carried Monday-Friday 09:00-20:00 and Saturday 09:00-18:30; it can be null). No coordinates.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def magalu(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/magalu/{endpoint}", headers=HEADERS, json=body, timeout=180)
    r.raise_for_status()
    return r.json()

# 1. 220V frost-free refrigerators from Magalu's own offers, best sellers first (2 credits)
grid = magalu("search", {"query": "geladeira frost free", "sort": "best_sellers",
                         "seller": "magalu", "attributes": {"voltagem": "220v"}})["data"]
card = grid["items"][0]
print(card["title"], card["price"], card["pix_price"], card["installment"])

# 2. The product: every payment method's plans and the seller (2 credits)
prod = magalu("product", {"product_id": card["product_id"]})["data"]
for m in prod["payment_methods"]:
    print(m["method"], m["plans"][-1]["count"], m["plans"][-1]["total"], m["plans"][-1]["interest"])
print(prod["seller"]["name"], prod["seller"]["cnpj"])

# 3. The newest reviews, 50 per page (2 credits)
revs = magalu("reviews", {"product_id": card["product_id"], "sort": "most_recent", "page_size": 50})["data"]
print(revs["rating"], revs["star_distribution"])

# Magalu prices change daily. Store each answer with fetched_at and run
# this on a schedule: that stored series is your history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Each call fetches the page when the request asks for it. Every `data` carries `store`, `host`, `country`, `currency` and `language`, and most carry `notes`.

- **search / category / deals** - (`query`, `term` on search; `path`, `category` {`name`, `canonical_url`, `breadcrumbs[]`} on category; `selection`, `selection_info` {`label`, `description`, `ends_at`} on deals), `url`, `page`, `page_size`, `total`, `total_pages`, `has_more`, `count`, `sponsored_count`, `site_sort` {`label`, `type`, `orientation`}, `sort`, `items[]` {`position`, `product_id`, `title`, `reference`, `brand`, `url`, `image`, `available`, `sponsored`, `price`, `list_price`, `discount_percent`, `pix_price`, `pix_discount_percent`, `installment` {`count`, `amount`, `total`, `interest`, `description`}, `currency`, `seller` {`id`, `name`, `is_magalu`}, `rating`, `review_count`, `coupon`, `deal_starts_at`, `deal_ends_at`, `badges`, `tags`, `category_id`, `subcategory_id`, `variants[]` {`name`, `type`, `current`, `options[]` {`value`, `variation_id`, `available`, `url`}}}, `facets[]` {`slug`, `label`, `param`, `values[]` {`value`, `label`, `count`, `selected`}}, `price_range` {`min`, `max`, `selected_min`, `selected_max`}, `rating_range`, `filters_applied`.
- **product** - `product_id`, `requested_id`, `title`, `reference`, `brand`, `entity`, `url`, `category` {`id`, `name`, `url`}, `subcategory`, `breadcrumbs[]`, `available`, `price`, `list_price`, `discount_percent`, `pix_price`, `pix_discount_percent`, `best_installment`, `payment_methods[]` {`method`, `plans[]` {`count`, `amount`, `total`, `interest`, `discount_percent`}}, `coupons[]`, `deal_starts_at`, `deal_ends_at`, `max_checkout_quantity`, `minimum_order_quantity`, `badges`, `tags`, `seller` {`id`, `name`, `legal_name`, `cnpj`, `is_magalu`, `seller_since`, `score`, `total_sales`, `delivery_rate`, `answer_rate`, `city`, `state`}, `rating`, `review_count`, `variants[]`, `images[]`, `specs[]` {`group`, `name`, `value`}, `questions` {`total`, `count`, `items[]` {`question_id`, `question`, `answer`, `asked_at`, `answered_at`}}.
- **reviews** - `product_id`, `rating`, `review_count`, `comment_count`, `star_distribution[]` {`stars`, `count`}, `aspect_ratings[]` {`id`, `label`, `rating`}, `summary`, `page`, `page_size`, `total`, `total_pages`, `count`, `sort`, `reviews[]` {`review_id`, `rating`, `title`, `text`, `submitted_at`, `variant[]` {`label`, `value`}, `aspects`, `sku`, `images`, `videos`}.
- **suggestions** - `query`, `count`, `suggestions[]` {`position`, `term`}.
- **stores** - `state`, `city`, `state_total`, `city_count`, `count`, `stores[]` {`store_id`, `name`, `city`, `neighborhood`, `state`, `url`} in the site's order.
- **store** - `store_id`, `name`, `street_address`, `city`, `state`, `cep`, `phone`, `url`, `opening_hours` (as the store page publishes them, or null).

## Guardrails

- Name it "Magazine Luiza (magazineluiza.com.br, Magalu, the Brazilian retailer)" on first mention. Magalu accounts, the Magalu app, MagaluPay balances and card offers are not read.
- Prices: quote `price`, `pix_price`, the installment plan and the `fetched_at` date, in BRL (R$). Prices are what a visitor who is not signed in sees on magazineluiza.com.br.
- Coupons and installments: quote them exactly as given. Never compute an after-coupon price, never combine a coupon with the Pix price, and quote interest and totals from the plan, never recomputed.
- Sellers: say whether Magalu sells it (`is_magalu` true) or a marketplace seller does, with the seller's business name. Business name, legal name and CNPJ are public business data.
- Stock: `available` is a flag, not a count. Never quote units, delivery dates, shipping costs or store availability: they are not returned.
- Comparing Magalu with KaBuM!, Mercado Libre or Amazon: compare the same item (same model reference from `specs`), colour and voltage, each with its date. Never call one retailer cheaper beyond the numbers shown.
- Reviews and questions: no reviewer or asker names or ids are returned. Quote a review as "a Magalu customer review"; `summary` is Magalu's own text, quote it as such.
- Images and copy: do not republish Magalu's product images or product copy; link items by `product_id` instead.
- Not available: shipping by CEP, store pickup, store stock, stock units, the Full delivery filter, GTIN, the marketing description, a star filter on reviews, price history (poll and store), account data, cart or checkout. This API cannot reserve or buy an item.
- Terms: Scavio does not store Magalu data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. Read Magazine Luiza's current terms of use for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, coupons, plans, ids, CNPJs, dates or ratings. Only return what the API returned, with the `fetched_at` time.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: "product_id or url is required"; "Pass product_id or url, not both."; "url must be a magazineluiza.com.br product link (https://www.magazineluiza.com.br/<name>/p/<id>/<dept>/<sub>/)."; "path must be a Magazine Luiza category path or link: a department (/eletrodomesticos/l/ed/) or a subcategory (/geladeira-refrigerador/eletrodomesticos/s/ed/refr/)."; "path is a product link: use /api/v1/magalu/product."; "selection must be a selection id as Magazine Luiza writes it, e.g. ofertasdodia, blackfriday2026 or blackfriday2026_celulares."; "attributes: the Full delivery filter is not available (Magazine Luiza lists no products for it on the page)."; "min_price must not be above max_price."; "state must be a Brazilian state code (UF): ac, al, ..."; "store_id or url is required".
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Magazine Luiza has no product <id>.", "Magazine Luiza has no category <path>.", "Magazine Luiza has no deal selection <id>.", "Magazine Luiza has no store <id>.", "Nothing was found for this search.". A search with no products answers an empty `200` with a note; a city with no store answers an empty list with a note.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api).
- `502` and `503` mean Magalu data was temporarily unavailable ("Magazine Luiza is temporarily unavailable. Please try again.", with `Retry-After` on a `503`). They are not charged, so retry after a few seconds.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.102.0
npm install scavio@0.103.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.magalu.search({ query: "geladeira frost free", sort: "best_sellers", attributes: { voltagem: "220v" } });
const { data: grid } = await scavio.magalu.category({ path: "/geladeira-refrigerador/eletrodomesticos/s/ed/refr/", seller: "magalu" });
const { data: deals } = await scavio.magalu.deals({ selection: "blackfriday2026", sort: "price_asc" });
const { data: product } = await scavio.magalu.product({ product_id: "238058800" });
const { data: reviews } = await scavio.magalu.reviews({ product_id: "238058800", sort: "most_recent", page_size: 50 });
const { data: terms } = await scavio.magalu.suggestions({ query: "geladeira" });
const { data: stores } = await scavio.magalu.stores({ state: "sp", city: "Sao Paulo" });
const { data: store } = await scavio.magalu.store({ store_id: "1000" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.magalu.search(...)`, `category`, `deals`, `product`, `reviews`, `suggestions`, `stores` and `store`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_magalu`, `get_magalu_category`, `get_magalu_deals`, `get_magalu_product`, `get_magalu_reviews`, `get_magalu_suggestions`, `get_magalu_stores` and `get_magalu_store`. Magalu is opt-in: add `magalu` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.102.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,magalu"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/magalu-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api), [category](https://scavio.dev/docs/magalu-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api), [deals](https://scavio.dev/docs/magalu-deals?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api), [product](https://scavio.dev/docs/magalu-product?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api), [reviews](https://scavio.dev/docs/magalu-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api), [suggestions](https://scavio.dev/docs/magalu-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api), [stores](https://scavio.dev/docs/magalu-stores?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api), [store](https://scavio.dev/docs/magalu-store?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api). Platform overview: [Magalu API](https://scavio.dev/magalu-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=magalu-magazine-luiza-api).
