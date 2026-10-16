// Legge i dati del brand da produzione/brand/brand.json (colori, font, nome, handle).
import fs from 'fs';
export default JSON.parse(fs.readFileSync(new URL('../brand/brand.json', import.meta.url), 'utf8'));
