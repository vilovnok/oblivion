from generator import Generator

file_path='dataset/dif_sents/sentencies_1.txt'

if __name__ == "__main__":
    gen = Generator()

    df_texts = gen.txt2df(file_path)
    
    
