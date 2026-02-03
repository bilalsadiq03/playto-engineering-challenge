import { apiPost } from "../api/client";
import CommentTree from "./CommentTree";

export default function PostCard({ post }) {
  const likePost = async () => {
    await apiPost(`/posts/${post.id}/like/`);
    window.location.reload(); 
  };

  return (
    <div className="border p-4 rounded">
      <div className="font-semibold">{post.author}</div>
      <p>{post.content}</p>

      <div className="flex gap-4 mt-2">
        <button
          onClick={likePost}
          className="text-sm text-blue-600"
        >
          ❤️ {post.like_count}
        </button>
      </div>

      <CommentTree postId={post.id} />
    </div>
  );
}
