// Laddar upp data/current.json och, om den finns, data/klorofyll.json till Vercel Blob. Kräver BLOB_READ_WRITE_TOKEN.
// Används av .github/workflows/refresh.yml. Token ger bara åtkomst till Blob-storen.
import { access, readFile } from 'node:fs/promises';
import { put } from '@vercel/blob';

async function upload(name, required) {
  const file = new URL(`../data/${name}`, import.meta.url);
  if (!required && !(await access(file).then(() => true, () => false))) {
    console.log(`Hoppar över ${name}, filen finns inte`);
    return;
  }
  const body = await readFile(file);
  JSON.parse(body); // avbryt hellre än att ladda upp trasig JSON
  const blob = await put(`oresund/${name}`, body, {
    access: 'public',
    addRandomSuffix: false,
    allowOverwrite: true,
    cacheControlMaxAge: 300,
    contentType: 'application/json',
  });
  console.log(`Uppladdad: ${blob.url}`);
}

await upload('current.json', true);
await upload('klorofyll.json', false);
