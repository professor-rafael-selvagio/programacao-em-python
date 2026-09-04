const app = document.querySelector('#aluno-app');
let estadoAtual;

async function estado() {
  const resposta = await fetch(`/api/aluno/${window.FEEDBACK_CODIGO}/estado`);
  const dados = await resposta.json();
  if (dados.encerrada) {
    app.innerHTML = '<div class="alert success">Este feedback foi encerrado. Obrigado!</div>' +
                '<img src="/assets/img/exit.jpeg" alt="Feedback encerrado" style="display:block; margin:20px auto; max-width:900px;">';
    return;
  }
  if (!estadoAtual || JSON.stringify(dados) !== JSON.stringify(estadoAtual)) {
    estadoAtual = dados;
    renderizar(dados);
  }
}

function blocoNota(pergunta, respondida) {
  const botoes = Array.from({length: 11}, (_, i) =>
    `<button type="button" class="nota" data-nota="${i}" ${respondida ? 'disabled' : ''}>${i}</button>`
  ).join('');
  return `<article class="question"><p class="muted">Pergunta ${pergunta.ordem} (nota)</p><h2>${pergunta.texto}</h2>${pergunta.escala ? `<p class="escala">📏 Escala: ${pergunta.escala}</p>` : ''}<form data-pergunta-id="${pergunta.id}" class="responder-form"><div class="notas">${botoes}</div><button type="submit" ${respondida ? 'disabled' : ''}>${respondida ? 'Resposta registrada' : 'Enviar resposta'}</button><p class="mensagem muted"></p></form></article>`;
}

function blocoAberta(pergunta) {
  return `<article class="question"><p class="muted">Pergunta ${pergunta.ordem} (aberta)</p><h2>${pergunta.texto}</h2><form data-pergunta-id="${pergunta.id}" class="responder-form"><textarea maxlength="2000" rows="6" placeholder="Escreva sua resposta" ${pergunta.respondida ? 'disabled' : ''}></textarea><button type="submit" ${pergunta.respondida ? 'disabled' : ''}>${pergunta.respondida ? 'Resposta registrada' : 'Enviar resposta'}</button><p class="mensagem muted"></p></form></article>`;
}

function renderizar(dados) {
  const nota = dados.pergunta ? blocoNota(dados.pergunta, dados.respondida) : '';
  const abertas = (dados.perguntas_abertas || []).map(blocoAberta).join('');
  app.innerHTML = `${nota}${abertas || '<p class="muted">Nenhuma pergunta aberta cadastrada.</p>'}`;
  document.querySelectorAll('.nota').forEach(botao => {
    botao.onclick = () => {
      botao.closest('form').querySelectorAll('.nota').forEach(b => b.classList.remove('selecionada'));
      botao.classList.add('selecionada');
    };
  });
  document.querySelectorAll('.responder-form').forEach(form => form.onsubmit = enviar);
}

async function enviar(evento) {
  evento.preventDefault();
  const form = evento.currentTarget;
  const selecionada = form.querySelector('.nota.selecionada');
  const campoTexto = form.querySelector('textarea');
  const texto = selecionada ? selecionada.dataset.nota : campoTexto.value.trim();
  const mensagem = form.querySelector('.mensagem');
  const resposta = await fetch(`/api/aluno/${window.FEEDBACK_CODIGO}/responder`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({pergunta_id: form.dataset.perguntaId, resposta: texto})
  });
  const dados = await resposta.json();
  mensagem.textContent = dados.ok ? 'Resposta registrada.' : dados.erro;
  if (dados.ok) form.querySelectorAll('textarea, .nota, button').forEach(c => c.disabled = true);
}

estado();
setInterval(estado, 2000);
