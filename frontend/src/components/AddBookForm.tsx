import { useState } from "react";
import { createBook } from "../services/booksApi";

interface AddBookFormProps {
  onBookAdded?: () => void;
}

export default function AddBookForm({ onBookAdded }: AddBookFormProps) {
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

    if (!title.trim() || !author.trim() || !category.trim() || !year) {
      setError("Please fill in all required fields.");
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
        year: Number(year),
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
    <form className="add-book-form" onSubmit={handleSubmit}>
      <h3>Add a New Book</h3>

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
      {success && <p className="form-success">Book added successfully!</p>}

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Adding..." : "Add Book"}
      </button>
    </form>
  );
}