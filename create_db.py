from magnus import app, db
from magnus.models import User

# Create an application context
app.app_context().push()

# Create all tables
db.create_all()

print("Database tables created successfully.")
