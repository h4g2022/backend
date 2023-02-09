from pydantic import BaseModel


class EmployerBaseSchema(BaseModel):
    company: str


class EmployerSchema(EmployerBaseSchema):
    employer_id: int
