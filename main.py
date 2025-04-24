#!/usr/bin/env python3
import os
import json
import argparse
from dotenv import load_dotenv
from scripts.chunker import chunk_documents
from scripts.embedder import embed_chunks
from scripts.uploader import upload_to_pinecone
from scripts.github_fetcher import fetch_github_markdown

def main():
    """
    Main function to orchestrate the document processing pipeline:
    1. Load documents from data/raw
    2. Chunk the documents
    3. Generate embeddings for chunks
    4. Save embeddings to disk
    5. Upload embeddings to Pinecone
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process documents and create vector database")
    parser.add_argument("--github", help="GitHub repository in format owner/name to fetch markdown files")
    parser.add_argument("--token", help="GitHub personal access token (optional)")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip fetching files from GitHub")
    parser.add_argument("--index-name", default="prompt-feedback", help="Name of the Pinecone index (default: prompt-feedback)")
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Define paths
    raw_data_dir = "data/raw"
    processed_data_path = "data/processed/embedded.json"
    
    # Make sure the output directories exist
    os.makedirs(os.path.dirname(processed_data_path), exist_ok=True)
    os.makedirs(raw_data_dir, exist_ok=True)
    
    # Step 0 (Optional): Fetch files from GitHub if requested
    if args.github and not args.skip_fetch:
        print(f"Fetching markdown files from GitHub repository: {args.github}")
        repo_parts = args.github.split("/")
        if len(repo_parts) != 2:
            print("Repository must be in format owner/name")
            return
        
        repo_owner, repo_name = repo_parts
        fetch_github_markdown(repo_owner, repo_name, raw_data_dir, args.token)
    
    # Step 1 & 2: Read and chunk documents
    print("Chunking documents...")
    chunks = chunk_documents(raw_data_dir)
    print(f"Created {len(chunks)} chunks")
    
    # Step 3: Generate embeddings
    print("Generating embeddings...")
    try:
        embedded_chunks = embed_chunks(chunks)
        print(f"Successfully embedded {len(embedded_chunks)} chunks")
        
        # Step 4: Save embeddings to disk
        print(f"Saving embeddings to {processed_data_path}...")
        with open(processed_data_path, 'w') as f:
            json.dump(embedded_chunks, f)
        
        # Step 5: Upload to Pinecone
        if embedded_chunks:
            print(f"Uploading to Pinecone index '{args.index_name}'...")
            upload_to_pinecone(embedded_chunks, args.index_name)
            print("Process completed successfully!")
        else:
            print("No embedded chunks to upload to Pinecone.")
    except Exception as e:
        print(f"Error during embedding process: {e}")
        print("Process failed.")

if __name__ == "__main__":
    main() 