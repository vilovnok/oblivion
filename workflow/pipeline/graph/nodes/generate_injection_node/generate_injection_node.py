from langchain_core.output_parsers import StrOutputParser, BaseOutputParser

from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.llms._base import _BaseLLM
from workflow.pipeline.graph.state import State

import pandas as pd




class GenerateInjectionNode(_BaseNode):
    """
    
    """

    def __init__(
        self,
        name: str,
        description: str,
        llm: _BaseLLM,
        prompt: str = None,
        output_parser: BaseOutputParser = StrOutputParser(),
        show_logs: bool = False,
        model_name: str = "Vikhrmodels/Vikhr-Llama-3.2-1B-Instruct-abliterated",
    ) -> None:
        super().__init__(name, description, llm, prompt, output_parser, model_name)
        self.show_logs = show_logs

    def create_questions(self, texts: list[str]) -> list[str]:
        questions = []
        for text in texts:
            prompt_injection = self.vllm.ChatCompletion(query=text)
            questions.append(prompt_injection)
        
        return questions

    # def create_questions(self, texts: list[str]) -> list[str]:
    #     questions = []
    #     for text in texts:
    #         prompt_injection = self.vllm.ChatCompletion(query=text)
    #         questions.append(prompt_injection)
        
    #     return questions



    def invoke(self, state: State):

        texts = state.history[-1].content
        prompts_injection = []

        questions = self.create_questions(texts=texts)

        print('*'*100)
        print(questions)
        print('*'*100)

        # df = pd.DataFrame({'prompt': texts, 'prompt_injection': prompts_injection})

        if self.show_logs:
            print(self.name)            
            # print(f"Shape of DataFrame: {df.shape}")
            print("----------------")

        return {"df": state.df}
