import asyncio
import os
from typing import Dict, Any, Optional
from backend.utils.logger import get_logger
from backend.utils.model_registry import AIModelRegistry

logger = get_logger(__name__)

class BrowserAgent:
    """
    yAI Pillar 8: Physical Browser Automation (Browser-Use)
    Automates a real headless browser using Playwright/browser-use.
    Can navigate, click, fill forms, and extract dynamic DOM information.
    """
    def __init__(self):
        # We need a strong reasoning/planning model for browser actions
        self.llm = AIModelRegistry.get_llm_for_tier("planning")

    async def browse(self, task: str) -> Dict[str, Any]:
        """
        Takes a natural language task and uses browser-use to execute it.
        """
        try:
            # We import here to avoid blocking startup if it's not installed yet
            from browser_use import Agent, Browser, BrowserConfig
            from langchain_openai import ChatOpenAI
            
            # Browser-Use works best with LangChain chat models
            logger.info(f"[BrowserAgent] Starting physical browser task: {task}")
            
            # Use headless browser for background tasks
            config = BrowserConfig(headless=True)
            browser = Browser(config=config)
            
            agent = Agent(
                task=task,
                llm=self.llm,
                browser=browser
            )
            
            result = await agent.run()
            await browser.close()
            
            return {
                "status": "success",
                "final_answer": result.final_result(),
                "history": [str(a) for a in result.action_results()]
            }
            
        except ImportError:
            logger.error("[BrowserAgent] browser-use is not installed.")
            return {"status": "error", "message": "browser-use library not installed."}
        except Exception as e:
            logger.error(f"[BrowserAgent] Browsing failed: {e}")
            return {"status": "error", "message": str(e)}

    async def test_app(self, url: str, test_scenario: str) -> Dict[str, Any]:
        """
        Specific workflow to navigate to an app we just deployed and smoke test it.
        """
        task = f"Navigate to {url}. {test_scenario}. If you find any errors, tracebacks, or broken UI elements, report them."
        logger.info(f"[BrowserAgent] Testing deployed app at {url}")
        return await self.browse(task)

    async def fetch_api_schema(self, url: str) -> Dict[str, Any]:
        """
        Autonomous extraction of API documentation from a webpage.
        """
        task = f"Go to {url} and extract the API schema or REST endpoints. Return it formatted as structured Markdown."
        return await self.browse(task)
