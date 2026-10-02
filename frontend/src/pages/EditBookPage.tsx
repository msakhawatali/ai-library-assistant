import { useParams, useNavigate } from "react-router-dom";
import EditBookForm from "../components/EditBookForm";

export default function EditBookPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <EditBookForm
      bookId={Number(id)}
      onBookUpdated={() => navigate("/books")}
    />
  );
}