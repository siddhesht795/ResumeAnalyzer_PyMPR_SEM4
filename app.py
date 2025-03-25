import streamlit as st
import base64
import os
import io
import re
import fitz  # PyMuPDF
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Functions
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file content once and store it
        file_bytes = uploaded_file.read()
        
        # Create image for display
        with fitz.open(stream=file_bytes, filetype="pdf") as pdf_doc:
            first_page = pdf_doc[0].get_pixmap()
            img_byte_arr = io.BytesIO(first_page.tobytes("jpeg"))
            image = Image.open(img_byte_arr)
        
        # Return both the image and the raw bytes for text extraction
        return image, file_bytes
    else:
        raise FileNotFoundError("No file uploaded")

def extract_text_from_pdf(pdf_bytes):
    """Algorithm to extract text from PDF using PyMuPDF"""
    text = ""
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def preprocess_text(text):
    """Text processing algorithm for normalization"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)     # Remove extra whitespace
    return text

def calculate_keyword_match(job_desc, resume_text):
    """Keyword matching algorithm with TF-IDF inspired scoring"""
    job_desc = preprocess_text(job_desc)
    resume_text = preprocess_text(resume_text)
    
    job_words = set(job_desc.split())
    resume_words = set(resume_text.split())
    
    # Calculate Jaccard similarity
    intersection = job_words.intersection(resume_words)
    union = job_words.union(resume_words)
    
    if not union:
        return 0
    
    similarity = len(intersection) / len(union)
    return round(similarity * 100, 2)

def extract_match_percentage(response_text):
    match = re.search(r"Match Percentage:\s*(\d+)%", response_text)
    if match:
        return int(match.group(1))
    else:
        return 0

def enhanced_match_percentage(response_text, job_desc, resume_text):
    """Hybrid scoring algorithm combining AI and keyword analysis"""
    # Extract percentage from Gemini response
    ai_match = extract_match_percentage(response_text)
    
    # Calculate keyword match
    keyword_match = calculate_keyword_match(job_desc, resume_text)
    
    # Weighted average (70% AI analysis, 30% keyword matching)
    weighted_score = 0.7 * ai_match + 0.3 * keyword_match
    return min(100, int(weighted_score))  # Cap at 100%

# Streamlit Configuration
st.set_page_config(page_title="Resume Analyzer")

# Page Styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f5f5;
    }
    h1 {
        color: #2c3e50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>Technical Resume Expert</h1>", unsafe_allow_html=True)

# Inputs
input_text = st.text_area("Job Description: ", key="input", height=200)
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully!")

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    submit1 = st.button("Analyse Resume")
with col2:
    submit2 = st.button("Improvement Suggestions")
with col3:
    submit3 = st.button("Match Percentage")

# Prompts
input_prompt1 = """
As a Technical HR Manager, evaluate this resume against the job description:
1. Identify matching skills and qualifications
2. Highlight strengths and weaknesses
3. Provide overall suitability assessment
"""

input_prompt2 = """
As a Career Advisor, provide specific recommendations:
1. Identify skill gaps
2. Suggest learning resources
3. Recommend improvement strategies
"""

input_prompt3 = """
As an ATS Scanner, provide:
1. Match percentage (bold)
2. Missing keywords (bold)
3. Final assessment (bold)
Format with clear headings.
"""

# Actions
if submit1:
    if uploaded_file is not None:
        try:
            pdf_image, pdf_bytes = input_pdf_setup(uploaded_file)
            pdf_base64 = base64.b64encode(pdf_bytes).decode()
            response = get_gemini_response(input_text, [{"mime_type": "application/pdf", "data": pdf_base64}], input_prompt1)
            
            st.subheader("Resume Analysis")
            st.image(pdf_image, caption="Resume Preview", width=300)
            st.write(response)
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
    else:
        st.warning("Please upload your resume first!")

elif submit2:
    if uploaded_file is not None:
        try:
            pdf_image, pdf_bytes = input_pdf_setup(uploaded_file)
            pdf_base64 = base64.b64encode(pdf_bytes).decode()
            response = get_gemini_response(input_text, [{"mime_type": "application/pdf", "data": pdf_base64}], input_prompt2)
            
            st.subheader("Improvement Suggestions")
            st.write(response)
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
    else:
        st.warning("Please upload your resume first!")

elif submit3:
    if uploaded_file is not None:
        try:
            pdf_image, pdf_bytes = input_pdf_setup(uploaded_file)
            pdf_base64 = base64.b64encode(pdf_bytes).decode()
            response = get_gemini_response(input_text, [{"mime_type": "application/pdf", "data": pdf_base64}], input_prompt3)
            
            resume_text = extract_text_from_pdf(pdf_bytes)
            match_percentage = enhanced_match_percentage(response, input_text, resume_text)
            
            st.subheader("Analysis Results")
            st.image(pdf_image, caption="Resume Preview", width=300)
            
            
            st.write(response)
                
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
    else:
        st.warning("Please upload your resume first!")