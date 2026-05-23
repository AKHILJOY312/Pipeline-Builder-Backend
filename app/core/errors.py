from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.constants.messages import API_MESSAGES
from app.constants.status_codes import HTTP_STATUS


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        return JSONResponse(
            status_code=HTTP_STATUS.UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": API_MESSAGES.VALIDATION_ERROR,
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ):
        if exc.status_code == HTTP_STATUS.NOT_FOUND:
            return JSONResponse(
                status_code=HTTP_STATUS.NOT_FOUND,
                content={
                    "success": False,
                    "message": API_MESSAGES.ROUTE_NOT_FOUND,
                },
            )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.detail if isinstance(exc.detail, str) else API_MESSAGES.HTTP_ERROR,
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=HTTP_STATUS.INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": API_MESSAGES.INTERNAL_SERVER_ERROR,
            },
        )
