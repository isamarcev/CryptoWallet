from fastapi import FastAPI, APIRouter
from routers import router

app = FastAPI()

app.include_router(router=router)
