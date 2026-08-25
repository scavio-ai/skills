---
name: website-screenshot-api
description: Capture a full-page PNG screenshot of any public URL, returned inline as a base64 data:image/png URI ready to drop into an <img> tag. One endpoint, three capture tiers - normal and advanced at 1 credit, ultra for the hardest sites at 5. Only a successful capture is billed. Returns url, image, image_format, mode and image_bytes.
version: 1.0.0
tags: website-screenshot, screenshot-api, url-to-screenshot, web-page-screenshot, full-page-screenshot, png, webpage-capture, visual-testing, website-preview, thumbnail, ocr-input, agent-tools, langchain, crewai, autogen, structured-data, json, ai-agents
metadata:
  openclaw:
    requires:
      env:
        - SCAVIO_API_KEY
    primaryEnv: SCAVIO_API_KEY
    timeout: 120
    throttle: 1
    emoji: "\U0001F4F8"
    homepage: https://scavio.dev/docs?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-screenshot-api
---

# Website Screenshot API - Full-Page PNG of Any URL

Give any public URL and get back a full-page PNG screenshot of the page, returned inline as a base64 `data:image/png` URI ready to drop into an `<img>` tag or decode to a file. Every capture is the full page, top to bottom.

## When to trigger

Use this skill when the user asks to:
- Screenshot a web page or capture a full-page image of a URL
- Grab a visual snapshot / preview / thumbnail of a website
- Turn a page into an image for a report, a slide, an email or a PDF
- Feed a rendered page to a vision model or an OCR step as a PNG
- Visually diff or archive how a page looks right now

## Setup

Get a free API key at [scavio.dev](https://scavio.dev/?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-screenshot-api) (50 free credits to get started, no card required):

```bash
export SCAVIO_API_KEY=sk_live_your_key
```

Every request is a `POST` with a JSON body and:

```
Authorization: Bearer $SCAVIO_API_KEY
```

## Endpoints

Base URL: `https://api.scavio.dev`.

| Endpoint | Credits | What it returns |
|---|---|---|
| `POST /api/v1/extract/screenshot` | 1-5 | A full-page PNG of the URL as a base64 `data:image/png` URI, plus its format, the capture tier used, and the image size in bytes |

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | required | The page to capture. `http(s)` only; a bare host like `example.com` is upgraded to `https`. Internal / loopback hosts are rejected. Always captured full-page |
| `mode` | string | `normal` | Capture tier: `normal`, `advanced`, or `ultra` |

Capture tiers and their cost:

| `mode` | Credits | Use it for |
|---|---|---|
| `normal` | 1 | Most sites - the default |
| `advanced` | 1 | Pages that load their content a moment after the first response, so the capture waits longer before shooting |
| `ultra` | 5 | The hardest, most heavily protected sites that the lower tiers cannot reach |

Start at `normal` and only step up if the returned image is blank or incomplete - the higher tiers cost more and are wasted on pages that do not need them.

## Scope notes

- The capture is **always the full page**, not just the visible viewport - long pages come back as tall images.
- The image is returned **inline** as a `data:image/png;base64,...` URI, not a hosted link. There is no URL to expire; you hold the bytes.
- Only a **successful** capture is billed. A page that cannot be captured (a `422`) or a target that is not found (a `404`) costs nothing.
- `image_bytes` is the size of the decoded PNG, so you can budget before decoding.

## Examples

```python
import base64
import requests

BASE = "https://api.scavio.dev"
# Your key from https://scavio.dev. Load it from your environment or secret
# store in real code - keep it out of source control.
API_KEY = "sk_your_key_here"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 1. Capture a full-page screenshot (normal tier, 1 credit)
shot = requests.post(f"{BASE}/api/v1/extract/screenshot", headers=HEADERS,
    json={"url": "https://example.com"}).json()

data = shot["data"]
print(data["mode"], data["image_format"], data["image_bytes"], "bytes")

# 2. The image is a data:image/png;base64 URI - strip the prefix, decode it,
#    and write the PNG to disk.
b64 = data["image"].split(",", 1)[1]
with open("example.png", "wb") as f:
    f.write(base64.b64decode(b64))

# 3. A tougher, heavily protected site - step up the capture tier (ultra, 5 credits)
hard = requests.post(f"{BASE}/api/v1/extract/screenshot", headers=HEADERS,
    json={"url": "https://www.nike.com", "mode": "ultra"}).json()
print(hard["credits_used"], "credits used")
```

curl:

```bash
curl -s https://api.scavio.dev/api/v1/extract/screenshot \
  -H "Authorization: Bearer $SCAVIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","mode":"normal"}'
```

## Response shape

Every response uses the envelope `{ data, response_time, credits_used, credits_remaining }`.

```json
{
  "data": {
    "url": "https://example.com/",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA7E...",
    "image_format": "png",
    "mode": "normal",
    "image_bytes": 16917
  },
  "response_time": 4255,
  "credits_used": 1,
  "credits_remaining": 4574
}
```

## Guardrails

- Cost tracks the tier: `normal` and `advanced` are **1 credit**, `ultra` is **5**. Only a successful capture is billed.
- The capture is always the **full page**. If the user only wants the fold, crop the returned PNG yourself.
- Never fabricate the image, its size or its contents. Only report what the API returned.
- The image URI can be large. Decode it to a file rather than pasting the base64 into a prompt.

## Failure handling

- `400` means an invalid or missing `url`, or an unreachable internal/loopback host. Fix and retry.
- `401` means the API key is invalid or missing. Check `SCAVIO_API_KEY`.
- `404` means the target page was not found.
- `422` means the page cannot be captured - try a higher `mode`, or accept that the site blocks capture.
- `429` means rate or usage limit exceeded. Wait before retrying. See [rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=website-screenshot-api).
- `502` / `503` mean the source is temporarily unavailable - wait a few seconds and retry.
- If `SCAVIO_API_KEY` is not set, prompt the user to export it before continuing.
