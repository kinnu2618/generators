import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
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

# Function to generate caption and hashtags based on the image description
def generate_caption_and_hashtags(image_description, language):
    prompt = (
        f"Write a caption for the image in {language}. Generate 5 hashtags for the image in a line in {language}:\n"
        f"\"{image_description}\""
    )
    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [prompt]}]
    )
    response = chat_session.send_message(prompt)
    return response.text

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

# Function for AI question-answering
def ask_ai_question(user_input):
    if not user_input.strip():
        raise ValueError("Question cannot be empty. Please enter a question.")
    
    prompt = f"give me the big paragrapic answer for whatever is asked\nquestion = {user_input}"
    
    chat_session = model.start_chat(
        history=[{"role": "user", "parts": [prompt]}]
    )
    
    response = chat_session.send_message(user_input)
    return response.text

# Streamlit interface layout configuration
st.set_page_config(layout="wide")

# Sidebar for selecting application mode
app_mode = st.sidebar.selectbox(
    "Choose Application", 
    ["TRANSLATION GENERATOR 🌍", "BLOG GENERATOR 📝", "CODE GENERATOR 💻", "CAPTION & HASHTAG GENERATOR 📷", "ASK AI 🤖"]
)

# Translation Generator Interface
if app_mode == "TRANSLATION GENERATOR 🌍":
    st.title('T R A N S L A T I O N 🌍')
    st.subheader('ENTER TEXT TO TRANSLATE INTO ANOTHER LANGUAGE!')

    input_language = st.sidebar.text_input("Input Language")
    output_language = st.sidebar.text_input("Output Language")
    text_to_translate = st.sidebar.text_area("Text to Translate")
    
    translate_button = st.sidebar.button("TRANSLATE 🌍")

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

    blog_title = st.sidebar.text_input("BLOG TITLE")
    keywords = st.sidebar.text_area("KEYWORDS (comma-separated)")
    num_words = st.sidebar.slider("NO. OF WORDS", min_value=1000, max_value=100000, step=1000)
    
    generate_blog_button = st.sidebar.button("GENERATE BLOG POST 📝")

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

    problem_statement = st.sidebar.text_area("PROBLEM STATEMENT")
    programming_language = st.sidebar.text_input("PROGRAMMING LANGUAGE")
    programming_type = st.sidebar.selectbox("PROGRAMMING TYPE", ["STATIC", "DYNAMIC"])
    
    generate_code_button = st.sidebar.button("GENERATE CODE 💻!")

    if generate_code_button:
        if problem_statement and programming_language and programming_type:
            with st.spinner("Generating code...!"):
                generated_code = generate_code(problem_statement, programming_language, programming_type)
                st.code(generated_code)
        else:
            st.error("Please provide a problem statement, programming language, and choose a programming type.")

# Caption and Hashtag Generator Interface with Image Upload
elif app_mode == "CAPTION & HASHTAG GENERATOR 📷":
    st.title('C A P T I O N  &  H A S H T A G S 📷')
    st.subheader('UPLOAD AN IMAGE AND GENERATE CAPTION AND HASHTAGS!')

    uploaded_image = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    caption_language = st.sidebar.text_input("Language")
    image_description = st.sidebar.text_area("Image Description")

    generate_caption_button = st.sidebar.button("GENERATE CAPTION & HASHTAGS 📷")

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
    
    if generate_caption_button:
        if uploaded_image and caption_language:
            if not image_description:
                st.warning("No image description provided. Please add one for better results.")
            with st.spinner("Generating caption and hashtags...!"):
                if image_description:
                    caption_and_hashtags = generate_caption_and_hashtags(image_description, caption_language)
                    st.write(caption_and_hashtags)
                else:
                    st.error("Please provide an image description.")
        else:
            st.error("Please upload an image and provide the language for caption and hashtags.")

# AI Question Answering Interface
elif app_mode == "ASK AI 🤖":
    st.title("ASK AI 🤖")
    st.subheader("Enter your question and get an AI-generated answer!")

    user_input = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        try:
            with st.spinner("Generating answer...!"):
                answer = ask_ai_question(user_input)
                st.subheader("Answer:")
                st.write(answer)
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
