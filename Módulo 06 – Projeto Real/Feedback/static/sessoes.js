document.querySelectorAll('[data-bloquear]').forEach(botao => botao.onclick = async () => {
  const acao = botao.textContent.trim() === 'Bloquear' ? 'bloquear' : 'desbloquear';
  if (!confirm(`${acao[0].toUpperCase() + acao.slice(1)} esta sessão?`)) return;
  const r = await fetch(`/api/professor/sessao/${botao.dataset.codigo}/${botao.dataset.token}/bloquear`, {method: 'POST'});
  if (r.ok) location.reload();
});
document.querySelector('#limpar-banco').onclick = async () => {
  if (!confirm('Limpar o banco apagará todas as sessões desbloqueadas e suas respostas. As sessões bloqueadas serão preservadas. Continuar?')) return;
  const r = await fetch('/api/professor/banco/limpar', {method: 'POST'});
  const d = await r.json();
  if (r.ok) { alert(`${d.removidas} sessão(ões) removida(s).`); location.reload(); }
  else alert(d.erro || 'Não foi possível limpar o banco.');
};
