# Agent Colette — PRD

## Origin
- Fork of upstream [Odysseus](https://github.com/pewdiepie-archdaemon/odysseus)
  (AGPL-3.0-or-later), rebranded as the user's personal AI workspace.
- Hosted inside Emergent platform pod (FastAPI on :8001, transparent Node
  HTTP/WS proxy on :3000 → :8001).

## Original problem statement
> "Przechwycić projekt i dokończ — wykorzystaj repozytorium
> https://github.com/pewdiepie-archdaemon/odysseus.git, zachowaj obecne
> możliwości, przebranżuj na Agenta Colette, zostaw opensource, minimalistyczny
> graficznie grafit · turkus · czarny · warcast."

## User persona
- Operator/owner of a self-hosted personal AI workspace who wants to track
  Odysseus upstream and apply a personal brand (Agent Colette) + a
  minimalist graphite/turquoise/black/warcast theme.

## Core requirements (static)
- Preserve 100% of Odysseus functionality (chat, agents, cookbook, deep
  research, notes, calendar, gallery, library, tasks, memory, email,
  MCP, RAG/Chroma).
- Rebrand visible "Odysseus" → "Agent Colette" without renaming code,
  CSS classes, route paths, or `localStorage` keys (so upstream merges
  stay clean).
- Apply graphite/turquoise/black/warcast palette in both `static/style.css`
  `:root` and `static/js/theme.js`'s `dark` preset (default theme).
- Keep the project open-source (AGPL-3.0-or-later) and configure a `upstream`
  git remote on `/app/backend` pointing at the Odysseus repo so the operator
  can `git fetch upstream && git merge upstream/dev`.

## What's been implemented (2026-01-15)
- **Code import**: Odysseus repo cloned into `/app/backend` (app.py, core,
  src, routes, services, static, integrations, mcp_servers, companion,
  config). All upstream tests/utilities preserved.
- **Emergent bootstrap**: `/app/backend/server.py` rewritten as a shim that
  prepares `ODYSSEUS_DATA_DIR`, copies `.env.example` → `.env`, creates
  required subdirs, and re-exports the FastAPI app for `uvicorn server:app`.
- **Frontend proxy**: `/app/frontend/proxy-server.js` (http-proxy 1.18) +
  `package.json` `start` script — port 3000 transparently proxies to :8001
  (HTTP + WebSocket).
- **Theme tokens**: `static/style.css` `:root` palette retuned to
  `#0e1114 / #d4ddde / #161a1f / #2a3338 / #2dd4bf` (graphite · warcast ·
  turquoise). Light-mode tokens retuned for contrast.
- **Default theme**: `static/js/theme.js` `dark` preset rebuilt as the Agent
  Colette palette with advanced overrides for `brandColor`, `sendBtnBg`,
  `sendBtnHover`, `toggleActive`. `--brand-color: #2dd4bf` added as token.
- **Rebrand**: titles, sidebar wordmark, welcome heading, current-meta,
  textarea placeholder ("Message Agent Colette…"), settings labels,
  manifest.json (name, short_name, theme_color, background_color), login
  page (title, logo SVG, favicon, focus colors, primary button).
- **Sigil**: SVG logo replaced — lozenge with centre dot (in turquoise),
  used on login page and welcome heading.
- **Documentation**: `/app/backend/AGENT_COLETTE.md` documents the fork
  and upstream-merge workflow. Upstream credit preserved in `LICENSE`,
  `ACKNOWLEDGMENTS.md`, and `README.md`.
- **Upstream remote**: `/app/backend` git repo has `upstream` remote
  pointing to https://github.com/pewdiepie-archdaemon/odysseus.git.
- **First-run admin seeded**: `colette` / `ColettePass123!` (admin).
- **Verified**: login renders, post-login workspace renders with all
  features in sidebar; `/api/health` and `/api/version` return 200.

## Prioritized backlog
- **P1** Configure default LLM provider — operator must add one via
  Settings → Models before chat/agent flows can run end-to-end.
- **P2** Add Agent-Colette-specific preset themes (e.g., `colette-light`,
  `colette-warcast-deep`) to `THEMES` map.
- **P2** Replace upstream PWA icons (`static/icons/icon-192.png`, `-512.png`)
  with the Colette sigil rendered as PNG.
- **P3** Custom 404 page rebrand.
- **P3** Optional `companion/` system-prompt rewrite to give the assistant
  a "Colette" persona (currently neutral).
