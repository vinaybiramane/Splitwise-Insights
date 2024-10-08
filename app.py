import streamlit as st
from insights_llm import create_agent
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
if not openai_api_key:
    st.error("OpenAI API key not found. Please set it in your .env file.")
    st.stop()


if __name__ == "__main__":
    st.title("Splitwise Spend QnA with Langchain Agent Workflow")

    # File upload
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Data preview:")
        st.dataframe(df.head())

        # Create agent
        agent = create_agent(df)

        # User input
        user_question = st.text_input("Ask a question about the data:")

        if user_question:
            with st.spinner("Analyzing..."):
                try:
                    response = agent.invoke(
                                            input = {
                                                "input" : user_question
                                                },
                                            handle_parsing_errors=True
                                            )
                    st.write("Answer:")
                    st.write(response)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")