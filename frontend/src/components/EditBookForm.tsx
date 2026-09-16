import { useState, useEffect } from "react";
import { getBookById, updateBook } from "../services/booksApi";

interface EditBookFormProps {
  bookId: number;
  onBookUpdated?: () => void;
}

export default function EditBookForm({ bookId, onBookUpdated }: EditBookFormProps) {
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [category, setCategory] = useState("");
  const [year, setYear] = useState("");
  const [available, setAvailable] = useState(true);

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchBook = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const book = await getBookById(bookId);
        setTitle(book.title);
        setAuthor(book.author);
        setCategory(book.category);
        setYear(String(book.year));
        setAvailable(book.available);
      } catch {
        setError("Could not load book details. Please try again.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchBook();
  }, [bookId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || !author.trim() || !category.trim() || !year) {
      setError("Please fill in all required fields.");
      return;
    }

    setError(null);
    setSuccess(false);
    setIsSubmitting(true);

    try {
      await updateBook(bookId, {
        title: title.trim(),
        author: author.trim(),
        category: category.trim(),
        year: Number(year),
        available,
      });

      setSuccess(true);
      onBookUpdated?.();
    } catch {
      setError("Could not update the book. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return <p className="form-status">Loading book details...</p>;
  }

  if (error && !title) {
    // Load hi fail ho gayi thi — form dikhane ka koi fayda nahi
    return <p className="form-error">{error}</p>;
  }

  return (
    <form className="add-book-form" onSubmit={handleSubmit}>
      <h3>Edit Book</h3>

      <label>
        Title
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          disabled={isSubmitting}
        />
      </label>

      <label>
        Author
        <input
          type="text"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          disabled={isSubmitting}
        />
      </label>

      <label>
        Category
        <input
          type="text"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          disabled={isSubmitting}
        />
      </label>

      <label>
        Year
        <input
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          disabled={isSubmitting}
        />
      </label>

      <label className="checkbox-label">
        <input
          type="checkbox"
          checked={available}
          onChange={(e) => setAvailable(e.target.checked)}
          disabled={isSubmitting}
        />
        Available
      </label>

      {error && <p className="form-error">{error}</p>}
      {success && <p className="form-success">Book updated successfully!</p>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Updating..." : "Update Book"}
      </button>
    </form>
  );
}