import { defineConfig } from 'vite';

function healthApiMiddleware(_request, response, next) {
  if (_request.url !== '/api/v1/health') {
    next();
    return;
  }

  response.statusCode = 200;
  response.setHeader('Content-Type', 'application/json');
  response.end(JSON.stringify({ status: 'ok' }));
}

export default defineConfig({
  plugins: [
    {
      name: 'health-api',
      configureServer(server) {
        server.middlewares.use(healthApiMiddleware);
      },
      configurePreviewServer(server) {
        server.middlewares.use(healthApiMiddleware);
      },
    },
  ],
});