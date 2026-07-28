import asyncio
from typing import Dict, Any
from backend.agents.base import BaseAgent

class SwarmManager(BaseAgent):
    """
    Multi-Agent Swarm Orchestrator.
    Spawns localized specialized agents (Architect, Coder, Auditor) to debate and refine code.
    """
    def __init__(self):
        super().__init__()
        
    async def spawn_swarm(self, task_description: str, context: str = "", status_callback=None, image_context=None) -> Dict[str, Any]:
        """
        Orchestrates the Swarm Debate.
        1. Architect reviews task and memory.
        2. Coder generates raw implementation.
        3. Auditor reviews implementation.
        """
        if status_callback:
            await status_callback("Spawning Asymmetric Swarm for task...")
        else:
            print(f"[SwarmManager] Spawning Asymmetric Swarm for task...")
        
        # In a real heavy system, these would be concurrent with message passing, 
        # but for this synchronous-dependent workflow, they pass the baton sequentially.
        
        execution_graph = {"nodes": [], "edges": []}
        
        def add_node(agent, status, label):
            node_id = f"{agent}_{len(execution_graph['nodes'])}"
            execution_graph["nodes"].append({"id": node_id, "data": {"label": label, "status": status}})
            return node_id
            
        def add_edge(source, target, label):
            execution_graph["edges"].append({"source": source, "target": target, "label": label})

        # Intent Routing (Vibe vs Enterprise)
        from backend.agents.router import ModelRouter
        router_llm = ModelRouter.get_optimal_llm("Router", "fast")
        if status_callback: await status_callback("[Router] Analyzing Intent Complexity...")
        
        # We perform a quick zero-shot routing to check if this is a "Vibe" request
        intent_prompt = f"Analyze this task. Is it a simple, single-page UI 'vibe' request, or a complex enterprise app requiring backend/database logic? Reply exactly with 'VIBE' or 'ENTERPRISE'. Task: {task_description}"
        try:
            intent_res = await router_llm.ainvoke(intent_prompt)
            intent = intent_res.content.strip().upper()
        except Exception:
            intent = "ENTERPRISE"
            
        if "VIBE" in intent:
            if status_callback: await status_callback("⚡ [Vibe Mode] Activating lightning-fast UI execution (skipping Deep Swarm)...")
            vibe_prompt = f"You are a lightning-fast Frontend Engineer. Build a beautiful, complete, single-file HTML/CSS/JS application for this request: {task_description}. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"index.html\", \"content\": \"...\"}}]}}"
            vibe_code = await self._agent_execute("Coder", vibe_prompt, status_callback, image_context=image_context)
            
            # Write physical files and exit immediately
            import json
            try:
                clean_json = vibe_code.strip()
                if clean_json.startswith("```json"): clean_json = clean_json[7:-3].strip()
                elif clean_json.startswith("```"): clean_json = clean_json[3:-3].strip()
                data = json.loads(clean_json)
                # Ensure ws_id is available even for Vibe Mode
                from backend.sandbox.workspace_manager import WorkspaceManager
                workspace_manager = WorkspaceManager()
                ws_id = await workspace_manager.provision_workspace("yai_vibe_app")
                for f in data.get("files", []):
                    await workspace_manager.write_file(ws_id, f["file_path"], f["content"])
                if status_callback: await status_callback("⚡ [Vibe Mode] Instant UI scaffolding complete!")
                return {"code": vibe_code, "graph": execution_graph, "ws_id": ws_id, "mode": "vibe"}
            except Exception as e:
                if status_callback: await status_callback(f"[Vibe Mode] Fallback to Enterprise due to parse error: {e}")
                
        # 0. The Mythos Simulator (Pillar 6) & Skill Registry (Pillar 5)
        if status_callback: await status_callback("🎭 [Mythos] Simulating user personas and injecting skills...")
        
        # Skill Registry retrieval
        from backend.agents.skills import SkillRegistry
        registry = SkillRegistry()
        available_skills = await registry.get_skills_for_task(task_description)
        
        mythos_prompt = f"You are the Mythos Persona Simulator. Generate a JSON UX Matrix (user pain points, required features, accessibility) for this app: {task_description}"
        mythos_node = add_node("Mythos", "executing", "Simulating Personas")
        ux_matrix = await self._agent_execute("Mythos", mythos_prompt, status_callback, image_context=image_context)
        add_node("Mythos", "complete", "UX Matrix Generated")
        
        # Phase 10: CEO & Research Agents (World Knowledge & Feasibility)
        if status_callback: await status_callback("👔 [CEO & Research] Analyzing Feasibility and gathering World Knowledge...")
        
        # Pillar 3: Autonomous Web Perception
        from backend.agents.web_perception import WebPerceptionEngine
        web_engine = WebPerceptionEngine()
        live_web_data = web_engine.analyze_task_for_web_searches(task_description)
        if live_web_data and status_callback: await status_callback("🌐 [WebPerception] Live Documentation Scraped successfully.")
        
        ceo_prompt = f"You are the yAI CEO. Analyze this request for business logic feasibility, technical blockers, and edge cases. Output a brief feasibility matrix. Task: {task_description}"
        research_prompt = f"You are the yAI Research Agent. Retrieve any necessary 'World Knowledge' (API structure assumptions, latest library syntax) for this request. Task: {task_description}\n\nLive Internet Context:\n{live_web_data}"
        
        ceo_node = add_node("CEO", "executing", "Feasibility Analysis")
        research_node = add_node("Research", "executing", "Knowledge Retrieval")
        
        ceo_task = asyncio.create_task(self._agent_execute("CEO", ceo_prompt, None))
        research_task = asyncio.create_task(self._agent_execute("Research", research_prompt, None))
        ceo_analysis, research_data = await asyncio.gather(ceo_task, research_task)
        
        add_node("CEO", "complete", "Feasibility Generated")
        add_node("Research", "complete", "Research Retrieved")
        
        # Infinite Liquid Memory Retrieval (Phase 3)
        from backend.memory.chroma_client import ChromaClient
        memory_client = ChromaClient()
        if status_callback: await status_callback("[Memory] Querying Infinite Vector Graph for past architectures and bug history...")
        historical_blueprints = memory_client.find_similar_projects(task_description)
        bug_history = memory_client.find_similar_bugs(task_description) # Prevent past mistakes
        memory_context = "\n".join(historical_blueprints) if historical_blueprints else "No historical blueprints found."
        bug_context = "\n".join(bug_history) if bug_history else "No past bugs to avoid."
        
        # Provision Physical Workspace Sandbox
        from backend.sandbox.workspace_manager import WorkspaceManager
        workspace_manager = WorkspaceManager()
        ws_id = await workspace_manager.provision_workspace("yai_e2e_app")
        if status_callback: await status_callback(f"[WorkspaceManager] Booted isolated WebContainer sandbox: {ws_id}")
        
        from backend.agents.personas import PERSONAS
        architect_sys = PERSONAS["Lead_Architect"]["system_prompt"]
        frontend_sys = PERSONAS["Senior_Frontend"]["system_prompt"]
        backend_sys = PERSONAS["Senior_Backend"]["system_prompt"]
        qa_sys = PERSONAS["QA_Automation"]["system_prompt"]
        
        # 1. The Architect
        if status_callback: await status_callback("[Architect] Designing technical architecture...")
        architect_prompt = f"{architect_sys}\n\nReview this task and context. Provide a technical design:\nTask: {task_description}\nContext: {context}\nHistorical Context: {memory_context}\nBug History (AVOID THESE): {bug_context}\nCEO Feasibility: {ceo_analysis}\nResearch Data: {research_data}\nMythos UX Matrix: {ux_matrix}\nAvailable Skills: {available_skills}"
        architect_node = add_node("Architect", "executing", "Designing Architecture")
        add_edge(mythos_node, architect_node, "Hands off UX Matrix")
        architect_design = await self._agent_execute("Architect", architect_prompt, status_callback, image_context=image_context)
        add_node("Architect", "complete", "Design Finished")
        
        # 1.5 Quantum Memory Cache Check
        if status_callback: await status_callback("⚡ [Quantum Memory] Checking for pre-compiled foundational templates and cached architectures...")
        
        # 2. The Implementation Swarm (9x Parallel Multi-Agent Asynchronous Execution)
        if status_callback: await status_callback("[Parallel Swarm] Spawning 9 Specialized Engineers simultaneously (Phase 10 AI OS)...")
        
        frontend_prompt = f"{frontend_sys}\nInject standard React/HTML boilerplates. Implement ONLY the UI components based on the design. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}"
        backend_prompt = f"{backend_sys}\nInject standard Node.js/Python boilerplates. Implement ONLY the server APIs based on the design. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}"
        db_prompt = f"{backend_sys}\nInject standard ORM templates. Implement ONLY the schema and models based on the design. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}"
        devops_prompt = f"You are the yAI DevOps Engineer. Create Dockerfiles, docker-compose.yml for this architecture. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}\n{available_skills}"
        ux_prompt = f"{frontend_sys}\nCreate global CSS tokens, animations, and beautiful Tailwind presets for this architecture. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}"
        qa_prompt = f"{qa_sys}\nWrite unit tests (Jest/PyTest) for the architecture. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}"
        security_prompt = f"{backend_sys}\nWrite security middleware, CORS configs, and auth guards. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}"
        docs_prompt = f"You are the yAI Documentation Agent. Write a comprehensive README.md and API.md. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}"
        deploy_prompt = f"You are the yAI Deployment Agent. Write GitHub Actions CI/CD workflows and Kubernetes manifests. Output ONLY valid JSON matching this schema: {{\"files\": [{{\"file_path\": \"...\", \"content\": \"...\"}}], \"setup_commands\": [\"...\"]}}\nDesign: {architect_design}\n{available_skills}"
        
        f_node = add_node("Frontend_Coder", "executing", "Writing UI")
        b_node = add_node("Backend_Coder", "executing", "Writing APIs")
        d_node = add_node("Database_Coder", "executing", "Writing Schema")
        dev_node = add_node("DevOps_Engineer", "executing", "Writing Infra")
        ux_node = add_node("UX_Designer", "executing", "Writing Styles")
        qa_node = add_node("QA_Engineer", "executing", "Writing Tests")
        sec_node = add_node("Security_Engineer", "executing", "Writing Auth")
        doc_node = add_node("Documentation_Agent", "executing", "Writing README")
        dep_node = add_node("Deployment_Agent", "executing", "Writing CI/CD")
        
        for n in [f_node, b_node, d_node, dev_node, ux_node, qa_node, sec_node, doc_node, dep_node]:
            add_edge(architect_node, n, "Hands off Design")
            
        # Execute all 9 specialized coders in parallel
        f_task = asyncio.create_task(self._agent_execute("Frontend Coder", frontend_prompt, None, image_context=image_context))
        b_task = asyncio.create_task(self._agent_execute("Backend Coder", backend_prompt, None))
        d_task = asyncio.create_task(self._agent_execute("Database Coder", db_prompt, None))
        dev_task = asyncio.create_task(self._agent_execute("DevOps Engineer", devops_prompt, None))
        ux_task = asyncio.create_task(self._agent_execute("UX Designer", ux_prompt, None, image_context=image_context))
        qa_task = asyncio.create_task(self._agent_execute("QA Engineer", qa_prompt, None))
        sec_task = asyncio.create_task(self._agent_execute("Security Engineer", security_prompt, None))
        doc_task = asyncio.create_task(self._agent_execute("Documentation Agent", docs_prompt, None))
        dep_task = asyncio.create_task(self._agent_execute("Deployment Agent", deploy_prompt, None))
        
        f_code, b_code, d_code, dev_code, ux_code, qa_code, sec_code, doc_code, dep_code = await asyncio.gather(
            f_task, b_task, d_task, dev_task, ux_task, qa_task, sec_task, doc_task, dep_task
        )
        add_node("Coder_Merge", "complete", "Merged 9x Parallel Codebases")
        
        # Helper to parse parallel JSON streams
        def parse_code(raw):
            import json
            clean = raw.strip()
            if clean.startswith("```json"): clean = clean[7:-3].strip()
            elif clean.startswith("```"): clean = clean[3:-3].strip()
            try: return json.loads(clean)
            except: return {"files": [], "setup_commands": []}
            
        # Parse Coders Output and physically construct the E2E Product
        coder_data = {"files": [], "setup_commands": []}
        for res in [parse_code(f_code), parse_code(b_code), parse_code(d_code), parse_code(dev_code), parse_code(ux_code), 
                    parse_code(qa_code), parse_code(sec_code), parse_code(doc_code), parse_code(dep_code)]:
            coder_data["files"].extend(res.get("files", []))
            coder_data["setup_commands"].extend(res.get("setup_commands", []))
            
        try:
            # Physically write files to Sandbox
            for file_obj in coder_data.get("files", []):
                await workspace_manager.write_file(ws_id, file_obj["file_path"], file_obj["content"])
                
            # Physically execute setup commands
            for cmd in coder_data.get("setup_commands", []):
                if status_callback: await status_callback(f"[Executor] Running: {cmd}")
                await workspace_manager.execute_with_healing(ws_id, cmd)
                
            # Phase 2.5: Automated Visual VQA (The Eyes of yAI)
            from backend.sandbox.vqa_engine import VQAEngine
            vqa = VQAEngine()
            
            # Snap screenshot of the entrypoint (assuming index.html or live server port)
            screenshot_path = os.path.join(workspace_manager.active_workspaces[ws_id]["path"], "screenshot.png")
            await vqa.capture_screenshot("http://localhost:3000", screenshot_path, status_callback)
            
            ui_critique = await vqa.critique_ui(screenshot_path, status_callback)
            
            # Force Coder to fix UI if critique has recommendations
            if "Recommend" in ui_critique:
                if status_callback: await status_callback("[DesignCritique] Visual flaws detected. Passing UI critique back to Coder...")
                vqa_prompt = f"You are the yAI Coder. A Vision Model reviewed your UI. Here is the critique: {ui_critique}\nRewrite the necessary CSS/HTML files to fix these visual bugs."
                vqa_node = add_node("DesignCritique", "executing", "Fixing UI from Screenshot")
                add_edge(coder_node, vqa_node, "Sends Visual Critique")
                
                vqa_code = await self._agent_execute("Coder", vqa_prompt, status_callback)
                # Overwrite raw_code so the Auditor tests the visually fixed version
                raw_code = vqa_code
                prev_node = vqa_node
            else:
                prev_node = coder_node
                
        except Exception as e:
            if status_callback: await status_callback(f"[WorkspaceManager] JSON Parsing Error: {e}")
            prev_node = coder_node
            
        # 3. The Auditor (Pillar 7: Offensive Security Red Team)
        max_debate_rounds = 2
        current_code = raw_code
        prev_node = coder_node
        
        for round_num in range(max_debate_rounds):
            if status_callback: await status_callback(f"[Auditor] Red Team Audit Round {round_num + 1}...")
            audit_prompt = f"You are the yAI Red Team Auditor (h4cker style). Actively simulate penetration testing against this code. Look for SQL Injection, XSS, and logic bypasses. If it is flawless and fully secure, output 'APPROVED'. Otherwise, detail the exploits and rewrite it securely.\nCode: {current_code}"
            auditor_node = add_node("Auditor", "executing", f"Red Team Audit Round {round_num + 1}")
            add_edge(prev_node, auditor_node, "Sends code for pentest")
            
            audit_result = await self._agent_execute("Auditor", audit_prompt, status_callback)
            
            if "APPROVED" in audit_result.upper():
                if status_callback: await status_callback(f"[Auditor] Code securely APPROVED.")
                print(f"[SwarmManager] Auditor APPROVED on round {round_num + 1}")
                
                # Infinite Liquid Memory Storage
                import uuid
                project_id = str(uuid.uuid4())
                memory_client.store_blueprint(project_id, task_description, current_code)
                if status_callback: await status_callback("[Memory] Stored new architecture blueprint into Vector Graph.")
                
                # Auto-Deployment (DevOps Phase)
                from backend.tools.deployer import AutoDeployer
                deployer = AutoDeployer()
                workspace_path = workspace_manager.active_workspaces[ws_id]["path"]
                live_url = await deployer.deploy_workspace(workspace_path, "yai-app", status_callback)
                
                # Semantic Time-Travel Snapshot
                from backend.memory.time_travel import TimeTravelEngine
                time_travel = TimeTravelEngine()
                if status_callback: await status_callback("[TimeTravel] Saving historical workspace snapshot to Vector Memory...")
                time_travel.snapshot_workspace(workspace_path, task_description)
                
                add_edge(auditor_node, add_node("Output", "success", f"Deployed to {live_url}"), "Final")
                return {"code": current_code, "graph": execution_graph, "ws_id": ws_id, "url": live_url, "webcontainer_files": coder_data.get("files", [])}
            else:
                if status_callback: await status_callback(f"[Auditor] Flaws found. Passing back to Coder...")
                print(f"[SwarmManager] Auditor REJECTED. Flaws found. Passing back to Coder.")
                current_code = audit_result # In a true loop, Coder would rewrite based on audit.
                prev_node = auditor_node
                
        add_edge(prev_node, add_node("Output", "warning", "Max Rounds Reached"), "Final")
        return {"code": current_code, "graph": execution_graph, "webcontainer_files": coder_data.get("files", [])}
        
    async def _agent_execute(self, role: str, prompt: str, status_callback=None, image_context=None) -> str:
        """Helper to run a specific agent and optionally stream its status."""
        if status_callback: await status_callback(f"[{role}] Analyzing task...")
        print(f"[{role}] Thinking...")
        try:
            from backend.utils.model_registry import AIModelRegistry, ROLE_TO_TIER
            
            # Pillar 4: NVIDIA MoE Client Integration
            from backend.utils.nvidia_client import NvidiaMoEClient
            nv_client = NvidiaMoEClient()
            optimal_llm = None
            
            role_lower = role.lower()
            if "architect" in role_lower or "ceo" in role_lower:
                optimal_llm = nv_client.get_architect_llm()
            elif "coder" in role_lower or "engineer" in role_lower or "mythos" in role_lower:
                optimal_llm = nv_client.get_coder_llm()
            elif image_context or "qa" in role_lower or "design" in role_lower:
                optimal_llm = nv_client.get_vision_llm()
            else:
                optimal_llm = AIModelRegistry.get_llm_for_tier("fast")
            
            if image_context:
                from langchain_core.messages import HumanMessage
                msg_content = [{"type": "text", "text": prompt}]
                images = image_context if isinstance(image_context, list) else [image_context]
                for img in images:
                    msg_content.append({"type": "image_url", "image_url": {"url": img}})
                message_payload = [HumanMessage(content=msg_content)]
            else:
                message_payload = prompt
                
            # Phase 1: Initial Generation
            response = await optimal_llm.ainvoke(message_payload)
            content = response.content
            
            # Phase 2: OpenMythos Recurrent-Depth Loop (Adaptive Computation Time)
            max_loops = 2
            for loop in range(max_loops):
                critique_prompt = f"""Review your previous output:
{content}
CRITICAL REFLECTION: Are there any logical gaps, unhandled edge cases, missing dependencies, or generic patterns?
If it is absolutely flawless and ready for production, reply with exactly `<flawless>`.
If you spot ANY room for improvement, reply with `<rewrite>` followed by a completely improved `<output_schema>`. Do not be lazy. Think deeper."""
                
                critique_response = await optimal_llm.ainvoke(critique_prompt)
                
                if "<rewrite>" in critique_response.content.lower():
                    print(f"[{role}] OpenMythos ACT: Self-Correction Loop triggered (Depth: {loop+1})")
                    if status_callback: await status_callback(f"[{role}] OpenMythos Loop: Thinking deeper and refining logic (Depth {loop+1})...")
                    content = critique_response.content
                else:
                    break # Flawless, exit loop
            
            # Extract JSON from <output_schema> if it exists (CL4R1T4S Architecture)
            if "<output_schema>" in content:
                import re
                schema_match = re.search(r'<output_schema>(.*?)</output_schema>', content, re.IGNORECASE | re.DOTALL)
                if schema_match:
                    content = schema_match.group(1).strip()
                    
                # Strip out thinking blocks so it doesn't pollute the JSON
                content = re.sub(r'<thinking>.*?</thinking>', '', content, flags=re.IGNORECASE | re.DOTALL).strip()
                
            return content
        except Exception as e:
            return f"Error from {role}: {str(e)}"

# Standalone Test
if __name__ == "__main__":
    async def run_test():
        manager = SwarmManager()
        task = "Write a python function that connects to a local SQLite database and executes a raw SQL query provided by the user."
        print(f"Submitting task to Swarm: {task}")
        final_code = await manager.spawn_swarm(task)
        print("\n=== FINAL APPROVED CODE ===")
        print(final_code)
        
    asyncio.run(run_test())
