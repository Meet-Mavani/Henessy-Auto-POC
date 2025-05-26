from models import Base,User,Comment
from connect import engine


print("creating the tables")
Base.metadata.create_all(bind=engine)