import re
import spacy
from pdfminer.high_level import extract_text as extract_pdf_text 
from docx import Document
import json

nlp = spacy.load("en_core_web_sm")

# Define a function that reads text from PDF
def extract_text_from_pdf(file_path):
    return extract_pdf_text(file_path)

# Define a function that reads text from DOCX
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to detremine the file type and extract text
def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Kindly upload PDF or DOCX file")
    
# Function to extract name
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
        return None


# Function to extract e-mail
def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'
    match = re.search(email_pattern,text)
    return match.group() if match else None

# Function to extract phone
def extract_phone(text):
    phone_pattern = r'\+?\d[\d\s\-\(\)]{8,}\d'
    match = re.search(phone_pattern, text)
    return match.group() if match else None

# Function to extract skills
def extract_skills(text):
    skills_list = ["python","java","r","sql","machine learning",
                   "deep learning","pandas","numpy",
                   "keras","pytorch","aws sagemaker",
                   "cloud computing","tensor flow"
                  ]
    skills_found = [skill for skill in skills_list if skill in text.lower()]
    return list(set(skills_found))

# Function to extract
def extract_education(text):
    doc = nlp(text)
    education = []
    # Common keywords indicating education section
    education_keywords = ["education", "academic", "university",
                          "college", "degree", "bachelor",
                          "master","phd","mba",
                          "b.sc","btech","mtech"
                         ]
    education_pattern = r'(?i)(bachelor|master|phd|diploma)\s*(?:of|in)?\s*([^\n,]+)'
    
    for sent in doc.sents:
        sent_text = sent.text
        if any(keyword.lower() in sent_text.lower() for keyword in education_keywords):
            match = re.search(education_pattern, sent_text)
            if match:
                degree = match.group(1)
                field = match.group(2).strip()
                # Look for organization (e.g., university) in the same sentence
                org = None
                for ent in sent.ents:
                    if ent.label_ == "ORG":
                        org = ent.text
                        break
                education.append({
                    "degree": degree,
                    "field": field,
                    "institution": org if org else "Unknown"
                })
    return education

# Function to parse resume
def parse_resume(file_path):
    text = extract_text(file_path)
    parsed_data = {"name": extract_name(text),
                   "email": extract_email(text),
                   "phone number": extract_phone(text),
                   "skills set": extract_skills(text),
                   "education": extract_education(text)}
    return parsed_data#json.dumps(parsed_data, indent=2)

#if __name__ == "__main__":
    #file_path = "C:/Users/Sanayak/Desktop/VICTOR ITINAH INIOBONG Resume.docx"
    #print(parse_resume(file_path))