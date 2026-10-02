import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { getAllBooks, deleteBook } from "../services/booksApi";
import type { Book } from "../services/booksApi";

export default function Books() {
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const navigate = useNavigate();

  const fetchBooks = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getAllBooks();
      setBooks(data);
    } catch {
      setError("Could not load books. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBooks();
  }, [fetchBooks]);

  const handleDelete = async (id: number) => {
    if (deletingId !== null) return;

    const confirmed = window.confirm("Are you sure you want to delete this book?");
    if (!confirmed) return;

    setDeleteError(null);
    setDeletingId(id);

    try {
      await deleteBook(id);
      setBooks((prev) => prev.filter((book) => book.id !== id));
    } catch {
      setDeleteError("Could not delete the book. Please try again.");
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) return <p className="books-status">Loading books...</p>;
  if (error) return <p className="books-status books-error">{error}</p>;

  return (
    <div>
      <div className="books-header">
        <button onClick={() => navigate("/books/new")}>Add Book</button>
      </div>

      {deleteError && <p className="books-error">{deleteError}</p>}

      {books.length === 0 ? (
        <p className="books-status">No books found.</p>
      ) : (
        <div className="books-list">
          {books.map((book) => (
            <div key={book.id} className="book-card">
              <h3>{book.title}</h3>
              <p><strong>Author:</strong> {book.author}</p>
              <p><strong>Category:</strong> {book.category}</p>
              <p><strong>Year:</strong> {book.year}</p>
              <p><strong>Available:</strong> {book.available ? "Yes" : "No"}</p>
              <div className="book-card-actions">
                <button onClick={() => navigate(`/books/${book.id}`)}>View</button>
                <button onClick={() => navigate(`/books/${book.id}/edit`)}>Edit</button>
                <button
                  onClick={() => handleDelete(book.id)}
                  disabled={deletingId === book.id}
                  className="delete-button"
                >
                  {deletingId === book.id ? "Deleting..." : "Delete"}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}