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

# Load external CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Set page configuration and load external CSS
st.set_page_config(layout="wide", page_title="Code Generator")
load_css("styles.css")

# Add a background image or header image
st.image('https://example.com/header_image.jpg', use_column_width=True)

# Title of the app with custom style
st.markdown("<h1> CODE GENERATOR 😜🤖</h1>", unsafe_allow_html=True)
st.subheader('ENTER YOUR PROBLEM STATEMENT AND CHOOSE OPTIONS TO GENERATE CODE!')

# Sidebar for user input with customized title and styling
with st.sidebar:
    st.image('https://example.com/sidebar_image.jpg', use_column_width=True)  # Add an image to the sidebar
    st.title("💡 INPUT YOUR CODE DETAILS")
    st.subheader("📝 ENTER DETAILS FOR CODE GENERATION")

    # Customized input fields
    problem_statement = st.text_input("PROBLEM STATEMENT👀")
    programming_language = st.text_input("PROGRAMMING LANGUAGE👨🏻‍🍳")
    
    # Dropdown selection for programming type with styling
    programming_type = st.selectbox(
        "PROGRAMMING TYPE",
        ("STATIC PROGRAMMING😜 ", "DYNAMIC PROGRAMMING🗿")
    )

    # Customized button
    submit_button = st.button("Generate Code 💻")

# If the user presses the button
if submit_button:
    if problem_statement and programming_language and programming_type:
        with st.spinner("🛠️ Generating code..."):
            # Call the generate_code function
            generated_code = generate_code(problem_statement, programming_language, programming_type)
            
            # Display the generated code with a custom layout
            st.markdown("<h3>📝 Generated Code:</h3>", unsafe_allow_html=True)
            st.code(generated_code)
    else:
        st.error("⚠️ Please provide a problem statement, programming language, and choose a programming type.")
