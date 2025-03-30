import torch
import pandas as pd
from tqdm import tqdm

from transformers import pipeline
from transformers import AutoTokenizer
from transformers.pipelines.text_classification import TextClassificationPipeline


class Engine:
    def __init__(self, model_name:str):

        self._setupModel(model_name=model_name)
        self.__tokenizer = AutoTokenizer.from_pretrained(model_name)    


    def _setupModel(self, model_name:str):
        self.__classifier = pipeline(
            "text-classification",
            model=model_name,
            device="cuda" if torch.cuda.is_available() else "cpu"
    )


    def classification(self, df: pd.DataFrame, batch_size:int=8, max_tokens:int=512):    
        """
        Prompt classification
        """
        df = df.reset_index(drop=False)
        
        results = []
        
        for batch_start in tqdm(range(0, len(df), batch_size), desc="Классификация", unit="batch"):        
            batch_end = min(batch_start + batch_size, len(df))
            batch = df.iloc[batch_start:batch_end]
            
            batch_texts =   []
            batch_indexes = []

            for _, row in batch.iterrows():
                tokens = self.__tokenizer(row['text'], truncation=True, return_tensors="pt")
                if len(tokens.input_ids[0]) <= max_tokens:
                    batch_texts.append(row['text'])
                    batch_indexes.append(row['index'])
            
            batch_results = self.__classifier(batch_texts)            
            for i, res in enumerate(batch_results):            
                if res['label']=='benign':
                    results.append(batch_indexes[i])
        
        return results