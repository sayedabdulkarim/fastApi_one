from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List

app = FastAPI()

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.todo_db
collection = db.todo_collection

class TodoItem(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: str
    description: str
    completed: bool = False

@app.post("/todos/", response_model=TodoItem)
async def create_todo_item(todo: TodoItem):
    result = await collection.insert_one(todo.dict(by_alias=True))
    if result.inserted_id:
        return todo
    raise HTTPException(status_code=400, detail="Failed to create todo item")

@app.get("/todos/", response_model=List[TodoItem])
async def get_todo_items():
    todos = await collection.find().to_list(1000)
    return todos

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo_item(todo_id: str):
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    if todo:
        return todo
    raise HTTPException(status_code=404, detail="Todo item not found")

@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo_item(todo_id: str, todo: TodoItem):
    result = await collection.update_one({"_id": ObjectId(todo_id)}, {"$set": todo.dict(by_alias=True)})
    if result.modified_count:
        return todo
    raise HTTPException(status_code=400, detail="Failed to update todo item")

@app.delete("/todos/{todo_id}")
async def delete_todo_item(todo_id: str):
    result = await collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count:
        return {"message": "Todo item deleted"}
    raise HTTPException(status_code=404, detail="Todo item not found")