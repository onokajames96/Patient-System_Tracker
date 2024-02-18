from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, event, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_admin = Column(Boolean, default=True)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address = Column(String(255))
    phone_number = Column(String(15))
    created_at = Column(DateTime, default=datetime.utcnow)  # Automatically set when a new record is created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Automatically updated when a record is modified

    patients = relationship("Patient", back_populates="user")

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(String(255))
    phone_number = Column(String(15))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="patients")
    medical_records = relationship("MedicalRecord", back_populates="patient")

class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    date = Column(Date, nullable=False)
    doctor_name = Column(String(100), nullable=False)
    diagnosis = Column(String(255), nullable=False)
    prescription = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False)

    patient = relationship("Patient", back_populates="medical_records")
    entries = relationship("MedicalRecordEntry", back_populates="record")

class MedicalRecordEntry(Base):
    __tablename__ = '/medical_record_entry'

    id = Column(Integer, primary_key=True)
    medical_record_id = Column(Integer, ForeignKey('medical_records.id'), nullable=False)
    entry_date = Column(Date, nullable=False)
    entry_text = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False)

    record = relationship("MedicalRecord", back_populates="entries")

# Event listener to automatically update the updated_at timestamp for all models
@event.listens_for(User, 'before_update')
@event.listens_for(Patient, 'before_update')
@event.listens_for(MedicalRecord, 'before_update')
@event.listens_for(MedicalRecordEntry, 'before_update')
def before_update_listener(mapper, connection, target):
    target.updated_at = datetime.utcnow()

