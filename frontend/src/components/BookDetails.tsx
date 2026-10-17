import { useEffect, useState } from "react";
import { getBookById } from "../services/booksApi";
import type { Book } from "../services/booksApi";

interface BookDetailsProps {
  bookId: number;
  onBack: () => void;
  onEdit: () => void;
}

export default function BookDetails({ bookId, onBack, onEdit }: BookDetailsProps) {
  const [book, setBook] = useState<Book | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // /books/abc jaisi invalid ID par API call nahi karni
  const isValidId = Number.isInteger(bookId) && bookId > 0;

  useEffect(() => {
    if (!isValidId) return;

    let ignore = false; // purani request ka result ignore karne ke liye

    const fetchBook = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const data = await getBookById(bookId);
        if (!ignore) setBook(data);
      } catch {
        if (!ignore) {
          setError(
            "Could not load this book. It may no longer exist, or the server is unavailable."
          );
        }
      } finally {
        if (!ignore) setIsLoading(false);
      }
    };

    fetchBook();

    return () => {
      ignore = true;
    };
  }, [bookId, isValidId]);

  const errorMessage = isValidId ? error : "This book link is invalid.";
  const loading = isValidId && isLoading;
  const bookToShow = isValidId && !loading && !errorMessage ? book : null;

  return (
    <div className="book-details">
      <div className="book-details-header">
        <h2>Book Details</h2>
        <p>Complete information about the selected book.</p>
      </div>

      {loading && (
        <p className="books-status loading">Loading book details...</p>
      )}

      {errorMessage && (
        <p className="books-status books-error" role="alert">
          {errorMessage}
        </p>
      )}

      {bookToShow && (
        <article className="book-details-card">
          <h3 className="book-details-title">{bookToShow.title}</h3>

          <dl className="book-details-list">
            <div className="book-details-row">
              <dt>Author</dt>
              <dd>{bookToShow.author}</dd>
            </div>
            <div className="book-details-row">
              <dt>Category</dt>
              <dd>{bookToShow.category}</dd>
            </div>
            <div className="book-details-row">
              <dt>Publication Year</dt>
              <dd>{bookToShow.year}</dd>
            </div>
            <div className="book-details-row">
              <dt>Availability</dt>
              <dd>
                <span
                  className={`status-badge ${
                    bookToShow.available ? "available" : "unavailable"
                  }`}
                >
                  {bookToShow.available ? "Available" : "Unavailable"}
                </span>
              </dd>
            </div>
          </dl>
        </article>
      )}

      <div className="book-details-actions">
        <button type="button" className="btn-secondary" onClick={onBack}>
          ← Back to Books
        </button>
        {bookToShow && (
          <button type="button" className="btn-primary" onClick={onEdit}>
            Edit Book
          </button>
        )}
      </div>
    </div>
  );
}