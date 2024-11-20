"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import React, { useState, useEffect } from 'react';

// Define a type for the book object
type Book = {
    id: number; // Assuming you have an id for each book
    title: string;
    authors?: string;
    description: string;
    publishedDate?: string;
    pageCount?: number;
    thumbnail?: string;
};

const BookSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Book[]>([]);

    const handleSearch = async () => {
        if (!query) return;

        setResults([])

        try {
            const response = await fetch(`http://127.0.0.1:5000/api/search?query=${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const text = await response.text(); // Get the response as text
            const data = JSON.parse(text); // Parse the text as JSON
            setResults(data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const handlePostRequest = async (searchText: string) => {
        // Implement your post request logic here
        console.log('Post request with:', searchText);
        // Set output based on the response if needed
    };

    return (
        <main className="p-8">
            <h1 className="text-center text-2xl font-bold mb-4">Bookalytic</h1>
            <div className="flex justify-center mb-6">
                <p className="text-center mb-6 text-gray-700 w-4/5 md:w-3/4 lg:w-2/3">
                Welcome to Bookalytic, where finding your next great read is as easy as describing what you're in the mood for! Just type in a few words about the kind of book you’re interested in—whether it's a thrilling mystery, a cozy romance, or a thought-provoking journey—and let Bookalytic deliver personalized book recommendations tailored to your tastes. Our smart recommendation engine considers genres, themes, tones, and styles to match you with books that capture exactly what you’re looking for. Discover new authors, explore hidden gems, and rediscover classic favorites with recommendations unique to your reading desires.
                </p>
            </div>
            <div className="mb-8 flex flex-col items-center">
                <div className="w-full flex justify-center">
                    <Input 
                        type="text" 
                        placeholder="Describe your ideal book and we will handle the rest..." 
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        className="w-4/5 md:w-3/4 lg:w-2/3 h-12"
                    />
                </div>
                <div className="mt-4 flex justify-center">
                    <Button className="py-4 px-6" onClick={handleSearch}>Search</Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.map((book) => (
                    <Card key={book.id}>
                        <CardHeader>
                            <CardTitle>{book.title}</CardTitle>
                            <CardDescription>{book.authors}</CardDescription>
                        </CardHeader>
                        <CardContent>
                            {book.thumbnail && (
                            <img 
                                src={book.thumbnail} 
                                alt={`${book.title} thumbnail`} 
                                className="w-48 h-auto mb-4"
                            />
                            )}
                            <p>{book.description}</p>
                        </CardContent>
                        <CardFooter>
                            <p className="text-sm text-muted-foreground">
                                Published: {book.publishedDate === 'NaN' || !book.publishedDate ? 'Unknown' : book.publishedDate} 
                                <br />
                                Page Count: {book.pageCount || 'Unknown'}
                            </p>
                        </CardFooter>
                    </Card>
                ))}
            </div>
        </main>
    );
};

export default BookSearch;
