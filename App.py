import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Streamlit Page Config
st.set_page_config(page_title="Tamil Dialect Translator", page_icon="", layout="centered")

st.markdown("""
    <style>
        body, .main {
            background-color: #000000;
            color: #ffffff;
        }
        label, .stTextInput label, .stSelectbox label, .stMarkdown {
            color: #ffffff !important;
            font-weight: bold;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {
            font-size: 16px;
            padding: 10px;
            background-color: #1e1e1e;
            color: #ffffff;
            border-radius: 6px;
            border: none;
        }
        .stButton>button {
            background-color: #444444;
            color: white;
            padding: 0.5em 2em;
            border-radius: 8px;
            font-size: 18px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #666666;
        }
        .translated-text-box {
            background-color: #1f1f1f;
            padding: 10px;
            border-radius: 10px;
            font-size: 18px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)




st.markdown("<h1 style='color:white; text-align:center;'>English ➡️ Tamil Dialect Translator</h1>", unsafe_allow_html=True)


user_api_key = st.text_input("Enter a Gemini API Key:", type="password")

text = st.text_input("Enter an English Sentence:")

dialect = st.selectbox(
    "Select Tamil Dialect:",
    options=["Chennai", "Kanyakumari", "Coimbatore"]
)


# Prompt template
prompt = PromptTemplate(
    input_variables=["dialect", "text"],
    template="""
You are a Tamil dialect translator. Translate the following English sentence into Tamil in the {dialect} dialect.

Only output the translated sentence. Do not provide any explanation or additional text.

English: {text}
"""
)

# Translate Button
if st.button("Translate"):
    if not user_api_key:
        st.error("Please enter your Gemini API key.")
    elif text and dialect:
        try:
            with st.spinner("Translating..."):
                # Initialize the LLM with user's API key
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    temperature=0.7,
                    google_api_key=user_api_key
                )
                # Chain using pipe syntax
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
