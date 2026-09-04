function corDaMedia(media) { return media === null ? '#9ca3af' : media <= 4 ? '#dc2626' : media <= 7 ? '#eab308' : '#16a34a'; }
function criarGraficoNotas(canvas, notas) {
  return new Chart(canvas.getContext('2d'), {type:'bar', data:{labels:[...Array(11).keys()], datasets:[{label:'Quantidade de respostas',data:notas,backgroundColor:'#4f46e5',borderRadius:6}]}, options:{responsive:true, scales:{y:{beginAtZero:true,ticks:{stepSize:1}},x:{title:{display:true,text:'Nota'}}}}});
}
function criarGraficoMedia(canvas, media) {
  return new Chart(canvas.getContext('2d'), {type:'bar', data:{labels:['Média'],datasets:[{label:media === null?'Sem respostas':`Média: ${media}`,data:[media || 0],backgroundColor:corDaMedia(media),borderRadius:8}]},options:{responsive:true,scales:{y:{min:0,max:10,ticks:{stepSize:1}},x:{title:{display:true,text:'Escala de 0 a 10'}}}}});
}
function escaparHtml(valor) {
  return String(valor).replace(/[&<>'"]/g, caractere => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[caractere]));
}
async function carregarRelatorio() {
  if (window.RELATORIO_GERAL) {
    const d = await (await fetch('/api/professor/relatorio-geral/dados')).json();
    document.querySelector('#respostas-gerais').textContent=d.respostas; document.querySelector('#media-geral').textContent=d.media ?? '—';
    criarGraficoNotas(document.querySelector('#grafico-geral'), d.notas); criarGraficoMedia(document.querySelector('#grafico-media-geral'), d.media); return;
  }
  const d = await (await fetch(`/api/professor/${window.FEEDBACK_CODIGO}/${window.FEEDBACK_TOKEN}/relatorio`)).json();
  const area = document.querySelector('#relatorios');
  area.innerHTML = `<section class="card"><h2>🌎 Geral da sessão</h2><p class="muted">Todas as respostas de nota desta sessão reunidas.</p><div class="charts"><div class="chart-wrap"><canvas id="grafico-sessao"></canvas></div><div class="chart-wrap"><canvas id="grafico-media-sessao"></canvas></div></div></section><h2 class="section-title">📋 Gráficos por pergunta</h2>`;
  criarGraficoNotas(document.querySelector('#grafico-sessao'), d.notas_gerais); criarGraficoMedia(document.querySelector('#grafico-media-sessao'), d.media_geral);
  d.perguntas.forEach((p, i) => {
    if (p.tipo !== 'nota') return;
    area.insertAdjacentHTML('beforeend', `<section class="card report-question"><h2>${p.ordem}. ${escaparHtml(p.pergunta)}</h2><p class="escala">📏 Escala: ${p.escala || '0 a 10'}</p><p class="muted">${p.respostas} resposta(s) · Média: ${p.media ?? '—'}</p><div class="charts"><div class="chart-wrap"><canvas id="pergunta-${i}"></canvas></div><div class="chart-wrap"><canvas id="media-${i}"></canvas></div></div></section>`);
    criarGraficoNotas(document.querySelector(`#pergunta-${i}`),p.notas);
    criarGraficoMedia(document.querySelector(`#media-${i}`),p.media);
  });
}
carregarRelatorio();
