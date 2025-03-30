import pandas as pd
from transformers import AutoTokenizer
from tqdm import tqdm

def prompt_classification(df: pd.DataFrame, model_name:str="cgoosen/prompt-tackler", batch_size:int=8, max_tokens:int=512):    

    tokenizer = AutoTokenizer.from_pretrained(model_name)    
    df = df.reset_index(drop=False)
    
    results = []
    
    for batch_start in tqdm(range(0, len(df), batch_size), desc="Классификация", unit="batch"):        
        batch_end = min(batch_start + batch_size, len(df))
        batch = df.iloc[batch_start:batch_end]
        
        batch_texts =   []
        batch_indices = []


        for idx, row in batch.iterrows():
            tokens = tokenizer(row['text'], truncation=True, return_tensors="pt")
            if len(tokens.input_ids[0]) <= max_tokens:
                batch_texts.append(row['text'])
                batch_indices.append(row['index'])

        
        batch_results = classifier(batch_texts)
        
        for i, res in enumerate(batch_results):            
            if res['label']=='benign':
                results.append(batch_indices[i])
    
    return results