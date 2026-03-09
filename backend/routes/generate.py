from agents.graph import graph
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class UserQuery(BaseModel):
    user_query: str

@router.post("/")
async def generate(user_query:UserQuery):
    result = graph.invoke({"user_query" : user_query.user_query})
    return {
        "code": result["code"],
        "syntax_valid": result["syntax_valid"],
        "video_path": result.get("video_path", "")
    }

@router.post("/edit")
async def edit(user_query:UserQuery):
    return{
        "message": "edit feature is not available yet!!"
    }