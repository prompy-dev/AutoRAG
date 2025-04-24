#!/usr/bin/env python3
import os
import subprocess
import shutil
import glob
from typing import List

def clone_github_repo(repo_owner: str, repo_name: str, output_dir: str, token: str = None) -> str:
    """
    Clone a GitHub repository to a local directory.
    
    Args:
        repo_owner: Owner of the repository
        repo_name: Name of the repository
        output_dir: Directory to save the repository
        token: GitHub personal access token (optional)
        
    Returns:
        Path to the cloned repository
    """
    # Create temp directory for the clone
    temp_clone_dir = os.path.join(output_dir, "_temp_clone")
    
    # Remove existing temp directory if it exists
    if os.path.exists(temp_clone_dir):
        shutil.rmtree(temp_clone_dir)
    
    # Create the temp directory
    os.makedirs(temp_clone_dir, exist_ok=True)
    
    # Construct the git clone URL with token if provided
    if token:
        clone_url = f"https://{token}@github.com/{repo_owner}/{repo_name}.git"
    else:
        clone_url = f"https://github.com/{repo_owner}/{repo_name}.git"
    
    # Clone the repository
    print(f"Cloning repository {repo_owner}/{repo_name}...")
    subprocess.run(["git", "clone", clone_url, temp_clone_dir], check=True)
    
    return temp_clone_dir

def find_markdown_files(directory: str) -> List[str]:
    """
    Find all markdown files in a directory recursively.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of paths to markdown files
    """
    # Use glob to find all .md, .mdx, and .markdown files
    md_files = glob.glob(f"{directory}/**/*.md", recursive=True)
    mdx_files = glob.glob(f"{directory}/**/*.mdx", recursive=True)
    markdown_files = glob.glob(f"{directory}/**/*.markdown", recursive=True)
    
    return md_files + mdx_files + markdown_files

def copy_markdown_files(source_dir: str, target_dir: str):
    """
    Copy all markdown files from source directory to target directory.
    
    Args:
        source_dir: Source directory containing markdown files
        target_dir: Target directory to copy files to
    """
    # Make sure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Find all markdown files
    markdown_files = find_markdown_files(source_dir)
    
    print(f"Found {len(markdown_files)} markdown files")
    
    # Copy each file to the target directory with a new name
    for file_path in markdown_files:
        # Get relative path from the source directory
        rel_path = os.path.relpath(file_path, source_dir)
        
        # Create sanitized filename (replace path separators with underscores)
        sanitized_name = rel_path.replace(os.path.sep, "_")
        
        # Full path in target directory
        target_path = os.path.join(target_dir, sanitized_name)
        
        # Copy the file
        print(f"Copying {rel_path} to {target_path}")
        shutil.copy2(file_path, target_path)

def fetch_github_markdown(repo_owner: str, repo_name: str, output_dir: str, token: str = None):
    """
    Fetch all markdown files from a GitHub repository by cloning it.
    
    Args:
        repo_owner: Owner of the repository
        repo_name: Name of the repository
        output_dir: Directory to save the markdown files
        token: GitHub personal access token (optional)
    """
    try:
        # Clone the repository
        clone_dir = clone_github_repo(repo_owner, repo_name, output_dir, token)
        
        # Copy markdown files to output directory
        copy_markdown_files(clone_dir, output_dir)
        
        # Remove the cloned repository
        print(f"Cleaning up temporary clone directory...")
        shutil.rmtree(clone_dir)
        
        print(f"Successfully fetched markdown files from {repo_owner}/{repo_name}")
    
    except Exception as e:
        print(f"Error fetching repository: {e}")
    
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Download markdown files from a GitHub repository")
    parser.add_argument("repo", help="Repository in format owner/name")
    parser.add_argument("--output", "-o", default="data/raw", help="Output directory")
    parser.add_argument("--token", "-t", help="GitHub personal access token")
    
    args = parser.parse_args()
    
    repo_parts = args.repo.split("/")
    if len(repo_parts) != 2:
        print("Repository must be in format owner/name")
        exit(1)
    
    repo_owner, repo_name = repo_parts
    
    fetch_github_markdown(repo_owner, repo_name, args.output, args.token)
    print(f"Downloaded markdown files from {args.repo} to {args.output}") 