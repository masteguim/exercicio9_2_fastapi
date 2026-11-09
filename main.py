
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str

items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]


@app.get("/")
def home():
    return {"message": "API FastAPI funcionando!"}


@app.get("/items")
def get_items():
    return {"items": items}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = next(
        (item for item in items if item["id"] == item_id),
        None
    )

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {"item": item}


@app.post("/items", status_code=201)
def create_item(item: Item):
    new_item = {
        "id": max(
            (i["id"] for i in items),
            default=0
        ) + 1,
        "name": item.name
    }

    items.append(new_item)
    return new_item


@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for item in items:
        if item["id"] == item_id:
            item["name"] = updated_item.name
            return item

    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return {"message": "Item deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Item not found"
    )
