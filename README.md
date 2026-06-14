# 🎭 Polymorph

**CLI com IA para personalização inteligente de currículos em PDF**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![Playwright](https://img.shields.io/badge/Playwright-PDF_Engine-45ba4b?style=flat&logo=playwright&logoColor=white)](https://playwright.dev)
[![License](https://img.shields.io/badge/License-MIT-brightgreen?style=flat)](LICENSE)

O Polymorph é uma CLI que usa a API do **Google Gemini** para adaptar automaticamente o seu currículo base para os requisitos exatos de cada vaga, renderizando PDFs profissionais em menos de 30 segundos. Candidatar com o mesmo currículo genérico é o erro mais comum — o Polymorph extrai as palavras-chave da vaga, reescreve seu resumo e reordena suas skills para maximizar compatibilidade com sistemas ATS.

---

## Índice

1. [Funcionalidades](#-funcionalidades)
2. [Arquitetura](#-arquitetura)
3. [Requisitos](#-requisitos)
4. [Instalação e Execução](#-instalação-e-execução)
5. [Como Usar](#-como-usar)
6. [Formato do Currículo Base](#-formato-do-currículo-base)
7. [Roadmap](#-roadmap)
8. [Licença](#-licença)

---

## ✨ Funcionalidades

Extraídas diretamente do código:

- **Otimização com Google Gemini** (`gemini-2.5-flash`) — extrai empresa, keywords e reescreve resumo, experiências e projetos com as palavras-chave certas; nunca inventa informações, apenas reorganiza e enfatiza o que já existe
- **Reordenação de skills por relevância** — coloca no topo as tecnologias mais importantes para a vaga específica
- **PDF engine com Playwright + Jinja2** — renderiza o HTML via Jinja2 e converte com Chromium headless; CSS injetado inline para renderização perfeita em formato A4
- **Cache em disco por MD5** — vagas idênticas não consomem tokens; o hash do texto da vaga é a chave do cache em `outputs/cache/`
- **Resiliência a rate limits** — detecta erro 429 e aplica backoff progressivo (20s × tentativa) com até 3 retentativas
- **Modo batch** — processa todos os `.txt` e `.md` de uma pasta em sequência; nome do arquivo vira nome da empresa
- **Modo `--skip-ai`** — gera PDF sem chamar a API, útil para testar o template ou quando a cota está esgotada
- **Editor interativo** — se nenhum texto de vaga for passado, abre o editor do sistema para colar a descrição

---

## 🏗️ Arquitetura

```
polymorph.py (entrypoint)
      │
      └── polymorph/cli.py (Typer)
               │
               ├── apply  ─────────────────────────────────┐
               └── batch  ──── loop de arquivos .txt/.md ──┘
                                        │
                                        ▼
                              PolymorphCore (core.py)
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
                    AIAgent (ai.py)            PDFEngine (pdf_engine.py)
                    Gemini API                 Playwright + Jinja2
                         │                             │
                         ▼                             ▼
                  outputs/cache/              outputs/{Empresa}_{Nome}.pdf
                  {md5_da_vaga}.json
```

### Fluxo de uma Candidatura

```
1. Lê inputs/my_resume.json
2. Verifica cache → se hit, pula a API
3. Envia prompt para Gemini → recebe JSON com:
     company, keywords, new_summary,
     prioritized_skills, new_experience, new_projects
4. Aplica as atualizações no contexto ResumeData
5. Renderiza HTML via Jinja2 (templates/resume.html)
6. Injeta CSS inline e converte para PDF com Playwright
7. Salva em outputs/{Empresa}_{NomeUsuario}.pdf
```

---

## 📋 Requisitos

- Python 3.10+
- Chave de API do Google AI Studio — [obtenha gratuitamente](https://aistudio.google.com/app/apikey)
- Chromium (instalado via Playwright)

---

## 🚀 Instalação e Execução

```bash
# 1. Clone o repositório
git clone https://github.com/Dom1ng0s/polymorph.git
cd polymorph

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Instale o browser do Playwright
playwright install chromium

# 4. Configure a chave de API
# Crie um arquivo .env na raiz:
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env

# 5. Edite seu currículo base
# Preencha inputs/my_resume.json com seus dados reais
```

---

## 📖 Como Usar

### Da Vaga ao PDF em 30 Segundos

```bash
# Modo interativo: abre editor para colar a descrição da vaga
python polymorph.py apply

# Modo direto: passa o texto da vaga como argumento
python polymorph.py apply --job "Vaga: Desenvolvedor Python..."

# Modo batch: processa todas as vagas em uma pasta
python polymorph.py batch --jobs-dir ./inputs/vagas/
```

### Tabela de Comandos

| Comando | Flag | Descrição |
|---|---|---|
| `apply` | — | Processa uma única vaga (interativo ou com `--job`) |
| `apply` | `--resume` / `-r` | Usa um arquivo JSON de currículo alternativo |
| `apply` | `--job` / `-j` | Passa o texto da vaga diretamente na linha de comando |
| `batch` | `--jobs-dir` / `-d` | Processa todos os `.txt` e `.md` de uma pasta |
| `batch` | `--resume` / `-r` | Usa currículo alternativo no processamento em lote |
| `apply` / `batch` | `--skip-ai` | Gera PDF sem chamar a API (usa currículo original) |

### Exemplo End-to-End

```bash
# Crie um arquivo com a descrição da vaga
echo "Vaga: Desenvolvedor Backend Python na Acme Corp.
Requisitos: Flask, Docker, PostgreSQL, REST APIs..." > inputs/vagas/acme_corp.txt

# Processe em lote (o nome do arquivo vira o nome da empresa)
python polymorph.py batch --jobs-dir ./inputs/vagas/

# Output gerado em:
# outputs/AcmeCorp_Davi_Domingos_de_Oliveira.pdf
```

---

## 📄 Formato do Currículo Base

O currículo base fica em `inputs/my_resume.json`. Estrutura esperada:

```json
{
  "name": "Seu Nome Completo",
  "contact_info": {
    "email": "seu@email.com",
    "linkedin": "linkedin.com/in/seuperfil",
    "github": "github.com/seuusuario",
    "location": "Cidade, Estado"
  },
  "summary": "Resumo profissional base (será reescrito pela IA para cada vaga).",
  "skills": ["Python", "Flask", "Docker", "MySQL", "Git"],
  "experience": [
    {
      "company": "Nome da Empresa",
      "role": "Cargo Ocupado",
      "period": "Jan 2024 – Atual",
      "description": "Descrição das responsabilidades (será otimizada pela IA)."
    }
  ],
  "projects": [
    {
      "name": "Nome do Projeto",
      "role": "Função no Projeto",
      "period": "2024",
      "technologies": ["Python", "Flask"],
      "description": "Descrição do projeto (será otimizada pela IA)."
    }
  ],
  "education": [
    {
      "institution": "Nome da Universidade",
      "degree": "Bacharelado em Ciência da Computação",
      "period": "2023 – 2027"
    }
  ]
}
```

---

## 🗺️ Roadmap

- [ ] Suporte a múltiplos templates de PDF (Moderno, Clássico, Acadêmico)
- [ ] Integração com outros LLMs (OpenAI, Anthropic, Llama local)
- [ ] Extração automática de vagas via URL (LinkedIn / Indeed)
- [ ] Interface Web com Streamlit para usuários não-técnicos

---

## 👤 Autor

**Davi Domingos de Oliveira**
Estudante de Ciência da Computação — UFAL | Backend Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davidomingosdeoliveira/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Dom1ng0s)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:odomingosdavi@gmail.com)

---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.
