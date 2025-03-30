import openai


class OpenAIClient:
    def __init__(self, port: str, model_name: str=None, openai_key: str=None):    

        openai_key="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"
        self.model_name = model_name        
        self.__setup_openai(api_key=openai_key, port=port) 
    
    def __setup_openai(self, api_key:str, port:str):
        openai.api_key = api_key
        openai.api_base = f"http://localhost:{port}/v1"

        self.client = openai


    def ChatCompletion(self, system_prompt:str, query:str):        
        try:
            messages=[ 
                {"role": "system", "content": system_prompt}, 
                {"role": "user", "content": query}
            ]

            response = self.client.ChatCompletion.create(
                model=self.model_name,
                temperature=0.2,
                frequency_penalty=0.2,
                max_tokens=1024,
                top_p=0.8,
                messages=messages
            )            
            answer = response["choices"][0]["message"]["content"]
            return answer

        except openai.error.InvalidRequestError as e:
            print(f"Invalid request: {e}")
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI error: {e}")        
        except Exception as e:
            print(f"Other error occurred: {e}")

    def Completion(self, prompt:str, content:str):
        prompt = prompt.replace('{context}', content)
        try:
            response = openai.Completion.create(
                model=self.model_name,
                temperature=0.0,
                prompt = prompt,
                max_tokens=1024,
            )
            return response["choices"][0]["text"]
        except Exception as error:
            print(f"Ошибка при вызове OpenAI:\n{error}")
        except openai.error.InvalidRequestError as e:
            print(f"Invalid request: {e}")
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI error: {e}")        
        except Exception as e:
            print(f"Other error occurred: {e}")

    def invoke(self, prompt: str, content:str):
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                temperature=0.2,
                frequency_penalty=0.2,
                max_tokens=784,
                top_p=0.8,
                messages=[
                    {"role": "system", "content": f'{prompt}'},
                    {"role": "user", "content": f'{content}'}
                    ]
                )
            return response["choices"][0]["message"]["content"]
        except Exception as error:
            print(f"Ошибка при вызове OpenAI:\n{error}")