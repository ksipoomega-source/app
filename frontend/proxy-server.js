/**
 * Agent Colette — frontend proxy
 *
 * The Emergent platform routes everything that isn't /api/* to port 3000.
 * Agent Colette's UI is served by the FastAPI backend on port 8001
 * (under /, /login, /static/*, /notes, /calendar, …), so we just proxy
 * port 3000 → 8001 transparently, including WebSocket upgrades.
 *
 * No React, no webpack — keeps the rebrand surface tiny so upstream
 * Odysseus updates can be pulled in with minimal conflicts.
 */
const http = require('http');
const httpProxy = require('http-proxy');

const TARGET = process.env.AGENT_COLETTE_BACKEND || 'http://localhost:8001';
const HOST = process.env.HOST || '0.0.0.0';
const PORT = parseInt(process.env.PORT || '3000', 10);

const proxy = httpProxy.createProxyServer({
  target: TARGET,
  changeOrigin: true,
  ws: true,
  xfwd: true,
  preserveHeaderKeyCase: true,
  proxyTimeout: 0,
  timeout: 0,
});

proxy.on('error', (err, req, res) => {
  console.error(`[proxy] ${req && req.method} ${req && req.url} -> ${err.message}`);
  if (res && !res.headersSent && res.writeHead) {
    res.writeHead(502, { 'Content-Type': 'text/plain' });
    res.end('Agent Colette backend is starting…');
  } else if (res && res.destroy) {
    res.destroy();
  }
});

const server = http.createServer((req, res) => {
  proxy.web(req, res);
});

server.on('upgrade', (req, socket, head) => {
  proxy.ws(req, socket, head);
});

server.listen(PORT, HOST, () => {
  console.log(`Agent Colette proxy listening on http://${HOST}:${PORT} -> ${TARGET}`);
});
