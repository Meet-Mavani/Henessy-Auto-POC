from main import session

from models import User,Comment

from sqlalchemy import select


# statement=select(User).where(User.username.in_(['Meet2','Meet']))

# result=session.scalars(statement)
# ## return the ORM Response Generator of the filtered data so we need to tranvers through it 
# for user in result:
#     print(user)

## Another Way

users=session.query(User).all()

for user in users:
    print(user)