from generator import Generator

file_path='/dataset/terrible_queries/sentencies_1.txt'

if __name__ == "__main__":
    gen = Generator()
    df_texts = gen.txt2df(file_path)
    
    
