export async function onRequest(context) {
  if (context.request.method === 'POST') {
    const { url } = await context.request.json();
    if (!url) return new Response('Bad Request', { status: 400 });

    // Increment view count in KV
    const key = `views:${url}`;
    const current = await context.env.BLOG_KV.get(key) || '0';
    const next = parseInt(current) + 1;
    await context.env.BLOG_KV.put(key, next.toString());

    return new Response(JSON.stringify({ views: next }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  // GET stats for admin
  const { searchParams } = new URL(context.request.url);
  const url = searchParams.get('url');
  if (url) {
    const views = await context.env.BLOG_KV.get(`views:${url}`) || '0';
    return new Response(JSON.stringify({ views }), { headers: { 'Content-Type': 'application/json' } });
  }

  return new Response('Not Found', { status: 404 });
}
