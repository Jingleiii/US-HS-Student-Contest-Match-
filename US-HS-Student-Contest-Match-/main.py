from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from Comparematch.loader import load_competitions_from_csv
from Comparematch.model import StudentProfile
from Comparematch.scoring import recommend

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "competitions_seed.csv"

TEMPLATES_DIR = BASE_DIR / "Web" / "main"

STATIC_DIR = BASE_DIR / "Web" / "style"

app = FastAPI(title="US HS Student Contest Match")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

competitions = load_competitions_from_csv(str(DATA_PATH))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/recommend", response_class=HTMLResponse)
def do_recommend(
    request: Request,
    grade: int = Form(...),
    academic_strength: int = Form(3),
    weekly_hours: float = Form(4.0),
    target_tier: str = Form("any"),
    interests: str = Form(""),
    prefer_online: str = Form("any"),   # any/online/offline
    prefer_team: str = Form("any"),     # any/team/individual
    topk: int = Form(8),
):
    prefer_online_map: dict[str, Optional[bool]] = {"any": None, "online": True, "offline": False}
    prefer_team_map: dict[str, Optional[bool]] = {"any": None, "team": True, "individual": False}

    interests_list = [x.strip() for x in interests.split(",") if x.strip()]

    profile = StudentProfile(
        grade=grade,
        academic_strength=academic_strength,
        interests=interests_list,
        weekly_hours=weekly_hours,
        target_tier=target_tier,
        prefer_online=prefer_online_map.get(prefer_online, None),
        prefer_team=prefer_team_map.get(prefer_team, None),
    )

    recs = recommend(profile, competitions, topk=topk)

    return templates.TemplateResponse(
        "results.html",
        {"request": request, "profile": profile, "recs": recs},
    )

from fastapi.responses import RedirectResponse

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return RedirectResponse(url="/static/favicon.ico")
