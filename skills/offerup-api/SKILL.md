---
name: offerup-api
description: OfferUp API for OfferUp (offerup.com, the US local marketplace for buying and selling used items, cars and trucks) - used asking prices by city - search OfferUp by keyword around any US ZIP code (required) with a radius, and location.resolved says which area OfferUp used (98101 read Seattle, 60601 Chicago, 75201 Dallas), so the same item's asking prices can be read metro by metro; sorted by best match, newest, distance or price, and for vehicles by newest model year or lowest mileage, filtered by asking price, condition and category, and in Cars & Trucks by dealer or private seller, make, model year and maximum mileage; filters_not_applied lists any filter OfferUp did not apply to the feed; 44-50 listings a page up to page 50, no total count, promoted listings marked sponsored; any OfferUp category by slug or id around a ZIP; one listing with asking price, original price, firm price, condition, posted date, description (phone numbers, emails and VIN-like codes removed), photos, category attributes, vehicle details (make, model, year, mileage, trim, drivetrain; no VIN), city and state and the seller's public numbers (seller type, rating, items sold, joined, response time; a name only for dealer and business accounts); a seller's public profile with rating tags, followers and the first 20 listings, plus website and opening hours for dealers and businesses; the category tree (14 top-level, 151 in all). 5 endpoints, 1 credit per call (a listing that needs a second fetch is 2). Asking prices, not sold prices; OfferUp publishes no sold listings; no shipping (OfferUp listings are local pickup since 2025), no search suggestions, no total count, no seller names for individuals, no VINs, no price history.
version: 1.0.0
tags: offerup, offerup-com, offerup-api, offerup-prices, offerup-price-check, offerup-used-prices, offerup-listings, offerup-search, offerup-cars, offerup-used-cars, offerup-trucks, offerup-dealers, offerup-seller, offerup-categories, offerup-local, offerup-seattle, offerup-los-angeles, offerup-chicago, offerup-dallas, used-prices, used-prices-by-city, asking-prices, local-marketplace, local-classifieds, used-cars, used-iphone-prices, resale, reseller, flipping, secondhand, price-research, price-comparison, marketplace, us-marketplace, usd, langchain, crewai, ai-agents, structured-data, json
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 240
    throttle: 1
    homepage: https://scavio.dev/offerup-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api
---

# OfferUp API - Used Prices by City, Listings, Cars

Read OfferUp (offerup.com, the US local marketplace for buying and selling used items, cars and trucks) around any US ZIP code: search, one category, one listing in full, a seller's public profile and the category tree. Every answer is what OfferUp's public pages show a visitor without an account at the moment of the call. All 5 endpoints return structured JSON at 1 credit per call (a listing that needs a second fetch is 2).

**Read-only data.** This skill reads the public pages OfferUp shows to any visitor and returns them as JSON for analysis. It uses no OfferUp account, no messaging, no offers, no saved searches and no purchase flow.

**The job this skill is for: OfferUp used asking prices by city.** What the same used item asks on OfferUp in different US metros, one `/search` per ZIP, next to its new price at Amazon and Walmart and its sold prices on Mercari for a sold baseline. Captured 2026-11-25: `/search` `{"q": "iphone 15", "zip": "98101"}` resolved to Seattle with a 30-mile radius and returned 47 listings; 11 titles named an iPhone 15 Pro Max 256GB, 3 of them at placeholder asks (0.01 and 5), and the other 8 asked 549 to 649.99 USD (median 572.50, arithmetic on that page). Run the same body with another metro's ZIP for the next row. OfferUp prices are **asking** prices: never call them sold prices, sale prices or market value.

Ten limits shape every answer, so say them plainly:
- **1 credit per call; a listing can be 2.** Search, category, categories and seller cost 1. A listing costs 1, or 2 when it had to be read a second way (a note in the answer says so); `credits_used` is the truth, and the balance check holds 2 for a listing call. A not-found (`404`) is charged; a refused input (`400`) and an upstream failure (`502`, `503`) are not.
- **A ZIP is required, and OfferUp names the area.** Search and category need `zip` (a 5-digit US ZIP). Results are around that ZIP's centre; `location.resolved` is the place OfferUp names for it (98101 Seattle, 60601 Chicago, 90012 Los Angeles, 75201 Dallas in the captures) and `location.radius_miles` the radius it applied. Listings come from nearby cities too (the Seattle page had Renton, Everett, Tacoma and Bellevue): report the resolved area and radius with every number. An unknown ZIP is a `400`, not charged.
- **Asking prices only, no sold data.** `price` is the seller's asking price as the listing shows it (buyers and sellers often agree a different price in person). OfferUp publishes no sold listings or sold prices. For a sold baseline use Mercari (`mercari-api`, `status: "sold"`), labelled as Mercari's.
- **No shipping.** OfferUp listings are local pickup: OfferUp's help center ("Nationwide shipping ending", 2025) says it removed the shipping option from all existing items. No shipping fields are returned; every price is a local price.
- **Placeholder and payment-plan asks.** Some tiles carry a price far below the item's other asks: 0.01, 1 and 5 on iPhone listings (some titles advertise a down payment), and 2,500 or 3,000 on 2022-2024 Tacomas whose other listings asked 24,488 to 56,019. Read the title (or the listing) and drop asks like these before you summarise, and say how many you dropped. `call_for_price` `true` means no price (`price` `null`).
- **Keyword matches are loose.** A search returns everything OfferUp matches: cases, screen protectors, trades and other models next to the phone, and under `newest` even unrelated items (the Chicago `couch` page led with sports tickets). Match the same item on title evidence (model + storage, year + mileage band) and drop bundles, "for parts" and trade posts.
- **No total count.** 44-50 listings a page, up to page 50; `count` is this page, `has_more` is `true` while a page carries listings. Never report a total from OfferUp; say how many pages you read.
- **Sort and filters as applied.** `sort` in the answer is the order OfferUp applied (default `best_match` on search, `newest` on category; category feeds have no `best_match`). Send the same `sort` on every page and in every metro you compare. `filters_applied` echoes what you sent; `filters_not_applied` lists any filter OfferUp did not apply to this feed (vehicle filters on a non-vehicle search), and the results are without it.
- **Vehicle filters live in Cars & Trucks.** `seller_type` (`dealer` or `private`), `make`, `year_min`, `year_max` and `max_mileage` are OfferUp's vehicle filters. `seller_type` on a search limits it to Cars & Trucks (`category_id` `5.1`, said in a note); with any other `category_id` it is a `400`.
- **Private sellers stay private.** No seller names (a dealer or business account's name only), usernames, avatars, phone numbers, emails, street addresses, coordinates or VINs are returned; phone numbers, emails and VIN-like codes in titles and descriptions read "[removed]". Locations are city and state. Nothing is cached or kept: store each answer with its `fetched_at` for your own series.

OfferUp publishes no public API for reading listings, prices, sellers or categories. OfferUp for Business (OfferUp Motors, storefronts) is seller-side tooling that syncs a dealer's own inventory into OfferUp, and OfferUp's Shopify app lists a merchant's own products on it; neither reads the marketplace. This skill reads the public search, category, listing and profile pages with one Scavio key. Other vendors offer OfferUp data tools; this skill reads OfferUp's own public pages.

OfferUp Inc. is based in Bellevue, Washington, and was founded in 2011. OfferUp's about page says "40M+ active users nationwide" (undated; read November 2026). Quote it with that source, never from the samples.

See also: for the same item's new price use `amazon-product-data` (Amazon) and `walmart-product-data` (Walmart); for sold prices use `mercari-api` (Mercari US, `status: "sold"`) and, for apparel, `poshmark-api`; for live listings elsewhere use `ebay-product-data` (live asks only: eBay sold listings are not available). Same item only: model, storage or edition, and for vehicles year and mileage band, must match in both titles; show each price with its marketplace, metro and date.

## When to trigger

Use this skill when the user asks to:
- Read what a used item asks on OfferUp around a US ZIP code or city
- Put the same item's OfferUp asking prices in two or more US metros side by side
- Compare OfferUp asking prices with the new price at Amazon or Walmart, or with Mercari sold prices
- Search OfferUp used cars and trucks by make, model year, mileage and dealer or private seller around a ZIP
- Browse one OfferUp category (furniture, cars-and-trucks, cell phones ...) around a ZIP, newest first or by price
- Read one OfferUp listing in full: asking price, original price, condition, posted date, photos, attributes, vehicle details
- Read a dealer's or seller's public OfferUp profile: rating, rating tags, items sold, joined, response time, first 20 listings, dealer website and hours
- List OfferUp's category tree with slugs and ids

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Every call in this skill costs 1 credit (a listing that needs a second fetch costs 2), so 50 credits cover up to 50 calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
Paid plans start with Hobby at $15 per month for 3,000 credits; on Growth,
1,000 credits cost $1.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`. In the captures, search and category took 2 to 5 seconds, categories about 4, and listing and seller 6 to 7. Allow a client timeout of at least 240 seconds: a busy moment can queue a request.

| Endpoint | What it returns | Credits |
|---|---|---|
| `POST /api/v1/offerup/search` | Listings for keywords around a ZIP: asking price, city, state, sponsored flag, firm price, vehicle miles; resolved area and radius; sorts, price / condition / category filters and the Cars & Trucks filters; 44-50 a page, `has_more`, no total | 1 |
| `POST /api/v1/offerup/listing` | One listing by id or link: asking and original price, firm, status, condition, posted / updated dates, description, photos, category, attributes, vehicle details (no VIN), city, state, local pickup, the seller's public numbers | 1, or 2 when it needs a second fetch |
| `POST /api/v1/offerup/category` | One OfferUp category by slug or id around a ZIP, same tiles, filters and paging as search (no `best_match` order) | 1 |
| `POST /api/v1/offerup/categories` | OfferUp's category tree: 14 top-level categories and their children, 151 in all, with slug, id and url | 1 |
| `POST /api/v1/offerup/seller` | A seller's public profile by id: seller type, rating, rating tags, items sold and bought, followers, joined, city, state, response time, last active, verified badges, the first 20 listings; dealers and businesses also name, website and opening hours | 1 |

## Market

US only: every answer carries `market` {`country` `us`, `currency` `USD`}. There is no `country` input. The area comes from `zip` (and `radius`), not from a market.

## Location, radius and paging

| Field / input | Meaning |
|---|---|
| `zip` (input) | Required on search and category. A 5-digit US ZIP (`98101`; ZIP+4 accepted). Results are around its centre |
| `radius` (input) | Miles: 5, 10, 20, 25, 30, 50, 80, 100, 200 or 1500. Goods feeds offer 5, 10, 20, 30 (default), 50 and 80; vehicle feeds 5, 25, 80 (default), 100, 200 and 1500. When OfferUp applies another radius a note says so |
| `location` (output) | {`zip`, `requested`, `resolved` (the place OfferUp names for the ZIP), `radius_miles` (the radius it applied)} |
| `page` (input) | 1-50 (default 1). 44-50 listings a page |
| `has_more`, `count` (output) | `has_more` is `true` while a page carries listings (and the page is below 50); `count` is this page. No total |

- **Metro by metro:** keep `q`, `sort`, filters and `radius` identical and change only `zip`. Report each metro as its `location.resolved` with `radius_miles`, the number of listings kept and dropped, and the date.
- **Tiles are short:** a result tile has no posted date, condition or seller. Read `/listing` for those (one call each), or filter by `condition` in the search.
- **Sponsored:** `sponsored` `true` marks a promoted OfferUp listing placed in the results (5 of 47 on the Seattle page). Keep or drop them consistently and say which.
- **Same item twice:** two listing ids can carry the same title, price and mileage (two 2025 Tacomas in Richardson at 30,472 USD and 24,740 miles in the Dallas capture). Dedupe by `listing_id`, and flag lookalike rows instead of counting them as two independent asks.

## Cars and trucks

Cars & Trucks is category `5.1` (slug `cars-and-trucks`) under Vehicles (`5`). Vehicle searches add two sorts (`newest_year`, `lowest_mileage`) and five filters:

| Input | Values |
|---|---|
| `seller_type` | `dealer` (OfferUp's verified dealers) or `private` (private sellers), as OfferUp labels them |
| `make` | The make as OfferUp lists it (Toyota, Ford, Honda ...; 61 makes) |
| `year_min`, `year_max` | Model years 1936-2027 |
| `max_mileage` | One of OfferUp's steps: 0, 25000, 50000, 75000, 100000, 125000, 150000, 175000, 200000 |

Tiles carry `vehicle_miles`. `/listing` adds `vehicle` {`make`, `model`, `year`, `mileage`, `trim`, `body`, `color`, `drivetrain`, `fuel`, `transmission`, `cylinders`, `mpg_city`, `mpg_highway`} and the category `attributes`; no VIN and no dealer stock number is ever returned. Compare vehicles by year range and mileage band in one metro, as asks, never as valuations.

## Workflow

1. **One metro.** `/search` with `q`, `zip` and an explicit `sort` (`best_match`, or `price_low` for the low end). Read `location.resolved` and `radius_miles`, then check `filters_not_applied` and `notes`.
2. **Clean the page.** Keep listings whose titles match the item (model + storage or edition; year + mileage band for vehicles); drop accessories, bundles, trades, "for parts", placeholder asks (0.01, 1, 5) and payment-plan figures; dedupe by `listing_id`. Count what you kept and dropped.
3. **More listings.** Raise `page` while `has_more` is `true` and the matches keep coming; stop when a page adds no matching titles. Say how many pages you read.
4. **More metros.** Repeat steps 1-3 with each metro's ZIP and the same body. Show each metro's kept count, low, high and median ask, with the resolved area, radius and date.
5. **Baselines.** New price: `amazon-product-data` and `walmart-product-data` for the same model and storage. Sold price: `mercari-api` `/search` with `status: "sold"`. Label each number with its marketplace and whether it is an ask, a new retail price or a sold price.
6. **One listing.** `/listing` with `listing_id` (`items[].listing_id`) or `url` for condition, posted date, attributes, vehicle details and the seller's public numbers.
7. **A dealer.** `/seller` with `seller_id` (a listing's `seller.id`) for the profile and its first 20 listings.
8. **A category.** `/categories` once for slugs and ids, then `/category` with `category` and `zip` (default `newest`).
9. **Price series:** there is no history. Store each answer with its `fetched_at`; that stored set is your record.

## Parameters

### Search (`/search`) and category (`/category`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `q` | string | required (search) | Keywords, up to 200 chars |
| `category` | string | required (category) | A category slug (`furniture`, `cars-and-trucks`) or id (`2.1`) from `/categories`. An unknown slug is a charged `404`; an unknown id is a `400` |
| `zip` | string or integer | required | A 5-digit US ZIP code |
| `radius` | integer | feed default | Miles: 5, 10, 20, 25, 30, 50, 80, 100, 200, 1500 (see above) |
| `page` | integer | 1 | 1-50 |
| `sort` | string | `best_match` (search), `newest` (category) | `best_match` (search only), `newest`, `distance`, `price_low`, `price_high`; vehicle feeds also `newest_year`, `lowest_mileage` |
| `min_price`, `max_price` | integer | none | Asking price bounds, whole USD, 0-1,000,000 |
| `condition` | string or list | none | One, a list or comma-separated: `new`, `open_box`, `refurbished`, `used`, `for_parts`, `other` |
| `category_id` | string | none | Search only: `categories[].id` or `children[].id` (`2.1` Furniture, `5.1` Cars & Trucks) |
| `seller_type` | string | none | Cars & Trucks: `dealer` or `private` |
| `make` | string | none | Vehicles: Toyota, Ford, Honda ... |
| `year_min`, `year_max` | integer | none | Vehicles: 1936-2027 |
| `max_mileage` | integer | none | Vehicles: 0, 25000 ... 200000 in steps of 25000 |

### Listing (`/listing`)

| Parameter | Type | Default | Description |
|---|---|---|---|
| `listing_id` | string | one of | An OfferUp listing id (`items[].listing_id`, `7a392126-fb9d-34c2-a6d8-1b94698428df`) |
| `url` | string | one of | An OfferUp listing link, `https://offerup.com/item/detail/<listing id>` |

### Seller (`/seller`), categories (`/categories`)

`/seller` takes `seller_id` (a listing's `seller.id`, digits, `8668343`, or an `offerup.com/p/<id>` link). `/categories` takes no input (send `{}`).

## Examples

### Asking prices in one metro

```bash
curl -X POST https://api.scavio.dev/api/v1/offerup/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "iphone 15", "zip": "98101", "sort": "best_match"}'
```

Captured `data` (2026-11-25; `items` cut to 3 of 47, `image` and `notes` dropped):

```json
{
  "query": "iphone 15",
  "page": 1,
  "sort": "best_match",
  "location": { "zip": "98101", "requested": "98101", "resolved": "Seattle", "radius_miles": 30 },
  "filters_applied": {},
  "filters_not_applied": [],
  "has_more": true,
  "count": 47,
  "items": [
    { "listing_id": "b4b883c5-00c9-37b0-826e-44b55075b013", "title": "iPhone 15 Pro Max 256gb", "price": 595, "call_for_price": false, "city": "Seattle", "state": "WA", "url": "https://offerup.com/item/detail/b4b883c5-00c9-37b0-826e-44b55075b013", "firm_price": null, "sponsored": false, "local_pickup": true, "vehicle_miles": null },
    { "listing_id": "ceef9307-e5c5-3513-a393-eca149efdf15", "title": "iPhone 15 pro max, black unlocked", "price": 650, "call_for_price": false, "city": "Everett", "state": "WA", "url": "https://offerup.com/item/detail/ceef9307-e5c5-3513-a393-eca149efdf15", "firm_price": null, "sponsored": true, "local_pickup": true, "vehicle_miles": null },
    { "listing_id": "91f6f0a1-6126-3365-9ae3-5ebb5d6b275e", "title": "iPhone 15 Pro 128GB Unlocked - White Titanium", "price": 450, "call_for_price": false, "city": "Bothell", "state": "WA", "url": "https://offerup.com/item/detail/91f6f0a1-6126-3365-9ae3-5ebb5d6b275e", "firm_price": null, "sponsored": false, "local_pickup": true, "vehicle_miles": null }
  ],
  "market": { "country": "us", "currency": "USD" }
}
```

The 47 tiles ran from 0.01 to 849.99 USD: placeholder asks (three at 0.01, one at 1, three at 5), cases, screen protectors and other accessories (5 to 30), a "for Parts ONLY" listing at 100 and a trade post sat next to the phones. The 8 iPhone 15 Pro Max 256GB listings left after dropping the placeholders asked 549 to 649.99 (median 572.50, arithmetic). Every tile read `local_pickup` `true`.

### A vehicle search with filters

```bash
curl -X POST https://api.scavio.dev/api/v1/offerup/search \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "toyota tacoma", "zip": "75201", "seller_type": "dealer", "year_min": 2018, "max_mileage": 100000, "sort": "lowest_mileage"}'
```

Captured (2026-11-25): `location` {`resolved` "Dallas", `radius_miles` 80}, `filters_applied` {`category_id` "5.1", `seller_type` "dealer", `year_min` 2018, `max_mileage` 100000}, `filters_not_applied` `[]`, the note "seller_type applies to Cars & Trucks: the search is limited to that category (category_id 5.1).", `count` 28, `has_more` `true`. First tiles: 2025 Toyota Tacoma 2WD, Dallas, 35,495 USD, `vehicle_miles` 10,017; 2021 Toyota Tacoma, Dallas, 30,654 USD, 80,492 miles (`sponsored` `true`). Two tiles had `call_for_price` `true` (`price` `null`), and four 2022-2024 Tacomas asked 2,500 or 3,000 while the other 22 priced tiles ran 24,488 to 56,019 (median 32,306): read those listings before using them.

### One dealer listing with vehicle details

```bash
curl -X POST https://api.scavio.dev/api/v1/offerup/listing \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"listing_id": "7a392126-fb9d-34c2-a6d8-1b94698428df"}'
```

Captured `data` (2026-11-25; `photos` cut to 1 of 24, `attributes` to 3 of 17, `description` and `notes` dropped):

```json
{
  "listing_id": "7a392126-fb9d-34c2-a6d8-1b94698428df",
  "title": "2021 Toyota Tacoma",
  "price": 27224,
  "original_price": 27224,
  "currency": "USD",
  "firm_price": false,
  "status": "listed",
  "removed": false,
  "condition": "used",
  "posted_at": "2026-11-25T04:33:34.992Z",
  "updated_at": null,
  "quantity": 1,
  "photos": ["https://images.offerup.com/OfY_W6AgXc4ZK5BZRvZDTZxr2mA=/640x480/c31a/c31a8cdad54d4b88b4f971113096328d.jpg"],
  "category": { "id": "5.1", "l1": "Vehicles", "l2": "Cars & Trucks" },
  "attributes": [
    { "name": "trim", "label": "Trim", "values": ["SR"] },
    { "name": "miles", "label": "Miles", "values": ["65692"] },
    { "name": "reportedSellerType", "label": "Reported Seller Type", "values": ["dealer"] }
  ],
  "vehicle": { "make": "Toyota", "model": "Tacoma", "year": 2021, "mileage": 65692, "trim": "SR", "body": "Double Cab", "color": "white", "drivetrain": "2WD", "fuel": "Regular gasoline", "transmission": "Automatic", "cylinders": 4, "mpg_city": 20, "mpg_highway": 23 },
  "city": "Fort Worth",
  "state": "TX",
  "local_pickup": true,
  "seller": {
    "id": "164992319",
    "seller_type": "dealer",
    "business_name": "AutoNation Ford South Ft Worth",
    "rating": null,
    "rating_count": 0,
    "items_sold": 0,
    "items_purchased": 0,
    "joined": "2025-07-30T22:58:07.000Z",
    "response_time": null,
    "last_active": "Active in the last day",
    "verified_badges": null
  },
  "url": "https://offerup.com/item/detail/7a392126-fb9d-34c2-a6d8-1b94698428df",
  "market": { "country": "us", "currency": "USD" }
}
```

`business_name` is set because the account is a dealer; for an individual it is `null`. No VIN appears anywhere. `seller.verified_badges` is `null` here: read `/seller` for the badges. An unknown listing id is a charged `404`.

### A dealer's public profile

```bash
curl -X POST https://api.scavio.dev/api/v1/offerup/seller \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"seller_id": "8668343"}'
```

Captured (2026-11-25): `seller_type` "dealer", `business_name` "Whatacars Auto Group LLC", `rating` 4.5 from `rating_count` 17, `rating_attributes` (On time 7, Friendly 6, Reliable 6, Communicative 6, Item as described 4), `items_sold` 925, `items_purchased` 5, `followers` 235, `joined` 2016-01-09, Dallas, TX, `response_time` "Responds in a few minutes", `verified_badges` ["95% reply rate", "Confirmed phone", "Confirmed Facebook", "Confirmed email"], `website`, `opening_hours` (Monday to Saturday 10:00 AM - 6:00 PM, Sunday closed) and `count` 20 `listings` (first: 2023 Ford F150 Regular Cab, 36,999 USD, 29,156 miles). The first 20 listings are all the profile shows.

### Category and categories

- `/category` `{"category": "furniture", "zip": "90012"}`: `category` {`id` "2.1", `name` "Furniture", `parent` Home & Garden}, `sort` "newest", `location` {`resolved` "Los Angeles", `radius_miles` 30}, `count` 49 (5 `sponsored`), first Grey leather power recliner 3 months old, Los Angeles, 400 USD. A free item reads `price` 0.
- `/categories` `{}`: `count` 14, `total` 151: Electronics & Media (`1`), Home & Garden (`2`), Clothing, Shoes, & Accessories (`3`), Baby & Kids (`4`), Vehicles (`5`; Cars & Trucks `5.1`, Motorcycles `5.2` ...), Toys, Games, & Hobbies, Sports & Outdoors, Collectibles & Art, Pet supplies, Health & Beauty, Wedding, Business equipment, Tickets, General. Each with `slug` and `url`.

### Python

```python
import statistics
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def offerup(endpoint, body):
    r = requests.post(f"{BASE}/api/v1/offerup/{endpoint}", headers=HEADERS, json=body, timeout=240)
    r.raise_for_status()
    return r.json()

# The same item's asking prices in several metros (1 credit per metro and page)
for zip_code in ("98101", "60601", "75201"):
    d = offerup("search", {"q": "iphone 15 pro max 256gb", "zip": zip_code, "sort": "best_match"})["data"]
    asks = [i["price"] for i in d["items"]
            if i["price"] and i["price"] >= 100
            and "pro max" in i["title"].lower() and "256" in i["title"]]
    loc = d["location"]
    print(loc["resolved"], loc["radius_miles"], len(d["items"]), len(asks),
          statistics.median(asks) if asks else None, d["filters_not_applied"])

# Store each answer with fetched_at: that stored set is your asking-price record.
```

## Response shapes

Every response uses the envelope `{ data, response_time, fetched_at, credits_used, credits_remaining }`. Everything is fetched when the request asks for it; nothing is cached. Every `data` carries `market` {`country`, `currency`} and `notes`.

- **tile** (search, category) - `listing_id`, `title`, `price` (asking price, USD; `null` with `call_for_price`), `call_for_price`, `city`, `state`, `url`, `image`, `firm_price`, `sponsored`, `local_pickup`, `vehicle_miles`.
- **search** - `query`, `page`, `sort`, `location` {`zip`, `requested`, `resolved`, `radius_miles`}, `filters_applied`, `filters_not_applied`, `has_more`, `count`, `items[]`.
- **category** - `category` {`id`, `name`, `slug`, `url`, `parent`}, then as search from `page`.
- **listing** - `listing_id`, `title`, `price`, `original_price`, `currency`, `firm_price`, `status`, `removed`, `condition`, `posted_at`, `updated_at`, `quantity`, `description`, `photos`, `category` {`id`, `l1`, `l2`}, `attributes[]` {`name`, `label`, `values`}, `vehicle` (cars and trucks), `city`, `state`, `local_pickup`, `seller` {`id`, `seller_type`, `business_name`, `rating`, `rating_count`, `items_sold`, `items_purchased`, `joined`, `response_time`, `last_active`, `verified_badges`}, `url`.
- **seller** - `seller_id`, `seller_type`, `business_name`, `rating`, `rating_count`, `rating_attributes[]` {`label`, `count`}, `items_sold`, `items_purchased`, `followers`, `joined`, `city`, `state`, `response_time`, `last_active`, `verified_badges`, `website`, `opening_hours[]` {`day`, `hours`}, `count`, `listings[]` {`listing_id`, `title`, `price`, `status`, `city`, `state`, `url`, `image`, `vehicle_miles`}, `url`.
- **categories** - `count` (top-level), `total`, `categories[]` {`id`, `name`, `slug`, `url`, `children[]` {`id`, `name`, `slug`, `url`}}.

`condition` (listing) is OfferUp's grade: `new`, `refurbished`, `open_box`, `used`, `for_parts`, `other`. `status` and `removed` are as OfferUp gives them; `price` is the asking price shown either way, never a sale price.

## Guardrails

- Name it "OfferUp (offerup.com, the US local marketplace for buying and selling used items, cars and trucks)" on first mention, "OfferUp" after that.
- Prices: every OfferUp number is an asking price. Quote it with USD, the resolved area, the radius and the `fetched_at` date ("asked on OfferUp around Seattle, 30-mile radius, Nov 25, 2026"). Never write "sold for", "sale price", "worth" or "market value" from OfferUp data; a sold number comes from Mercari and is labelled as Mercari's.
- Summaries: report counts kept and dropped, low, high and median per metro, with the pages read. Show the numbers and their differences only: no "deal", "underpriced", "overpriced", "worth it" or "best city to buy" verdicts, no "prices are falling" (there is no history).
- Comparisons: same item only (model + storage or edition; year + mileage band for vehicles), each price with its marketplace, metro or retailer and date. eBay numbers are live listings only, never sold prices.
- Private sellers: never name, describe or try to identify a private seller; no usernames, phone numbers, emails, addresses or coordinates (none are returned). Business or dealer names only as `business_name` returns them. Do not feature an individual seller's listing beyond its title, price, city, state and condition; prefer aggregates.
- Vehicles: no VINs (none are returned) and no valuations; seller type only as OfferUp labels it (`dealer`, `private`, `individual`, `business`).
- Descriptive only: no verdicts on OfferUp, a seller or a listing, and no commentary on OfferUp's business. Quote OfferUp's own figures only with their source.
- Do not republish OfferUp photos or descriptions at length; link listings by `url` instead.
- Terms: Scavio does not collect or store OfferUp data: each call fetches the public page at the moment the request asks for it and returns what it shows as JSON, with no response cache. OfferUp's terms of use cover how its site may be used; read the current terms for your use case and get your own advice. This is not legal advice.
- Never fabricate prices, listings, ids, areas, seller numbers or vehicle details. Only return what the API returned, with the `fetched_at` time and the listing `url`.
- Not available: sold listings or sold prices (OfferUp does not show them publicly), shipping (OfferUp listings are local pickup), search suggestions, a total result count, a seller's listings past the first 20, messaging or offers, price history (store your own).

## Failure handling

- `400` means a missing or invalid parameter, and it is not charged: search without `q`; search or category without `zip`, a ZIP that is not 5 digits, or "zip <zip> is not a known US ZIP code."; a `radius` outside 5, 10, 20, 25, 30, 50, 80, 100, 200, 1500; `page` outside 1-50; an unknown `sort`, or `best_match` on category; `min_price` above `max_price`, or prices that are not whole dollars; an unknown `condition`; `seller_type` with a `category_id` other than `5.1`; an unknown `make`; `year_min` above `year_max` or years outside 1936-2027; a `max_mileage` off OfferUp's steps; `category_id` sent to category ("the category endpoint takes category"); a category id that is not in the tree; listing without `listing_id` or `url`, a malformed id, a link that is not an offerup.com/item/detail/ link, or an id and a link naming different listings; seller without `seller_id`, or one that is not digits or an offerup.com/p/ link.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is out of credits. The body carries `billing_url`.
- `404` means not found, and it is charged: "OfferUp has no listing <id>.", "OfferUp has no seller <id>.", "OfferUp has no such category.". Take ids and slugs from a previous answer rather than guessing them. A search with no matches is a `200` with `count` 0.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api).
- `502` means OfferUp data was temporarily unavailable ("OfferUp is temporarily unavailable. Please try again."). It is not charged, so retry after a few seconds.
- `503` with a `Retry-After` header means OfferUp is busy ("OfferUp is busy right now. Please retry in a few seconds."): wait the `Retry-After` seconds and send it again. Not charged.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## SDKs

```bash
pip install scavio==0.89.0
npm install scavio@0.90.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const { data: hits } = await scavio.offerup.search({ q: "iphone 15", zip: "98101", sort: "best_match" });
const { data: trucks } = await scavio.offerup.search({ q: "toyota tacoma", zip: "75201", seller_type: "dealer", year_min: 2018, sort: "lowest_mileage" });
const { data: listing } = await scavio.offerup.listing({ listing_id: "7a392126-fb9d-34c2-a6d8-1b94698428df" });
const { data: furniture } = await scavio.offerup.category({ category: "furniture", zip: "90012" });
const { data: tree } = await scavio.offerup.categories();
const { data: dealer } = await scavio.offerup.seller({ seller_id: "8668343" });
```

In Python (`from scavio import ScavioClient`, `client = ScavioClient()`) the same methods are `client.offerup.search(...)`, `listing`, `category`, `categories` and `seller`, with the same parameter names as keyword arguments.

## MCP

The Scavio MCP server exposes all 5 endpoints as tools: `search_offerup`, `get_offerup_listing`, `get_offerup_category`, `get_offerup_categories` and `get_offerup_seller`. OfferUp is opt-in: add `offerup` to `SCAVIO_PLATFORMS`.

```json
{
  "mcpServers": {
    "scavio": {
      "command": "npx",
      "args": ["-y", "@scavio/mcp-server@0.89.0"],
      "env": {
        "SCAVIO_API_KEY": "sk_live_your_key",
        "SCAVIO_PLATFORMS": "default,offerup"
      }
    }
  }
}
```

## Docs

Full reference per endpoint: [search](https://scavio.dev/docs/offerup-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api), [listing](https://scavio.dev/docs/offerup-listing?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api), [category](https://scavio.dev/docs/offerup-category?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api), [categories](https://scavio.dev/docs/offerup-categories?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api), [seller](https://scavio.dev/docs/offerup-seller?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api). Overview: [OfferUp API](https://scavio.dev/offerup-api?utm_source=agent-skills&utm_medium=skill&utm_campaign=offerup-api).
