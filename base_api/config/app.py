# -*- coding: utf-8 -*-
import pathlib
from typing import List
import toml
from fastapi import FastAPI
from fastapi_helper import DefaultHTTPException
from fastapi_helper.exceptions.validation_exceptions import init_validation_handler
from pydantic import ValidationError
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from base_api.apps.frontend.auth import auth_router
from base_api.apps.frontend.chat import chat_router
from base_api.apps.frontend.ibay import front_ibay_router
from base_api.apps.frontend.user_profile import profile_router
from base_api.apps.frontend.wallets import wallets_router
from base_api.config.celery_utils import create_celery
from base_api.config.lifetime import register_shutdown_event, register_startup_event
from base_api.config.router import router


def get_project_data() -> dict:
    pyproject_path = pathlib.Path("base_api/pyproject.toml")
    pyproject_data = toml.load(pyproject_path.open())
    poetry_data = pyproject_data["tool"]["poetry"]
    return poetry_data


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        # Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def get_application() -> FastAPI:
    poetry_data = get_project_data()
    app_ = FastAPI(
        title=poetry_data["name"],
        description=poetry_data["description"],
        version=poetry_data["version"],
        docs_url="/docs",
        redoc_url="/redoc",
        # middleware=make_middleware(),
        # openapi_tags=metadata_tags
    )
    app_.celery_app = create_celery()
    init_validation_handler(app=app_)

    register_startup_event(app_)
    register_shutdown_event(app_)

    app_.mount("/static", StaticFiles(directory="base_api/static"), name="static")
    app_.include_router(router)
    app_.include_router(auth_router)
    app_.include_router(profile_router)
    app_.include_router(chat_router)
    app_.include_router(wallets_router)
    app_.include_router(front_ibay_router)
    return app_


app = get_application()

celery = app.celery_app


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    errors = []
    for each in exc.errors():
        result = {
            "code": "validation-error",
            "type": each.get("type"),
            "field": each.get("loc")[0],
            "message": each.get("msg"),
        }
        errors.append(result)

    return JSONResponse({"detail": errors}, status_code=422)


@app.exception_handler(DefaultHTTPException)
async def backend_validation_handler(request: Request, exc: DefaultHTTPException) -> JSONResponse:
    content = {
        "code": exc.code,
        "type": exc.type,
        "message": exc.message,
        "field": getattr(exc, "field", '')
    }
    return JSONResponse(
        {"detail": [content]},
        status_code=exc.status_code,
    )
