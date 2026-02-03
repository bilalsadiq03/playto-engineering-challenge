import { useEffect, useState } from "react";
import { apiGet } from "../api/client";
import PostCard from "./PostCard";

export default function Feed() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    apiGet("/feed/").then(setPosts);
  }, []);

  return (
    <div className="space-y-4">
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
