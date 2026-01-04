"""Test authentication functions"""
import bcrypt
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
MONGODB_URL = "mongodb+srv://dany:dany123@cluster0.jugrkro.mongodb.net/test"
client = MongoClient(MONGODB_URL)
db = client.todoapp_streamlit

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Test 1: Create a test user
print("=" * 50)
print("TEST 1: Creating test user")
print("=" * 50)

# Check if test user exists
test_user = db.users.find_one({"username": "testuser"})
if test_user:
    print("✅ Test user already exists")
    print(f"   Username: {test_user['username']}")
    print(f"   Email: {test_user['email']}")
else:
    # Create test user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": hash_password("test123"),
        "created_at": datetime.utcnow()
    }
    result = db.users.insert_one(user_data)
    print("✅ Test user created successfully!")
    print(f"   User ID: {result.inserted_id}")
    print(f"   Username: testuser")
    print(f"   Password: test123")

# Test 2: Verify password
print("\n" + "=" * 50)
print("TEST 2: Testing password verification")
print("=" * 50)

user = db.users.find_one({"username": "testuser"})
if user:
    # Test correct password
    correct = verify_password("test123", user["password"])
    print(f"✅ Correct password (test123): {correct}")
    
    # Test wrong password
    wrong = verify_password("wrongpass", user["password"])
    print(f"✅ Wrong password (wrongpass): {wrong}")
else:
    print("❌ User not found")

# Test 3: List all users
print("\n" + "=" * 50)
print("TEST 3: All users in database")
print("=" * 50)

users = list(db.users.find())
if users:
    for i, user in enumerate(users, 1):
        print(f"{i}. Username: {user['username']}, Email: {user['email']}")
else:
    print("No users found in database")

print("\n" + "=" * 50)
print("SUMMARY")
print("=" * 50)
print("You can now login with:")
print("  Username: testuser")
print("  Password: test123")
print("\nOr create a new account in the Streamlit app!")
print("=" * 50)
