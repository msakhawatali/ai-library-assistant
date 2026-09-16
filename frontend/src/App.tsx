import Header from "./components/Header";
import Chat from "./components/Chat";
import Books from "./components/Books";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Books />
        <Chat />
      </main>
    </div>
  );
}

export default App;