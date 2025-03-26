# Resume Analyzer AI

A Streamlit-powered application that leverages Google's Gemini AI to perform in-depth resume analysis against job descriptions. Provides actionable insights, improvement suggestions, and hybrid scoring combining AI analysis with keyword matching.

## Features

- **AI-Powered Resume Analysis**: Comprehensive evaluation against job requirements
- **Improvement Suggestions**: Skill gap analysis and career development recommendations
- **Hybrid Match Percentage**: Combines Gemini AI analysis with keyword scoring

## Technologies Used

- **Google Gemini AI** - Core analysis engine
- **Streamlit** - Web application framework
- **PyMuPDF** - PDF text extraction and processing
- **Python-dotenv** - Environment configuration
- **Pillow** - Image processing

## Installation

1. Clone the repository:
```bash
git clone "https://github.com/siddhesht795/ResumeAnalyzer_PyMPR_SEM4.git"
cd ResumeAnalyzer_PyMPR_SEM4
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
GOOGLE_API_KEY=your_api_key_here #Set your API key
```

4. Run the application:
```bash
streamlit run app.py
```
