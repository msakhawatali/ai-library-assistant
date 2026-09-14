export interface Book {
  id: number;
  title: string;
  author: string;
  category: string;
  year: number;
  available: boolean;
}

export interface BookCreate {
  title: string;
  author: string;
  category: string;
  year: number;
  available?: boolean;
}

export interface BookUpdate {
  title?: string;
  author?: string;
  category?: string;
  year?: number;
  available?: boolean;
}

const BOOKS_URL = "http://127.0.0.1:8000/api/books";

export async function getAllBooks(): Promise<Book[]> {
  const response = await fetch(BOOKS_URL);

  if (!response.ok) {
    throw new Error("Failed to fetch books");
  }

  return await response.json();
}

export async function getBookById(id: number): Promise<Book> {
  const response = await fetch(`${BOOKS_URL}/${id}`);

  if (!response.ok) {
    throw new Error("Failed to fetch book");
  }

  return await response.json();
}

export async function createBook(book: BookCreate): Promise<Book> {
  const response = await fetch(BOOKS_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(book),
  });

  if (!response.ok) {
    throw new Error("Failed to create book");
  }

  return await response.json();
}

export async function updateBook(
  id: number,
  book: BookUpdate
): Promise<Book> {
  const response = await fetch(`${BOOKS_URL}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(book),
  });

  if (!response.ok) {
    throw new Error("Failed to update book");
  }

  return await response.json();
}

export async function deleteBook(id: number): Promise<void> {
  const response = await fetch(`${BOOKS_URL}/${id}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete book");
  }
}