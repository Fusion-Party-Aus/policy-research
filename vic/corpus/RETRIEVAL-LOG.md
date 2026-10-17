# Retrieval log

> **Status:** Snapshot — not a live feed
> **Retrieved:** 2026-10-16T14:16:29Z
> **Method:** HTTP GET with curl, following redirects
> **AI assistance:** Retrieval automated by Policy Researcher agent; structure verified manually

## Endpoints

| File | URL | HTTP status | Size (bytes) | SHA-256 |
| --- | --- | --- | --- | --- |
| policies.json | `https://vic.fusionparty.org.au/api/policies.json` | 200 | 289580 | `717057699d69ece07f90afd1e58d9473f5b35c2275a2a63a3ecb4f43169e32bf` |
| research.json | `https://vic.fusionparty.org.au/api/research.json` | 200 | 228262 | `df30a305755ffdb09e8bc07eea8ec3be7c04cebcd7da70283b5e778de11d8482` |

## Notes

- The authorised URLs in the issue description use `/API/` (uppercase). The server treats paths as case-sensitive; only lowercase `/api/` returns HTTP 200. The uppercase form redirects to a 404 page. Browser address bars may normalise the case automatically.
- `policies.json` reports `generated_at: 2026-10-16T14:16:18.431Z` and `platform_updated_at: 2026-10-12T07:14:15Z`.
- `research.json` reports `generated_at: 2026-10-16T14:16:18.954Z` and `collection_updated_at: 2026-10-08T10:57:54Z`.
- Both files are dynamic API exports generated on request, not static snapshots. Content may change between retrievals.
- No pagination parameters were observed; the API returned all records in a single response.
- No authentication was required.

## Scope and limitations

These exports represent the publicly accessible Victorian policy and research corpus from Fusion's Sanity CMS, exported via the website's public JSON API. This retrieval cannot verify:
- Whether additional unpublished or draft content exists in Sanity.
- Whether attachments, images or other assets referenced in the CMS are included.
- Whether the export includes all historical versions or only the current revision.

The `policy_count: 41` field matches the actual number of policy objects in the array (41). The research endpoint does not include an explicit count field; 25 resources were returned.
