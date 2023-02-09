from typing import List

from pydantic import BaseModel
from app.schemas.talent import JobTypeEnum, JobModeEnum


class ListingBaseSchema(BaseModel):
    job_title: str
    job_description: str
    job_types: List[JobTypeEnum]
    job_modes: List[JobModeEnum]
    location: str


class ListingSchema(ListingBaseSchema):
    listing_id: int
    company: str
    email: str


class DeletedRows(BaseModel):
    deleted_rows: int