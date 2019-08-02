from TravNo import db
from TravNo.Models import User

user = User.query.first()

print(user)