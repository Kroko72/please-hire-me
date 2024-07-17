from uuid import UUID
from db.create_table import App
from fastapi import FastAPI
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, insert, select, delete, update
from db.config import host, user, password, db_name, port
from generated_model import Example

app = FastAPI()
Base = declarative_base()
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}', future=True)

@app.post("/engine/", response_model=Example)
def save_item(item: Example):
    with engine.connect() as conn:
        statement = insert(App).values(kind=item.kind, name=item.name, version=item.version,
                                          description=item.description, json=item.model_dump_json())
        conn.execute(statement)
        conn.commit()
    return item

@app.get("/engine/{uuid}/")
def get_item(uuid: UUID):
    with engine.connect() as conn:
        statement = select(App).where(App.uuid==uuid)
        res = conn.execute(statement).fetchall()
    return res

@app.get("/engine/{uuid}/state")
def get_item_state(uuid: UUID):
    with engine.connect() as conn:
        statement = select(App.state).where(App.uuid==uuid)
        res = conn.execute(statement).fetchall()
    return res
    
@app.delete("/engine/{uuid}/")
def delete_item(uuid: UUID):
    with engine.connect() as conn:
        statement = delete(App).where(App.uuid==uuid)
        res = conn.execute(statement)
        conn.commit()
    return res
    
@app.put("/engine/{uuid}/state", response_model=str)
def update_state(uuid: UUID, state: str):
    with engine.connect() as conn:
        statement = update(App).where(App.uuid==uuid).values(state=state)
        conn.execute(statement)
        conn.commit()
    return state
    
@app.put("/engine/{uuid}/configuration", response_model=dict)
def update_configuration(uuid: UUID, configuration: dict):
    with engine.connect() as conn:
        statement = update(App).where(App.uuid==uuid).values(configuration=configuration)
        conn.execute(statement)
        conn.commit()
    return configuration
    
@app.put("/engine/{uuid}/specification", response_model=dict)
def update_configuration(uuid: UUID, specification: dict):
    with engine.connect() as conn:
        statement = update(App).where(App.uuid==uuid).values(specification=specification)
        conn.execute(statement)
        conn.commit()
    return specification

@app.put("/engine/{uuid}/settings", response_model=dict)
def update_configuration(uuid: UUID, settings: dict):
    with engine.connect() as conn:
        statement = update(App).where(App.uuid==uuid).values(settings=settings)
        conn.execute(statement)
        conn.commit()
    return settings


    