# Zero-API Policy

## Mandatory rule

Do not call, configure, request, store, or depend on any third-party API, key, token, endpoint, SDK, hosted model, or external service integration.

## Allowed routes

- Use platform-native browsing and open official webpages normally.
- Read files uploaded by the user.
- Read user-exported PDF, RIS, BibTeX, NBIB, CSV, XLSX, JSON, DOCX, and PPTX files.
- Run local Python or R only when the current environment already supports it.
- Use a local model only when the user already has the environment and explicitly chooses it.
- Guide manual export from authenticated or licensed interfaces and verify returned files.

## Forbidden routes

- Do not ask for an API key or token.
- Do not create `.env` instructions for a third-party service.
- Do not send direct network requests from bundled scripts.
- Do not install PaperQA2, ArcDeck, SPECTER2, Binoculars, Fast-DetectGPT, RAID, Vale, or a commercial detector as a prerequisite.
- Do not silently replace an unavailable local adapter with a remote service.

## Degradation behavior

Keep the five-family, 35-stage workflow operational when an optional local adapter is absent. Explain which automation is unavailable, produce the strongest non-fabricated intermediate artifact, and issue a manual or hybrid operation companion when real execution or authenticated access is necessary.
