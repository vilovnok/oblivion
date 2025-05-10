import os
import pandas as pd
from dotenv import load_dotenv

from workflow.pipeline.graph.binary_graph import BinaryGraph


load_dotenv()


def main():
    label2text = {}
    graph = BinaryGraph(model_name=os.getenv("MODEL"), 
                        port=os.getenv("port_v2"), 
                        show_logs=True)

    for label, texts in zip(label2text.keys(),label2text.values()):
        graph.resolve(label=label, texts=texts)        

if __name__ == '__main__':
    main()