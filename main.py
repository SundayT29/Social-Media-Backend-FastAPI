from fastapi import FastAPI
from database import Base, engine
from api import router

app = FastAPI(
    title='Social Media App',
    description='Backend Social media application',
    version='0.1'
)

Base.metadata.create_all(bind=engine)
app.include_router(router)
