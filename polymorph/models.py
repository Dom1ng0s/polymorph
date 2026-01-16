from dataclasses import dataclass, field
from typing import List, Set, Optional, Dict

@dataclass
class ResumeData:
    """Estrutura do currículo base do usuário."""
    name: str
    contact_info: Dict[str, str]
    summary: str
    skills: List[str]
    experience: List[Dict[str, str]] = field(default_factory=list)
    projects: List[Dict[str, str]] = field(default_factory=list) 
    education: List[Dict[str, str]] = field(default_factory=list)
    certifications: List[Dict[str, str]] = field(default_factory=list)

@dataclass
class JobDescription:
    """Dados da vaga processada."""
    raw_text: str
    extracted_keywords: Set[str] = field(default_factory=set)
    company_name: Optional[str] = None
    role_title: Optional[str] = None

@dataclass
class ApplicationContext:
    """Estado atual da execução."""
    resume: ResumeData
    job: JobDescription
    match_score: float = 0.0
    generated_content: Dict[str, str] = field(default_factory=dict)
    output_path: str = ""