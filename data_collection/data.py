import requests
import pandas as pd
import nltk
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# this gets the resources we need for tokenizing and stemming
nltk.download('punkt')

# porter stemmer used for stemming the words eg. Runner, Running -> Run
ps = PorterStemmer()

# This is my Google Books API key
API_KEY = 'AIzaSyDlNvzgJDvhkgvlWdB3SIAADY-LQnyBSVE'

# This queries the API to retrieve the data
def fetch_books_data(query, start_index=0, max_results=40):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&startIndex={start_index}&maxResults={max_results}&key={API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def process_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    return ' '.join(tokens)

# Extract book metadata, only if a description exists
def extract_book_data(item):
    volume_info = item.get('volumeInfo', {})
    title = volume_info.get('title', 'N/A')
    description = volume_info.get('description', None) 
    image_links = volume_info.get('imageLinks',{})
    thumbnail = image_links.get('thumbnail', 'No Image Available') 
    
    # only go forward if the description exists, we only want books with descriptions.
    if description:
        categories = ', '.join(volume_info.get('categories', []))

        preprocessed_title = process_text(title)
        preprocessed_description = process_text(description)
        preprocessed_categories = process_text(categories)
        preprocessed_text = process_text(f"{title} {description} {categories}")

        return {
            'title': volume_info.get('title','N/A'),
            'preprocessed_title': preprocessed_title,
            'authors': ', '.join(volume_info.get('authors', [])),
            'publisher': volume_info.get('publisher', 'N/A'),
            'publishedDate': volume_info.get('publishedDate', 'N/A'),
            'categories': preprocessed_categories,
            'averageRating': volume_info.get('averageRating', 'N/A'),
            'ratingsCount': volume_info.get('ratingsCount', 'N/A'),
            'pageCount': volume_info.get('pageCount', 'N/A'),
            'language': volume_info.get('language', 'N/A'),
            'description': volume_info.get('description'),
            'preprocessed_text': preprocessed_text,
            'thumbnail': thumbnail
        }
    return None  # Return None if there's no description

# This collects the data based on the 10 different genres we chose
def collect_books_data(queries, max_books_per_query=400):
    books_data = []
    for query in queries:
        start_index = 0
        books_collected = 0
        while books_collected < max_books_per_query:
            data = fetch_books_data(query, start_index)
            if not data or 'items' not in data:
                break
            
            for item in data['items']:
                book_data = extract_book_data(item)
                if book_data:  # Only add books with descriptions
                    books_data.append(book_data)
                    books_collected += 1

                if books_collected >= max_books_per_query:
                    break
            
            start_index += 40  # Continue querying until 400 books with descriptions are collected
    
    return books_data

queries = ['Fiction', 'Science Fiction', 'History', 'Fantasy', 'Horror', 'Romance', 'Mystery', 'Biography', 'Thriller', 'True Crime']

books_data = collect_books_data(queries)

books_df = pd.DataFrame(books_data)

books_df.to_csv('books_datasetnew.csv', index=False)

print(books_df.head())


import matplotlib.pyplot as plt

# Ensure missing descriptions are handled by filling NaNs with an empty string
books_df['description'] = books_df['description'].fillna('')

# Calculate the length of each description in terms of word count
books_df['description_length'] = books_df['description'].apply(lambda x: len(x.split()))

# Plot the histogram of description lengths
books_df['description_length'].hist(bins=30, color='lightcoral')
plt.title('Distribution of Description Lengths')
plt.xlabel('Number of Words in Description')
plt.ylabel('Number of Books')
plt.tight_layout()

# Save and display the plot
plt.savefig('description_lengths.png')
plt.show()