from fastapi import FastAPI
from routes.routes import router as crud_router

app = FastAPI()

# Include the routes
app.include_router(crud_router, tags=["CRUD Operations"])

@app.get("/")
async def root():
    return {"message": "Loan Management API is running!"}
