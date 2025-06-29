from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import models
import auth
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    # Create database engine
    engine = create_engine(os.getenv("DATABASE_URL"))
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            # Create admin user
            admin_user = models.User(
                email="admin@example.com",
                username="admin",
                hashed_password=auth.get_password_hash("admin123"),  # Change this password in production
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization completed!") 