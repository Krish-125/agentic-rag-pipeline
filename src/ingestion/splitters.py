from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(documents: list[Document], chunk_size: int = 800, chunk_overlap: int = 150) -> list[Document]:
    """
    Split a list of Document objects into smaller chunks based on the specified chunk size and overlap.

    Args:
        documents (list[Document]): A list of Document objects to be split.
        chunk_size (int): The maximum size of each chunk. Default is 800 characters.
        chunk_overlap (int): The number of characters to overlap between chunks. Default is 150 characters.

    Returns:
        list[Document]: A list of Document objects representing the split chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    text_docs = []
    passthrough_docs = []

    for doc in documents:
       content_type = doc.metadata.get("content_type")
       if content_type in ("text", "markdown"):
           text_docs.append(doc)
       else:
           passthrough_docs.append(doc)

    split_text_docs = splitter.split_documents(text_docs)

    return split_text_docs + passthrough_docs

# if __name__ == "__main__":
#     from loaders import load_document

#     all_docs = load_document("sample.pdf")
#     print(f"Before splitting: {len(all_docs)} documents")

#     split_docs = split_documents(all_docs)
#     print(f"After splitting: {len(split_docs)} documents")

#     for d in split_docs[:5]:  # Print metadata and first 100 characters of the first 5 documents
#         print("----")
#         print(f"Document metadata: {d.metadata}")
#         print(f"Document content (first 150 chars): {d.page_content[:150]}...")