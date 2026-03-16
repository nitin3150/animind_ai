from pydantic import BaseModel

class UserQuery(BaseModel):
    user_query: str

class EditQuery(BaseModel):
    user_query: str
    file_name: str