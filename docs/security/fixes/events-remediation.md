# Relatório de Remediação de Segurança (MODERADA) - UAB Eventos

Este documento detalha as correções aplicadas para sanar as vulnerabilidades de nível moderado identificadas na inspeção de cibersegurança dos módulos de eventos.

## 1. Vulnerabilidades Corrigidas

### 1.1 Controle de Acesso Quebrado (Broken Access Control) em Detalhes de Eventos (CWE-639, CWE-285)
- **Correção**: Implementada proteção de rota e validação de permissão granular.
- **Impacto**: Usuários anônimos não podem mais acessar detalhes de eventos. Usuários logados sem perfil administrativo/secretário só podem visualizar detalhes de eventos que já foram `DEFERIDOS`.
- **Implementação**:
  - Adicionado decorator `@login_required` à rota `/events/<int:id>`.
  - Adicionada verificação de status do evento vs papel do usuário na sessão.

### 1.2 Exposição Indevida de Dados na Listagem de Agenda (CWE-284)
- **Correção**: Segregação de visibilidade baseada em autenticação.
- **Impacto**: A agenda pública (usuários não logados) agora exibe estritamente eventos com status `DEFERIDO`. Eventos `PENDENTE` e `INDEFERIDO` tornaram-se invisíveis para o público externo.
- **Implementação**:
  - Alterada a rota `/events` para verificar o ID do usuário na sessão.
  - Se não autenticado, a rota força o uso do método `EventoService.listar_eventos_deferidos()`.

### 1.3 Proteção Adicional na API de Eventos
- **Correção**: Garantia de filtragem no endpoint de dados assíncronos.
- **Impacto**: O endpoint `/api/events` (usado pelo FullCalendar) foi endurecido para retornar apenas eventos aprovados, prevenindo o vazamento de rascunhos de agenda por chamadas diretas à API.

## 2. Status das Ações Prioritárias

1.  **Blindagem da Rota de Detalhes**: ✅ CONCLUÍDO
2.  **Segregação da Listagem de Agenda**: ✅ CONCLUÍDO
3.  **Hardening da API de Dados**: ✅ CONCLUÍDO

## 3. Próximos Passos Sugeridos
- Implementar sanitização de input com a biblioteca `Bleach` para mitigar riscos de XSS em campos de texto livre (Título/Descrição).
- Implementar rota segura para servir anexos (Ofícios), removendo-os da pasta `static` pública.
- Migrar IDs sequenciais para UUIDs nas URLs públicas para prevenir enumeração de banco de dados.
