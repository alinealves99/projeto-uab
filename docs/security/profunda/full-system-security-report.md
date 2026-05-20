# Relatório de Inspeção de Cibersegurança (PROFUNDA) - Projeto UAB

## 1. Resumo Executivo
Esta inspeção profunda analisou a arquitetura completa do sistema, incluindo configurações de servidor, cadeia de suprimentos de software (dependencies), gestão de arquivos e proteção de dados em trânsito. O sistema apresenta melhorias significativas em relação às inspeções anteriores, mas ainda possui vulnerabilidades estruturais críticas. O maior risco identificado reside na **Exposição Pública de Documentos Oficiais** (Ofícios) e na **Ausência de Headers de Segurança** essenciais, que deixam a aplicação vulnerável a ataques de Clickjacking, MIME-sniffing e XSS complexos.

## 2. Quantidade de Achados por Severidade
- **Crítica**: 1 (Exposição de Dados Sensíveis via Static Uploads)
- **Alta**: 2 (Configuração de Segurança de Headers e Software Supply Chain)
- **Média**: 3 (Gestão de Secret Key, Ausência de CSP e Rate Limiting Incompleto)
- **Baixa**: 2 (Logs de Erro e IDs Sequenciais Internos)

---

## 3. Detalhamento dos Achados

### 3.1 Exposição Pública de Documentos Sensíveis (CWE-219 / CWE-284)
- **Localização**: `app/services/upload_service.py` e diretório `app/static/uploads/`.
- **Descrição**: O sistema salva arquivos de Ofícios (PDF/Imagens) na pasta `static`, que é servida diretamente pelo servidor web sem passar por qualquer verificação de autenticação ou autorização do Flask.
- **Evidência**: `upload_folder = os.path.join('app', 'static', 'uploads')`. Qualquer pessoa que conheça o nome do arquivo (mesmo com o prefixo UUID) pode baixá-lo anonimamente.
- **Impacto**: Vazamento de documentos oficiais da instituição para usuários não autorizados.
- **Severidade**: **CRÍTICA**
- **Recomendação**: Mover a pasta de uploads para fora da pasta `static` e criar uma rota protegida por `@login_required` para servir os arquivos via `send_from_directory`.
- **CWE**: CWE-284

### 3.2 Ausência de Proteção de Headers HTTP (CWE-693)
- **Localização**: `app/__init__.py`.
- **Descrição**: A aplicação não envia headers de segurança fundamentais como `X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy` (CSP) ou `Strict-Transport-Security` (HSTS).
- **Evidência**: O arquivo `create_app` não configura middleware ou decoradores para injetar esses headers.
- **Impacto**: Aumenta o risco de ataques de Clickjacking, Cross-Site Scripting (XSS) e ataques de interceptação de tráfego.
- **Severidade**: **ALTA**
- **Recomendação**: Utilizar a extensão `Flask-Talisman` para implementar todos os headers de segurança recomendados pela OWASP.
- **CWE**: CWE-693

### 3.3 Vulnerabilidades na Cadeia de Suprimentos (Software Supply Chain)
- **Localização**: `requirements.txt`.
- **Descrição**: O projeto utiliza versões de bibliotecas que podem conter vulnerabilidades conhecidas por não estarem em suas versões de segurança mais recentes (ex: Flask 3.0.0, Werkzeug 3.0.1).
- **Evidência**: Versões fixas e antigas em relação aos patches de segurança atuais.
- **Impacto**: Exploração de falhas conhecidas (CVEs) nas dependências subjacentes.
- **Severidade**: **ALTA**
- **Recomendação**: Executar `pip-audit` ou `safety` periodicamente e atualizar dependências para as versões de patch mais recentes.
- **CWE**: CWE-1104

### 3.4 Fallback para Secret Key Insegura (CWE-330)
- **Localização**: `projeto-uab/config.py`.
- **Descrição**: O sistema possui um valor padrão estático para `SECRET_KEY` caso a variável de ambiente não seja encontrada.
- **Evidência**: `SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")`.
- **Impacto**: Se a aplicação for implantada sem um `.env` configurado corretamente, as sessões do Flask serão assinadas com uma chave previsível ("dev-key"), permitindo a falsificação de cookies de sessão.
- **Severidade**: **MÉDIA**
- **Recomendação**: Forçar a falha da aplicação caso `SECRET_KEY` não esteja presente no ambiente em modo produção.
- **CWE**: CWE-1391

### 3.5 Ausência de Content Security Policy (CSP)
- **Localização**: Global (`app/templates/layout.html`).
- **Descrição**: Não há uma política de segurança de conteúdo definida para restringir a origem de scripts, estilos e fontes.
- **Evidência**: Ausência de metatag CSP ou header CSP.
- **Impacto**: Ataques de XSS tornam-se muito mais eficazes, pois scripts maliciosos podem ser injetados de qualquer origem externa.
- **Severidade**: **MÉDIA**
- **Recomendação**: Implementar uma política CSP restritiva que permita apenas recursos locais ou de CDNs confiáveis.
- **CWE**: CWE-1021

---

## 4. As 5 Ações Mais Urgentes (Prioritárias)

1.  **Privatização de Uploads**: Mover a pasta `uploads` para um diretório privado e criar uma rota autenticada para download de ofícios.
2.  **Implementação do Flask-Talisman**: Adicionar headers de segurança (HSTS, CSP, XFO) globalmente.
3.  **Endurecimento da Secret Key**: Remover o valor padrão "dev-key" e lançar erro se a chave não estiver no ambiente.
4.  **Auditoria de Dependências**: Atualizar bibliotecas para versões de patch estáveis (ex: Flask 3.0.3+, Werkzeug 3.0.3+).
5.  **Sanitização de HTML na Entrada**: Implementar o `Bleach` para limpar campos de texto livre (`descricao`, `titulo`) antes de salvar no banco de dados.
