import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
try:
    from agent.utils.groq_helper import analyze_image_with_groq
except:
    from utils.groq_helper import analyze_image_with_groq

MODEL = st.secrets.get("OPENAI_MODEL")
API_KEY = st.secrets.get("OPENAI_KEY")

class State(MessagesState):
    plantuml_code: str = Field(default="", description="The PlantUML code representing the flowchart.")
    image_path: str = Field(default="", description="The path to the image file.")

@tool
def explain_plantuml_code(plantuml_code: str):
    """
    A tool that explains the given PlantUML code.
    """
    EXPLANATION_SYSTEM_MESSAGE = """
    Explain in detail the following PlantUML code.
    This is the PlantUML code:
    {plantuml_code}
    """
    system_msg = EXPLANATION_SYSTEM_MESSAGE.format(plantuml_code=plantuml_code)

    response = llm.invoke([SystemMessage(content=system_msg)])
    return response.content

@tool
def analyze_image(image_path: str):
    """
    A tool that analyzes the given image using the Groq API.
    """
    print(f"analyze_image called with image_path: {image_path}")
    prompt = "Describe the image in detail."
    response = analyze_image_with_groq(image_path, prompt=prompt)
    print(f"analyze_image response: {response}")
    return response

def assistant(state: State):
    MODEL_SYSTEM_MESSAGE = """
You are a helpful assistant specialized in explaining flowcharts. 
Your role is to answer questions based on the provided flowchart, which may be available in PlantUML format and/or as an image.

Guidelines:
1. If the user requests a description or explanation of the flowchart in PlantUML format, use the tool 'explain_plantuml_code' to generate the explanation.
2. If an image path is provided, use the tool 'analyze_image' when:
   - The user asks questions about the image.
   - The user requests a description of the image.
   - The user asks for an explanation of a specific section of the flowchart in the image.

Resources:
- PlantUML code: {plantuml_code}
- Image path: {image_path}
"""
    system_msg = MODEL_SYSTEM_MESSAGE.format(plantuml_code=state["plantuml_code"], image_path=state["image_path"])
    response = llm_with_tools.invoke([SystemMessage(content=system_msg)]+state["messages"])
    return {"messages": [response]}

def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

def invoke(message, plantuml_code, image_path=None, thread_id="1"):
    config = {"configurable": {"thread_id": thread_id}}
    messages = [HumanMessage(content=message)]
    response = graph.invoke({"messages": messages,
                             "plantuml_code":plantuml_code,
                             "image_path": image_path}, config=config)
    return response["messages"][-1].content

llm = ChatOpenAI(model=MODEL, api_key=API_KEY, temperature=1)
tools = [explain_plantuml_code, analyze_image]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

# Build the graph directly
builder = StateGraph(State)
builder.add_node("assistant", assistant)
builder.add_node("tools", tool_node)

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", should_continue, ["tools", END])
builder.add_edge("tools", "assistant")

# Checkpointer for short-term (within-thread) memory
within_thread_memory = MemorySaver()
graph = builder.compile(checkpointer=within_thread_memory)
graph_image = graph.get_graph(xray=True).draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(graph_image)

if __name__ == "__main__":
    file_path = "puml_examples/flow_1.puml"
    # Open the file and read it as a string
    with open(file_path, "r", encoding="utf-8") as file:
        puml_content = file.read()

    while True:
        user_message = input("You: ")
        if user_message.lower() == "exit":
            break
        response = invoke(user_message, plantuml_code=puml_content, thread_id="test_thread")
        print("Assistant:", response)