import os
import json
import random

class DatasetGenerator:
    """
    yAI Distillation Engine.
    Procedurally generates highly specific training datasets for fine-tuning 
    massive parameter models (like Nemotron-3-Ultra) for agentic workflows.
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
    def generate_karpathy_dpo(self, num_samples: int = 100):
        """
        Direct Preference Optimization Dataset to eliminate conversational filler.
        Format: {"prompt": "...", "chosen": "...", "rejected": "..."}
        """
        filepath = os.path.join(self.output_dir, "karpathy_dpo.jsonl")
        print(f"[DatasetGenerator] Synthesizing {num_samples} samples for DPO (Karpathy Mode)...")
        
        prompts = [
            "Write a python script to reverse a string.",
            "Fix the CORS error in this Express app.",
            "Generate a React button component.",
            "How do I connect to MongoDB in Node?"
        ]
        
        yapping_prefixes = [
            "Hello there! I would be absolutely delighted to assist you with this.",
            "Certainly! Here is the code you requested.",
            "I apologize for any previous confusion. To solve this issue:",
            "Sure thing! Let me break this down for you step-by-step."
        ]
        yapping_suffixes = [
            "\n\nI hope this helps! Please let me know if you need any further assistance.",
            "\n\nIf you have any more questions, feel free to ask!",
            "\n\nHappy coding!"
        ]
        
        valid_responses = [
            "```python\ndef reverse_string(s):\n    return s[::-1]\n```",
            "```javascript\napp.use(cors({ origin: '*' }));\n```",
            "```jsx\nexport const Button = () => <button className='btn'>Click</button>;\n```",
            "```javascript\nawait mongoose.connect(process.env.MONGO_URI);\n```"
        ]

        with open(filepath, 'w', encoding='utf-8') as f:
            for _ in range(num_samples):
                idx = random.randint(0, len(prompts)-1)
                prompt = prompts[idx]
                code = valid_responses[idx]
                
                chosen = code
                rejected = f"{random.choice(yapping_prefixes)}\n{code}{random.choice(yapping_suffixes)}"
                
                row = {
                    "prompt": prompt,
                    "chosen": chosen,
                    "rejected": rejected
                }
                f.write(json.dumps(row) + "\n")
                
        return filepath

    def generate_swarm_sft(self, num_samples: int = 100):
        """
        Supervised Fine Tuning Dataset for strict Swarm JSON schema compliance.
        Format: {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
        """
        filepath = os.path.join(self.output_dir, "swarm_schema_sft.jsonl")
        print(f"[DatasetGenerator] Synthesizing {num_samples} samples for SFT (Swarm Schema Compliance)...")
        
        tasks = [
            "Build the UI for the login page.",
            "Create the User model in SQLAlchemy.",
            "Write the deployment Dockerfile."
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for _ in range(num_samples):
                task = random.choice(tasks)
                
                system_prompt = "You are the yAI Coder. Output ONLY valid JSON matching this schema: {\"files\": [{\"file_path\": \"...\", \"content\": \"...\"}], \"setup_commands\": [\"...\"]}"
                
                # Perfect JSON generation
                target_json = {
                    "files": [{"file_path": "src/App.jsx", "content": "// Code"}],
                    "setup_commands": ["npm install"]
                }
                
                row = {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Task: {task}"},
                        {"role": "assistant", "content": f"```json\n{json.dumps(target_json)}\n```"}
                    ]
                }
                f.write(json.dumps(row) + "\n")
                
        return filepath

    def generate_self_healing_sft(self, num_samples: int = 100):
        """
        Supervised Fine Tuning Dataset for autonomous self-healing and debugging.
        """
        filepath = os.path.join(self.output_dir, "self_healing_sft.jsonl")
        print(f"[DatasetGenerator] Synthesizing {num_samples} samples for SFT (Autonomous Debugging)...")
        
        errors = [
            "TypeError: Cannot read properties of undefined (reading 'map')",
            "ModuleNotFoundError: No module named 'langchain_google_genai'",
            "SyntaxError: Unexpected token '<'"
        ]
        
        fixes = [
            "Added optional chaining `?.map()` to prevent crashes on undefined data arrays.",
            "Added `langchain-google-genai` to `requirements.txt` and ran `pip install`.",
            "Fixed JSX syntax error by wrapping sibling elements in a React Fragment `<></>`."
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for _ in range(num_samples):
                idx = random.randint(0, len(errors)-1)
                
                row = {
                    "messages": [
                        {"role": "system", "content": "You are the yAI Debugger. Fix the provided stack trace by outputting a Git patch or explanation."},
                        {"role": "user", "content": f"The build failed with this error:\n{errors[idx]}"},
                        {"role": "assistant", "content": fixes[idx]}
                    ]
                }
                f.write(json.dumps(row) + "\n")
                
        return filepath
