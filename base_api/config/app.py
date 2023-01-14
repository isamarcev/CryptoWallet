from fastapi import FastAPI, APIRouter
from base_api.config.routers import router

app = FastAPI()

app.include_router(router=router)
