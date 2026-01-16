import csv

def get_product_details(product_id: str, data_path: str):
    """
    Retrieve a CSV row for the given product_id (ASIN).

    Args:
        product_id: Amazon-style ASIN to look for
        data_path: path to CSV file containing product data

    Returns:
        dict representing the CSV row if found, else None
    """
    with open(data_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get("asin") == product_id:
                return row
    return None
