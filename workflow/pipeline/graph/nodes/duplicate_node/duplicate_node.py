from workflow.pipeline.graph.nodes._base import _BaseNode
from workflow.pipeline.graph.state import State

from langchain_core.messages import AIMessage

from tqdm import tqdm

import re
import pandas as pd

class RmDuplicatesNode(_BaseNode):
    """
    
    """

    def __init__(
        self,        
        name: str,
        description: str,
        port: int = 7987,
        model_name: str = "Qwen/Qwen2.5-7B-Instruct",
        show_logs: bool = False,
    ) -> None:
        super().__init__(name=name, description=description, model_name=model_name, port=port)
        self.show_logs = show_logs

    def get_first_n_tokens(self, text:str, n=5):
        tokens = re.findall(r'\w+', text)
        return ' '.join(tokens[:n]) 

    def find_duplicate_texts(self, df: pd.DataFrame, column_name: str='text', threshold: int = 5):
        df = df.copy()
        df["token_group"] = df[column_name].apply(lambda x: self.get_first_n_tokens(x, 5))
        duplicate_indexes = []
        seen_counts = {}
        
        for idx, row in df.iterrows():
            key = row["token_group"]
            if key not in seen_counts:
                    seen_counts[key] = 0
            seen_counts[key] += 1

            if seen_counts[key] > threshold:
                duplicate_indexes.append(idx)
        
        return duplicate_indexes, seen_counts

    def invoke(self, state: State):
        texts = state.history[-1].content 
        
        sample_ground_truth, len_ground_truth = 'nan', 'any'
        sample_ground_drop, len_ground_drop = 'nan', 'any'

        df = pd.DataFrame({"text": texts})
        indexes, counts = self.find_duplicate_texts(df=df)
        
        print('\n\n')
        print(f"Indexes {indexes}")
        print('\n\n')
        
        # if indexes:

        #     ground_truth  = df[~df.index.isna(indexes)].copy()['text']
        #     ground_drop = df[df.index.isna(indexes)].copy()['text']

        #     sample_ground_truth, len_ground_truth = ground_truth[-1], len(ground_truth)
        #     sample_ground_drop, len_ground_drop = ground_drop[-1], len(ground_drop)

        #     state.history.append(AIMessage(name=f'{self.name}-No', content=ground_truth)) 
        #     state.history.append(AIMessage(name=f'{self.name}-Yes', content=sample_ground_drop)) 
            
        indexes = [str(index) for index in indexes]
        state.history.append(AIMessage(name=f'{self.name}', content=indexes)) 

            # state.partition = True
        
        if self.show_logs:
            print(self.name)            
            print(f'Ground Truth: \n{sample_ground_truth}\nAll shapes: {len(len_ground_truth)}')
            print(f'Ground Drop: \n{sample_ground_drop}\nAll shapes: {len(len_ground_drop)}')
            print("----------------")

        return {"history": state.history}
