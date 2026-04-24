from itertools import count   
import requests   
from bs4 import BeautifulSoup   
 
# Step 1: Fetch the HTML content of the website   
BASE_URL = "http://books.toscrape.com/"   
print("Fetching book datat pleas wait")
def fetch_html(url):   
    response = requests.get(url)  # Retrieves the HTML content   
    if response.status_code == 200:  # Checks if the request was successful (status code 200 means OK) 
        return response.text   
    else:   
        print(f"Failed to fetch {url}, status code: {response.status_code}")   
        return None   
 
# Step 2: Get all genre URLs 
def get_genre_urls():   
    html_content = fetch_html(BASE_URL)   
    soup = BeautifulSoup(html_content, 'html.parser')   
    genre_links = soup.select('ul.nav-list ul li a')  # Select all genre links   
    genres = {   
        link.text.strip(): BASE_URL + link['href'] for link in genre_links   
    }   
    return genres   
 
# Step 3: Parse the HTML and extract book details from each genre page   
def extract_books_by_genre():   
    genres = get_genre_urls()   
    books = []   
 
    for genre_name, genre_url in genres.items():   
        url = genre_url   
        while url:   
            html_content = fetch_html(url)   
            soup = BeautifulSoup(html_content, 'html.parser')  # Parse the HTML content   
            for article in soup.select('article.product_pod'):  # Select all book containers   
                title = article.h3.a['title']  # Extract the title attribute   
                stock = article.select_one('p.instock.availability').text.strip()  # Extract stock availability   
                books.append({'title': title, 'genre': genre_name, 'stock': stock})   
            # Find the "Next" button and update the URL   
            next_button = soup.select_one('li.next a')   
            if next_button:   
                next_page = next_button['href']   
                url = genre_url.rsplit('/', 1)[0] + '/' + next_page   
            else:   
                url = None  # No more pages   
    return books   
 
if __name__ == "__main__":   
    books = extract_books_by_genre()   
    print("Extracted All Book Details:")  
    new = []
  
    choice = input("Would you like to filter by Title, Genre or Stock (please enter the choices as displayed on screen) or if you would like to stop filtering type x: ")   
        
    if choice.lower() == "title":   
        filter_title = input("Enter the title to filter by: ")   
        for book in books:   
            if filter_title.lower() in book['title'].lower():   
                print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}")
                new.append(book)
    elif choice.lower() == "genre":   
        filter_genre = input("Enter the genre to filter by: ")   
        for book in books:   
            if filter_genre.lower() in book['genre'].lower():   
                print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}") 
                new.append(book)
    elif choice.lower() == "stock":   
        filter_stock = input("Enter the stock status to filter by (e.g., 'In stock'): ")   
        for book in books:   
            if filter_stock.lower() in book['stock'].lower():   
                print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}")
                new.append(book)
    elif choice.lower() == "x":   
        print("Exiting filtering.")  
    else:   
        print("Invalid choice. No filtering applied.") 

    while True:
        choice = input("Would you like to filter by Title, Genre or Stock (please enter the choices as displayed on screen) or if you would like to stop filtering type x: ")
        if choice.lower() == "title":   
            filter_title = input("Enter the title to filter by: ")   
            for book in new:   
                if filter_title.lower() in book['title'].lower():   
                    print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}")
                    new.append(book)
        elif choice.lower() == "genre":   
            filter_genre = input("Enter the genre to filter by: ")   
            for book in new:   
                if filter_genre.lower() in book['genre'].lower():   
                    print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}") 
                    new.append(book)
        elif choice.lower() == "stock":   
            filter_stock = input("Enter the stock status to filter by (e.g., 'In stock'): ")   
            for book in new:   
                if filter_stock.lower() in book['stock'].lower():   
                    print(f"Title: {book['title']}, Genre: {book['genre']}, Stock: {book['stock']}")
                    new.append(book)
        elif choice.lower() == "x":   
            print("Exiting filtering.")
            break
        else:   
            print("Invalid choice. No filtering applied.") 

