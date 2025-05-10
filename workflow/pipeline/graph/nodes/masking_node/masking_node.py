from langchain_core.messages import AIMessage

from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.state import State

from .prompt import system_prompt
from tqdm import tqdm



class MaskingNode(_BaseNode):
    def __init__(
        self,
        name: str,
        description: str,
        port: int = 7987,  
        prompt: str = system_prompt,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
        show_logs: bool = False,
    ) -> None:
        super().__init__(name=name, description=description, prompt=prompt, model_name=model_name, port=port)
        self.show_logs = show_logs


    def masking(self, texts:list[str]) -> list[str]:
        result = []
        for text in tqdm(texts, desc="Masking", unit="mask"):            
            response = self.vllm.ChatCompletion(query=text)            
            result.append(response + "</action>")

        return result

    def invoke(self, state: State):     
        history = state.history
        texts = history[-1].content
        responses = self.masking(texts=texts)
        state.history.append(AIMessage(name=self.name, content=responses)) 
        
        if self.show_logs:
            print(self.name)        
            print(f'Masking: {responses[-1]}')
            print(f'Masking in history: {state.history}')    
            print("----------------")

        return {"history": state.history}
