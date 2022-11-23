# Importing FastApi modules
from fastapi import FastAPI

# Importing Routers
from controllers.items import main as r_items
from controllers.users import main as r_users

# Initializing the application
app = FastAPI(
    docs_url = "/api/v1/docs",
    redoc_url = "/api/v1/redocs",
    title = "My API",
    description = "My super simple api",
    version = "1.0",
    openapi_url = "/api/v1/openapi.json"
)

# Including the items router
app.include_router(r_items.router)
# Including the users router
app.include_router(r_users.router)