---
name: lennar-homes-api
description: Lennar API for Lennar (lennar.com, the US homebuilder; 32 states, 104 metro markets) - what a new Lennar home costs today next to the price Lennar showed before, as Lennar's own pages show it (a move-in ready Melrose II in Kresston, Montgomery, Texas read 384,990 USD, was 424,990 USD, against the plan's 424,990 USD starting price; a Providence in Knightsbridge, Kissimmee, Florida read 436,320 USD, was 471,320 USD, with an estimated move-in of Dec 14, 2026) with homesite search by market, state, city, map point or map box, filtered by beds, baths, price, square feet, home type, active adult or lifestyle community, quick move-in or under construction, feature codes and school filters, 7 sorts, up to 200 a page with Lennar's counts of communities, plans and homesites; communities with every plan and homesite, the HOA fee, tax rate, deposit and sales center hours; floor plans with included features; one homesite with its incentive, offer end date and estimated payment; master-planned communities; every market and one market's cities, feature codes and school districts; each market's current promotion with its offers and legal copy exactly as Lennar shows them; Lennar's own monthly payment estimate for a homesite at a down payment and interest rate; place suggestions and link lookups. 11 endpoints, 1 credit per call. US only, USD. No price history, resale homes, reviews or sales consultant names.
version: 1.0.0
tags: lennar, lennar-com, lennar-homes, lennar-api, lennar-new-homes, lennar-prices, lennar-communities, lennar-floor-plans, lennar-quick-move-in, lennar-move-in-ready, lennar-incentives, lennar-promotions, lennar-deals, lennar-hoa, lennar-markets, lennar-payment-estimate, lennar-master-planned, new-homes, new-home-prices, new-construction, new-construction-homes, homebuilder, home-builder, builder-incentives, quick-move-in-homes, floor-plans, master-planned-communities, active-adult-communities, hoa-fees, property-tax-rate, price-tracking, price-monitoring, incentive-monitoring, market-comparison, housing-market, real-estate, real-estate-data, us-real-estate, usd, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    homepage: https://scavio.dev/lennar-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api
---

# Lennar Homes API - New Home Prices, Communities, Incentives

Read Lennar (lennar.com, the US homebuilder): new-home search across its markets; one community with every plan and homesite; one floor plan; one homesite with its price, previous price, incentive and offer dates; master-planned communities; every market and one market's search filters; each market's current promotion; Lennar's own monthly payment estimate; place suggestions and link lookups. Every answer is what Lennar's public pages show a visitor without an account at the moment of the call, in USD. All 11 endpoints return structured JSON at 1 credit per call.

**Read-only data.** This skill reads the public pages Lennar shows to any visitor and returns them as JSON for analysis. It uses no Lennar account, no saved homes, no tour or contact request, no lead form and no purchase or financing flow.

**The job this skill is for: new-home price tracking and incentive monitoring.** A homesite carries its current `price` and Lennar's `was_price`, the plan's `starting_price`, the offer flag and end date, and the estimated move-in date; a market's promotion carries its offers and legal copy exactly as Lennar shows them. Captured 2026-11-26 (1 credit per call):

| Homesite (`lot_id`) | Community, city (market) | Plan, size | `price` | `was_price` | Plan `starting_price` | Offer / move-in |
|---|---|---|---|---|---|---|
| 22704535134 | Kresston, Montgomery, TX (HOU) | Melrose II, 4 bd, 2,731 sq ft | 384,990 | 424,990 | 424,990 | move-in ready |
| 22704536201 | Kresston, Montgomery, TX (HOU) | Cabot II, 3 bd, 2,386 sq ft | 339,990 | 389,990 | 389,990 | move-in ready |
| 11171720255 | Knightsbridge, Kissimmee, FL (ORL) | Providence, 4 bd, 2,595 sq ft | 436,320 | 471,320 | 466,320 | offer to 2027-11-26; est. move-in 2026-12-14 |
| 3625514040 | Freedom II, Surprise, AZ (PHO) | Aurora Plan 5580, 4 bd, 2,836 sq ft | 648,490 | 678,490 | 599,990 | offer to 2027-11-26; move-in ready |

Market level, the same day: the Dallas / Ft. Worth market (DAL) counted 890 homesites, 372 plans and 60 communities, the lowest-priced homesite a 661 sq ft home in The Alcove Dream, Princeton at 117,499 USD; Phoenix (PHO) had 167 quick move-in homesites with 4+ beds in 19 communities. The DAL promotion read "Black Friday Deals!" with "Up to $20,000 Price Reduction" for a purchase agreement signed between 11/23/26 and 11/29/26 and closed by 12/31/26, as Lennar's legal copy states it. Quote each price with the homesite or plan, the community, USD and the `fetched_at` date, and quote `was_price` as "Lennar's previous price", not as a discount Scavio computed. For resale homes in the same area use `zillow-property-data`, `redfin-property-data` or `realtor-com-property-data`, matched on city or ZIP, beds and size.

Ten limits shape every answer, so say them plainly:
- **1 credit per call, every endpoint.** `credits_used` in every answer says what was spent; a promotion read is still 1 credit. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **Current prices, not a history.** `price` and `was_price` (homesites) and `starting_price` and `was_starting_price` (plans) are what Lennar shows now. Lennar publishes no price history; store each answer with its `fetched_at` to build one.
- **Homes mode mixes two kinds.** `mode: "homes"` lists homesites (`type: "homesite"`) and, where Lennar lists them, floor plans with no homesite released yet (`type: "plan"`); `total` is Lennar's count of that list and `totals` gives communities, plans and homesites. `mode: "communities"` lists communities (`type: "community"`) and master-planned communities (`type: "master_planned"`).
- **Search pages.** 25 a page by default, up to 200; `page * page_size` cannot reach past result 10,000. `is_fallback: true` means Lennar had no exact match for the place and shows its fallback results.
- **Filter codes come from the market.** `features` and `school_district` take the codes `/market` lists for that market (Phoenix: 24 feature codes such as `SSTORY`, `3GAR`, and 20 school districts).
- **Promotions as Lennar words them.** `/promotions` returns the market-wide promotion page's title, offers, incentives and legal copy exactly as Lennar shows them, and the homesites that page lists where it lists any (`[]` on the DAL capture); `promotion` is `null` when none runs.
- **Payment estimate is Lennar's calculator.** `/payment` returns the monthly amounts Lennar's calculator gives (Lennar Mortgage, LLC) for a homesite, a down payment and an interest rate sent as a decimal (`0.065` for 6.5%), with its own legal disclaimer. It is not a loan quote.
- **No personal data.** No sales consultant names. A community's `sales_office` carries the public sales phone and hours only.
- **US only, USD.** There is no `country`, `currency` or `language` input.
- **Response times.** In the captures reads answered in 0.7 to 5.2 seconds and filtered searches in up to 6.4. Set a client timeout of at least 120 seconds and send one request at a time.

Lennar publishes no public developer API or listing feed. This skill reads Lennar's public pages with one Scavio key.

See also: `zillow-property-data`, `redfin-property-data`, `realtor-com-property-data` (resale and new-construction listings by area), `trulia-api` (neighborhood data). Same area only: match on city or ZIP, beds and size, and name the site and date with every number.

## When to trigger

Use this skill when the user asks to:
- Track the price of a Lennar homesite or floor plan, and its previous price, over time
- Monitor Lennar incentives: a market's current promotion, its offers and dates, and homesites flagged with an offer
- Find Lennar new homes in a market, state, city, ZIP area or map box, filtered by beds, baths, price, size, home type, quick move-in or under construction, active adult or lifestyle, features or schools
- Read a Lennar community with every plan and homesite, the HOA fee, the tax rate, the deposit and the sales center hours
- Read a Lennar floor plan with its included features and available homesites, or a master-planned community with its communities
- Compare Lennar markets: plan counts, homesite counts, starting prices and promotions across metros
- Get Lennar's own monthly payment estimate for a homesite at a given down payment and interest rate
- Look up Lennar market codes, place suggestions or what a lennar.com path refers to

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

A call without `SCAVIO_API_KEY` set gets `401` on every endpoint below. The whole
path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit, so 50 credits cover 50 calls (for example a daily price check on 7 homesites for a week, with 1 credit left).

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, plan, resolve and payment answered in under 2 seconds, community, markets, search and suggestions in 1.8-3.3, home, master-planned and market in 3-4.5, promotions in 5.2 and filtered searches in up to 6.4. Set a client timeout of at least 120 seconds, and send one request at a time.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/lennar/search` | Homesites and plans (`mode: "homes"`) or communities and master-planned communities (`mode: "communities"`) for a market, state, city, text, map point with radius or map box; filters, 7 sorts, 1-200 a page, `total`, `totals` and `has_more` | 1 |
| `POST /api/v1/lennar/community` | One community by community number: address, market, price range, size, bed and bath ranges, homesite count, HOA fee, development fee, tax rate, deposit, sales center hours, sales phone, schools, amenities, and every plan with its homesites | 1 |
| `POST /api/v1/lennar/plan` | One floor plan by community number + plan number: beds, baths, size, garages, starting price and previous starting price, tours, floor plan images, included features by category, homesites, other plans | 1 |
| `POST /api/v1/lennar/home` | One homesite by lot id: price, previous price, beds, baths, size, stories, closing cost incentive, estimated move-in date, offer flag and end date, estimated payment where shown, plan and community (HOA fee, tax rate) | 1 |
| `POST /api/v1/lennar/master-planned` | One master-planned community by id: price text, ranges, location and every community in it with base price, price range, homesite count, HOA fee and tax rate | 1 |
| `POST /api/v1/lennar/markets` | Every state and metro market Lennar builds in, with market code and plan count | 1 |
| `POST /api/v1/lennar/market` | One metro market by code: plan count, phone, promotion page path, cities, feature codes and school districts (the search filter codes) | 1 |
| `POST /api/v1/lennar/suggestions` | The places, communities and plans Lennar suggests for a few letters, each with the search input it stands for | 1 |
| `POST /api/v1/lennar/resolve` | What a lennar.com path is (community, plan, home or master-planned) and its ids | 1 |
| `POST /api/v1/lennar/promotions` | A market's current promotion: title, offers, incentives and legal copy as Lennar shows them, and the homesites it lists | 1 |
| `POST /api/v1/lennar/payment` | Lennar's calculator estimate for a homesite at a down payment and interest rate: principal and interest, property tax, insurance, mortgage insurance, HOA and community development fee | 1 |

## Market

US only, USD: 32 states and 104 metro markets on the capture. Market codes are 2-4 letters (`DAL` Dallas / Ft. Worth, `HOU` Houston, `PHO` Phoenix, `ORL` Orlando); `/markets` lists every one. There is no `country`, `currency` or `language` input.

## Price, incentive and community fields

| Field | Meaning |
|---|---|
| `price`, `was_price` (homesite) | Lennar's current price and its previous price as the page shows them; `was_price` is `null` when Lennar shows none |
| `starting_price`, `was_starting_price` (plan) | The plan's starting price and Lennar's previous starting price |
| `price_text` | Lennar's own price wording where it shows text instead of a number |
| `status` | The homesite's status as Lennar gives it (`move_in_ready` on the captures) |
| `hot_of_the_week`, `badge` | Lennar's "hot of the week" flag and badge text ("Featured") |
| `offer_available`, `offer_end_date` | Whether Lennar flags an offer on the homesite, and its end date |
| `closing_cost_incentive`, `incentive_disclaimer` | The closing cost incentive and its disclaimer, where the homesite page shows one |
| `est_move_in_date`, `reserved` | Estimated move-in date and the reserved flag |
| `estimated_monthly_payment` | Lennar's payment figures where a search card shows them ({`principal_and_interest`, `property_tax`, `home_insurance`, `mortgage_insurance`, `hoa_fee`, `community_development_fee`, `loan_type`, `rate_type`, `is_market_rate`}) |
| `hoa_fee`, `hoa_fee_is_monthly`, `development_fee`, `tax_rate_percent`, `deposit_amount` (community) | The community's HOA fee and whether Lennar marks it monthly, development fee, tax rate in percent and deposit amount |
| `promotion.offers[]` | {`header`, `type`, `title`, `incentives`, `legal`, `legal_details`}: each offer as Lennar words it |

- **Previous price, not a computed discount.** Say "price 384,990 USD, Lennar's previous price 424,990 USD"; any difference you compute, label as computed.
- **HOA fee period.** Quote `hoa_fee` with `hoa_fee_is_monthly` as Lennar marks it.

## Workflow

1. **Markets.** `/markets` for every market code, or `/suggestions` (`{"query": "Katy"}`): each suggestion carries `search`, the exact input of `/search` (market, state, city, bounds, beds_min).
2. **Filters.** `/market` with the market code for its feature codes and school districts.
3. **Search.** `/search` with the place, filters and `sort`. Note `totals`, `has_more` and each result's `lot_id`, `comnum` or `mpc_id`.
4. **Detail.** `/home` with `lot_id`, `/community` with `comnum`, `/plan` with `comnum` + `plan_number`, `/master-planned` with `mpc_id`. A lennar.com path goes through `/resolve` first.
5. **Incentives.** `/promotions` with the market code; `/payment` with `lot_id`, `comnum`, `down_payment` and `interest_rate` for Lennar's estimate.
6. **Report.** Each price with the homesite or plan, community, USD and `fetched_at` date; offers as Lennar words them with their dates; no verdict on a home or a market.
7. **Over time:** store each answer with its `fetched_at`; prices, previous prices and promotions change as Lennar updates them, and that stored set is your price and incentive history.

## Parameters

### Search (`/search`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `mode` | string | `homes` | `homes` (homesites and floor plans) or `communities` (communities and master-planned communities) |
| `market` | string | one of | A Lennar market code (`DAL`, `PHO`, `ORL`, `HOU`; `markets[].code`) |
| `state` | string | one of | A two-letter state code (`TX`) |
| `city` | string | one of | A city name (`/market` `cities[].name`, `Katy`), alone or with `market` or `state`; 1-80 characters |
| `text` | string | one of | Lennar's text search, 1-100 characters (matches community and plan names; use suggestions for places) |
| `latitude`, `longitude` | number | one of | A map point (latitude 17 to 72, longitude -180 to -60); they go together |
| `radius` | integer | none | With latitude + longitude: 1-100 miles |
| `bounds` | object | one of | A map box {`north`, `east`, `south`, `west`} (a suggestion's `search.bounds`) |
| `beds_min`, `baths_min` | integer | none | 1-6 |
| `price_min`, `price_max` | integer | none | USD |
| `sqft_min`, `sqft_max` | integer | none | Square feet |
| `home_types` | list | none | Any of `single_family`, `multi_family`, `next_gen`, `single_story` |
| `community_types` | list | none | `active_adult` (55+) or `lifestyle` |
| `availability` | list | none | Homesite availability: `quick_move_in` (move-in ready), `under_construction`, `coming_soon`, `future_release` |
| `community_status` | list | none | `active`, `coming_soon` or `sold_out` |
| `features` | list | none | Up to 10 feature codes as `/market` gives them (`SSTORY`, `3GAR`, `SWIMMING_POOL`) |
| `school_district` | string | none | A school district code as `/market` gives it |
| `school_types` | list | none | `public`, `private`, `charter` |
| `school_levels` | list | none | `elementary`, `middle`, `high` |
| `school_rating` | string | none | Lennar's school rating filter: `A`, `B`, `C` or `D` |
| `sort` | string | `featured` | `featured`, `newest`, `distance` (needs latitude + longitude), `price_asc`, `price_desc`, `sqft_asc`, `sqft_desc` |
| `page` | integer | 1 | 1-1000 |
| `page_size` | integer | 25 | 1-200 |

One place is required: `market`, `state`, `city`, `text`, `latitude` + `longitude`, or `bounds`.

### Detail, markets, suggestions, resolve, promotions, payment

| Endpoint | Parameters |
|---|---|
| `/community` | `comnum` (required, digits, `22704`; `community.comnum`) |
| `/plan` | `comnum` and `plan_number` (both required; letters and digits, `4504` or `C090`; `plans[].plan_number`) |
| `/home` | `lot_id` (required, 6-16 letters and digits, `11171720255`; `homes[].lot_id`) |
| `/master-planned` | `mpc_id` (required integer, `1916`; `communities[].mpc_id` in a community search) |
| `/markets` | none (send `{}`) |
| `/market` | `market` (required market code, `PHO`) |
| `/suggestions` | `query` (required, 2-80 characters: the start of a city, ZIP, region, community or plan name); `market` (favor one market); `limit` 1-20 (default 10) |
| `/resolve` | exactly one of `url` (a lennar.com community, plan, home or master-planned page) or `path` (`/new-homes/...`) |
| `/promotions` | `market` (required market code, `DAL`) |
| `/payment` | `lot_id`, `comnum`, `down_payment` (USD) and `interest_rate` (a decimal above 0 and up to 1: `0.065` for 6.5%), all required |

## Examples

### One homesite: price, previous price, offer and move-in date

```bash
curl -X POST https://api.scavio.dev/api/v1/lennar/home \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"lot_id": "11171720255"}'
```

Captured `data` (2026-11-26; `overview` shortened; `image`, `url`, `virtual_tour_url` and the plan and community `url` dropped):

```json
{
  "lot_id": "11171720255",
  "homesite_number": "0255",
  "name": "Providence",
  "status": "move_in_ready",
  "address": "5156 Worchester Drive",
  "latitude": 28.260456,
  "longitude": -81.477325,
  "price": 436320,
  "was_price": 471320,
  "price_text": null,
  "currency": "USD",
  "beds": 4,
  "baths": 2,
  "half_baths": 1,
  "garages": 2,
  "stories": 2,
  "sqft": 2595,
  "closing_cost_incentive": null,
  "incentive_disclaimer": null,
  "est_move_in_date": "2026-12-14",
  "reserved": false,
  "hot_of_the_week": false,
  "badge": null,
  "offer_available": true,
  "offer_end_date": "2027-11-26",
  "tourable": true,
  "overview": "This new two-story home is a family-friendly haven. ...",
  "estimated_monthly_payment": null,
  "plan": {"plan_number": "2575", "name": "Providence", "starting_price": 466320},
  "community": {"comnum": "11171", "name": "Knightsbridge", "city": "Kissimmee", "market": "ORL", "hoa_fee": 88, "tax_rate_percent": 1.48}
}
```

### Homesites in a market, lowest price first

```bash
curl -X POST https://api.scavio.dev/api/v1/lennar/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"market": "DAL", "sort": "price_asc"}'
```

Captured `data` (2026-11-26; `homes` cut to the 1st and 3rd of 25, `image` and `url` fields and `notes` dropped):

```json
{
  "mode": "homes",
  "market": "DAL",
  "sort": "price_asc",
  "page": 1,
  "page_size": 25,
  "total": 890,
  "totals": {"communities": 60, "plans": 372, "homesites": 890},
  "is_fallback": false,
  "count": 25,
  "has_more": true,
  "homes": [
    {"type": "homesite", "lot_id": "29114951L30", "status": "move_in_ready", "address": "1036 Robin Hill Lane", "beds": 1, "baths": 2, "half_baths": 0, "sqft": 661, "price": 117499, "was_price": null, "price_text": null, "currency": "USD", "badge": null, "hot_of_the_week": true, "offer_available": false, "offer_end_date": null, "estimated_monthly_payment": null, "plan": {"plan_number": "1031", "name": "Henley", "starting_price": 114999}, "community": {"comnum": "29114", "name": "The Alcove Dream", "city": "Princeton", "market": "DAL"}},
    {"type": "homesite", "lot_id": "29122901E04", "status": "move_in_ready", "address": "315 Kola Road", "beds": 2, "baths": 2, "half_baths": 0, "sqft": 771, "price": 148999, "was_price": 156999, "price_text": null, "currency": "USD", "badge": null, "hot_of_the_week": false, "offer_available": false, "offer_end_date": null, "estimated_monthly_payment": null, "plan": {"plan_number": "1906", "name": "Brayton", "starting_price": 152999}, "community": {"comnum": "29122", "name": "Broadview Collection", "city": "Princeton", "market": "DAL"}}
  ]
}
```

Quick move-in homes with 4+ beds in Phoenix: `{"market": "PHO", "availability": ["quick_move_in"], "beds_min": 4}` (167 homesites in 19 communities; the first, lot 3625514040 in Freedom II, Surprise, at 648,490 USD, was 678,490 USD, with `estimated_monthly_payment` {"principal_and_interest": 2706.26, "property_tax": 270.2, "home_insurance": 81.06, "mortgage_insurance": 0, "hoa_fee": 205, "loan_type": "C", "rate_type": "Fixed"}).

### A market's current promotion

```bash
curl -X POST https://api.scavio.dev/api/v1/lennar/promotions \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"market": "DAL"}'
```

Captured `data` (2026-11-26; `promo_url`, `notes` and the long `legal` texts dropped):

```json
{
  "market": {"code": "DAL", "name": "Dallas / Ft. Worth", "state": "TX"},
  "promotion": {
    "title": "Black Friday Deals!",
    "offers": [
      {
        "header": "Limited-Time Deals on New Homes",
        "type": "AND Promotion",
        "title": "Up to $20,000 Price Reduction¹",
        "incentives": ["Up to 1/2 Off Homesite Premium²", "Move-In Ready Appliance Package³ (Includes Washer and Dryer)"],
        "legal": "Offers available when you sign a purchase agreement on a select new home in the greater Dallas-Fort Worth area between 11/23/26 and 11/29/26 and closes and fully funds by 12/31/26."
      }
    ],
    "homesites": []
  }
}
```

### Community, plan, master-planned, markets, payment

- `/community` `{"comnum": "22704"}`: Kresston, Montgomery, TX (Houston market), NextGen and Single Family, 339,990 to 522,990 USD, 48 homesites, 7 plans from Cabot II (389,990 USD, 2 homesites) to Oak Hill IV (522,990 USD), `hoa_fee` 100 with `hoa_fee_is_monthly` false, `tax_rate_percent` 3, `deposit_amount` 100, sales center hours by day, amenities Swimming Pool and Community Center.
- `/plan` `{"comnum": "22704", "plan_number": "4504"}`: Melrose II, 4 beds, 3 baths, 2,731 sq ft, 2 garages, from 424,990 USD, 2 homesites (384,990 USD was 424,990; 410,490 USD was 435,490), included features in 8 categories (Kitchen, Owners Suite, Interior, Exterior, Energy Efficiency ...).
- `/master-planned` `{"mpc_id": 1916}`: Samara, League City, TX, "$256,990 - $699,990" across 11 communities, each with base price, homesite count, HOA fee (95.83) and tax rate (3.02%).
- `/markets` `{}`: 104 markets in 32 states (Phoenix PHO 263 plans, Birmingham BRM 89 ...). `/market` `{"market": "PHO"}`: 263 plans, 14 cities, 24 feature codes, 20 school districts.
- `/payment` `{"lot_id": "11171720255", "comnum": "11171", "down_payment": 40000, "interest_rate": 0.065}`: principal and interest 2,505.01, property tax 536.67 (rate 0.01476), home insurance 109.08, mortgage insurance 257.61, HOA 88, community development fee 225.33 USD a month, down payment 9.17%, with Lennar Mortgage, LLC's disclaimer.
- `/suggestions` `{"query": "Katy"}`: 10 suggestions (Katy Area, TX region; Katy, TX city with `search` {"market": "HOU", "state": "TX", "city": "Katy", "bounds": ...}; ZIP 77493; "3+ bed homes Katy, TX"; "Katy, TX homes under $400K"; master-planned Sunterra Lakes and Sofi Lakes). `/resolve` `{"path": "/new-homes/texas/houston/montgomery/kresston/melrose-ii"}`: `type` plan, `ids` {"comnum": "22704", "plan_number": "4504"}.

### Python

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def lennar(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/lennar/{endpoint}", headers=HEADERS, json=body, timeout=120)
    r.raise_for_status()
    return r.json()

# Move-in ready homes with 4+ beds in Phoenix (1 credit)
s = lennar("search", {"market": "PHO", "availability": ["quick_move_in"], "beds_min": 4, "sort": "price_asc"})["data"]
print(s["totals"])
for h in s["homes"][:10]:
    print(h["lot_id"], h["community"]["name"], h["price"], "was", h["was_price"], "offer", h["offer_available"], h["offer_end_date"])

# The market's promotion (1 credit)
p = lennar("promotions", {"market": "PHO"})["data"]["promotion"]
if p:
    print(p["title"], [o["title"] for o in p["offers"]])

# Store each answer with fetched_at: that stored set is your price and incentive history.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Search, suggestions, promotions and payment answers carry `notes`.

- **search** - `mode`, the place echoed (`market`, `state`, `city`, `text`, `latitude`, `longitude`, `bounds` as sent), `sort`, `page`, `page_size`, `total`, `totals` {`communities`, `plans`, `homesites`}, `is_fallback`, `count`, `has_more`, `homes[]` or `communities[]`, `notes`.
- **homes[]** - type homesite: `lot_id`, `status`, `address`, `beds`, `baths`, `half_baths`, `sqft`, `price`, `was_price`, `price_text`, `currency`, `badge`, `hot_of_the_week`, `offer_available`, `offer_end_date`, `estimated_monthly_payment`, `image`, `url`, `plan` {`plan_number`, `name`, `starting_price`, `url`}, `community` {`comnum`, `name`, `city`, `market`}; type plan: `plan_number`, `name`, `status`, `beds`, `baths`, `half_baths`, `sqft`, `starting_price`, `price_text`, `available_homesites`, `active_adult`, `next_gen`, `image`, `url`, `community`.
- **communities[]** - type community: `comnum`, `name`, `status`, `badge`, `brand`, `types`, `base_price`, `price_text`, `bed_range`, `bath_range`, `sqft_range`, `address`, `zip`, `latitude`, `longitude`, `city`, `market`, `url`; type master_planned: `mpc_id`, `name`, `status`, `price_text`, `search_price_text`, ranges, `city`, `market`, `url`, `communities[]` {`comnum`, `base_price`}.
- **community** - `comnum`, `name`, `status`, `brand`, `types`, `address`, `city`, `state`, `zip`, `latitude`, `longitude`, `market` {`code`, `name`}, `master_planned`, `base_price`, `price_range` {`min`, `max`}, `price_text`, `currency`, `sqft_range`, `bed_range`, `bath_range`, `stories_range`, `homesites_count`, `tourable`, `hoa_fee`, `hoa_fee_is_monthly`, `development_fee`, `tax_rate_percent`, `deposit_amount`, `overview`, `hours[]` {`day`, `opening`, `closing`, `by_appointment`}, `sales_office` {`phone`, `time_zone`, `phone_hours`}, `schools[]` {`name`, `grades`, `district`, `public`}, `amenities`, `image`, `url`, `plans[]` {`plan_number`, `name`, `status`, `beds`, `baths`, `half_baths`, `sqft`, `garages`, `starting_price`, `price_text`, `next_gen`, `active_adult`, `available_homesites`, `url`, `homesites[]` {`lot_id`, `status`, `address`, `beds`, `baths`, `half_baths`, `sqft`, `price`, `was_price`, `est_move_in_date`, `hot_of_the_week`, `url`}}.
- **plan** - `plan_number`, `name`, `status`, `beds`, `baths`, `half_baths`, `sqft`, `garages`, `starting_price`, `was_starting_price`, `price_text`, `currency`, `next_gen`, `available_homesites`, `tourable`, `virtual_tour_url`, `video_tour_url`, `overview`, `image`, `floor_plans[]` {`name`, `image`}, `included_features[]` {`category`, `items`}, `homesites[]` {`lot_id`, `status`, `address`, `sqft`, `price`, `was_price`, `url`}, `other_homes[]` {`name`, `starting_price`, `available_homesites`, `url`}, `community`, `url`.
- **home** - `lot_id`, `homesite_number`, `name`, `status`, `address`, `latitude`, `longitude`, `price`, `was_price`, `price_text`, `currency`, `beds`, `baths`, `half_baths`, `garages`, `stories`, `sqft`, `closing_cost_incentive`, `incentive_disclaimer`, `est_move_in_date`, `reserved`, `hot_of_the_week`, `badge`, `offer_available`, `offer_end_date`, `tourable`, `virtual_tour_url`, `overview`, `estimated_monthly_payment`, `image`, `url`, `plan`, `community` {`comnum`, `name`, `city`, `market`, `hoa_fee`, `tax_rate_percent`, `url`}.
- **master-planned** - `mpc_id`, `name`, `status`, `brand`, `overview`, `price_text`, `search_price_text`, `currency`, `bed_range`, `bath_range`, `sqft_range`, `latitude`, `longitude`, `city`, `market`, `url`, `communities[]` {`comnum`, `name`, `status`, `types`, `base_price`, `price_range`, `homesites_count`, `hoa_fee`, `tax_rate_percent`, `url`}.
- **markets** - `state_count`, `market_count`, `states[]` {`code`, `name`, `markets[]` {`code`, `name`, `plan_count`, `latitude`, `longitude`, `url`}}. **market** - `code`, `name`, `state` {`code`, `name`}, `plan_count`, `latitude`, `longitude`, `phone`, `promo_url`, `url`, `cities[]` {`name`, `url`}, `features[]` {`name`, `code`}, `school_districts[]` {`name`, `code`}.
- **suggestions** - `query`, `market`, `count`, `suggestions[]` {`category`, `type`, `text`, `search`, `path`, `url`}, `notes`. **resolve** - `path`, `type`, `page_type`, `ids` {`comnum`, `plan_number`, `lot_id`, `mpc_id`}.
- **promotions** - `market` {`code`, `name`, `state`}, `promo_url`, `promotion` {`title`, `legal`, `offers[]` {`header`, `type`, `title`, `incentives`, `legal`, `legal_details`}, `homesites[]` {`lot_id`, `community`, `comnum`, `city`, `plan`, `plan_number`, `address`, `zip`, `beds`, `baths`, `sqft`, `price`, `was_price`, `status`, `est_move_in_date`, `url`}} or `null`, `notes`.
- **payment** - `lot_id`, `comnum`, `input` {`down_payment`, `interest_rate`}, `currency`, `estimate` {`principal_and_interest`, `property_tax`, `property_tax_rate`, `home_insurance`, `home_insurance_rate`, `mortgage_insurance`, `mortgage_insurance_rate`, `hoa_fee`, `community_development_fee`, `down_payment`, `down_payment_percent`, `interest_rate`, `legal_disclaimer`}, `notes`.

## Guardrails

- Name it "Lennar (lennar.com, the US homebuilder)" on first mention, "Lennar" after that.
- Prices: USD with the homesite (`lot_id`) or plan, the community and the `fetched_at` date ("Melrose II homesite 22704535134 in Kresston: 384,990 USD, Lennar's previous price 424,990 USD, fetched Nov 26, 2026"). `was_price` is Lennar's previous price as shown; never call a difference a saving Lennar offers unless Lennar's own copy says so.
- Promotions: quote offers, incentives, dates and legal copy as Lennar words them, with the market and the `fetched_at` date; say that offers apply on select homes under Lennar's own terms. Never restate an offer as a guarantee.
- Payment estimate: "Lennar's calculator estimate (Lennar Mortgage, LLC)" with the down payment and rate used; never present it as a loan offer, a rate quote or advice.
- No personal data: never name a sales consultant; use the community's public sales phone and hours only.
- Fair housing: describe communities with the data as Lennar gives it; do not characterize an area by who lives there, and do not steer anyone toward or away from an area.
- Descriptive only: no commentary on Lennar's business, pricing practices or policies, and no ranking of homes or communities as a recommendation.
- Do not republish Lennar photos, floor plan images or descriptions in bulk. Write lennar.com as plain text and cite lot ids, community numbers and capture dates rather than linking Lennar pages.
- Terms: Scavio keeps no copy: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. It uses no account and no lead, tour, purchase or financing flow. Lennar's terms of use restrict automated access to its sites and linking to them; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, previous prices, offers, lot ids, community numbers or payment figures. Only return what the API returned, with the `fetched_at` time.
- Not available: price history (store answers over time), resale homes, reviews or ratings, sales consultant names, contracts, reservations or financing applications.

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without a place ("Send a place: market (a market code), state, city, text, latitude + longitude, or bounds (suggestions returns each place's search input)."); latitude without longitude ("latitude and longitude go together."); `radius` alone ("radius (miles) needs latitude and longitude."); `sort: "distance"` without a point ("sort distance needs latitude and longitude."); bad bounds ("bounds: north must be above south and east above west."); a `_min` above its `_max` ("price_min must not be above price_max."); paging too deep ("page * page_size reaches past result 10000; narrow the search instead."); a bad market code ("market must be a Lennar market code (2-4 letters, e.g. DAL, PHO, ORL: markets[].code from the markets endpoint)."); a bad `comnum`, `plan_number` or `lot_id` ("lot_id must be a Lennar homesite lot id (letters and digits, e.g. 22704535134: homes[].lot_id)."); a feature code with other characters; a list value outside its list; `/resolve` with neither or both of `url` and `path`, or a link that is not a lennar.com new-homes page; `/payment` with the rate as a percent ("interest_rate must be a decimal, not a percent: 0.065 for 6.5% (values above 1 are refused).") or without `down_payment` ("down_payment is required (USD)."); suggestions under 2 characters ("query must be at least 2 characters.").
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "Lennar has no community <comnum>. Check comnum (community.comnum in search answers).", "Lennar has no plan <plan_number> in community <comnum>. ...", "Lennar has no homesite <lot_id>. Check lot_id (homes[].lot_id in search answers); a sold homesite leaves the site.", "Lennar has no master-planned community <mpc_id>. ...", "Lennar has no market <code>. The markets endpoint lists every market code.", "Lennar found nothing for this search.", "Lennar suggests nothing for this text.", "Lennar's promotion page for <code> is no longer online.", "Lennar gives no payment estimate for homesite <lot_id> in community <comnum>. Check lot_id and comnum (the home endpoint gives both).". A sold homesite leaves the site, so a lot id that worked before can turn into a `404`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api).
- `502` means Lennar data was temporarily unavailable ("Lennar is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means the service is busy ("Lennar is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.98.0
npm install scavio@0.99.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: homes } = await scavio.lennar.search({ market: "PHO", availability: ["quick_move_in"], beds_min: 4 });
const { data: community } = await scavio.lennar.community({ comnum: "22704" });
const { data: plan } = await scavio.lennar.plan({ comnum: "22704", plan_number: "4504" });
const { data: home } = await scavio.lennar.home({ lot_id: "11171720255" });
const { data: mpc } = await scavio.lennar.masterPlanned({ mpc_id: 1916 });
const { data: markets } = await scavio.lennar.markets({});
const { data: market } = await scavio.lennar.market({ market: "PHO" });
const { data: places } = await scavio.lennar.suggestions({ query: "Katy" });
const { data: link } = await scavio.lennar.resolve({ path: "/new-homes/texas/houston/montgomery/kresston/melrose-ii" });
const { data: promo } = await scavio.lennar.promotions({ market: "DAL" });
const { data: payment } = await scavio.lennar.payment({ lot_id: "11171720255", comnum: "11171", down_payment: 40000, interest_rate: 0.065 });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.lennar.search(...)`, `community`, `plan`, `home`, `master_planned`, `markets`, `market`, `suggestions`, `resolve`, `promotions` and `payment`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 11 endpoints as tools: `search_lennar`, `get_lennar_community`, `get_lennar_plan`, `get_lennar_home`, `get_lennar_master_planned`, `get_lennar_markets`, `get_lennar_market`, `get_lennar_suggestions`, `resolve_lennar_url`, `get_lennar_promotions` and `get_lennar_payment`. Lennar is opt-in: add `lennar` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.98.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,lennar"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/lennar-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [community](https://scavio.dev/docs/lennar-community?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [plan](https://scavio.dev/docs/lennar-plan?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [home](https://scavio.dev/docs/lennar-home?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [master-planned](https://scavio.dev/docs/lennar-master-planned?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [markets](https://scavio.dev/docs/lennar-markets?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [market](https://scavio.dev/docs/lennar-market?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [suggestions](https://scavio.dev/docs/lennar-suggestions?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [resolve](https://scavio.dev/docs/lennar-resolve?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [promotions](https://scavio.dev/docs/lennar-promotions?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api), [payment](https://scavio.dev/docs/lennar-payment?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api). Overview: [Lennar API](https://scavio.dev/lennar-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=lennar-homes-api).
