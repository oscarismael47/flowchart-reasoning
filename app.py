import os
import uuid
import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image
from agent.agent import invoke 
from io import StringIO
from plantuml import PlantUML # https://github.com/vgilabert94/streamlit-image-zoom/tree/main

plantuml_server = PlantUML(url="http://www.plantuml.com/plantuml/img/") # Public PlantUML server (you can also host your own)
out_folder = "out"
diagram_path = f"{out_folder}/flow_chart.png"

# Create folder if it does not exist
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

def display_past_values(image_path, python_diagram_code):
    st.session_state.image_path = image_path
    st.session_state.python_diagram_code = python_diagram_code

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


if "image_path" not in st.session_state:
    st.session_state.image_path = None

if "uml_code" not in st.session_state:
    st.session_state.uml_code = None

if "chart_image_path" not in st.session_state:
    st.session_state.chart_image_path = None


with st.sidebar:
    
    # Display chat messages from history on app rerun
    with st.container(height=400):
        for message in st.session_state.messages:
            with st.chat_message(name=message["role"]):
                st.markdown(message["content"])
                if "image" in message["metadata"]:
                    st.image(message["metadata"]["image"], width=400)
                if "uml_code" in message["metadata"]:
                    with st.expander("PlantUML code"):
                        st.code(message["metadata"]["uml_code"], language="plantuml")

    user_input = st.chat_input("What is up?",
                                accept_file=True,
                                file_type=["jpg", "jpeg", "png", "puml"],
                            )


    if user_input:     

        user_metadata = {}
        assistant_metadata = {}


        if  user_input.text:
            message = user_input.text
        
        if  user_input["files"]:
            if user_input["files"][0].type == "application/octet-stream":
                stringio = StringIO(user_input["files"][0].getvalue().decode("utf-8"))
                st.session_state.uml_code = stringio.read()
                uml_code_name = user_input["files"][0].name
                user_metadata["uml_code"] = st.session_state.uml_code
                user_metadata["uml_code_name"] = uml_code_name


            if user_input["files"][0].type in ["image/jpeg", "image/png"]:
                image_data = user_input["files"][0]
                image_name = user_input["files"][0].name
                user_metadata["image"] = image_data
                st.session_state.image_path = f"{out_folder}/{image_name}"
                with open(st.session_state.image_path, "wb") as f:
                    f.write(image_data.read())
            

        response = invoke( message=message,
                           plantuml_code=st.session_state.uml_code,
                           image_path=st.session_state.image_path,
                           thread_id=st.session_state.chat_id)
        

        st.session_state.messages.append({"role": "user", "content": message,"metadata": user_metadata})
        st.session_state.messages.append({"role": "assistant", "content": response, "metadata": assistant_metadata})
        st.rerun()

    if st.session_state.uml_code:
        with open(diagram_path, "wb") as f:
            f.write(plantuml_server.processes(st.session_state.uml_code))
        st.session_state.chart_image_path = diagram_path

if st.session_state.chart_image_path:
    img = Image.open(st.session_state.chart_image_path)
    image_zoom(img, mode="both", size=(700, 500), keep_aspect_ratio=True, keep_resolution=True, zoom_factor=4.0, increment=0.2)
