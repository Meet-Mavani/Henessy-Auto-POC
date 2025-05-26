## session class use to add data in table
from models import User,Comment
from sqlalchemy.orm import Session
from connect import engine
from main import session


user1=User(
    username="Meet",
    email_address="meet@crest.com",
    comments=[
        Comment(text="hello Meet"),
        Comment(text="This is Meet")
    ]
)

user2=User(
    username="Meet1",
    email_address="meet1@crest.com",
    comments=[
        Comment(text="hello Meet1"),
        Comment(text="This is Meet1")
    ]
)

user3=User(
    username="Meet2",
    email_address="meet2@crest.com",
    comments=[
        Comment(text="hello Meet2"),
        Comment(text="This is Meet2")
    ]
)

session.add_all([user1,user2,user3])

session.commit()    