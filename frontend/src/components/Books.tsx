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

  if (isLoading) return <p className="books-status loading">Loading books...</p>;
  if (error) return <p className="books-status books-error">{error}</p>;

  return (
    <div>
      <div className="books-page-header">
        <div>
          <h2>Books Library</h2>
          <p className="books-subtitle">Browse, manage, and explore the library's collection.</p>
        </div>
        <div className="books-header-actions">
          <span className="books-count">{books.length} {books.length === 1 ? "book" : "books"}</span>
          <button className="btn-primary" onClick={() => navigate("/books/new")}>
            Add Book
          </button>
        </div>
      </div>

      {deleteError && <p className="books-error">{deleteError}</p>}

      {books.length === 0 ? (
        <div className="books-empty">
          <p>No books found in the library yet.</p>
          <button className="btn-primary" onClick={() => navigate("/books/new")}>
            Add your first book
          </button>
        </div>
      ) : (
        <div className="books-list">
          {books.map((book) => (
            <div key={book.id} className="book-card">
              <div className="book-card-header">
                <h3 className="book-title">{book.title}</h3>
                <span className={`status-badge ${book.available ? "available" : "unavailable"}`}>
                  {book.available ? "Available" : "Unavailable"}
                </span>
              </div>
              <p className="book-meta"><strong>Author:</strong> {book.author}</p>
              <p className="book-meta"><strong>Category:</strong> {book.category}</p>
              <p className="book-meta"><strong>Year:</strong> {book.year}</p>
              <div className="book-card-actions">
                <button onClick={() => navigate(`/books/${book.id}`)}>View</button>
                <button onClick={() => navigate(`/books/${book.id}/edit`)}>Edit</button>
                <button
                  onClick={() => handleDelete(book.id)}
                  disabled={deletingId !== null}
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