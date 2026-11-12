# OLX API - Listings, Ads, Sellers, 7 OLX Europe Markets

Read OLX classified ads from the seven OLX Europe sites: olx.pl (Poland), olx.ro (Romania), olx.pt (Portugal), olx.bg (Bulgaria), olx.ua (Ukraine), olx.kz (Kazakhstan) and olx.uz (Uzbekistan). Search by keyword and / or category, sorted by relevance, newest or price, filtered by price, condition, private or business seller, OLX delivery, photos, region, city or district with a radius, and by the category's own filters (rooms, area, year, mileage and the rest), which the filters endpoint lists with their values and live counts. Each ad comes with its price in the site's currency, condition, every parameter, category, location with ids, created / refreshed / valid-to dates, the promoted flag with its slot on the page, the business flag and the OLX delivery flag. Read one ad in full by id or link, a seller's business flag, business name, member-since date and number of live ads, and a seller's live ads. Look up the category tree, location ids for the location filters, the suggestions the search box shows, and the ads OLX recommends next to an ad. All 9 endpoints return structured JSON and cost 1 credit each.

**Which OLX:** this skill covers OLX Europe only, the seven sites above. OLX Brasil (olx.com.br), OLX India (olx.in), OLX Bosnia (olx.ba), olx.co.id and the Dubizzle-run OLX sites (Pakistan, Egypt, Lebanon) are different companies on different platforms and are not covered. If the user means one of those, say so instead of calling this API.

Data comes in the site's language exactly as OLX writes it: Polish titles and parameters on olx.pl ("Używane", "Model telefonu"), Romanian on olx.ro, Portuguese on olx.pt, Bulgarian on olx.bg, Ukrainian on olx.ua, and Russian by default on olx.kz and olx.uz (Kazakh or Uzbek with `language`). Quote those values as returned; translate them for the user only in your own words around the data, never inside it.

OLX's own API, the OLX Partner API (developer.olx.pl and its sister portals), is a seller-integration API. Its spec says it lets partners "integrate with local sites by posting, managing adverts and communicating with OLX users via internal messaging system", after an OLX user authorizes the app. The developer.olx.pl FAQ answers the read question directly: "Can I use API to read other people ads? It is not possible - you can manage only your own ads added on your authorized OLX account." This skill reads public OLX ads with one Scavio key instead.

Privacy is built in: private sellers come back as an id only. Seller names, phone numbers, emails, exact map positions, last-seen times and car VINs are never returned, and phone numbers and email addresses written into titles and descriptions are replaced with `[phone removed]` / `[email removed]`. `business_name` is filled for business sellers only.

See also: for Allegro, Poland's largest marketplace for new goods, use `allegro-api`; for second-hand fashion on Vinted (including vinted.pl and vinted.ro) use `vinted-api`; for eBay listings and sold comps use `ebay-product-data`.

## When to trigger

Use this skill when the user asks to:
- Search OLX (olx.pl, olx.ro, olx.pt, olx.bg, olx.ua, olx.kz or olx.uz) for an item and get asking prices in PLN, RON, EUR, UAH, KZT or UZS
- Monitor prices of used goods on OLX: poll a search or a list of ads on a schedule and store price, previous price and status per run
- Build a new-listing monitor that polls an OLX search sorted by newest and diffs the ad ids against the last run (the user's code sends any notification; this API does not)
- Analyse the used-car market (make, model, year, mileage, fuel, price) or the rental and property market (rooms, area, price per m², city, district) from OLX ads
- Track resellers and possible counterfeits of a brand: who lists it, private or business, where, and at what price
- Research salaries from OLX job ads (salary from / to, period, gross or net)
- Read one OLX ad in full by link or id: description, every parameter, category, photos, location and status
- Check an OLX seller: business or private, business name, member since, how many live ads, and their ads
- Find the category id, filter keys and values, or location ids to build a precise OLX search
- Replace the OLX Partner API for reading other people's ads, which it does not allow

Do not use it to message sellers, reveal or collect phone numbers, build contact lists of private persons, bid, snipe or buy. None of that is possible through this API.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every endpoint in this skill costs 1 credit, so the free credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
On Growth, 1,000 credits cost $1, so 1,000 OLX calls cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In testing, most calls answered in 1 to 48 seconds and `/filters` in 20 to 71 seconds. Set a client timeout of at least 120 seconds.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/olx/search` | 1 | A page of ads for a keyword and / or category (40 by default, up to 50, plus the promoted ads OLX places on the page), each with `id`, `url`, `title`, `description_snippet`, `price`, `salary`, `condition`, `params`, `category_id`, `location`, `created_at`, `refreshed_at`, `valid_to`, `status`, `is_promoted`, `promoted_position`, `is_highlighted`, `is_business`, `olx_delivery`, `photos`, `seller`. Plus `total`, `total_capped`, `total_pages`, `has_next_page`, `promoted_count` and `applied_filters` |
| `POST /api/v1/olx/offer` | 1 | One ad by `offer_id` or `url`: title, the full description as plain text, price, salary for jobs, condition, every parameter, `category` with breadcrumb, all photos, location, dates, `status`, `is_active`, `is_promoted`, `olx_delivery`, `is_job`, and the seller (`id`, `is_business`, `business_name`, `member_since`) |
| `POST /api/v1/olx/seller` | 1 | One seller by `user_id`: `is_business`, `business_name` (business sellers only), `member_since`, `active_ads` and `ads_url` (the seller's page on OLX) |
| `POST /api/v1/olx/seller-ads` | 1 | One seller's live ads, in the search shape, with the search sorts and filters and an optional `query` |
| `POST /api/v1/olx/filters` | 1 | The filters a category offers, ready to send to search: `key`, `label`, `type`, `kind` (range or choice), `unit`, `send_as` (the keys to use), suggested `steps`, and for choice filters every value with its label and live ad count. Plus ad counts per region (or per city inside `region_id`) and per category |
| `POST /api/v1/olx/categories` | 1 | The category tree: `id`, `name`, `parent_id`, `level`, `path`, `url`, `type`, `count` (live ads) and `children`. Top level with direct children, or one category's whole subtree with `parent_id` |
| `POST /api/v1/olx/locations` | 1 | Cities and districts matching a name, with `city_id`, `district_id` and `region_id` for the search location filters, plus municipality, county and region names |
| `POST /api/v1/olx/suggestions` | 1 | The suggestions the OLX search box shows for what was typed, each with the category it is most searched in |
| `POST /api/v1/olx/similar` | 1 | The ads OLX recommends next to one ad (about 30), in the search item shape |

## Markets

Every endpoint takes `country` (default `pl`). Prices come in the site's currency and labels in its language.

| `country` | Site | Currency | Language | Endpoints |
|---|---|---|---|---|
| `pl` | olx.pl | PLN | Polish (`pl`) | all 9 |
| `ro` | olx.ro | RON | Romanian (`ro`) | all 9 |
| `pt` | olx.pt | EUR | Portuguese (`pt`) | all 9 |
| `bg` | olx.bg | EUR | Bulgarian (`bg`) | all 9 |
| `ua` | olx.ua | UAH | Ukrainian (`uk`) | all 9 |
| `kz` | olx.kz | KZT | Russian (`ru`) by default; Kazakh with `language: "kk"` | 7: not `/filters` or `/similar`; no `olx_delivery` filter |
| `uz` | olx.uz | UZS | Russian (`ru`) by default; Uzbek with `language: "uz"` | 7: not `/filters` or `/similar`; no `olx_delivery` filter |

`language` is accepted on `/search`, `/seller-ads` and `/offer` for `kz` (`kk` or `ru`) and `uz` (`uz` or `ru`) only; anywhere else it returns `400`. An ad `url` sets the market by itself; if you also send a different `country`, the call returns `400`. Category, region and city ids are per site: look them up with `/categories` and `/locations` for each `country`.

**Converted prices.** Some sellers price in another currency. Where the site converts it for display (olx.uz ads priced in y.e., olx.ro ads in EUR, olx.ua ads in USD or EUR), `price.value` and `price.currency` are the converted figure in the site's currency, and `original_value` / `original_currency` keep what the seller entered. On an olx.uz ad page `price.label` can still show the seller's y.e. text ("745 у.е.") while `value` is in UZS.

## Workflow

1. **Find ads:** call `/search` with `query` (any language) and / or `category_id`, add `sort` and filters. `applied_filters` echoes what was sent. Page with `page` until `has_next_page` is `false`, within the 1,000-result window.
2. **Precise filters:** get the category id from `/categories` (or an item's `category_id`, or a suggestion's `category_id` from `/suggestions`), call `/filters` for it, then send the `send_as` keys in `filters` on `/search`: `{"filter_float_m:from": 40, "filter_enum_rooms": ["two", "three"]}`. Location ids come from `/locations`.
3. **One ad in full:** `/offer` with the `id` from a search item (or the ad link) for the description, every parameter, breadcrumb, photos and seller.
4. **Price monitoring:** poll `/offer` for a fixed list of ad ids, or `/search` for a query, on a schedule; store `price.value`, `price.previous_value`, `status` and the time per run and compare runs yourself. A `404` on a tracked ad means it ended or was removed. There is no price history endpoint.
5. **New-listing monitor:** poll `/search` with `sort: "newest"` and the filters you need, keep the ad ids you have already seen, and treat unseen ids as new. `newest` orders by last refresh, approximately (neighbouring ads can be a few minutes out of order; sort by `refreshed_at` yourself for a strict order), so check `created_at` to tell a new ad from a refreshed old one.
6. **Check a seller:** `seller.id` from any item feeds `/seller` (business or private, business name, member since, live ad count) and `/seller-ads` (their ads, with the search sorts and filters).

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | one of | Search keywords (1-200 chars), in any language. A query with no exact match returns the closest ads, never an empty list |
| `category_id` | string or integer | one of | Search inside one category: `categories[].id` of `/categories` or an item's `category_id` (e.g. `84` = cars on olx.pl). Send `query`, `category_id` or both |
| `country` | string | `pl` | `pl`, `ro`, `pt`, `bg`, `ua`, `kz` or `uz` |
| `language` | string | site's | `kz`: `kk` or `ru`; `uz`: `uz` or `ru`. Refused on the other sites |
| `page` | integer | 1 | 1-based. `page` x `page_size` may not exceed 1,000: OLX serves the first 1,000 results of a search only |
| `page_size` | integer | 40 | Ads per page, 1-50. Promoted ads come on top of these (a page of 40 returned about 52 items) |
| `sort` | string | `relevance` | `relevance`, `newest` (most recently posted or refreshed first), `price_low_to_high` or `price_high_to_low`. Promoted ads are not sorted |
| `min_price` / `max_price` | number | none | Price range in the site's currency. `min_price` must not be above `max_price` |
| `condition` | string | all | `new`, `used`, `refurbished` or `damaged`, in categories that have a condition |
| `seller_type` | string | all | `private` (individuals) or `business` |
| `olx_delivery` | boolean | false | Only ads that can be bought with OLX delivery (shipped through OLX). Not on `kz` or `uz` |
| `with_photos` | boolean | false | Only ads with photos |
| `region_id` | string or integer | none | Only ads in this region: `region_id` from `/locations` or an item's `location` |
| `city_id` | string or integer | none | Only ads in this city: `city_id` from `/locations` (e.g. `17871` = Warszawa) |
| `district_id` | string or integer | none | Only ads in this district of a city: `district_id` from `/locations` |
| `distance_km` | integer | none | With `city_id`: include ads within this many km of the city: `0`, `2`, `5`, `10`, `15`, `30`, `50`, `75` or `100` |
| `filters` | object | none | The category's own filters, keys from `/filters` `send_as`: a range as `filter_float_<name>:from` / `:to` with a number (`filter_float_year:from` 2018, `filter_float_milage:to` 100000), a choice as `filter_enum_<name>` with one value or a list (`filter_enum_rooms` `["two"]`). Up to 20 keys; other keys are refused |
| `include_promoted` | boolean | true | Keep the promoted ads OLX places on each page; each is flagged `is_promoted` with its slot |

### Offer (`/offer`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `offer_id` | string or integer | one of | An OLX ad id: `items[].id` of a search (e.g. `1107557408`) |
| `url` | string | one of | An OLX ad link on any of the seven sites. Send `offer_id` or `url`, not both |
| `country` | string | `pl` | Used with `offer_id`; a `url` sets its own market |
| `language` | string | site's | As on search (`kz` / `uz` only) |

### Seller (`/seller`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string or integer | required | An OLX seller id: `items[].seller.id` of a search or `seller.id` of an ad (e.g. `2547532895`) |
| `country` | string | `pl` | As on search |

### Seller ads (`/seller-ads`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `user_id` | string or integer | required | As on seller |
| `query` | string | none | Search within the seller's ads |
| `category_id` | string or integer | none | Only the seller's ads in this category |
| `country`, `language` | | | As on search |
| `page`, `page_size`, `sort`, every search filter, `include_promoted` | | | As on search |

### Filters (`/filters`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `category_id` | string or integer | required | The category (e.g. `14` = flats for sale on olx.pl, `84` = cars) |
| `query` | string | none | Count values for this keyword inside the category |
| `region_id` | string or integer | none | Count values in this region only (the location counts then list its cities) |
| `country` | string | `pl` | `pl`, `ro`, `pt`, `bg` or `ua` (`kz` and `uz` return `400`) |

### Categories (`/categories`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `parent_id` | string or integer | none | Return this category's whole subtree. Without it: the top-level categories with their direct children (`children_count` says which go deeper) |
| `country` | string | `pl` | As on search |

### Locations (`/locations`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | At least 2 letters of a city or district name (2-100 chars), in the site's language or script (`Warszawa`, `Bucuresti`, `Київ`, `Алматы`) |
| `country` | string | `pl` | As on search |

### Suggestions (`/suggestions`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `query` | string | required | What the user has typed so far (1-100 chars) |
| `country` | string | `pl` | As on search |

### Similar (`/similar`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `offer_id` / `url` | | one of | As on offer |
| `country` | string | `pl` | `pl`, `ro`, `pt`, `bg` or `ua` (`kz` and `uz` return `400`) |

## Examples

### Search

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "iphone"}'
```

Captured `data` (2 of 52 items shown: the first promoted ad and an organic one; params and photos trimmed to the first 2 and 1):

```json
{
  "query": "iphone",
  "category_id": null,
  "sort": "relevance",
  "applied_filters": {},
  "total": 159080,
  "total_capped": true,
  "page": 1,
  "page_size": 40,
  "total_pages": 25,
  "has_next_page": true,
  "count": 52,
  "promoted_count": 12,
  "items": [
    {
      "id": 1111695669,
      "url": "https://www.olx.pl/d/oferta/iphone-13-pro-128-gb-2-lata-gwarancji-bat-100-raty-0-CID99-ID1deyPj.html",
      "title": "iPhone 13 PRO 128 GB | 2 lata gwarancji | Bat.:  100%  | Raty 0%",
      "description_snippet": "Na sprzedaż jedna konkretna sztuka iPhone’a 13 PRO w super stanie! Specyfikacja: • Bateria 100% • Pamięć: 128B • Kolor: CZARNY • Stan wizualny: jak nowy Dlaczego warto? • Do 24 miesięcy gwarancji - z możliwością rozszerzenia o uszkodzenia mechaniczne. • Telefon w 100% sprawny, przetestowany. • 14...",
      "price": {
        "value": 1399,
        "currency": "PLN",
        "negotiable": true,
        "type": "price",
        "label": "1 399 zł",
        "previous_value": null,
        "original_value": null,
        "original_currency": null
      },
      "salary": null,
      "condition": "used",
      "params": [
        {"key": "state", "name": "Stan", "value": "Używane", "normalized_value": "used"},
        {"key": "phonemodel", "name": "Model telefonu", "value": "iPhone 13 Pro", "normalized_value": "iphone-13-pro"}
      ],
      "category_id": 2298,
      "category_type": "electronics",
      "location": {"city": "Poznań", "city_id": 13983, "district": "Jeżyce", "district_id": 325, "region": "Wielkopolskie", "region_id": 1},
      "created_at": "2026-11-12T14:05:55.000Z",
      "refreshed_at": "2026-11-12T14:09:28.000Z",
      "valid_to": "2026-12-12T14:05:56.000Z",
      "status": "active",
      "is_promoted": true,
      "promoted_position": 1,
      "is_highlighted": false,
      "is_business": true,
      "olx_delivery": false,
      "photos": ["https://ireland.apollo.olxcdn.com/v1/files/sjb6ebpp8b3n-PL/image;s=3491x3491"],
      "seller": {"id": 779240302, "business_name": "Luxtrade – zakupy, które dają więcej za mniej."}
    },
    {
      "id": 1111738479,
      "url": "https://www.olx.pl/d/oferta/iphone-12-64gb-czarny-CID99-ID1deJXN.html",
      "title": "iPhone 12 64GB czarny",
      "description_snippet": "Telefon działa bez zarzutu. Ma widoczne na zdjęciach ślady użytkowania, ekran posiada drobne ryski niewidoczne przy naklejonym szkle.",
      "price": {
        "value": 400,
        "currency": "PLN",
        "negotiable": true,
        "type": "price",
        "label": "400 zł",
        "previous_value": null,
        "original_value": null,
        "original_currency": null
      },
      "salary": null,
      "condition": "new",
      "params": [
        {"key": "state", "name": "Stan", "value": "Nowe", "normalized_value": "new"},
        {"key": "phonemodel", "name": "Model telefonu", "value": "iPhone 12", "normalized_value": "iphone-12"}
      ],
      "category_id": 2298,
      "category_type": "electronics",
      "location": {"city": "Kielce", "city_id": 7971, "district": null, "district_id": null, "region": "Świętokrzyskie", "region_id": 13},
      "created_at": "2026-11-12T17:20:11.000Z",
      "refreshed_at": "2026-11-12T17:23:38.000Z",
      "valid_to": "2026-12-12T17:20:12.000Z",
      "status": "active",
      "is_promoted": false,
      "promoted_position": null,
      "is_highlighted": false,
      "is_business": false,
      "olx_delivery": true,
      "photos": ["https://ireland.apollo.olxcdn.com/v1/files/e26mne9np6vo1-PL/image;s=750x1000"],
      "seller": {"id": 131292893, "business_name": null}
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

`count` is 52 for a `page_size` of 40 because 12 promoted ads (`promoted_count`) sit on the page with the 40 organic ones. They are interleaved, not grouped: on this page slots 1-3 were promoted, then organic ads, then promoted again from slot 14. Organic ads have `is_promoted: false` and `promoted_position: null`. `total` is OLX's count of matching ads (159,080) and `total_capped: true` says there are more than the 1,000 anyone can page through, so `total_pages` is 25 at 40 per page.

### Offer

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/offer \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"offer_id": "1107557408"}'
```

Captured `data` (description cut to its first lines and 4 of 6 photos trimmed):

```json
{
  "id": 1107557408,
  "url": "https://www.olx.pl/d/oferta/iphone-13-pro-128gb-graphite-pudelko-etui-szybki-ochronne-100-sprawny-CID99-ID1cXcha.html",
  "title": "iPhone 13 Pro 128GB Graphite | Pudełko + Etui + Szybki ochronne | 100% Sprawny",
  "description": "TYLKO ODBIÓR OSOBISTY\n\nCześć!\n\nMam na sprzedaż flagowy smartphone iPhone 13 Pro w wersji 128 GB i klasycznym, eleganckim kolorze Graphite (Grafitowy).\n\nTelefon ...",
  "price": {
    "value": 950,
    "currency": "PLN",
    "negotiable": false,
    "type": "price",
    "label": "950 zł",
    "previous_value": null,
    "original_value": null,
    "original_currency": null
  },
  "salary": null,
  "condition": "used",
  "params": [
    {"key": "state", "name": "Stan", "value": "Używane", "normalized_value": "used"},
    {"key": "phonemodel", "name": "Model telefonu", "value": "iPhone 13 Pro", "normalized_value": "iphone-13-pro"},
    {"key": "builtinmemory_phones", "name": "Wbudowana pamięć", "value": "128GB", "normalized_value": "128gb"},
    {"key": "phonecharger", "name": "Ładowarka w komplecie", "value": "Nie", "normalized_value": "no"}
  ],
  "category": {
    "id": 2298,
    "type": "electronics",
    "breadcrumb": [
      {"id": 99, "name": "Elektronika", "url": "https://www.olx.pl/elektronika/"},
      {"id": 1838, "name": "Telefony", "url": "https://www.olx.pl/elektronika/telefony/"},
      {"id": 1839, "name": "Smartfony i telefony komórkowe", "url": "https://www.olx.pl/elektronika/telefony/smartfony-telefony-komorkowe/"},
      {"id": 2298, "name": "iPhone", "url": "https://www.olx.pl/elektronika/telefony/smartfony-telefony-komorkowe/iphone/"}
    ]
  },
  "location": {"city": "Warszawa", "city_id": 17871, "district": "Żoliborz", "district_id": 363, "region": "Mazowieckie", "region_id": 2},
  "photos": [
    "https://ireland.apollo.olxcdn.com/v1/files/tomgr0m5ytyr-PL/image;s=1000x750",
    "https://ireland.apollo.olxcdn.com/v1/files/nzisvmy1quun1-PL/image;s=1000x750"
  ],
  "created_at": "2026-10-25T13:39:23.000Z",
  "refreshed_at": "2026-10-25T13:41:50.000Z",
  "valid_to": "2026-11-24T13:39:24.000Z",
  "status": "active",
  "is_active": true,
  "is_business": false,
  "is_promoted": true,
  "is_highlighted": true,
  "olx_delivery": false,
  "is_job": false,
  "seller": {"id": 8598981, "is_business": false, "business_name": null, "member_since": "2012-08-04T16:03:23.000Z"},
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

`seller` is an id and `member_since` only, because this is a private seller (`is_business: false`, `business_name: null`). `is_job` is `true` on job ads, which carry `salary` (`from`, `to`, `period`, `currency`, `gross`, `negotiable`) and no photos.

### Seller

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "2547532895"}'
```

Captured `data`:

```json
{
  "id": 2547532895,
  "is_business": true,
  "business_name": "Smartfony.net - Ogrodowa 9, Poznań",
  "member_since": "2025-06-03T11:53:41.000Z",
  "ads_url": "https://www.olx.pl/oferty/user/2MpbGf/",
  "active_ads": 65,
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

`business_name` is the name OLX shows for a business seller (here a shop with its address as part of its name); it is `null` for private sellers. OLX shows no seller ratings or reviews, so there are none to return.

### Seller ads

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/seller-ads \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "2547532895"}'
```

Captured `data` (1 of 40 items shown, trimmed as on search):

```json
{
  "user_id": 2547532895,
  "query": null,
  "category_id": null,
  "sort": "relevance",
  "applied_filters": {},
  "total": 65,
  "total_capped": false,
  "page": 1,
  "page_size": 40,
  "total_pages": 2,
  "has_next_page": true,
  "count": 40,
  "promoted_count": 0,
  "items": [
    {
      "id": 1100659974,
      "url": "https://www.olx.pl/d/oferta/iphone-17-512-gb-white-sim-esim-standard-asis-bateria-100-0-cykli-gwarancja-12m-nieaktywowany-CID99-ID1cufVe.html",
      "title": "iPhone 17 512 GB White | SIM+eSIM | Standard ASIS+ | Bateria 100% | 0 cykli | Gwarancja 12M | NIEAKTYWOWANY",
      "description_snippet": "APPLE IPHONE 17 512gb WHITE Nieaktywowany | Oryginalne części Apple | 100% bateria | 0 cykli | Zweryfikowany IMEI | Raty na Smartfony.net STANDARD ASIS+ Bez historii aktywacji • Gwarancja dystrybutora • Najkorzystniejsza cena ⸻ NAJWAŻNIEJSZE INFORMACJE Model: iPhone 17 Pamięć: 512 GB Kolor: White...",
      "price": {
        "value": 3799,
        "currency": "PLN",
        "negotiable": false,
        "type": "price",
        "label": "3 799 zł",
        "previous_value": null,
        "original_value": null,
        "original_currency": null
      },
      "salary": null,
      "condition": "new",
      "params": [
        {"key": "state", "name": "Stan", "value": "Nowe", "normalized_value": "new"},
        {"key": "phonemodel", "name": "Model telefonu", "value": "iPhone 17", "normalized_value": "iphone-17"}
      ],
      "category_id": 2298,
      "category_type": "electronics",
      "location": {"city": "Poznań", "city_id": 13983, "district": "Winogrady", "district_id": 727, "region": "Wielkopolskie", "region_id": 1},
      "created_at": "2026-09-25T11:47:35.000Z",
      "refreshed_at": "2026-11-12T16:02:21.000Z",
      "valid_to": "2026-11-24T11:47:35.000Z",
      "status": "active",
      "is_promoted": false,
      "promoted_position": null,
      "is_highlighted": true,
      "is_business": true,
      "olx_delivery": true,
      "photos": ["https://ireland.apollo.olxcdn.com/v1/files/kkei0bodf4ix2-PL/image;s=838x1000"],
      "seller": {"id": 2547532895, "business_name": "Smartfony.net - Ogrodowa 9, Poznań"}
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

### Filters

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/filters \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "14"}'
```

Captured `data` (3 of 9 filters and 3 region counts shown):

```json
{
  "category_id": 14,
  "query": null,
  "region_id": null,
  "total": 41437,
  "filters": [
    {
      "key": "filter_enum_market",
      "label": "Rynek",
      "type": "select",
      "kind": "choice",
      "unit": null,
      "send_as": ["filter_enum_market"],
      "steps": [],
      "values": [{"value": "primary", "label": "Pierwotny", "count": 11397}, {"value": "secondary", "label": "Wtórny", "count": 30040}]
    },
    {
      "key": "filter_float_m",
      "label": "Powierzchnia",
      "type": "input",
      "kind": "range",
      "unit": "m²",
      "send_as": ["filter_float_m:from", "filter_float_m:to"],
      "steps": [25, 40, 50, 60, 70, 80, 100, 120, 150],
      "values": []
    },
    {
      "key": "filter_enum_rooms",
      "label": "Liczba pokoi",
      "type": "select",
      "kind": "choice",
      "unit": null,
      "send_as": ["filter_enum_rooms"],
      "steps": [],
      "values": [
        {"value": "one", "label": "1 pokój", "count": 4004},
        {"value": "two", "label": "2 pokoje", "count": 16622},
        {"value": "three", "label": "3 pokoje", "count": 15102},
        {"value": "four", "label": "4 i więcej", "count": 5709}
      ]
    }
  ],
  "locations": {
    "type": "region",
    "items": [{"id": 2, "name": "Mazowieckie", "count": 6874}, {"id": 6, "name": "Śląskie", "count": 5806}, {"id": 3, "name": "Dolnośląskie", "count": 4378}]
  },
  "categories": [
    {"id": 3, "name": "Nieruchomości", "count": 41437},
    {"id": 14, "name": "Sprzedaż", "count": 41437},
    {"id": 1307, "name": "Mieszkania", "count": 41437}
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

Send a filter back to `/search` under its `send_as` key: a range filter takes a number per bound, a choice filter takes `values[].value` ids. For flats of 40 m² and up with two or three rooms in Warszawa:

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"category_id": "14", "city_id": "17871", "sort": "newest", "filters": {"filter_float_m:from": 40, "filter_enum_rooms": ["two", "three"]}}'
```

### Categories

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/categories \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Captured `data` (1 of 19 top-level categories shown, with 2 of its 12 children):

```json
{
  "parent_id": null,
  "parent": null,
  "count": 19,
  "categories": [
    {
      "id": 5,
      "name": "Motoryzacja",
      "parent_id": null,
      "level": 1,
      "path": "motoryzacja",
      "url": "https://www.olx.pl/motoryzacja/",
      "type": "automotive",
      "count": 4585439,
      "children_count": 12,
      "children": [
        {
          "id": 80,
          "name": "Pozostała motoryzacja",
          "parent_id": 5,
          "level": 2,
          "path": "motoryzacja/pozostala-motoryzacja",
          "url": "https://www.olx.pl/motoryzacja/pozostala-motoryzacja/",
          "type": "automotive",
          "count": 1272,
          "children_count": 0
        },
        {
          "id": 81,
          "name": "Motocykle i Skutery",
          "parent_id": 5,
          "level": 2,
          "path": "motoryzacja/motocykle-skutery",
          "url": "https://www.olx.pl/motoryzacja/motocykle-skutery/",
          "type": "automotive",
          "count": 47198,
          "children_count": 9
        }
      ]
    }
  ],
  "total_categories": 3357,
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

### Locations

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/locations \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "Warszawa"}'
```

Captured `data` (3 of 20 locations shown):

```json
{
  "query": "Warszawa",
  "count": 20,
  "locations": [
    {
      "type": "city",
      "city": "Warszawa",
      "city_id": 17871,
      "district": null,
      "district_id": null,
      "municipality": "Warszawa",
      "county": "Warszawa",
      "region": "Mazowieckie",
      "region_id": 2
    },
    {
      "type": "city",
      "city": "Warszawa",
      "city_id": 76109,
      "district": null,
      "district_id": null,
      "municipality": "Wronki",
      "county": "szamotulski",
      "region": "Wielkopolskie",
      "region_id": 1
    },
    {
      "type": "district",
      "city": "Warszawa",
      "city_id": 17871,
      "district": "Białołęka",
      "district_id": 365,
      "municipality": "Warszawa",
      "county": "Warszawa",
      "region": "Mazowieckie",
      "region_id": 2
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

Two cities share the name: `city_id` 17871 is the capital (Mazowieckie), 76109 a village in Wielkopolskie. Check `region` before using an id.

### Suggestions

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/suggestions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "rower"}'
```

Captured `data` (3 of 10 suggestions shown):

```json
{
  "query": "rower",
  "count": 10,
  "suggestions": [
    {
      "text": "rower",
      "type": "category",
      "category_id": 1651,
      "category": "Rowery górskie",
      "parent_categories": [{"id": 461, "name": "Rowery"}, {"id": 767, "name": "Sport i Hobby"}]
    },
    {
      "text": "rower elektryczny",
      "type": "category",
      "category_id": 1649,
      "category": "Rowery elektryczne",
      "parent_categories": [{"id": 461, "name": "Rowery"}, {"id": 767, "name": "Sport i Hobby"}]
    },
    {
      "text": "rower",
      "type": "category",
      "category_id": 1650,
      "category": "Rowery miejskie",
      "parent_categories": [{"id": 461, "name": "Rowery"}, {"id": 767, "name": "Sport i Hobby"}]
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

### Similar

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/similar \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"offer_id": "1107557408"}'
```

Captured `data` (1 of 29 items shown, trimmed as on search):

```json
{
  "offer_id": 1107557408,
  "count": 29,
  "items": [
    {
      "id": 1109127005,
      "url": "https://www.olx.pl/d/oferta/iphone-13-pro-128gb-CID99-ID1d3MBf.html",
      "title": "Iphone 13 pro 128gb",
      "description_snippet": "iPhone 13 Pro z pamięcią wewnętrzną 128 GB. Telefon w stanie jak na zdjęciu",
      "price": {
        "value": 550,
        "currency": "PLN",
        "negotiable": true,
        "type": "price",
        "label": "550 zł",
        "previous_value": null,
        "original_value": null,
        "original_currency": null
      },
      "salary": null,
      "condition": "used",
      "params": [
        {"key": "state", "name": "Stan", "value": "Używane", "normalized_value": "used"},
        {"key": "phonemodel", "name": "Model telefonu", "value": "iPhone 13 Pro", "normalized_value": "iphone-13-pro"}
      ],
      "category_id": 2298,
      "category_type": "electronics",
      "location": {"city": "Warszawa", "city_id": 17871, "district": "Włochy", "district_id": 357, "region": "Mazowieckie", "region_id": 2},
      "created_at": "2026-11-01T09:46:22.000Z",
      "refreshed_at": "2026-11-01T09:49:37.000Z",
      "valid_to": "2026-12-01T09:46:23.000Z",
      "status": "active",
      "is_promoted": false,
      "promoted_position": null,
      "is_highlighted": false,
      "is_business": false,
      "olx_delivery": false,
      "photos": ["https://ireland.apollo.olxcdn.com/v1/files/59k1anh7bm4i2-PL/image;s=750x1000"],
      "seller": {"id": 2308444981, "business_name": null}
    }
  ],
  "country": "pl",
  "language": "pl",
  "currency": "PLN"
}
```

### olx.uz: converted prices and Russian labels

```bash
curl -X POST https://api.scavio.dev/api/v1/olx/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "iphone", "country": "uz"}'
```

One captured item (params and photos trimmed):

```json
{
  "id": 66722816,
  "url": "https://www.olx.uz/d/obyavlenie/iphone-17-80-sicl-ID4wXEs.html",
  "title": "iphone 17 80 sicl",
  "description_snippet": "Продам iPhone 17 256gb sim+ esim 2 симкарты прошли регистрацию 80 циклов зарядки ,ещё на гарантии ,телефон в новом состоянии.",
  "price": {
    "value": 10058412,
    "currency": "UZS",
    "negotiable": true,
    "type": "price",
    "label": "10 058 412 сум",
    "previous_value": 10297898,
    "original_value": 840,
    "original_currency": "UYE"
  },
  "salary": null,
  "condition": "new",
  "params": [
    {"key": "mobile_phone_manufacturer", "name": "Марка телефона", "value": "Apple", "normalized_value": "2065"},
    {"key": "state", "name": "Состояние", "value": "Новый", "normalized_value": "new"}
  ],
  "category_id": 85,
  "category_type": "electronics",
  "location": {"city": "Самарканд", "city_id": 161, "district": null, "district_id": null, "region": "Самаркандская область", "region_id": 33},
  "created_at": "2026-11-10T08:42:31.000Z",
  "refreshed_at": "2026-11-10T08:44:48.000Z",
  "valid_to": "2026-12-10T08:42:31.000Z",
  "status": "active",
  "is_promoted": true,
  "promoted_position": 3,
  "is_highlighted": true,
  "is_business": false,
  "olx_delivery": false,
  "photos": ["https://frankfurt.apollo.olxcdn.com/v1/files/ae6n5b52zpq92-UZ/image;s=700x700"],
  "seller": {"id": 535487416, "business_name": null}
}
```

The seller priced this ad at 840 y.e. (`original_value`, `original_currency: "UYE"`); `value` is the site's UZS conversion and `previous_value` is the earlier price in UZS. Labels are Russian because olx.uz answers in Russian unless `language: "uz"` is sent. On olx.kz and olx.uz, `total` is `null` once a search reaches 1,000 ads, because those sites hide the real count; smaller result sets, such as one seller's ads, still return the real number.

An olx.uz ad read with `/offer` (captured, other fields trimmed):

```json
{
  "id": 66749653,
  "url": "https://www.olx.uz/d/obyavlenie/iphone-16pro-max-256-desert-titan-esim-ID4v4Dj.html",
  "title": "Iphone 16Pro Max 256 Desert Titan E'sim",
  "price": {
    "value": 8920853.5,
    "currency": "UZS",
    "negotiable": true,
    "type": "price",
    "label": "745 у.е.",
    "previous_value": null,
    "original_value": 745,
    "original_currency": "UYE"
  },
  "country": "uz",
  "language": "ru",
  "currency": "UZS"
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

def olx(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/olx/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()["data"]

# 1. Resolve the city id (1 credit)
city = next(l for l in olx("locations", {"query": "Warszawa"})["locations"]
            if l["type"] == "city" and l["region"] == "Mazowieckie")

# 2. Newest ads in the category, organic only (1 credit per poll)
seen = set()  # persist this between runs in real code

def poll():
    res = olx("search", {
        "category_id": "14",
        "city_id": city["city_id"],
        "sort": "newest",
        "include_promoted": False,
        "filters": {"filter_float_m:from": 40, "filter_enum_rooms": ["two", "three"]},
    })
    fresh = [i for i in res["items"] if i["id"] not in seen]
    seen.update(i["id"] for i in res["items"])
    return fresh

for ad in poll():
    p = ad["price"] or {}
    print(ad["created_at"], ad["refreshed_at"], p.get("value"), p.get("currency"), ad["title"], ad["url"])
```

The first run fills `seen`; later runs return only ads not seen before. Compare `created_at` with your last run time to separate brand-new ads from refreshed old ones.

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched live.

- **ad item** (search, seller-ads and similar `items[]`) - `id`, `url`, `title`, `description_snippet`, `price` {`value`, `currency`, `negotiable`, `type` (`price`, `free`, `exchange`, `budget`), `label`, `previous_value`, `original_value`, `original_currency`} or `null`, `salary` {`from`, `to`, `period`, `currency`, `gross`, `negotiable`} or `null`, `condition`, `params[]` {`key`, `name`, `value`, `normalized_value`}, `category_id`, `category_type`, `location` {`city`, `city_id`, `district`, `district_id`, `region`, `region_id`}, `created_at`, `refreshed_at`, `valid_to`, `status`, `is_promoted`, `promoted_position`, `is_highlighted`, `is_business`, `olx_delivery`, `photos[]`, `seller` {`id`, `business_name`}.
- **search** - `query`, `category_id`, `sort`, `applied_filters`, `total`, `total_capped`, `page`, `page_size`, `total_pages`, `has_next_page`, `count`, `promoted_count`, `items[]`, `country`, `language`, `currency`.
- **seller-ads** - `user_id` plus the search fields.
- **similar** - `offer_id`, `count`, `items[]`, `country`, `language`, `currency`.
- **offer** - `id`, `url`, `title`, `description`, `price`, `salary`, `condition`, `params[]`, `category` {`id`, `type`, `breadcrumb[]` {`id`, `name`, `url`}}, `location`, `photos[]`, `created_at`, `refreshed_at`, `valid_to`, `status`, `is_active`, `is_business`, `is_promoted`, `is_highlighted`, `olx_delivery`, `is_job`, `seller` {`id`, `is_business`, `business_name`, `member_since`}, `country`, `language`, `currency`.
- **seller** - `id`, `is_business`, `business_name`, `member_since`, `ads_url`, `active_ads` (`null` on kz and uz for a seller with 1,000 or more ads), `country`, `language`, `currency`.
- **filters** - `category_id`, `query`, `region_id`, `total`, `filters[]` {`key`, `label`, `type`, `kind` (`range`, `choice`), `unit`, `send_as[]`, `steps[]`, `values[]` {`value`, `label`, `count`}}, `locations` {`type` (`region`, `city`), `items[]` {`id`, `name`, `count`}}, `categories[]` {`id`, `name`, `count`}, `country`, `language`, `currency`.
- **categories** - `parent_id`, `parent`, `count`, `total_categories`, `categories[]` {`id`, `name`, `parent_id`, `level`, `path`, `url`, `type`, `count`, `children_count`, `children[]`}, `country`, `language`, `currency`.
- **locations** - `query`, `count`, `locations[]` {`type` (`city`, `district`), `city`, `city_id`, `district`, `district_id`, `municipality`, `county`, `region`, `region_id`}, `country`, `language`, `currency`.
- **suggestions** - `query`, `count`, `suggestions[]` {`text`, `type` (`query`, `category`), `category_id`, `category`, `parent_categories[]` {`id`, `name`}}, `country`, `language`, `currency`.

## Guardrails

- OLX Europe only: olx.pl, olx.ro, olx.pt, olx.bg, olx.ua, olx.kz and olx.uz. Never present results as OLX Brasil, OLX India, OLX Bosnia or a Dubizzle-run OLX site.
- Always give the currency (PLN, RON, EUR, UAH, KZT, UZS) and the site. Never add up or compare prices across sites as if they were one market.
- Prices are asking prices on live ads, not sale prices. `price` is `null` on some service ads; `type: "free"` (giveaway) and `"exchange"` (swap) ads have `value: 0`, and implausible prices appear (one captured olx.pl search had a phone at 70,000,000 zł). Filter by `type` and a sensible price range before quoting a minimum, average or "cheapest".
- `previous_value` is the earlier price when the seller lowered it. It is not a price history; for one, poll and store prices yourself.
- Converted prices: when `original_currency` is set, `value` is the site's conversion and `original_value` / `original_currency` are what the seller asked. Quote both when it matters.
- The search window is 1,000 results (OLX's own cap). `total_capped: true` means more ads exist than can be paged; narrow by category, location, price or filters to reach the rest. On kz and uz, `total` is `null` for those large searches.
- Promoted ads are paid placements interleaved with organic results and are not sorted by the chosen sort. Use `is_promoted` / `promoted_position` to separate organic from paid, or send `include_promoted: false`. Never call the first result the cheapest or the newest without checking.
- `newest` orders by the last refresh, not first posting: sellers can refresh an ad to the top. Use `created_at` for when the ad was first posted and `refreshed_at` for the last refresh.
- A nonsense or misspelled query returns the closest ads OLX finds, not an empty list. Check titles before reporting that something is listed.
- `condition` and every parameter are what the seller chose. Read the description before relying on them.
- Category filters are per category and per site. Get the keys from `/filters` (`send_as`) and the choice values from `values[].value`; any other key is refused with `400`.
- Sellers: `is_business` separates business sellers from private individuals; `business_name` is the name OLX shows for a business seller and is `null` for private sellers. OLX shows no seller ratings or reviews, and there are no view counts, so neither is returned. Use seller data to judge a listing or track business resellers, not to profile or contact private persons.
- Never returned: private sellers' names, phone numbers, emails, exact map positions, last-seen times, profile photos and car VINs. Phone numbers and emails inside ad text come back as `[phone removed]` / `[email removed]`. Do not try to recover them.
- Not available: messaging, phone reveal, delivery prices or checkout, buying or bidding, price statistics or average prices, price history, view counts, seller ratings and notifications. This API reads ads; it does not post, manage or contact.
- OLX's terms change over time. Before building a product on OLX data, check OLX's current terms and your local law; this is not legal advice.
- Never fabricate prices, ads, sellers or counts. Only return what the API returned, with the ad `url`.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no `query` or `category_id` on search; neither or both of `offer_id` / `url`; a `url` that is not an OLX ad link on one of the seven sites, or one whose site differs from `country`; `language` on a site other than kz / uz, or on an endpoint other than search, seller-ads and offer; `country` `kz` or `uz` on `/filters` or `/similar`; `olx_delivery` on kz or uz; `page` x `page_size` above 1,000; `min_price` above `max_price`; `distance_km` without `city_id`; a `filters` key that is not a `filter_float_` / `filter_enum_` key; a price range sent both as `min_price` / `max_price` and in `filters`; `condition` together with a `filter_enum_state` filter; a `locations` query under 2 letters.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means no such ad or seller. An ad that never existed and an ad that has ended answer the same `404` ("does not exist or is no longer active"). Not-founds are charged (1 credit): take ids and links from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api).
- `502` means OLX was temporarily unavailable or returned an unusable answer. Upstream checks sometimes fail; retried automatically. It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means OLX is busy: wait the `Retry-After` seconds (5) and send it again. Not charged.

## SDKs

```bash
pip install scavio==0.53.0
npm install scavio@0.54.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: found } = await scavio.olx.search({ query: "iphone", sort: "price_low_to_high", condition: "used" });
const { data: ad } = await scavio.olx.offer({ offer_id: "1107557408" });
const { data: seller } = await scavio.olx.seller({ user_id: "2547532895" });
const { data: ads } = await scavio.olx.sellerAds({ user_id: "2547532895", sort: "newest" });
const { data: filters } = await scavio.olx.filters({ category_id: "14" });
const { data: tree } = await scavio.olx.categories({ parent_id: "5" });
const { data: places } = await scavio.olx.locations({ query: "Warszawa" });
const { data: typed } = await scavio.olx.suggestions({ query: "rower" });
const { data: similar } = await scavio.olx.similar({ offer_id: "1107557408" });
const { data: kz } = await scavio.olx.search({ query: "iphone", country: "kz", language: "kk" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.olx.search(...)`, `client.olx.offer(...)`, `client.olx.seller(...)`, `client.olx.seller_ads(...)`, `client.olx.filters(...)`, `client.olx.categories(...)`, `client.olx.locations(...)`, `client.olx.suggestions(...)` and `client.olx.similar(...)`.

## MCP

The Scavio MCP server exposes all nine endpoints as tools: `search_olx`, `get_olx_offer`, `get_olx_seller`, `get_olx_seller_ads`, `get_olx_filters`, `get_olx_categories`, `search_olx_locations`, `get_olx_suggestions` and `get_olx_similar`. OLX is opt-in: add `olx` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.51.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,olx"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/olx-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [offer](https://scavio.dev/docs/olx-offer?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [seller](https://scavio.dev/docs/olx-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [seller ads](https://scavio.dev/docs/olx-seller-ads?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [filters](https://scavio.dev/docs/olx-filters?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [categories](https://scavio.dev/docs/olx-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [locations](https://scavio.dev/docs/olx-locations?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [suggestions](https://scavio.dev/docs/olx-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api), [similar](https://scavio.dev/docs/olx-similar?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api). Overview: [OLX API](https://scavio.dev/olx-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=olx-api).
