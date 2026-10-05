import { BrowserRouter, Routes, Route, Navigate, NavLink } from "react-router-dom";
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
          <NavLink
            to="/chat"
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            AI Chat
          </NavLink>
          <NavLink
            to="/books"
            className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
          >
            Books
          </NavLink>
        </nav>
        <main className="main-content">
          <div className="page-container">
          <Routes>
            <Route path="/" element={<Navigate to="/chat" replace />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/books" element={<BooksPage />} />
            <Route path="/books/new" element={<AddBookPage />} />
            <Route path="/books/:id" element={<BookDetailsPage />} />
            <Route path="/books/:id/edit" element={<EditBookPage />} />
          </Routes>
          </div>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;