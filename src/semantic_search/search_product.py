import numpy as np

def search_product(query_embedding: list[float],
                   product_embeddings: dict,
                   result_count: int = 5,
                   similarity_threshold: float = 0.0):
    """
    Search for products closest to the query embedding.

    Args:
        query_embedding: list of floats (embedding of search query)
        product_embeddings: dict mapping product_id -> embedding (list of floats)
        result_count: max number of results to return
        similarity_threshold: minimum cosine similarity to include result

    Returns:
        List of dicts: [{"product_id": ..., "similarity": ...}, ...]
    """
    results = []

    query_emb = query_embedding.values

    # Precompute query norm
    query_vec = np.array(query_emb)
    query_norm = np.linalg.norm(query_vec)

    for product_id, emb in product_embeddings.items():
        product_emb = emb.values
        emb_vec = np.array(product_emb)
        emb_norm = np.linalg.norm(emb_vec)
        if emb_norm == 0 or query_norm == 0:
            sim = 0.0
        else:
            sim = float(np.dot(query_vec, emb_vec) / (query_norm * emb_norm))

        if sim >= similarity_threshold:
            results.append({"product_id": product_id, "similarity": sim})

    # Sort descending by similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)

    # Return top N
    return results[:result_count]
