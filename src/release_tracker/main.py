from fastapi import FastAPI

app = FastAPI(title="Release Tracker", description="API for tracking software releases", version="1.0.0")

@app.get("/projects")
def list_projects() -> list[dict]:
    return [
        {"id": 1, "name": "Project A", "version": "1.0.0"},
        {"id": 2, "name": "Project B", "version": "2.1.0"},
        {"id": 3, "name": "Project C", "version": "3.0.5"},
    ]