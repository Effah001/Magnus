from magnus import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)


    def __repr__(self):
        """
        String representation of the user class
        """
        user_string = "User({}, {}, {}, {}, {})"
        return user_string.format(self.id, self.username, self.password,
                                  self.email, self.created_at)
