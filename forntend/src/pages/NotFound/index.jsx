import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-6xl font-bold">404</h1>

      <p>Page Not Found</p>

      <Link to="/">Go Home</Link>
    </main>
  );
};

export default NotFound;
