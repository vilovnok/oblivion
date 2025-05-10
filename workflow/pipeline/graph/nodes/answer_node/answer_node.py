from langchain_core.output_parsers import StrOutputParser, BaseOutputParser
from langchain_core.messages import AIMessage

from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.llms._base import _BaseLLM
from workflow.pipeline.graph.state import State

import pandas as pd


class AnswerNode(_BaseNode):
    def __init__(
        self,        
        name: str,
        description: str,
        prompt: str = None,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
        port: int = 7987,
        show_logs: bool = False,
    ) -> None:
        super().__init__(name=name, description=description, prompt=prompt, model_name=model_name, port=port)
        self.show_logs = show_logs

    # def create_csv(self, prompt_injection:list[str], prompt:list[str], label: str) -> pd.DataFrame:
    #     df = pd.DataFrame({"prompt_injection":prompt_injection, "prompt":prompt})
    #     name = "data_p1.csv" if label == 'yes' else "data_p2.csv"
        
    #     df.to_csv(name, index=False)
    #     return df

    def invoke(self, state: State):     
        history = state.history
        label = state.label

        names = [store.name for store in history]
        # print(names)

    
        if label == 'no':
            texts = [msg.content for msg in history if msg.name == "Start Node"]
            texts = [text for text in texts[0]]

            prompt_injections = [msg.content for msg in history if msg.name == "Generate Injection Node"]
            prompt_injections = [prompt_injection for prompt_injection in prompt_injections[0]]

            print(len(prompt_injections))
            print(len(texts))
            # prompt_injection = history[-1].content
            # prompt = history[0].content
            df = pd.DataFrame({"text": texts, "prompt_injection": prompt_injections})
            df.to_csv('perep_new.csv', index=False)
        else:
            prompt_injections = [msg.content for msg in history if msg.name == "Start Node"]
            prompt_injections = [prompt_injection for prompt_injection in prompt_injections[0]]

            texts = [msg.content for msg in history if msg.name == "Generate Query Node"]
            texts = [text for text in texts[0]]
            
            df = pd.DataFrame({"text": texts, "prompt_injection": prompt_injections})            
            df.to_csv('perep_new_text.csv', index=False)

            # prompt = history[-1].content
            # prompt_injection = history[0].content
            # df = self.create_csv(prompt_injection=prompt_injections, prompt=prompts, label=label)        
        if self.show_logs:
            print(self.name)        
            # print(f'Shape of DataFrame: {df.shape}')
            print("----------------")
