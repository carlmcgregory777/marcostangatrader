# Jingle GUIDO IO. «Brindi tu. Guido io!» con strumenti campionati veri (soundfont FluidR3, gleitz/midi-js-soundfonts).
# Battuta 1: coro «aah» + ottoni cantano la melodia sulle sillabe Brin-di TU · Gui-do i-O.
# Battuta 2: piano e basso, Mark dice lo slogan; «io» cade sull'accordo finale pieno (coro + ottoni + glockenspiel).
# Uso: python3 jingle_sf.py <cartella_campioni> <voce_slogan.wav> <voce_loop.wav|-> <out.wav>
import numpy as np, wave, sys, os, subprocess, urllib.request
D, VOICE, LOOP, OUT = sys.argv[1:5]
SR = 44100; BPM = 150; B = 60 / BPM; E = B / 2; HIT = 8 * B
NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
def nn(m): return f"{NAMES[m % 12]}{m // 12 - 1}"
_cache = {}
def sample(inst, m):
    k = (inst, m)
    if k in _cache: return _cache[k]
    mp3 = os.path.join(D, f"{inst}_{nn(m)}.mp3"); wav = mp3[:-4] + ".wav"
    if not os.path.exists(mp3):
        urllib.request.urlretrieve(f"https://gleitz.github.io/midi-js-soundfonts/FluidR3_GM/{inst}-mp3/{nn(m)}.mp3", mp3)
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp3, "-ac", "1", "-ar", str(SR), wav], check=True)
    w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
    _cache[k] = x; return x
LOOPLEN = 2.2 if LOOP != "-" else 0
DUR = HIT + 0.75 + LOOPLEN
N = int(DUR * SR); bus = {k: np.zeros(N) for k in ("mel", "piano", "bass", "glock", "perc", "voice")}
def note(busk, inst, m, s, d, amp=1.0, rel=0.25):
    x = sample(inst, m)[: int((d + rel) * SR)].copy()
    n = len(x); r = int(rel * SR)
    if n > r: x[n - r:] *= np.linspace(1, 0, r)
    i = int(s * SR); e = min(N, i + n); bus[busk][i:e] += x[: e - i] * amp
SYL = [(0, 1, 76), (1, 1, 79), (2, 2, 84), (4, 1, 81), (5, 1, 79), (6, 1, 79), (7, 1, 84)]
for s8, d8, m in SYL:
    note("mel", "choir_aahs", m, s8 * E, d8 * E, 1.0, 0.12)
    note("mel", "brass_section", m, s8 * E, d8 * E * 0.9, 0.55, 0.08)
    note("glock", "glockenspiel", m + 12, s8 * E, d8 * E, 0.35, 0.4)
CH = {0: [60, 64, 67], 1: [60, 64, 67], 2: [65, 69, 72], 3: [67, 71, 74],
      4: [60, 64, 67], 5: [57, 60, 64], 6: [65, 69, 72], 7: [67, 71, 74]}
BASS = {0: 36, 1: 36, 2: 41, 3: 43, 4: 36, 5: 33, 6: 41, 7: 43}
for b in range(8):
    for m in CH[b]: note("piano", "bright_acoustic_piano", m, b * B + E, E * 0.8, 0.45, 0.1)  # «pa» in controtempo
    note("bass", "electric_bass_finger", BASS[b], b * B, B * 0.85, 0.9, 0.08)
# percussione leggera: legnetto sui tempi 2 e 4
for b in range(1, 8, 2): note("perc", "woodblock", 72, b * B, 0.15, 0.25, 0.05)
# accordo finale pieno
for m in [48, 60, 64, 67, 72]: note("piano", "bright_acoustic_piano", m, HIT, 1.3, 0.6, 0.5)
for m in [72, 76, 79]: note("mel", "choir_aahs", m, HIT, 1.2, 0.7, 0.5)
for m in [67, 72, 76]: note("mel", "brass_section", m, HIT, 0.5, 0.45, 0.3)
note("glock", "glockenspiel", 96, HIT, 1.0, 0.5, 0.6); note("bass", "electric_bass_finger", 36, HIT, 1.2, 0.9, 0.4)
def loadv(p):
    w = wave.open(p); v = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    if w.getnchannels() == 2: v = v.reshape(-1, 2).mean(1)
    return v / (np.max(np.abs(v)) + 1e-9)
v = loadv(VOICE); vs = HIT - len(v) / SR + 0.1
i = int(vs * SR); bus["voice"][i:i + len(v)] += v[: N - i]
if LOOP != "-":
    lv = loadv(LOOP); i = int((HIT + 1.0) * SR); bus["voice"][i:i + len(lv)] += lv[: N - i] * 0.95
music = bus["mel"] * 0.5 + bus["piano"] * 0.55 + bus["bass"] * 0.7 + bus["glock"] * 0.5 + bus["perc"] * 0.6
env = np.convolve(np.abs(bus["voice"]), np.ones(2500) / 2500, "same"); duck = 1 - 0.5 * np.minimum(1, env * 6)
rng = np.random.default_rng(2); n = int(1.3 * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 3.5)
F = 1 << (N + n - 1).bit_length(); y = np.fft.irfft(np.fft.rfft(music, F) * np.fft.rfft(ir, F), F)[:N]
music = music + 0.15 * y / np.max(np.abs(y)) * np.max(np.abs(music))
out = music * duck + bus["voice"] * 1.0
out = out / np.max(np.abs(out)) * 0.9
fd = int(0.35 * SR); out[-fd:] *= np.linspace(1, 0, fd)
st = np.stack([out, np.roll(out, int(0.008 * SR))], 1)
w = wave.open(OUT, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
print(f"HIT={HIT:.3f} DUR={DUR:.3f} voce_da={vs:.2f}")
