# Document Loaders

This folder contains practical examples for working with document loaders in LangChain. A document loader is the component that reads data from a source and converts it into documents that can be used by LLM-based applications.

## What is a document loader?

In LangChain, a document loader helps transform raw content into structured documents that can be used in downstream AI workflows. Each loaded document typically contains:

- the document text content
- metadata such as source, title, and file type
- a format that can be passed into prompts, chains, or vector stores

Document loaders are essential when building applications that need to work with:

- PDFs and text files
- website content
- folders of documents
- custom knowledge bases for retrieval and question answering

## What this folder demonstrates

This folder includes examples for several common loader types:

- loading plain text files
- loading PDF documents
- loading multiple PDFs from a directory
- loading content from web pages

## Example scripts

### [text_loader.py](text_loader.py)
Loads a local text file and converts it into a LangChain document that can be processed further.

### [pypdf_loader.py](pypdf_loader.py)
Reads content from a PDF file using PyPDF so it can be passed into an LLM pipeline.

### [directory_loader.py](directory_loader.py)
Loads multiple PDF files from a folder, which is useful for batch processing and document ingestion.

### [webBase_loader.py](webBase_loader.py)
Fetches content from a web page and uses it as input for an AI workflow.

## Typical workflow

A typical document-loading workflow looks like this:

1. Load data from a source
2. Convert it into LangChain documents
3. Pass the documents into a prompt, chain, or vector database
4. Generate summaries, answers, or embeddings

## How to run the examples

From this folder, you can run the sample scripts with Python:

```bash
python text_loader.py
```

You can also try:

```bash
python pypdf_loader.py
python directory_loader.py
python webBase_loader.py
```

## Notes

Some examples may require API keys and internet access, especially the web-based loader.

## Summary

Document loaders are the bridge between raw data and intelligent applications. They make it possible to feed local files, PDFs, and web content into LangChain pipelines and turn them into useful AI-ready inputs.
