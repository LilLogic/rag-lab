from src.client.llm_client import generate


def extract_tags(document_text: str):
    prompt = (f"""You are extracting metadata for a technical document.
    
    Return exactly 5 lowercase keywords that best describe technical concepts explicitly mentioned or strongly represented in the document.
    
    Rules:
    - One or two words per keyword.
    - Separate keywords with commas.
    - No explanations.
    - No numbering.
    - No punctuation other than commas.
    
    Example:
    rag, embeddings, pgvector, retrieval, evaluation
    
    {document_text}""")

    tags_str = generate(prompt)

    return parse_tags(tags_str)


def parse_tags(tags_str: str):
    return [tag.strip() for tag in tags_str.split(",")]
