from flask import Flask, request, jsonify
from algorithm import BM25  # Ensure you import the BM25 class
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Initialize the BM25 algorithm
bm25 = BM25()

@app.route('/api/search', methods=['GET'])
def search_books():
    """
    Search for books based on a query parameter.
    
    Returns:
        JSON response with the top suggested books.
    """
    query = request.args.get('query', '')
    print('Received search query:', query)  # Log the received query

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    
    # Get suggested books from BM25
    suggested_books = bm25.search(query)

    # Ensure all suggested books have valid data
    valid_books = []
    for book in suggested_books:
        if isinstance(book.get('score'), (int, float)) and book.get('title') and book.get('authors'):
            if 'categories' in book and (book['categories'] is None or isinstance(book['categories'], str)):
                valid_books.append(book)
            else:
                book['categories'] = None
                valid_books.append(book)
    return jsonify(valid_books)

if __name__ == "__main__":
    app.run(debug=True)
