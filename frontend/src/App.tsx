import { useState } from "react";
import Header from "./components/Header";
import Chat from "./components/Chat";
import Books from "./components/Books";
import AddBookForm from "./components/AddBookForm";
import "./App.css";

function App() {
  const [refreshKey, setRefreshKey] = useState(0)

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Chat />
        <Books key={refreshKey} />
        <AddBookForm onBookAdded={() => setRefreshKey((k) => k + 1)} />
      </main>
    </div>
  );
}

export default App;