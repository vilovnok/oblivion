import hydra
from omegaconf import DictConfig

import subprocess

from huggingface_hub import login


@hydra.main(version_base=None, config_path="../../", config_name="config")
def run(cfg: DictConfig):        
    
    login(token=cfg.model.hf_token)
    
    command = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", cfg.model.synth_model,
        "--gpu-memory-utilization", str(cfg.model.gpu_memory_utilization),
        "--port", str(cfg.api.port_another)
    ]
    subprocess.run(command)


if __name__ == "__main__":
    run()