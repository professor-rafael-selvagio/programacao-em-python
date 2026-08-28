# Feedback de Turmas

Aplicação web didática para o professor conduzir uma pesquisa com perguntas liberadas uma por vez. Os alunos respondem pelo navegador, e o professor acompanha resultados consolidados em tempo real.

## Instalação

No terminal, entre nesta pasta e crie um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows, ative o ambiente com `.venv\Scripts\activate`.

## Execução

```bash
python app.py
```

Abra `http://127.0.0.1:5454` no computador do professor. A aplicação escuta em `0.0.0.0:5454`, portanto pode ser acessada por outros dispositivos da mesma rede. O login do professor é solicitado antes da área de controle.

Login padrão do professor:

- E-mail: `professor.rafael.selvagio@gmail.com`
- Senha: `Dets5000`

Para produção, altere essas credenciais usando as variáveis `PROFESSOR_LOGIN` e `PROFESSOR_SENHA`.

O banco `banco.db` é criado automaticamente e não deve ser versionado. O SQLite é mais adequado que um CSV para respostas simultâneas porque oferece transações, restrições de unicidade e gravações concorrentes controladas. O CSV continua sendo usado apenas como entrada simples das perguntas.

## Como usar

1. Informe o nome da turma.
2. Se quiser, envie um CSV com as colunas `id,tipo,pergunta`. Sem upload, serão usadas as perguntas de `perguntas.csv`.
3. Compartilhe o link de aluno exibido na tela de controle.
4. Os alunos informam opcionalmente o nome e respondem à pergunta atual.
5. Use **Próxima pergunta** para liberar a próxima questão. As telas dos alunos consultam o estado automaticamente a cada dois segundos.
6. Na área **Sessões**, abra os gráficos por pergunta, o gráfico geral da sessão ou o gráfico geral consolidado de todos os feedbacks.
7. Use **Encerrar feedback** ao terminar.

Na tela de sessões, use **Bloquear** para proteger uma sessão. Uma sessão bloqueada não será removida pelo botão **Limpar banco**; ela pode ser desbloqueada quando necessário. A limpeza exige confirmação e remove somente as sessões desprotegidas, junto com suas respostas.

As respostas usam um identificador interno do navegador para impedir duplicidade, mas esse identificador e os nomes não aparecem nos resultados. A tela do professor acompanha somente perguntas de nota, com contagens, média e distribuição. Respostas abertas ficam salvas no banco para uma consulta posterior, sem monitoramento durante a aplicação.

## Acesso pela rede local

Descubra o IP do computador do professor:

- macOS/Linux: `ifconfig` ou `ip addr`;
- Windows: `ipconfig`.

Se o IP for `192.168.0.10`, os alunos acessam `http://192.168.0.10:5000`. Todos devem estar na mesma rede. Se não abrir, confira se a rede permite comunicação entre dispositivos e autorize o Python ou a porta 5000 no firewall. Em redes públicas ou corporativas, o isolamento de clientes pode impedir esse acesso.

## Formato do CSV

```csv
id,tipo,pergunta
1,nota,"De 0 a 10, quanto você avalia o conteúdo?"
2,aberta,"O que poderia ser melhorado?"
```

`tipo` deve ser exatamente `nota` ou `aberta`. Perguntas de nota aceitam somente valores inteiros de 0 a 10; respostas abertas aceitam até 2.000 caracteres.
