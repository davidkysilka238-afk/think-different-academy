import './style.css';

document.querySelector('#app').innerHTML = `
  <section class="hero" aria-labelledby="page-title">
    <div class="hero__glow" aria-hidden="true"></div>
    <h1 id="page-title">Think different Academy</h1>
    <p class="health-status" aria-live="polite">Status: Loading...</p>
    <p class="health-status team-info" aria-live="polite">Team: Loading...</p>
    <form class="member-form">
      <label for="member-name">Add a team member</label>
      <div class="member-form__controls">
        <input id="member-name" name="name" type="text" maxlength="100" required />
        <button type="submit">Save member</button>
      </div>
      <p class="form-status" aria-live="polite"></p>
    </form>
  </section>
`;

const healthStatus = document.querySelector('.health-status');
const teamInfo = document.querySelector('.team-info');
const memberForm = document.querySelector('.member-form');
const memberName = document.querySelector('#member-name');
const formStatus = document.querySelector('.form-status');
const saveButton = memberForm.querySelector('button[type="submit"]');

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

async function loadTeam() {
  const response = await fetch('/api/v1/team');
  if (!response.ok) {
    throw new Error(`Team request failed with HTTP ${response.status}`);
  }
  const { team, members } = await response.json();
  teamInfo.textContent = `${team} | ${members.join(', ')}`;
}

loadTeam().catch(() => {
  teamInfo.textContent = 'Team data unavailable';
});

memberForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  saveButton.disabled = true;
  formStatus.textContent = 'Saving...';

  try {
    const response = await fetch('/api/v1/team/members', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: memberName.value }),
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.error || `Request failed with HTTP ${response.status}`);
    }

    memberForm.reset();
    formStatus.textContent = `${result.name} was saved to the database.`;
    try {
      await loadTeam();
    } catch {
      formStatus.textContent = `${result.name} was saved, but the team display could not be refreshed.`;
    }
  } catch (error) {
    formStatus.textContent = `Could not save member: ${error.message}`;
  } finally {
    saveButton.disabled = false;
  }
});
