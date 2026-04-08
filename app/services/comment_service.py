from datetime import datetime, timezone

from fastapi import HTTPException

from ..models import Comment
from ..schemas import CommentCreate
from ..repositories import PostRepository, CommentRepository


class CommentService:
    def __init__(self, post_repo: PostRepository, comment_repo: CommentRepository):
        self.post_repo = post_repo
        self.comment_repo = comment_repo

    def get_comments(self, post_id: str) -> list[Comment]:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail={"error": "게시글을 찾을 수 없습니다."})
        return post.comments

    def create_comment(self, post_id: str, data: CommentCreate, author: str) -> Comment:
        post = self.post_repo.find_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail={"error": "게시글을 찾을 수 없습니다."})
        if not data.content:
            raise HTTPException(status_code=400, detail={"error": "댓글 내용은 필수입니다."})
        comment = Comment(
            id=str(int(datetime.now(timezone.utc).timestamp() * 1000)),
            content=data.content,
            author=author,
            post_id=post_id,
        )
        return self.comment_repo.save(comment)

    def delete_comment(self, comment_id: str) -> None:
        comment = self.comment_repo.find_by_id(comment_id)
        if not comment:
            raise HTTPException(status_code=404, detail={"error": "댓글을 찾을 수 없습니다."})
        self.comment_repo.delete(comment)
