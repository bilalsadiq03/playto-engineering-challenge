import { useEffect, useState } from "react";
import Feed from "./components/Feed";
import Leaderboard from "./components/Leaderboard";
import Login from "./components/Login";
import { apiGet } from "./api/client";

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUser = async () => {
    try {
      const data = await apiGet("/me/");
      setUser(data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  if (loading) return null;

  if (!user) {
    return <Login onLogin={fetchUser} />;
  }

  return (
    <div className="max-w-4xl mx-auto p-6 grid grid-cols-3 gap-6">
      <div className="col-span-2">
        <Feed />
      </div>
      <div>
        <Leaderboard />
      </div>
    </div>
  );
}
