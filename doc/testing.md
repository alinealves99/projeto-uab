# Plano de Testes (Baseado em TDD)

## 1. Estratégia de Testes

Utilizaremos o ciclo **Red-Green-Refactor**. Os testes serão divididos em:
- **Unitários**: Lógica de modelos e serviços.
- **Integração**: Rotas, persistência e controle de acesso.
- **Segurança**: Validação de roles e estados de usuário.

## 2. Cenários de Teste

### 2.1 Gestão de Usuários (ADMINISTRADOR apenas)
- `test_admin_acessa_lista_usuarios`: Garante que ADMIN vê a lista de usuários (Status 200).
- `test_nao_admin_bloqueado_lista_usuarios`: Garante que outros perfis são redirecionados (Status 302).
- `test_criar_usuario_valido`: Criação de novo usuário com sucesso.
- `test_editar_usuario_perfil`: Alteração de Role de CONSULTOR para SECRETARIO.
- `test_inativar_usuario`: Muda status `ativo` para False.
- `test_redefinir_senha_usuario`: Altera senha_hash e valida novo login.

### 2.2 Autenticação e Bloqueio
- `test_login_usuario_ativo`: Login bem-sucedido.
- `test_login_usuario_inativo`: Tentativa de login com usuário `ativo=False` deve falhar com mensagem de erro.
- `test_logout_limpa_sessao`: Garante que dados da sessão são removidos.

### 2.3 Eventos Indeferidos e Visibilidade
- `test_evento_indeferido_oculto_agenda`: Garante que eventos INDEFERIDOS não aparecem no endpoint da agenda pública.
- `test_acesso_lista_indeferidos_autorizado`: ADMIN e SECRETARIO acessam a lista (Status 200).
- `test_acesso_lista_indeferidos_negado`: CONSULTOR não acessa a lista (Status 302).
- `test_dados_lista_indeferidos`: Valida se a lista exibe justificativa e responsável pela decisão.

### 2.4 Interface e Menus (Mock de Sessão)
- `test_menu_usuarios_visivel_apenas_admin`: Verifica se o link "Usuários" aparece no HTML apenas para ADMIN.
- `test_menu_indeferidos_oculto_consultor`: Verifica se o link "Eventos Indeferidos" está oculto para CONSULTOR.

### 2.5 Regressão e Segurança
- `test_protecao_rota_admin_id_direto`: Tenta editar usuário via ID em POST sem ser ADMIN.
- `test_upload_sanitizacao`: (Existente) Validação de segurança em nomes de arquivos.
- `test_conflito_horario_evento`: (Existente) Garante que eventos não se sobrepõem.

## 3. Ferramentas
- **pytest**: Executor.
- **coverage**: Mínimo de 80% de cobertura.
- **factory-boy**: Geração de massa (Usuários e Eventos).
- **pytest-flask**: Test client e session management.

## 4. Instruções de Execução
```bash
# Executar suite completa
pytest

# Gerar cobertura
coverage run -m pytest
coverage report -m
```
