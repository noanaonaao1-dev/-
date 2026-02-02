export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.pathname.startsWith('/admin')) {
    const cookie = context.request.headers.get('Cookie') || '';
    if (cookie.includes('auth=true')) {
      return await context.next();
    }

    if (context.request.method === 'POST') {
      const formData = await context.request.formData();
      const password = formData.get('password');

      if (password === context.env.ADMIN_PASSWORD) {
        return new Response('Authenticated', {
          status: 302,
          headers: {
            'Location': '/admin/',
            'Set-Cookie': 'auth=true; Path=/; HttpOnly; SameSite=Strict'
          }
        });
      }
    }

    // Login page (Japanese)
    return new Response(`
      <!DOCTYPE html>
      <html lang="ja">
      <head>
        <meta charset="UTF-8">
        <title>管理者ログイン - PROG-AUTO-LAB</title>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body class="bg-slate-100 flex items-center justify-center h-screen font-sans">
        <form method="POST" class="bg-white p-10 rounded-3xl shadow-xl w-96 border border-slate-200">
          <h1 class="text-2xl font-black mb-8 text-slate-900 tracking-tighter">管理者ログイン</h1>
          <div class="mb-6">
            <label class="block text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">パスワード</label>
            <input type="password" name="password" placeholder="••••••••" class="w-full border-slate-200 border p-3 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all">
          </div>
          <button type="submit" class="w-full bg-slate-900 text-white p-3 rounded-xl font-bold hover:bg-slate-800 transition-colors shadow-lg shadow-slate-200">
            ログイン
          </button>
          <p class="text-center mt-8">
            <a href="/" class="text-xs text-slate-400 hover:text-slate-600">← サイトに戻る</a>
          </p>
        </form>
      </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html; charset=UTF-8' }
    });
  }

  return await context.next();
}
