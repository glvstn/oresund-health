// Laddar upp data/current.json till Vercel Blob. Kräver BLOB_READ_WRITE_TOKEN.
// Används av .github/workflows/refresh.yml. Token ger bara åtkomst till Blob-storen.
import { readFile } from 'node:fs/promises';
import { put } from '@vercel/blob';

const body = await readFile(new URL('../data/current.json', import.meta.url));
JSON.parse(body); // avbryt hellre än att ladda upp trasig JSON
const blob = await put('oresund/current.json', body, {
  access: 'public',
  addRandomSuffix: false,
  allowOverwrite: true,
  cacheControlMaxAge: 300,
  contentType: 'application/json',
});
console.log(`Uppladdad: ${blob.url}`);
