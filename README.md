# CatFactsRAG

A simple Retrieval-Augmented Generation (RAG) project that answers questions about cats using a local facts database and LLMs via [Ollama](https://ollama.com/).

## Features

- Loads cat facts from `facts.txt`
- Embeds facts and queries using a selected embedding model
- Retrieves the most relevant facts for a user question
- Uses a language model to answer questions based only on retrieved facts

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) installed and running
- See `requirements.txt` for Python dependencies

## Usage

1. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
2. Run the app:
    ```sh
    python main.py
    ```
3. Enter your question about cats when prompted.

## How it works

- Loads facts from `facts.txt`
- Embeds each fact and stores in memory
- When you ask a question, embeds the query and retrieves the top relevant facts
- Passes the facts and your question to the language model for an answer

## Configuration

- Change embedding or language models by editing `main.py`:
    - `EMBEDDING_MODEL`
    - `LANGUAGE_MODEL`

## File Structure

- `main.py` — main application logic
- `facts.txt` — database of cat facts
- `requirements.txt` — Python dependencies
- `README.md` — project documentation

## Example

```
Ask a question about cats...
> How fast can a cat run?
```