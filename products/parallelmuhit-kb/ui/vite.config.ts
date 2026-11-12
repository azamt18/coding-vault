import { defineConfig } from "vite";

// `npm run dev` proxies the question box's /api to the local server (python3 serve.py, port 8787).
// the static build has no server; the box hides itself when /api/health fails.
export default defineConfig({
  server: { proxy: { "/api": "http://127.0.0.1:8787" } },
});
