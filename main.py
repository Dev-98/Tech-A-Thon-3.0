import streamlit as st
import spacy
import base64, re
from pyresparser import ResumeParser
from streamlit_tags import st_tags
from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")


# Function to extract summary and skills from resume
def extract_summary_and_skills(text):
    # Process the text using spaCy
    doc = nlp(text)
    
    # Extract summary
    summary = [sent.text for sent in doc.sents if len(sent.text.split()) > 5][:3]  # Extract first 3 sentences
    
    # Extract skills (you might want to customize this based on your requirements)
    skills = [ent.text for ent in doc.ents if ent.label_ == "ORG" or ent.label_ == "PRODUCT"]
    
    return " ".join(summary), ", ".join(skills)

# Function to convert text into embeddings
def text_to_embedding(text):
    # Convert text to embeddings using your preferred method (e.g., BERT, Word2Vec)
    # Replace this with your actual code for converting text to embeddings
    embedding = [0.1] * 100  # Placeholder embedding
    return embedding

def pdf_reader(pdf_file):
    
    text = extract_text(pdf_file).lower()
    # skill = text.split("skills")[1:]
   
    token_text = word_tokenize(text)
    stop_words = stopwords.words('english')
    clean_text = []
    for i in token_text:
        if i not in stop_words:
            clean_text.append(i)
    clean_text = " ".join(clean_text)
    
    pattern = re.compile(r'[^a-zA-Z0-9\s]')
    clean_text = re.sub(pattern, '', clean_text).replace("\n", "")
    
    # Define a regular expression pattern to match numbers
    pattern2 = r'\d+'

    # Remove numbers from the text using regex substitution
    text_without_numbers = re.sub(pattern2, '', clean_text)
    
    return text_without_numbers

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Streamlit app
def main():
    st.title("Resume Matcher")
    st.write("Upload a PDF resume to extract summary and skills.")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Read PDF file
        save_image_path = './Uploaded_Resumes/' + uploaded_file.name
        with open(save_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        show_pdf(save_image_path)
        resume_text = ""  # Placeholder for resume text
        with st.spinner("Extracting text from PDF..."):
        
            resume_data = ResumeParser(uploaded_file).get_extracted_data()
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

                st.header("**Resume Analysis**")
                st.success("Hello " + resume_data['name'])
                st.subheader("**Your Basic info**")
                try:
                    st.text('Name: ' + resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: ' + str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #1ed760;'>You are at intermediate level!</h4>''',
                                unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >= 3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #fba171;'>You are at experience level!''',
                                unsafe_allow_html=True)

                st.subheader("**Skills Recommendation💡**")
                ## Skill shows
                keywords = st_tags(label='### Skills that you have',
                                   text='See our skills recommendation',
                                   value=resume_data['skills'], key='1')
                
                
        
        # Extract summary and skills
        with st.spinner("Extracting summary and skills..."):
            summary, skills = extract_summary_and_skills(resume_text)
        
        # Display summary and skills
        st.write("Summary:")
        st.write(summary)
        st.write("Skills:")
        st.write(skills)
        
        # Convert summary and skills to embeddings
        # with st.spinner("Converting text to embeddings..."):
        #     summary_embedding = text_to_embedding(summary)
        #     skills_embedding = text_to_embedding(skills)
        
        # # Search Pinecone DB using embeddings
        # # with st.spinner("Searching Pinecone DB..."):
        # #     summary_results = search_pinecone(summary_embedding)
        # #     skills_results = search_pinecone(skills_embedding)
        
        # # Display search results
        # st.write("Summary Search Results:")
        # st.write(summary_results)
        # st.write("Skills Search Results:")
        # st.write(skills_results)

if __name__ == "__main__":
    main()
