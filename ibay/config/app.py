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

from ibay.config.lifetime import register_startup_event, register_shutdown_event


def get_project_data() -> dict:
    pyproject_path = pathlib.Path("ibay/pyproject.toml")
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
    init_validation_handler(app=app_)
    # app_.exception_handler(DefaultHTTPException)
    register_startup_event(app_)
    register_shutdown_event(app_)

    # app_.mount("/static", StaticFiles(directory="base_api/static"), name="static")
    # app_.include_router(router)
    # app_.include_router(auth_router)
    # app_.include_router(profile_router)
    # app_.include_router(chat_router)
    # app_.include_router(wallets_router)
    # app_.include_router(front_ibay_router)
    return app_


app = get_application()


