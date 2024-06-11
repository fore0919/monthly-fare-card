from pydantic import BaseModel


class CoordinateSchema(BaseModel):
    start_lng: float
    start_lat: float
    end_lng: float
    end_lat: float
