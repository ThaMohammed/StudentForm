-- Create the database
CREATE DATABASE student_registration;

-- Connect to the database
\c student_registration;

-- Create sequences for IDs
CREATE SEQUENCE IF NOT EXISTS user_id_seq;
CREATE SEQUENCE IF NOT EXISTS registration_id_seq;

-- Note: The tables will be created by SQLAlchemy when the application starts
-- This script only creates the database 