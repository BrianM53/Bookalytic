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
    authors: string;
    description: string;
    publishedDate?: string; // Optional field for published date
};

const BookSearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState<Book[]>([]);
    const [output, setOutput] = useState<string | null>(null); // For additional output if needed

    const handleSearch = async () => {
        if (!query) return;

        try {
            const response = await fetch(`http://localhost:5000/api/search?query=${encodeURIComponent(query)}`);
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
            <div className="mb-8">
                <Input 
                    type="text" 
                    placeholder="Search" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <Button onClick={handleSearch}>Search</Button>
                <Button onClick={() => handlePostRequest(query)}>Get Output</Button>
            </div>
            
            {output && <div className="output">{output}</div>}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.map((book) => (
                    <Card key={book.id}>
                        <CardHeader>
                            <CardTitle>{book.title}</CardTitle>
                            <CardDescription>{book.authors}</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p>{book.description}</p>
                        </CardContent>
                        <CardFooter>
                            <p className="text-sm text-muted-foreground">
                                Published: {book.publishedDate || 'Unknown'}
                            </p>
                        </CardFooter>
                    </Card>
                ))}
            </div>
        </main>
    );
};

export default BookSearch;
