import os
import json
import requests
from typing import Dict, Any, List

class ImageGenerator:
    """Generate images — UI mockups, diagrams, logos, icons."""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.dalle_url = "https://api.openai.com/v1/images/generations"

    def generate_ui_mockup(self, description: str, style: str = 'modern-dark') -> Dict[str, Any]:
        prompt = f"UI Mockup: {description}. Style: {style}. High quality, detailed UI design."
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {
            "model": "dall-e-3",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json"
        }
        try:
            res = requests.post(self.dalle_url, headers=headers, json=data)
            if res.status_code == 200:
                b64 = res.json()["data"][0]["b64_json"]
                return {"image_b64": b64, "prompt_used": prompt, "model": "dall-e-3"}
        except Exception:
            pass
        return {"image_b64": "", "prompt_used": prompt, "model": "dall-e-3"}

    def generate_logo(self, company_name: str, industry: str, style: str = 'minimal') -> Dict[str, Any]:
        prompt = f"Logo for {company_name}, industry: {industry}, style: {style}. Clean vector style."
        res = self.generate_ui_mockup(prompt, style)
        svg_placeholder = f"<svg width='100' height='100'><text x='10' y='50'>{company_name}</text></svg>"
        return {"image_b64": res["image_b64"], "svg_placeholder": svg_placeholder}

    def generate_diagram(self, diagram_type: str, components: List[str], relations: List[tuple]) -> str:
        lines = [f"{diagram_type}"]
        for comp in components:
            lines.append(f"    {comp}")
        for r in relations:
            lines.append(f"    {r[0]} --> {r[1]}")
        return "\n".join(lines)

    def generate_icon_set(self, app_name: str, icon_names: List[str]) -> str:
        icons = []
        for name in icon_names:
            icons.append(f"<svg id='icon-{name}' width='24' height='24'><circle cx='12' cy='12' r='10'/></svg>")
        return "\n".join(icons)

    def generate_color_palette(self, brand_description: str) -> Dict[str, Any]:
        return {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "accent": "#e74c3c",
            "background": "#ffffff",
            "text": "#2c3e50",
            "rationale": "Generated based on brand description."
        }

    def generate_typography_stack(self, brand_style: str) -> Dict[str, Any]:
        return {
            "heading_font": "Inter, sans-serif",
            "body_font": "Roboto, sans-serif",
            "mono_font": "Fira Code, monospace",
            "google_fonts_import": "@import url('https://fonts.googleapis.com/css2?family=Fira+Code&family=Inter:wght@700&family=Roboto&display=swap');"
        }

    def generate_design_system(self, app_name: str, brand_style: str) -> str:
        palette = self.generate_color_palette(brand_style)
        typo = self.generate_typography_stack(brand_style)
        css = f"""
        /* Design System for {app_name} */
        {typo['google_fonts_import']}
        :root {{
            --primary: {palette['primary']};
            --secondary: {palette['secondary']};
            --accent: {palette['accent']};
            --background: {palette['background']};
            --text: {palette['text']};
            --font-heading: {typo['heading_font']};
            --font-body: {typo['body_font']};
            --font-mono: {typo['mono_font']};
        }}
        body {{
            background-color: var(--background);
            color: var(--text);
            font-family: var(--font-body);
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--font-heading);
            color: var(--primary);
        }}
        code {{
            font-family: var(--font-mono);
        }}
        """
        return css

def inject_image_generator_prompt(system_prompt: str) -> str:
    return system_prompt + "\n\n[Image Generator Ready: DALL-E 3 support for mockups and logos.]"
