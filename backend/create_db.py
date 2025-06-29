import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv
import getpass

load_dotenv()

def create_database():
    # Get PostgreSQL password
    print("Please enter your PostgreSQL password:")
    password = getpass.getpass()
    
    # Connect to PostgreSQL server
    try:
        conn = psycopg2.connect(
            user="postgres",
            password=password,
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Create a cursor
        cur = conn.cursor()
        
        try:
            # Create database
            cur.execute("CREATE DATABASE student_registration")
            print("Database 'student_registration' created successfully!")
            
            # Close the connection to the default database
            cur.close()
            conn.close()
            
            # Connect to the new database
            conn = psycopg2.connect(
                user="postgres",
                password=password,
                host="localhost",
                port="5432",
                database="student_registration"
            )
            cur = conn.cursor()
            
            # Create sequences
            cur.execute("CREATE SEQUENCE IF NOT EXISTS user_id_seq")
            cur.execute("CREATE SEQUENCE IF NOT EXISTS registration_id_seq")
            print("Sequences created successfully!")
            
            # Update .env file with the correct password
            env_content = f"""DATABASE_URL=postgresql://postgres:{password}@localhost/student_registration
SECRET_KEY=your-super-secret-key-here"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            print(".env file updated with database connection details!")
            
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()
            
    except psycopg2.OperationalError as e:
        print("\nError: Could not connect to PostgreSQL. Please make sure:")
        print("1. PostgreSQL is installed on your system")
        print("2. PostgreSQL service is running")
        print("3. The password you entered is correct")
        print("\nDetailed error:", str(e))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("Creating database and sequences...")
    create_database()
    print("Database setup completed!") 