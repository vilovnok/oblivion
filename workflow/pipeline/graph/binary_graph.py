from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph

from workflow.pipeline.graph.nodes import (
    ClassifierRouter,
    ParaphraseOrFinishRouter,
    AnswerNode,    
    MaskingNode,
    ClassifierNode,
    GenerateInjectionNode,
    GenerateQueryNode,
    RmDuplicatesNode,
    ParaphrasingNode
)

from workflow.pipeline.graph.llms import LlamaLLM
from workflow.pipeline.graph.state import State

class BinaryGraph:
    def __init__(self, 
                port: int,                
                name: str="qwen",
                model_name: str="Qwen/Qwen2.5-7B-Instruct",                
                show_logs: bool = False
    ) -> None:


        self.show_logs = show_logs
        self.history = []
        self.label = None
        self.partition = None
        self.port = port
        self.model_name = model_name
        self.graph = self._build_graph()
    
    def _build_graph(self):
        graph = StateGraph(State)

        # Initialize nodes
        classifier_node = ClassifierNode(
            name="Classifier Node",
            description=ClassifierNode.__doc__,
            model_name=self.model_name,
            port=self.port,
            show_logs=self.show_logs,
        )        
        classifier_router = ClassifierRouter(
            name="Classifier Router",
            description=ClassifierRouter.__doc__,
            mapping={
                "no": "generate_injection",
                "yes": "masking",
            },
            show_logs=self.show_logs
        )    
        paraphrase_or_finish_router = ParaphraseOrFinishRouter(
            name="Paraphrase Or Finish Router",
            description=ParaphraseOrFinishRouter.__doc__,
            mapping={
                "yes": "paraphrasing",
                "no": "answer",
            },
            show_logs=self.show_logs
        )    
        answer_node = AnswerNode(
            name="Answer Node",
            description=AnswerNode.__doc__,
            model_name=self.model_name,
            port=self.port,
            show_logs=self.show_logs,
        )       
        masking_node = MaskingNode(
            name="Masking Node",
            description=MaskingNode.__doc__,
            model_name=self.model_name,
            port=self.port,
            show_logs=self.show_logs,
        )
        generate_query_node = GenerateQueryNode(
            name="Generate Query Node",
            description=GenerateQueryNode.__doc__,
            model_name=self.model_name,
            port=self.port,
            show_logs=self.show_logs,
        )        
        generate_injection_node = GenerateInjectionNode(
            name="Generate Injection Node",
            description=GenerateInjectionNode.__doc__,
            model_name=self.model_name,
            port=self.port,
            show_logs=self.show_logs
        )   
        removing_duplicates_node = RmDuplicatesNode( 
            name="Duplicate Node",
            description=RmDuplicatesNode.__doc__,
            model_name=self.model_name,
            port=self.port,
            show_logs=self.show_logs,
        )    
        paraphrasing_node = ParaphrasingNode(
            name="Paraphrasing Node",
            description=ParaphrasingNode.__doc__,
            model_name=self.model_name,
            port=self.port,
            show_logs=self.show_logs,
        )        

        # Add nodes to graph
        graph.add_node("classifier", classifier_node.invoke)
        graph.add_node("generate_query", generate_query_node.invoke)
        graph.add_node("generate_injection", generate_injection_node.invoke)
        graph.add_node("masking", masking_node.invoke)
        graph.add_node("paraphrasing", paraphrasing_node.invoke)        
        graph.add_node("answer", answer_node.invoke)
        graph.add_node("removing_duplicates", removing_duplicates_node.invoke)

        # Set up graph relations
        graph.add_edge(START, "classifier")
        graph.add_conditional_edges(
            "classifier",
            classifier_router.invoke,
            classifier_router.mapping,
        )
        graph.add_edge("masking", 'generate_query')
        graph.add_edge("generate_query", "answer")
        graph.add_edge("generate_injection", "removing_duplicates")
        graph.add_conditional_edges(
            "removing_duplicates",
            paraphrase_or_finish_router.invoke,
            paraphrase_or_finish_router.mapping,
        )
        graph.add_edge("paraphrasing",  END)
        graph.add_edge("answer",  END)

        return graph.compile()
    

    def invoke(self, label:str, texts:list):
        self.history.append(HumanMessage(name="Start Node",content=texts)) 
        self.label = label
        answer = self.graph.invoke(
            {"history": self.history,
            "label": self.label,
            "partition": self.partition}
        )
        return answer["history"][-1]

    def clear_history(self):
        self.history = []
        self.label = None

    def resolve(self, label:str, texts:list):
        self.invoke(label=label, texts=texts)
        self.clear_history()