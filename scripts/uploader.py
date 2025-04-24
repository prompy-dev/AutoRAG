#!/usr/bin/env python3
import os
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from tqdm import tqdm

def initialize_pinecone(index_name: str = "prompt-feedback"):
    """
    Initialize the Pinecone client and create the index if it doesn't exist.
    
    Args:
        index_name: Name of the Pinecone index to use
    
    Returns:
        Pinecone index object
    """
    # Get API key from environment variables
    api_key = os.getenv("PINECONE_API_KEY")
    
    if not api_key:
        raise ValueError("PINECONE_API_KEY must be set")
    
    # Initialize Pinecone with the new API pattern
    pc = Pinecone(api_key=api_key)
    
    # Index parameters
    dimension = 1536  # Dimension for text-embedding-3-small
    metric = "cosine"
    
    # Check if our index already exists
    existing_indexes = [index.name for index in pc.list_indexes()]
    if index_name not in existing_indexes:
        print(f"Creating Pinecone index '{index_name}'...")
        # Create a serverless index with simplified approach
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )          
        )
    
    # Connect to the index
    index = pc.Index(index_name)
    return index

def upload_to_pinecone(embedded_chunks: List[Dict[str, Any]], index_name: str = "prompt-feedback"):
    """
    Upload embedded chunks to Pinecone.
    
    Args:
        embedded_chunks: List of chunks with embeddings
        index_name: Name of the Pinecone index to use
    """
    # Initialize Pinecone
    index = initialize_pinecone(index_name)
    
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