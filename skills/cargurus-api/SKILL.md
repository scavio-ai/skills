---
name: cargurus-api
description: CarGurus API for CarGurus (cargurus.com, the car marketplace run by CarGurus, Inc., in the US, Canada and the UK) - used car asking prices next to CarGurus' own expected price and deal rating, as CarGurus labels them (Great Deal, Good Deal, Fair Deal, High Price, Overpriced, No Price Analysis); a 2019 Toyota RAV4 LE AWD near New York asked 19,445 USD against a CarGurus expected price of 21,255 and was rated Great Deal on Nov 26, 2026; search listings around a US ZIP code, a Canadian postal code or a UK postcode with a radius (or nationwide) on five market-languages (us, us-es, ca, ca-fr, uk) with prices in USD, CAD or GBP, by make, model and trim, 24 tiles a page, 11 sorts (best deal first, price, mileage, distance, model year, newest listed), filtered by year, price, mileage, drivetrain, colour, body type, condition, seller type, deal rating, fuel, transmission, single owner, no accidents and recent price drops, with CarGurus' facet counts on request; each listing carries price, original price, price with fees, expected price and the difference, deal rating and score, the last price drop, days on market, mileage, options, highlights and the dealer's public details; one dealer with address, phones, hours, rating, every review CarGurus shows on the page (no names) and its listings; up to 150 dealers near a US ZIP code; CarGurus price trends (the CarGurus Index, a make, a model and each model year, 30, 90 and 365 days back, daily series); model-year research pages with trims, MSRP, price figures and owner reviews; expert reviews; makes and models with listing counts. 8 endpoints, 1 credit per call. No listing detail page, VINs, private-seller details or sold prices.
version: 1.0.0
tags: cargurus, cargurus-com, cargurus-api, cargurus-listings, cargurus-search, cargurus-deal-rating, cargurus-expected-price, cargurus-imv, cargurus-price-trends, cargurus-index, cargurus-dealers, cargurus-dealer-reviews, cargurus-research, cargurus-expert-reviews, cargurus-canada, cargurus-uk, used-car-prices, used-car-listings, car-listings, deal-rating, expected-price, price-drops, days-on-market, car-dealers, dealer-reviews, used-car-price-trends, car-prices-canada, car-prices-uk, cad, gbp, usd, spanish, french, car-market, price-research, price-comparison, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/cargurus-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api
---

# CarGurus API - Deal Ratings, Expected Price, Listings, Price Trends

Read CarGurus (cargurus.com, the car marketplace run by CarGurus, Inc., in the US, Canada and the UK) on its US, Canadian and UK sites: search listings, one dealer with its reviews and inventory, the dealers near a US ZIP code, CarGurus' price trends, model-year research pages, expert reviews, and the makes and models with listing counts. Every answer is what CarGurus' public pages show a visitor without an account at the moment of the call, in the market's language and currency. All 8 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages CarGurus shows to any visitor and returns them as JSON for analysis. It uses no CarGurus account, no saved searches, no messaging, no financing and no dealer contact forms.

**The job this skill is for: asking price next to CarGurus' expected price and deal rating.** Every listing carries CarGurus' own price analysis: `expected_price` (CarGurus' expected price for the car), `expected_price_difference` (expected minus asking: positive when the car asks less), and `deal_rating` with `deal_rating_label` and `deal_score`. Report them exactly as CarGurus labels them, next to the asking price and the mileage. Captured 2026-11-26 with `/search`:

| Listing (dealer city, placement) | Mileage | Asking | CarGurus expected price | Difference | `deal_rating_label` |
|---|---|---|---|---|---|
| 2019 Toyota RAV4 LE AWD (West Nyack, NY, standard) | 64,213 mi | 19,445 USD | 21,255 | 1,810 | Great Deal |
| 2024 Toyota RAV4 LE AWD (Hempstead, NY, standard) | 21,162 mi | 26,357 USD | 28,395 | 2,038 | Great Deal |
| 2017 Toyota RAV4 SE AWD (Brooklyn, NY, standard) | 126,632 mi | 13,700 USD | 13,706 | 6 | Fair Deal |
| 2024 Toyota RAV4 LE AWD (Valley Stream, NY, priority, sponsored) | 36,084 mi | 27,000 USD | 27,763 | 763 | Good Deal |
| 2009 Toyota RAV4 Base 4WD (North York, ON) | 260,570 km | 5,490 CAD | 6,190 | 700 | Good Deal |
| 2008 Toyota RAV4 Limited V6 AWD (Brampton, ON) | 168,700 km | 4,990 CAD | null | null | No Price Analysis |
| 2022 Ford Focus (Morley, priority, sponsored) | 20,988 mi | 16,130 GBP | 21,410 | 5,280 | Great Deal |

The rating is CarGurus', not a verdict: quote it as "CarGurus rates it a Great Deal", never as "a great deal". A car CarGurus does not analyse reads No Price Analysis with `expected_price` null, and a few US tiles carry no rating at all (`deal_rating` null): say so, never fill it in. Labels come in the market's language (us-es "Gran oferta", "Buena oferta"; uk "High price"). Put each row with its listing id, market, currency, mileage unit and the capture date.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** A make or model name resolved on a first CarGurus page is still 1. `credits_used` in every answer says what was spent. A not-found (`404`: an unknown dealer, research page or model) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **No listing detail endpoint.** CarGurus' listing pages are not served, so there is no `/listing`. Each search result already carries the price, original price, price with fees, expected price, deal rating, the last price drop, days on market, mileage, options, highlights, specs and the dealer; `url` is the listing's CarGurus page for people.
- **Five market-languages, three sites.** `market` `us` (cargurus.com, USD, miles), `us-es` (its Spanish pages), `ca` (cargurus.ca, CAD, km), `ca-fr` (its French pages), `uk` (cargurus.co.uk, GBP, miles). Labels come in the market's language (`ca-fr`: "Bonne affaire", "Affaire formidable"; `us-es`: "Trato justo"). Not every endpoint serves every market: `dealers` us and us-es; `price_trends` and `expert_reviews` us, ca and uk; `research` us only.
- **Ids are per site.** Make and model ids differ by site (Ford is `m2` on the US and Canadian sites, `m273` on the UK site; Toyota `m7` and `m201`). Send names, or ids from that market's `/makes` and `/models`.
- **Sponsored placements are flagged.** CarGurus inserts its priority and featured placements into the results out of the requested order: `sponsored` true and `placement` (`priority`, `featured`, `standard`, `personalized`) say which. In the `ca` capture sorted `price_low`, sponsored RAV4s at 32,712, 42,990 and 27,999 CAD led a page that then ran 4,990, 5,490, 5,999. Skip sponsored tiles when you read an order or a cheapest price.
- **24 tiles a page.** About 18-24 listings a page (CarGurus' own promotion tiles are left out), `page` 1-500; `total` and `page_count` are CarGurus' counts.
- **Reviews are what the page shows.** `/dealer` returns every dealer review CarGurus embeds in the page (`review_count` is CarGurus' count; the UK capture returned 49 of 50). CarGurus offers no review paging, sort or star filter: filter on your side. Reviewer names are not returned; a name quoted in a review or a dealer reply reads `[name]`.
- **No private-seller details, no VINs.** No VINs, stock numbers or private-seller details are returned (a listing from a non-dealer seller keeps only its region). Dealer names, addresses, phones, hours and ratings are CarGurus' public dealer details.
- **Price trends are CarGurus' averages.** `/price-trends` returns CarGurus' published averages (the CarGurus Index, a make, a model, each model year) with the change 30, 90 and 365 days back and a daily series. They are average asking prices as CarGurus publishes them, not sold prices.
- **Pages can be slow.** Answers took 3 to 31 seconds in the captures and can take up to two minutes; CarGurus occasionally fails a page, which comes back as a `502` (not charged). Set a client timeout of at least 240 seconds and send one request at a time.

CarGurus publishes no public API for reading listings. Its dealer products (Listings, PriceVantage, StockVantage, VINMax, Dealer Dashboard at dealers.cargurus.com) are for dealers: inventory flows into CarGurus, not out. This skill reads CarGurus' public search, dealer, price trends, research and review pages with one Scavio key. Other vendors offer CarGurus data tools; this skill reads CarGurus' own public pages.

CarGurus, Inc. (NASDAQ: CARG) says on its investor site "We operate online marketplaces in the U.S., U.K., and Canada." Quote it with that source, never from the samples.

See also: `autotrader-api` (Autotrader's KBB Fair Purchase Price range and deal label for US listings), `cars-com-api` (Cars.com listings and dealers), `carmax-api` (CarMax's own prices), `carvana-api` (Carvana's online prices) and `offerup-api` (local used-car asks). Same car only: year, make, model, trim and a mileage band must match; show each price with its marketplace, market, currency and date, and keep each site's price analysis labelled as that site's.

## When to trigger

Use this skill when the user asks to:
- Read CarGurus asking prices for a make and model around a US ZIP code, a Canadian postal code or a UK postcode
- Put an asking price next to CarGurus' expected price and deal rating
- Find only the listings CarGurus rates a Great or Good Deal, single-owner cars, cars with no accidents or recent price drops
- Compare the same model's CarGurus prices across the US, Canada and the UK, or in Spanish or French
- Read one CarGurus dealer's address, phones, hours, rating, reviews and listings
- Find the dealers with listings near a US ZIP code, with their listing counts
- Read CarGurus' used-car price trends for the market, a make, a model or a model year
- Read a model year's trims with MSRP, CarGurus' price figures and owner reviews, or CarGurus' expert reviews

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, dealers answered in 3-10 seconds, expert reviews 4-11, price trends 4-10, makes and models 5-11, research 5-14, dealer 6-22 and search 4-31. Allow up to two minutes, set a client timeout of at least 240 seconds, and send one request at a time.

| Endpoint | What it returns | Markets | Credits |
|---|---|---|---|
| `POST /api/v1/cargurus/search` | Listings around a place: price, expected price, deal rating, price drop, mileage, specs, dealer; total, pages, applied filters, trims, facets on request | us, us-es, ca, ca-fr, uk | 1 |
| `POST /api/v1/cargurus/dealer` | One dealer: address, phones, website, hours, rating, every review on the page, its listings (paged, sorted, filtered like search), nearby dealers | us, us-es, ca, ca-fr, uk | 1 |
| `POST /api/v1/cargurus/dealers` | Up to 150 dealers with listings near a US ZIP code (optionally for one make or model), with listing counts and ratings | us, us-es | 1 |
| `POST /api/v1/cargurus/price-trends` | CarGurus price trends for the market, a make or a model: averages today, 30, 90 and 365 days back, daily series, model years with `research_id` | us, ca, uk | 1 |
| `POST /api/v1/cargurus/research` | One model year: trims with MSRP and specs, price figures, test-drive review, owner reviews and CarGurus' AI summary as given | us | 1 |
| `POST /api/v1/cargurus/expert-reviews` | CarGurus' expert reviews, 24 a page, with rating and `research_id` | us, ca, uk | 1 |
| `POST /api/v1/cargurus/makes` | Every make the market's site lists, with `make_id` | us, us-es, ca, ca-fr, uk | 1 |
| `POST /api/v1/cargurus/models` | One make's models with CarGurus' listing counts, nationwide or around a place | us, us-es, ca, ca-fr, uk | 1 |

## Markets

| `market` | Site | Language | Currency | Distance | `zip` takes |
|---|---|---|---|---|---|
| `us` (default) | cargurus.com | en | USD | miles | a 5-digit US ZIP code |
| `us-es` | cargurus.com/es | es | USD | miles | a 5-digit US ZIP code |
| `ca` | cargurus.ca | en | CAD | km | a Canadian postal code (`M5V 2T6`) |
| `ca-fr` | cargurus.ca/fr | fr | CAD | km | a Canadian postal code |
| `uk` | cargurus.co.uk | en | GBP | miles | a UK postcode (`M1 1AE`) |

Every answer carries `market` {`market`, `country`, `language`, `currency`, `distance_unit`}. `distance`: us and uk 10, 25, 50 (default), 75, 100, 150, 200, 500 miles; ca 25, 50, 75, 100, 250, 500 km; or `"nationwide"`.

## Prices and ratings

| Field | Meaning |
|---|---|
| `price`, `price_text`, `currency` | The asking price on the listing and the text CarGurus shows ("$27,000", "40 995 $", "£16,130"); `null` when the listing shows no price |
| `original_price` | The listing's earlier price where CarGurus shows one |
| `price_with_fees`, `fee_disclosure` | The price with the dealer's fees where CarGurus gives it, and its disclosure code |
| `expected_price`, `expected_price_difference` | CarGurus' expected price for the car and expected minus asking (positive = the car asks less); `null` without an analysis |
| `deal_rating`, `deal_rating_label`, `deal_score` | CarGurus' rating (`GREAT_PRICE`, `GOOD_PRICE`, `FAIR_PRICE`, `POOR_PRICE`, `OVERPRICED`, `OUTLIER`, `NA`), its label in the market's language and its score, as given |
| `price_drop` | {`previous_price`, `amount`, `dropped_at`}: the last price drop CarGurus shows, else `null` |
| `days_on_market` | CarGurus' days-on-market count |
| `mileage`, `mileage_unit` | Miles (us, us-es, uk) or km (ca, ca-fr) |
| `highlights` | CarGurus' highlights as given ("No accidents", "1 owner", "NHTSA 5 star safety rating") |
| `placement`, `sponsored` | `standard`, `priority`, `featured` or `personalized`; `sponsored` true on priority and featured placements |
| `dealer` | {`dealer_id`, `name`, `city`, `region`, `postal_code`, `phone`, `franchise_dealer`, `franchise_make`, `rating`, `url`}: public dealer details |

- **Deal rating names:** the `deal_rating` input takes `great`, `good`, `fair`, `high`, `overpriced`, `uncertain`, `no_analysis` or CarGurus' own names (`GREAT_PRICE` ...).
- **Ids:** `listing_id`, `dealer_id` (digits), `make_id` (`m7`), `model_id` (`d306`), `trim_id`, `research_id` (`c31935`). Send them as strings.

## Workflow

1. **Pick the market and the place.** `market` and a `zip` in that market's format. For a model name in doubt, `/makes` and `/models` give that site's ids and listing counts.
2. **Search.** `/search` with `zip`, `make`, `model` (and `trim`, `distance`, `sort`, filters). Note `location.resolved`, `total`, `page_count` and `applied_filters`. Add `include_facets: true` once to see CarGurus' filters with counts.
3. **Read the price analysis.** For each non-sponsored listing: `price`, `mileage`, `expected_price`, `expected_price_difference`, `deal_rating_label`, `price_drop` and `days_on_market`, all as given.
4. **Dealers.** `/dealers` with a US `zip` for the dealers near it with listing counts; `/dealer` with `dealer_id` for its address, hours, reviews and listings.
5. **Market context.** `/price-trends` for the CarGurus Index, a make or a model (30, 90, 365 days and the daily series); `model_years[].research_id` opens `/research` for a model year's trims, MSRP and owner reviews.
6. **Report.** Each car with year, make, model, trim, mileage and unit, asking price with currency, CarGurus' expected price and rating as CarGurus labels them, the dealer's city, the listing id, the market and the capture date.
7. **Price series:** CarGurus' `/price-trends` is its own series; for listings there is no history beyond `price_drop`. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`) and the dealer's listings (`/dealer`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `market` | string | `us` | `us`, `us-es`, `ca`, `ca-fr`, `uk` |
| `zip` | string | required (search) | A US ZIP code, Canadian postal code or UK postcode, per market |
| `distance` | integer or string | 50 | The radii above, or `"nationwide"` |
| `make` | string | none | A make name (Toyota, Mercedes-Benz) or that site's `make_id` |
| `model` | string | none | A model name (RAV4, F-150) or `model_id`. Needs `make` |
| `trim` | string | none | A trim as CarGurus names it (XLE, XLT). Needs `model` |
| `page` | integer | 1 | 1-500; 24 tiles a page |
| `sort` | string | `best_match` | `best_match`, `best_deal` (CarGurus' "Best deals first", used cars), `price_low`, `price_high`, `mileage_low`, `mileage_high`, `closest`, `year_newest`, `year_oldest`, `listed_newest`, `listed_oldest` |
| `year_min`, `year_max` | integer | none | Model year range |
| `price_min`, `price_max` | integer | none | Whole units of the market's currency |
| `mileage_min`, `mileage_max` | integer | none | Miles, or km in ca / ca-fr |
| `drivetrain` | string or list | none | `awd`, `4wd`, `fwd`, `rwd`, `4x2` |
| `color` | string or list | none | black, blue, brown, gold, gray, green, orange, pink, purple, red, silver, teal, white, yellow |
| `body_type` | string or list | none | coupe, convertible, hatchback, minivan (mpv), pickup, sedan (saloon), suv, van, wagon (estate) |
| `condition` | string or list | none | us / ca: `used`, `certified`, `third_party_certified`; uk: `approved_used` |
| `seller_type` | string or list | none | `franchise_dealer` or `cargurus_partner` |
| `deal_rating` | string or list | none | `great`, `good`, `fair`, `high`, `overpriced`, `uncertain`, `no_analysis` |
| `fuel_type` | string or list | none | gasoline (petrol), diesel, electric, hybrid, flex_fuel, cng, biodiesel, hydrogen, dual_fuel |
| `transmission` | string or list | none | `automatic` or `manual` |
| `single_owner`, `no_accidents`, `price_drops_only` | boolean | false | CarGurus' single-owner, no-accidents and recent-price-drop filters |
| `filters` | object | none | Other CarGurus filters by their key from `facets[].key` (up to 12): daysOnMarketMin/Max, minMpg/maxMpg, hideWithoutPhotos, hideFrameDamaged, hideTheft, interiorColors, hideFleet, hideLemon, hideSalvage, doors, installedOptionIds, safetyRatings, averageDealerRatings, EV battery range and charging time ... |
| `include_facets` | boolean | false | Search only: also return `facets` with counts |

`/dealer` takes `dealer_id` or `url` (a cargurus.com, .ca or .co.uk `/Cars/m-<dealer name>-sp<id>` link; its site sets the market) plus the listing parameters above for its inventory (no `zip`, `distance` or `include_facets`).

### Dealers, price trends, research, expert reviews, makes, models

| Endpoint | Parameters |
|---|---|
| `/dealers` | `zip` (required, US), `market` (`us` or `us-es`), `distance`, `make`, `model` |
| `/price-trends` | `market` (`us`, `ca`, `uk`), optional `make`, optional `model` (with `make`); without `make`: the market's index, makes and body styles |
| `/research` | `research_id` (`c31935`) or `url`, or `year` with `make` and `model`; `market` `us` |
| `/expert-reviews` | `market` (`us`, `ca`, `uk`), `page` 1-200 |
| `/makes` | `market` |
| `/models` | `make` (required: name or `make_id`), `market`, optional `zip` and `distance` (else nationwide) |

## Examples

### Search a model around a ZIP code

```bash
curl -X POST https://api.scavio.dev/api/v1/cargurus/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"zip": "10001", "make": "Toyota", "model": "RAV4"}'
```

Captured `data` (2026-11-26; `listings` cut to 1 of 22, `trims`, `facets` and `notes` dropped; `photo`, `options` and `url` dropped from the listing):

```json
{
  "market": {"market": "us", "country": "us", "language": "en", "currency": "USD", "distance_unit": "miles"},
  "location": {"zip": "10001", "resolved": "New York, NY", "distance": 50, "distance_unit": "miles", "nationwide": false},
  "make": {"id": "m7", "name": "Toyota"},
  "model": {"id": "d306", "name": "RAV4"},
  "trim": null,
  "make_model_trim_path": "m7/d306",
  "sort": "best_match",
  "applied_filters": {"distance": 50, "makeModelTrimPaths": ["m7/d306"]},
  "total": 1107,
  "page": 1,
  "page_count": 53,
  "has_more": true,
  "count": 22,
  "listings": [
    {"listing_id": "462468149", "title": "2024 Toyota RAV4", "name": "2024 Toyota RAV4 LE AWD", "year": 2024, "make": "Toyota", "make_id": "m7", "model": "RAV4", "model_id": "d306", "trim": "LE AWD", "trim_id": "t108870", "body_type": "SUV / Crossover", "condition": "CPO", "price": 27000, "price_text": "$27,000", "currency": "USD", "original_price": 29277, "price_with_fees": 27175, "fee_disclosure": "BASE_PRICE_DISCLOSED", "expected_price": 27763, "expected_price_difference": 763, "deal_rating": "GOOD_PRICE", "deal_rating_label": "Good Deal", "deal_score": 1.655, "price_drop": null, "days_on_market": 33, "mileage": 36084, "mileage_unit": "miles", "exterior_color": "Magnetic Gray Metallic", "interior_color": "Black", "transmission": "8-Speed Automatic", "drivetrain": "All-Wheel Drive", "engine": "2.5L I4", "fuel_type": "Gasoline", "mpg": {"city": 27, "highway": 34, "combined": 30.15, "unit": "MPG"}, "doors": "4 doors", "highlights": ["No accidents", "NHTSA 5 star safety rating"], "safety_rating": "5", "photo_count": 37, "placement": "priority", "sponsored": true, "distance": 15.9, "seller_type": "dealer", "dealer": {"dealer_id": "54565", "name": "Advantage Toyota", "city": "Valley Stream", "region": "NY", "postal_code": "11581", "phone": "(516) 980-3271", "franchise_dealer": true, "franchise_make": "Toyota", "rating": 2.88, "url": "https://www.cargurus.com/Cars/m-Advantage-Toyota-sp54565"}}
  ]
}
```

This first tile is a sponsored priority placement. Further down the page a 2025 RAV4 XLE FWD carried `price_drop` {`previous_price` 28695, `amount` 700, `dropped_at` "2026-11-25T01:23:43.000Z"}. `trims` lists the model's trims with counts (Limited AWD 130, XLE Premium FWD 113, LE 50 ...).

### Other markets and filters

- `/search` `{"market": "ca", "zip": "M5V 2T6", "make": "Toyota", "model": "RAV4", "sort": "price_low"}`: Toronto, ON, 50 km, `total` 720 over 32 pages, CAD and km; three sponsored tiles first (a 2024 RAV4 XLE AWD at 32,712), then a 2008 RAV4 Limited V6 AWD at 4,990 with No Price Analysis.
- `/search` `{"market": "uk", "zip": "M1 1AE", "make": "Ford", "model": "Focus", "sort": "mileage_low"}`: Manchester, `make` {`id` m273}, `model` {`id` d3082}, `total` 944; a 2022 Ford Focus at 16,130 GBP ("£16,130") against an expected 21,410, Great Deal.
- `/search` `{"market": "ca-fr", "zip": "H2X 1Y4", "distance": 100, "deal_rating": ["great", "good"]}`: Montreal, QC, `total` 6744, `applied_filters` {`dealRatings` [GREAT_PRICE, GOOD_PRICE]}; French titles and labels ("Nissan Kicks 2018", "9 992 $", "VUS", "Traction avant", "Affaire formidable").
- `/search` `{"zip": "75201", "distance": 100, "make": "Ford", "model": "F-150", "trim": "XLT", "sort": "price_high", "deal_rating": "great", "seller_type": "franchise_dealer"}`: Dallas, TX, `make_model_trim_path` m2/d337/XLT, `total` 19, every tile Great Deal.

### One dealer with reviews and listings

```bash
curl -X POST https://api.scavio.dev/api/v1/cargurus/dealer \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"dealer_id": "440818"}'
```

Captured (2026-11-26; abridged): `dealer` Pristine Mitsubishi, 1158 Jericho Tpke, Commack, NY 11725, `sales_phone` (631) 529-1459, `service_phone` (631) 864-1200, `hours` Monday-Friday 9:00 AM-8:00 PM, Saturday-Sunday 10:00 AM-6:00 PM, `rating` 2.14, `review_count` 43; `reviews` 43 (28 one-star, 9 five-star, 3 four-star, 2 two-star, 1 three-star), each {`review_id`, `rating`, `date`, `content`, `purchase_status`, `dealer_response` {`text`, `date`}} with names in the text read as `[name]`; `inventory` {`total` 192, `page` 1, `page_count` 9, `count` 23, `listings` [...]}, first a 2024 Audi Q4 e-tron Sportback at 26,295 against an expected 28,248, Great Deal; `nearby_dealers` with address, rating and listing count.

- `/dealer` `{"dealer_id": "316651", "page": 2, "sort": "price_low"}`: Karp Automotive, Rockville Centre, NY, `inventory` page 2 of 18 (`total` 410).
- `/dealer` `{"dealer_id": "348647", "market": "ca"}`: Northwest Autohaus, North York, ON, 5 of 5 reviews, 72 listings.

### Dealers near a ZIP, price trends, research, expert reviews, makes, models

- `/dealers` `{"zip": "10001", "distance": 25}`: New York, NY, 150 dealers, `total_listings` 50252; first Certified Performance Motors (Valley Stream, NY, 15.9 miles, 202 listings, rating 2.44); `rating` null where CarGurus shows none.
- `/price-trends` `{}` (us): the CarGurus Index `average_price` 28,289 USD (with fees 28,732), 30 days ago 28,636 (-1.21%), 90 days ago 29,124 (-2.87%), 365 days ago 27,834; 47 makes and 9 body styles; `series` 76 daily points, last 2026-11-23 at 28,282.
- `/price-trends` `{"market": "ca", "make": "Toyota", "model": "RAV4"}`: the Canadian index 33,026 CAD, Toyota RAV4 31,031 CAD (+0.85% on 30 days ago, +0.92% on 90), 20 model years each with a `research_id`. `{"market": "uk"}`: index 16,153 GBP, 34 makes.
- `/research` `{"research_id": "c31935"}`: 2022 Toyota 4Runner, 13 trims (Trail Special Edition 4WD MSRP 41,950, SR5 Premium 4WD 43,390 ...), `pricing` {`today_price` 38579, `one_month_ago_price` 39053, `one_year_ago_price` 40019, `original_msrp_min` 38105, `original_msrp_max` 52420}, a test-drive review by CarGurus editors, `owner_reviews` {`average_rating` 4.78, `total_ratings` 9, `ai_summary` (CarGurus' own AI summary, as CarGurus shows it)}. `{"year": 2021, "make": "Ford", "model": "F-150"}` found `c30674` with 45 trims and 31 owner reviews.
- `/expert-reviews` `{"page": 2}`: `total` 1683 over 71 pages; first "2026 Honda Accord Review", `rating` 7, `research_id` c34552.
- `/makes` `{}`: 119 makes on cargurus.com (`m4` Acura ...); on the UK site 101 (Ford `m273`, Toyota `m201`). `/models` `{"make": "Toyota"}`: 73 models nationwide, Camry 24,494 listings, RAV4 23,165, Tacoma 20,410, Corolla 19,137.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def cargurus(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/cargurus/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The same model in the US and Canada, asking price next to CarGurus' expected price (1 credit each)
for body in [{"market": "us", "zip": "10001"}, {"market": "ca", "zip": "M5V 2T6"}]:
    d = cargurus("search", {**body, "make": "Toyota", "model": "RAV4", "sort": "best_deal"})["data"]
    print(d["market"]["currency"], d["location"]["resolved"], d["total"])
    for car in d["listings"]:
        if car["sponsored"]:
            continue  # priority / featured placements sit out of the requested order
        print(car["listing_id"], car["name"], car["mileage"], car["mileage_unit"], car["price"],
              car["expected_price"], car["expected_price_difference"], car["deal_rating_label"])

# Store each answer with fetched_at: that stored set is your price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` and `notes`.

- **listing tile** (search `listings[]`, dealer `inventory.listings[]`) - `listing_id`, `title`, `name`, `year`, `make`, `make_id`, `model`, `model_id`, `trim`, `trim_id`, `body_type`, `condition`, `price`, `price_text`, `currency`, `original_price`, `msrp`, `price_with_fees`, `fee_disclosure`, `expected_price`, `expected_price_difference`, `deal_rating`, `deal_rating_label`, `deal_score`, `price_drop` {`previous_price`, `amount`, `dropped_at`}, `days_on_market`, `mileage`, `mileage_unit`, `exterior_color`, `interior_color`, `transmission`, `drivetrain`, `engine`, `fuel_type`, `mpg` {`city`, `highway`, `combined`, `unit`}, `ev`, `doors`, `options`, `highlights`, `safety_rating`, `ulez_compliant` (uk), `photo`, `photo_count`, `placement`, `sponsored`, `buying_option`, `distance`, `seller_type`, `dealer`, `url`.
- **search** - `market`, `location` {`zip`, `resolved`, `distance`, `distance_unit`, `nationwide`}, `make` {`id`, `name`}, `model`, `trim`, `make_model_trim_path`, `sort`, `applied_filters`, `total`, `page`, `page_count`, `has_more`, `count`, `listings[]`, `trims[]` {`trim`, `count`} (with a model), `facets[]` {`facet`, `label`, `key`, `min_key`, `max_key`, `values[]` {`value`, `label`, `count`}, `range`} (with `include_facets`).
- **dealer** - `dealer` {`dealer_id`, `name`, `address` {`street`, `city`, `region`, `postal_code`}, `sales_phone`, `service_phone`, `website`, `maps_url`, `location`, `logo`, `hours[]` {`day`, `open`, `close`, `is_open`}, `current_day`, `rating`, `review_count`, `social`, `url`}, `review_count_returned`, `reviews[]` {`review_id`, `rating`, `date`, `content`, `purchase_status`, `delivery`, `helpful`, `dealer_response`}, `inventory` {`make`, `model`, `trim`, `sort`, `total`, `page`, `page_count`, `has_more`, `count`, `listings[]`}, `nearby_dealers[]`.
- **dealers** - `location`, `make`, `model`, `count`, `total_listings`, `dealers[]` {`dealer_id`, `name`, `rating`, `distance`, `city`, `region`, `listing_count`, `url`}.
- **price trends** - `scope` (`market`, `make` or `model`), `make`, `model`, `currency`, `name`, `groups` {`index`, `makes`, `models`, `model_years`, `body_styles`: [{`id`, `name`, `parent`, `average_price`, `average_price_with_fees`, `history[]` {`days_ago`, `average_price`, `average_price_with_fees`, `change_to_today_pct`, `change_with_fees_to_today_pct`}, `research_id`}]}, `series[]` {`id`, `name`, `points[]` {`date`, `price`, `price_with_fees`}}, `market_movers` {`decrease`, `increase`}, `faqs` (CarGurus' text), `date_range`, `listings_url`.
- **research** - `research_id`, `name`, `make`, `model`, `year`, `currency`, `trims[]` {`trim_id`, `name`, `msrp`, `engine`, `horsepower`, `drivetrain`, `fuel_economy_city`, `fuel_economy_highway`, `seating_capacity`, `cargo_space`}, `pricing`, `price_series`, `test_drive_review`, `owner_reviews` {`average_rating`, `total_ratings`, `count_by_rating`, `ai_summary`, `count`, `reviews[]` {`review_id`, `rating`, `title`, `content`, `date`}}, `listings_url`, `url`.
- **expert reviews** - `page`, `page_size`, `total`, `page_count`, `has_more`, `count`, `reviews[]` {`title`, `vehicle`, `rating`, `updated_at`, `summary`, `image`, `author`, `research_id`, `url`}.
- **makes** - `count`, `makes[]` {`make_id`, `name`, `popular`}. **models** - `make` {`id`, `name`}, `location`, `count`, `models[]` {`model_id`, `name`, `count`, `popular`}.

## Guardrails

- Name it "CarGurus (cargurus.com, the car marketplace run by CarGurus, Inc., in the US, Canada and the UK)" on first mention, "CarGurus" after that.
- Prices: quote each with its currency, mileage and unit, year, make, model, trim, the dealer's city, the listing id, the market and the `fetched_at` date ("listed on cargurus.com on Nov 26, 2026"). These are asking prices, never sold prices.
- Ratings: quote `expected_price`, `expected_price_difference` and `deal_rating_label` exactly as CarGurus gives them and say they are CarGurus' ("CarGurus' expected price is 21,255 and it rates the car a Great Deal"). Never fill in a missing analysis, never re-rate a car, and give no buy or negotiate advice beyond the numbers shown.
- Sponsored: name priority and featured placements as sponsored; leave them out of any order or cheapest-price claim.
- Comparisons: the same year, make, model, trim and a similar mileage band; across markets keep each currency and unit as given (no conversion unless the user asks, and then label it converted with the rate and date). Keep each site's price analysis labelled as that site's.
- Reviews: no reviewer names (none are returned); quote review text sparingly, with the dealer, rating and date.
- No VINs, no private-seller details: none are returned; never add or guess one.
- Descriptive only: no commentary on CarGurus' business, its dealers, its ratings method or its pricing practices. Quote CarGurus, Inc. figures only with their source and date.
- Do not republish CarGurus photos, listing text or reviews in bulk. Write cargurus.com as plain text and cite listing ids, dealer names and capture dates rather than linking CarGurus pages.
- Terms: Scavio does not collect or store CarGurus data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no contact forms. CarGurus' terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, expected prices, ratings, mileages, listing ids, dealers or reviews. Only return what the API returned, with the `fetched_at` time.
- Not available: a listing detail page, VINs, stock numbers, private-seller details, sold prices, search suggestions, dealer lists on the Canadian and UK sites, research pages outside the US site.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: no `zip`, or one not in the market's format ("zip must be a 5-digit US ZIP code (e.g. 10001).", "... a Canadian postal code (e.g. M5V 2T6).", "... a UK postcode (e.g. M1 1AE or SW1A 1AA)."), a `market` outside the five or not served by the endpoint ("market ca is not served for this endpoint: it takes us, us-es."), a `distance` the site does not offer, a `sort` outside the 11, a make the site does not list, `model` without `make`, a `trim` with a slash, a filter value not offered, more than 12 `filters` keys, `dealer_id` and `url` together, a malformed `research_id`.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "No CarGurus dealer <id>.", "No CarGurus research page <id>.", "No model "<model>" among the <make> models CarGurus lists for this request. Send a model name as CarGurus shows it, or model_id from models.", "No CarGurus UK dealer <id> with listings: send the dealer's CarGurus link (url) instead.". Take ids and names from a previous answer rather than guessing them.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api).
- `502` means CarGurus data was temporarily unavailable ("CarGurus is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds; UK dealer pages needed up to three tries in the captures.
- `503` with a `Retry-After` header means the service is busy ("CarGurus is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.96.0
npm install scavio@0.97.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: rav4 } = await scavio.cargurus.search({ zip: "10001", make: "Toyota", model: "RAV4" });
const { data: dealer } = await scavio.cargurus.dealer({ dealer_id: "440818" });
const { data: near } = await scavio.cargurus.dealers({ zip: "10001", distance: 25 });
const { data: trends } = await scavio.cargurus.priceTrends({ market: "ca", make: "Toyota", model: "RAV4" });
const { data: year } = await scavio.cargurus.research({ research_id: "c31935" });
const { data: expert } = await scavio.cargurus.expertReviews({ page: 2 });
const { data: makes } = await scavio.cargurus.makes({ market: "uk" });
const { data: models } = await scavio.cargurus.models({ make: "Toyota" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.cargurus.search(...)`, `dealer`, `dealers`, `price_trends`, `research`, `expert_reviews`, `makes` and `models`, with the same parameter names as keyword arguments. Set the client timeout to 240 seconds.

## MCP

The Scavio MCP server exposes all 8 endpoints as tools: `search_cargurus`, `get_cargurus_dealer`, `get_cargurus_dealers`, `get_cargurus_price_trends`, `get_cargurus_research`, `get_cargurus_expert_reviews`, `get_cargurus_makes` and `get_cargurus_models`. CarGurus is opt-in: add `cargurus` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.96.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,cargurus"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/cargurus-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api), [dealer](https://scavio.dev/docs/cargurus-dealer?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api), [dealers](https://scavio.dev/docs/cargurus-dealers?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api), [price trends](https://scavio.dev/docs/cargurus-price-trends?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api), [research](https://scavio.dev/docs/cargurus-research?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api), [expert reviews](https://scavio.dev/docs/cargurus-expert-reviews?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api), [makes](https://scavio.dev/docs/cargurus-makes?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api) and [models](https://scavio.dev/docs/cargurus-models?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api). Platform overview: [CarGurus API](https://scavio.dev/cargurus-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=cargurus-api).
