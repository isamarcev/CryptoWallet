import pathlib
from typing import List
from fastapi import FastAPI
import toml
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from base_api.apps.frontend.auth import auth_router
from base_api.apps.frontend.chat import chat_router
from base_api.apps.frontend.user_profile import profile_router
from base_api.config.lifetime import register_startup_event, register_shutdown_event
from base_api.config.router import router


def get_project_data() -> dict:
    pyproject_path = pathlib.Path("pyproject.toml")
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

    register_startup_event(app_)
    register_shutdown_event(app_)
    app_.mount("/static", StaticFiles(directory="static"), name="static")
    app_.include_router(router)
    app_.include_router(auth_router)
    app_.include_router(profile_router)
    app_.include_router(chat_router)
    return app_


app = get_application()



