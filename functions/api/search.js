async function getKV(context) {
  if (context.env.BLOG_KV) return context.env.BLOG_KV;

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
      }
    };
  }
  return null;
}

export async function onRequest(context) {
  const { searchParams } = new URL(context.request.url);
  const query = searchParams.get('q')?.toLowerCase();
  const lang = searchParams.get('lang') || 'jp';

  if (!query) return new Response('[]', { headers: { 'Content-Type': 'application/json' } });

  let metadata = [];
  const kv = await getKV(context);

  if (kv) {
    const metadataRaw = await kv.get('metadata');
    if (metadataRaw) {
      metadata = JSON.parse(metadataRaw);
    }
  }

  // Fallback to static file if KV fails or is empty
  if (metadata.length === 0) {
    const url = new URL(context.request.url);
    const staticRes = await fetch(`${url.origin}/metadata.json`);
    if (staticRes.ok) {
      metadata = await staticRes.json();
    }
  }

  const results = metadata.filter(p =>
    p.lang === lang &&
    (p.title.toLowerCase().includes(query) || (p.description && p.description.toLowerCase().includes(query)))
  ).slice(0, 10);

  return new Response(JSON.stringify(results), {
    headers: { 'Content-Type': 'application/json' }
  });
}
