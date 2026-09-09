import Header from "./components/Header";
import Chat from "./components/Chat";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Chat />
      </main>
    </div>
  );
}

export default App;