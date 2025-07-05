from fastapi import FastAPI
from app.controllers.document_controller import document_controller as document_router

app = FastAPI()

# Include the document processing routes
app.include_router(document_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Document API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)