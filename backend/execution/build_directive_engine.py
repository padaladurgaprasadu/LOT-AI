"""
LOT AI Autonomous [BUILD] Directive Engine

This module provides the BuildDirectiveEngine for auto-planning and building multi-file projects.
It detects [BUILD] directives and generates project blueprints and file structures.
"""
import re
from typing import Dict, Any
from backend.utils.logger import get_logger

logger = get_logger(__name__)

def inject_build_directive_prompt(system_prompt: str, user_message: str) -> str:
    """
    Enhances system prompts when [BUILD] is detected in the user message.
    """
    if "[BUILD]" in user_message.upper():
        logger.info("Injecting [BUILD] directive instructions into system prompt.")
        build_instructions = (
            "\n\n[BUILD] DIRECTIVE DETECTED:\n"
            "The user has requested to build a full project. Please act as a master software architect and engineer.\n"
            "Analyze the request to determine the best project structure, technology stack, and implementation details.\n"
            "Output the response in a structured manner indicating the project type, requirements, and a detailed blueprint."
        )
        return system_prompt + build_instructions
    return system_prompt


class BuildDirectiveEngine:
    """
    Engine for processing [BUILD] directives, generating project blueprints,
    and executing the build process.
    """
    
    SUPPORTED_PROJECT_TYPES = [
        'web_app', 'rest_api', 'cli_tool', 'ml_pipeline', 
        'mobile_app', 'full_stack', 'microservice'
    ]

    def __init__(self):
        logger.info("Initialized BuildDirectiveEngine")

    def parse_build_directive(self, user_message: str) -> Dict[str, Any]:
        """
        Extracts project name, type, and requirements from a [BUILD] directive.
        """
        logger.info(f"Parsing build directive from message: {user_message[:50]}...")
        
        # Default extraction
        directive = {
            "project_name": "lot_ai_project",
            "project_type": "full_stack",
            "requirements": [],
            "description": ""
        }
        
        match = re.search(r'\[BUILD\]\s*(.*)', user_message, re.IGNORECASE | re.DOTALL)
        if match:
            description = match.group(1).strip()
            directive["description"] = description
            
            # Simple heuristic for project type
            description_lower = description.lower()
            if 'api' in description_lower or 'rest' in description_lower:
                directive["project_type"] = "rest_api"
            elif 'cli' in description_lower or 'command line' in description_lower:
                directive["project_type"] = "cli_tool"
            elif 'ml' in description_lower or 'machine learning' in description_lower or 'pipeline' in description_lower:
                directive["project_type"] = "ml_pipeline"
            elif 'mobile' in description_lower or 'ios' in description_lower or 'android' in description_lower:
                directive["project_type"] = "mobile_app"
            elif 'web' in description_lower or 'react' in description_lower or 'html' in description_lower:
                directive["project_type"] = "web_app"
            elif 'microservice' in description_lower:
                directive["project_type"] = "microservice"
                
            # Extract potential project name
            words = description.split()
            if len(words) > 0:
                # Use a simplified slug as project name
                first_few_words = "_".join(words[:3]).lower()
                clean_name = re.sub(r'[^a-z0-9_]', '', first_few_words)
                if clean_name:
                    directive["project_name"] = clean_name
            
            directive["requirements"] = [description]
            
        logger.debug(f"Parsed directive: {directive}")
        return directive

    def generate_project_blueprint(self, directive: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a file tree with file names, purposes, and code skeletons based on the directive.
        """
        logger.info(f"Generating blueprint for project type: {directive.get('project_type')}")
        
        project_name = directive.get("project_name", "app")
        project_type = directive.get("project_type", "full_stack")
        
        blueprint = {
            "project_name": project_name,
            "project_type": project_type,
            "files": []
        }
        
        if project_type == "rest_api":
            blueprint["files"] = [
                {"path": "main.py", "purpose": "Entry point for FastAPI application", "skeleton": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {'status': 'ok'}\n"},
                {"path": "requirements.txt", "purpose": "Dependencies", "skeleton": "fastapi\nuvicorn\n"}
            ]
        elif project_type == "cli_tool":
            blueprint["files"] = [
                {"path": "cli.py", "purpose": "Main CLI logic", "skeleton": "import argparse\n\ndef main():\n    parser = argparse.ArgumentParser()\n    parser.parse_args()\n\nif __name__ == '__main__':\n    main()\n"},
                {"path": "requirements.txt", "purpose": "Dependencies", "skeleton": ""}
            ]
        else:
            blueprint["files"] = [
                {"path": "app.py", "purpose": "Main application file", "skeleton": "# Main Application\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()\n"},
                {"path": "README.md", "purpose": "Project documentation", "skeleton": f"# {project_name}\n\nGenerated by LOT AI.\n"}
            ]
            
        logger.debug(f"Generated blueprint with {len(blueprint['files'])} files")
        return blueprint

    def execute_build(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns status of each file generated based on the blueprint.
        (In a real scenario, this would write to disk, but here it returns simulated status).
        """
        logger.info(f"Executing build for blueprint: {blueprint.get('project_name')}")
        
        results = {
            "status": "success",
            "files_created": []
        }
        
        for file_info in blueprint.get("files", []):
            path = file_info.get("path")
            # Simulate file creation
            logger.debug(f"Simulating creation of {path}")
            results["files_created"].append({
                "path": path,
                "status": "created",
                "bytes": len(file_info.get("skeleton", ""))
            })
            
        logger.info(f"Build executed successfully. {len(results['files_created'])} files generated.")
        return results
