from typing import Dict, List
from abc import ABC


from langchain_core.messages import FunctionMessage, BaseMessage

from workflow.vllm_service.openai_client import OpenAIClient
from workflow.pipeline.graph.state import State



class _BaseNode(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            port: int = 7987,
            prompt: list[str] | str = "",
            model_name: str = "Qwen/Qwen2.5-7B-Instruct",
        ) -> None:
        
        self.name = name
        self.description = description
        
        self.vllm = VLLMAdapter(prompt=prompt, model_name=model_name, port=port)

    def get_summary(self, history: List[BaseMessage]):
        print(f'History::: {history}')
        for replic in history[::-1]:
            if isinstance(replic, FunctionMessage) and replic.name == "SummarizationNode":
                return replic.content
        raise Exception("Not found summary")


class _BaseRouter(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            mapping: Dict,
        ) -> None:
        self.name = name
        self.description = description
        self._mapping = mapping

    @property
    def mapping(self):
        return self._mapping

    def invoke(self, state: State):
        pass


class VLLMAdapter(ABC):
    def __init__(self, prompt:str, model_name: str, port: int):
        
        self.prompt = prompt
        self._setupVLLM(model_name=model_name, port=port)

    def _setupVLLM(self, model_name: str, port: int):   
        self.vllm_client = OpenAIClient(model_name=model_name, port=port)        
    
    def ChatCompletion(self, query: str):
        response = self.vllm_client.ChatCompletion(system_prompt=self.prompt, query=query)
        return response
    
    def ChatCompletionEnh(self, system_prompt:str, query: str):
        response = self.vllm_client.ChatCompletion(system_prompt=system_prompt, query=query)
        return response
    
    def Completion(self, content: str, prompt:str=None,):
        if not prompt:
            prompt = self.prompt
        response = self.vllm_client.Completion(prompt=prompt, content=content)
        return response