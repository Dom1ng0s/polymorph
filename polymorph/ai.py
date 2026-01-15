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
        """
        Versão com RETRY AUTOMÁTICO para lidar com erro 429 (Rate Limit).
        """
        
        resume_content = {
            "experience": resume_data.get("experience", []),
            "projects": resume_data.get("projects", [])
        }
        
        resume_str = json.dumps(resume_content, ensure_ascii=False)

        prompt = f"""
        Analise a VAGA e o CURRÍCULO fornecidos abaixo.
        
        OBJETIVO: Otimização completa do currículo.
        
        TAREFAS:
        1. Identifique o nome da empresa e keywords.
        2. Reescreva 'description' de experiências e projetos.
        
        REGRAS:
        - VERACIDADE TOTAL. Não invente nada.
        - Retorne APENAS JSON válido.
        
        FORMATO JSON:
        {{
            "company": "Nome da Empresa",
            "keywords": ["Skill1", "Skill2"],
            "new_experience": [],
            "new_projects": []
        }}

        VAGA:
        {job_text}

        CURRÍCULO:
        {resume_str}
        """
        
        # Tenta até 3 vezes se der erro de cota
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
                # Se for erro de cota (429), espera e tenta de novo
                if "429" in error_str:
                    wait_time = 20 * (attempt + 1) # Espera 20s, 40s...
                    print(f"   ⏳ Cota de IA excedida (429). Aguardando {wait_time}s para tentar novamente...")
                    time.sleep(wait_time)
                    continue # Tenta de novo
                
                # Se for outro erro, ou se acabaram as tentativas
                print(f"[AI Error] Falha na otimização: {e}")
                break
        
        # Fallback em caso de falha total
        return {
            "company": "Erro_AI",
            "keywords": [],
            "new_experience": resume_data.get("experience", []),
            "new_projects": resume_data.get("projects", [])
        }