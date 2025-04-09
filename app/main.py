from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas, crud
from .database import Base, engine, SessionLocal

app = FastAPI()

# При запуске приложения создаём таблицы
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Получение сессии БД
async def get_db():
    async with SessionLocal() as session:
        yield session

# Получить все задачи
@app.get("/tasks", response_model=list[schemas.TaskOut])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    return await crud.get_tasks(db)

# Получить одну задачу
@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Создать новую задачу
@app.post("/tasks", response_model=schemas.TaskOut)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_task(db, task)

# Удалить задачу
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Deleted"}

# Изменить задачу
@app.patch("/tasks/{task_id}", response_model=schemas.TaskOut)
async def update_task(task_id: int, data: schemas.TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.is_done = data.is_done
    await db.commit()
    await db.refresh(task)
    return task
