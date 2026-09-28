import { useEffect, useState } from "react";
import { getBookById } from "../services/booksApi";
import type { Book } from "../services/booksApi";

interface BookDetailsProps {
  bookId: number;
  onBack: () => void;
}

export default function BookDetails({ bookId, onBack }: BookDetailsProps) {
  const [book, setBook] = useState<Book | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchBook = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await getBookById(bookId);
        setBook(data);
      } catch {
        setError("Could not load book details. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchBook();
  }, [bookId]);

  return (
    <div className="book-details">
      <button className="back-button" onClick={onBack}>
        ← Back to Books
      </button>

      {isLoading && <p className="books-status">Loading book details...</p>}

      {error && <p className="books-status books-error">{error}</p>}

      {book && !isLoading && !error && (
        <div className="book-card book-details-card">
          <h2>{book.title}</h2>
          <p><strong>Author:</strong> {book.author}</p>
          <p><strong>Category:</strong> {book.category}</p>
          <p><strong>Year:</strong> {book.year}</p>
          <p><strong>Available:</strong> {book.available ? "Yes" : "No"}</p>
        </div>
      )}
    </div>
  );
}