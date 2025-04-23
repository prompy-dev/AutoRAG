#!/usr/bin/env python3
import os
from typing import List, Dict, Any
from openai import OpenAI
from tqdm import tqdm

def embed_chunks(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generate embeddings for text chunks using OpenAI's text-embedding-3-small model.
    
    Args:
        chunks: List of chunk dictionaries with text and metadata
        
    Returns:
        List of chunks with added embedding vectors
    """
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Process each chunk
    embedded_chunks = []
    for chunk in tqdm(chunks, desc="Embedding chunks"):
        try:
            # Generate embedding for chunk
            response = client.embeddings.create(
                input=chunk["text"],
                model="text-embedding-3-small"
            )
            
            # Extract the embedding from the response
            embedding = response.data[0].embedding
            
            # Add embedding to chunk
            chunk_with_embedding = {
                **chunk,
                "embedding": embedding
            }
            
            embedded_chunks.append(chunk_with_embedding)
        except Exception as e:
            print(f"Error embedding chunk {chunk['id']}: {e}")
    
    return embedded_chunks 