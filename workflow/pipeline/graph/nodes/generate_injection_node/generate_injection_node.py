from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.generator.generator import Generator
from workflow.pipeline.graph.state import State

from langchain_core.messages import AIMessage

from .prompt import prompt

import pandas as pd

class GenerateInjectionNode(_BaseNode):
    """
    
    """
    def __init__(
        self,
        name: str,
        description: str,
        prompt: str = prompt,
        show_logs: bool = False,
        port: int = 7987,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
    ) -> None:
        super().__init__(name=name, description=description, prompt=prompt, model_name=model_name, port=port)
        self.show_logs = show_logs

    def create_actions(self, df: pd.DataFrame) -> list[str]:
        generator = Generator(df=df)        
        df_0_25 = generator.generate_prompt(funlike='circled', percentage_range=[0.0, 0.25], addition_prompt=True)
        df_25_50 = generator.generate_prompt(funlike='space', percentage_range=[0.25, 0.5], addition_prompt=True)
        df_50_75 = generator.generate_prompt(funlike='unicode', percentage_range=[0.5, 0.75], addition_prompt=True)
        df_75_1 = generator.generate_prompt(funlike='txt', percentage_range=[0.75, 1.0], addition_prompt=True)

        
        df_full = pd.DataFrame({"prompt_injection":(df_0_25['prefixes_circled'].to_list() + 
                                                    df_25_50['prefixes_space'].to_list() + 
                                                    df_50_75['prefixes_unicode'].to_list() + 
                                                    df_75_1['prefixes_txt'].to_list())})
        
        
        return df_full['prompt_injection'].to_list()

    def invoke(self, state: State):
        texts = state.history[-1].content        
        df = pd.DataFrame({'action': texts})

        print(df.shape)
        
        responses = self.create_actions(df=df)
        state.history.append(AIMessage(name=self.name, content=responses)) 

        if self.show_logs:
            print(self.name)            
            print(f"Shape of DataFrame: {len(responses)}")
            print("----------------")

        return {"history": state.history}
