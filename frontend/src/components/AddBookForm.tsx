import { useState } from "react";
import { createBook } from "../services/booksApi";

interface AddBookFormProps {
  onBookAdded?: () => void;
  onCancel?: () => void;
}

export default function AddBookForm({ onBookAdded, onCancel }: AddBookFormProps) {
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [category, setCategory] = useState("");
  const [year, setYear] = useState("");
  const [available, setAvailable] = useState(true);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const resetForm = () => {
    setTitle("");
    setAuthor("");
    setCategory("");
    setYear("");
    setAvailable(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSubmitting) return;

    
    if (
      !title.trim() ||
      !author.trim() ||
      !category.trim() ||
      !year.trim()
    ) {
      setError("Please fill in all required fields.");
      return;
    }

    const numericYear = Number(year);

    if (!Number.isInteger(numericYear) || numericYear <= 0) {
      setError("Please enter a valid publication year.");
      return;
    }


    setError(null);
    setSuccess(false);
    setIsSubmitting(true);

    try {
      await createBook({
        title: title.trim(),
        author: author.trim(),
        category: category.trim(),
        year: numericYear,
        available,
      });

      setSuccess(true);
      resetForm();
      onBookAdded?.();
    } catch {
      setError("Could not add the book. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form className="book-form" onSubmit={handleSubmit}>
      <div className="book-form-header">
        <h2>Add a New Book</h2>
        <p>Fill in the details below to add a book to the library.</p>
      </div>

      <div className="form-field">
        <label htmlFor="add-title">Title</label>
        <input
          id="add-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="add-author">Author</label>
        <input
          id="add-author"
          type="text"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="add-category">Category</label>
        <input
          id="add-category"
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field">
        <label htmlFor="add-year">Year</label>
        <input
          id="add-year"
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          disabled={isSubmitting}
        />
      </div>

      <div className="form-field form-field-checkbox">
        <input
          id="add-available"
          type="checkbox"
          checked={available}
          onChange={(e) => setAvailable(e.target.checked)}
          disabled={isSubmitting}
        />
        <label htmlFor="add-available">Available</label>
      </div>

      {error && <p className="form-error" role="alert">{error}</p>}
      {success && <p className="form-success" role="status">Book added successfully!</p>}

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
          {isSubmitting ? "Adding..." : "Add Book"}
        </button>
      </div>
    </form>
  );
}