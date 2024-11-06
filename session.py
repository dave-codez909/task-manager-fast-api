from sqlmodel import Session, select
from db import get_engine
from models import Task

def execute_task(task_id: int):
    engine = get_engine()
    with Session(engine) as session:
        
        statement = select(Task).where(Task.id == task_id)
        result = session.exec(statement)
        task_to_execute = result.one_or_none()

        if not task_to_execute:
            print(f"Task with ID {task_id} not found.")
            return

       
        task_to_execute.status = "completed"
        session.add(task_to_execute)
        session.commit()
        print(f"Task {task_id} has been marked as completed.")
