#!/usr/bin/env python3
import os
from typing import List, Dict, Any
from openai import OpenAI
from tqdm import tqdm

def truncate_text(text: str, max_tokens: int = 8000) -> str:
    """
    Truncate text to ensure it doesn't exceed the maximum token limit.
    This is a simple approximation - roughly 4 chars per token for English text.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens allowed
        
    Returns:
        Truncated text
    """
    # Simple approximation: ~4 chars per token for English
    char_limit = max_tokens * 4
    
    if len(text) > char_limit:
        print(f"Warning: Truncating text from {len(text)} chars to ~{char_limit} chars")
        return text[:char_limit]
    
    return text

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
    failures = 0
    max_tokens = 8000  # text-embedding-3-small has a limit of 8191 tokens
    
    for chunk in tqdm(chunks, desc="Embedding chunks"):
        try:
            # Ensure text doesn't exceed token limit
            truncated_text = truncate_text(chunk["text"], max_tokens)
            
            # Generate embedding for chunk
            response = client.embeddings.create(
                input=truncated_text,
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
            failures += 1
            print(f"Error embedding chunk {chunk['id']}: {e}")
            print(f"Chunk length: {len(chunk['text'])} characters")
            
            # Try again with a more aggressive truncation if this looks like a token limit issue
            if "token" in str(e).lower() or "limit" in str(e).lower():
                try:
                    # Try again with half the text
                    half_length = len(chunk["text"]) // 2
                    truncated_text = chunk["text"][:half_length]
                    
                    print(f"Retrying with {len(truncated_text)} characters...")
                    
                    response = client.embeddings.create(
                        input=truncated_text,
                        model="text-embedding-3-small"
                    )
                    
                    embedding = response.data[0].embedding
                    
                    chunk_with_embedding = {
                        **chunk,
                        "embedding": embedding,
                        "text": truncated_text,  # Replace with truncated text
                        "truncated": True  # Flag that this was truncated
                    }
                    
                    embedded_chunks.append(chunk_with_embedding)
                    print("Retry succeeded with shorter text")
                except Exception as retry_error:
                    print(f"Retry also failed: {retry_error}")
    
    if failures > 0:
        print(f"Warning: {failures} chunks failed to embed out of {len(chunks)} total chunks")
    
    return embedded_chunks 