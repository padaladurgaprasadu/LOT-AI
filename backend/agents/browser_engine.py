import asyncio
import base64
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class BrowserEngine:
    """
    yAI Pillar 3: Visual Autonomous Browsing Engine (Playwright + Qwen VLM)
    Enables agents to visually inspect URLs, navigate DOM trees, and extract API schemas.
    """
    
    def __init__(self):
        self.browser = None
        self.context = None
        
    async def init_browser(self):
        if not self.browser:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 800},
                device_scale_factor=1
            )
            
    async def teardown(self):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

    async def scan_url(self, url: str) -> dict:
        """
        Navigates to the URL, extracts the textual DOM for RAG, 
        and captures a base64 screenshot for VLM analysis.
        """
        logger.info(f"[BrowserEngine] Scanning URL: {url}")
        await self.init_browser()
        page = await self.context.new_page()
        
        try:
            # Wait until network is idle to ensure dynamic React/Vue content loads
            await page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Extract Screenshot
            screenshot_bytes = await page.screenshot(full_page=True)
            b64_img = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # Extract DOM Text
            html = await page.content()
            soup = BeautifulSoup(html, 'lxml')
            
            # Remove scripts and styles for clean text extraction
            for script in soup(["script", "style", "noscript"]):
                script.extract()
                
            text = soup.get_text(separator=' ', strip=True)
            
            return {
                "url": url,
                "screenshot_base64": b64_img,
                "text_content": text,
                "title": await page.title()
            }
        except Exception as e:
            logger.error(f"[BrowserEngine] Failed to scan {url}: {e}")
            return {"error": str(e)}
        finally:
            await page.close()

    async def analyze_with_vlm(self, url: str, query: str) -> str:
        """
        Combines the BrowserEngine with the Qwen VLM from NvidiaMoEClient
        to visually answer user questions about a webpage.
        """
        scan_data = await self.scan_url(url)
        if "error" in scan_data:
            return f"Failed to access URL: {scan_data['error']}"
            
        from backend.utils.nvidia_client import NvidiaMoEClient
        from langchain_core.messages import HumanMessage
        
        nv_client = NvidiaMoEClient()
        vlm = nv_client.get_vision_llm()
        
        system_prompt = (
            "You are an elite QA and Web Extraction Agent. "
            "You are provided with a screenshot of a webpage and its extracted text. "
            f"Webpage Title: {scan_data['title']}\\n"
            f"Extracted Text Snippet (first 2000 chars): {scan_data['text_content'][:2000]}\\n\\n"
            "Analyze the screenshot visually and combine it with the text to fulfill the user's request."
        )
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": f"{system_prompt}\\n\\nUser Request: {query}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{scan_data['screenshot_base64']}"}}
            ]
        )
        
        try:
            response = await vlm.ainvoke([message])
            return response.content
        except Exception as e:
            return f"VLM Analysis Failed: {str(e)}"
