from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import engine, Base
from .routers import post_router, comment_router, auth_router
from .seed import seed_initial_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Community API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})


app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)


@app.on_event("startup")
def on_startup():
    seed_initial_data()
