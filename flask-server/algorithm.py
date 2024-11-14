import math
from typing import List, Dict
import numpy as np
from collections import Counter
import requests
import json
import argparse
import pandas as pd  # Import pandas for CSV handling

class BM25:
    def __init__(self, k1=1.5, b=0.75):
        """
        Initialize BM25 with parameters
        
        Args:
            k1: Term frequency saturation parameter (default: 1.5)
            b: Length normalization parameter (default: 0.75)
        """
        self.k1 = k1
        self.b = b
        
        # Fetch and store books data
        self.books = self._fetch_books()
        
        # Create documents from preprocessed text
        self.documents = [
            book['preprocessed_text'].lower().split() if 'preprocessed_text' in book else []
            for book in self.books
        ]
        
        # Calculate lengths and averages
        self.lengths = [len(doc) for doc in self.documents]
        if self.documents:
            self.avg_length = sum(self.lengths) / len(self.documents)
        else:
            self.avg_length = 0  # Set to 0 or handle as needed
            print("Can't access books")

        
        # Calculate document frequencies
        self.doc_freqs = {}
        self.calculate_doc_frequencies()
        
        # Calculate IDF scores
        self.idf_scores = {}
        self.calculate_idf_scores()
    
    def _fetch_books(self):
        """Fetch books data from the local CSV file"""
        try:
            data = pd.read_csv('books_dataset.csv')  # Read the CSV file
            return data.to_dict(orient='records')  # Convert to list of dictionaries
        except (FileNotFoundError, pd.errors.EmptyDataError) as e:
            print(f"Error fetching books data: {e}")
            return []  
    
    def calculate_doc_frequencies(self):
        """Calculate document frequencies for both title and text"""
        for document in self.documents:
            for term in set(document):
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1
    
    def calculate_idf_scores(self):
        """Calculate IDF scores for both title and text"""
        total_docs = len(self.documents)
        
        for term, doc_freq in self.doc_freqs.items():
            self.idf_scores[term] = math.log((total_docs - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
    
    def score_document(self, query: str, doc_index: int) -> float:
        """
        Calculate combined BM25 score for a single document
        
        Args:
            query: Search query string
            doc_index: Index of document to score
            
        Returns:
            float: Combined BM25 score
        """
        # Calculate text score
        text_score = self._score_component(
            query,
            doc_index,
            self.documents,
            self.lengths,
            self.avg_length,
            self.idf_scores
        )
        
        return text_score
    
    def _score_component(self, query: str, doc_index: int, documents: List[List[str]], 
                        lengths: List[int], avg_length: float, idf_scores: Dict[str, float]) -> float:
        """Helper method to calculate BM25 score for a single component (title or text)"""
        score = 0.0
        doc_length = lengths[doc_index]
        length_norm = 1 - self.b + self.b * (doc_length / avg_length)
        
        # Get term frequencies
        doc_term_freqs = Counter(documents[doc_index])
        
        # Score each query term
        query_terms = query.lower().split()
        for term in query_terms:
            if term not in idf_scores:
                continue
                
            tf = doc_term_freqs.get(term, 0)
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * length_norm
            score += idf_scores[term] * (numerator / denominator)
            
        return score
    
    def search(self, query: str, top_k: int = 6, normalize_scores: bool = True) -> List[dict]:
        """
        Search books with a query and return top k results
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            normalize_scores: Whether to normalize scores to 0-1 range
            
        Returns:
            List of dicts containing book information and search scores
        """
        scores = []
        for i in range(len(self.documents)):
            score = self.score_document(query, i)
            scores.append((i, score))
            
        # Sort by score in descending order
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Normalize scores if requested
        if normalize_scores and sorted_scores:
            max_score = sorted_scores[0][1]
            if max_score > 0:
                sorted_scores = [(idx, score/max_score) for idx, score in sorted_scores]
        
        # Return top k results with book information
        results = []
        for idx, score in sorted_scores[:top_k]:
            book = self.books[idx]
            results.append({
                'title': book['title'],
                'authors': book['authors'],
                'description': book['description'],
                'score': float(score),
                'categories': book['categories'],
                'publication_date': book.get('publication_date', 'N/A')
            })
            
        return results


