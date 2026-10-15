import { useState, useEffect } from "react";
import { getBookById, updateBook } from "../services/booksApi";

interface EditBookFormProps {
  bookId: number;
  onBookUpdated?: () => void;
  onCancel?: () => void;
}

export default function EditBookForm({
  bookId,
  onBookUpdated,
  onCancel,
}: EditBookFormProps) {
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [category, setCategory] = useState("");
  const [year, setYear] = useState("");
  const [available, setAvailable] = useState(true);

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchBook = async () => {
      setIsLoading(true);
      setLoadError(null);
      try {
        const book = await getBookById(bookId);
        setTitle(book.title);
        setAuthor(book.author);
        setCategory(book.category);
        setYear(String(book.year));
        setAvailable(book.available);
      } catch {
        setLoadError("Could not load book details. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchBook();
  }, [bookId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSubmitting) return;


    if (
      !title.trim() ||
      !author.trim() ||
      !category.trim() ||
      !year.trim()
    ) {
      setSubmitError("Please fill in all required fields.");
      return;
    }

    const numericYear = Number(year);

    if (!Number.isInteger(numericYear) || numericYear <= 0) {
      setSubmitError("Please enter a valid publication year.");
      return;
    }


    setSubmitError(null);
    setSuccess(false);
    setIsSubmitting(true);

    try {
      await updateBook(bookId, {
        title: title.trim(),
        author: author.trim(),
        category: category.trim(),
        year: numericYear,
        available,
      });

      setSuccess(true);
      onBookUpdated?.();
    } catch {
      setSubmitError("Could not update the book. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <p className="form-status">Loading book details...</p>;
  }

  if (loadError) {
    return (
      <div className="book-form">
        <p className="form-error" role="alert">{loadError}</p>
        <div className="form-actions">
          <button type="button" className="btn-secondary" onClick={onCancel}>
            Back to Books
          </button>
        </div>
      </div>
    );
  }

  return (
    <form className="book-form" onSubmit={handleSubmit}>
      <div className="book-form-header">
        <h2>Edit Book</h2>
        <p>Update the details below and save your changes.</p>
      </div>

      <div className="form-field">
        <label htmlFor="edit-title">Title</label>
        <input
          id="edit-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="edit-author">Author</label>
        <input
          id="edit-author"
          type="text"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="edit-category">Category</label>
        <input
          id="edit-category"
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="edit-year">Year</label>
        <input
          id="edit-year"
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field form-field-checkbox">
        <input
          id="edit-available"
          type="checkbox"
          checked={available}
          onChange={(e) => setAvailable(e.target.checked)}
          disabled={isSubmitting}
        />
        <label htmlFor="edit-available">Available</label>
      </div>

      {submitError && <p className="form-error" role="alert">{submitError}</p>}
      {success && <p className="form-success" role="status">Book updated successfully!</p>}

      <div className="form-actions">
        <button
          type="button"
          className="btn-secondary"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </button>
        <button type="submit" className="btn-primary" disabled={isSubmitting}>
          {isSubmitting ? "Saving..." : "Save Changes"}
        </button>
      </div>
    </form>
  );
}