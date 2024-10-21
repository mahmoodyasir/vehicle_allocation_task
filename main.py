from fastapi import FastAPI
from database import mongodb
from setup import setup

app = FastAPI()
setup(app)

@app.on_event("startup")
async def startup():
  await mongodb.init(False)


@app.on_event("shutdown")
async def shutdown():
  await mongodb.close()