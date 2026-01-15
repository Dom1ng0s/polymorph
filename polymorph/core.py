import json
import asyncio
import hashlib
from pathlib import Path
from typing import Optional
from .models import ResumeData, JobDescription, ApplicationContext
from .ai import AIAgent
from .pdf_engine import PDFEngine

class PolymorphCore:
    def __init__(self, resume_path: str):
        self.resume_path = Path(resume_path)
        self.context: ApplicationContext = None
        self.ai = AIAgent()
        self.renderer = PDFEngine()
        
        self.cache_dir = Path("outputs/cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self, job_text: str, company_name: Optional[str] = None):
        if not self.resume_path.exists():
            raise FileNotFoundError(f"Currículo não encontrado em: {self.resume_path}")
        
        with open(self.resume_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        resume = ResumeData(
            name=data.get("name", ""),
            contact_info=data.get("contact_info", {}),
            summary=data.get("summary", ""),
            skills=set(data.get("skills", [])),
            experience=data.get("experience", []),
            projects=data.get("projects", []),
            education=data.get("education", []),
            certifications=data.get("certifications", [])
        )
        
        job = JobDescription(raw_text=job_text, company_name=company_name)
        self.context = ApplicationContext(resume=resume, job=job)
        print(f"[Core] Contexto carregado. Candidato: {resume.name}")

    def _get_cache_key(self, job_text: str) -> str:
        return hashlib.md5(job_text.encode('utf-8')).hexdigest()

    async def run_pipeline(self, output_suffix: str = "", skip_ai: bool = False):
        if not self.context:
            raise ValueError("Contexto não inicializado.")

        cache_key = self._get_cache_key(self.context.job.raw_text)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        ai_result = None

        if skip_ai:
             print("     Modo SKIP-AI ativado: Usando currículo original.")
             ai_result = {} 
        
        elif cache_file.exists():
            print("    Cache encontrado! Carregando dados do disco...")
            try:
                ai_result = json.loads(cache_file.read_text(encoding='utf-8'))
            except:
                print("    Cache corrompido, ignorando.")

        if ai_result is None:
            print("[Core] Iniciando pipeline AI (Chamada API)...")
            resume_dict = {
                "experience": self.context.resume.experience,
                "projects": self.context.resume.projects
            }
            
            print("   ->  Processando Vaga e Currículo (Gemini)...")
            ai_result = await asyncio.to_thread(
                self.ai.optimize_resume, 
                resume_dict, 
                self.context.job.raw_text
            )
            
            # CORREÇÃO: Só salva no cache se NÃO for um erro
            if ai_result.get("company") != "Erro_AI":
                cache_file.write_text(json.dumps(ai_result, ensure_ascii=False, indent=2), encoding='utf-8')
                print("    Resultado salvo em cache.")
            else:
                print("     Aviso: Resultado com erro não foi salvo no cache.")
        
        # Aplica os resultados
        if not self.context.job.company_name:
            self.context.job.company_name = ai_result.get("company", "Empresa")
        
        if ai_result.get("keywords"):
            self.context.job.extracted_keywords = set(ai_result.get("keywords", []))
            print(f"      Keywords: {self.context.job.extracted_keywords}")

        if ai_result.get("new_experience"):
            print("      Experiências atualizadas.")
            self.context.resume.experience = ai_result.get("new_experience")

        if ai_result.get("new_projects"):
            print("      Projetos atualizados.")
            self.context.resume.projects = ai_result.get("new_projects")

        await self._step_render_pdf(output_suffix)
        print("[Core] Pipeline finalizado.")

    async def _step_render_pdf(self, suffix: str = ""):
        print("   ->  Renderizando PDF (Playwright)...")
        
        company_raw = self.context.job.company_name or "Empresa"
        company = company_raw.replace(" ", "")
        user_name = self.context.resume.name.replace(" ", "_")
        
        safe_company = "".join(c for c in company if c.isalnum() or c in "_-")
        safe_user = "".join(c for c in user_name if c.isalnum() or c in "_-")
        
        filename = f"{safe_company}_{safe_user}{suffix}.pdf"
        
        output_file = await self.renderer.render(self.context, filename)
        print(f" PDF gerado com sucesso em: {output_file}")