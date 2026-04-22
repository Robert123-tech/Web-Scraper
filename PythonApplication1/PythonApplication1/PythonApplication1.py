from itertools import count
import requests
from bs4 import BeautifulSoup
hi = input("entt")
# Step 1: Fetch the HTML content of the website
BASE_URL = "http://books.toscrape.com/"
def fetch_html(url):
    response = requests.get(url)  # Retrieves the HTML content
    if response.status_code == 200:  # Checks if the request was successful (status code 200 means OK)
        print(f"Successfully fetched {url}")  # Print a success message with the URL
        return response.text
    else:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return None

# Step 2: Parse the HTML and extract book titles
def extract_book_titles():
    url = BASE_URL
    titles = []
    while url:
        html_content = fetch_html(url)
        soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content
        for article in soup.select('article.product_pod'):  # Select all book containers
            title = article.h3.a['title']  # Extract the title attribute
            titles.append(title)
        # Find the "Next" button and update the URL
        next_button = soup.select_one('li.next a')
        if next_button:
            next_page = next_button['href']
            url = BASE_URL + next_page if 'catalogue/' in next_page else BASE_URL + 'catalogue/' + next_page
        else:
            url = None  # No more pages
    return titles

if __name__ == "__main__":
    book_titles = extract_book_titles()
    print("Extracted Book Titles:")
    for title in book_titles:
        print(title)
    choice = input("would you like to filter by Titel, Genre or Stock (please enter the choices as displayed on screen): ")
    
    if choice == "Titel":
        print("you have chosen to filter by titel")
