from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class StudentRegistrationBase(BaseModel):
    # Personal Information
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    date_of_birth: date
    gender: str
    
    # Address Information
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str
    
    # Education Information
    highest_education: str
    institution_name: str
    graduation_year: Optional[int] = None
    
    # Professional Information
    current_occupation: Optional[str] = None
    years_of_experience: Optional[int] = None
    previous_company: Optional[str] = None
    
    # Course Information
    course_name: str
    course_duration: str
    preferred_batch_timing: str
    preferred_start_date: date
    
    # Additional Information
    how_did_you_hear: Optional[str] = None
    expectations: Optional[str] = None
    previous_programming_experience: bool = False
    programming_languages_known: Optional[str] = None

class StudentRegistrationCreate(StudentRegistrationBase):
    pass

class StudentRegistration(StudentRegistrationBase):
    id: int
    registration_date: datetime
    status: str
    user_id: int
    notes: Optional[str] = None

    class Config:
        from_attributes = True 