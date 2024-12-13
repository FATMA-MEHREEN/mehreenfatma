import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape WebScraper.io
def scrape_webscraper(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    data = []

    # Find all product listings
    products = soup.find_all("div", class_="thumbnail")
    for product in products:
        # Extract product name
        name = product.find("a", class_="title").text.strip() if product.find("a", class_="title") else "N/A"
        
        # Extract product price
        price = product.find("h4", class_="price").text.strip() if product.find("h4", class_="price") else "N/A"
        
        # Extract product description
        description = product.find("p", class_="description").text.strip() if product.find("p", class_="description") else "N/A"
        
        # Extract product link
        link = "https://webscraper.io" + product.find("a", class_="title")["href"] if product.find("a", class_="title") else "N/A"
        
        # Add to data list
        data.append({"Name": name, "Price": price, "Description": description, "Link": link})
    
    return data

# Save data to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main execution
if __name__ == "__main__":
    url = "https://webscraper.io/test-sites/e-commerce/allinone"
    scraped_data = scrape_webscraper(url)

    if scraped_data:
        save_to_csv(scraped_data, "webscraper_data.csv")
