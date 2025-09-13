# flowchart-reasoning

A Streamlit application designed to help users analyze, interpret, and reason about flowcharts by leveraging PlantUML for diagram generation and advanced AI models for automated explanations, image analysis, and interactive chat-based assistance.

## Features

- **Upload PlantUML files or flowchart images**: Supports `.puml`, `.jpg`, `.jpeg`, and `.png`.
- **Automatic diagram rendering**: Generates flowchart images from PlantUML code.
- **AI-powered explanations**: Uses OpenAI and Groq models to explain flowcharts and analyze images.
- **Chat interface**: Interact with the assistant to ask questions about your flowchart.
- **Image zoom**: Zoom and pan generated diagrams for detailed inspection.

## Usage

1. **Setup environment**  
   Create and activate a Python 3.12 virtual environment:
   ```
   # Create env
   uv venv --python 3.12

   # Activate env (Windows PowerShell)
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**
   ```
   uv pip install -r requirements.txt
   ```

3. **Configure secrets**  
   Add your API keys to `.streamlit/secrets.toml`:
   ```
   OPENAI_KEY = "your-openai-key"
   OPENAI_MODEL = "gpt-4o"  # or your preferred model
   GROQ_KEY = "your-groq-key"
   GROQ_MODEL_VISION = "groq-vision-model-name"
   ```

4. **Run the app**
   ```
   streamlit run app.py
   ```

5. **Interact**
   - Upload a PlantUML file or flowchart image.
   - Ask questions or request explanations in the chat sidebar.

## File Structure

- `app.py`: Main Streamlit app.
- `agent/agent.py`: AI agent logic and tool integration.
- `agent/utils/groq_helper.py`: Groq vision API helper.
- `puml_examples/`: Example PlantUML files.
- `requirements.txt`: Python dependencies.

## References

- [PlantUML](https://plantuml.com/)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://github.com/langchain-ai/langchain)

## Example Flowcharts

Below are example diagrams generated and used by the application:

### Shopping Cart & Coupon Logic

![Shopping Cart & Coupon Logic](./puml_examples/flow_1.png)

### Agent Reasoning Graph

![Agent Reasoning Graph](./static/graph.png)