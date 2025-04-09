from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

# Получить все задачи
async def get_tasks(db: AsyncSession):
    result = await db.execute(select(models.Task))
    return result.scalars().all()

# Получить одну задачу по ID
async def get_task(db: AsyncSession, task_id: int):
    return await db.get(models.Task, task_id)

# Создать задачу
async def create_task(db: AsyncSession, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

# Удалить задачу
async def delete_task(db: AsyncSession, task_id: int):
    task = await db.get(models.Task, task_id)
    if task:
        await db.delete(task)
        await db.commit()
    return task
