# Prompt Engineering RAG System

A Python application for building a vector database in Pinecone from instructional documents on prompt engineering. This system processes documents, generates embeddings using OpenAI, and stores them in Pinecone for retrieval.

## Features

- Processes `.txt`, `.md`, `.mdx`, and `.markdown` files from a data directory
- Chunks documents into ~1000-character segments
- Generates embeddings using OpenAI's `text-embedding-3-small` model
- Stores embeddings in a Pinecone vector database
- Saves processed data to a local JSON file

## Setup

### Prerequisites

- Python 3.7+
- OpenAI API key
- Pinecone API key

### Installation

1. Clone this repository:

   ```
   git clone [repository-url]
   cd prompt-feedback-rag
   ```

2. Create a virtual environment and activate it:

   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:

   ```
   cp .env.example .env
   ```

5. Add your API keys to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

### Prepare Data

Place your prompt engineering documents in the `data/raw/` directory. The system supports `.txt`, `.md`, `.mdx`, and `.markdown` files.

## Usage

Run the main script to process documents and create the vector database:

```
python3 main.py
```

### Fetching Documents from GitHub

You can automatically fetch markdown files from a GitHub repository:

```
python3 main.py --github owner/repo-name
```

If the repository is private, you'll need a GitHub personal access token:

```
python3 main.py --github owner/repo-name --token your_github_token
```

To use previously fetched files without downloading again:

```
python3 main.py --github owner/repo-name --skip-fetch
```

### Processing Pipeline

The script will:

1. (Optional) Fetch markdown documents from GitHub if requested
2. Read documents from `data/raw/`
3. Chunk the documents into ~1000-character segments
4. Generate embeddings for each chunk
5. Save the embeddings to `data/processed/embedded.json`
6. Initialize a Pinecone index (name: `prompt-feedback`)
7. Upload the embedded chunks to Pinecone

## Project Structure

```
prompt-feedback-rag/
├── data/
│   ├── raw/            # Place your documents here
│   └── processed/      # Output directory for processed data
├── scripts/
│   ├── __init__.py     # Package initialization
│   ├── chunker.py      # Functions for chunking documents
│   ├── embedder.py     # Functions for generating embeddings
│   └── uploader.py     # Functions for uploading to Pinecone
├── .env                # Environment variables (create from .env.example)
├── .env.example        # Example environment file
├── main.py             # Main script
├── README.md           # This file
└── requirements.txt    # Project dependencies
```

## Modules

- **Chunker**: Splits documents into chunks of approximately 1000 characters
- **Embedder**: Generates embeddings for text chunks using OpenAI
- **Uploader**: Manages Pinecone database initialization and uploads

## License

[Specify the license here]
