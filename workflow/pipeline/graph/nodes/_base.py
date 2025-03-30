from typing import Dict, List
from abc import ABC

from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import FunctionMessage, BaseMessage
from langchain_core.prompts import PromptTemplate

from workflow.pipeline.graph.llms._base import _BaseLLM
from workflow.pipeline.graph.state import State
from workflow.vllm_service.openai_client import OpenAIClient


class _BaseNode(ABC):
    def __init__(
            self,
            name: str,
            description: str,
            llm: _BaseLLM,
            prompt: list[str] | str = "",
            output_parser: BaseOutputParser = StrOutputParser(),
            port: int = 7986,
            model_name: str = None
        ) -> None:
        
        self.name = name
        self.description = description
        self.chain = None # PromptTemplate.from_template(prompt) | llm.llm | output_parser
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
    
    def Completion(self, content: str, prompt:str=None,):
        if not prompt:
            prompt = self.prompt
        response = self.vllm_client.Completion(prompt=prompt, content=content)
        return response