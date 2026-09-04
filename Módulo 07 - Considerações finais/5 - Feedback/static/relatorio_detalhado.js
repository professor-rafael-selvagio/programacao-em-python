const areaDetalhada = document.querySelector('#detalhado');

function escapar(valor) {
  return String(valor ?? '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
}

async function carregarDetalhado() {
  const resposta = await fetch(`/api/professor/${window.FEEDBACK_CODIGO}/${window.FEEDBACK_TOKEN}/relatorio-detalhado`);
  const dados = await resposta.json();
  if (!resposta.ok) { areaDetalhada.innerHTML = `<p class="alert">${escapar(dados.erro)}</p>`; return; }
  const notas = dados.perguntas.filter(p => p.tipo === 'nota');
  const abertas = dados.perguntas.filter(p => p.tipo === 'aberta');
  if (!dados.alunos.length) { areaDetalhada.innerHTML = '<section class="card"><p class="muted">Nenhuma resposta registrada.</p></section>'; return; }
  areaDetalhada.innerHTML = `<p class="muted">${dados.alunos.length} aluno(s) responderam.</p>` + dados.alunos.map(aluno => {
    const respostas = aluno.respostas;
    return `<section class="card report-question"><h2>👤 ${escapar(aluno.nome)}</h2><h3>Notas</h3><div class="table-wrap"><table><thead><tr><th>Pergunta</th><th>Resposta</th></tr></thead><tbody>${notas.map(p => `<tr><td>${p.ordem + 1}. ${escapar(p.texto)}</td><td>${escapar(respostas[p.id] ?? '—')}</td></tr>`).join('')}</tbody></table></div><h3>Respostas abertas</h3>${abertas.map(p => `<div class="comentario"><strong>${p.ordem + 1}. ${escapar(p.texto)}</strong><p>${respostas[p.id] ? escapar(respostas[p.id]).replace(/\n/g, '<br>') : 'Não respondida.'}</p></div>`).join('')}</section>`;
  }).join('');
}

carregarDetalhado();
