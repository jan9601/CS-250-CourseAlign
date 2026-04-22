from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.load_sections import load_sections
from app.api.routes import router

DATA_PATH = Path(__file__).parent.parent / "data" / "raw" / "testData.csv"


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.sections = load_sections(DATA_PATH)
    yield


app = FastAPI(title="CourseAlign API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
