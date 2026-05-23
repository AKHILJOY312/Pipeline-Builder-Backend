from fastapi import FastAPI, Form, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


# Root Route
@app.get("/")
def read_root():
    return {"Ping": "Pong"}


# Parse Pipeline Route
@app.post("/pipelines/parse")
def parse_pipeline(
    pipeline: str = Form(...)
):
    
    # Manual Validation
    if len(pipeline.strip()) < 3:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Pipeline must contain at least 3 characters"
            }
        )

    return {
        "success": True,
        "status": "parsed",
        "pipeline": pipeline
    }


# Global Validation Error Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": exc.errors()
        }
    )


# Route Not Found Handler
@app.exception_handler(404)
async def not_found_handler(
    request: Request,
    exc: StarletteHTTPException
):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Route not found"
        }
    )


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error"
        }
    )