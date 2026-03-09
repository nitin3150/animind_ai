from fastapi import FastAPI
from routes.generate import router

app = FastAPI()

app.include_router(router,prefix="/generate",tags=["generate"])

@app.get("/")
async def root():
    return {"message": "App is running!!"}