from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel

# https://www.youtube.com/watch?v=-ykeT6kk4bk&ab_channel=TechWithTim


class Branch(BaseModel):
    id: int
    name: str
    full_adress: str
    city: str
    employees: int
    manager: str
    working_hours: str
    car_park_capacity: int
    estabilishment_date: str
    close_date: str


app = FastAPI()

initial_branches = {
    1: {
        "id": 1,
        "name": "Warszawa 112",
        "full_adress": "Jerozolimskie 200, 02-486 Warszawa",
        "city": "Warszawa",
        "employees": 35,
        "manager": "Alexander McKwacz",
        "working_hours": "08:00 - 21:00",
        "car_park_capacity": 45,
        "estabilishment_date": "2015-03-03",
        "close_date": "",
    },
    2: {
        "id": 2,
        "name": "Warszawa 113",
        "full_adress": "Jana Rosoła 65, 02-786 Warszawa",
        "city": "Warszawa",
        "employees": 25,
        "manager": "Tomasz Sznycel",
        "working_hours": "09:00 - 17:00",
        "car_park_capacity": 20,
        "estabilishment_date": "2016-03-03",
        "close_date": "",
    },
    3: {
        "id": 3,
        "name": "Kraków 214",
        "full_adress": "Kazimierza Wielkiego 33, 30-074 Kraków",
        "city": "Kraków",
        "employees": 10,
        "manager": "Mieczysław Stonoga",
        "working_hours": "09:00 - 17:00",
        "car_park_capacity": 10,
        "estabilishment_date": "2019-01-01",
        "close_date": "",
    },
    4: {
        "id": 4,
        "name": "Wrocław 301",
        "full_adress": "Sucha 1, 50-086 Wrocław",
        "city": "Wrocław",
        "employees": 10,
        "manager": "Tytus Atomowy",
        "working_hours": "10:00 - 18:00",
        "car_park_capacity": 5,
        "estabilishment_date": "2020-01-01",
        "close_date": "",
    },
}

branches = {branch_id: Branch(**data) for branch_id, data in initial_branches.items()}


@app.get("/get_branch/{branch_id}")
def get_branch(
    branch_id: int = Path(description="ID of branch you would like to view"),
):
    return branches[branch_id]


@app.get("/get_manager_branch")
def get_manager_branch(manager: str = None):
    for id in branches:
        if branches[id].manager == manager:
            return {"id": branches[id].id, "name": branches[id].name}
    raise HTTPException(status_code=404, detail="Manager not found")


@app.post("/create_branch/{branch_id}")
def create_branch(branch_id: int, branch: Branch):
    if branch_id in branches:
        raise HTTPException(status_code=400, detail="Branch_id already exists")

    branches[branch_id] = branch
    return branches[branch_id]


@app.put("/close_branch/{branch_id}/{close_date}")
def close_branch(branch_id: int, close_date: str, branch: Branch):
    if branch_id not in branches:
        raise HTTPException(status_code=404, detail="Branch not found")

    if branch.close_date != None:
        branches[branch_id].close_date = branch.close_date


@app.delete("/delete_branch/{branch_id}")
def delete_branch(branch_id: int):
    if branch_id not in branches:
        raise HTTPException(status_code=404, detail="Branch not found")

    del branches[branch_id]
