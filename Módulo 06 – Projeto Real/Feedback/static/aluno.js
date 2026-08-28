const app = document.querySelector('#aluno-app');
let perguntaAtual = 0;
async function estado() {
  const resposta = await fetch(`/api/aluno/${window.FEEDBACK_CODIGO}/estado`);
  const dados = await resposta.json();
  if (dados.encerrada) { app.innerHTML = '<div class="alert success">Este feedback foi encerrado. Obrigado!</div>'; return; }
  if (!dados.pergunta) return;
  if (dados.pergunta.ordem !== perguntaAtual || !document.querySelector('#responder-form')) renderizar(dados);
}
function renderizar(dados) {
  perguntaAtual = dados.pergunta.ordem;
  const entrada = dados.pergunta.tipo === 'nota'
    ? `<div class="notas">${Array.from({length: 11}, (_, i) => `<button type="button" class="nota" data-nota="${i}">${i}</button>`).join('')}</div>`
    : '<textarea id="resposta" maxlength="2000" rows="6" placeholder="Escreva sua resposta"></textarea>';
  app.innerHTML = `<p class="muted">Pergunta ${dados.pergunta.ordem}</p><h2>${dados.pergunta.texto}</h2>${dados.pergunta.escala ? `<p class="escala">📏 Escala: ${dados.pergunta.escala}</p>` : ''}<form id="responder-form">${entrada}<button type="submit">Enviar resposta</button><p id="mensagem" class="muted"></p></form>`;
  document.querySelectorAll('.nota').forEach(botao => botao.onclick = () => { document.querySelectorAll('.nota').forEach(b => b.classList.remove('selecionada')); botao.classList.add('selecionada'); });
  document.querySelector('#responder-form').onsubmit = enviar;
}
async function enviar(evento) {
  evento.preventDefault();
  const selecionada = document.querySelector('.nota.selecionada');
  const texto = selecionada ? selecionada.dataset.nota : document.querySelector('#resposta').value.trim();
  const resposta = await fetch(`/api/aluno/${window.FEEDBACK_CODIGO}/responder`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({resposta: texto})});
  const dados = await resposta.json();
  document.querySelector('#mensagem').textContent = dados.ok ? 'Resposta registrada. Aguarde a próxima pergunta.' : dados.erro;
  if (dados.ok) document.querySelectorAll('#responder-form input, #responder-form textarea, #responder-form button').forEach(c => c.disabled = true);
}
estado(); setInterval(estado, 2000);
