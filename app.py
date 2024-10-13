
import streamlit as st
import pinecone
import cohere
from sentence_transformers import SentenceTransformer

# Correct initialization for Pinecone
api_key = '87a3914b-75ee-4c0c-b4cf-b294158e0747'
pinecone_client = pinecone.Pinecone(api_key=api_key)

index_name = "qa-bot-index"
index = pinecone_client.Index(index_name)

# SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Cohere
co = cohere.Client('omTyaHvoeFTz8JelXtrfXxdal0FFkvMVK4UDAKff')

st.title("Interactive Clean Energy QA Bot")

# Function to query Pinecone
def query_pinecone(question):
    query_embedding = model.encode(question).tolist()  # Convert to list
    result = index.query(vector=query_embedding, top_k=1, include_metadata=True)
    best_match_paragraph = result['matches'][0]['metadata']['text']
    return best_match_paragraph

# Function to generate an answer using Cohere
def generate_answer(question, context):
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    response = co.generate(model='command-xlarge-nightly', prompt=prompt, max_tokens=150)
    return response.generations[0].text.strip()

# Streamlit user interaction
user_question = st.text_input("Ask a question about clean energy:")

if user_question:
    st.write("You asked:", user_question)

    # Retrieve relevant paragraph
    retrieved_paragraph = query_pinecone(user_question)
    st.write("Retrieved Paragraph:", retrieved_paragraph)

    # Generate detailed answer
    generated_answer = generate_answer(user_question, retrieved_paragraph)
    st.write("Generated Answer:", generated_answer)
    