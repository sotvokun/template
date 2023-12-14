from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Do something on startup here
    yield
    # Do something on shutdown here
    pass

app = FastAPI(
    lifespan=lifespan,
)
