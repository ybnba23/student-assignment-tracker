from fastapi import FastAPI

from assignment_tracker.interface.api.routers.health import HealthRouter
from assignment_tracker.interface.api.routers.v1 import router

app = FastAPI(title="Student Assignment Tracker")
app.include_router(HealthRouter)
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("assignment_tracker.app:app", host="localhost", port=8000, reload=True)
