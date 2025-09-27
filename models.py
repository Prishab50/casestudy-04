from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator, root_validator
import hashlib 

def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

class SurveySubmission(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    user_agent: Optional[str] = Field(None, max_length=1000)
    email: EmailStr
    age: int = Field(..., ge=13, le=120)
    consent: bool = Field(..., description="Must be true to accept")
    rating: int = Field(..., ge=1, le=5)
    comments: Optional[str] = Field(None, max_length=1000)
    submission_id: Optional[str] = Field(None, max_length=1000)

    @validator("comments")
    def _strip_comments(cls, v):
        return v.strip() if isinstance(v, str) else v

    @validator("consent")
    def _must_consent(cls, v):
        if v is not True:
            raise ValueError("consent must be true")
        return v
    
    @root_validator(pre=True)
    def generate_submission_id(cls, values):
        if "submission_id" not in values or not values["submission_id"]:
            email = values.get("email", "")
            timestamp = str(datetime)
            values["submission_id"] = sha256(email + timestamp)
        return values
        
#Good example of inheritance
class StoredSurveyRecord(BaseModel):
    name: str
    user_agent: Optional[str] = None
    hashed_email: str
    hashed_age: str
    consent: bool
    rating: int
    comments: Optional[str] = None
    submission_id: str
    received_at: datetime
    ip: str