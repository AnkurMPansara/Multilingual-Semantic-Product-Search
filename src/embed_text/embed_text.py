import time
from google import genai
from google.genai import types


def embed_text(
    texts: list[str],
    client: genai.Client,
    model: str = "gemini-embedding-001",
    dimensions: int = 384,
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> list[list[float]]:
    """
    Generate an embedding vector for a single text using the Gemini API.

    Args:
        text: input text to embed
        client: an already-initialized GenAI client instance (google.genai.GenAI)
        model: embedding model name (default: "gemini-embedding-001")
        dimensions: optional output dimensionality
        task_type: embedding task type (e.g., "RETRIEVAL_DOCUMENT" or "RETRIEVAL_QUERY")

    Returns:
        list of floats representing the embedding vector (first embedding returned)
    """
    # Time for rate limiting
    EMBEDDING_RESPONSE_TIME=6000
    start = time.time()
    # Build config using both dimensions and task_type
    config = types.EmbedContentConfig(
        output_dimensionality=dimensions,
        task_type=task_type,
    )

    response = client.models.embed_content(
        model=model,
        contents=texts,
        config=config
    )

    elapsed_ms = (time.time() - start) * 1000
    remaining = EMBEDDING_RESPONSE_TIME - elapsed_ms

    if remaining > 0:
        time.sleep(remaining / 1000)

    return response.embeddings