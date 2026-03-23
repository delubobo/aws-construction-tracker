from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import FRONTEND_ORIGINS
from app.database import engine, Base

# Import models so SQLAlchemy knows about them before create_all
import app.models  # noqa: F401

from app.routers import rfis, submittals, change_orders, ofm, vendors, dashboard, export


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="RFI & Change Order Tracker",
    description="AWS Data Center Expansion — Lubbock Region, Phase 2",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rfis.router)
app.include_router(submittals.router)
app.include_router(change_orders.router)
app.include_router(ofm.router)
app.include_router(vendors.router)
app.include_router(dashboard.router)
app.include_router(export.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "aws-construction-tracker"}
