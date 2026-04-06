from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import PostCreate, PostResponse, PostSummary, CommentResponse
from ..repositories import PostRepository
from ..services import PostService
from ..auth import get_current_user

router = APIRouter(prefix="/api/posts", tags=["posts"])


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(PostRepository(db))


@router.get("", response_model=list[PostSummary])
def list_posts(service: PostService = Depends(get_post_service)):
    posts = service.get_all_posts()
    return [
        PostSummary(
            id=p.id,
            title=p.title,
            content=p.content,
            author=p.author,
            createdAt=p.created_at,
            likes=p.likes,
            commentCount=len(p.comments),
        )
        for p in posts
    ]


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: str, service: PostService = Depends(get_post_service)):
    post = service.get_post(post_id)
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.author,
        createdAt=post.created_at,
        likes=post.likes,
        comments=[
            CommentResponse(id=c.id, content=c.content, author=c.author, createdAt=c.created_at)
            for c in post.comments
        ],
    )


@router.post("", response_model=PostResponse, status_code=201)
def create_post(
    data: PostCreate,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    data.author = current_user.username
    post = service.create_post(data)
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.author,
        createdAt=post.created_at,
        likes=post.likes,
        comments=[],
    )


@router.delete("/{post_id}")
def delete_post(
    post_id: str,
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    post = service.get_post(post_id)
    if post.author != current_user.username:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="본인이 작성한 게시글만 삭제할 수 있습니다.")
    service.delete_post(post_id)
    return {"message": "게시글이 삭제되었습니다."}


@router.patch("/{post_id}/like", response_model=PostResponse)
def like_post(post_id: str, service: PostService = Depends(get_post_service)):
    post = service.toggle_like(post_id)
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        author=post.author,
        createdAt=post.created_at,
        likes=post.likes,
        comments=[
            CommentResponse(id=c.id, content=c.content, author=c.author, createdAt=c.created_at)
            for c in post.comments
        ],
    )
