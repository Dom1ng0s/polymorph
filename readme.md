<div align="center">

# 🎯 Polymorph

**Automação CLI com IA para personalização inteligente de currículos em PDF**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini AI](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Playwright](https://img.shields.io/badge/Playwright-PDF_Engine-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> Candidatar para 10 vagas com o mesmo currículo genérico é o erro mais comum no mercado. O **Polymorph** resolve isso: lê a descrição da vaga, usa IA para reescrever seu currículo com as palavras-chave certas e gera um PDF profissional — tudo em segundos, via linha de comando.

</div>

---

## ✨ Como Funciona

```
Descrição da Vaga (texto)
         │
         ▼
  ┌─────────────┐      ┌──────────────────┐      ┌─────────────────┐
  │  currículo  │ ───► │  Google Gemini   │ ───► │  Jinja2 + HTML  │
  │  base.json  │      │  (reescreve e    │      │  (renderiza o   │
  └─────────────┘      │   personaliza)   │      │   template)     │
                       └──────────────────┘      └────────┬────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Playwright     │
                                                 │  (HTML → PDF)   │
                                                 └────────┬────────┘
                                                          │
                                                          ▼
                                               📄 curriculo_vaga.pdf
```

---

## 🚀 Funcionalidades

**IA Contextual com Google Gemini**
O modelo lê a descrição da vaga e reescreve o resumo e as experiências do currículo para destacar exatamente o que o recrutador está procurando, sem inventar informações — apenas reorganizando e enfatizando o que já existe.

**PDF Engine com Playwright + Jinja2**
Nada de bibliotecas PDF limitadas. O currículo é renderizado como HTML via Jinja2 e convertido em PDF pelo Playwright (Chromium headless), garantindo pixel-perfect e suporte a CSS moderno.

**Processamento em Lote (Batch)**
Tem 20 vagas para aplicar? Coloque os arquivos `.txt` em uma pasta e rode um único comando. O Polymorph processa todas em sequência, gerando um PDF personalizado para cada uma.

**Cache Inteligente**
Vagas similares não consomem tokens desnecessários. O sistema de cache evita chamadas redundantes à API e reduz custo de uso.

**Resiliência a Rate Limits**
Backoff automático no caso de Rate Limit da API do Gemini — o processamento em lote não quebra no meio.

---

## 💻 Comandos

```bash
# Processar uma vaga (abre editor para colar o texto)
python polymorph.py apply

# Processar uma vaga com currículo customizado
python polymorph.py apply --resume meu_cv.json

# Processar todas as vagas de um diretório (batch)
python polymorph.py batch --jobs-dir vagas/

# Gerar PDF sem IA (apenas template + currículo base)
python polymorph.py batch --skip-ai
```

| Comando | Flag | Descrição |
|---|---|---|
| `apply` | — | Processa uma única vaga interativamente |
| `batch` | `--jobs-dir` | Processa todos os `.txt` de um diretório |
| `apply` / `batch` | `--resume` | Usa um arquivo JSON de currículo alternativo |
| `apply` / `batch` | `--skip-ai` | Gera PDF sem chamar a API (modo offline) |

---

## 📁 Estrutura do Projeto

```
polymorph/
├── polymorph.py         # Ponto de entrada CLI (argparse)
├── polymorph/           # Módulos internos
│   ├── ai.py            # Integração com Google Gemini (cache + rate limit)
│   ├── pdf.py           # Engine de geração de PDF (Playwright)
│   └── parser.py        # Leitura e validação do currículo JSON
├── templates/           # Templates HTML do currículo (Jinja2)
├── inputs/              # Currículo base em JSON
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.10+
- Chave de API do [Google AI Studio](https://aistudio.google.com/app/apikey) (gratuita)

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/Dom1ng0s/polymorph.git
cd polymorph

# 2. Instale as dependências Python
pip install -r requirements.txt

# 3. Instale o Chromium (para o Playwright gerar PDF)
playwright install chromium

# 4. Configure sua chave de API
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env
```

### Configure seu Currículo Base

Edite o arquivo `inputs/resume.json` com suas informações. Esse é o currículo "master" que a IA vai personalizar para cada vaga:

```json
{
  "name": "Davi Domingos",
  "title": "Backend Developer",
  "summary": "Seu resumo genérico aqui...",
  "experience": [
    {
      "company": "Projeto X",
      "role": "Desenvolvedor Python",
      "description": "O que você fez..."
    }
  ],
  "skills": ["Python", "Flask", "MySQL"]
}
```

---

## 🛠️ Stack Tecnológica

| Responsabilidade | Tecnologia |
|---|---|
| **Linguagem** | Python 3.10+ |
| **IA / LLM** | Google Gemini API |
| **Geração de PDF** | Playwright (Chromium headless) |
| **Templating** | Jinja2 |
| **CLI** | argparse |
| **Config** | python-dotenv |

---

## 🗺️ Roadmap

- [ ] Suporte a múltiplos templates de PDF (Moderno, Clássico, Acadêmico)
- [ ] Integração com outros LLMs (OpenAI, Anthropic, Llama 3 local)
- [ ] Extração automática de vagas via URL (LinkedIn / Indeed)
- [ ] Interface Web com Streamlit para usuários não-técnicos

---

## 👤 Autor

**Davi Domingos de Oliveira**
Estudante de Ciência da Computação — UFAL | Backend Developer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davidomingosdeoliveira/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Dom1ng0s)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat&logo=gmail&logoColor=white)](mailto:odomingosdavi@gmail.com)
