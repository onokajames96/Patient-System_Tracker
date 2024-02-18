# migrations.py

from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, DateTime
from sqlalchemy.engine import reflection
from sqlalchemy.orm import sessionmaker
# from app.models import Base, User, Patient, MedicalRecord, MedicalRecordEntry
import sqlalchemy
# app/models.py
import models
def apply_migration():
    # Database connection URI
    DB_URI = 'sqlite:///patient_system.db'
    
    # Create an engine and connect to the database
    engine = create_engine(DB_URI)
    conn = engine.connect()

    # Initialize metadata and reflection
    metadata = MetaData()
    metadata.reflect(bind=engine)
    inspector = sqlalchemy.inspect(engine)

    # Begin a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Define a list of models
    model_classes = [models.User, models.Patient, models.MedicalRecord, models.MedicalRecordEntry]

    # Iterate over the models and apply migrations
    for model_class in model_classes:
        # Access the table from the metadata
        table = model_class.__table__

        # Check if the table exists
        if table.name in inspector.get_table_names():
            # Check if 'created_at' column already exists
            if 'created_at' not in table.columns:
                # Add 'created_at' column
                created_at_column = Column('created_at', DateTime, default=datetime.utcnow)
                created_at_column.create(table)
                
            # Check if 'updated_at' column already exists
            if 'updated_at' not in table.columns:
                # Add 'updated_at' column
                updated_at_column = Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
                updated_at_column.create(table)

            print(f"Migration applied successfully to table '{table.name}'.")
        else:
            print(f"Table '{table.name}' not found. Migration aborted.")

    # Commit the transaction and close the session
    session.commit()
    session.close()

if __name__ == '__main__':
    apply_migration()
