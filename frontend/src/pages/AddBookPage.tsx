import { useNavigate } from "react-router-dom";
import AddBookForm from "../components/AddBookForm";

export default function AddBookPage() {
  const navigate = useNavigate();

  return (
    <AddBookForm onBookAdded={() => navigate("/books")} />
  );
}