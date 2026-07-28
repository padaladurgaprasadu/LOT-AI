import os
import argparse
from dataset_generator import DatasetGenerator

def main():
    parser = argparse.ArgumentParser(description="yAI ML Distillation Pipeline")
    parser.add_argument("--samples", type=int, default=100, help="Number of rows to generate per dataset")
    args = parser.parse_args()
    
    print("=========================================")
    print("    yAI Foundation Model Distillation    ")
    print("=========================================")
    print(f"[Pipeline] Initializing pipeline with {args.samples} samples per dataset...")
    
    output_dir = os.path.join(os.path.dirname(__file__), "datasets")
    generator = DatasetGenerator(output_dir)
    
    # 1. DPO Dataset
    dpo_path = generator.generate_karpathy_dpo(args.samples)
    print(f"  -> Successfully generated: {dpo_path}")
    
    # 2. SFT JSON Schema Dataset
    schema_path = generator.generate_swarm_sft(args.samples)
    print(f"  -> Successfully generated: {schema_path}")
    
    # 3. SFT Autonomous Debugging Dataset
    healing_path = generator.generate_self_healing_sft(args.samples)
    print(f"  -> Successfully generated: {healing_path}")
    
    print("\n[OK] Data Distillation Complete. JSONL files are ready for NVIDIA / HuggingFace upload.")

if __name__ == "__main__":
    main()
