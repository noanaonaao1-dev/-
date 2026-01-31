export async function onRequest(context) {
  const { searchParams } = new URL(context.request.url);
  const query = searchParams.get('q')?.toLowerCase();
  const lang = searchParams.get('lang') || 'jp';

  if (!query) return new Response(JSON.stringify([]), { headers: { 'Content-Type': 'application/json' } });

  // In Cloudflare, we'd list KV keys or fetch a pre-built index from KV
  // For this implementation, we assume metadata is stored in KV under 'metadata' key
  const metadataRaw = await context.env.BLOG_KV.get('metadata');
  if (!metadataRaw) return new Response(JSON.stringify([]), { headers: { 'Content-Type': 'application/json' } });

  const pages = JSON.parse(metadataRaw);
  const results = pages.filter(p =>
    p.lang === lang &&
    (p.title.toLowerCase().includes(query) || (p.description && p.description.toLowerCase().includes(query)))
  ).slice(0, 10);

  return new Response(JSON.stringify(results), {
    headers: { 'Content-Type': 'application/json' }
  });
}
