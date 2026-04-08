from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import CommentCreate, CommentResponse
from ..repositories import PostRepository, CommentRepository
from ..services import CommentService
from ..auth import get_current_user

router = APIRouter(prefix="/api", tags=["comments"])


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(PostRepository(db), CommentRepository(db))


@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
def list_comments(
    post_id: str,
    service: CommentService = Depends(get_comment_service),
):
    comments = service.get_comments(post_id)
    return [
        CommentResponse(
            id=c.id,
            content=c.content,
            author=c.author,
            createdAt=c.created_at,
        )
        for c in comments
    ]


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
    post_id: str,
    data: CommentCreate,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    comment = service.create_comment(post_id, data, author=current_user.username)
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        author=comment.author,
        createdAt=comment.created_at,
    )


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: str,
    service: CommentService = Depends(get_comment_service),
    current_user: User = Depends(get_current_user),
):
    comment = service.comment_repo.find_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
    if comment.author != current_user.username:
        raise HTTPException(status_code=403, detail="본인이 작성한 댓글만 삭제할 수 있습니다.")
    service.delete_comment(comment_id)
    return {"message": "댓글이 삭제되었습니다."}
