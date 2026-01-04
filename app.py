import streamlit as st
from datetime import datetime
import bcrypt
from pymongo import MongoClient
from bson import ObjectId
import os

# Page config
st.set_page_config(
    page_title="Todo App",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb+srv://dany:dany123@cluster0.jugrkro.mongodb.net/test")
client = MongoClient(MONGODB_URL)
db = client.todoapp_streamlit

# Custom CSS for beautiful minimal light mode design
st.markdown("""
<style>
    /* Light mode colors */
    :root {
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --bg-tertiary: #e9ecef;
        --text-primary: #1a1a1a;
        --text-secondary: #6c757d;
        --accent: #5b7cff;
        --accent-hover: #4c6aff;
        --border: #dee2e6;
        --shadow: rgba(0, 0, 0, 0.08);
        --success: #28a745;
        --error: #dc3545;
        --warning: #ffc107;
        --info: #17a2b8;
    }
    
    /* Main container - light background */
    .main {
        padding: 2rem 1rem;
        background-color: var(--bg-secondary);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Global text colors */
    .main, .main * {
        color: var(--text-primary) !important;
    }
    
    /* Input labels */
    .stTextInput label,
    .stTextArea label,
    .stCheckbox label,
    .stRadio label {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
    }
    
    /* Light mode inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid var(--border);
        padding: 0.75rem;
        font-size: 15px;
        background-color: white !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-secondary) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px rgba(91, 124, 255, 0.1) !important;
    }
    
    /* Light mode buttons */
    .stButton > button {
        width: 100%;
        background: var(--accent) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: var(--accent-hover) !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(91, 124, 255, 0.3);
    }
    
    /* Radio buttons in light mode */
    .stRadio > div {
        background-color: white;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid var(--border);
    }
    
    .stRadio > div > label {
        color: var(--text-primary) !important;
    }
    
    .stRadio > div > label > div {
        color: var(--text-primary) !important;
    }
    
    /* Checkboxes */
    .stCheckbox {
        background-color: transparent;
        padding: 0.25rem;
        border-radius: 4px;
    }
    
    .stCheckbox label {
        color: var(--text-primary) !important;
    }
    
    /* Todo item - light mode */
    .todo-item {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px var(--shadow);
    }
    
    .todo-item:hover {
        border-color: var(--accent);
        box-shadow: 0 4px 12px rgba(91, 124, 255, 0.15);
        transform: translateY(-1px);
    }
    
    .todo-item.completed {
        opacity: 0.6;
        background: var(--bg-secondary);
    }
    
    .todo-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 0.25rem;
        color: var(--text-primary) !important;
    }
    
    .todo-title.completed {
        text-decoration: line-through;
        color: var(--text-secondary) !important;
    }
    
    .todo-description {
        font-size: 14px;
        color: var(--text-secondary) !important;
    }
    
    /* Header - light mode */
    .app-header {
        text-align: center;
        margin-bottom: 2rem;
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px var(--shadow);
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--accent) !important;
        margin-bottom: 0.5rem;
    }
    
    .app-subtitle {
        color: var(--text-secondary) !important;
        font-size: 1rem;
    }
    
    /* Stats - light mode */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .stat-box {
        flex: 1;
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid var(--border);
        box-shadow: 0 2px 4px var(--shadow);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent) !important;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: var(--text-secondary) !important;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Form containers */
    div[data-testid="stForm"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border);
        box-shadow: 0 2px 8px var(--shadow);
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    /* Paragraphs */
    p {
        color: var(--text-primary) !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--border);
        opacity: 0.5;
    }
    
    /* Alert boxes */
    .stSuccess, .element-container .stSuccess {
        background-color: rgba(40, 167, 69, 0.1) !important;
        color: var(--success) !important;
        border: 1px solid var(--success);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stError, .element-container .stError {
        background-color: rgba(220, 53, 69, 0.1) !important;
        color: var(--error) !important;
        border: 1px solid var(--error);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stWarning, .element-container .stWarning {
        background-color: rgba(255, 193, 7, 0.1) !important;
        color: #856404 !important;
        border: 1px solid var(--warning);
        border-radius: 8px;
        padding: 1rem;
    }
    
    .stInfo, .element-container .stInfo {
        background-color: rgba(23, 162, 184, 0.1) !important;
        color: var(--info) !important;
        border: 1px solid var(--info);
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Markdown text */
    .markdown-text-container {
        color: var(--text-primary) !important;
    }
    
    /* Streamlit default text */
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] {
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'todos' not in st.session_state:
    st.session_state.todos = []

# Database helper functions
def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def get_user_by_username(username):
    """Get user by username"""
    return db.users.find_one({"username": username})

def get_user_by_email(email):
    """Get user by email"""
    return db.users.find_one({"email": email})

def create_user(username, email, password):
    """Create new user"""
    # Check if user exists
    if get_user_by_username(username):
        return False, "Username already exists"
    if get_user_by_email(email):
        return False, "Email already registered"
    
    # Create user
    user_data = {
        "username": username,
        "email": email,
        "password": hash_password(password),
        "created_at": datetime.utcnow()
    }
    
    try:
        result = db.users.insert_one(user_data)
        return True, str(result.inserted_id)
    except Exception as e:
        return False, str(e)

def authenticate_user(username, password):
    """Authenticate user"""
    user = get_user_by_username(username)
    if not user:
        return False, "Invalid username or password"
    
    if verify_password(password, user["password"]):
        return True, user
    return False, "Invalid username or password"

def get_user_todos(user_id):
    """Get all todos for a user"""
    todos = list(db.todos.find({"user_id": user_id}).sort("created_at", -1))
    for todo in todos:
        todo["id"] = str(todo["_id"])
    return todos

def create_todo_db(user_id, title, description=""):
    """Create new todo"""
    todo_data = {
        "user_id": user_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    try:
        result = db.todos.insert_one(todo_data)
        return True, str(result.inserted_id)
    except Exception as e:
        return False, str(e)

def update_todo_db(todo_id, user_id, **updates):
    """Update todo"""
    try:
        updates["updated_at"] = datetime.utcnow()
        result = db.todos.update_one(
            {"_id": ObjectId(todo_id), "user_id": user_id},
            {"$set": updates}
        )
        return result.modified_count > 0
    except Exception as e:
        return False

def delete_todo_db(todo_id, user_id):
    """Delete todo"""
    try:
        result = db.todos.delete_one({"_id": ObjectId(todo_id), "user_id": user_id})
        return result.deleted_count > 0
    except Exception as e:
        return False

# App helper functions
def login(username, password):
    """Login user"""
    success, result = authenticate_user(username, password)
    if success:
        st.session_state.user_id = str(result["_id"])
        st.session_state.user = {
            "username": result["username"],
            "email": result["email"]
        }
        return True, "Login successful!"
    return False, result

def signup(username, email, password):
    """Sign up new user"""
    return create_user(username, email, password)

def load_todos():
    """Load user's todos"""
    if st.session_state.user_id:
        st.session_state.todos = get_user_todos(st.session_state.user_id)
        return True
    return False

def create_todo(title, description=""):
    """Create new todo"""
    if st.session_state.user_id:
        success, _ = create_todo_db(st.session_state.user_id, title, description)
        if success:
            load_todos()
            return True
    return False

def toggle_todo(todo_id, completed):
    """Toggle todo completion"""
    if st.session_state.user_id:
        success = update_todo_db(todo_id, st.session_state.user_id, completed=not completed)
        if success:
            load_todos()
            return True
    return False

def delete_todo(todo_id):
    """Delete todo"""
    if st.session_state.user_id:
        success = delete_todo_db(todo_id, st.session_state.user_id)
        if success:
            load_todos()
            return True
    return False

# Auth Pages
def show_login():
    """Display login page"""
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="app-title">✅ Todo App</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Sign in to manage your tasks</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if username and password:
                success, message = login(username, password)
                if success:
                    st.success("✅ " + message)
                    st.rerun()
                else:
                    st.error("❌ " + message)
            else:
                st.warning("⚠️ Please fill in all fields")
    
    st.markdown("---")
    if st.button("Don't have an account? Sign up"):
        st.session_state.show_signup = True
        st.rerun()

def show_signup():
    """Display signup page"""
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    st.markdown('<h1 class="app-title">✅ Todo App</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Create your account</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        username = st.text_input("👤 Username", placeholder="Choose a username")
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not all([username, email, password, confirm_password]):
                st.warning("⚠️ Please fill in all fields")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters")
            else:
                success, result = signup(username, email, password)
                if success:
                    st.success("✅ Account created! Please login.")
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error(f"❌ {result}")
    
    st.markdown("---")
    if st.button("Already have an account? Login"):
        st.session_state.show_signup = False
        st.rerun()

def show_todos():
    """Display todo list page"""
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="app-header">', unsafe_allow_html=True)
        st.markdown('<h1 class="app-title">✅ My Todos</h1>', unsafe_allow_html=True)
        if st.session_state.user:
            st.markdown(f'<p class="app-subtitle">Welcome, {st.session_state.user["username"]}!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.user_id = None
            st.session_state.user = None
            st.session_state.todos = []
            st.rerun()
    
    # Load todos
    load_todos()
    
    # Stats
    total_todos = len(st.session_state.todos)
    completed_todos = sum(1 for todo in st.session_state.todos if todo['completed'])
    pending_todos = total_todos - completed_todos
    
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number">{total_todos}</div>
                <div class="stat-label">Total</div>
            </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number">{pending_todos}</div>
                <div class="stat-label">Pending</div>
            </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number">{completed_todos}</div>
                <div class="stat-label">Completed</div>
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add new todo
    st.markdown("### ➕ Add New Todo")
    with st.form("add_todo_form", clear_on_submit=True):
        title = st.text_input("What needs to be done?", placeholder="Enter todo title")
        description = st.text_area("Description (optional)", placeholder="Add more details...", height=100)
        submitted = st.form_submit_button("Add Todo")
        
        if submitted:
            if title.strip():
                if create_todo(title, description):
                    st.success("✅ Todo added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add todo")
            else:
                st.warning("⚠️ Please enter a title")
    
    st.markdown("---")
    # Display todos
    st.markdown("### 📋 Your Todos")
    
    if not st.session_state.todos:
        st.info("🎉 No todos yet! Start by adding one above.")
    else:
        # Filter options
        filter_option = st.radio("Filter:", ["All", "Pending", "Completed"], horizontal=True)
        
        filtered_todos = st.session_state.todos
        if filter_option == "Pending":
            filtered_todos = [t for t in st.session_state.todos if not t['completed']]
        elif filter_option == "Completed":
            filtered_todos = [t for t in st.session_state.todos if t['completed']]
        
        for todo in filtered_todos:
            completed_class = "completed" if todo['completed'] else ""
            title_class = "completed" if todo['completed'] else ""
            
            col1, col2, col3 = st.columns([0.5, 4, 1])
            
            with col1:
                checkbox = st.checkbox(
                    "",
                    value=todo['completed'],
                    key=f"check_{todo['id']}",
                    label_visibility="collapsed"
                )
                if checkbox != todo['completed']:
                    toggle_todo(todo['id'], todo['completed'])
                    st.rerun()
            
            with col2:
                st.markdown(f'''
                    <div class="todo-item {completed_class}">
                        <div class="todo-title {title_class}">{todo['title']}</div>
                        {f'<div class="todo-description">{todo["description"]}</div>' if todo.get('description') else ''}
                    </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                if st.button("🗑️", key=f"del_{todo['id']}", help="Delete todo"):
                    if delete_todo(todo['id']):
                        st.success("Todo deleted!")
                        st.rerun()

# Main app
def main():
    # Initialize show_signup if not exists
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    # Route to appropriate page
    if st.session_state.user_id:
        show_todos()
    else:
        if st.session_state.show_signup:
            show_signup()
        else:
            show_login()

if __name__ == "__main__":
    main()
