import json
import asyncio
from typing import Dict, Any, List
from playwright.async_api import async_playwright

class PerceptionEngine:
    """
    Advanced Perception Engine for yAI.
    Parses web pages mathematically using Playwright, injecting JavaScript to 
    extract only visible, interactable elements with their spatial coordinates.
    """
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """Initializes the headless browser context."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            # Run chromium headlessly
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            self.page = await self.context.new_page()

    async def navigate(self, url: str) -> bool:
        """Navigates to a URL and waits for the network to idle."""
        if not self.page:
            await self.start()
        try:
            await self.page.goto(url, wait_until="networkidle", timeout=30000)
            return True
        except Exception as e:
            print(f"[PerceptionEngine] Navigation failed: {e}")
            return False

    async def extract_spatial_tree(self) -> Dict[str, Any]:
        """
        Injects JS to extract a mathematical layout of the page.
        Returns a compressed JSON spatial tree of only visible elements.
        """
        if not self.page:
            return {"error": "Browser not started"}

        # Proprietary JS injection to extract visible, interactive elements
        js_script = """
        () => {
            const isVisible = (element) => {
                const style = window.getComputedStyle(element);
                return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
            };
            
            const interactiveSelectors = 'a, button, input, select, textarea, [role="button"], [tabindex]:not([tabindex="-1"])';
            const elements = document.querySelectorAll(interactiveSelectors);
            
            const spatialTree = [];
            
            elements.forEach((el, index) => {
                if (isVisible(el)) {
                    const rect = el.getBoundingClientRect();
                    // Only include elements that actually take up space in the viewport
                    if (rect.width > 0 && rect.height > 0) {
                        spatialTree.push({
                            id: index,
                            tag: el.tagName.toLowerCase(),
                            text: (el.innerText || el.value || el.placeholder || '').substring(0, 50).trim(),
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            w: Math.round(rect.width),
                            h: Math.round(rect.height),
                            href: el.href || null
                        });
                    }
                }
            });
            
            return {
                title: document.title,
                url: window.location.href,
                elements: spatialTree
            };
        }
        """
        
        try:
            spatial_data = await self.page.evaluate(js_script)
            return spatial_data
        except Exception as e:
            return {"error": str(e)}

    async def click_element(self, element_id: int, spatial_data: Dict[str, Any]) -> bool:
        """Clicks an element based on its extracted coordinates."""
        try:
            target = next((el for el in spatial_data['elements'] if el['id'] == element_id), None)
            if not target:
                return False
                
            x = target['x'] + (target['w'] / 2)
            y = target['y'] + (target['h'] / 2)
            
            await self.page.mouse.click(x, y)
            await self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            print(f"[PerceptionEngine] Click failed: {e}")
            return False

    async def capture_visual_context(self) -> str:
        """
        Takes a screenshot of the active page and returns it as a Base64 JPEG string.
        Used by Qwen-3.5-VLM to physically "see" the page.
        """
        import base64
        if not self.page:
            return ""
        try:
            screenshot_bytes = await self.page.screenshot(type="jpeg", quality=60)
            base64_str = base64.b64encode(screenshot_bytes).decode("utf-8")
            return base64_str
        except Exception as e:
            print(f"[PerceptionEngine] Screenshot failed: {e}")
            return ""

    async def close(self):
        """Cleans up browser resources."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

# Standalone Test
if __name__ == "__main__":
    import sys
    async def run_test():
        url = sys.argv[1] if len(sys.argv) > 1 else "https://news.ycombinator.com"
        print(f"Booting Perception Engine to scan: {url}")
        
        engine = PerceptionEngine()
        await engine.start()
        
        success = await engine.navigate(url)
        if success:
            print("Page loaded successfully. Extracting Spatial Tree...")
            tree = await engine.extract_spatial_tree()
            print(f"\nExtracted Title: {tree.get('title')}")
            print(f"Found {len(tree.get('elements', []))} interactive elements.")
            
            # Print first 5 elements for verification
            print("\nSample Elements:")
            for el in tree.get('elements', [])[:5]:
                print(f"[{el['tag'].upper()}] '{el['text']}' @ (X:{el['x']}, Y:{el['y']})")
                
        await engine.close()
        
    asyncio.run(run_test())
