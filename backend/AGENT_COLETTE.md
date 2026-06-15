# Agent Colette

**Agent Colette** is your personal AI workspace — a friendly fork of
[Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) running inside
the Emergent platform. It keeps every capability of upstream Odysseus
(chat + agents, cookbook, deep research, documents, email, notes, calendar,
gallery, memory, MCP, …) and re-skins the interface with a minimalist
**graphite · turquoise · black · warcast** palette.

This fork stays open-source under AGPL-3.0-or-later (same as Odysseus).

## What changed vs. upstream Odysseus

- **Branding** — wordmark "Odysseus" → "Agent Colette" across the login
  page, sidebar, welcome screen, PWA manifest, and tab titles.
  Internal identifiers (CSS classes, `localStorage` keys like
  `odysseus-theme`, route names) are intentionally **unchanged** so
  `git pull upstream/dev` rebases cleanly.
- **Theme tokens** — the `:root` palette in `static/style.css` is replaced
  with the graphite/turquoise/black warcast set. Light-mode tokens are also
  retuned for contrast.
- **Logo** — the upstream "boat" SVG is swapped for a sharp geometric
  Colette sigil (a turquoise lozenge with a centre dot).
- **Emergent bootstrap** — `server.py` prepares `data/`, `.env`, and sane
  defaults for `AUTH_ENABLED`, `SECURE_COOKIES`, and `ALLOWED_ORIGINS`, then
  re-exports `app.py`'s FastAPI app for `uvicorn server:app`.
- **Frontend proxy** — `/app/frontend/proxy-server.js` forwards port 3000
  (Emergent's public ingress) to port 8001 (the FastAPI app) so the entire
  Colette UI is reachable through the platform's preview URL.

## Pulling upstream updates

A git remote is configured for the upstream Odysseus repo. To pull the
latest changes:

```bash
cd /app/backend
git fetch upstream
git merge upstream/dev      # or upstream/main for the curated branch
```

Most updates apply cleanly because the rebrand only touches a handful of
visible strings and the colour-token block at the top of `style.css`.

## Local layout

```
/app/backend/                Agent Colette backend (FastAPI)
  app.py                     upstream orchestrator (unchanged)
  server.py                  Emergent bootstrap shim → re-exports app
  static/                    UI (rebranded)
  core/ src/ routes/ …       upstream code
  data/                      runtime data (sessions, db, uploads — gitignored)
/app/frontend/
  proxy-server.js            port-3000 → port-8001 transparent proxy
  package.json               `yarn start` runs the proxy
```

## First-run setup

1. Open the Emergent preview URL — you land on the login screen.
2. Set a username and password — the first account becomes admin.
3. Use **Settings → Models / Providers** to plug in an LLM endpoint
   (Ollama, OpenAI, Anthropic, your local llama.cpp, …). Agent Colette
   keeps your keys local.

## License & credit

AGPL-3.0-or-later. All upstream credits live in [`ACKNOWLEDGMENTS.md`](ACKNOWLEDGMENTS.md)
and [`LICENSE`](LICENSE). Original project © Odysseus contributors.
