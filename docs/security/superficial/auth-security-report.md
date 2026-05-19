# Relatório de Inspeção de Cibersegurança (SUPERFICIAL) - UAB Eventos

## 1. Resumo Executivo
Esta inspeção superficial focou nos módulos de autenticação, gestão de usuários e autorização. O sistema demonstra boas práticas básicas, como o uso de hashes de senha via `PBKDF2` (padrão do Werkzeug) e decorators de controle de acesso. No entanto, foram identificadas falhas críticas relacionadas à gestão de sessões, ausência de proteção contra CSRF em rotas sensíveis e falta de rate limiting, o que expõe o sistema a ataques de força bruta e sequestro de sessão.

## 2. Quantidade de Achados por Severidade
- **Crítica**: 1
- **Alta**: 2
- **Média**: 2
- **Baixa**: 1

---

## 3. Detalhamento dos Achados

### 3.1 Falta de Proteção CSRF (Cross-Site Request Forgery)
- **Localização**: `app/routes/usuarios.py` (rotas `POST` como `toggle_usuario` e `reset_password`).
- **Descrição**: Rotas que realizam alterações de estado no sistema via `POST` não possuem validação de tokens CSRF.
- **Evidência**: O formulário é processado diretamente sem verificação de token de sincronização.
- **Impacto**: Um atacante pode induzir um administrador autenticado a clicar em um link malicioso que desativa usuários ou altera senhas sem o seu conhecimento.
- **Severidade**: **ALTA**
- **Recomendação**: Implementar `Flask-WTF` para proteção CSRF global.
- **CWE**: CWE-352

### 3.2 Ausência de Rate Limiting no Login
- **Localização**: `app/routes/auth.py` (rota `/login`).
- **Descrição**: Não há limite de tentativas de login por IP ou usuário.
- **Evidência**: A função `autenticar` é chamada repetidamente sem qualquer bloqueio temporal ou exponencial.
- **Impacto**: Permite ataques de força bruta (brute force) e preenchimento de credenciais (credential stuffing).
- **Severidade**: **ALTA**
- **Recomendação**: Utilizar `Flask-Limiter` para restringir tentativas de login.
- **CWE**: CWE-307

### 3.3 Cookies de Sessão Inseguros
- **Localização**: Configuração global do Flask (implícito em `app/__init__.py`).
- **Descrição**: Não foram identificadas configurações explícitas para `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE` e `SESSION_COOKIE_SAMESITE`.
- **Evidência**: Ausência de `app.config['SESSION_COOKIE_SECURE'] = True` etc.
- **Impacto**: Facilita o roubo de sessão via ataques XSS ou interceptação de tráfego (se o site não for HTTPS).
- **Severidade**: **CRÍTICA** (se o ambiente for produção) / **MÉDIA** (desenvolvimento).
- **Recomendação**: Configurar cookies de sessão com atributos `HttpOnly`, `Secure` e `SameSite=Lax`.
- **CWE**: CWE-614, CWE-1004

### 3.4 Divulgação de Mensagem de Erro Específica (Enumeração de Usuários)
- **Localização**: `app/services/usuario_service.py` (método `autenticar`).
- **Descrição**: O sistema retorna "Sua conta está desativada" se o email existir mas o usuário estiver inativo.
- **Evidência**: `return None, "Sua conta está desativada..."`
- **Impacto**: Permite que um atacante confirme se um email específico está cadastrado no sistema (User Enumeration).
- **Severidade**: **BAIXA**
- **Recomendação**: Retornar mensagens genéricas como "Credenciais inválidas" independentemente do motivo da falha.
- **CWE**: CWE-204

### 3.5 Fixação de Sessão (Session Fixation)
- **Localização**: `app/routes/auth.py` (método `login`).
- **Descrição**: O ID da sessão não é explicitamente regenerado após o login bem-sucedido.
- **Evidência**: `session.update(session_data)` apenas adiciona dados à sessão existente.
- **Impacto**: Um atacante pode pré-estabelecer um ID de sessão e aguardar o usuário se autenticar.
- **Severidade**: **MÉDIA**
- **Recomendação**: Chamar `session.clear()` ou regenerar a sessão imediatamente após o login bem-sucedido.
- **CWE**: CWE-384

### 3.6 Exposição de Erros do ORM (Verbose Errors)
- **Localização**: `app/services/usuario_service.py` (blocos `try/except`).
- **Descrição**: Erros de exceção do banco de dados são convertidos em string e retornados ao usuário.
- **Evidência**: `except Exception as e: return None, str(e)`
- **Impacto**: Pode vazar informações sobre a estrutura das tabelas, nomes de colunas ou a engine do banco em caso de falha crítica.
- **Severidade**: **MÉDIA**
- **Recomendação**: Registrar o erro técnico em logs e retornar uma mensagem amigável e genérica ao usuário.
- **CWE**: CWE-209

---

## 4. As 5 Ações Mais Urgentes (Prioritárias)

1. **Habilitar Proteção CSRF**: Ativar o `Flask-WTF` para todos os formulários e rotas que alteram dados.
2. **Endurecer Cookies de Sessão**: Configurar `SESSION_COOKIE_HTTPONLY=True` e `SESSION_COOKIE_SECURE=True` (em produção).
3. **Implementar Rate Limiting**: Restringir tentativas de login na rota `/login` para mitigar ataques de força bruta.
4. **Regenerar Sessão no Login**: Garantir que um novo ID de sessão seja gerado após a autenticação bem-sucedida.
5. **Padronizar Mensagens de Erro**: Substituir retornos técnicos de exceção (`str(e)`) por mensagens genéricas ("Erro ao processar solicitação").
