import pandas as pd
import os
from dotenv import load_dotenv
from langchain import hub
from langchain_experimental.agents import create_csv_agent, create_pandas_dataframe_agent
from langchain_openai import AzureChatOpenAI


load_dotenv()

def create_agent(df):
    
    base_prompt = hub.pull('langchain-ai/react-agent-template')
    
    # print("Base Prompt", base_prompt.template)
    
    csv_agent = create_pandas_dataframe_agent(
    prompt = base_prompt,
    llm = AzureChatOpenAI(
        azure_deployment="gpt-35-turbo",  # or your deployment
        api_version="2023-03-15-preview",  # or your api version
        temperature=0),
    df = df,
    verbose = True,
    allow_dangerous_code=True
    )
    
    return csv_agent

if __name__ == "__main__":
    
    uploaded_file = 'Splitwise export for Home.csv'
    df = pd.read_csv(uploaded_file)
    
    agent = create_agent(df)
    
    user_question = 'Please give category wise spending of each person from september month onwards. Only consider positive values'
    response = agent.invoke(
                                            input = {
                                                "input" : user_question
                                                },
                                            handle_parsing_errors=True
                                            )