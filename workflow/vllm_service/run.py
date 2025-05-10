import os
import subprocess
from dotenv import load_dotenv
from huggingface_hub import login



load_dotenv()
print(os.getenv('MODEL'))

def run():        
    model = os.getenv('MODEL')
    hf_token = os.getenv('HF_TOKEN')
    gpu_memory_utilization = os.getenv('gpu_memory_utilization')
    port = os.getenv('port_v2')

    login(token=hf_token)

    command = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", model,
        "--gpu-memory-utilization", str(gpu_memory_utilization),
        "--port", str(port)
    ]
    subprocess.run(command)

if __name__ == "__main__":
    run()