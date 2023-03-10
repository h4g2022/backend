from enum import Enum
from typing import List,  Union
from uuid import UUID

from pydantic import BaseModel
from pydantic.networks import EmailStr


class JobTypeEnum(str, Enum):
    full_time = "Full-time"
    part_time = "Part-time"
    contract = "Contract"


class JobModeEnum(str, Enum):
    on_site = "On-site"
    hybrid = "Hybrid"
    remote = "Remote"


class TalentBaseSchema(BaseModel):
    name: str
    story: str
    job_types: List[JobTypeEnum]
    job_modes: List[JobModeEnum]
    job_title: str
    skills: List[str]
    availability: List[int]
    is_displayed: bool
    linkedin_url: str


class TalentSchema(TalentBaseSchema):
    talent_id: int
    photo_url: str


class TalentDetailSchema(TalentSchema):
    email: EmailStr
    center_location: str
    weekly_hours: int
    treatment_type: str


class TalentEditSchema(TalentBaseSchema):
    photo_id: Union[str, UUID]
    center_location: str
    weekly_hours: int
    treatment_type: str


class TalentFullSchema(TalentBaseSchema):
    photo_url: str
    center_location: str
    weekly_hours: int
    treatment_type: str
