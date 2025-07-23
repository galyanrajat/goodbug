def read_urls_from_file(file_path):
    """
    Reads a list of URLs from a text file.
    
    Args:
        file_path (str): Path to the file containing URLs.
    
    Returns:
        list: A list of URLs.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls