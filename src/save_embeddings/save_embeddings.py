import os
import pickle

def save_embedding(product_id: str, product_embedding: list[float], embedding_path: str):
    """
    Save a single product embedding to a pickle cache with product_id -> embedding mapping.

    Args:
        product_id: Amazon-style ASIN (string)
        product_embedding: list of floats
        embedding_path: path to pickle file
    """
    # Load existing cache if it exists
    if os.path.exists(embedding_path):
        with open(embedding_path, "rb") as f:
            data = pickle.load(f)
            embeddings_dict = data
    else:
        embeddings_dict = {}

    # Add or update entry
    embeddings_dict[product_id] = product_embedding

    # Save back
    with open(embedding_path, "wb") as f:
        pickle.dump(embeddings_dict, f)