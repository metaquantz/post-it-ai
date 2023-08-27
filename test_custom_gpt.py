from llama_index import (
    SimpleDirectoryReader,
    GPTVectorStoreIndex,
    LLMPredictor,
    ServiceContext,
    load_index_from_storage,
    StorageContext,
)
from langchain import OpenAI
import gradio as gr
import os

os.environ["OPENAI_API_KEY"] = "apikey"


def construct_index(directory_path):
    num_outputs = 512

    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0.7, model_name="text-davinci-003", max_tokens=num_outputs
        )
    )

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    docs = SimpleDirectoryReader(directory_path).load_data()

    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)

    index.storage_context.persist(persist_dir=os.getcwd())

    return index


def chatbot(input_text):
    storage_context = StorageContext.from_defaults(persist_dir=os.getcwd())
    index = load_index_from_storage(storage_context=storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response.response


def run_chatbot():
    iface = gr.Interface(
        fn=chatbot,
        inputs=gr.inputs.Textbox(lines=7, label="Enter your text"),
        outputs="text",
        title="Custom-trained AI Chatbot",
    )

    index = construct_index("docs")
    iface.launch(share=True)


run_chatbot()
