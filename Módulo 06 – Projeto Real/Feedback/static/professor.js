const contexto = document.querySelector('#grafico').getContext('2d');
const contextoMedia = document.querySelector('#grafico-media').getContext('2d');
let grafico, graficoMedia;
async function atualizar() {
  const r = await fetch(`/api/professor/${window.FEEDBACK_CODIGO}/${window.FEEDBACK_TOKEN}/dados`);
  if (!r.ok) return;
  const d = await r.json();
  document.querySelector('#pergunta-num').textContent = `${d.pergunta_atual}/${d.total_perguntas}`;
  document.querySelector('#conectados').textContent = d.conectados;
  document.querySelector('#respostas').textContent = d.respostas;
  document.querySelector('#media').textContent = d.media ?? '—';
  document.querySelector('#pergunta').textContent = d.pergunta || 'Feedback encerrado';
  document.querySelector('#escala').textContent = d.escala ? `📏 Escala: ${d.escala}` : '';
  document.querySelector('#proxima').disabled = d.encerrada || d.pergunta_atual >= d.total_perguntas;
  const graficosNotas = document.querySelector('#graficos-notas');
  const abertaAviso = document.querySelector('#aberta-aviso');
  if (d.tipo === 'nota') {
    graficosNotas.style.display = 'grid'; abertaAviso.style.display = 'none';
    if (grafico) grafico.destroy();
    grafico = new Chart(contexto, {type: 'bar', data: {labels: [...Array(11).keys()], datasets: [{label: 'Quantidade de respostas', data: d.notas, backgroundColor: '#4f46e5', borderRadius: 6}]}, options: {responsive: true, plugins: {legend: {display: true}}, scales: {y: {beginAtZero: true, ticks: {stepSize: 1}}, x: {title: {display: true, text: 'Nota'}}}}});
    if (graficoMedia) graficoMedia.destroy();
    const corMedia = d.media === null ? '#9ca3af' : d.media <= 4 ? '#dc2626' : d.media <= 7 ? '#eab308' : '#16a34a';
    graficoMedia = new Chart(contextoMedia, {type: 'bar', data: {labels: ['Média'], datasets: [{label: d.media === null ? 'Sem respostas' : `Média: ${d.media}`, data: [d.media || 0], backgroundColor: corMedia, borderRadius: 8}]}, options: {responsive: true, plugins: {legend: {display: true}}, scales: {y: {min: 0, max: 10, ticks: {stepSize: 1}}, x: {title: {display: true, text: 'Escala de 0 a 10'}}}}});
  } else {
    graficosNotas.style.display = 'none'; abertaAviso.style.display = 'block'; document.querySelector('#media').textContent = '—';
  }
}
document.querySelector('#proxima').onclick = async () => { await fetch(`/api/professor/${window.FEEDBACK_CODIGO}/${window.FEEDBACK_TOKEN}/proxima`, {method: 'POST'}); atualizar(); };
document.querySelector('#encerrar').onclick = async () => { if (confirm('Deseja encerrar este feedback?')) { await fetch(`/api/professor/${window.FEEDBACK_CODIGO}/${window.FEEDBACK_TOKEN}/encerrar`, {method: 'POST'}); atualizar(); } };
atualizar(); setInterval(atualizar, 2000);
