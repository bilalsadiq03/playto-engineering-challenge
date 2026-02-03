import { useEffect, useState } from "react";
import { apiGet, apiPost } from "../api/client";

function Comment({ comment }) {
  const likeComment = async () => {
    await apiPost(`/comments/${comment.id}/like/`);
    window.location.reload();
  };

  return (
    <div className="ml-4 border-l pl-4 mt-2">
      <div className="text-sm font-medium">{comment.author}</div>
      <p className="text-sm">{comment.content}</p>

      <button
        onClick={likeComment}
        className="text-xs text-blue-600"
      >
        ❤️
      </button>

      {comment.children.map(child => (
        <Comment key={child.id} comment={child} />
      ))}
    </div>
  );
}

export default function CommentTree({ postId }) {
  const [comments, setComments] = useState([]);

  useEffect(() => {
    apiGet(`/posts/${postId}/comments/`).then(setComments);
  }, [postId]);

  return (
    <div className="mt-3">
      {comments.map(comment => (
        <Comment key={comment.id} comment={comment} />
      ))}
    </div>
  );
}
