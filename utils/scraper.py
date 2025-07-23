import os
import requests
from bs4 import BeautifulSoup
import json

class Scraper:
    def __init__(self, output_dir, logger=None):
        """
        Initialize the scraper with an output directory and a logger.
        
        Args:
            output_dir (str): Directory to store scraped data.
            logger: A Logger instance for logging messages.
        """
        self.output_dir = output_dir
        self.logger = logger  # Use the provided logger or default to None

    def scrape_data(self, url):
        """
        Scrapes structured data from a given URL.
        
        Args:
            url (str): The URL of the webpage to scrape.
        
        Returns:
            dict: A dictionary containing the structured data, or None if scraping fails.
        """
        try:
            if self.logger:
                self.logger.info(f"Fetching URL: {url}")
            response = requests.get(url, timeout=10, allow_redirects=True)

            if response.status_code != 200:
                if self.logger:
                    self.logger.error(f"Failed to fetch. Status code: {response.status_code}")
                return None

            soup = BeautifulSoup(response.text, "html.parser")
            structured_data = []
            current_section = None

            for tag in soup.find_all(["h1", "h2", "h3", "p", "ul", "ol"]):
                tag_name = tag.name

                if tag_name in ["h1", "h2", "h3"]:
                    if current_section:
                        structured_data.append(current_section)
                    current_section = {
                        "heading": tag.get_text(strip=True),
                        "level": tag_name,
                        "content": []
                    }

                elif tag_name == "p" and current_section:
                    text = tag.get_text(strip=True)
                    links = [{"text": a.get_text(strip=True), "url": a["href"]} for a in tag.find_all("a", href=True)]
                    current_section["content"].append({
                        "type": "paragraph",
                        "text": text,
                        "links": links
                    })

                elif tag_name in ["ul", "ol"] and current_section:
                    list_items = [li.get_text(strip=True) for li in tag.find_all("li")]
                    current_section["content"].append({
                        "type": "list",
                        "items": list_items
                    })

            if current_section:
                structured_data.append(current_section)

            if self.logger:
                self.logger.info(f"Successfully scraped data from: {url}")
            return structured_data

        except requests.exceptions.RequestException as e:
            if self.logger:
                self.logger.error(f"Error fetching webpage: {e}")
            return None

    def save_data(self, data, filename):
        """
        Saves scraped data to a JSON file.
        
        Args:
            data (dict): The scraped data to save.
            filename (str): Name of the output file.
        """
        try:
            os.makedirs(self.output_dir, exist_ok=True)
            output_file = os.path.join(self.output_dir, filename)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if self.logger:
                self.logger.info(f"Data saved to: {output_file}")
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error saving data to file: {e}")

    def scrape_links(self, links):
        """
        Scrapes data for a list of URLs and saves the results.
        
        Args:
            links (list): List of URLs to scrape.
        """
        for i, url in enumerate(links, start=1):
            if self.logger:
                self.logger.info(f"Processing URL {i}/{len(links)}: {url}")
            data = self.scrape_data(url)
            if data:
                filename = f"link_{i}.json"
                self.save_data(data, filename)
            else:
                if self.logger:
                    self.logger.error(f"Failed to scrape data for URL: {url}")