
import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI

st.set_page_config(page_title="Creative Writing Assessment", layout="centered")

st.title("📝 Creative Writing Assessment Tool")
st.write("Upload a short creative writing sample (PDF). The system will evaluate it using the Nova Scotia writing rubric.")

openai_api_key = st.text_input("🔑 Enter your OpenAI API Key:", type="password")

uploaded_file = st.file_uploader("📄 Upload your PDF", type=["pdf"])

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def analyze_text(text, api_key):
    client = OpenAI(api_key=api_key)

    rubric_prompt = f'''
You are an expert writing evaluator using the Nova Scotia Analytic Writing Rubric. 
Evaluate the following short creative writing sample and assign a score (1–4) with an explanation for each of the 4 rubric categories:

1. Ideas
2. Organization
3. Language Use
4. Conventions

Format your response clearly like this:

Ideas: Score - Explanation  
Organization: Score - Explanation  
Language Use: Score - Explanation  
Conventions: Score - Explanation

Text:
{text}
'''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": rubric_prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

if uploaded_file and openai_api_key:
    st.info("Processing your writing... please wait ⏳")
    extracted_text = extract_text_from_pdf(uploaded_file)
    result = analyze_text(extracted_text, openai_api_key)
    st.subheader("📊 Assessment Result")
    st.text(result)
