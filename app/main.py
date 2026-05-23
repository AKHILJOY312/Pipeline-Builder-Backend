from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.pipelines import router as pipelines_router
from app.constants.routes import ROUTES
from app.core.errors import register_exception_handlers


app = FastAPI(title="Pipeline Processing Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(ROUTES.ROOT)
def read_root():
    return {"Ping": "Pong"}


app.include_router(pipelines_router)
register_exception_handlers(app)
