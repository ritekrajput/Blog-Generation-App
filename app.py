import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import streamlit as st
from langchain.prompts import PromptTemplate
import os

## Function To get response from LLAma 3.2 model

def getLLamaresponse(input_text, no_words, blog_style):
    ### LLama3.2 model
    model_id = "meta-llama/Llama-3.2-3B"
    st.write("use_auth_token",st.secrets["DB_TOKEN"])

    # Load the model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True,use_auth_token=["DB_TOKEN"])
    tokenizer = AutoTokenizer.from_pretrained(model_id,use_auth_token=st.secrets["DB_TOKEN"])

    llm = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
        device_map="auto"
    )
    
    ## Prompt Template
    template = """
        Write a blog on {input_text} for {blog_style}.Keep it engaging ,informative,and around {no_words} words.
            """
    
    prompt = PromptTemplate(input_variables=["blog_style", "input_text", 'no_words'],
                            template=template)
    
    formatted_prompt = prompt.format(blog_style=blog_style, input_text=input_text, no_words=no_words)
    
    ## Generate the response from the LLama 3.2 model
    response = llm(formatted_prompt, max_length=int(no_words) + len(formatted_prompt.split()), pad_token_id=tokenizer.eos_token_id, truncation=True)
    print(response)
    return response


st.set_page_config(page_title="Generate Blogs",
                    page_icon='🤖',
                    layout='centered',
                    initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

input_text=st.text_input("Enter the Blog Topic")

## creating to more columns for additonal 2 fields

col1,col2=st.columns([5,5])

with col1:
    no_words=st.text_input('No of Words')
with col2:
    blog_style=st.selectbox('Writing the blog for',
                            ('Researchers','Data Scientist','Common People'),index=0)
    
submit=st.button("Generate")

## Final response
if submit:
    st.write(getLLamaresponse(input_text,no_words,blog_style))
