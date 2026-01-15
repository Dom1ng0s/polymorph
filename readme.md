
# 🎯 Polymorph

**Polymorph** é uma ferramenta de automação CLI (Command Line Interface) que utiliza Inteligência Artificial para personalizar currículos automaticamente com base na descrição da vaga.

O objetivo é otimizar o tempo de candidatura, garantindo que o currículo destaque as experiências e palavras-chave mais relevantes para cada oportunidade.

## 🚀 Funcionalidades

-   **🤖 IA Integrada:** Usa o **Google Gemini** para analisar a vaga e reescrever o resumo/experiências do currículo.
-   **📄 Renderização de PDF:** Gera currículos em PDF modernos e limpos usando **Playwright** e **Jinja2**.
-   **⚡ Cache Inteligente:** Salva resultados da IA localmente para economizar tokens e acelerar reprocessamentos.
-   **🔄 Modo Batch:** Processa uma pasta inteira de vagas (.txt) de uma só vez.
-   **🛡️ Retry Automático:** Lida automaticamente com limites de taxa da API (Rate Limits).

## 🛠️ Tecnologias

-   Python 3.10+
-   [Google Generative AI (Gemini)](https://ai.google.dev/)
-   [Playwright](https://playwright.dev/python/) (PDF Engine)
-   Typer (CLI)
-   Jinja2 (Templating)

## 📦 Instalação

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/Dom1ng0s/polymorph.git](https://github.com/Dom1ng0s/polymorph.git)
    cd polymorph
    ```

2.  Crie um ambiente virtual e instale as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    playwright install chromium
    ```

3.  Configure as variáveis de ambiente:
    Crie um arquivo `.env` na raiz e adicione sua chave do Google Gemini:
    ```
    GOOGLE_API_KEY=sua_chave_aqui
    ```

## 💻 Uso

### 1. Candidatura Única
Abre um editor para você colar a vaga e gera o PDF.
```bash
python polymorph.py apply

```

### 2. Processamento em Lote

Processa todas as vagas (arquivos .txt) de uma pasta específica.

```bash
python polymorph.py batch --jobs-dir "vagas/"

```

### 3. Opções Extras

Pular a etapa de IA e apenas gerar o PDF com o currículo base:

```bash
python polymorph.py batch --jobs-dir "vagas/" --skip-ai

```

### ⚡ Teste Rápido

Para ver a mágica acontecer agora mesmo, rode o comando com os arquivos de exemplo incluídos:

```bash
python polymorph.py apply --resume inputs/resume_example.json --job "$(cat vagas/vaga_exemplo.txt)"

```

**Nota para Windows (PowerShell):**

```powershell
python polymorph.py apply --resume inputs/resume_example.json --job (Get-Content vagas/vaga_exemplo.txt -Raw)

```

---

Desenvolvido por **Davi Domingos**.

