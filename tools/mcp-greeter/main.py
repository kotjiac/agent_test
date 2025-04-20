import os
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel

PORT = int(os.getenv("GREETER_PORT"))

class GreetRequest(BaseModel):
    name: str

app = FastAPI()

mcp = FastApiMCP(
    app,
    name="Greeter API",
    description="A simple example API using FastAPI and FastApiMCP",
    describe_all_responses=True,
    describe_full_response_schema=True
)

@app.post("/greet", operation_id="greet_user")
async def greet(data: GreetRequest):
    return {"output": f"Hello, {data.name}! **Greetings** from Greeter API!"}

mcp.mount()
mcp.setup_server()
