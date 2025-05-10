from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import AIMessage

from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.llms._base import _BaseLLM
from workflow.pipeline.graph.state import State

from .prompt import system_prompt

from tqdm import tqdm

class GenerateQueryNode(_BaseNode):
    """
    
    """

    def __init__(
        self,        
        name: str,
        description: str,
        prompt: str = system_prompt,
        port: int = 7987,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
        show_logs: bool = False,
    ) -> None:
        super().__init__(name=name, description=description, prompt=prompt, model_name=model_name, port=port)
        self.show_logs = show_logs        

    def generate_query(self, texts:list[str]) -> list[str]:
        result = []        
        for text in tqdm(texts, desc="Generating queries", unit="query"):
            text = "Text: " + text + "\n\nYou must only return question: "
            response = self.vllm.ChatCompletion(query=text)        
            result.append(response)
        return result
    
    def invoke(self, state: State):
        texts = state.history[-1].content 

        responses = self.generate_query(texts=texts)
        state.history.append(AIMessage(name=self.name, content=responses)) 
        
        if self.show_logs:
            print(self.name)            
            print(f'Generated queries: {responses[-1]}')
            # print(f'Generated in history: {state.history}')                
            print("----------------")

        return {"history": state.history}
