import os
import json
import asyncio
from typing import Dict, Any
from backend.sandbox.workspace_manager import WorkspaceManager

class GStackGenerator:
    """
    yAI Omni-Intelligence Pillar 4: G-Stack Generative SaaS Engine.
    Scaffolds a full-stack SaaS (React/Next.js frontend + Supabase backend) 
    in a single WebContainer-style workspace.
    """
    def __init__(self, workspace_manager: WorkspaceManager):
        self.wm = workspace_manager

    async def scaffold_saas(self, project_name: str, schema_sql: str, frontend_code: str) -> Dict[str, Any]:
        """
        Provisions a workspace and instantly writes the G-Stack boilerplate.
        """
        print(f"[GStackGenerator] Initiating Generative SaaS Build for '{project_name}'...")
        
        # 1. Provision the workspace
        ws_id = await self.wm.provision_workspace(project_name)
        
        # 2. Setup standard package.json (Hallmark + Supabase dependencies)
        package_json = {
            "name": project_name,
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@supabase/supabase-js": "^2.38.4",
                "tailwindcss": "^3.3.0",
                "lucide-react": "^0.292.0"
            }
        }
        
        await self.wm.execute_in_workspace(ws_id, f"echo '{json.dumps(package_json)}' > package.json")
        
        # 3. Scaffold Supabase DB Schema
        await self.wm.execute_in_workspace(ws_id, "mkdir -p supabase/migrations")
        
        # Escape single quotes in schema_sql for bash echo
        safe_sql = schema_sql.replace("'", "'\\''")
        await self.wm.execute_in_workspace(ws_id, f"echo '{safe_sql}' > supabase/migrations/00000000000000_init.sql")
        
        # 4. Scaffold Frontend code
        await self.wm.execute_in_workspace(ws_id, "mkdir -p src/components")
        
        safe_frontend = frontend_code.replace("'", "'\\''")
        await self.wm.execute_in_workspace(ws_id, f"echo '{safe_frontend}' > src/App.jsx")
        
        # 5. Provide Supabase Client boilerplate
        supabase_client = """
import { createClient } from '@supabase/supabase-js'
const supabaseUrl = process.env.VITE_SUPABASE_URL || 'http://127.0.0.1:54321'
const supabaseAnonKey = process.env.VITE_SUPABASE_ANON_KEY || 'anon-key'
export const supabase = createClient(supabaseUrl, supabaseAnonKey)
"""
        await self.wm.execute_in_workspace(ws_id, f"echo '{supabase_client.strip()}' > src/supabaseClient.js")

        print(f"[GStackGenerator] G-Stack successfully scaffolded in workspace {ws_id}.")
        return {
            "status": "success",
            "workspace_id": ws_id,
            "message": f"Full-stack SaaS '{project_name}' generated successfully."
        }
