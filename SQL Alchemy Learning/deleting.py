from main import session
from models import User,Comment

commit=session.query(Comment).filter_by(id=1).first()

session.delete(commit)

session.commit()