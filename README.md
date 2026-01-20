# GitLab Backup Script 🔄

Script Python para realizar backups automatizados de repositórios do GitLab, com suporte a dois modos: Snapshot (ZIP) e Mirror (Git completo com histórico).

## 📋 Recursos

- ✅ Backup de múltiplos grupos do GitLab
- 🗜️ **Modo Snapshot**: Exporta apenas os arquivos atuais em ZIP (leve e rápido)
- 📚 **Modo Mirror**: Clone completo com histórico e branches (seguro e versátil)
- 📁 Organização automática por data e grupo
- 🔐 Dados sensíveis protegidos em arquivo `.env` (não commitado)
- 📋 Logs detalhados durante a execução

## 🚀 Instalação

### Pré-requisitos

- Python 3.7+
- Git instalado no sistema (necessário para modo Mirror)
- Acesso a servidor GitLab com token de autenticação

### Passos

1. **Clone ou baixe o repositório**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd gitlab-backup-script
   ```

2. **Instale as dependências Python**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure o arquivo `.env`**
   ```bash
   # Copie o arquivo template
   cp .env.example .env
   
   # Edite com suas credenciais
   # (Use seu editor favorito: nano, vi, VS Code, etc)
   ```

4. **Preencha as variáveis de ambiente em `.env`**
   ```env
   GITLAB_URL=https://seu-gitlab-server.com/
   GITLAB_TOKEN=seu_token_pessoal_aqui
   GITLAB_GROUP_IDS=123;456;789
   BACKUP_BASE_DIR=/ caminho/para/backups
   ```

## 🎯 Como Usar

### Execução Básica

```bash
python backup.py
```

O script abrirá um menu interativo para escolher o tipo de backup:

```
========================================
 SELECIONE O TIPO DE BACKUP
========================================
 [1] SNAPSHOT (ZIP) - Apenas arquivos (Leve/Rápido)
 [2] MIRROR (GIT)   - Histórico Completo (Pesado/Seguro)
========================================
Opção (1 ou 2): 
```

### Modo 1️⃣ - SNAPSHOT (ZIP)
- Exporta apenas os arquivos atuais de cada repositório
- Compactado em formato ZIP
- **Vantagens**: Execução rápida, menor consumo de espaço em disco
- **Desvantagens**: Sem histórico de commits ou branches

### Modo 2️⃣ - MIRROR (Git)
- Clone completo com todo o histórico de commits
- Mantém branches, tags e histórico de desenvolvimento
- **Vantagens**: Backup íntegro e seguro, recuperação completa possível
- **Desvantagens**: Mais lento, consome mais espaço em disco

## 📁 Estrutura de Diretórios Gerada

Após cada execução, a estrutura será organizada desta forma:

```
backups_base/
├── YYYY-MM-DD/
│   ├── Snapshot/
│   │   ├── Grupo_1/
│   │   │   ├── repositorio_a.zip
│   │   │   ├── repositorio_b.zip
│   │   │   └── repositorio_c.zip
│   │   └── Grupo_2/
│   │       ├── repositorio_d.zip
│   │       └── repositorio_e.zip
│   └── Mirror/
│       ├── Grupo_1/
│       │   ├── repositorio_a.git
│       │   ├── repositorio_b.git
│       │   └── repositorio_c.git
│       └── Grupo_2/
│           ├── repositorio_d.git
│           └── repositorio_e.git
└── YYYY-MM-DD/
    └── ...
```

## ⚙️ Configuração

### Variáveis de Ambiente (`.env`)

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `GITLAB_URL` | URL do servidor GitLab | `https://gitlab.empresa.com/` |
| `GITLAB_TOKEN` | Token de acesso pessoal (PAT) | `glpat-xxxxxxxxxxxx` |
| `GITLAB_GROUP_IDS` | IDs dos grupos a fazer backup (separados por `;`) | `101;202;303;404` |
| `BACKUP_BASE_DIR` | Diretório raiz para armazenar os backups | `/mnt/backups/gitlab` ou `D:\backups` |

### Como Obter o Token do GitLab

1. Faça login em sua instância GitLab
2. Acesse **Preferências de Usuário** → **Tokens de Acesso**
3. Crie um novo token com os seguintes escopos:
   - ✅ `api` - Acesso completo à API
   - ✅ `read_repository` - Leitura de repositórios
4. Copie o token gerado e salve em `GITLAB_TOKEN` no arquivo `.env`
5. ⚠️ **Nunca compartilhe ou commit este token**

### Como Encontrar os IDs de Grupos

#### Método 1: Via Interface Web
1. Acesse a seção de Administração do GitLab
2. Navegue até **Grupos**
3. Clique em cada grupo e veja o ID na URL: `https://gitlab.com/groups/<ID>`

#### Método 2: Via API do GitLab
```bash
# Listar todos os grupos (requer token)
curl --header "PRIVATE-TOKEN: seu_token" \
     "https://seu-gitlab-server.com/api/v4/groups?per_page=100"
```

#### Método 3: Inferir da URL
- URL do grupo: `https://gitlab.com/groups/seu-grupo`
- Acessar `/admin/groups` (permissão de admin)

## 🔒 Segurança e Boas Práticas

- ⚠️ **NÃO faça commit do arquivo `.env`** - Ele está protegido no `.gitignore`
- 🔑 **Regenere o token regularmente** - Idealmente a cada 90 dias
- 👁️ **Revise permissões do token** - Use apenas escopos necessários
- 🛡️ **Mantenha `.env.example` como template** - Compartilhe apenas o template
- 🔐 **Proteja seus backups** - Use permissões de arquivo restritivas
- 📋 **Teste restauração** - Verifique periodicamente se seus backups funcionam

## 📝 Exemplo de Execução

```bash
$ python backup.py
✅ Conectado como: usuario_gitlab

========================================
 SELECIONE O TIPO DE BACKUP
========================================
 [1] SNAPSHOT (ZIP) - Apenas arquivos (Leve/Rápido)
 [2] MIRROR (GIT)   - Histórico Completo (Pesado/Seguro)
========================================
Opção (1 ou 2): 1

>> Modo escolhido: SNAPSHOT (ZIP)

Iniciando processamento de 4 grupos...

📂 GRUPO: Grupo_de_Desenvolvimento (ID: 101)
   Salvando em: /backups/2026-01-15/Snapshot/Grupo_de_Desenvolvimento
   Encontrados 7 projetos.
   ⬇️  Baixando: api-backend..., ✅ (ZIP salvo)
   ⬇️  Baixando: web-frontend..., ✅ (ZIP salvo)
   ⬇️  Baixando: banco-dados..., ✅ (ZIP salvo)
   ...

📂 GRUPO: Grupo_de_Infraestrutura (ID: 202)
   ...
```

## 🛠️ Troubleshooting

### ❌ Erro: "GITLAB_TOKEN não definido"
**Solução:**
- Verifique se o arquivo `.env` existe no mesmo diretório que `backup.py`
- Confirme que a variável `GITLAB_TOKEN` está preenchida no `.env`
- Não deixe a linha em branco: `GITLAB_TOKEN=seu_token_aqui`

### ❌ Erro: "Falha de autenticação / 401 Unauthorized"
**Solução:**
- Token expirado? Gere um novo token no GitLab
- Token sem permissões? Regenere com escopos `api` e `read_repository`
- URL do GitLab incorreta? Verifique `GITLAB_URL` no `.env`

### ❌ Erro: "git: command not found" (Modo Mirror)
**Solução:**
- Git não está instalado no sistema
- Git está instalado mas não está no PATH (variável de ambiente)
- [Baixe e instale Git](https://git-scm.com/)
- Reinicie o terminal após a instalação

### ❌ Erro: "Permission denied" ao criar diretório
**Solução:**
- Verifique permissões do diretório em `BACKUP_BASE_DIR`
- Execute com privilégios adequados (sudo/admin se necessário)
- Use um caminho onde você tenha permissão de escrita

### ⏱️ Backup muito lento
**Causas e soluções:**
- **Modo Mirror é naturalmente mais lento** - Copia todo o histórico
- **Repositórios muito grandes** - Podem levar vários minutos
- **Conexão de rede lenta** - Considere melhorar a largura de banda
- **Dica:** Agende para horários fora do pico de uso

### 📦 Erro: "ModuleNotFoundError: No module named 'gitlab' or 'dotenv'"
**Solução:**
```bash
# Reinstale as dependências
pip install -r requirements.txt

# Ou instale individualmente
pip install python-gitlab python-dotenv
```

## 📚 Dependências

| Pacote | Versão | Propósito |
|--------|--------|----------|
| `python-gitlab` | 3.0.0+ | SDK oficial para GitLab API |
| `python-dotenv` | 0.19.0+ | Carregamento de variáveis de `.env` |
| `git` | (sistema) | Necessário para modo Mirror |

## 📄 Estrutura de Arquivos do Projeto

```
gitlab-backup-script/
├── backup.py              # Script principal
├── requirements.txt       # Dependências Python
├── .env                   # Configuração com credenciais (NÃO commitar)
├── .env.example           # Template de configuração (commitar)
├── .gitignore             # Arquivos ignorados no Git
└── README.md              # Este arquivo
```

## 🔄 Agendamento Automático

### Linux/macOS: Usando cron
```bash
# Abra o editor de cron
crontab -e

# Adicione uma linha para executar diariamente às 2:00 AM
0 2 * * * cd /caminho/para/gitlab-backup-script && python backup.py << EOF
2
EOF
```

### Windows: Usando Task Scheduler
1. Abra **Agendador de Tarefas**
2. Crie uma **Nova Tarefa**
3. Configure para executar: `python C:\caminho\para\backup.py`
4. Defina a frequência desejada

## 🤝 Contribuições

Encontrou um bug? Tem uma sugestão? Sua contribuição é bem-vinda!

- Reporte problemas descrevendo passos para reproduzir
- Sugira melhorias abrindo uma issue
- Envie pull requests com correções ou novas funcionalidades

## 📄 Licença

Este projeto é distribuído sob licença aberta e pode ser usado livremente para fins comerciais e educacionais.

---

**Última atualização:** Não especificado  
**Maintainer:** Não especificado  
**Status:** Ativo ✨
