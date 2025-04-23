#!/usr/bin/env python3
import os
import json
from dotenv import load_dotenv
from scripts.chunker import chunk_documents
from scripts.embedder import embed_chunks
from scripts.uploader import upload_to_pinecone

def main():
    """
    Main function to orchestrate the document processing pipeline:
    1. Load documents from data/raw
    2. Chunk the documents
    3. Generate embeddings for chunks
    4. Save embeddings to disk
    5. Upload embeddings to Pinecone
    """
    # Load environment variables
    load_dotenv()
    
    # Define paths
    raw_data_dir = "data/raw"
    processed_data_path = "data/processed/embedded.json"
    
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    
    # Step 1 & 2: Read and chunk documents
    print("Chunking documents...")
    chunks = chunk_documents(raw_data_dir)
    print(f"Created {len(chunks)} chunks")
    
    # Step 3: Generate embeddings
    print("Generating embeddings...")
    embedded_chunks = embed_chunks(chunks)
    
    # Step 4: Save embeddings to disk
    print(f"Saving embeddings to {processed_data_path}...")
    with open(processed_data_path, 'w') as f:
        json.dump(embedded_chunks, f)
    
    # Step 5: Upload to Pinecone
    print("Uploading to Pinecone...")
    upload_to_pinecone(embedded_chunks)
    
    print("Process completed successfully!")

if __name__ == "__main__":
    main() 