from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from workflow.pipeline.graph.nodes import (
    ClassifierRouter,
    # RetrieverNode,
    # AnswerNode,
    # NoInfoNode,
    ClassifierNode,
    GenerateInjectionNode,
    GenerateQueryNode
)

# from workflow.pipeline.graph.database import Retriever
from workflow.pipeline.graph.llms import LlamaLLM
from workflow.pipeline.graph.state import State

class BinaryGraph:
    def __init__(self, 
                name: str="qwen",
                model_name: str="Qwen/Qwen2.5-7B-Instruct",                
                show_logs: bool = False, 
                ) -> None:
        
        self.llm = LlamaLLM(name=name, model_name=model_name)

        self.show_logs = show_logs
        # self.save_online_metric = save_online_metric

        self.graph = self._build_graph()
        self.history = []
        self.label = None
        self.df = None

    
    def _build_graph(self):
        graph = StateGraph(State)
        # retriever = Retriever(device=0)

        # Initialize nodes
        classifier_node = ClassifierNode(
            name="Classifier Node",
            description=ClassifierNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs
        )        
        classifier_router = ClassifierRouter(
            name="Classifier Router",
            description=ClassifierRouter.__doc__,
            mapping={
                "no": "generate_injection",
                "yes": "generate_query",
            },
            show_logs=self.show_logs
        )        
        # retriever_node = RetrieverNode(
        #     name="Retriever Node",
        #     description=RetrieverNode.__doc__,
        #     retriever=retriever,
        #     show_logs=self.show_logs,
        # )
        # answer_node = AnswerNode(
        #     name="Answer Node",
        #     description=AnswerNode.__doc__,
        #     llm=self.llm,
        #     retriever=retriever,
        #     show_logs=self.show_logs
        # )       
        # no_info_node = NoInfoNode(
        #     name="NoInfoNode",
        #     description=NoInfoNode.__doc__,
        # )
        generate_query_node = GenerateQueryNode(
            name="Generate Query Node",
            description=GenerateQueryNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs
        )        
        
        generate_injection_node = GenerateInjectionNode(
            name="Generate Injection Node",
            description=GenerateInjectionNode.__doc__,
            llm=self.llm,
            show_logs=self.show_logs
        )        

        # Add nodes to graph
        graph.add_node("classifier", classifier_node.invoke)
        graph.add_node("generate_query", generate_query_node.invoke)
        graph.add_node("generate_injection", generate_injection_node.invoke)

        # graph.add_node("retriever", retriever_node.invoke)
        # graph.add_node("no_info", no_info_node.invoke)
        # graph.add_node("answer", answer_node.invoke)
        # graph.add_node("extract", extract_node.invoke)

        # Set up graph relations
        graph.add_edge(START, "classifier")
        graph.add_conditional_edges(
            "classifier",
            classifier_router.invoke,
            classifier_router.mapping,
        )
        # graph.add_edge("extract", 'retriever')
        # graph.add_edge('retriever', "answer")

        # graph.add_edge("answer",  END)
        # graph.add_edge("no_info", END)
        graph.add_edge("generate_query", END)
        graph.add_edge("generate_injection", END)

        return graph.compile()
    

    def invoke(self, label:str, texts:list):
        self.history.append(HumanMessage(content=texts)) 
        self.label = label 
        answer = self.graph.invoke(
            {"history": self.history,
            "label": self.label}
        )

        return answer["history"][-1]

    def clear_history(self):
        self.history = []
        self.activity_name = None
        self.label = None

    def resolve(self, label:str, texts:list):
        self.invoke(label=label, texts=texts)       
        self.clear_history()