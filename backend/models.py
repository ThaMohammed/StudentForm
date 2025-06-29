from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Date, Sequence
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    registrations = relationship("StudentRegistration", back_populates="user")

class StudentRegistration(Base):
    __tablename__ = "student_registrations"

    id = Column(Integer, Sequence('registration_id_seq'), primary_key=True, index=True)
    # Personal Information
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    
    # Address Information
    address_line1 = Column(String)
    address_line2 = Column(String, nullable=True)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String)
    
    # Education Information
    highest_education = Column(String)
    institution_name = Column(String)
    graduation_year = Column(Integer, nullable=True)
    
    # Professional Information
    current_occupation = Column(String, nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    previous_company = Column(String, nullable=True)
    
    # Course Information
    course_name = Column(String)
    course_duration = Column(String)
    preferred_batch_timing = Column(String)
    preferred_start_date = Column(Date)
    
    # Additional Information
    how_did_you_hear = Column(String, nullable=True)
    expectations = Column(Text, nullable=True)
    previous_programming_experience = Column(Boolean, default=False)
    programming_languages_known = Column(String, nullable=True)
    
    # Registration Details
    registration_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # e.g., "pending", "approved", "rejected"
    notes = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="registrations") 