from fastapi import Depends,FastAPI,status,HTTPException,Query
from sqlalchemy.orm import Session
from database import Base,engine,get_db
import models
from schemas import TaskCreate,TaskResponse,TaskUpdate,TaskPatch
app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.get("/")
def home():
    return {"message":"Task manager API is running"}

@app.post(
    "/tasks",
    response_model = TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get("/tasks",response_model = list[TaskResponse])
def get_tasks(
    skip: int = Query(default = 0,ge= 0),
    limit: int = Query(default=20,ge=1,le=100),
    completed : bool | None = None,
    db: Session = Depends(get_db),              
):
    query = db.query(models.Task)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
    tasks = (
        query
        .order_by(models.Task.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return tasks
    
    


@app.get("/tasks/{task_id}", response_model = TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Task not found"
        )

    return task

@app.put("/tasks/{task_id}",response_model = TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate,db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Task Not found"
        )
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    task.priority = task_data.priority
    db.commit()
    db.refresh(task)

    return task

@app.patch("/tasks/{task_id}",response_model=TaskResponse)
def patch_task(task_id:int,task_data:TaskPatch,db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "task not found"
        )
    updates = task_data.model_dump(exclude_unset = True)

    for field,value  in updates.items():
        setattr(task,field,value)
    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "task not found"
        )
    db.delete(task)
    db.commit()

    return None