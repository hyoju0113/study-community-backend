from .post_router import router as post_router
from .comment_router import router as comment_router
from .auth_router import router as auth_router
from .rooms import router as rooms_router
from .reservations import router as reservations_router
from .admin import router as admin_router

__all__ = ["post_router", "comment_router", "auth_router", "rooms_router", "reservations_router", "admin_router"]
