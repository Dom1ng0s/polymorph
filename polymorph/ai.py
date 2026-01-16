import os
import json
import time
import google.generativeai as genai
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self, model_name="models/gemini-2.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def optimize_resume(self, resume_data: Dict, job_text: str) -> Dict[str, Any]:
        
        
        resume_content = {
            "summary": resume_data.get("summary", ""),
            "skills": resume_data.get("skills", []),
            "experience": resume_data.get("experience", []),
            "projects": resume_data.get("projects", [])
        }
        
        resume_str = json.dumps(resume_content, ensure_ascii=False)

        prompt = f"""
        Analise a VAGA e o CURRÍCULO fornecidos abaixo.
        
        OBJETIVO: Otimização para sistemas ATS (Applicant Tracking Systems).
        
        TAREFAS:
        1. Identifique o nome da empresa e keywords.
        2. GERE UM NOVO RESUMO ('new_summary') em 1ª pessoa. Deve incluir o CARGO DA VAGA e as 3 tecnologias principais logo na primeira frase.
        3. REORDENE AS SKILLS ('prioritized_skills') colocando as mais importantes para a vaga no topo da lista.
        4. Reescreva o campo 'description' dentro de 'new_experience' e 'new_projects' usando palavras-chave da vaga. MANTENHA OS OUTROS CAMPOS (company, period, role, etc) INTACTOS.
        
        REGRAS:
        - VERACIDADE TOTAL. Não invente skills.
        - Mantenha a estrutura de lista de objetos para experiências e projetos.
        - O campo de texto DEVE se chamar "description".
        - Retorne APENAS JSON válido.
        
        FORMATO JSON OBRIGATÓRIO:
        {{
            "company": "Nome da Empresa",
            "keywords": ["Key1", "Key2"],
            "new_summary": "Resumo otimizado...",
            "prioritized_skills": ["Skill1", "Skill2"],
            "new_experience": [
                {{
                    "company": "Nome da Empresa Original",
                    "role": "Cargo Original",
                    "period": "Data Original",
                    "description": "Texto da descrição reescrito e otimizado..."
                }}
            ],
            "new_projects": [
                {{
                    "name": "Nome do Projeto",
                    "role": "Cargo/Função Original (MANTENHA)",
                    "period": "Período Original (MANTENHA)",
                    "technologies": ["Tech1", "Tech2"],
                    "description": "Descrição do projeto reescrita..."
                }}
            ]
        }}

        VAGA:
        {job_text}

        CURRÍCULO:
        {resume_str}
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                text = response.text.strip()
                
                if text.startswith("```"):
                    lines = text.split("\n")
                    if lines[0].startswith("```"): lines = lines[1:]
                    if lines and lines[-1].startswith("```"): lines = lines[:-1]
                    text = "\n".join(lines)
                
                return json.loads(text)
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str:
                    wait_time = 20 * (attempt + 1)
                    print(f"    Cota de IA excedida (429). Aguardando {wait_time}s...")
                    time.sleep(wait_time)
                    continue 
                
                print(f"[AI Error] Falha na otimização: {e}")
                break
        
        return {
            "company": "Erro_AI",
            "keywords": [],
            "new_summary": resume_data.get("summary", ""),
            "prioritized_skills": resume_data.get("skills", []),
            "new_experience": resume_data.get("experience", []),
            "new_projects": resume_data.get("projects", [])
        }