from enum import Enum
from typing import List

from pydantic import BaseModel


class JobTypeEnum(str, Enum):
    full_time = "Full-time"
    part_time = "Part-time"
    contract = "Contract"


class JobModeEnum(str, Enum):
    on_site = "On-site"
    hybrid = "Hybrid"
    remote = "Remote"


class TalentBaseSchema(BaseModel):
    story: str
    job_types: List[JobTypeEnum]
    job_modes: List[JobModeEnum]
    job_title: str
    skills: List[str]
    availability: List[int]
    photo_url: str
    is_displayed: bool
    linkedin_url: str


class TalentSchema(TalentBaseSchema):
    talent_id: int


class TalentDetailSchema(TalentSchema):
    center_location: str
    weekly_hours: int
    treatment_type: str
