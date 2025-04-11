import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Set page configuration
st.set_page_config(
    page_title="Tamil Dialect Translator", 
    page_icon="🗣️", 
    layout="centered"
)

# Custom CSS to enforce the dark theme and style
custom_css = """
<style>
    /* Ensure full-page background using Streamlit's container class */
    .block-container {
        background-color: #000000;
        color: #ffffff;
    }
    /* Style headings and paragraphs inside markdown */
    h1, h2, h3, p {
        color: #ffffff;
    }
    /* Overriding default label and input colors */
    label, .stTextInput label, .stSelectbox label, .stMarkdown {
        color: #ffffff !important;
        font-weight: bold;
    }
    /* Custom style for text input and select boxes */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {
        font-size: 16px;
        padding: 10px;
        background-color: #1e1e1e;
        color: #ffffff;
        border-radius: 6px;
        border: none;
    }
    /* Button styling */
    .stButton > button {
        background-color: #444444;
        color: white;
        padding: 0.5em 2em;
        border-radius: 8px;
        font-size: 18px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #666666;
    }
    /* Box for translated text */
    .translated-text-box {
        background-color: #1f1f1f;
        padding: 10px;
        border-radius: 10px;
        font-size: 18px;
        color: white;
        margin-top: 1em;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Title for the app
st.markdown("<h1 style='text-align:center;'>English ➡️ Tamil Dialect Translator</h1>", unsafe_allow_html=True)

# Input fields
user_api_key = st.text_input("Enter a Gemini API Key:", type="password")
text = st.text_input("Enter an English Sentence:")
dialect = st.selectbox("Select Tamil Dialect:", options=["Chennai", "Kanyakumari", "Coimbatore"])

# Prompt template for translation
prompt = PromptTemplate(
    input_variables=["dialect", "text"],
    template="""
You are a Tamil dialect translator. Translate the following English sentence into Tamil in the {dialect} dialect.

Only output the translated sentence. Do not provide any explanation or additional text.

English: {text}
"""
)

# Translation processing when button is clicked
if st.button("Translate"):
    if not user_api_key:
        st.error("Please enter your Gemini API key.")
    elif text and dialect:
        try:
            with st.spinner("Translating..."):
                # Initialize the Google Generative AI module using user's API key
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    temperature=0.7,
                    google_api_key=user_api_key
                )
                chain = prompt | llm
                result = chain.invoke({
                    "dialect": dialect,
                    "text": text
                })
            st.success(f"Translated in {dialect} dialect:")
            st.markdown(f"<div class='translated-text-box'>{result.content}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Translation failed: {e}")
    else:
        st.warning("Please fill in both the English sentence and select a dialect.")
