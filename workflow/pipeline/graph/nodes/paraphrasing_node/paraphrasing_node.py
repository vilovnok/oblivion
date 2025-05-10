from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import AIMessage

from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.llms._base import _BaseLLM
from workflow.pipeline.graph.state import State
from workflow.generator.generator import Generator

from .prompt import prefix, system_prompt

from tqdm import tqdm

import pandas as pd


class ParaphrasingNode(_BaseNode):
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


    def create_system_prompt(self, system_prompt:str) -> str:
        gen = Generator(skip_init=True)
        instructions = "\n\n".join(["``\n"+ gen._sampling(query="\nUser's request ...") + "\n``" for _ in range(2)])        
        system_prompt = system_prompt.replace("{instructions}", instructions)

        return system_prompt


    def paraphrasing(self, texts: list[str]) -> list[str]:
        result = []

        for text in tqdm(texts, desc="Paraphrasing", unit="query"):
            text = text + '\n\n'+ prefix
            prompt = self.create_system_prompt(system_prompt=system_prompt)
            res = self.vllm.ChatCompletionEnh(system_prompt=prompt, query=text)  
            result.append(res)
            
            # print('*'*100)
            # print(f'Prompt Request:')
            # print(f'System prompt: {prompt}')
            # print('-----------'*10)
            # print(f'Response: {res}')
        return result

    def invoke(self, state: State):
        history = state.history 
        
        texts = [msg.content for msg in history if msg.name == "Generate Injection Node"]
        indexes = [msg.content for msg in history if msg.name == "Duplicate Node"]

        df = pd.DataFrame({"text": texts})
        texts = df[df.index.isin(indexes)].copy()['text']
        responses = self.paraphrasing(texts=texts)


        state.history.append(AIMessage(name=self.name, content=responses)) 
        

        if self.show_logs:
            print(self.name)            
            print(f'Paraphrasing: {responses[-1]}')
            # print(f'Paraphrased in history: {state.history}')                
            print("----------------")

        df.loc[indexes, 'text'] = responses
        df.to_csv('perep.csv', index=False)

        # df = pd.DataFrame({"pere": responses, "origin": state.history[-2].content})
        # df.to_csv('perep.csv', index=False)

        return {"history": state.history}