from fastapi import FastAPI
from routes.routes import router as person_router
from config.database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routes
app.include_router(person_router)
