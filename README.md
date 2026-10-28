# Smart and Resilient SMTP Automation Engine

Automated, rate-controlled email delivery and campaign management system built with Python, Streamlit, and Docker, engineered for high deliverability, anti-spam resilience, and auditability.

---

## 1. Problema de Negócio e Contexto

No envio de comunicações institucionais e campanhas operacionais personalizadas em escala moderada (B2B, prospecção qualificada ou notificações corporativas), ferramentas simples de script enfrentam dois problemas severos:

1. **Degradação de Reputação e Bloqueios em Filtros Anti-Spam:** Disparos síncronos em rajada com intervalos fixos e mensagens estáticas disparam heurísticas de firewalls corporativos e provedores de e-mail (SPF/DKIM/DMARC e filtros comportamentais), levando o IP ou domínio de envio para *blacklists*.
2. **Invisibilidade e Falta de Rastreabilidade Operacional:** Scripts sem interface de auditoria não informam em tempo real quais destinatários falharam, quais conexões expiraram por *timeout* e qual o percentual efetivo de entrega da campanha.

Este projeto foi construído para fornecer um motor resiliente e auditável de envios que:
- Simula cadência humana através de intervalos estocásticos calculados dinamicamente.
- Personaliza o conteúdo e anexos em nível de destinatário em tempo real.
- Disponibiliza um dashboard visual de controle operacional com métricas de entrega e falhas.
- Garante portabilidade e persistência de dados de envio via contêineres Docker.

---

## 2. Processo e Racional das Escolhas Técnicas

### 2.1. Controle Estocástico de Cadência (Anti-Blocking Rate Limiting)
- **Delays Aleatórios vs. Intervalos Rígidos:** Provedores de e-mail identificam com facilidade padrões mecânicos de disparo em intervalos idênticos (ex.: exatamente a cada 5.0 segundos). O módulo `core/` introduz uma distribuição aleatória de atrasos (jitter) entre envios sucessivos, emulando o comportamento de um operador humano e preservando a reputação do remetente.
- **Tratamento Resiliente de Falhas de Conexão:** O pipeline intercepta exceções específicas de protocolo (`smtplib.SMTPAuthenticationError`, `smtplib.SMTPServerDisconnected`) com tentativas automáticas de reconexão controlada (*exponential backoff* leve) antes de registrar falha definitiva.

### 2.2. Segurança e Segregação de Credenciais
- **Zero Credenciais em Código:** O sistema proíbe senhas hardcoded. A autenticação utiliza o protocolo seguro SSL/TLS com Senhas de Aplicativo (*App Passwords*) injetadas via variáveis de ambiente ou mascaradas na interface gráfica.
- **Isolamento de Contatos:** A base de destinatários (`data/contacts.csv`) e o histórico de processamento (`data/finished.csv`) operam como arquivos locais desacoplados da lógica de execução.

### 2.3. Persistência e Portabilidade com Docker
- **Volumes Persistentes:** O manifesto Docker foi configurado com bind mounts para os diretórios `config/`, `data/` e `attachments/`. Essa decisão assegura que campanhas interrompidas possam ser retomadas sem perda do histórico de envios e sem rebuild da imagem Docker.

---

## 3. Resultados Atingidos e Métricas de Validação

### 3.1. Eficiência de Entrega
- **Taxa de Entregabilidade:** Redução drástica da taxa de devolução (*bounce*) e eliminação de incidentes de bloqueio por spam em disparos sequenciais controlados.
- **Auditoria Transacional:** Rastreamento determinístico gravado em `data/finished.csv` contendo carimbo de data/hora, destinatário, status (`SUCESSO` / `FALHA`) e código de resposta do servidor SMTP.

### 3.2. Observabilidade em Tempo Real
- **Dashboard Streamlit:** Acompanhamento instantâneo do progresso da fila de envio, taxa percentual de sucesso vs. erro e inspeção direta dos logs de transmissão.

---

## 4. Arquitetura da Solução e Estrutura

```text
smtp_email_sender/
├── app.py                      # Interface Streamlit para monitoramento e parametrização
├── runner.py                   # Orquestrador do fluxo de disparo e processamento da fila
├── Dockerfile                  # Manifesto de conteinerização
├── requirements.txt            # Dependências com versões especificadas
├── core/                       # Lógica de conexão SMTP e motor de cadência estocástica
├── config/                     # Parametrizações de remetente, assunto e templates
├── data/
│   ├── contacts.csv            # Base de destinatários alvo
│   └── finished.csv            # Registro auditável de disparos concluídos
├── attachments/                # Documentos e relatórios anexados às mensagens
└── templates/                  # Modelos de corpo de e-mail com variáveis dinâmicas
```

---

## 5. Como Executar

### 5.1. Pré-requisitos
- Python 3.9 ou superior
- Conta de e-mail com suporte a SMTP autenticado (ex.: Gmail com Senha de Aplicativo ativada)

### 5.2. Instalação e Execução Local

1. Clone o repositório:
```bash
git clone https://github.com/RicsonRamos/smtp_email_sender.git
cd smtp_email_sender
```

2. Crie e ative um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Prepare a lista de contatos em `data/contacts.csv`:
```csv
company,email
Empresa Exemplo,contato@empresaexemplo.com
```

5. Inicie o dashboard de controle:
```bash
streamlit run app.py
```
Acesse a aplicação no navegador em `http://localhost:8501`.

### 5.3. Execução via Docker com Volumes Persistentes

1. Construa a imagem Docker:
```bash
docker build -t smtp-automator .
```

2. Inicialize o contêiner montando os volumes de persistência:
```bash
docker run -p 8501:8501 \
  -v $(pwd)/config:/app/config \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/attachments:/app/attachments \
  smtp-automator
```
Acesse `http://localhost:8501`.
