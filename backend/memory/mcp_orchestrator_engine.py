"""
LOT AI 5 Sovereign MCP Servers Orchestrator Engine v1.0
=========================================================
Connects LOT AI to 5 Sovereign Model Context Protocol (MCP) Servers:
1. Context7 MCP (Up-to-date real-time tech documentation)
2. GitHub MCP (Repository code search, PR automation, issue tracking)
3. Playwright MCP (E2E headless browser testing, scraping & visual QA)
4. Sequential Thinking MCP (Multi-step logical chain reasoning & debugging)
5. Filesystem MCP (Sandboxed air-gapped code reading, writing & AST edits)
"""

import logging

logger = logging.getLogger(__name__)

SOVEREIGN_MCP_SERVERS = {
    "context7": {
        "name": "Context7 MCP",
        "description": "Real-time up-to-date API & library documentation fetcher",
        "tools": ["get_docs", "search_api_reference", "fetch_library_spec"]
    },
    "github": {
        "name": "GitHub MCP",
        "description": "Repository search, pull request creation & issue tracking",
        "tools": ["search_code", "create_pull_request", "get_file_contents", "list_issues"]
    },
    "playwright": {
        "name": "Playwright MCP",
        "description": "E2E browser testing, visual regression & DOM automation",
        "tools": ["navigate_page", "click_element", "take_screenshot", "evaluate_script"]
    },
    "sequential_thinking": {
        "name": "Sequential Thinking MCP",
        "description": "Multi-step analytical reasoning & complex bug root cause analysis",
        "tools": ["think_step_by_step", "validate_hypothesis", "derive_solution"]
    },
    "filesystem": {
        "name": "Filesystem MCP",
        "description": "Sandboxed air-gapped file reading, writing & AST modification",
        "tools": ["read_file_content", "write_file_content", "list_directory_tree"]
    }
}

def inject_mcp_orchestrator_prompt(system_prompt: str) -> str:
    """
    Injects the 5 Sovereign MCP Servers capability specification into AI system prompts.
    """
    mcp_block = "\n\n[🔌 LOTAI 5 SOVEREIGN MCP SERVERS ORCHESTRATOR]:\n"
    mcp_block += "You are equipped with 5 Sovereign Model Context Protocol (MCP) Servers:\n"
    for key, mcp in SOVEREIGN_MCP_SERVERS.items():
        mcp_block += f"  • {mcp['name']}: {mcp['description']} (Tools: {', '.join(mcp['tools'])})\n"
    mcp_block += "Use Sequential Thinking for multi-step reasoning, Context7 for latest docs, GitHub for repos, Playwright for visual E2E QA, and Filesystem for clean edits.\n"
    return system_prompt + mcp_block
