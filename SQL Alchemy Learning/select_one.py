from main import session
from models import User
xyz=session.query(User).filter_by(
    username = 'Meet1'
).first()
print(xyz)