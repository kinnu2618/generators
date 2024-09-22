import os
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

# Function to generate code based on the problem statement, language, and type
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

# Function to load the external CSS file
def load_css(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    if os.path.exists(file_path):
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"CSS file not found: {file_name}")

# Set page configuration and load the CSS file
st.set_page_config(layout="wide", page_title="Code Generator")
load_css("styles.css")

# Add an optional header image (replace with your image URL)
st.image('https://i.pinimg.com/474x/7f/08/49/7f08493bc0004396c9eff78102928afc.jpg', use_column_width=True)

# Title and description of the app
st.markdown("<h1>💻 CODE GENERATOR 😜🤖</h1>", unsafe_allow_html=True)
st.subheader('Enter your problem statement and choose options to generate code!')

# Sidebar for user input
with st.sidebar:
    st.image('https://tse1.mm.bing.net/th?id=OIP.l7yfZxejSdQkR89sVHP1CwHaFd&pid=Api&P=0&h=180', use_column_width=True)  # Add an image to the sidebar
    st.title("💡 INPUT YOUR CODE DETAILS")
    st.subheader("📝 ENTER DETAILS FOR CODE GENERATION")

    # Input fields for problem statement, programming language, and programming type
    problem_statement = st.text_input("PROBLEM STATEMENT👀")
    programming_language = st.text_input("PROGRAMMING LANGUAGE👨🏻‍🍳")
    
    # Dropdown selection for programming type
    programming_type = st.selectbox(
        "PROGRAMMING TYPE",
        ("STATIC PROGRAMMING😜", "DYNAMIC PROGRAMMING🗿")
    )

    # Generate code button
    submit_button = st.button("Generate Code 💻")

# If the user presses the button
if submit_button:
    if problem_statement and programming_language and programming_type:
        with st.spinner("🛠️ Generating code..."):
            # Call the generate_code function
            generated_code = generate_code(problem_statement, programming_language, programming_type)
            
            # Display the generated code
            st.markdown("<h3>📝 Generated Code:</h3>", unsafe_allow_html=True)
            st.code(generated_code)
    else:
        st.error("⚠️ Please provide a problem statement, programming language, and choose a programming type.")
