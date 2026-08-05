"""
LOT AI 7-Layer AIOS Architecture Blueprint.
Defines the core structure and components of the LOT AI operating system.
"""

import json
from backend.utils.logger import get_logger

logger = get_logger(__name__)

class LOTAIArchitectureBlueprint:
    """
    Represents the 7-Layer Architecture Blueprint for LOT AI.
    """
    def __init__(self):
        self.layers = {
            "Layer 1: Hardware Abstraction": [
                "NVIDIA NIM",
                "GPU clusters"
            ],
            "Layer 2: Model Nebula": [
                "12 NVIDIA models",
                "8 frontier models",
                "MoE router"
            ],
            "Layer 3: Agent Swarm": [
                "37 expert agents (40yr experience each)"
            ],
            "Layer 4: Memory & Intelligence": [
                "Sovereign Memory",
                "ChromaDB",
                "Neo4j",
                "Knowledge Graph"
            ],
            "Layer 5: Execution Runtime": [
                "Sandbox",
                "Docker VM",
                "AST Analyzer",
                "Self-Healing"
            ],
            "Layer 6: MCP Protocol": [
                "5 Sovereign MCP Servers",
                "Context7",
                "GitHub",
                "Playwright",
                "Sequential",
                "Filesystem"
            ],
            "Layer 7: Application Interface": [
                "API Gateway",
                "CLI",
                "Web UI",
                "SDK"
            ]
        }
        logger.info("Initialized LOTAIArchitectureBlueprint")

    def generate_json_blueprint(self) -> str:
        """
        Returns the full architecture blueprint as a JSON string.
        """
        logger.info("Generating JSON blueprint")
        return json.dumps(self.layers, indent=4)

    def generate_mermaid_diagram(self) -> str:
        """
        Returns a Mermaid diagram string representing the architecture.
        """
        logger.info("Generating Mermaid diagram")
        mermaid = ["graph TD;"]
        
        layers = list(self.layers.keys())
        # Connect layers hierarchically
        for i in range(len(layers) - 1):
            mermaid.append(f'    "{layers[i + 1]}" --> "{layers[i]}";')
            
        # Add components to layers
        for layer, components in self.layers.items():
            for comp in components:
                mermaid.append(f'    "{layer}" --- "{comp}";')
                
        return "\n".join(mermaid)


def inject_architecture_prompt(system_prompt: str) -> str:
    """
    Injects the architecture blueprint into a provided system prompt.
    
    Args:
        system_prompt (str): The original system prompt.
        
    Returns:
        str: The updated system prompt containing the architecture blueprint.
    """
    blueprint = LOTAIArchitectureBlueprint()
    architecture_json = blueprint.generate_json_blueprint()
    
    injected_prompt = (
        f"{system_prompt}\n\n"
        f"--- LOT AI Architecture Blueprint ---\n"
        f"{architecture_json}\n"
    )
    logger.info("Injected architecture blueprint into system prompt")
    return injected_prompt
