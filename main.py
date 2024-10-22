from fastapi import FastAPI, Request
from database import mongodb
from setup import setup
from utils import utils
from dotenv import load_dotenv

app = FastAPI()
setup(app)

load_dotenv()

@app.on_event("startup")
async def startup():
  await mongodb.init(False)
  
  
@app.get("/", status_code=200)
async def initial(request: Request):
  
  current_url = str(request.url)
  
  return utils.create_response(
        status_code=200,
        success=True,
        message=f"App Running. Go to {current_url}docs"
      )


@app.on_event("shutdown")
async def shutdown():
  await mongodb.close()
  
  
