from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(include_in_schema=False)

# Path to app/templates relative to smartgrid/api/v1/views.py
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@router.get("/zones", response_class=HTMLResponse)
async def get_zones(request: Request):
    return templates.TemplateResponse(request=request, name="zones.html")


@router.get("/meters", response_class=HTMLResponse)
async def get_meters(request: Request):
    return templates.TemplateResponse(request=request, name="meters.html")


@router.get("/readings", response_class=HTMLResponse)
async def get_readings(request: Request):
    return templates.TemplateResponse(request=request, name="readings.html")


@router.get("/analytics", response_class=HTMLResponse)
async def get_analytics(request: Request):
    return templates.TemplateResponse(request=request, name="analytics.html")


@router.get("/reports", response_class=HTMLResponse)
async def get_reports(request: Request):
    return templates.TemplateResponse(request=request, name="reports.html")


@router.get("/alerts", response_class=HTMLResponse)
async def get_alerts(request: Request):
    return templates.TemplateResponse(request=request, name="alerts.html")
