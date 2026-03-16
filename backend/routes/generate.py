import os
from agents.graph import graph
from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from utils.save_code import get_tmp_dir
from schema.query import UserQuery, EditQuery

router = APIRouter()

@router.post("/")
async def generate(user_query:UserQuery):
    result = graph.invoke({"messages": [HumanMessage(content=user_query.user_query)]})
    
    code_result = result.get("code", "")
    latest_code = code_result[-1] if isinstance(code_result, list) else code_result
    
    return {
        "code": latest_code,
        "syntax_valid": result.get("syntax_valid", False),
        "video_path": result.get("video_path", ""),
        "file_name": result.get("file_name", "")
    }

@router.post("/edit")
async def edit(query:EditQuery):
    tmp_dir = os.path.join(get_tmp_dir(), "code")
    file_path = os.path.join(tmp_dir, query.file_name)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Code file not found. Ensure file_name includes the .py extension.")
        
    with open(file_path, "r") as f:
        existing_code = f.read()

    result = graph.invoke({
        "messages": [HumanMessage(content=query.user_query)],
        "code": [existing_code]
    })
    
    code_result = result.get("code", "")
    latest_code = code_result[-1] if isinstance(code_result, list) else code_result
    
    return {
        "code": latest_code,
        "syntax_valid": result.get("syntax_valid", False),
        "video_path": result.get("video_path", ""),
        "file_name": result.get("file_name", "")
    }