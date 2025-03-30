CLASSIFIER_CATALOG_NODE_PROMPT = """
 You will be provided with text input, delimited by ###. Your task is to classify the input into one of the following categories:  
1. resume
2. job posting
3. other  

### Guidelines:  
- Classify the text as resume if it contains information about an individual's education, skills, work experience, or professional summary.  
- Classify the text as "Job Posting" if it includes details about job responsibilities, qualifications, company descriptions, or position requirements.  
- If the text does not fit into either of these categories, classify it as "Other". 
- Do not include explanations, reasoning, or any additional information in your response.  

Important:
    - your answer must be in json format {similary_name: class}

Query:
{context}  

Answer:  
"""