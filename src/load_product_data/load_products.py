import csv

def load_products(data_path: str):
    """
    Load the entire product CSV file.

    Args:
        data_path: path to CSV file containing product data

    Returns:
        List of dicts, each dict represents a CSV row
    """
    products = []
    with open(data_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(row)
    return products
