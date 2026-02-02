async function getKV(context) {
  // 1. Native binding (No token needed)
  if (context.env.BLOG_KV) return context.env.BLOG_KV;

  // 2. Fallback to REST API (Token needed)
  const {
    CLOUDFLARE_KV_NAMESPACE_ID: id,
    CLOUDFLARE_API_TOKEN: token,
    CLOUDFLARE_ACCOUNT_ID: account
  } = context.env;

  if (id && token && account) {
    const baseUrl = `https://api.cloudflare.com/client/v4/accounts/${account}/storage/kv/namespaces/${id}/values`;
    return {
      get: async (key) => {
        const res = await fetch(`${baseUrl}/${key}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        return res.ok ? await res.text() : null;
      },
      put: async (key, value) => {
        await fetch(`${baseUrl}/${key}`, {
          method: 'PUT',
          headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'text/plain' },
          body: value
        });
      }
    };
  }
  return null; // No KV available
}

export async function onRequest(context) {
  const kv = await getKV(context);

  if (!kv) {
    // If KV is not set up, just return a graceful message or empty data
    if (context.request.method === 'POST') {
      return new Response(JSON.stringify({ views: 0, note: 'KV not bound' }), {
        headers: { 'Content-Type': 'application/json' }
      });
    }
    return new Response(JSON.stringify({ views: 0 }), { headers: { 'Content-Type': 'application/json' } });
  }

  if (context.request.method === 'POST') {
    try {
      const { id } = await context.request.json();
      if (!id) return new Response('Bad Request', { status: 400 });

      const key = `views:${id}`;
      const current = await kv.get(key) || '0';
      const next = parseInt(current) + 1;
      await kv.put(key, next.toString());

      return new Response(JSON.stringify({ views: next }), {
        headers: { 'Content-Type': 'application/json' }
      });
    } catch (e) {
      return new Response(JSON.stringify({ views: 0, error: e.message }), { status: 200 });
    }
  }

  const { searchParams } = new URL(context.request.url);
  const id = searchParams.get('id');
  if (id) {
    const views = await kv.get(`views:${id}`) || '0';
    return new Response(JSON.stringify({ views }), { headers: { 'Content-Type': 'application/json' } });
  }

  return new Response('Not Found', { status: 404 });
}
