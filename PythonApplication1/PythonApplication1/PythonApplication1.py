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
 
# Step 2: Parse the HTML and extract book details 
def extract_book_details(): 
    url = BASE_URL 
    books = [] 
    while url: 
        html_content = fetch_html(url) 
        soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content 
        for article in soup.select('article.product_pod'):  # Select all book containers 
            title = article.h3.a['title']  # Extract the title attribute 
            stock = article.select_one('p.instock.availability').text.strip()  # Extract stock availability
            genre = soup.select_one('ul.breadcrumb li:nth-of-type(3)')  # Extract genre from breadcrumb
            genre_text = genre.text.strip() if genre else "Unknown"
            books.append({'title': title, 'genre': genre_text, 'stock': stock}) 
        # Find the "Next" button and update the URL 
        next_button = soup.select_one('li.next a') 
        if next_button: 
            next_page = next_button['href'] 
            url = BASE_URL + next_page if 'catalogue/' in next_page else BASE_URL + 'catalogue/' + next_page 
        else: 
            url = None  # No more pages 
    return books 
 
if __name__ == "__main__": 
    books = extract_book_details() 
    print("Extracted Book Details:") 
    for book in books: 
        print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}") 
    choice = input("Would you like to filter by Titel, Genre or Stock (please enter the choices as displayed on screen): ") 
     
    if choice.lower() == "title": 
        filter_value = input("Enter the title to filter by: ")
        filtered_books = [book for book in books if filter_value.lower() in book['title'].lower()]
        print("Filtered Books by Title:")
        for book in filtered_books:
            print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}")
    elif choice.lower() == "genre": 
        filter_value = input("Enter the genre to filter by: ")
        filtered_books = [book for book in books if filter_value.lower() in book['genre'].lower()]
        print("Filtered Books by Genre:")
        for book in filtered_books:
            print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}")
    elif choice.lower() == "stock": 
        filter_value = input("Enter the stock status to filter by (e.g., 'In stock'): ")
        filtered_books = [book for book in books if filter_value.lower() in book['stock'].lower()]
        print("Filtered Books by Stock:")
        for book in filtered_books:
            print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}")
    else:
        print("Invalid choice. No filtering applied.")
