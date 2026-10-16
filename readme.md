# guidoio.social

Produzione contenuti Instagram per @guidoio_. Struttura copiata dal progetto marco-social, con brand separato.

- `CLAUDE.md` — istruzioni per Claude (lette a ogni sessione). Compilato il 16/10/2026.
- `.claude/skills`, `.claude/agents` — skill di marketing/Instagram e aiutanti economici (Haiku, Sonnet).
- `theory/` — sintesi Theory University.
- `produzione/brand/brand.json` — colori, font, sigla, handle: modificare qui, gli script si adeguano.
- `produzione/script/` — generatori:
  - `slides.mjs` caroselli 4:5 da JSON → `node script/slides.mjs contenuti/esempio.json out/` (con `OFF=1` la numerazione conta anche la copertina)
  - `cover_personaggio45.mjs` copertina carosello 4:5 con foto del personaggio → `node script/cover_personaggio45.mjs "Titolo<br><em>accento</em>" "sottotitolo" "#1" foto.png out.jpg`
  - `cover_personaggio.mjs` copertina reel 9:16, stessa sintassi
  - `story.mjs` storia 9:16 da HTML
  - `render.mjs` reel da pagina HTML animata (`window.render(t)`) → MP4
  - `synth.py` base musicale + effetti da un JSON di tempi
- `docs/` — stato pubblicazioni e piano.

Uso (dalla cartella `produzione`). Il progetto gira solo in locale. Gli import di Playwright puntano ancora a `/opt/node22/lib/node_modules/playwright/index.mjs`: dopo `npm i -g playwright` cambiarli con il percorso di `npm root -g`.
