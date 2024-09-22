import streamlit as st
import google.generativeai as genai
from apikey import google_gemini_api_key  # Replace this with your actual API key import method

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
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Generate a comprehensive, engaging blog post relevant to the given title \"{title}\" and keywords \"{keywords}\". Make sure to incorporate these keywords in the blog post. The blog should be approximately {num_words} words in length, suitable for an online audience. Ensure the content is original, informative, and maintains a consistent tone throughout.",
                ],
            },
        ]
    )
    response = chat_session.send_message("INSERT_INPUT_HERE")
    return response.text

# Function to generate code
def generate_code(problem_statement, programming_language, programming_type):
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Generate a code relevant to the given problem statement \"{problem_statement}\" in programming language \"{programming_language}\". The code should be either \"{programming_type}\" based. Make sure the code is original, informative, and suitable for an online audience.",
                ],
            },
        ]
    )
    response = chat_session.send_message("INSERT_INPUT_HERE")
    return response.text

# Streamlit interface layout configuration
st.set_page_config(layout="wide")

# Sidebar for selecting between Blog Generator or Code Generator
st.sidebar.title("SELECT APPLICATION")
app_mode = st.sidebar.selectbox("Choose Application", ["Blog Generator 📝", "Code Generator 💻"])

# Blog Generator Interface
if app_mode == "Blog Generator":
    st.title('📝 BLOG GENERATOR 😎')
    st.subheader('Enter your topic and get a blog post generated for you!')

    # Sidebar for blog post input
    st.sidebar.title("BLOG DETAILS")
    st.sidebar.subheader("Enter Details for Blog Generation")

    blog_title = st.sidebar.text_input("Blog Title")
    keywords = st.sidebar.text_area("Keywords (comma-separated)")
    num_words = st.sidebar.slider("Number of Words", min_value=1000, max_value=100000, step=100)
    
    generate_blog_button = st.sidebar.button("Generate Blog Post 📝")

    # If the user presses the button to generate blog
    if generate_blog_button:
        if blog_title and keywords:
            with st.spinner("Generating blog post..."):
                blog_content = generate_blog_post(blog_title, keywords, num_words)
                st.write(blog_content)
        else:
            st.error("Please provide both a blog title and keywords.")

# Code Generator Interface
elif app_mode == "Code Generator":
    st.title('💻 CODE GENERATOR 🤖')
    st.subheader('Enter your problem statement and get code generated!')

    # Sidebar for code input
    st.sidebar.title("CODE DETAILS")
    st.sidebar.subheader("Enter Details for Code Generation")

    problem_statement = st.sidebar.text_input("Problem Statement")
    programming_language = st.sidebar.text_input("Programming Language (e.g., Python, Java)")
    
    # Select between Static or Dynamic programming
    programming_type = st.sidebar.selectbox("Programming Type", ["Static", "Dynamic"])
    
    generate_code_button = st.sidebar.button("Generate Code 💻")

    # If the user presses the button to generate code
    if generate_code_button:
        if problem_statement and programming_language and programming_type:
            with st.spinner("Generating code..."):
                generated_code = generate_code(problem_statement, programming_language, programming_type)
                st.code(generated_code)
        else:
            st.error("Please provide a problem statement, programming language, and choose a programming type.")
