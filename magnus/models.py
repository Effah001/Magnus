from magnus import db, login_manager
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_active = db.Column(db.Boolean(), default=True)

    def __repr__(self):
        """
        String representation of the user class
        """
        user_string = "User({}, {}, {}, {}, {})"
        return user_string.format(self.id, self.username, self.password,
                                  self.email, self.created_at)


# Define the user loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
