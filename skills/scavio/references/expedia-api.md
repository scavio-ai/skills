# Expedia API - Hotel Prices, Property Details, Price Calendar

Read Expedia (expedia.com, Expedia Group's travel booking site): hotel search for a place and dates with Expedia's sorts and filters, one property in full, Expedia's price calendar for a property, and Expedia's destination suggestions. Every answer is what Expedia's public pages show a visitor without an account at the moment of the call, in the market's language and currency (51 market-languages). All 4 endpoints return structured JSON, billed on what each call costs: 2 credits per call in the captures.

**Read-only data.** This skill reads the public pages Expedia shows to any visitor and returns them as JSON for analysis. It uses no Expedia account, no member sign-in, no saved trip, no booking and no payment step.

**The job this skill is for: what a hotel stay costs on Expedia for given dates, as Expedia's first results page shows it.** `/search` returns, for each property Expedia shows at the top of its first results page, the price for those exact dates: the nightly price, the stay total, the struck-through price and Expedia's own fee line, in the market's currency. Captured 2026-11-26:

| Search (`market`) | Dates, guests | `matched_total`, `count` | One property card (`price`) |
|---|---|---|---|
| Las Vegas, NV (`us`) | Jan 25-28, 2027 (3 nights), 2 adults | 487, 3 (`partial: true`) | New York-New York Hotel & Casino: "$558 total" ($119 nightly, was $796), "Total with taxes and fees", badges Ad and Member Price available |
| Las Vegas, NV (`us`) | Jan 20-23, 2027, 2 adults | 24, 10 (`partial: false`) | ARIA Resort & Casino: "$1,297 total" ($326 nightly, was $1,932) |
| London, England (`en-gb`) | Jan 25-28, 2027, 2 adults | 500, 3 (`partial: true`) | Bedford Hotel: "£398" for 3 nights (£133 per night), "includes taxes & fees", rating 8.8 (1,870 reviews) |
| Paris, France (`fr-fr`) | Mar 5-7, 2027, 2 adults | 484, 3 (`partial: true`) | Hotel de Roubaix: "430 €" for 2 nights (215 € par nuit, was 543 €), "taxes et frais compris", deal "-113 €", rating 9,4 Exceptionnel |
| 東京 (`ja-jp`) | Feb 1-4, 2027, 2 adults | 497, 3 (`partial: true`) | ザ ノット 東京新宿: "￥14,695" a night (was ￥23,300), "合計 ￥48,492", deal "ブラックフライデー 37% OFF" |

`price.lead` says which figure is the card's large price: the stay total in the `us`, `en-gb` and `fr-fr` captures, the nightly price in `ja-jp`. Quote both figures with the dates, the guests, the market and the fee line as Expedia wrote it. For the same hotel on other sites use `booking-com-hotel-data` or `google-hotels-api`, matched on dates and guests; for guest reviews, which this skill does not return, `tripadvisor-reviews-api`.

Nine limits shape every answer, so say them plainly:
- **Billed on actual cost: 2 credits per call in the captures.** Each call is billed on what the attempt that answered for the right market cost: 2 credits for most pages, 1 on some New Zealand, Korea and Indonesia pages. Expedia sometimes answers with another country's site; Scavio asks again (up to 3 attempts, suggestions 2), and those attempts are not billed. `credits_used` in every answer says what was spent. A call needs 6 credits of balance to start (suggestions 4), since that is the most it can hold. A not-found (`404`) is charged; a refused input (`400`), another market's page and an upstream failure (`502`, `503`) are not.
- **The first results page only, usually 3 properties.** `/search` returns the top results Expedia shows on the first page of its results. On most requests that page carries 3 properties (`partial: true`, with a note); on some it carries 10. No further page can be fetched. `matched_total` is Expedia's own count of matches. Narrow with `sort`, `star`, `amenity` and `guest_rating_min`, or retry later for more of the first page. Say so whenever `partial` is true.
- **Prices are for the dates asked, as Expedia shows them.** `price` {`amount`, `amount_display`, `lead`, `nightly`, `nightly_display`, `total`, `total_display`, `was`, `was_display`, `was_applies_to`, `fees_text`, `stay_text`, `price_messages`, `currency`}; `fees_text` is Expedia's own line ("Total with taxes and fees", "includes taxes & fees"). A card Expedia shows without a price has `price: null`.
- **Sponsored cards stay in place.** `sponsored: true` marks Expedia's paid placements (its "Ad" badge; all 3 cards on the Las Vegas capture). Report them as Expedia's ads, in their position.
- **A property is fetched without dates.** `/property` returns the hotel's page in full but no rooms and no rates for dates. For dated prices use `/search`; for a price per day use `/price-calendar`.
- **The price calendar is Expedia's own figure.** `/price-calendar` returns the price Expedia shows for each day, from today to about 10 months ahead (up to 302 days), labelled by Expedia "Lowest prices in the past 24 hours" (`label` in the market's language, `label_en` in English; the `ja-jp` capture read "過去 24 時間の最低価格 (税、サービス料別)", taxes and service charges not included). `check_in` and `check_out` only open the page; the calendar spans Expedia's own window. A day without a price has `price: null`.
- **Hotel pages are held in 7 markets.** `/property` and `/price-calendar` are not available in `en-gb`, `pt-br`, `zh-hk`, `en-hk`, `zh-hans-hk`, `en-my` and `en-ph`: Expedia answered hotel pages there with another country's site on every probe. Search and suggestions work in those markets.
- **Slow pages.** In the captures suggestions answered in 1.9 to 4.2 seconds, search in 4 to 13, a property in 4.3 to 14 and a price calendar in 3.2 to 13. A call can take up to about 4 minutes when Expedia answers slowly: set a client timeout of at least 250 seconds and send one request at a time.
- **What is not there.** No review texts (the rating summary and Expedia's own `guest_liked` lines only), no rooms or rates on a property, no results past Expedia's first page, no flights, cars, packages or activities, no booking, no member-only prices behind sign-in. Vrbo and Expedia Group's other sites are separate.

Expedia Group's own API access (its Rapid API for content, shopping and booking) is for approved partners, not a self-serve key. This skill reads Expedia's public pages with one Scavio key.

See also: `vrbo-api` (Expedia Group's vacation rental site), `booking-com-hotel-data` and `google-hotels-api` (hotel prices for the same dates), and `tripadvisor-reviews-api` (guest reviews). Same hotel, same dates and guests: name the site, market, currency and capture date with every price.

## When to trigger

Use this skill when the user asks to:
- Find Expedia hotels in a place for specific dates and adults, with the nightly price, the stay total, the struck-through price and Expedia's fee line
- Sort Expedia results by price or guest rating, or filter by star rating, an amenity (pool, pets, free parking, spa ...) or a minimum guest rating
- Compare what a hotel stay costs on Expedia across markets and currencies (US, UK, Canada in English or French, Germany, France, Spain, Italy, Mexico, Japan, Korea, Australia, India, UAE ...)
- Read one Expedia property in full: stars, address, guest rating summary, every amenity, every fee, deposit and resort fee line, check-in and check-out policies, pet and children policies, nearby places, FAQs and photos
- Read Expedia's price calendar for a hotel: the price per day Expedia shows for the coming months
- Look up Expedia's destination suggestions and region ids for a place name

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 2 credits each in the captures (1 on some New Zealand, Korea and Indonesia pages), so 50 credits cover about 25 calls (for example 8 hotels: one search, one property page and one price calendar each).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 1.9-4.2 seconds, search in 4-13, property in 4.3-14 and the price calendar in 3.2-13. A call can take up to about 4 minutes when Expedia answers slowly. Set a client timeout of at least 250 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/expedia/search` | The top hotels Expedia shows on the first page of its results for a place, dates and adults (3 on most requests, up to 10), with Expedia's sorts and filters: nightly price, stay total, struck-through price, fee line, deal, scarcity text, rating, badges, Member Price and VIP Access flags, sponsored flag, coordinates, images; `matched_total`, `partial` | 2 (actual cost) |
| `POST /api/v1/expedia/property` | One property by id or path, without dates: stars, address, coordinates, region id, rating summary, description, every amenity group, guest-liked lines, every fee line, policies, important information, nearby places, FAQs, photos | 2 (actual cost) |
| `POST /api/v1/expedia/price-calendar` | Expedia's price calendar for one property: the price per day from today to about 10 months ahead, with Expedia's label | 2 (actual cost) |
| `POST /api/v1/expedia/suggestions` | Destination suggestions for a partial place name: type, region id, names, coordinates, country, airport code | 2 (actual cost) |

## Market

51 Expedia market-languages, chosen with `market` (default `us`); each answers in its own language and currency. A bare country code picks the market's main language (`gb` -> `en-gb`, `de` -> `de-de`, `jp` -> `ja-jp`, `be` -> `nl-be`, `hk` -> `zh-hk`). Labels and texts come in the market's language as Expedia writes them; field names are English. `es-cl`, `es-co`, `es-pe`, `es-cr` and `en-eg` are Expedia's Chile, Colombia, Peru, Costa Rica and Egypt sites, served on expedia.com in their own currency.

| `market` | Market | Site | Language, currency | Property and price calendar |
|---|---|---|---|---|
| `us` | United States | expedia.com | en_US, USD | yes |
| `es-us` | United States (Spanish) | expedia.com | es_MX, USD | yes |
| `zh-us` | United States (Chinese) | expedia.com | zh_CN, USD | yes |
| `en-gb` | United Kingdom | expedia.co.uk | en_GB, GBP | held |
| `en-ie` | Ireland | expedia.ie | en_IE, EUR | yes |
| `en-ca` | Canada | expedia.ca | en_CA, CAD | yes |
| `fr-ca` | Canada (French) | expedia.ca | fr_CA, CAD | yes |
| `en-au` | Australia | expedia.com.au | en_AU, AUD | yes |
| `en-nz` | New Zealand | expedia.co.nz | en_AU, NZD | yes |
| `de-de` | Germany | expedia.de | de_DE, EUR | yes |
| `de-at` | Austria | expedia.at | de_DE, EUR | yes |
| `de-ch` | Switzerland | expedia.ch | de_CH, CHF | yes |
| `fr-ch` | Switzerland (French) | expedia.ch | fr_CH, CHF | yes |
| `fr-fr` | France | expedia.fr | fr_FR, EUR | yes |
| `nl-be` | Belgium | expedia.be | nl_BE, EUR | yes |
| `fr-be` | Belgium (French) | expedia.be | fr_BE, EUR | yes |
| `nl-nl` | Netherlands | expedia.nl | nl_NL, EUR | yes |
| `it-it` | Italy | expedia.it | it_IT, EUR | yes |
| `es-es` | Spain | expedia.es | es_ES, EUR | yes |
| `da-dk` | Denmark | expedia.dk | da_DK, DKK | yes |
| `sv-se` | Sweden | expedia.se | sv_SE, SEK | yes |
| `no-no` | Norway | expedia.no | nb_NO, NOK | yes |
| `fi-fi` | Finland | expedia.fi | fi_FI, EUR | yes |
| `es-mx` | Mexico | expedia.mx | es_MX, MXN | yes |
| `pt-br` | Brazil | expedia.com.br | pt_BR, BRL | held |
| `es-ar` | Argentina | expedia.com.ar | es_AR, ARS | yes |
| `es-cl` | Chile | expedia.com | es_MX, CLP | yes |
| `es-co` | Colombia | expedia.com | es_MX, COP | yes |
| `es-pe` | Peru | expedia.com | es_MX, PEN | yes |
| `es-cr` | Costa Rica | expedia.com | es_MX, USD | yes |
| `en-eg` | Egypt | expedia.com | en_US, EGP | yes |
| `ja-jp` | Japan | expedia.co.jp | ja_JP, JPY | yes |
| `en-jp` | Japan (English) | expedia.co.jp | en_US, JPY | yes |
| `ko-kr` | South Korea | expedia.co.kr | ko_KR, KRW | yes |
| `en-kr` | South Korea (English) | expedia.co.kr | en_US, KRW | yes |
| `zh-tw` | Taiwan | expedia.com.tw | zh_TW, TWD | yes |
| `zh-hk` | Hong Kong | expedia.com.hk | zh_HK, HKD | held |
| `en-hk` | Hong Kong (English) | expedia.com.hk | en_HK, HKD | held |
| `zh-hans-hk` | Hong Kong (Simplified Chinese) | expedia.com.hk | zh_CN, HKD | held |
| `en-sg` | Singapore | expedia.com.sg | en_SG, SGD | yes |
| `en-my` | Malaysia | expedia.com.my | en_MY, MYR | held |
| `en-ph` | Philippines | expedia.com.ph | en_PH, PHP | held |
| `id-id` | Indonesia | expedia.co.id | id_ID, IDR | yes |
| `en-id` | Indonesia (English) | expedia.co.id | en_GB, IDR | yes |
| `th-th` | Thailand | expedia.co.th | th_TH, THB | yes |
| `en-th` | Thailand (English) | expedia.co.th | en_GB, THB | yes |
| `vi-vn` | Vietnam | expedia.com.vn | vi_VN, VND | yes |
| `en-in` | India | expedia.co.in | en_GB, INR | yes |
| `en-ae` | United Arab Emirates | expedia.ae | en_US, AED | yes |
| `ar-ae` | United Arab Emirates (Arabic) | expedia.ae | ar_AE, AED | yes |
| `ar-sa` | Saudi Arabia | expedia.sa | ar_AE, SAR | yes |

Taiwan in English, Saudi Arabia in English and Expedia's Rest of Europe site are not offered (the site did not answer in that market's language or currency).

## Prices, deals and badges

| Field | Meaning |
|---|---|
| `price.amount`, `price.amount_display` | The card's large price, as Expedia shows it |
| `price.lead` | `nightly` or `total`: which figure the large price is (markets differ) |
| `price.nightly`, `price.nightly_display` | The nightly price ("$119 nightly", "215 € par nuit") |
| `price.total`, `price.total_display` | The stay total for the dates ("$558 total", "合計 ￥48,492") |
| `price.was`, `price.was_display`, `price.was_applies_to` | The struck-through price and whether it is a nightly or total figure |
| `price.fees_text` | Expedia's own line under the total ("Total with taxes and fees", "includes taxes & fees", "taxes et frais compris"); `null` where Expedia shows none |
| `price.stay_text`, `price.price_messages` | Expedia's stay line ("for 3 nights, Jan 25 - Jan 28") and every price line on the card |
| `deal` | Expedia's deal badge ("Black Friday $754 off", "-113 €") |
| `scarcity` | Expedia's scarcity text as shown ("We have 1 left at this price") |
| `badges`, `vip_access`, `member_price`, `sponsored` | Expedia's badges ("Ad", "Member Price available", "VIP Access") and the flags read from them |
| `rating` | {`score`, `score_display`, `label`, `review_count`, `review_count_text`}: Expedia's guest rating summary, out of 10 |

- **Member Price.** `member_price: true` means the card carries Expedia's "Member Price available" badge; the price shown is the price a visitor without an account sees.
- **Changes over time:** prices, deals and the calendar change as Expedia updates them. Any change you compute between two captures, label as computed with both `fetched_at` dates.

## Workflow

1. **The place.** `/suggestions` (`{"query": "new yo"}`) returns places with `region_id`; or send `destination` as you would type it on Expedia.
2. **Prices for the dates.** `/search` with `destination` or `region_id`, `check_in`, `check_out`, `adults`, and optionally `sort`, `star`, `amenity`, `guest_rating_min` and `market`. Check `partial`, `matched_total`, `applied` and the notes.
3. **One property.** `/property` with `id` (`properties[].property_id`) or `path` (`properties[].path`): fees, policies and amenities as Expedia writes them.
4. **Price by day.** `/price-calendar` with `path` from search (recommended) or `id`, plus `check_in` and `check_out` to open the page. Note `begin`, `end`, `days_with_price` and `label`.
5. **Report.** Each price with Expedia, the market, the currency, the dates, the guests, `fees_text` and the `fetched_at` date; say whether a figure is nightly or total; say when `partial` is true.
6. **Over time:** store each answer with its `fetched_at`; that stored set is your price record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `destination` | string | one of | A place as you would type it on Expedia (city, area, landmark or airport), 1-200 characters |
| `region_id` | string or integer | one of | Or an Expedia region id: `places[].region_id` of suggestions (`2621`) |
| `check_in` | string | required | Check-in date, `YYYY-MM-DD`, not in the past and within 500 days |
| `check_out` | string | required | Check-out date, `YYYY-MM-DD`, at most 28 nights after `check_in` |
| `adults` | integer | 2 | Adults in the room, 1-14. One room |
| `sort` | string | `recommended` | `recommended`, `price_asc`, `price_desc` or `review` (guest rating): Expedia's own sort options |
| `star` | integer | none | Expedia's star rating filter, 1-5 |
| `amenity` | string | none | One of Expedia's popular amenity filters: `POOL`, `PETS`, `WIFI`, `AIR_CONDITIONING`, `FREE_AIRPORT_TRANSPORTATION`, `HOT_TUB`, `SPA_ON_SITE`, `WASHER_DRYER`, `KITCHEN_KITCHENETTE`, `ELECTRIC_CAR`, `GYM`, `CRIB`, `FREE_PARKING`, `BALCONY_OR_TERRACE`, `RESTAURANT_IN_HOTEL` |
| `guest_rating_min` | integer | none | Expedia's guest rating filter: `7` (7+), `8` (8+) or `9` (9+) |
| `market` | string | `us` | One of the 51 market codes above, or a country code |

### Property (`/property`), price calendar (`/price-calendar`), suggestions (`/suggestions`)

| Endpoint | Parameters |
|---|---|
| `/property` | one of `id` (an Expedia property id, 2-12 digits: `properties[].property_id` of search, `17117062`) or `path` (`properties[].path` of search, `/New-York-Hotels-PUBLIC.h17117062.Hotel-Information`, or an Expedia hotel link); `market` (not `en-gb`, `pt-br`, `zh-hk`, `en-hk`, `zh-hans-hk`, `en-my`, `en-ph`) |
| `/price-calendar` | one of `id` or `path` (recommended: some market sites answer a page opened from the id alone without its calendar); `check_in` and `check_out` (`YYYY-MM-DD`, required: they open the page, the calendar spans Expedia's own window); `adults` 1-14 (default 2); `market` (not the 7 held markets) |
| `/suggestions` | `query` (or `text`), 2-100 characters: what a traveller has typed so far; `limit` 1-8 (default 8); `market` |

## Examples

### Prices for a place and dates

```bash
curl -X POST https://api.scavio.dev/api/v1/expedia/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"destination": "Las Vegas, NV", "check_in": "2027-01-25", "check_out": "2027-01-28", "adults": 2}'
```

Captured `data` (2026-11-26; `properties` cut to 2 of 3, `images` to 1 each, `price_messages` dropped, `notes` cut to 1 of 4):

```json
{
  "market": "us",
  "language": "en_US",
  "currency": "USD",
  "destination": "Las Vegas, NV",
  "region_id": "5456204",
  "destination_name": "Las Vegas, NV, United States of America (LAS-Harry Reid Intl.)",
  "check_in": "2027-01-25",
  "check_out": "2027-01-28",
  "nights": 3,
  "adults": 2,
  "rooms": 1,
  "sort": "recommended",
  "filters": {},
  "applied": {"sort": "RECOMMENDED"},
  "matched_total": 487,
  "results_heading": "487 Properties in Las Vegas, NV, United States of America (LAS-Harry Reid Intl.). January 25, 2027 through January 28, 2027",
  "count": 3,
  "partial": true,
  "properties": [
    {
      "position": 1,
      "property_id": "41080",
      "name": "New York-New York Hotel & Casino",
      "path": "/Las-Vegas-Hotels-New-York-New-York-Hotel-Casino.h41080.Hotel-Information",
      "neighborhood": "Las Vegas Strip",
      "messages": ["Las Vegas Strip"],
      "rating": {"score": 8.8, "score_display": "8.8", "label": "Excellent", "review_count": 15820, "review_count_text": "15,820 reviews"},
      "price": {"amount_display": "$558 total", "amount": 558, "lead": "total", "nightly": 119, "nightly_display": "$119 nightly", "total": 558, "total_display": "$558 total", "was": 796, "was_display": "$796", "was_applies_to": "total", "fees_text": "Total with taxes and fees", "stay_text": "for 3 nights, Jan 25 - Jan 28", "currency": "USD"},
      "deal": null,
      "scarcity": null,
      "badges": ["Ad", "Member Price available"],
      "vip_access": false,
      "member_price": true,
      "sponsored": true,
      "coordinates": {"latitude": 36.102863, "longitude": -115.17352},
      "images": ["https://mediaim.expedia.com/lodging/1000000/50000/41100/41080/c33c138e.jpg"]
    },
    {
      "position": 2,
      "property_id": "95163580",
      "name": "Fontainebleau Las Vegas, MICHELIN Key Award Hotel",
      "path": "/Las-Vegas-Hotels-Fontainebleau-Las-Vegas.h95163580.Hotel-Information",
      "neighborhood": "Las Vegas Strip",
      "messages": ["Las Vegas Strip"],
      "rating": {"score": 9.4, "score_display": "9.4", "label": "Exceptional", "review_count": 19396, "review_count_text": "19,396 reviews"},
      "price": {"amount_display": "$1,947 total", "amount": 1947, "lead": "total", "nightly": 517, "nightly_display": "$517 nightly", "total": 1947, "total_display": "$1,947 total", "was": 2701, "was_display": "$2,701", "was_applies_to": "total", "fees_text": "Total with taxes and fees", "stay_text": "for 3 nights, Jan 25 - Jan 28", "currency": "USD"},
      "deal": "Black Friday $754 off",
      "scarcity": null,
      "badges": ["Ad"],
      "vip_access": false,
      "member_price": false,
      "sponsored": true,
      "coordinates": {"latitude": 36.137645, "longitude": -115.160407},
      "images": ["https://mediaim.expedia.com/lodging/96000000/95170000/95163600/95163580/3e320266.jpg"]
    }
  ],
  "notes": [
    "Expedia's first page carried 3 properties on this request (partial: true; it carries up to 10 on some requests). Retry later for more of the first page."
  ]
}
```

### Another market

```bash
curl -X POST https://api.scavio.dev/api/v1/expedia/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"destination": "London, England", "check_in": "2027-01-25", "check_out": "2027-01-28", "adults": 2, "market": "en-gb"}'
```

Captured (2026-11-26): `currency` GBP, `region_id` 2114, `matched_total` 500, `count` 3, `partial` true. Bedford Hotel: `amount_display` "£398", `lead` "total", `nightly_display` "£133 per night", `fees_text` "includes taxes & fees", `stay_text` "for 3 nights, 25 Jan - 28 Jan"; Strand Palace Hotel "£607" (£202 per night); Park Plaza London Westminster Bridge "£728" (£243 per night).

### One property

```bash
curl -X POST https://api.scavio.dev/api/v1/expedia/property \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "17117062"}'
```

Captured `data` (2026-11-26; `description` and texts shortened; `amenities` cut to 2 of 14 groups, `fees` to 3 of 8, `policies` to 1 of 7, `nearby` to 1 of 3 groups and 2 places, `faqs` to 1 of 5, `photos` to 1 of 49; `about`, `guest_liked`, `important_information`, `neighborhood_text` and `notes` dropped):

```json
{
  "market": "us",
  "language": "en_US",
  "currency": "USD",
  "property_id": "17117062",
  "requested_id": "17117062",
  "name": "PUBLIC, an Ian Schrager hotel",
  "path": "/New-York-Hotels-PUBLIC.h17117062.Hotel-Information",
  "stars": 4,
  "featured": [],
  "address": {"street": "215 Chrystie St", "locality": "New York", "region": "NY", "postal_code": "10002", "country": "USA"},
  "coordinates": {"latitude": 40.723087, "longitude": -73.992066},
  "region_id": "2621",
  "rating": {"score": 8.8, "score_display": "8.8", "best": 10, "label": "Excellent", "review_count": 4116, "review_count_text": "See all 4,116 reviews"},
  "description": "Near New York University and Washington Square Park, PUBLIC, an Ian Schrager hotel provides a nightclub, a rooftop terrace, and ...",
  "amenities": [
    {"group": "Popular amenities", "items": ["Pet friendly", "Restaurant", "Air conditioning"]},
    {"group": "Parking and transportation", "items": ["Covered self parking on site (USD 40 per night)"]}
  ],
  "fees": [
    "Deposit: USD 200.00 per accommodation, per stay",
    "Resort fee: USD 51.64 per accommodation, per night",
    "Pet fee: USD 100 per accommodation, per stay"
  ],
  "policies": [
    {"kind": null, "heading": "Check-in", "texts": ["Check-in start time: 3:00 PM; Check-in end time: 3:00 AM", "Early check-in subject to availability"]}
  ],
  "nearby": [
    {"group": "What's nearby", "places": [{"name": "New Museum", "distance": "0.1 miles", "travel_time": "2 min walk"}, {"name": "Bowery Ballroom", "distance": "0.3 miles", "travel_time": "5 min walk"}]}
  ],
  "faqs": [
    {"question": "How much is parking?", "answer": "Self parking is available for USD 40 per night."}
  ],
  "photo_count": 49,
  "photos": [
    {"url": "https://images.trvl-media.com/lodging/18000000/17120000/17117100/17117062/33210c6e.jpg", "caption": "A rooftop terrace with a city skyline view at sunset, ..."}
  ]
}
```

`guest_liked` are Expedia's own summary lines ("What guests liked about the gym": "The hotel's gym is well-equipped and excellent."), not review texts. In `ja-jp` the same property came back as "パブリック イアン シュレーガー ホテル" in JPY.

### Price calendar

```bash
curl -X POST https://api.scavio.dev/api/v1/expedia/price-calendar \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "17117062", "check_in": "2027-01-25", "check_out": "2027-01-28"}'
```

Captured `data` (2026-11-26; `days` cut to 3 of 256, `notes` dropped):

```json
{
  "market": "us",
  "language": "en_US",
  "currency": "USD",
  "property_id": "17117062",
  "name": "PUBLIC, an Ian Schrager hotel",
  "check_in": "2027-01-25",
  "check_out": "2027-01-28",
  "adults": 2,
  "label": "Lowest prices in the past 24 hours",
  "label_en": "Lowest prices in the past 24 hours",
  "begin": "2026-11-26",
  "end": "2027-08-08",
  "count": 256,
  "days_with_price": 247,
  "days": [
    {"date": "2026-11-26", "price": 392, "price_display": "$392"},
    {"date": "2026-11-27", "price": null, "price_display": null},
    {"date": "2026-11-28", "price": 420, "price_display": "$420"}
  ]
}
```

Across the 247 priced days the calendar ran from $252 (2027-01-03) to $1,043 (2026-12-02). Other captures: Hotel de Roubaix, Paris (`fr-fr`, "Notre prix le plus bas au cours des dernières 24 heures") 142 € to 272 € over 287 priced days; ザ ノット 東京新宿 (`ja-jp`) ￥10,044 to ￥63,287 over 258 priced days, taxes and service charges not included per Expedia's label.

### Destination suggestions

`/suggestions` with `{"query": "new yo"}` returned 8 places: Manhattan (`NEIGHBORHOOD`, `region_id` 129440), New York, NY (NYC-All Airports) (`METROCODE`, 6139058), Times Square (`POI`, 502080) ..., each with `display_name`, `full_name`, coordinates, `country_code` and `airport_code`.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def expedia(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/expedia/{endpoint}", headers=HEADERS, json=body, timeout=250)
    r.raise_for_status()
    return r.json()

# The region id for a place (2 credits)
places = expedia("suggestions", {"query": "new yo"})["data"]["places"]
region = places[0]["region_id"]

# Prices for the dates (2 credits)
res = expedia("search", {"region_id": region, "check_in": "2027-01-25", "check_out": "2027-01-28", "adults": 2, "sort": "price_asc"})
s = res["data"]
print(s["destination_name"], s["matched_total"], "partial" if s["partial"] else "", res["credits_used"], "credits")
for p in s["properties"]:
    pr = p["price"] or {}
    print(p["property_id"], pr.get("nightly_display"), pr.get("total_display"), pr.get("fees_text"), "ad" if p["sponsored"] else "")

# Expedia's price per day for the first property (2 credits)
first = s["properties"][0]
cal = expedia("price-calendar", {"path": first["path"], "check_in": "2027-01-25", "check_out": "2027-01-28"})["data"]
print(cal["label"], cal["begin"], cal["end"], cal["days_with_price"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `market`, `language`, `currency` and `notes`.

- **search** - `market`, `language`, `currency`, `destination`, `region_id`, `destination_name`, `check_in`, `check_out`, `nights`, `adults`, `rooms`, `sort`, `filters` (as sent), `applied` (the selections Expedia's page echoed), `matched_total`, `results_heading`, `count`, `partial`, `properties[]`, `notes`.
- **property card** (search) - `position`, `property_id`, `name`, `path`, `neighborhood`, `messages`, `rating` {`score`, `score_display`, `label`, `review_count`, `review_count_text`}, `price` {`amount`, `amount_display`, `lead`, `nightly`, `nightly_display`, `total`, `total_display`, `was`, `was_display`, `was_applies_to`, `fees_text`, `stay_text`, `price_messages`, `currency`} or `null`, `deal`, `scarcity`, `badges`, `vip_access`, `member_price`, `sponsored`, `coordinates` {`latitude`, `longitude`} or `null`, `images`.
- **property** - `market`, `language`, `currency`, `property_id`, `requested_id`, `name`, `path`, `stars`, `featured`, `address` {`street`, `locality`, `region`, `postal_code`, `country`}, `coordinates`, `region_id`, `rating` {`score`, `score_display`, `best`, `label`, `review_count`, `review_count_text`} or `null`, `description`, `about[]` {`kind`, `heading`, `texts`}, `amenities[]` {`group`, `items`}, `guest_liked[]` {`heading`, `text`}, `fees[]`, `policies[]` {`kind`, `heading`, `texts`}, `important_information[]` {`kind`, `heading`, `texts`}, `neighborhood_text`, `nearby[]` {`group`, `places[]` {`name`, `distance`, `travel_time`}}, `faqs[]` {`question`, `answer`}, `photo_count`, `photos[]` {`url`, `caption`}, `notes`.
- **price calendar** - `market`, `language`, `currency`, `property_id`, `name`, `check_in`, `check_out`, `adults`, `label`, `label_en`, `begin`, `end`, `count`, `days_with_price`, `days[]` {`date`, `price`, `price_display`}, `notes`.
- **suggestions** - `market`, `language`, `currency`, `query`, `count`, `places[]` {`type` (CITY, NEIGHBORHOOD, POI, AIRPORT, METROCODE ...), `region_id`, `name`, `display_name`, `full_name`, `primary_name`, `secondary_name`, `latitude`, `longitude`, `country`, `country_code`, `airport_code`}, `notes`.

## Guardrails

- Name it "Expedia (expedia.com, Expedia Group's travel booking site)" on first mention, "Expedia" after that.
- Prices: quote each with the currency, the dates and nights, the guests, the market, `fees_text` as Expedia wrote it and the `fetched_at` date ("$558 total for 3 nights, Jan 25-28, 2027, 2 adults, total with taxes and fees, on expedia.com on Nov 26, 2026"). Say whether a figure is nightly or total. A price calendar figure is "the price Expedia's calendar showed for that day, labelled lowest prices in the past 24 hours", never a quote for the user's stay.
- Partial answers: when `partial` is true, say that Expedia's first page carried 3 properties on that request, not the whole result set.
- Sponsored cards: name them as Expedia's paid placements, in their position; do not drop or reorder them silently.
- Fees: quote fee, deposit and resort fee lines exactly as Expedia writes them, with the property and date.
- Comparisons: the same hotel, dates and guests, the market and currency beside every number, named site and date. Convert currencies only when asked, and label the result computed with the rate used. No verdict on which hotel is better value beyond the numbers shown.
- Descriptive only: no commentary on Expedia's business, fees, ranking, pricing practices or policies.
- Do not republish Expedia photos or descriptions. Write expedia.com as plain text and cite property ids, region ids and capture dates rather than linking Expedia pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no booking flow. Expedia's terms of use cover how its site and content may be used, including automated access; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, ratings, property ids, fees or policies. Return what the API returned, with the `fetched_at` time.
- Not available: review texts, rooms and rates on a property, results past Expedia's first page, flights, cars, packages, activities, booking, member-only prices, and hotel pages in the 7 held markets.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `destination` or `region_id` ("Send destination (a place name) or region_id (places[].region_id of suggestions)."); a date that is not `YYYY-MM-DD` ("check_in must be a date as YYYY-MM-DD.") or not a real date; "check_in must not be in the past."; "check_in must be within 500 days from today."; "check_out must be after check_in."; "A stay can be at most 28 nights."; a `sort` or `amenity` outside its list ("sort must be one of recommended, price_asc, price_desc, review."); `adults`, `star`, `guest_rating_min` or `limit` outside its range; a `region_id` that is not digits; a `market` outside the 51 codes ("market must be one of us, es-us, ... (or a country code such as gb, de, jp). Taiwan in English, Saudi Arabia in English and Expedia's Rest of Europe site are not offered ..."); `/property` or `/price-calendar` in a held market ("property is not available for market en-gb (United Kingdom): Expedia answers hotel pages there with another country's site. Search and suggestions work in this market; hotel pages are held in en-gb, pt-br, zh-hk, en-hk, zh-hans-hk, en-my, en-ph."); without exactly one of `id` or `path` ("Send one of id (properties[].property_id of search) or path (properties[].path of search, or an Expedia hotel link)."), an id that is not digits ("id must be an Expedia property id as search returns it (digits, e.g. 17117062).") or a path that is not a hotel page ("path is not an Expedia hotel page (expected /<name>.h<id>.Hotel-Information)."); suggestions under 2 characters ("query must be at least 2 characters.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits, or below what the call can hold (6 credits, suggestions 4). The body carries `billing_url`.
- `404` means not found, and it is charged at what it cost (2 credits in the captures): "Expedia has no property ...". Take property ids and paths from a search answer and region ids from suggestions rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api).
- `502` means Expedia data was temporarily unavailable ("Expedia is temporarily unavailable. Please try again.") or Expedia answered with another country's site on every attempt ("Expedia answered with another country's site on every attempt. Please try again; this was not charged."). It is not charged, so retry after a few seconds. On `/price-calendar`, send `path` rather than `id` if it repeats.
- `503` with a `Retry-After` header means the service is busy ("Expedia is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: places } = await scavio.expedia.suggestions({ query: "new yo" });
const { data: hotels } = await scavio.expedia.search({ destination: "Las Vegas, NV", check_in: "2027-01-25", check_out: "2027-01-28", adults: 2 });
const { data: gb } = await scavio.expedia.search({ destination: "London, England", check_in: "2027-01-25", check_out: "2027-01-28", market: "en-gb" });
const { data: property } = await scavio.expedia.property({ id: "17117062" });
const { data: calendar } = await scavio.expedia.priceCalendar({ id: "17117062", check_in: "2027-01-25", check_out: "2027-01-28" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.expedia.search(...)`, `property`, `price_calendar` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 4 endpoints as tools: `search_expedia`, `get_expedia_property`, `get_expedia_price_calendar` and `get_expedia_suggestions`. Expedia is opt-in: add `expedia` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,expedia"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/expedia-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api), [property](https://scavio.dev/docs/expedia-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api), [price calendar](https://scavio.dev/docs/expedia-price-calendar?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api), [suggestions](https://scavio.dev/docs/expedia-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api). Overview: [Expedia API](https://scavio.dev/expedia-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=expedia-api).
