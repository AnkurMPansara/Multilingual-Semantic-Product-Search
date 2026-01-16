<a name="readme-top"></a>
# Multilingual Semantic Product Search

A Python-based semantic search system that uses Google's Gemini embedding models to enable multilingual product search. This project allows users to search through product catalogs using natural language queries, finding products based on semantic similarity rather than exact keyword matches.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This project implements a semantic product search system that:

1. **Loads product data** from a CSV file
2. **Generates embeddings** for each product using Google's Gemini embedding model
3. **Caches embeddings** to avoid redundant API calls
4. **Performs semantic search** by comparing query embeddings with product embeddings using cosine similarity
5. **Returns relevant products** ranked by similarity score

The system supports multilingual queries and can understand the semantic meaning of search terms, making it more powerful than traditional keyword-based search.

## ✨ Features

- 🔍 **Semantic Search**: Find products based on meaning, not just keywords
- 🌍 **Multilingual Support**: Works with queries in multiple languages (via Gemini embeddings)
- 💾 **Embedding Caching**: Saves embeddings to disk to avoid redundant API calls
- ⚡ **Batch Processing**: Efficiently processes products in batches
- 🎯 **Similarity Scoring**: Returns products ranked by relevance
- 🔄 **Incremental Updates**: Only generates embeddings for new products

## 🏗️ Architecture

The system follows a modular architecture with the following components:

```
┌─────────────────┐
│   Product CSV   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Load Products  │─────▶│  Generate        │
│                 │      │  Embeddings      │
└─────────────────┘      └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Save Embeddings │
                         │  (Pickle Cache)  │
                         └────────┬─────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐      ┌──────────────────┐    ┌─────────────────┐
│  User Query     │─────▶│  Query Embedding │───▶│  Cosine         │
│                 │      │                  │    │  Similarity     │
└─────────────────┘      └──────────────────┘    └────────┬────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │  Top Results   │
                                                 │  with Details   │
                                                 └─────────────────┘
```

## 📁 Project Structure

```
Multilingual-Semantic-Product-Search/
│
├── main.py                          # Main application entry point
├── requirements.txt                 # Python dependencies
├── run.bat                          # Windows execution script
├── run.sh                           # Linux/Mac execution script
├── .gitignore                       # Git ignore rules
│
├── data/
│   ├── product_data.csv            # Product catalog CSV file
│   └── PLACE_YOUR_PRODUCT_DATA_CSV_FILE_HERE.txt
│
├── src/
│   ├── __init__.py
│   │
│   ├── embed_text/
│   │   ├── __init__.py
│   │   └── embed_text.py          # Text embedding generation
│   │
│   ├── save_embeddings/
│   │   ├── __init__.py
│   │   └── save_embeddings.py     # Save embeddings to pickle file
│   │
│   ├── load_embeddings/
│   │   ├── __init__.py
│   │   └── load_embeddings.py     # Load embeddings from pickle file
│   │
│   ├── load_product_data/
│   │   ├── __init__.py
│   │   └── load_products.py       # Load product CSV data
│   │
│   └── semantic_search/
│       ├── search_product.py      # Cosine similarity search
│       └── get_product_details.py # Retrieve product details by ID
│
└── vector_embedding/
    ├── product_embeddings.pkl     # Cached embeddings (generated)
    └── SAVE_THIS_FILE_FOR_FUTURE_USE.txt
```

## 🔧 Prerequisites

- **Python 3.8+** (Python 3.9 or higher recommended)
- **Google Gemini API Key** - Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Product Data CSV** - A CSV file with product information

### Required CSV Format

Your product CSV file should contain at least the following columns:
- `asin` - Product identifier (Amazon Standard Identification Number)
- `title` - Product title/name
- `imgUrl` - Product image URL
- `productURL` - Product page URL
- `price` - Product price
- `categoryName` or `category_id` - Product category

Example CSV structure:
```csv
asin,title,imgUrl,productURL,stars,reviews,price,listPrice,category_id,isBestSeller,boughtInLastMonth
B014TMV5YE,"Product Title",https://...,https://...,4.5,100,139.99,159.99,104,False,2000
```

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Multilingual-Semantic-Product-Search
```

### 2. Install Dependencies

#### Option A: Using the provided scripts (Recommended)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

#### Option B: Manual Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

**Note:** The `.env` file is gitignored for security. Never commit your API key.

### 4. Prepare Product Data

Place your product CSV file in the `data/` directory and name it `product_data.csv`, or update the `PRODUCT_DATA_PATH` in `main.py`.

## ⚙️ Configuration

You can modify the following settings in `main.py`:

```python
# Paths
PRODUCT_DATA_PATH = "data/product_data.csv"
EMBEDDING_PATH = "vector_embedding/product_embeddings.pkl"

# Embedding Configuration
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSIONS = 1536
EMBEDDING_BATCH_SIZE = 10
EMBEDDING_REQUEST_PER_MINUTE = 100
PRODUCT_EMBEDDING_TASK_TYPE = "RETRIEVAL_DOCUMENT"
QUERY_EMBEDDING_TASK_TYPE = "RETRIEVAL_QUERY"

# Search Configuration
result_count = 5                    # Number of results to return
similarity_threshold = 0.0          # Minimum similarity score
```

## 🚀 Usage

### Running the Application

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
./run.sh
```

**Or manually:**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Set environment variable (if not using .env)
export GEMINI_API_KEY=your_api_key_here  # Linux/Mac
set GEMINI_API_KEY=your_api_key_here  # Windows

# Run the application
python main.py
```

### Using the Search

1. **First Run**: The application will generate embeddings for all products in your CSV file. This may take some time depending on the number of products and API rate limits.

2. **Subsequent Runs**: Only new products (not in the embedding cache) will be processed, making subsequent runs much faster.

3. **Search Query**: When prompted, enter your search query in any language:
   ```
   Enter your search query: comfortable running shoes
   Enter your search query: zapatillas de correr cómodas
   Enter your search query: 舒适的跑鞋
   ```

4. **Results**: The application will display the top 5 most similar products with:
   - Product ID (ASIN)
   - Similarity Score (0.0 to 1.0)
   - Product Name
   - Product Price
   - Category
   - Product URL
   - Image URL

## 🔍 How It Works

### 1. **Product Embedding Generation**

- Products are loaded from the CSV file
- For each product, a text representation is created: `"{title} {categoryName}"`
- The text is sent to Google's Gemini embedding API to generate a vector representation
- Embeddings are cached in a pickle file to avoid regenerating them

### 2. **Query Processing**

- User enters a search query
- The query is converted to an embedding vector using the same model
- Different task types are used:
  - `RETRIEVAL_DOCUMENT` for products (optimized for documents)
  - `RETRIEVAL_QUERY` for queries (optimized for search queries)

### 3. **Semantic Search**

- Cosine similarity is calculated between the query embedding and all product embeddings
- Products are ranked by similarity score (higher = more relevant)
- Top N results above the similarity threshold are returned

### 4. **Result Display**

- For each result, product details are fetched from the CSV
- Results are displayed with similarity scores and product information

### Mathematical Foundation

The similarity between query and product is calculated using **cosine similarity**:

```
similarity = (query_vector · product_vector) / (||query_vector|| × ||product_vector||)
```

Where:
- `·` is the dot product
- `||vector||` is the L2 norm (magnitude) of the vector

This measures the cosine of the angle between two vectors, ranging from -1 (opposite) to 1 (identical), with 0 meaning orthogonal (unrelated).

## 📚 Dependencies

### Core Dependencies

- **google-genai (1.59.0)**: Google's Gemini API client for generating embeddings
- **numpy (2.4.1)**: Numerical computing library for vector operations and cosine similarity calculations

### Python Standard Library

- `os` - Environment variable access
- `math` - Mathematical operations
- `time` - Rate limiting
- `csv` - CSV file reading
- `pickle` - Embedding cache serialization

## 📝 File Structure Details

### Main Application

- **`main.py`**: Orchestrates the entire workflow:
  - Loads products and existing embeddings
  - Generates embeddings for new products
  - Handles user input
  - Performs search and displays results

### Source Modules

- **`embed_text/embed_text.py`**: 
  - Generates embeddings using Gemini API
  - Implements rate limiting to respect API quotas
  - Supports batch processing

- **`save_embeddings/save_embeddings.py`**: 
  - Saves individual product embeddings to pickle cache
  - Maintains a dictionary mapping product_id → embedding

- **`load_embeddings/load_embeddings.py`**: 
  - Loads the embedding cache from disk
  - Returns empty dict if cache doesn't exist

- **`load_product_data/load_products.py`**: 
  - Reads CSV file and returns list of product dictionaries

- **`semantic_search/search_product.py`**: 
  - Computes cosine similarity between query and all products
  - Ranks and filters results by similarity threshold
  - Returns top N results

- **`get_product_details/get_product_details.py`**: 
  - Retrieves full product details from CSV by ASIN

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: GEMINI_API_KEY not found
   ```
   **Solution**: Ensure your `.env` file exists with `GEMINI_API_KEY=your_key`, or set it as an environment variable.

2. **CSV File Not Found**
   ```
   FileNotFoundError: data/product_data.csv
   ```
   **Solution**: Place your CSV file in the `data/` directory or update `PRODUCT_DATA_PATH` in `main.py`.

3. **Rate Limiting**
   ```
   Rate limit exceeded
   ```
   **Solution**: Reduce `EMBEDDING_REQUEST_PER_MINUTE` in `main.py` or wait before retrying.

4. **Missing Dependencies**
   ```
   ModuleNotFoundError: No module named 'google'
   ```
   **Solution**: Install dependencies: `pip install -r requirements.txt`

5. **Embedding Cache Issues**
   - If embeddings seem incorrect, delete `vector_embedding/product_embeddings.pkl` to regenerate them.

### Performance Tips

- **First Run**: Can be slow for large catalogs. Consider processing in smaller batches.
- **Subsequent Runs**: Much faster as only new products are processed.
- **Batch Size**: Adjust `EMBEDDING_BATCH_SIZE` based on your API quota and needs.
- **Similarity Threshold**: Increase `similarity_threshold` to filter out less relevant results.

## 🔐 Security Notes

- **Never commit** your `.env` file or API keys to version control
- The `.gitignore` file already excludes `.env` files
- Keep your Gemini API key secure and rotate it if compromised

## 📄 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## 📧 Contact

- **Ankur Pansara**  
  GitHub: [@AnkurMPansara](https://github.com/AnkurMPansara)  
  Email: [ankur.at.surat@gmail.com](mailto:ankur.at.surat@gmail.com)  
  LinkedIn: [Ankur Pansara](https://www.linkedin.com/in/ankur-pansara)  

---

**Note**: This project uses Google's Gemini embedding models. Make sure you comply with Google's API usage terms and pricing when using this system.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
