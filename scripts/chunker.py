#!/usr/bin/env python3
import os
from typing import List, Dict, Any
import uuid

def read_file(file_path: str) -> str:
    """
    Read the content of a file.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        The content of the file as a string
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def split_into_chunks(text: str, file_name: str, target_size: int = 750) -> List[Dict[str, Any]]:
    """
    Split a text into chunks of approximately target_size characters.
    
    Args:
        text: The text to split
        file_name: Original file name for metadata
        target_size: Target size for each chunk in characters (default 750)
        
    Returns:
        List of dictionaries containing chunk text and metadata
    """
    # For simple chunking, we'll split by paragraphs first, then combine
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If paragraph itself is very long, split it further
        if len(paragraph) > target_size * 1.5:
            # Split long paragraph into sentences
            sentences = paragraph.replace('. ', '.\n').split('\n')
            for sentence in sentences:
                if len(current_chunk) + len(sentence) > target_size and current_chunk:
                    chunks.append({
                        "id": str(uuid.uuid4()),
                        "text": current_chunk.strip(),
                        "metadata": {
                            "source": file_name
                        }
                    })
                    current_chunk = sentence
                else:
                    if current_chunk:
                        current_chunk += " " + sentence
                    else:
                        current_chunk = sentence
        # Normal paragraph handling
        elif len(current_chunk) + len(paragraph) > target_size and current_chunk:
            chunks.append({
                "id": str(uuid.uuid4()),
                "text": current_chunk.strip(),
                "metadata": {
                    "source": file_name
                }
            })
            current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append({
            "id": str(uuid.uuid4()),
            "text": current_chunk.strip(),
            "metadata": {
                "source": file_name
            }
        })
    
    return chunks

def chunk_documents(directory: str) -> List[Dict[str, Any]]:
    """
    Process all .txt, .md, and .mdx files in a directory and chunk them.
    
    Args:
        directory: Path to the directory containing documents
        
    Returns:
        List of dictionaries containing chunks with their metadata
    """
    all_chunks = []
    
    for filename in os.listdir(directory):
        if filename.endswith(('.txt', '.md', '.mdx', '.markdown')):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}...")
            
            text = read_file(file_path)
            file_chunks = split_into_chunks(text, filename)
            
            all_chunks.extend(file_chunks)
            print(f"  Created {len(file_chunks)} chunks from {filename}")
    
    return all_chunks 