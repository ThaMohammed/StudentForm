from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import auth
from database import engine, get_db
import pandas as pd
from datetime import datetime, timedelta
from fastapi.responses import FileResponse
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Registration API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to create users")
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/registrations/", response_model=schemas.StudentRegistration)
def create_registration(
    registration: schemas.StudentRegistrationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_registration = models.StudentRegistration(
        **registration.dict(),
        user_id=current_user.id,
        status="pending"
    )
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration

@app.get("/registrations/", response_model=List[schemas.StudentRegistration])
def get_registrations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.is_admin:
        registrations = db.query(models.StudentRegistration).offset(skip).limit(limit).all()
    else:
        registrations = db.query(models.StudentRegistration).filter(
            models.StudentRegistration.user_id == current_user.id
        ).offset(skip).limit(limit).all()
    return registrations

@app.get("/registrations/{registration_id}", response_model=schemas.StudentRegistration)
def get_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    registration = db.query(models.StudentRegistration).filter(models.StudentRegistration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    if not current_user.is_admin and registration.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this registration")
    return registration

@app.put("/registrations/{registration_id}", response_model=schemas.StudentRegistration)
def update_registration(
    registration_id: int,
    registration: schemas.StudentRegistrationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_registration = db.query(models.StudentRegistration).filter(models.StudentRegistration.id == registration_id).first()
    if not db_registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    if not current_user.is_admin and db_registration.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this registration")
    
    for key, value in registration.dict().items():
        setattr(db_registration, key, value)
    
    db.commit()
    db.refresh(db_registration)
    return db_registration

@app.delete("/registrations/{registration_id}")
def delete_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_registration = db.query(models.StudentRegistration).filter(models.StudentRegistration.id == registration_id).first()
    if not db_registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    if not current_user.is_admin and db_registration.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this registration")
    
    db.delete(db_registration)
    db.commit()
    return {"message": "Registration deleted successfully"}

@app.get("/export/registrations")
def export_registrations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can export registrations")
    
    # Get registrations ordered by first name and last name
    registrations = db.query(models.StudentRegistration).order_by(
        models.StudentRegistration.first_name,
        models.StudentRegistration.last_name
    ).all()
    
    data = []
    for reg in registrations:
        data.append({
            "First Name": reg.first_name,
            "Last Name": reg.last_name,
            "Email": reg.email,
            "Phone": reg.phone,
            "Date of Birth": reg.date_of_birth,
            "Gender": reg.gender,
            "Address": f"{reg.address_line1}, {reg.address_line2 if reg.address_line2 else ''}",
            "City": reg.city,
            "State": reg.state,
            "Postal Code": reg.postal_code,
            "Country": reg.country,
            "Education": reg.highest_education,
            "Institution": reg.institution_name,
            "Graduation Year": reg.graduation_year,
            "Current Occupation": reg.current_occupation,
            "Years of Experience": reg.years_of_experience,
            "Previous Company": reg.previous_company,
            "Course": reg.course_name,
            "Course Duration": reg.course_duration,
            "Preferred Batch": reg.preferred_batch_timing,
            "Start Date": reg.preferred_start_date,
            "Registration Date": reg.registration_date,
            "Status": reg.status,
            "Previous Programming Experience": "Yes" if reg.previous_programming_experience else "No",
            "Programming Languages": reg.programming_languages_known,
            "How did you hear": reg.how_did_you_hear,
            "Expectations": reg.expectations,
            "Notes": reg.notes
        })
    
    df = pd.DataFrame(data)
    filename = f"registrations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    
    return FileResponse(
        filename,
        media_type="text/csv",
        filename=filename
    ) 