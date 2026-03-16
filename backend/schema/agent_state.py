from typing import Annotated
from typing import TypedDict,List
from langchain_core.messages import BaseMessage,HumanMessage,AIMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage],add_messages]
    code: Annotated[List[str],add_messages]
    syntax_valid: bool
    syntax_err: str
    execution: bool
    execution_err: str
    video_path: str
    file_name: str
    fix_attempts: int