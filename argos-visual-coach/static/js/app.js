// ── Clock ──────────────────────────────────────────────
function updateClock() {
  const now = new Date();
  const el = document.getElementById('clock');
  if (el) el.textContent = now.toTimeString().split(' ')[0];
}
setInterval(updateClock, 1000);
updateClock();

// ── Navigation ─────────────────────────────────────────
function goPage(page, el) {
  document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  const pg = document.getElementById('pg-' + page);
  if (pg) pg.classList.add('active');
  if (el) el.classList.add('active');
}

// ── Tab Prédios ────────────────────────────────────────
document.querySelectorAll('.tab-predio').forEach(tab => {
  tab.addEventListener('click', function () {
    document.querySelectorAll('.tab-predio').forEach(t => t.classList.remove('active'));
    this.classList.add('active');

    // volta para o painel
    document.querySelectorAll('.page-view').forEach(p => p.classList.remove('active'));
    document.getElementById('pg-dashboard').classList.add('active');
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelectorAll('.nav-item')[0].classList.add('active');

    const predio = this.dataset.predio;
    filterAmbientes(predio);
  });
});

function filterAmbientes(predio) {
  const cards = document.querySelectorAll('#grid-amb .card-ambiente');
  const title = document.getElementById('sec-ambientes');
  cards.forEach(c => {
    c.style.display = 'block';
  });
  if (title) {
    title.textContent = predio === 'todos'
      ? 'AMBIENTES MONITORADOS — TODOS OS PRÉDIOS'
      : `AMBIENTES — PRÉDIO ${predio}`;
  }
  // visual filter only (all buildings share same environments)
}

// ── Modal Ambiente ──────────────────────────────────────
function openAmbModal(el) {
  const data = JSON.parse(el.dataset.json);
  const statusLabel = { ok: 'NORMAL', warn: 'ATENÇÃO', crit: 'CRÍTICO' };
  const statusColor = { ok: 'var(--green)', warn: 'var(--yellow)', crit: 'var(--red)' };

  document.getElementById('m-icon').textContent  = data.icon;
  document.getElementById('m-title').textContent = data.nome;
  document.getElementById('m-sub').textContent   = data.detalhe + ' · Argos Visual Coach';

  document.getElementById('m-grid').innerHTML = `
    <div class="info-block">
      <div class="info-block-label">OCUPAÇÃO</div>
      <div class="info-block-val">${data.pessoas} / ${data.cap}</div>
    </div>
    <div class="info-block">
      <div class="info-block-label">CÂMERAS</div>
      <div class="info-block-val">${data.cameras} ativas</div>
    </div>
    <div class="info-block">
      <div class="info-block-label">STATUS</div>
      <div class="info-block-val" style="color:${statusColor[data.status]}">${statusLabel[data.status]}</div>
    </div>
    <div class="info-block">
      <div class="info-block-label">PRÉDIOS</div>
      <div class="info-block-val">A · B · C · D</div>
    </div>
  `;
  document.getElementById('overlay').classList.add('open');
}

// ── Modal Câmera ────────────────────────────────────────
function openCamModal(el) {
  const data = JSON.parse(el.dataset.json);

  document.getElementById('m-icon').textContent  = data.icon;
  document.getElementById('m-title').textContent = data.nome;
  document.getElementById('m-sub').textContent   = data.predio + ' · Argos Visual Coach';

  document.getElementById('m-grid').innerHTML = `
    <div class="info-block">
      <div class="info-block-label">RESOLUÇÃO</div>
      <div class="info-block-val">${data.res}</div>
    </div>
    <div class="info-block">
      <div class="info-block-label">FPS</div>
      <div class="info-block-val">${data.fps}</div>
    </div>
    <div class="info-block">
      <div class="info-block-label">UPTIME</div>
      <div class="info-block-val">${data.uptime}</div>
    </div>
    <div class="info-block">
      <div class="info-block-label">EVENTOS</div>
      <div class="info-block-val">${data.eventos} hoje</div>
    </div>
  `;
  document.getElementById('overlay').classList.add('open');
}

function closeModal(e) {
  if (!e || e.target === document.getElementById('overlay')) {
    document.getElementById('overlay').classList.remove('open');
  }
}

// ── Live polling /api/status ────────────────────────────
async function pollStatus() {
  try {
    const resp = await fetch('/api/status');
    const data = await resp.json();
    const el = document.getElementById('m-pessoas');
    if (el) el.textContent = data.total_pessoas;

    const lu = document.getElementById('last-update');
    if (lu) lu.textContent = 'Última atualização: ' + data.timestamp;
  } catch (e) { /* silencioso */ }
}
setInterval(pollStatus, 8000);

// ── Server IP display ───────────────────────────────────
const ipEl = document.getElementById('server-ip');
if (ipEl) ipEl.textContent = window.location.host;

// ── PWA service worker ──────────────────────────────────
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/static/sw.js').catch(() => {});
}
