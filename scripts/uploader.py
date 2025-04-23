#!/usr/bin/env python3
import os
from typing import List, Dict, Any
import pinecone
from tqdm import tqdm

def initialize_pinecone():
    """
    Initialize the Pinecone client and create the index if it doesn't exist.
    
    Returns:
        Pinecone index object
    """
    # Get API key from environment variables
    api_key = os.getenv("PINECONE_API_KEY")
    
    if not api_key:
        raise ValueError("PINECONE_API_KEY must be set")
    
    # Initialize Pinecone (newer versions only need API key)
    pinecone.init(api_key=api_key)
    
    # Index parameters
    index_name = "prompt-feedback"
    dimension = 1536  # Dimension for text-embedding-3-small
    metric = "cosine"
    
    # Check if our index already exists
    if index_name not in pinecone.list_indexes():
        print(f"Creating Pinecone index '{index_name}'...")
        pinecone.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric
        )
    
    # Connect to the index
    index = pinecone.Index(index_name)
    return index

def upload_to_pinecone(embedded_chunks: List[Dict[str, Any]]):
    """
    Upload embedded chunks to Pinecone.
    
    Args:
        embedded_chunks: List of chunks with embeddings
    """
    # Initialize Pinecone
    index = initialize_pinecone()
    
    # Prepare vectors for upsert
    vectors = []
    batch_size = 100  # Recommended batch size
    
    for chunk in embedded_chunks:
        vectors.append({
            "id": chunk["id"],
            "values": chunk["embedding"],
            "metadata": {
                "text": chunk["text"],
                "source": chunk["metadata"]["source"]
            }
        })
        
        # If we've reached the batch size, upsert and reset
        if len(vectors) >= batch_size:
            index.upsert(vectors=vectors)
            vectors = []
    
    # Upsert any remaining vectors
    if vectors:
        index.upsert(vectors=vectors)
    
    print(f"Successfully uploaded {len(embedded_chunks)} vectors to Pinecone") 