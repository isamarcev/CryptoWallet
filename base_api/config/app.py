
from fastapi import FastAPI

from base_api.config.router import router

app = FastAPI()

app.include_router(router)



