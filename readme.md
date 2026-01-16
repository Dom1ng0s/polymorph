# 🎯 Polymorph

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AI-Gemini-blue?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini AI">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
</p>

**Polymorph** é uma ferramenta de automação CLI que utiliza Inteligência Artificial para personalizar currículos automaticamente com base na descrição da vaga. O objetivo é garantir que seu currículo destaque as experiências e palavras-chave mais relevantes para cada oportunidade, otimizando seu tempo de candidatura.

## 🚀 Funcionalidades Principais

- **🤖 IA Contextual:** Utiliza o **Google Gemini** para reescrever resumos e experiências focando nos requisitos da vaga.
- **📄 PDF Engine:** Gera currículos modernos e limpos usando **Playwright** e **Jinja2**.
- **⚡ Performance:** Cache inteligente para economizar tokens e processamento em lote (batch) para múltiplas vagas.
- **🛡️ Resiliência:** Tratamento automático de Rate Limits da API.

## 💻 Comandos Disponíveis

| Comando | Descrição | Exemplo de Uso |
| :--- | :--- | :--- |
| `apply` | Processa uma única vaga (abre editor para colar o texto). | `python polymorph.py apply` |
| `batch` | Processa todos os arquivos `.txt` de um diretório. | `python polymorph.py batch --jobs-dir "vagas/"` |
| `--skip-ai` | Gera o PDF usando apenas o currículo base, sem IA. | `python polymorph.py batch --skip-ai` |
| `--resume` | Especifica um arquivo de currículo JSON customizado. | `python polymorph.py apply --resume meu_cv.json` |

## 📦 Instalação Rápida

```bash
git clone https://github.com/Dom1ng0s/polymorph.git
cd polymorph
pip install -r requirements.txt
playwright install chromium
# Adicione sua GOOGLE_API_KEY no arquivo .env
```

## 🗺️ Roadmap de Evolução

- [ ] Suporte a múltiplos templates de PDF (Moderno, Clássico, Acadêmico).
- [ ] Integração com outros LLMs (OpenAI, Anthropic, Llama 3 local).
- [ ] Extração automática de vagas via URL (LinkedIn/Indeed).
- [ ] Interface Web (Streamlit) para usuários não-técnicos.

---
Desenvolvido com ☕ por [Davi Domingos](https://github.com/Dom1ng0s)
