from main import session
from models import User,Comment

from sqlalchemy import select


statement=select(Comment).join(Comment.user).where(
    User.username=='Meet'
).where(
    Comment.text=="hello Meet"
)

res=session.scalars(statement).one()


print(res)