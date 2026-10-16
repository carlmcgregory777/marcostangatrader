# Sigla GUIDO IO. — «Brindi tu. Guido io!» (approvata da Marco il 16/10/2026)

Va **in fondo a ogni reel, sempre uguale** (4 s): non cambiarla, non accorciarla, non rimusicarla.

- `Sigla_GUIDO_IO.mp4` — sigla pronta (1080×1920, 30 fps, 3,96 s): «BRINDI TU.» → «GUIDO IO» → il punto arancione si accende sull'accordo finale. Basta concatenarla dopo l'ultima scena del reel.
- `sigla_audio.mp3` — solo audio (jingle + voce).
- `voce_slogan_mark_v4.mp3` — voce dello slogan da sola.
- `jingle_sigla.py` — come è fatto il jingle: 150 BPM, coro «aah» + ottoni + glockenspiel cantano la melodia sulle sillabe Brin-di TU · Gui-do i-O (Mi-Sol-DO · La-Sol-Sol-DO), poi piano + basso e la voce; campioni veri FluidR3 (gleitz/midi-js-soundfonts), scaricati in automatico.
  Rifarlo: `python3 jingle_sigla.py <cartella_campioni> <voce.wav> - out.wav` (voce = slogan con atempo 1.12).
- `sigla_logo.html` — animazione del logo (`render.mjs sigla_logo.html?hit=3.2 frames 3.95 out.mp4`).

**Voce:** Mark = modello `elevenlabs_v4`, preset `27c04473-84a9-4b60-a41f-c8e8458bd4f1`.
Attenzione: lo stesso preset con `text2speech_v2` (variant elevenlabs) suona diverso e Marco l'ha bocciato.

**Montaggio del reel (stile approvato):** voce Mark v4 accelerata ×1,15, scene corte (voce + 0,3 s), musica sotto con ducking, sigla in fondo, nessuna coda di silenzio così Instagram riparte subito dal gancio (loop). Niente frasi di loop parlate: suonano male.
