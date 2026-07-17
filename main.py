import alembic
from fastapi import FastAPI
from database import engine
from routers.guides import router as guide_router
from routers.categories import router as category_router
from models import Base

app = FastAPI()
app.include_router(category_router)
app.include_router(guide_router)
@app.get('/')
def read_root():
    return {'message': 'Hello Kitty'}