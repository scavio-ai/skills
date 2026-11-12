# Company Enrichment API - Emails, Phones, Socials, Owner from a Website or Google Maps

Turn a business website, or a Google Maps place_id, into contact data: the emails and phone numbers the company publishes, its social profiles, its contact page, and the owner or founder's name and title together with the page that names them. Every value comes from a page that was read live on this call; an owner is only returned when a cited page names them. One endpoint, structured JSON.

## When to trigger

Use this skill when the user asks to:
- Find a company's email address, phone number or social profiles from its website
- Find out who owns or founded a small business, with a source
- Turn a list of Google Maps results (plumbers in Austin, dentists in Leeds) into a lead list with contacts
- Enrich a CRM or spreadsheet of business websites with emails, phones and socials
- Find a business's contact page

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=company-enrichment-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=agent-skills&utm_medium=skill&utm_campaign=company-enrichment-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Company Enrich costs 10 credits from a website and 20 from a place_id, so the free credits cover a handful of test calls.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

## Endpoint

| Endpoint | Credits | Description |
|---|---|---|
| `POST https://api.scavio.dev/api/v1/company/enrich` | 10 / 20 | Contacts and owner from a website (10) or a Google Maps place_id (20) |

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Parameters

Provide `url` or `place_id`. With neither, the API answers `400` (not charged).

| Parameter | Type | Description |
|---|---|---|
| `url` | string | The company's own website, with or without `https://` (3-2048 chars). A social profile URL (Facebook, Instagram, LinkedIn...) is a `400`: pass the business's own site. If you send both, `url` is the site that gets read |
| `place_id` | string | A Google Maps place_id, as returned in `local_results[].place_id` by the Google Maps search endpoint (10-300 chars). The listing is looked up first for name, address, phone and website, then the website is read |

## Workflow

1. **From a website:** call `/company/enrich` with `{"url": "..."}`.
2. **From Google Maps:** call `POST /api/v2/google/maps/search` (1 credit, see the `google-maps-api` skill), keep each `local_results[].place_id`, then call `/company/enrich` with `{"place_id": "..."}` for each business.
3. **Read the result:** contacts are in `data.company`; the owner, when a page names one, is in `data.owner`; the pages that were read are in `data.pages_read`.

## Example

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Enrich one company from its website (10 credits)
res = requests.post(f"{BASE}/api/v1/company/enrich", headers=HEADERS,
    json={"url": "https://reliantplumbing.com"}, timeout=180).json()
company = res["data"]["company"]
print(company["name"], company["emails"], company["phones"], company["socials"])
owner = res["data"]["owner"]
if owner:
    print(owner["name"], "-", owner["title"], "(source:", owner["source_url"] + ")")

# 2. From a Google Maps search to a lead list (1 credit + 20 per business)
search = requests.post(f"{BASE}/api/v2/google/maps/search", headers=HEADERS,
    json={"query": "plumbers", "ll": "@30.2672,-97.7431,12z"}, timeout=60).json()
for place in search["local_results"][:5]:
    lead = requests.post(f"{BASE}/api/v1/company/enrich", headers=HEADERS,
        json={"place_id": place["place_id"]}, timeout=180)
    if lead.status_code != 200:
        continue  # 502 = site unreachable, not charged
    data = lead.json()["data"]
    print(data["company"]["name"], data["company"]["emails"],
          data["owner"]["name"] if data["owner"] else None)
```

## Response

The payload is under `data`; the envelope adds `response_time` (ms), `fetched_at`, `credits_used` (the exact charge) and `credits_remaining`.

- `data.company`: `name`, `website`, `domain`, `emails[]` (addresses printed on the site, company-domain first), `phones[]` (digits only), `socials` (one profile URL per network found: facebook, instagram, linkedin, x, tiktok, youtube, pinterest), `contact_page` (or null), `address` and `place_id` (filled when you pass a place_id).
- `data.owner`: `name`, `title` (owner, founder, co-founder, president, CEO or managing director, as the source states it), `source_url` (the page that names them), `email`, `email_status` (`published` when an address on the site matches the owner's name, otherwise `not_found` with `email` null). `data.owner` is `null` when no page names one.
- `data.pages_read[]`: the home page plus up to 3 contact, about or team pages, and the privacy and terms pages.

Real response captured 2026-11-10 (`url: https://reliantplumbing.com`, phones trimmed to 3):

```json
{
  "data": {
    "company": {
      "name": "Reliant Plumbing",
      "website": "https://reliantplumbing.com/",
      "domain": "reliantplumbing.com",
      "emails": ["office@reliantplumbing.com"],
      "phones": ["5122226029", "5129003549", "5123996886"],
      "socials": {
        "facebook": "https://www.facebook.com/ReliantPlumbingTx",
        "youtube": "https://www.youtube.com/channel/UC6sOp-XAWD1NwU6aosEHEPA",
        "instagram": "https://www.instagram.com/reliant_plumbing_tx/"
      },
      "contact_page": "https://reliantplumbing.com/contact-us/",
      "address": null,
      "place_id": null
    },
    "owner": {
      "name": "Max Hicks",
      "title": "Founder",
      "source_url": "https://reliantplumbing.com/about-us/",
      "email": null,
      "email_status": "not_found"
    },
    "pages_read": [
      "https://reliantplumbing.com/",
      "https://reliantplumbing.com/contact-us/",
      "https://reliantplumbing.com/about-us/",
      "https://reliantplumbing.com/privacy-policy/",
      "https://reliantplumbing.com/terms-conditions/"
    ]
  },
  "response_time": 27498,
  "fetched_at": "2026-11-10T16:53:37.418Z",
  "credits_used": 10,
  "credits_remaining": 69632
}
```

## Guardrails

- 10 credits from a `url`, 20 from a `place_id` (1 when the Maps listing has no readable website). Tell the user the total before enriching a long list: 50 Maps results by place_id is 1,000 credits.
- Each call reads several pages live. Calls usually take 10-45 seconds and a slow site can take about 2 minutes: use a request timeout of at least 180 seconds, and enrich long lists a few at a time rather than all at once.
- Never fabricate an email, phone number or owner. Only return what the API returned; when `data.owner` is null, say no page names an owner.
- An owner `email` is only present when the site publishes it. Do not guess addresses from a name and domain.
- Pass the business's own website as `url`, not a social profile.

## Failure handling

- `400` means neither `url` nor `place_id` was sent, or `url` is a social profile. Not charged. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `402` means the balance is too low; the body carries `billing_url`.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=company-enrichment-api).
- `502` "The company website could not be reached." Not charged. The site is down or blocks readers; skip it or try again later.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
