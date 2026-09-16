import { useEffect, useState } from "react";
import { getAllBooks } from "../services/booksApi";
import type { Book } from "../services/booksApi";
import EditBookForm from "./EditBookForm";

export default function Books() {
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const data = await getAllBooks();
        setBooks(data);
      } catch {
        setError("Could not load books. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchBooks();
  }, []);

  if (isLoading) {
    return <p className="books-status">Loading books...</p>;
  }

  if (error) {
    return <p className="books-status books-error">{error}</p>;
  }

  if (books.length === 0) {
    return <p className="books-status">No books found.</p>;
  }

    if (editingId !== null) {
    return (
      <EditBookForm
        bookId={editingId}
        onBookUpdated={() => {
          setEditingId(null);
          setIsLoading(true);
          getAllBooks()
            .then(setBooks)
            .catch(() => setError("Could not load books. Please try again later."))
            .finally(() => setIsLoading(false));
        }}
      />
    );
  }

  return (
    <div className="books-list">
      {books.map((book) => (
        <div key={book.id} className="book-card">
          <h3>{book.title}</h3>
          <p>
            <strong>Author:</strong> {book.author}
          </p>
          <p>
            <strong>Category:</strong> {book.category}
          </p>
          <p>
            <strong>Year:</strong> {book.year}
          </p>
          <p>
            <strong>Available:</strong> {book.available ? "Yes" : "No"}
          </p>
          <button onClick={() => setEditingId(book.id)}>Edit</button>
        </div>
      ))}
    </div>
  );
}