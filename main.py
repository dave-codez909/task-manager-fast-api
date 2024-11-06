from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, SQLModel, select
from typing import List
from db import create_db_and_tables, get_session
from models import Task

app = FastAPI(
    title="task manager",
    description="the best task manager",
    version="1.0.0"
    )


create_db_and_tables()

@app.get("/tasks/", response_model=List[Task])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    return tasks

@app.post("/tasks/", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id)
    result = session.exec(statement)
    task = result.one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

   
    task.title = task_data.title
    task.description = task_data.description
    task.status = task_data.status
    task.due_date = task_data.due_date
    task.priority = task_data.priority

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.id == task_id)
    result = session.exec(statement)
    task = result.one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": f"Task {task_id} has been deleted successfully."}