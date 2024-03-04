import streamlit as st
import spacy
import pinecone

# Load English tokenizer, tagger, parser, NER, and word vectors
nlp = spacy.load("en_core_web_sm")

# Initialize Pinecone client
pinecone.init(api_key="your_pinecone_api_key")
index = pinecone.Index("your_index_name")

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

# Function to search Pinecone DB using embeddings
def search_pinecone(embedding):
    # Search Pinecone DB using the embedding
    results = index.query(queries=[embedding], top_k=10)
    return results

# Streamlit app
def main():
    st.title("Resume Matcher")
    st.write("Upload a PDF resume to extract summary and skills.")
    
    # File upload
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Read PDF file
        resume_text = ""  # Placeholder for resume text
        with st.spinner("Extracting text from PDF..."):
            # Use PyPDF2 or similar library to extract text from PDF
            # Replace this with your actual code for extracting text from PDF
            resume_text = "Text extracted from PDF resume"
        
        # Extract summary and skills
        with st.spinner("Extracting summary and skills..."):
            summary, skills = extract_summary_and_skills(resume_text)
        
        # Display summary and skills
        st.write("Summary:")
        st.write(summary)
        st.write("Skills:")
        st.write(skills)
        
        # Convert summary and skills to embeddings
        with st.spinner("Converting text to embeddings..."):
            summary_embedding = text_to_embedding(summary)
            skills_embedding = text_to_embedding(skills)
        
        # Search Pinecone DB using embeddings
        with st.spinner("Searching Pinecone DB..."):
            summary_results = search_pinecone(summary_embedding)
            skills_results = search_pinecone(skills_embedding)
        
        # Display search results
        st.write("Summary Search Results:")
        st.write(summary_results)
        st.write("Skills Search Results:")
        st.write(skills_results)

if __name__ == "__main__":
    main()
