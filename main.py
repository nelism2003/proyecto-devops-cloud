from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Inicialización de la aplicación
app = FastAPI(
    title="Mi Aplicación DevOps - API de Tareas",
    description="API REST funcional con operaciones CRUD integradas y almacenamiento en memoria.",
    version="1.0.0"
)

class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

# Base de datos ficticia en memoria efímero
tasks_db: List[Task] = [
    Task(id=1, title="Configurar VPC", description="Establecer subredes y security groups en AWS", completed=True),
    Task(id=2, title="Crear Dockerfile", description="Escribir manifiesto para contenedorizar FastAPI", completed=True),
    Task(id=3, title="Verificar Pipeline", description="Validar la automatización de CI/CD en Render", completed=False)
]

# Bienvenida
@app.get("/", tags=["General"])
def read_root():
    return {
        "status": "Online",
        "proyecto": "Ecosistema DevOps Completo",
        "mensaje": "¡Bienvenido a la API REST corriendo en un contenedor Docker!"
    }

# Obtener las tareas
@app.get("/tasks", response_model=List[Task], tags=["Tareas"])
def get_tasks():
    return tasks_db

# Agregar una nueva tarea
@app.post("/tasks", response_model=Task, tags=["Tareas"], status_code=201)
def create_task(task: Task):
    # Validar si el ID ya existe para evitar duplicados
    for t in tasks_db:
        if t.id == task.id:
            raise HTTPException(status_code=400, detail="El ID de la tarea ya existe.")
    tasks_db.append(task)
    return task

# Actualizar el estado de una tarea
@app.put("/tasks/{task_id}", response_model=Task, tags=["Tareas"])
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db[index] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Tarea no encontrada.")

# Eliminar una tarea
@app.delete("/tasks/{task_id}", tags=["Tareas"])
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task.id == task_id:
            tasks_db.pop(index)
            return {"message": f"Tarea con ID {task_id} eliminada exitosamente."}
    raise HTTPException(status_code=404, detail="Tarea no encontrada.")