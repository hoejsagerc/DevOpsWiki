# Importing FastApi Modules
from fastapi import FastAPI

# Importing Controllers
from routers.auth import main as r_auth

# Importing Controller Models
from routers.auth import models as auth_models

# Importing database config
from database import engine



# Initializing the application
app = FastAPI(
    docs_url = "/api/v1/docs",
    redoc_url = "/api/v1/redocs",
    title = "Shunt IOT API",
    description = "API for supporting the Shunt IOT Application by Region Nord",
    version = "1.0.0",
    openapi_url = "/api/v1/openapi.json"
)


# Initializing all the database models
auth_models.Base.metadata.create_all(bind=engine)


# Including the Controllers into the application
app.include_router(r_auth.router)