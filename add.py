from magnus import db
from magnus.models import User

# Add a new user
user1 = User(username='john', password='password123')
db.session.add(user1)
db.session.commit()


user2 = User(username='Ama', password='password1')
db.session.add(user2)
db.session.commit()

