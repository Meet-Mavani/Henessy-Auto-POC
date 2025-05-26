from sqlalchemy.orm import Session
from connect import engine

# Create a session factory instead of a global session
session = Session(bind=engine)