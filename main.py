from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List
import mysql.connector # type: ignore
from mysql.connector import Error # type: ignore
from passlib.context import CryptContext # type: ignore
from datetime import date

# FastAPI setup
app = FastAPI(
    title="Task Manager API",
    description="A simple CRUD API for managing tasks with MySQL backend",
    version="1.0.0"
)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="task_manager"
        )
        return connection
    except Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {e}"
        )

# Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    user_id: int
    username: str
    email: str
    created_at: str

class TaskCreate(BaseModel):
    title: str
    description: str = None
    status: str = "pending"
    priority: str = "medium"
    due_date: date = None

class TaskResponse(TaskCreate):
    task_id: int
    user_id: int
    created_at: str
    updated_at: str

# CRUD Operations

# User Operations
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: mysql.connector = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    
    # Check if username or email exists
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", 
                  (user.username, user.email))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    
    # Hash password
    hashed_password = pwd_context.hash(user.password)
    
    # Insert new user
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (user.username, user.email, hashed_password)
    )
    db.commit()
    
    # Get the created user
    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    created_user = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return created_user

# Task Operations
@app.post("/users/{user_id}/tasks/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, task: TaskCreate, db: mysql.connector = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if not cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Insert new task
    cursor.execute(
        """INSERT INTO tasks 
        (user_id, title, description, status, priority, due_date) 
        VALUES (%s, %s, %s, %s, %s, %s)""",
        (user_id, task.title, task.description, task.status, 
         task.priority, task.due_date)
    )
    db.commit()
    
    # Get the created task
    task_id = cursor.lastrowid
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    created_task = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return created_task

@app.get("/users/{user_id}/tasks/", response_model=List[TaskResponse])
def get_user_tasks(user_id: int, db: mysql.connector = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    
    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if not cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's tasks
    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return tasks

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate, db: mysql.connector = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    
    # Check if task exists
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    existing_task = cursor.fetchone()
    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update task
    cursor.execute(
        """UPDATE tasks SET 
        title = %s, 
        description = %s, 
        status = %s, 
        priority = %s, 
        due_date = %s 
        WHERE task_id = %s""",
        (task.title, task.description, task.status, 
         task.priority, task.due_date, task_id)
    )
    db.commit()
    
    # Get the updated task
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    updated_task = cursor.fetchone()
    
    cursor.close()
    db.close()
    
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: mysql.connector = Depends(get_db_connection)):
    cursor = db.cursor()
    
    # Check if task exists
    cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
    if not cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Delete task
    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    db.commit()
    
    cursor.close()
    db.close()
    
    return None