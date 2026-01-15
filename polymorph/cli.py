import typer
import asyncio
import sys
from pathlib import Path
from typing import Optional
from .core import PolymorphCore

app = typer.Typer(help="Polymorph: Automação de Currículos com IA")

@app.callback()
def main():
    
    pass

@app.command(name="apply")
def apply_command(
    resume_path: Path = typer.Option(
        Path("inputs/my_resume.json"), 
        "--resume", "-r",
        help="Caminho para o JSON do currículo."
    ),
    job_text: Optional[str] = typer.Option(
        None, 
        "--job", "-j",
        help="Texto da vaga (Se vazio, abre editor)."
    )
):
    
    if not job_text:
        typer.echo("Abrindo editor para a descrição da vaga...")
        job_text = typer.edit(text="# Cole a descrição da vaga aqui e salve/feche.")
        
        if not job_text or job_text.strip().startswith("#"):
            typer.secho("Operação cancelada: Nenhuma descrição fornecida.", fg=typer.colors.RED)
            raise typer.Exit()

    try:
        typer.secho(f"Lendo currículo: {resume_path}", fg=typer.colors.BLUE)
        
        core = PolymorphCore(str(resume_path))
        core.load_data(job_text)
        
        typer.secho("Processando pipeline...", fg=typer.colors.YELLOW)
        
        
        asyncio.run(core.run_pipeline())
        
        typer.secho(" Sucesso!", fg=typer.colors.GREEN)

    except Exception as e:
        typer.secho(f" Erro: {e}", fg=typer.colors.RED)


@app.command(name="batch")
def batch_command(
    jobs_dir: Path = typer.Option(..., "--jobs-dir", "-d", help="Pasta com as vagas (.txt)."),
    resume_path: Path = typer.Option(Path("inputs/my_resume.json"), "--resume", "-r"),
    skip_ai: bool = typer.Option(False, "--skip-ai", help="Pula a etapa de IA e usa o currículo original.")
):
    
    if not jobs_dir.exists():
        typer.secho(f" Pasta '{jobs_dir}' não encontrada.", fg=typer.colors.RED)
        raise typer.Exit()
        
    job_files = list(jobs_dir.glob("*.txt")) + list(jobs_dir.glob("*.md"))
    
    if not job_files:
        typer.secho(" Nenhum arquivo encontrado.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    typer.secho(f" Processando {len(job_files)} vagas de '{jobs_dir}'...", fg=typer.colors.BLUE)

    success_count = 0

    for job_file in job_files:
        try:
            company_from_file = job_file.stem.replace("_", " ").title()
            
            typer.secho(f"\nTarget: {company_from_file} ({job_file.name})", fg=typer.colors.CYAN)
            
            job_text = job_file.read_text(encoding="utf-8")
            
            core = PolymorphCore(str(resume_path))
            core.load_data(job_text, company_name=company_from_file)
            
            asyncio.run(core.run_pipeline(skip_ai=skip_ai))
            
            success_count += 1
            
        except Exception as e:
            typer.secho(f" Falha em {job_file.name}: {e}", fg=typer.colors.RED)

    typer.secho(f"\n Concluído! {success_count}/{len(job_files)} processados.", fg=typer.colors.GREEN)