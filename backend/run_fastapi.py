import psutil

from main.config import Environments
from main.settings import current_env
from main.urls import UrlRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])

# Add all routers from apps
UrlRouter(app).add_router_from_apps()

# Running the app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    no_of_cpus = psutil.cpu_count(logical=False)
    no_of_workers = int(no_of_cpus / 2) - 1
    workers = no_of_workers if no_of_workers > 1 else 1
    print(f'Current CPU(s) found - {no_of_cpus}. Initialising no of workers - {workers}')

    # set reload to False if you want to check concurrency
    is_reload = False if current_env == Environments.PROD else True
    uvicorn.run('run_fastapi:app', host="0.0.0.0", port=9000, reload=is_reload, log_level="debug", workers=workers)
