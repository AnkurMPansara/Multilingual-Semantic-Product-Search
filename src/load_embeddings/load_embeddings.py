import os
import pickle

def load_embedding(embedding_path: str):
    """
    Load the product_id -> embedding dictionary from the pickle cache.

    Args:
        embedding_path: path to pickle file

    Returns:
        dict mapping product_id (str) to embedding (list of floats)
    """
    if not os.path.exists(embedding_path):
        return {}  # return empty dict if file does not exist

    with open(embedding_path, "rb") as f:
        embeddings_dict = pickle.load(f)

    return embeddings_dict
