from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .api import api_router

app = FastAPI(title="CourseAlign API", version="0.1.0")
app.include_router(api_router)


@app.exception_handler(FileNotFoundError)
async def data_file_missing(_: Request, __: FileNotFoundError):
    return JSONResponse(status_code=503, content={"detail": "Course data unavailable"})


@app.exception_handler(Exception)
async def unhandled(_: Request, __: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/health")
def health():
    return {"status": "ok"}
