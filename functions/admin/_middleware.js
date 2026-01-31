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

    // Login page
    return new Response(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>Admin Login</title>
        <script src="https://cdn.tailwindcss.com"></script>
      </head>
      <body class="bg-gray-100 flex items-center justify-center h-screen">
        <form method="POST" class="bg-white p-8 rounded-lg shadow-md w-96">
          <h1 class="text-2xl font-bold mb-6">Admin Login</h1>
          <input type="password" name="password" placeholder="Password" class="w-full border p-2 rounded mb-4">
          <button type="submit" class="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Login</button>
        </form>
      </body>
      </html>
    `, {
      headers: { 'Content-Type': 'text/html' }
    });
  }

  return await context.next();
}
