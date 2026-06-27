# 🎯 Polymorph

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=flat&logo=google&logoColor=white)](https://ai.google.dev)
[![License](https://img.shields.io/badge/licença-MIT-brightgreen?style=flat)](LICENSE)

Sistemas ATS descartam currículos que não contêm as palavras-chave exatas da vaga, mesmo quando o candidato tem a experiência certa. O Polymorph lê um currículo base em JSON, analisa o texto da vaga com o Gemini e gera um PDF adaptado: resumo reescrito, skills reordenadas e experiências com vocabulário alinhado à posição.

## Instalação

```bash
git clone https://github.com/Dom1ng0s/polymorph.git
cd polymorph
pip install -r requirements.txt
playwright install chromium
echo "GOOGLE_API_KEY=sua_chave_aqui" > .env
```

Chave de API gratuita em [aistudio.google.com](https://aistudio.google.com/app/apikey).

## Uso

```bash
# Uma vaga: passa o texto diretamente ou abre editor interativo
python polymorph.py apply --job "Backend Developer Python Flask Docker..."

# Várias vagas: cada .txt da pasta vira uma candidatura
python polymorph.py batch --jobs-dir ./inputs/vagas/
```

O PDF sai em `outputs/{Empresa}_{Nome}.pdf`.

## Before / After (execução real — vaga Backend Developer Python/Flask/Docker)

**Resumo — antes:**
```
Desenvolvedor Backend apaixonado por automação e eficiência. Tenho experiência em
construir APIs robustas e scripts que resolvem problemas reais. Busco desafios onde
possa aplicar Python e Inteligência Artificial para otimizar processos.
```

**Resumo — depois:**
```
Como Desenvolvedor Backend com experiência em Python e Docker, possuo um histórico
comprovado no desenvolvimento de APIs REST e na criação de pipelines de dados
eficientes, buscando aplicar minhas habilidades para otimizar processos e integrar
sistemas complexos.
```

**Skills — antes:** Python · FastAPI · Selenium · Docker · PostgreSQL · Git · Linux · GCP

**Skills — depois:** Python · Docker · FastAPI · PostgreSQL · Git · Linux · Selenium · GCP

Docker subiu de 4a para 2a posição porque a vaga mencionou "containerização com Docker" como requisito explícito.

**Experiência — antes:**
```
Auxiliei na migração de scripts legados para Python 3. Implementei rotinas de web
scraping para coleta de dados de mercado, reduzindo o trabalho manual da equipe de
marketing em 40%.
```

**Experiência — depois:**
```
Contribuí ativamente para a modernização de sistemas legados, migrando scripts críticos
para Python 3. Desenvolvi e implementei pipelines de dados eficientes via web scraping
para coleta de dados de mercado, otimizando processos e reduzindo o trabalho manual da
equipe de marketing em 40%.
```

O conteúdo é o mesmo. A descrição ganhou "pipelines de dados" e "dados de mercado" — palavras-chave exatas da vaga — sem inventar nenhuma informação nova.

## O que a IA faz (e o que não faz)

O prompt instrui o Gemini a: reescrever o resumo com o cargo da vaga e as 3 principais tecnologias na primeira frase, reordenar as skills colocando as mais relevantes no topo, e reescrever as descrições de experiências e projetos com palavras-chave da vaga.

O que não acontece: nenhuma informação nova é inventada. O modelo trabalha só com o que já está no JSON. Isso está explícito no prompt com "VERACIDADE TOTAL. Não invente skills."

## Decisões técnicas

**Cache MD5.** O hash do texto da vaga é a chave do cache em `outputs/cache/`. Processar a mesma vaga duas vezes (para ajustar o template, por exemplo) não consome tokens. O cache só é salvo se a API retornar resultado sem erro.

**Modo batch.** O comando `batch` lê todos os `.txt` e `.md` de uma pasta e processa em sequência. O nome do arquivo vira o nome da empresa no PDF. Útil para candidaturas em massa onde cada vaga já foi salva como arquivo.

**Resiliência a 429.** Quando a API retorna erro de cota, o scraper aguarda `20s * tentativa` antes de tentar novamente, com até 3 tentativas. Isso cobre o rate limit do tier gratuito do Gemini sem precisar de fila.

## Formato do currículo base

O currículo fica em `inputs/my_resume.json`. Veja o exemplo completo em `inputs/resume_example.json`. Campos principais:

```json
{
  "name": "Seu Nome",
  "summary": "Resumo base (será reescrito para cada vaga)",
  "skills": ["Python", "Flask", "Docker"],
  "experience": [
    {
      "company": "Empresa",
      "role": "Cargo",
      "period": "Jan 2024 - Atual",
      "description": "Descrição das responsabilidades"
    }
  ],
  "projects": [...]
}
```

## Licença

MIT
