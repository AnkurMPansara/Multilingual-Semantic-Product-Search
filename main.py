import os
import math
from google import genai
from src.embed_text.embed_text import embed_text
from src.save_embeddings.save_embeddings import save_embedding
from src.load_embeddings.load_embeddings import load_embedding
from src.load_product_data.load_products import load_products
from src.semantic_search.search_product import search_product
from src.semantic_search.get_product_details import get_product_details

# Load secrets from env variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Paths
PRODUCT_DATA_PATH = "data/product_data.csv"
EMBEDDING_PATH = "vector_embedding/product_embeddings.pkl"

# Config
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 1536
EMBEDDING_BATCH_SIZE = 10
EMBEDDING_REQUEST_PER_MINUTE = 100
PRODUCT_EMBEDDING_TASK_TYPE = "RETRIEVAL_DOCUMENT"
QUERY_EMBEDDING_TASK_TYPE = "RETRIEVAL_QUERY"

# Load product data
products = load_products(PRODUCT_DATA_PATH)

# Load existing embeddings
product_embeddings = load_embedding(EMBEDDING_PATH)

# Get gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Loop over each product and ensure embedding exists
unidexed_products = [product for product in products if product.get("asin") not in product_embeddings]
if len(unidexed_products) == 0:
    print("All products already have embeddings.")
else:
    unidexed_product_count = len(unidexed_products)
    print(f"Total {unidexed_product_count} products missing from embedding")
    batch_count = math.ceil(unidexed_product_count/EMBEDDING_BATCH_SIZE)
    for batch_index in range(batch_count):
        start = batch_index*EMBEDDING_BATCH_SIZE
        end = min(start+EMBEDDING_BATCH_SIZE, unidexed_product_count)
        unidexed_product_batch = unidexed_products[start:end]
        batch_texts = [f"{product.get("title", "")} {product.get("categoryName", "")}" for product in unidexed_product_batch]
        batch_product_ids = [product.get("asin", "") for product in unidexed_product_batch]
        print(f"Embedding batch {batch_index}...")
        batch_embeddings = embed_text(batch_texts, client, EMBEDDING_MODEL, EMBEDDING_DIMENSIONS, PRODUCT_EMBEDDING_TASK_TYPE, EMBEDDING_REQUEST_PER_MINUTE)
        for product_id, embedding in zip(batch_product_ids, batch_embeddings):
            save_embedding(product_id, embedding, EMBEDDING_PATH)
            product_embeddings[product_id] = embedding
        print(f"Embedding saved for the batch {batch_index}, remaining products: {max(0, unidexed_product_count - (batch_index+1)*EMBEDDING_BATCH_SIZE)}")


# Prompt user for search query
user_query = input("Enter your search query: ")
embedding_result = embed_text([user_query], client, EMBEDDING_MODEL, EMBEDDING_DIMENSIONS, QUERY_EMBEDDING_TASK_TYPE, 0)
query_embedding = embedding_result[0]

# Perform search
top_results = search_product(
    query_embedding=query_embedding,
    product_embeddings=product_embeddings,
    result_count=5,
    similarity_threshold=0.0
)

# Fetch product details for each result and print
for result in top_results:
    asin = result["product_id"]
    similarity = result["similarity"]
    details = get_product_details(asin, PRODUCT_DATA_PATH)
    if details:
        print(f"Product ID: {asin}")
        print(f"Similarity Score: {similarity:.4f}")
        print(f"Product Name: {details.get('title')}")
        print(f"Product Price: {details.get('price')}")
        print(f"Category: {details.get('categoryName')}")
        print(f"Product URL: {details.get('productURL')}")
        print(f"Image URL: {details.get('imgUrl')}")
        print("-" * 50)
