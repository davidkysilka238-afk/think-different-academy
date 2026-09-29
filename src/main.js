import './style.css';

document.querySelector('#app').innerHTML = `
  <section class="hero" aria-labelledby="page-title">
    <div class="hero__glow" aria-hidden="true"></div>
    <h1 id="page-title">Think different Academy</h1>
    <p class="health-status" aria-live="polite">Status: Loading...</p>
  </section>
`;

const healthStatus = document.querySelector('.health-status');

fetch('/api/v1/health')
  .then((response) => {
    if (!response.ok) {
      throw new Error(`Health check failed with HTTP ${response.status}`);
    }
    return response.json();
  })
  .then(({ status }) => {
    healthStatus.textContent = `Status: ${status.toUpperCase()}`;
  })
  .catch(() => {
    healthStatus.textContent = 'Status: unavailable';
  });
