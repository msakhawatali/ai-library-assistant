import { BrowserRouter, Routes, Route, Navigate, Link } from "react-router-dom";
import Header from "./components/Header";
import Chat from "./components/Chat";
import BooksPage from "./pages/BooksPage";
import AddBookPage from "./pages/AddBookPage";
import BookDetailsPage from "./pages/BookDetailsPage";
import EditBookPage from "./pages/EditBookPage";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Header />
        <nav className="main-nav">
          <Link to="/chat">AI Chat</Link>
          <Link to="/books">Books</Link>
        </nav>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/chat" replace />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/books" element={<BooksPage />} />
            <Route path="/books/new" element={<AddBookPage />} />
            <Route path="/books/:id" element={<BookDetailsPage />} />
            <Route path="/books/:id/edit" element={<EditBookPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;