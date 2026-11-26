---
name: vrbo-api
description: Vrbo API for Vrbo (vrbo.com, Expedia Group's vacation rental site, 20 vrbo.com market-languages) - what a stay costs on Vrbo for your dates and guests, as Vrbo shows it (Destin, Florida for Jan 15-18, 2027 with 2 adults matched 395 rentals, and the first 50 ran from $81 to $457 a night and $243 to $1,371 for the 3 nights, all fees included) with the nightly price, the stay total, the strike-through price, Vrbo's fee line and deal text; vacation-rental search by place name or region id, check-in and check-out (up to 90 nights), adults and children's ages, 5 sorts and Vrbo's filters (property type, amenity, house rule incl. pets, location type, Premier Host, minimum bedrooms), the first 50 results of a search, each with its rating and review count, badges, sponsored flag, coordinates and images; one property in full by id or link, without dates, with its location, rating, highlights, bedrooms, bathrooms and sleeps, every amenity group, house rules, important information, description, the Premier Host badge and the host's languages (no host name), photos, nearby places and the site's default-stay price; destination suggestions with the region ids search takes. 3 endpoints, 2 credits per attempt Vrbo needs (search 2 to 8, property and suggestions 2). 20 market-languages, each in its own language and currency. No reviews, availability calendar, dated price on a property or results past the first 50.
version: 1.0.0
tags: vrbo, vrbo-com, vrbo-api, vrbo-prices, vrbo-search, vrbo-property, vrbo-listings, vrbo-rentals, vrbo-vacation-rentals, vrbo-nightly-rates, vrbo-amenities, vrbo-house-rules, vrbo-premier-host, vrbo-deals, vrbo-suggestions, expedia-group, vacation-rentals, vacation-rental-prices, holiday-rentals, short-term-rentals, cabin-rentals, beach-rentals, pet-friendly-rentals, nightly-rates, stay-total, travel, travel-data, lodging, accommodation, rate-shopping, multi-currency, price-monitoring, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/vrbo-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api
---

# Vrbo API - Vacation Rental Prices, Property Details, Destination Search

Read Vrbo (vrbo.com, Expedia Group's vacation rental site): vacation-rental search for a place, dates and guests with Vrbo's sorts and filters, one property in full, and Vrbo's destination suggestions. Every answer is what Vrbo's public pages show a visitor without an account at the moment of the call, in the market's language and currency (20 vrbo.com market-languages). All 3 endpoints return structured JSON, billed at 2 credits per attempt Vrbo needs.

**Read-only data.** This skill reads the public pages Vrbo shows to any visitor and returns them as JSON for analysis. It uses no Vrbo account, no trip board, no booking, no message to a host and no payment step.

**The job this skill is for: what a stay costs on Vrbo for given dates and guests, across the rentals Vrbo lists first for a place.** `/search` returns, for each of the first 50 properties, the price Vrbo shows for those exact dates: the nightly price, the stay total and Vrbo's own fee line, in the market's currency. Captured 2026-11-26:

| Search (market) | Dates, guests | `matched_total` | First 50: nightly / stay total | One property (`price`) |
|---|---|---|---|---|
| Destin, Florida (`us`) | Jan 15-18, 2027 (3 nights), 2 adults | 395 | $81-$457 / $243-$1,371, "All fees included" | 1046285, condo, 1 bedroom: $203 a night, "$610 for 3 nights", rating 9.8 (221 reviews), Premier Host |
| Gatlinburg cabins, pets allowed, `price_low` (`us`, region 7474) | Feb 12-15, 2027, 4 adults, children 5 and 7 | 355 | $166-$348 / $498-$1,044 | 5052281, cabin: $166 a night (was $177), "$498 for 3 nights", "Early booking $34 off" |
| Cornwall, England (`en-gb`) | May 14-17, 2027, 2 adults | 375 | £70-£642 / £210-£1,925, "includes taxes & fees" | 11546610, cottage: "£548 for 3 nights, 1 cottage" (£183 per night) |
| Okinawa (`ja-jp`) | May 14-17, 2027, 2 adults, child 4 | 66 | ￥9,130-￥79,636 / ￥33,144-￥262,800 | pdp/lo/9848668, apartment: ￥18,048 a night (was ￥25,782), "合計 ￥59,558", "￥23,203 OFF" |

The stay total is Vrbo's figure, not the nightly price times the nights (Destin: $203 a night, $610 for 3 nights). Quote both with the dates, the guests, the market and the fee line as Vrbo wrote it. For the same place on other sites use `booking-com-hotel-data` or `google-hotels-api`, matched on dates and guests; for guest reviews, which this skill does not return, `tripadvisor-reviews-api`.

Nine limits shape every answer, so say them plainly:
- **2 credits per attempt Vrbo needs.** Vrbo serves its results page in two forms, a full one with 50 properties or a short one with 3. When the short one comes back, Scavio asks again, up to 4 attempts in all, and bills 2 credits for each attempt in the right market: a search costs 2 to 8 credits (2 to 6 in most captures), and needs 8 credits of balance to start. A property or suggestions call costs 2. An attempt that fails or answers for another market is not billed. `credits_used` in every answer says what was spent. A not-found property (`404`) is charged 2; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **`partial: true` means 3 properties, not 50.** If all 4 attempts return the short page, the 3 properties it shows come back with `partial: true` and `attempts: 4` (8 credits); retry later for the full page. Say so whenever `partial` is true.
- **The first 50 only.** Vrbo's results pages carry their first 50 properties and no further page: `matched_total` is Vrbo's count of matches (395), `page_label` its own wording ("1 - 50 of 300+"). Narrow with `sort` and the filters rather than paging.
- **Prices are for the dates asked, as Vrbo shows them.** `price.lead` says which figure is the card's large price: in the US market the nightly price ("$203", "per night, Jan 15 - Jan 18"), in `en-gb` the stay total ("£548 for 3 nights, 1 cottage"). `fees_text` is Vrbo's own fee line ("All fees included", "includes taxes & fees"). `was` and `was_applies_to` are the strike-through price and what it is a price of.
- **Sponsored cards stay in place.** `sponsored: true` marks Vrbo's paid placements (its "Ad" badge; 12 of the first 50 in Destin). Report them as Vrbo's ads, in their position.
- **A property is fetched without dates.** `/property` returns the listing in full but no price for your dates: `default_price` is the site's own default stay, labelled "the site's own default stay, not a quote" (1046285: $176 "avg per night", lines "$352 for 2 nights", "Dec 9 - Dec 11"), and `null` when the page shows none. Read dated prices from `/search`.
- **Host details stop at the badge.** `host` is the Premier Host badge, its text and the host's languages (`null` when the page has no host section). No host name, biography, photo or contact is returned.
- **Language and currency follow the market.** Labels, amenities and rules come in the market's language (`ja-jp`: "最高に素晴らしい"); host-written titles and descriptions can stay in the host's language. Field names are English.
- **What is not there.** No reviews (the rating and review count only), no availability calendar, no price for chosen dates on a property, no results past the first 50, no booking. abritel.fr, fewo-direkt.de, stayz.com.au and bookabach.co.nz are separate Expedia Group sites and are not covered.

Vrbo's own API access is Expedia Group's partner program (listings, bookings and reviews for approved partners), not a self-serve API. This skill reads Vrbo's public pages with one Scavio key.

See also: `booking-com-hotel-data` and `google-hotels-api` (hotel and apartment prices for the same dates), and `tripadvisor-reviews-api` (guest reviews). Same place, same dates and guests: name the site, market, currency and capture date with every price.

## When to trigger

Use this skill when the user asks to:
- Find Vrbo vacation rentals in a place for specific dates and guests, with the nightly price, the stay total and Vrbo's fee line
- Sort Vrbo results by price, guest rating or review count, or filter by property type (house, cabin, condo ...), an amenity (pool, hot tub ...), pets allowed, a location type (oceanfront, lake, ski-in/ski-out ...), Premier Host or a minimum number of bedrooms
- Compare what a stay costs on Vrbo across markets and currencies (US, UK, Canada in English or French, Mexico, Brazil, Spain, Italy, Japan, Australia ...)
- Read one Vrbo property in full: location, rating, bedrooms, bathrooms and sleeps, every amenity, house rules (check-in and check-out, minimum age, children, pets, events, smoking), important information, description, photos and what is nearby
- Look up Vrbo's destination suggestions and region ids for a place name

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Calls in this skill cost 2 credits per attempt Vrbo needs: property and suggestions 2, a search 2 to 8. So 50 credits cover, for example, 6 destinations: one suggestions call (2 credits) and one search (2 to 6 credits, as most captured searches billed) each.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, suggestions answered in 1.5-2.4 seconds, property in 3.5-7.1 (up to 25 in the first measurements) and search in 6-28 (each attempt 3.7 to 43 seconds; a search can take up to about 3 minutes). Set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/vrbo/search` | The first 50 vacation rentals for a place, dates and guests, with Vrbo's sorts and filters: nightly price, stay total, strike-through price, fee line, deal, rating, badges, sponsored flag, coordinates, images; `matched_total`, `page_label`, `partial`, `attempts` | 2 per attempt (2-8) |
| `POST /api/v1/vrbo/property` | One property by id or link, without dates: location, rating, highlights, space, amenities, house rules, important information, description, host badge and languages, photos, nearby places, the site's default-stay price | 2 |
| `POST /api/v1/vrbo/suggestions` | Destination suggestions for a partial place name: type, region id, names, coordinates, country | 2 |

## Market

20 vrbo.com market-languages, chosen with `market` (default `us`); each answers in its own language and currency:

| `market` | Language, currency | `market` | Language, currency |
|---|---|---|---|
| `us` | English, USD | `de-at` | German, EUR |
| `en-gb` | English, GBP | `el-gr` | Greek, EUR |
| `en-ca` | English, CAD | `fi-fi` | Finnish, EUR |
| `fr-ca` | French, CAD | `da-dk` | Danish, DKK |
| `es-mx` | Spanish, MXN | `sv-se` | Swedish, SEK |
| `pt-br` | Portuguese, BRL | `no-no` | Norwegian, NOK |
| `es-es` | Spanish, EUR | `ja-jp` | Japanese, JPY |
| `it-it` | Italian, EUR | `en-sg` | English, SGD |
| `pt-pt` | Portuguese, EUR | `en-au` | English, AUD |
| `nl-nl` | Dutch, EUR | `en-nz` | English, NZD |

The market sets the language, currency and price wording, not where the rental is: a `fr-ca` search for Lake Tahoe lists US rentals, in French and priced in CAD. Every answer carries `market`, `language` and `currency`. A property link keeps its own market unless `market` is sent.

## Prices, deals and badges

| Field | Meaning |
|---|---|
| `price.nightly`, `price.nightly_display` | The nightly price for the dates as Vrbo shows it (`203`, `"$203"`; `"£183 per night"`) |
| `price.total`, `price.total_display` | The stay total as Vrbo states it (`610`, `"$610 for 3 nights"`; `"5 148 $ CA au total"`) |
| `price.lead` | `nightly` or `total`: which one is the card's large price (markets differ) |
| `price.was`, `price.was_display`, `price.was_applies_to` | The strike-through price and whether it is a nightly or a total price (`177`, `"$177"`, `nightly`) |
| `price.stay_text` | Vrbo's line beside the price (`"per night, Jan 15 - Jan 18"`, `"for 3 nights, 14 May - 17 May"`) |
| `price.fees_text` | Vrbo's own fee line (`"All fees included"`, `"includes taxes & fees"`, `"Le total comprend les taxes et les frais"`) |
| `price.price_messages` | Every line under the price, as shown |
| `deal` | Vrbo's deal text (`"Early booking $34 off"`, `"Réservation hâtive : -369 $ CA"`, `"￥23,203 OFF"`) or `null` |
| `badges` | Vrbo's badges as written (`Premier Host`, `Ad`, `Loved by Guests`, `Annonce`, `Hôte de choix`) |
| `sponsored` | `true` for Vrbo's paid placements, kept in their position |
| `messages`, `details` | The type / bedrooms / beds line as shown, split in `details`, and the other lines (e.g. "Fully refundable until Dec 16") |
| `rating` | {`score` (out of 10), `score_display`, `label` ("Exceptional"), `review_count`, `review_count_text`, `external_reviews`} |
| `default_price` (property) | The site's own default stay {`label`, `price`, `price_display`, `qualifier`, `messages`, `site_note`, `currency`}: never a quote for the user's dates |

- **Per night from a total:** if you divide `price.total` by `nights`, label it computed (610 / 3 = 203.33, computed); Vrbo's own nightly figure is `price.nightly`.
- **Property ids:** `property_id` is the input of `/property` and has three forms, all as search returns them: `1046285`, `3695349vb` and `pdp/lo/9848668`. `expedia_property_id` is a second id Vrbo carries; it is not an input.
- **Region ids:** `places[].region_id` from `/suggestions` (`6906` for Destin) is the exact input of `/search`; a typed `destination` can resolve to a nearby place (Okinawa resolved to "OKINAWAフルーツらんど, 名護市"), so read `destination_name` back.

## Workflow

1. **Place.** `/suggestions` with `query` (and `market`) for the region ids Vrbo uses: a city, neighbourhood, landmark or airport.
2. **Prices for the dates.** `/search` with `region_id` (or `destination`), `check_in`, `check_out`, `adults`, `children` and any sort or filter. Check `partial`, `applied` (the filters and sort Vrbo's page echoed) and `applied_guests`; note `matched_total`.
3. **One property.** `/property` with a `property_id` from the search, in the same `market`, for its space, amenities, house rules, important information and photos.
4. **Report.** Each price with the dates, nights, guests, market, currency, `fees_text` and the `fetched_at` date; sponsored cards marked as Vrbo's ads; `partial` stated when true; no verdict.
5. **Price series:** there is no price history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `destination` | string | none | A place as you would type it on Vrbo (`Destin, Florida`, `Cornwall, England`), 1-200 characters. Send this or `region_id` |
| `region_id` | string or integer | none | A Vrbo region id: `places[].region_id` of `/suggestions` (digits only, e.g. `6906`) |
| `check_in` | string | required | Check-in date, `YYYY-MM-DD`; not in the past, within 500 days from today |
| `check_out` | string | required | Check-out date, `YYYY-MM-DD`; after `check_in`, at most 90 nights later |
| `adults` | integer | 2 | Adults, 1-30 |
| `children` | list of integers | none | Children's ages, one per child (0-17), at most 10 (`[5, 7]`) |
| `sort` | string | `recommended` | `recommended`, `price_low`, `price_high`, `review` (guest rating), `review_count` |
| `property_type` | string | none | `house`, `apartment_or_condo`, `cottage`, `cabin`, `estate`, `resort`, `villa`, `hotel`, `houseboat`, `guest_house`, `boat`, `chalet`, `RV` |
| `amenity` | string | none | One of `pool`, `private_pool`, `heated_pool`, `hot_tub`, `balcony`, `king_sized_bed`, `parking`, `internet_available`, `fireplace`, `washer`, `clothes_dryer`, `electric_vehicle_charging_station`, `air_conditioning`, `television`, `outdoor_grill`, `patio_or_deck`, `garden_or_backyard`, `bed_linens_provided`, `crib`, `stove`, `microwave`, `oven`, `dishwasher`, `kids_high_chair`, `iron_and_board` |
| `house_rule` | string | none | One of `pets_allowed`, `pet_free`, `children_allowed`, `events_allowed`, `smoking_allowed` |
| `pets_allowed` | boolean | false | Pet-friendly places only (the same as `house_rule` `pets_allowed`; send one of the two) |
| `location_type` | string | none | One of `oceanfront`, `waterfront`, `downtown_location`, `lake_location`, `mountains_location`, `rural_location`, `golf_course`, `village_location`, `skiin_skiout` |
| `premier_host` | boolean | false | Places run by Premier Hosts only |
| `bedrooms_min` | integer | none | This many bedrooms or more, 1-10 (Vrbo may still mix in sponsored places) |
| `market` | string | `us` | One of the 20 market codes above |

One value per filter group. A filter Vrbo's page did not echo as applied is named in `notes`.

### Property (`/property`) and suggestions (`/suggestions`)

| Endpoint | Parameters |
|---|---|
| `/property` | one of `id` (a `property_id` from search: `1046285`, `12245744ha`, `pdp/lo/30792130`) or `url` (a vrbo.com property link, any market; the link's market is used unless `market` is sent); `market` |
| `/suggestions` | `query` (2-100 characters, what a traveller has typed so far); `limit` 1-8 (default 8); `market` |

## Examples

### Prices for a place and dates

```bash
curl -X POST https://api.scavio.dev/api/v1/vrbo/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"destination": "Destin, Florida", "check_in": "2027-01-15", "check_out": "2027-01-18", "adults": 2}'
```

Captured `data` (2026-11-26; `properties` cut to 2 of 50, `images`, `url` and `path` dropped, `notes` cut to 1 of 3):

```json
{
  "market": "us",
  "language": "en_US",
  "currency": "USD",
  "destination": "Destin, Florida",
  "region_id": "6906",
  "destination_name": "Destin, Florida, United States of America",
  "check_in": "2027-01-15",
  "check_out": "2027-01-18",
  "nights": 3,
  "adults": 2,
  "children": [],
  "sort": "recommended",
  "filters": {},
  "applied": {"sort": "RECOMMENDED"},
  "matched_total": 395,
  "page_label": "1 - 50 of 300+",
  "count": 50,
  "partial": false,
  "attempts": 2,
  "properties": [
    {"position": 1, "property_id": "2957152", "expedia_property_id": "83704063", "title": "Pelican Retreat by AvantStay | 5 MINS TO BEACH | Pet Friendly w/ Pool & BBQ!", "details": ["House", "3 bedrooms", "6 beds"], "messages": ["House · 3 bedrooms · 6 beds"], "location_messages": ["5 min walk to the beach"], "rating": {"score": 9.2, "score_display": "9.2", "label": "Wonderful", "review_count": 57, "review_count_text": "57 reviews", "external_reviews": false}, "price": {"nightly": 457, "nightly_display": "$457", "total": 1371, "total_display": "$1,371 for 3 nights", "was": null, "was_display": null, "was_applies_to": null, "lead": "nightly", "stay_text": "per night, Jan 15 - Jan 18", "fees_text": "All fees included", "price_messages": ["$1,371 for 3 nights", "All fees included"], "currency": "USD"}, "deal": null, "badges": ["Ad"], "sponsored": true, "coordinates": {"latitude": 30.381576, "longitude": -86.420167}},
    {"position": 3, "property_id": "1046285", "expedia_property_id": "18979234", "title": "Upgraded 5th Flr Pelican Beach Resort -1 bedroom - On the beach-", "details": ["Condo", "1 bedroom", "4 beds"], "messages": ["Condo · 1 bedroom · 4 beds"], "location_messages": ["On the beach"], "rating": {"score": 9.8, "score_display": "9.8", "label": "Exceptional", "review_count": 221, "review_count_text": "221 reviews", "external_reviews": false}, "price": {"nightly": 203, "nightly_display": "$203", "total": 610, "total_display": "$610 for 3 nights", "was": null, "was_display": null, "was_applies_to": null, "lead": "nightly", "stay_text": "per night, Jan 15 - Jan 18", "fees_text": "All fees included", "price_messages": ["$610 for 3 nights", "All fees included"], "currency": "USD"}, "deal": null, "badges": ["Premier Host"], "sponsored": false, "coordinates": {"latitude": 30.3844, "longitude": -86.474692}}
  ],
  "notes": ["Vrbo's results pages carry their first 50 properties only (no further page can be fetched): narrow with sort and filters."]
}
```

This search took 2 attempts (4 credits). Across the 50 cards the nightly price ran from $81 to $457 and the stay total from $243 to $1,371; 12 cards were sponsored. Newer answers also carry `applied_guests` ({"adults": 2, "children": []}): the guests Vrbo's page searched for.

### Filters, children and a sort

```bash
curl -X POST https://api.scavio.dev/api/v1/vrbo/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"region_id": "7474", "check_in": "2027-02-12", "check_out": "2027-02-15", "adults": 4, "children": [5, 7], "property_type": "cabin", "pets_allowed": true, "sort": "price_low"}'
```

Captured (2026-11-26, 1 attempt, 2 credits): `destination_name` "Gatlinburg, Tennessee, United States of America", `filters` {"property_type_group": "cabin", "house_rules_group": "pets_allowed"} and `applied` the same plus `"sort": "PRICE_LOW_TO_HIGH"`, `matched_total` 355, 50 cards. The first: 5052281, `details` ["1 bedroom", "3 beds", "Game room", "Outdoor pool", "Dog-friendly"], rating 10 (12 reviews), `price` {"nightly": 166, "total": 498, "total_display": "$498 for 3 nights", "was": 177, "was_applies_to": "nightly", "fees_text": "All fees included"}, `deal` "Early booking $34 off", `badges` ["Premier Host"].

A search of the same region for Feb 19-21 with children 5 and 7 got Vrbo's short page on all 4 attempts: `count` 3, `partial` true, `attempts` 4, 8 credits, and the note "Vrbo answered with its short 3-card page on all 4 attempts: these are its first 3 results (partial). Retry later for the 50-card page."

### Another market

`{"destination": "Cornwall, England", "check_in": "2027-05-14", "check_out": "2027-05-17", "adults": 2, "market": "en-gb"}` (2 attempts, 4 credits): `currency` GBP, `matched_total` 375, the total as the lead price: `price` {"nightly": 183, "nightly_display": "£183 per night", "total": 548, "total_display": "£548 for 3 nights, 1 cottage", "lead": "total", "stay_text": "for 3 nights, 14 May - 17 May", "fees_text": "includes taxes & fees"}. With `market: "fr-ca"`, `amenity: "hot_tub"` and `bedrooms_min: 3`, Lake Tahoe listed 352 matches in CAD ("1 108 $ CA" a night, "5 148 $ CA au total", `deal` "Réservation hâtive : -369 $ CA").

### One property

```bash
curl -X POST https://api.scavio.dev/api/v1/vrbo/property \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id": "1046285"}'
```

Captured `data` (2026-11-26, 2 credits; `highlights` cut to 1 of 2, `amenities` to 1 of 15 groups and that group to 8 of 21 items, `house_rules` to 5 of 9, `nearby` to 1 of 3 groups and that group to 3 of 5 places; `important_information`, `photos` (66), `description`, `breadcrumbs`, `url` and `notes` dropped):

```json
{
  "market": "us",
  "language": "en_US",
  "currency": "USD",
  "requested_id": "1046285",
  "property_id": "1046285",
  "expedia_property_id": "18979234",
  "title": "Upgraded 5th Flr Pelican Beach Resort -1 bedroom - On the beach-",
  "property_type": "Condo",
  "location": {"locality": "Destin", "region": "FL", "country": "USA", "address_lines": ["Destin", "FL"], "latitude": 30.3844, "longitude": -86.474692, "region_id": "6906"},
  "rating": {"score": 9.8, "score_display": "9.8", "best": 10, "label": "Exceptional", "review_count": 221, "review_count_text": "See all 221 reviews"},
  "highlights": [{"title": "Beach, waves and sand", "text": "Guests enjoy the stunning beach views at this property."}],
  "space": {"bedrooms": 1, "bathrooms": 2, "sleeps": 6, "texts": ["1 bedroom", "2 bathrooms", "Sleeps 6"]},
  "amenities": [{"group": "Popular amenities", "items": ["On beach", "Hot tub on site", "Porch or lanai", "Private pool", "Waterpark access", "On-site fitness center", "Barbecue grill", "Free WiFi"]}],
  "house_rules": [
    {"kind": null, "heading": null, "texts": ["Check in after 4:00 PM"]},
    {"kind": null, "heading": null, "texts": ["Check out before 10:00 AM"]},
    {"kind": null, "heading": null, "texts": ["Minimum age to rent: 25"]},
    {"kind": "child_friendly", "heading": "Children", "texts": ["Children allowed: ages 0-17"]},
    {"kind": "pets__none", "heading": "Pets", "texts": ["No pets allowed"]}
  ],
  "special_features": [],
  "damage_and_incidentals": ["You will be responsible for any damage to the rental property caused by you or your party during your stay."],
  "host": {"premier_host": true, "premier_host_label": "Premier Host", "premier_host_text": "They consistently provide great experiences for their guests", "languages": ["English"]},
  "photo_count": 66,
  "nearby": [{"group": "What's nearby", "places": [{"name": "Big Kahuna's Water and Adventure Park", "distance": "0.7 km", "travel_time": "8 min walk"}, {"name": "Choctawhatchee Bay", "distance": "1.2 km", "travel_time": "14 min walk"}, {"name": "Destin Harbor", "distance": "1.6 km", "travel_time": "19 min walk"}]}],
  "default_price": {"label": "the site's own default stay, not a quote", "price": 176, "price_display": "$176", "qualifier": "avg per night", "messages": ["$352 for 2 nights", "All fees included", "Dec 9 - Dec 11"], "site_note": "Add dates for total pricing", "currency": "USD"}
}
```

The same property on search for Jan 15-18 read $203 a night and $610 for 3 nights: the search price is the one for the user's dates. In `en-gb`, 11546610 (Perranporth) read `space` 2 bedrooms, 1 bathroom, sleeps 4, a Pets group "Pet friendly", and `default_price` `null`. In `ja-jp`, `pdp/lo/9848668` came back in Japanese (`property_type` "アパートメント", `rating.label` "とても素晴らしい", 360 reviews, 54 photos) with `host` `null`. A property id Vrbo does not have answered `404` "Vrbo has no property 999999999." and was charged 2 credits.

### Destination suggestions

`/suggestions` `{"query": "destin"}` (2 credits): 8 places, first `{"type": "CITY", "region_id": "6906", "name": "Destin", "display_name": "Destin, Florida, United States", "latitude": 30.385611, "longitude": -86.465149, "country_code": "US"}`, then Destin Beaches (POI), Crystal Beach (NEIGHBORHOOD), Destin Harbor Boardwalk (POI), the Destin-Fort Walton Beach airport (AIRPORT) ... `{"query": "gatlinburg"}` gave Gatlinburg (CITY, `7474`) first; `{"query": "lake tahoe", "market": "ja-jp"}` gave the names in Japanese (レイク タホ, `180041`).

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def vrbo(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/vrbo/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The region id for a place (2 credits)
places = vrbo("suggestions", {"query": "destin"})["data"]["places"]
region = places[0]["region_id"]

# Prices for the dates and guests (2 credits per attempt Vrbo needs, 2 to 8)
res = vrbo("search", {"region_id": region, "check_in": "2027-01-15", "check_out": "2027-01-18", "adults": 2, "sort": "price_low"})
s = res["data"]
print(s["destination_name"], s["matched_total"], "partial" if s["partial"] else "", res["credits_used"], "credits")
for p in s["properties"]:
    pr = p["price"] or {}
    print(p["property_id"], pr.get("nightly_display"), pr.get("total_display"), pr.get("fees_text"), "ad" if p["sponsored"] else "")

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every answer carries `market`, `language`, `currency` and `notes`.

- **search** - `market`, `language`, `currency`, `destination`, `region_id`, `destination_name`, `check_in`, `check_out`, `nights`, `adults`, `children`, `sort`, `filters` (as sent), `applied` (the selections Vrbo's page echoed), `applied_guests` {`adults`, `children`}, `matched_total`, `page_label`, `count`, `partial`, `attempts`, `properties[]`, `notes`.
- **property card** (search) - `position`, `property_id`, `expedia_property_id`, `url`, `path`, `title`, `details`, `messages`, `location_messages`, `rating` {`score`, `score_display`, `label`, `review_count`, `review_count_text`, `external_reviews`}, `price` {`nightly`, `nightly_display`, `total`, `total_display`, `was`, `was_display`, `was_applies_to`, `lead`, `stay_text`, `fees_text`, `price_messages`, `currency`} (or `null`), `deal`, `badges`, `sponsored`, `coordinates` {`latitude`, `longitude`}, `images`.
- **property** - `market`, `language`, `currency`, `requested_id`, `property_id`, `expedia_property_id`, `url`, `title`, `property_type`, `location` {`locality`, `region`, `country`, `address_lines`, `latitude`, `longitude`, `region_id`}, `rating` {`score`, `score_display`, `best`, `label`, `review_count`, `review_count_text`}, `highlights[]` {`title`, `text`}, `space` {`bedrooms`, `bathrooms`, `sleeps`, `texts`}, `amenities[]` {`group`, `items`}, `house_rules[]` {`kind`, `heading`, `texts`}, `important_information[]` {`kind`, `heading`, `texts`}, `special_features`, `description`, `damage_and_incidentals`, `host` {`premier_host`, `premier_host_label`, `premier_host_text`, `languages`} or `null`, `photo_count`, `photos[]` {`url`, `caption`}, `nearby[]` {`group`, `places[]` {`name`, `distance`, `travel_time`}}, `default_price` {`label`, `price`, `price_display`, `qualifier`, `messages`, `site_note`, `currency`} or `null`, `breadcrumbs[]` {`name`, `url`}, `notes`.
- **suggestions** - `market`, `language`, `currency`, `query`, `count`, `places[]` {`type` (CITY, NEIGHBORHOOD, POI, AIRPORT ...), `region_id`, `name`, `display_name`, `full_name`, `primary_name`, `secondary_name`, `latitude`, `longitude`, `country`, `country_code`}, `notes`.

## Guardrails

- Name it "Vrbo (vrbo.com, Expedia Group's vacation rental site)" on first mention, "Vrbo" after that.
- Prices: quote each with the currency, the dates and nights, the guests, the market, `fees_text` as Vrbo wrote it and the `fetched_at` date ("$610 for 3 nights, Jan 15-18, 2027, 2 adults, all fees included, on vrbo.com on Nov 26, 2026"). Say whether a figure is nightly or total. Never present `default_price` as a price for the user's dates.
- Partial answers: when `partial` is true, say that only Vrbo's first 3 properties came back, not 50.
- Sponsored cards: name them as Vrbo's paid placements, in their position; do not drop or reorder them silently.
- Comparisons: the same place, dates and guests, the market and currency beside every number, named site and date. Convert currencies only when asked, and label the result computed with the rate used. No verdict on which rental is better value beyond the numbers shown.
- Hosts: no host is named or identified; `host` is the Premier Host badge and languages only.
- Descriptive only: no commentary on Vrbo's business, fees, pricing practices or policies.
- Do not republish Vrbo photos or descriptions. Write vrbo.com as plain text and cite property ids, region ids and capture dates rather than linking Vrbo pages.
- Terms: Scavio does not collect or store Vrbo data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no booking flow. Vrbo's terms of use cover how its site and content may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, ratings, property ids, amenities or rules. Only return what the API returned, with the `fetched_at` time.
- Not available: reviews (rating and count only), the availability calendar, a price for chosen dates on a property, results past the first 50, booking, host identity, and Vrbo's sister sites (abritel.fr, fewo-direkt.de, stayz.com.au, bookabach.co.nz).

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `destination` or `region_id` ("Send destination (a place name) or region_id (places[].region_id of suggestions)."); a date that is not `YYYY-MM-DD` ("check_in must be a date as YYYY-MM-DD.") or not a real date; "check_in must not be in the past."; "check_in must be within 500 days from today."; "check_out must be after check_in."; "A stay can be at most 90 nights."; children that are not ages 0-17 ("children must be a list of ages from 0 to 17 (one per child).") or more than 10; a `sort`, `property_type`, `amenity`, `house_rule` or `location_type` outside its list; `pets_allowed` with another `house_rule` ("pets_allowed and house_rule are one Vrbo filter group: send one of them."); a `region_id` that is not digits; a `market` outside the 20 codes; `/property` without exactly one of `id` or `url` ("Send one of id (properties[].property_id of search) or url (a vrbo.com property link)."), an id not in a search form ("id must be a Vrbo property id as search returns it (e.g. 5054966, 12245744ha or pdp/lo/30792130)."), or a link that is not a vrbo.com property page; suggestions under 2 characters ("query must be at least 2 characters.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits, or below what the call can bill (8 for a search, 2 for the others). The body carries `billing_url`.
- `404` means not found, and it is charged 2 credits: "Vrbo has no property 999999999.". Take property ids from a search answer and region ids from suggestions rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api).
- `502` means Vrbo data was temporarily unavailable ("Vrbo is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Vrbo is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.97.0
npm install scavio@0.98.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: places } = await scavio.vrbo.suggestions({ query: "destin" });
const { data: stays } = await scavio.vrbo.search({ region_id: "6906", check_in: "2027-01-15", check_out: "2027-01-18", adults: 2, sort: "price_low" });
const { data: gb } = await scavio.vrbo.search({ destination: "Cornwall, England", check_in: "2027-05-14", check_out: "2027-05-17", market: "en-gb" });
const { data: property } = await scavio.vrbo.property({ id: "1046285" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.vrbo.search(...)`, `property` and `suggestions`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 3 endpoints as tools: `search_vrbo`, `get_vrbo_property` and `get_vrbo_suggestions`. Vrbo is opt-in: add `vrbo` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.97.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,vrbo"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/vrbo-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api), [property](https://scavio.dev/docs/vrbo-property?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api), [suggestions](https://scavio.dev/docs/vrbo-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api). Overview: [Vrbo API](https://scavio.dev/vrbo-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=vrbo-api).
