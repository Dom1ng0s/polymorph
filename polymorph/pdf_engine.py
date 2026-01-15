import asyncio
import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from playwright.async_api import async_playwright
from .models import ApplicationContext

# Função auxiliar para converter Markdown em HTML
def markdown_to_html(text):
    if not text:
        return ""
    # Substitui **texto** por <strong>texto</strong>
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    return Markup(html)

class PDFEngine:
    def __init__(self):
        self.template_dir = Path("templates")
        self.output_dir = Path("outputs")
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # REGISTRA O FILTRO NO JINJA
        self.env.filters['md'] = markdown_to_html
        
        self.output_dir.mkdir(exist_ok=True)

    async def render(self, context: ApplicationContext, filename="CV_Gerado.pdf") -> str:
        """
        Renderiza o HTML e converte para PDF usando Playwright.
        """
        # 1. Preparar o HTML com Jinja2
        template = self.env.get_template("resume.html")
        html_content = template.render(r=context.resume)
        
        # 2. Ler o CSS e INJETAR DIRETAMENTE no HTML (Correção de Path/Cache)
        css_path = self.template_dir / "style.css"
        if css_path.exists():
            css_text = css_path.read_text(encoding="utf-8")
            # Substitui o link pelo conteúdo inline
            html_with_style = html_content.replace(
                '<link rel="stylesheet" href="style.css">', 
                f'<style>\n{css_text}\n</style>'
            )
        else:
            print(f" Aviso: {css_path} não encontrado.")
            html_with_style = html_content

        output_path = self.output_dir / filename

        # 3. Gerar PDF com Playwright
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            await page.set_content(html_with_style)
            
            await page.pdf(
                path=output_path,
                format="A4",
                print_background=True,
                margin={"top": "1.25cm", "right": "1.25cm", "bottom": "1.25cm", "left": "1.25cm"}
            )
            
            await browser.close()
        
        return str(output_path)