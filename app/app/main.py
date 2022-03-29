import logging
import os
from typing import List

import uvicorn
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from context import ContextLoader
from fastapi import FastAPI

from prediction_service import PredictionService

logging.getLogger().addHandler(logging.StreamHandler())

description = """
Give Me The Odds API lets you get the odds of successfully reaching the destination planet.
You can read more about the challenge [here](https://github.com/dataiku/millenium-falcon-challenge).
"""

app = FastAPI(
    title="Give Me The Odds",
    description=description
)


@app.on_event("startup")
def get_prediction_service():
    mission_details_file_path: str = os.path.abspath("./default_inputs/millennium-falcon.json")
    mission_details = ContextLoader.load_mission_details(file_path=mission_details_file_path)
    logging.info("Finished loading mission details...")
    return PredictionService(mission_details=mission_details)


prediction_service: PredictionService = get_prediction_service()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url=f"/docs/", status_code=303)


class InterceptedDataModel(BaseModel):
    countdown: int
    bounty_hunters: List[dict] = []


@app.post("/v1/mission-success/")
async def mission_calculate(item: InterceptedDataModel):
    intercepted_data_raw = jsonable_encoder(item)
    logging.info(f"Intercepted raw data: {intercepted_data_raw}")
    intercepted_data = ContextLoader.load_intercepted_data(raw_intercepted_data=intercepted_data_raw)
    return prediction_service.get_probability_of_success(countdown=intercepted_data.countdown,
                                                         hunter_schedule=intercepted_data.bounty_hunter_schedule)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
