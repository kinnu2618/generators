import os
import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key  

# Configure the API key for Google Gemini AI
genai.configure(api_key=google_gemini_api_key)

# Configuration for generation
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "max_output_tokens": 2048,
    "response_mime_type": "text/plain",
}

# Define the GenerativeModel for Gemini 1.0 Pro
model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
)

# Function to generate a blog post
def generate_blog_post(title, keywords, num_words):
    prompt = (
        f"Generate a comprehensive, engaging blog post relevant to the title '{title}' "
        f"and incorporating the keywords: {keywords}. The blog should be approximately {num_words} words long."
    )
    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [prompt]}]
    )
    response = chat_session.send_message(prompt)
    return response.text

# Function to generate code
def generate_code(problem_statement, programming_language, programming_type):
    prompt = (
        f"Generate code for the following problem statement: '{problem_statement}' "
        f"in {programming_language}. The code should be in {programming_type} type of programming."
    )
    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [prompt]}]
    )
    response = chat_session.send_message(prompt)
    return response.text

# Function to translate text
def translate_text(input_language, output_language, text):
    prompt = (
        f"Translate this text from {input_language} into {output_language}, "
        f"using simple language:\n\"{text}\""
    )
    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [prompt]}]
    )
    response = chat_session.send_message(prompt)
    return response.text

# Streamlit interface layout configuration
st.set_page_config(layout="wide")

# Sidebar for selecting between Translation, Blog Generator, or Code Generator
st.sidebar.title("SELECT APPLICATION")
app_mode = st.sidebar.selectbox(
    "Choose Application", 
    ["TRANSLATION GENERATOR 🌍", "BLOG GENERATOR 📝", "CODE GENERATOR 💻"]
)

# Translation Generator Interface
if app_mode == "TRANSLATION GENERATOR 🌍":
    st.title('T R A N S L A T I O N 🌍')
    st.subheader('ENTER TEXT TO TRANSLATE INTO ANOTHER LANGUAGE!')

    # Sidebar for translation input
    st.sidebar.title("TRANSLATION DETAILS")
    st.sidebar.subheader("ENTER DETAILS FOR TRANSLATION")

    input_language = st.sidebar.text_input("INPUT LANGUAGE")
    output_language = st.sidebar.text_input("OUTPUT LANGUAGE")
    text_to_translate = st.sidebar.text_area("TEXT TO TRANSLATE")
    
    translate_button = st.sidebar.button("TRANSLATE 🌍")

    # If the user presses the button to translate
    if translate_button:
        if input_language and output_language and text_to_translate:
            with st.spinner("Translating...!"):
                translation = translate_text(input_language, output_language, text_to_translate)
                st.write(translation)
        else:
            st.error("Please provide input language, output language, and text to translate.")

# Blog Generator Interface
elif app_mode == "BLOG GENERATOR 📝":
    st.title('B L O G 😎')
    st.subheader('ENTER YOUR TOPIC AND GET A BLOG POST GENERATED FOR YOU!')

    # Sidebar for blog post input
    st.sidebar.title("BLOG DETAILS")
    st.sidebar.subheader("ENTER DETAILS FOR BLOG GENERATION")

    blog_title = st.sidebar.text_input("BLOG TITLE")
    keywords = st.sidebar.text_area("KEYWORDS (comma-separated)")
    num_words = st.sidebar.slider("NO.OF WORDS", min_value=1000, max_value=100000, step=1000)
    
    generate_blog_button = st.sidebar.button("GENERATE BLOG POST 📝")

    # If the user presses the button to generate blog
    if generate_blog_button:
        if blog_title and keywords:
            with st.spinner("Generating blog post...!"):
                blog_content = generate_blog_post(blog_title, keywords, num_words)
                st.write(blog_content)
        else:
            st.error("Please provide both a blog title and keywords.")

# Code Generator Interface
elif app_mode == "CODE GENERATOR 💻":
    st.title('C O D E 🤖')
    st.subheader('ENTER YOUR PROBLEM STATEMENT AND GET CODE GENERATED!')

    # Sidebar for code input
    st.sidebar.title("CODE DETAILS")
    st.sidebar.subheader("ENTER CONTEXT FOR CODE GENERATION")

    problem_statement = st.sidebar.text_area("PROBLEM STATEMENT")
    programming_language = st.sidebar.text_input("PROGRAMMING LANGUAGE")
    
    # Select between Static or Dynamic programming
    programming_type = st.sidebar.selectbox("PROGRAMMING TYPE", ["STATIC", "DYNAMIC"])
    
    generate_code_button = st.sidebar.button("GENERATE CODE 💻!")

    # If the user presses the button to generate code
    if generate_code_button:
        if problem_statement and programming_language and programming_type:
            with st.spinner("Generating code...!"):
                generated_code = generate_code(problem_statement, programming_language, programming_type)
                st.code(generated_code)
        else:
            st.error("Please provide a problem statement, programming language, and choose a programming type.")
