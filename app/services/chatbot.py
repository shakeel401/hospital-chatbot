from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from app.models.state import State
from app.services.tools import (
    get_doctor_list,
    book_doctor_appointment,
    pay_medical_bill,
    check_hospital_medicine_availability, 
    patient_symptom_checker
)


# Initialize Graph
graph_builder = StateGraph(State)
memory = MemorySaver()
# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
# Define tools
hospital_tools = [
    get_doctor_list,
    book_doctor_appointment,
    pay_medical_bill,
    check_hospital_medicine_availability,
    patient_symptom_checker
]

llm_with_tools = llm.bind_tools(hospital_tools)

def chatbot(state: State):
    system_prompt = [
        {"role": "system", "content": """You are a Hospital AI Assistant. Your role is to assist patients with hospital-related queries, such as booking appointments, checking medicine availability, processing payments, and analyzing symptoms.  

### **Responsibilities:**  
1. **Appointment & Doctor Assistance:**  
   - Provide a list of available doctors using `get_doctor_list`.  
   - Book appointments using `book_doctor_appointment`.  

2. **Medicine & Payments:**  
   - Check medicine availability with `check_hospital_medicine_availability`.  
   - Process payments through `pay_medical_bill`.  

3. **Symptom Analysis:**  
   - Assess symptoms with `patient_symptom_checker`.  
   - Provide guidance based on hospital data.  

4. **Engaging & Focused Interaction:**  
   - Keep responses accurate, concise, and helpful.  
   - If greeted, introduce yourself and explain how you can help.  
   - If asked non-medical queries, politely clarify your expertise.  
"""},
    ] + state["messages"]
    
    return {"messages": [llm_with_tools.invoke(system_prompt)]}
# Add chatbot node
graph_builder.add_node("chatbot", chatbot)

# Tool Node for executing hospital-related tools
tool_node = ToolNode(tools=hospital_tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

# Compile the graph
graph = graph_builder.compile(checkpointer=memory)

# Function to run chatbot

def run_chatbot(user_input: str, thread_id: str):
    try:
        # Create the state with user input
        state = {"messages": [HumanMessage(content=user_input)]}
        config = {"configurable": {"thread_id": thread_id}}

        # Invoke the chatbot
        response = graph.invoke(state, config=config)
        

        # Ensure response contains messages
        if not response or "messages" not in response:
            raise ValueError("Invalid response format from graph.invoke")
        
        return {"bot_message": response}

    except Exception as e:
        raise ValueError(f"Chatbot processing error: {str(e)}")
