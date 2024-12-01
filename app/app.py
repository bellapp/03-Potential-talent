import streamlit as st
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from langchain_community.llms import HuggingFaceHub
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import tempfile
import os
import pandas as pd
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ModelManager:
    @staticmethod
    def get_available_local_models() -> list:
        return ["mistral:instruct", "llama2", "codellama", "neural-chat"]

    @staticmethod
    def get_available_groq_models() -> list:
        return ["llama2-70b-4096", "mixtral-8x7b-32768", "gemma-7b-it"]

    @staticmethod
    def get_available_huggingface_models() -> list:
        return ["google/flan-t5-xxl", "gpt2", "facebook/opt-1.3b"]

    @staticmethod
    def initialize_model(model_provider: str, model_name: str) -> Any:
        try:
            if model_provider == "Local (Ollama)":
                return Ollama(
                    model=model_name,
                    base_url="http://ollama:11434"  # Using Docker service name
                )
            elif model_provider == "Groq":
                groq_api_key = os.getenv("GROQ_API_KEY")
                if not groq_api_key:
                    st.error("Groq API key not found!")
                    return None
                return ChatGroq(api_key=groq_api_key, model_name=model_name)
            elif model_provider == "HuggingFace":
                hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
                if not hf_api_key:
                    st.error("HuggingFace API key not found!")
                    return None
                return HuggingFaceHub(repo_id=model_name, huggingfacehub_api_token=hf_api_key)
            return None
        except Exception as e:
            st.error(f"Error initializing model: {e}")
            return None

class JobSimilarityApp:
    def __init__(self):
        self.model_manager = ModelManager()
        self.prompt_template = self.create_prompt()

    @staticmethod
    def create_prompt() -> ChatPromptTemplate:
        template = """Analyze the following entries and find similar matches to the query.
        Use cosine similarity to rank each entry.

        Query: {query}

        Entries to compare:
        {entries}

        Output: Provide the top 5 ranking job titles with their:
        1. Job Title
        2. ID
        3. Location
        4. Similarity Score (0-1)

        Format each result on a new line with clear separation.
        """
        return ChatPromptTemplate.from_template(template=template)

    def setup_sidebar(self) -> Dict[str, Any]:
        with st.sidebar:
            st.header("Configuration")

            # Model Selection
            st.subheader("Model Selection")
            model_provider = st.selectbox(
                "Select Model Provider",
                ["Local (Ollama)", "Groq", "HuggingFace"]
            )

            if model_provider == "Local (Ollama)":
                available_models = self.model_manager.get_available_local_models()
            elif model_provider == "Groq":
                available_models = self.model_manager.get_available_groq_models()
            else:
                available_models = self.model_manager.get_available_huggingface_models()

            model_name = st.selectbox("Select Model", available_models)

            # Data Management
            st.subheader("Data Management")
            uploaded_files = st.file_uploader(
                "Upload CSV Files",
                type=['csv'],
                accept_multiple_files=True
            )

            if uploaded_files:
                st.write("Uploaded files:")
                for file in uploaded_files:
                    st.write(f"- {file.name}")

            return {
                "model_provider": model_provider,
                "model_name": model_name,
                "uploaded_files": uploaded_files
            }

    def process_csv(self, uploaded_file, query: str, model) -> tuple:
        tmp_file_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name

            loader = CSVLoader(
                file_path=tmp_file_path,
                csv_args={"delimiter": ";"},
            )
            data = loader.load()

            entries = [doc.page_content for doc in data]
            chain = LLMChain(llm=model, prompt=self.prompt_template)

            with st.spinner("Analyzing job titles..."):
                response = chain.run(query=query, entries=entries)

            return response, data[:5]

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            return None, None
        finally:
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

    def display_results(self, response: str):
        if response:
            st.markdown("### Analysis Results")
            st.markdown("---")

            results = response.split('\n')
            for result in results:
                if result.strip():
                    st.markdown(f"- {result}")

            st.download_button(
                label="Download Results",
                data=response,
                file_name="similarity_results.txt",
                mime="text/plain"
            )

    def run(self):
        st.title("Job Title Similarity Search")

        config = self.setup_sidebar()

        model = self.model_manager.initialize_model(
            config["model_provider"],
            config["model_name"]
        )

        if not model:
            st.error("Failed to initialize model. Please check your configuration.")
            return

        st.markdown("""
        ## Job Title Analysis
        Search for similar job titles in your dataset.

        **File Requirements:**
        - CSV format with semicolon (;) delimiter
        - Required columns: job_title, id, location
        """)

        if config["uploaded_files"]:
            selected_file = st.selectbox(
                "Select file to analyze",
                [file.name for file in config["uploaded_files"]]
            )

            selected_file_obj = next(
                (f for f in config["uploaded_files"] if f.name == selected_file),
                None
            )

            if selected_file_obj:
                try:
                    df = pd.read_csv(selected_file_obj, sep=";")
                    st.subheader("Sample of selected data")
                    st.dataframe(df.head())

                    query = st.text_input(
                        "Enter your search query:",
                        placeholder="e.g., 'Human Resources Manager'"
                    )

                    if query:
                        response, sample_data = self.process_csv(
                            selected_file_obj,
                            query,
                            model
                        )
                        if response:
                            self.display_results(response)

                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    app = JobSimilarityApp()
    app.run()