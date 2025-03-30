import hydra
from omegaconf import DictConfig
import threading
import subprocess

from huggingface_hub import login


@hydra.main(version_base=None, config_path="../../", config_name="config")
def run(cfg: DictConfig):        
    
    login(token=cfg.model.hf_token)
    
    command = [
        "python", "-m", "vllm.entrypoints.openai.api_server",
        "--model", cfg.model.qwen,
        "--gpu-memory-utilization", str(cfg.model.gpu_memory_utilization),
        "--port", str(cfg.api.port_another)
    ]
    subprocess.run(command)


if __name__ == "__main__":
    run()



# # import subprocess
# # import threading
# # from omegaconf import DictConfig
# # import hydra
# # from huggingface_hub import login

# def start_vllm_server(command: list, server_name: str):
#     """Запускает vLLM сервер в отдельном потоке"""
#     print(f"Запуск {server_name} сервера: {' '.join(command)}")
#     try:
#         subprocess.run(command, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Ошибка в {server_name} сервере: {e}")

# @hydra.main(version_base=None, config_path="../../", config_name="config")
# def run(cfg: DictConfig):
#     # Аутентификация в Hugging Face
#     login(token=cfg.model.hf_token)
    
#     # Конфигурация для основного сервера
#     main_server_cmd = [
#         "python", "-m", "vllm.entrypoints.openai.api_server",
#         "--model", cfg.model.synth_model,
#         "--gpu-memory-utilization", str(cfg.model.gpu_memory_utilization),
#         "--port", str(cfg.api.port),
#         "--tensor-parallel-size", "1"  # 1 GPU на сервер
#     ]
    
#     # Конфигурация для второго сервера (другой порт/модель)
#     second_server_cmd = [
#         "python", "-m", "vllm.entrypoints.openai.api_server",
#         "--model", cfg.model.qwen,  # Добавьте в config.yaml
#         "--gpu-memory-utilization", str(cfg.model.gpu_memory_utilization),
#         "--port", str(cfg.api.port_another + 1),  # Следующий порт
#         "--tensor-parallel-size", "1"
#     ]
    
#     # Запуск в отдельных потоках
#     threads = [
#         threading.Thread(target=start_vllm_server, args=(main_server_cmd, "основной")),
#         threading.Thread(target=start_vllm_server, args=(second_server_cmd, "вторичный"))
#     ]
    
#     for t in threads:
#         t.start()
    
#     # Ожидание завершения (по Ctrl+C)
#     for t in threads:
#         t.join()

# if __name__ == "__main__":
#     run()