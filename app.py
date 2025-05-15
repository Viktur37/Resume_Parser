import streamlit as st
import os
from resume_parser import parse_resume
import json

# Set the page title for the Streamlit app
st.title("Resume Parser")

# Create a file uploader widget for PDF or DOCX files
uploaded_file = st.file_uploader("Upload a Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    # Save the uploaded file temporarily
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Parse the resume using the parse_resume function from resume_parser.py
        parsed_data = parse_resume(file_path)
        
        # Display a header for the parsed information
        st.header("Parsed Resume Information")
        
        # Display the extracted name
        st.subheader("Name")
        st.write(parsed_data.get("name", "Not found"))
        
        # Display the extracted email
        st.subheader("Email")
        st.write(parsed_data.get("email", "Not found"))
        
        # Display the extracted phone number
        st.subheader("Phone Number")
        st.write(parsed_data.get("phone number", "Not found"))
        
        # Display the extracted skill set
        st.subheader("Skills")
        skills = parsed_data.get("skills set", [])
        if skills:
            st.write(", ".join(skills))
        else:
            st.write("Not found")
        
        # Display the extracted education details
        st.subheader("Education")
        education = parsed_data.get("education", [])
        if education:
            for edu in education:
                st.write(f"- {edu['degree']} in {edu['field']} from {edu['institution']}")
        else:
            st.write("Not found")
        
        # Display raw JSON output
        st.subheader("Raw JSON Output")
        st.json(parsed_data)
        
    except Exception as e:
        # Display an error message if parsing fails
        st.error(f"Error parsing resume: {str(e)}")
    
    finally:
        # Clean up by removing the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

else:
    # Display an info message when no file is uploaded
    st.info("Please upload a PDF or DOCX resume file to parse.")