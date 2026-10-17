import { useParams, useNavigate } from "react-router-dom";
import BookDetails from "../components/BookDetails";

export default function BookDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  return (
    <BookDetails
      key={bookId}
      bookId={bookId}
      onBack={() => navigate("/books")}
      onEdit={() => navigate(`/books/${id}/edit`)}
    />
  );
}