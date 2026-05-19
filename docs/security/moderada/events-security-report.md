# Relatório de Inspeção de Cibersegurança (MODERADA) - UAB Eventos

## 1. Resumo Executivo
Esta inspeção de nível moderado focou no ciclo de vida dos eventos, abrangendo desde a criação e visualização até o fluxo de aprovação e exclusão. O sistema apresenta uma estrutura sólida com uso de ORM e auto-escaping em templates, o que previne a maioria das falhas de Injeção de SQL e XSS simples. No entanto, foram detectadas falhas significativas em **Controle de Acesso Quebrado (Broken Access Control)** e **Divulgação de Informações**, onde dados sensíveis (eventos pendentes ou indeferidos) estão acessíveis a usuários não autorizados ou anônimos por meio de referências diretas ou rotas públicas.

## 2. Quantidade de Achados por Severidade
- **Crítica**: 0
- **Alta**: 2
- **Média**: 3
- **Baixa**: 1

---

## 3. Detalhamento dos Achados

### 3.1 Acesso Público a Detalhes de Eventos Sensíveis (IDOR / BFLA)
- **Localização**: `app/routes/eventos.py` (rota `/events/<int:id>`).
- **Descrição**: A rota de detalhes do evento não exige autenticação nem valida o status do evento antes de exibi-lo.
- **Evidência**: `def detalhes_evento(id)` não possui decorators de proteção. Um usuário anônimo pode visualizar detalhes de eventos `PENDENTE` ou `INDEFERIDO` se souber o ID.
- **Impacto**: Divulgação de informações institucionais privadas, como justificativas de indeferimento ou rascunhos de eventos.
- **Severidade**: **ALTA**
- **Recomendação**: Implementar `@login_required` e garantir que usuários não-administrativos vejam apenas eventos `DEFERIDO`.
- **CWE**: CWE-639 (IDOR), CWE-285

### 3.2 Listagem Pública de Eventos Não Aprovados
- **Localização**: `app/routes/eventos.py` (rota `/events`).
- **Descrição**: A rota de listagem (Agenda Modo Lista) exibe todos os eventos (Pendente, Deferido, Indeferido) para qualquer pessoa que acesse a URL.
- **Evidência**: `listar_eventos()` chama `EventoService.listar_eventos_por_perfil(session.get('user_role'))`, mas a rota em si não é protegida e o serviço retorna todos os eventos se o papel for nulo ou não validado.
- **Impacto**: Vazamento de toda a fila de solicitações e rejeições da instituição para o público externo.
- **Severidade**: **ALTA**
- **Recomendação**: Restringir a exibição de eventos `PENDENTE` e `INDEFERIDO` apenas para usuários autenticados com papéis de `ADMINISTRADOR` ou `SECRETARIO`.
- **CWE**: CWE-284

### 3.3 Falta de Sanitização na Entrada de Dados (XSS Persistente)
- **Localização**: `app/routes/eventos.py` (método `criar_evento`) e `app/services/evento_service.py`.
- **Descrição**: Embora o Jinja2 escape a saída, não há sanitização na entrada para campos de texto como `titulo` e `descricao`.
- **Evidência**: Os dados do formulário são passados diretamente para o modelo sem limpeza de tags HTML ou scripts.
- **Impacto**: Se um administrador desativar acidentalmente o auto-escape em algum template futuro ou se os dados forem consumidos por uma API externa insegura, scripts maliciosos podem ser executados.
- **Severidade**: **MÉDIA**
- **Recomendação**: Utilizar uma biblioteca como `Bleach` para limpar entradas de texto durante a criação/edição.
- **CWE**: CWE-79

### 3.4 Enumeração de Dados via IDs Sequenciais
- **Localização**: `app/routes/eventos.py` (detalhes e exclusão).
- **Descrição**: O uso de IDs inteiros sequenciais para eventos facilita a varredura (scraping) de todo o banco de dados.
- **Evidência**: Referências diretas a `<int:id>`.
- **Impacto**: Um atacante pode iterar de 1 a N para descobrir todos os eventos registrados no sistema.
- **Severidade**: **MÉDIA**
- **Recomendação**: Considerar o uso de UUIDs para identificadores públicos ou implementar rate limiting rigoroso para evitar varredura.
- **CWE**: CWE-209

### 3.5 Manipulação Insegura de Caminho de Arquivo (Path Traversal)
- **Localização**: `app/templates/events/approve.html` (link para Ofício).
- **Descrição**: O link para o ofício aponta diretamente para o sistema de arquivos estáticos.
- **Evidência**: `url_for('static', filename='uploads/' + (evento.oficio_path or ''))`.
- **Impacto**: Embora o `upload_service` use `secure_filename`, a exposição direta de arquivos na pasta static pode permitir o acesso a arquivos de outros eventos se os nomes forem previsíveis.
- **Severidade**: **MÉDIA**
- **Recomendação**: Servir arquivos privados através de uma rota autenticada que verifique se o usuário tem permissão para ver aquele anexo específico.
- **CWE**: CWE-22

### 3.6 Ausência de Logs de Auditoria para Decisões Críticas
- **Localização**: `app/services/evento_service.py` (método `processar_decisao`).
- **Descrição**: O sistema altera o status de aprovação de eventos sem registrar o log de quem realizou a ação além do campo no banco de dados.
- **Evidência**: Não há chamadas a um sistema de logging persistente para auditoria de segurança.
- **Impacto**: Dificuldade em rastrear ações maliciosas ou indevidas em caso de comprometimento de conta de secretário.
- **Severidade**: **BAIXA**
- **Recomendação**: Implementar logs de aplicação (ex: Python `logging`) para todas as mudanças de status de eventos.
- **CWE**: CWE-778

---

## 4. Plano de Ação Recomendado (Ações Prioritárias)

1.  **Blindagem da Rota de Detalhes**: Adicionar `@login_required` e filtro de status na rota `/events/<id>`.
2.  **Segregação da Listagem de Agenda**: Alterar `listar_eventos()` para filtrar resultados com base na autenticação (Anônimo = apenas Deferidos).
3.  **Proteção de Anexos**: Mover a pasta `uploads` para fora da pasta `static` e criar uma rota protegida para download.
4.  **Sanitização de Input**: Implementar limpeza de HTML em todos os campos de texto livre.
5.  **Hardening de IDs**: Adicionar uma camada de validação ou UUIDs para dificultar a enumeração.
