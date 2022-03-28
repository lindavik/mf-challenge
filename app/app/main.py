import logging
import os
from typing import List

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from app.context import ContextLoader
from app.mission import Mission
from fastapi import FastAPI

logging.getLogger().addHandler(logging.StreamHandler())

description = """
Give Me The Odds API lets you get the odds of successfully reaching the destination planet.
You can read more about the challenge [here](https://github.com/dataiku/millenium-falcon-challenge).
"""

app = FastAPI(
    title="Give Me The Odds",
    description=description
)

mission: Mission = None


@app.on_event("startup")
async def startup_event():
    mission_details_file_path: str = os.path.abspath("./../../inputs/millennium-falcon.json")
    mission_details = ContextLoader.load_mission_details(file_path=mission_details_file_path)
    mission = Mission(mission_details=mission_details)
    use_default_intercepted_data = False
    if use_default_intercepted_data:
        intercepted_data_file: str = ""  # todo populate with args
        intercepted_data = ContextLoader.load_intercepted_data_from_file(file_path=intercepted_data_file)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url=f"/docs/", status_code=303)


class InterceptedDataModel(BaseModel):
    countdown: int
    bounty_hunters: List[dict] = []


@app.post("/v1/mission-success/")
async def mission_calculate(item: InterceptedDataModel):
    intercepted_data_raw = jsonable_encoder(item)
    intercepted_data = ContextLoader.load_intercepted_data(raw_intercepted_data=intercepted_data_raw)
    return mission.get_mission_outcome(intercepted_data=intercepted_data)
