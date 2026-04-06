from .post_router import router as post_router
from .comment_router import router as comment_router
from .auth_router import router as auth_router

__all__ = ["post_router", "comment_router", "auth_router"]
