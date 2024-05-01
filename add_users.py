from magnus import app, db
from magnus.models import User

# Function to add user data to the database
def add_user(username, password, email):
    # Create an application context
    with app.app_context():
        # Check if a user with the same username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists. Skipping...")
            return

        # Create a new user instance
        user = User(username=username, password=password, email=email)

        # Add the user to the session
        db.session.add(user)

        # Commit the session to save changes to the database
        db.session.commit()

# Add some sample users
add_user(username='john', password='password123', email='john@example.com')
add_user(username='jane', password='password456', email='jane@example.com')

print("Users added successfully.")

# Query and print all users from the database
with app.app_context():
    users = User.query.all()
    print("All users in the database:")
    for user in users:
        print(user)
