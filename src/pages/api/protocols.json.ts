import fs from 'node:fs';
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  const fileUrl = new URL('../../../docs/api/protocols.json', import.meta.url);
  const buffer = fs.readFileSync(fileUrl);
  return new Response(buffer, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
};
