from fastapi import FastAPI
import os

app = FastAPI(title="Mi Aplicación DevOps")

@app.get("/")
def read_root():
    return {
        "status": "Instancia funcionando",
        "entorno": "Producción en la Nube",
        "mensaje": "¡Hola Mundo! Mi infraestructura DevOps está viva."
    }

@app.get("/health")
def health_check():
    # Esto servirá más adelante para el Load Balancer y Kubernetes
    return {"status": "healthy"}
    