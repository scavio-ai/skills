---
name: url-to-markdown-api
description: "Turn any URL into clean Markdown, plain text or raw HTML for LLM prompts and RAG chunks. One endpoint, three fetch tiers: normal and advanced (renders JavaScript) at 1 credit, ultra for hard bot walls at 2. Only a successful extraction is billed. Returns url, format, mode, content and content_length."
version: 1.0.0
tags: url-to-markdown, extract, read-url, web-scraping, html-to-markdown, content-extraction, page-content, readability, rag, llm-context, javascript-rendering, agent-tools, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4C4"
    homepage: https://scavio.dev/docs/extract?utm_source=agent-skills&utm_medium=skill&utm_campaign=url-to-markdown-api
---

# URL to Markdown - Web Page Extract API

Read any web page and get it back as clean Markdown, plain text, or raw HTML. This is the read-a-page primitive: one URL in, page content out.

**Extract is not a platform - it is a core endpoint.** There is no namespace, no per-site parser and no site-specific parameters. It works on any http(s) URL.

## When to trigger

Use this skill when the user asks to:
- Read, summarise, or quote a specific web page
- Turn a URL into Markdown or plain text for an LLM prompt or a RAG chunk
- Pull an article, docs page, changelog, pricing page or blog post into the conversation
- Fetch a page that blocked a plain HTTP request
- Grab the raw HTML of a page to parse it yourself

This is usually the right first tool whenever a user pastes a link and asks a question about what is on it.

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=url-to-markdown-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

### If you do not have a key yet

An agent running this skill without `SCAVIO_API_KEY` set will get `401` on every
call below. The whole path from nothing to a working key is self-serve:

1. Sign up at [dashboard.scavio.dev](https://dashboard.scavio.dev/sign-up?utm_source=clawhub&utm_medium=skill&utm_campaign=url-to-markdown-api) - email or Google, no card required.
2. A key is created for the account automatically at signup. It is on the dashboard under API Keys, ready to copy.
3. A new account starts with 50 credits. Endpoints in this skill cost 1 credit each unless the table below says otherwise.

When the balance runs out the API answers `402` with a JSON body carrying
`billing_url`. Topping up needs no code change - the same key keeps working.
The smallest purchase is 2,500 credits for $25, and monthly plans work out
cheaper per credit if the usage is steady rather than one-off.

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoint

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/extract` | 1, 1 or 2 by `mode` | `{ url, format, mode, content, content_length }` |

No pagination - one URL, one response.

## Cost is a function of the body

Extract is **tier-priced**, so there is no single "costs N credits" answer. The `mode` parameter sets the price:

| `mode` | What it does | Credits |
|---|---|---|
| `normal` (default) | Plain datacenter fetch | **1** |
| `advanced` | Renders JavaScript before reading | **1** |
| `ultra` | Heaviest fetch, for the hardest bot walls | **2** |

`advanced` costs the same as `normal`, so reach for it freely on any page that renders client-side. `ultra` is the only step that doubles the price - escalate to it only after `normal` or `advanced` came back empty or blocked.

**Billing is charge-on-success.** Only a `2xx` extraction is billed. A dead link, a bot wall or a timeout costs nothing, so escalating a failed fetch to a higher tier does not stack charges for the failures.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | The page to read (1-2048 chars). http(s) only; a bare host is upgraded to `https`. |
| `format` | string | `markdown` | `html`, `markdown`, `text` |
| `mode` | string | `normal` | `normal`, `advanced`, `ultra`. **This is the price-bearing parameter.** |

### What the three formats actually are

- **`markdown`** (default) - a readability extraction: the article content, cleaned of navigation and chrome, as Markdown. This is what you want for an LLM prompt or a RAG chunk.
- **`html`** - the raw page exactly as fetched. Use it when you intend to parse the DOM yourself.
- **`text`** - that same readability Markdown, flattened to plain text. The flattener is deliberately conservative about CommonMark, so `snake_case` identifiers, `__dunders__` and inline code survive intact rather than being eaten as emphasis markers.

### URL guard

`http` and `https` only. A bare host is upgraded to `https` for you. Loopback, private, link-local and cloud-metadata hosts are rejected with a `400` - the fetch happens server-side, so pointing this at `localhost` would only ever reach someone else's loopback, not the user's.

## Examples

```python
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. The common case: a page as clean Markdown, 1 credit
page = requests.post(f"{BASE}/api/v1/extract", headers=HEADERS,
    json={"url": "https://example.com/pricing"}).json()

print(page["data"]["content"][:500], page["data"]["content_length"])

# 2. Plain text for an embedding pipeline, still 1 credit
plain = requests.post(f"{BASE}/api/v1/extract", headers=HEADERS,
    json={"url": "https://example.com/blog/post", "format": "text"}).json()

# 3. A client-rendered page: advanced renders JavaScript and STILL costs 1 credit
spa = requests.post(f"{BASE}/api/v1/extract", headers=HEADERS,
    json={"url": "https://example.com/app/docs", "mode": "advanced"}).json()

# 4. Raw HTML to parse yourself
raw = requests.post(f"{BASE}/api/v1/extract", headers=HEADERS,
    json={"url": "https://example.com", "format": "html"}).json()
```

Escalate tiers only on failure. Failed fetches are not billed, so this ladder
costs 1 credit on success at any step and 2 only if it has to reach `ultra`:

```python
def read(url, format="markdown"):
    """normal (1cr) -> advanced (1cr) -> ultra (2cr). Only the successful call is billed."""
    for mode in ("normal", "advanced", "ultra"):
        r = requests.post(f"{BASE}/api/v1/extract", headers=HEADERS,
                          json={"url": url, "format": format, "mode": mode})
        if r.status_code == 200:
            data = r.json()["data"]
            if data["content_length"]:
                return data
        if r.status_code == 400:
            break            # bad or blocked URL - a higher tier will not fix it
    return None
```

## Response shape

The envelope is `{ data, response_time, credits_used, credits_remaining }`, and `data` is:

```json
{
  "url": "https://example.com/pricing",
  "format": "markdown",
  "mode": "normal",
  "content": "# Pricing\n\nSimple, usage-based pricing...",
  "content_length": 4821
}
```

`url`, `format` and `mode` echo what was actually used, so you can log which tier paid for the result. `credits_used` in the envelope tells you whether the call cost 1 or 2.

## Guardrails

- **Never quote a flat price for this endpoint.** It is 1 credit for `normal` and `advanced` and 2 for `ultra`. If you tell the user what a run will cost, price it by mode.
- Start at `normal`. Escalate to `advanced` for a page that renders client-side, and to `ultra` only when the cheaper tiers came back blocked or empty - that is the only step that doubles the cost.
- Do not retry a failed fetch at the same tier more than once. Failures are free, but they are also usually deterministic; change the tier instead.
- Use `markdown` or `text` for anything going into a model prompt. `html` is for parsing, and it burns context.
- A short `content_length` on a `200` usually means a bot wall or a client-rendered shell, not an empty page. Escalate the tier before reporting the page as blank.
- Never invent page content. If the extraction is empty, say the page could not be read rather than answering from memory about what the URL probably says.
- Attribute what you quote: keep the source URL alongside any content you surface.
- Respect the user's intent about what to fetch. This reads publicly reachable pages only; it does not log in, submit forms, or bypass a paywall.

## Failure handling

- `400` means the URL was rejected: a non-http(s) scheme, a malformed URL, or a loopback / private / link-local / metadata host. Not billed. A higher `mode` will not fix it.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the page does not exist upstream. Not billed.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=url-to-markdown-api).
- `502` / `503` mean the fetch failed or upstream is unavailable. **Not billed** - retry once, then escalate `mode` rather than hammering the same tier.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.

## Python SDK

`langchain-scavio` has no extract tool - use the Scavio SDK directly. Extract is a **top-level method**, not a namespace: `client.extract(...)`, never `client.extract.extract(...)`.

```bash
pip install scavio==0.15.0
```

```python
from scavio import ScavioClient

client = ScavioClient()  # reads SCAVIO_API_KEY

page = client.extract("https://example.com/pricing")
plain = client.extract("https://example.com/blog/post", format="text")
spa = client.extract("https://example.com/app/docs", mode="advanced")   # still 1 credit
```

JavaScript / TypeScript:

```bash
npm install scavio@0.15.0
```

```js
import { Scavio } from "scavio";

const scavio = new Scavio(); // reads SCAVIO_API_KEY
const page = await scavio.extract({ url: "https://example.com/pricing" });
const spa = await scavio.extract({ url: "https://example.com/app/docs", mode: "advanced" });
```
