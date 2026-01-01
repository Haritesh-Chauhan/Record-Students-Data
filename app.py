import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional theme
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    div[data-testid="stForm"] {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .success-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
        animation: fadeIn 0.8s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .welcome-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .welcome-subtitle {
        font-size: 1.5rem;
        margin-top: 1rem;
        font-style: italic;
    }
    h1, h2, h3 {
        color: white !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    [data-testid="stSidebar"] h1 {
        color: black !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Database initialization
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  certificate TEXT DEFAULT 'Not Issued',
                  course TEXT NOT NULL,
                  email TEXT NOT NULL,
                  father_name TEXT NOT NULL,
                  university_roll TEXT NOT NULL,
                  contact TEXT NOT NULL,
                  parent_contact TEXT NOT NULL,
                  college TEXT NOT NULL,
                  college_course TEXT NOT NULL,
                  semester TEXT NOT NULL,
                  department TEXT NOT NULL,
                  dob TEXT NOT NULL,
                  address TEXT NOT NULL,
                  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# Validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    return phone.isdigit() and len(phone) == 10

def validate_age(dob):
    try:
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return 15 <= age <= 100
    except:
        return False

# Insert student data
def insert_student(data):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''INSERT INTO students (name, certificate, course, email, father_name, 
                 university_roll, contact, parent_contact, college, college_course, 
                 semester, department, dob, address) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (data['name'], 'Not Issued', data['course'], data['email'], 
               data['father_name'], data['university_roll'], data['contact'],
               data['parent_contact'], data['college'], data['college_course'],
               data['semester'], data['department'], data['dob'], data['address']))
    conn.commit()
    student_id = c.lastrowid
    conn.close()
    return student_id

# Get all students
def get_all_students():
    conn = sqlite3.connect('students.db')
    df = pd.read_sql_query("SELECT * FROM students ORDER BY id DESC", conn)
    conn.close()
    return df

# Get student by ID
def get_student_by_id(student_id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = c.fetchone()
    conn.close()
    return student

# Initialize database
init_db()

# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'student_id' not in st.session_state:
    st.session_state.student_id = None

# Sidebar navigation
st.sidebar.title("🎓 Navigation")
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.page = 'home'
    st.session_state.authenticated = False
    st.rerun()

if st.sidebar.button("👨‍🎓 Student Registration", use_container_width=True):
    st.session_state.page = 'student'
    st.rerun()

if st.sidebar.button("👨‍🏫 Teacher Login", use_container_width=True):
    st.session_state.page = 'teacher'
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Fill all fields carefully!")

# HOME PAGE
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align: center;'>🎓 Welcome to AI Learning Portal</h1>", unsafe_allow_html=True)
    # st.markdown("<h3 style='text-align: center; color: #f0f0f0;'>Chauhan Sir's Class</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; margin-top: 2rem;'>
            <h2 style='color: #667eea; text-align: center;'>📚 Choose Your Role</h2>
            <p style='color: #555; text-align: center; font-size: 1.1rem;'>
                Students can register for the new batch<br>
                Teachers can view all registered students
            </p>
        </div>
        """, unsafe_allow_html=True)

# STUDENT REGISTRATION PAGE
elif st.session_state.page == 'student':
    if st.session_state.student_id is None:
        st.markdown("<h1 style='text-align: center;'>👨‍🎓 Student Registration Form</h1>", unsafe_allow_html=True)
        
        with st.form("student_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("📝 Full Name *", placeholder="Enter your full name")
                course = st.text_input("📚 Course *", placeholder="e.g., AI & Machine Learning")
                email = st.text_input("📧 Email *", placeholder="your.email@example.com")
                father_name = st.text_input("👨‍👦 Father's Name *", placeholder="Enter father's name")
                university_roll = st.text_input("🎫 University Roll Number *", placeholder="Enter roll number")
                contact = st.text_input("📱 Contact Number *", placeholder="10-digit mobile number")
                parent_contact = st.text_input("📞 Parent's Contact *", placeholder="10-digit mobile number")
            
            with col2:
                college = st.text_input("🏛️ College *", placeholder="Enter college name")
                college_course = st.text_input("🎓 College Course *", placeholder="e.g., B.Tech CSE")
                semester = st.selectbox("📖 Semester *", ["Select", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"])
                department = st.text_input("🏢 Department *", placeholder="e.g., Computer Science")
                dob = st.date_input("🎂 Date of Birth *", min_value=datetime(1950, 1, 1), max_value=datetime.today())
                address = st.text_area("🏠 Address *", placeholder="Enter complete address")
            
            submitted = st.form_submit_button("✅ Register Now", use_container_width=True)
            
            if submitted:
                errors = []
                
                # Validation
                if not name.strip():
                    errors.append("❌ Name is required")
                if not course.strip():
                    errors.append("❌ Course is required")
                if not validate_email(email):
                    errors.append("❌ Invalid email format")
                if not father_name.strip():
                    errors.append("❌ Father's name is required")
                if not university_roll.strip():
                    errors.append("❌ University roll number is required")
                if not validate_phone(contact):
                    errors.append("❌ Contact number must be 10 digits")
                if not validate_phone(parent_contact):
                    errors.append("❌ Parent's contact must be 10 digits")
                if not college.strip():
                    errors.append("❌ College name is required")
                if not college_course.strip():
                    errors.append("❌ College course is required")
                if semester == "Select":
                    errors.append("❌ Please select semester")
                if not department.strip():
                    errors.append("❌ Department is required")
                if not validate_age(str(dob)):
                    errors.append("❌ Invalid age (must be between 15-100 years)")
                if not address.strip():
                    errors.append("❌ Address is required")
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    student_data = {
                        'name': name,
                        'course': course,
                        'email': email,
                        'father_name': father_name,
                        'university_roll': university_roll,
                        'contact': contact,
                        'parent_contact': parent_contact,
                        'college': college,
                        'college_course': college_course,
                        'semester': semester,
                        'department': department,
                        'dob': str(dob),
                        'address': address
                    }
                    
                    student_id = insert_student(student_data)
                    st.session_state.student_id = student_id
                    st.success("✅ Registration successful!")
                    st.rerun()
    
    else:
        # Show confirmation and welcome message
        student = get_student_by_id(st.session_state.student_id)
        
        st.markdown("""
        <div class='success-box'>
            <div class='welcome-title'>🎉 Registration Successful!</div>
            <p style='font-size: 1.3rem;'>Your details have been recorded</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; color: white; margin: 2rem 0;'>📋 Your Submitted Details</h3>", unsafe_allow_html=True)
        
        # Create a white container for details
        st.markdown("""
        <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>S.No:</strong> {student[0]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Name:</strong> {student[1]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Certificate:</strong> {student[2]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Course:</strong> {student[3]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Email:</strong> {student[4]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Father's Name:</strong> {student[5]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>University Roll:</strong> {student[6]}</p>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Contact:</strong> {student[7]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Parent's Contact:</strong> {student[8]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>College:</strong> {student[9]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>College Course:</strong> {student[10]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Semester:</strong> {student[11]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>Department:</strong> {student[12]}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 0.5rem 0;'><strong style='color: #667eea;'>DOB:</strong> {student[13]}</p>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='color: #333; font-size: 1.1rem; margin: 1rem 0;'><strong style='color: #667eea;'>Address:</strong> {student[14]}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='success-box' style='margin-top: 2rem;'>
            <div class='welcome-title'>🚀 Welcome to Haritesh Chauhan Class</div>
            <div class='welcome-subtitle'>Let's Learn About AI! 🤖✨</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.student_id = None
            st.session_state.page = 'home'
            st.rerun()

# TEACHER LOGIN PAGE
elif st.session_state.page == 'teacher':
    if not st.session_state.authenticated:
        st.markdown("<h1 style='text-align: center;'>👨‍🏫 Teacher Authentication</h1>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.markdown("<div style='background: white; padding: 2rem; border-radius: 15px;'>", unsafe_allow_html=True)
                username = st.text_input("👤 Username", placeholder="Enter username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
                login = st.form_submit_button("🔓 Login", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                if login:
                    # Simple authentication (you can change these credentials)
                    if username == "teacher" and password == "chauhan123":
                        st.session_state.authenticated = True
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
    else:
        st.markdown("<h1 style='text-align: center;'>📊 All Registered Students</h1>", unsafe_allow_html=True)
        
        df = get_all_students()
        
        if len(df) > 0:
            st.markdown(f"<h3 style='color: white;'>Total Students: {len(df)}</h3>", unsafe_allow_html=True)
            
            # Display DataFrame with styling
            st.dataframe(
                df.style.set_properties(**{
                    'background-color': 'white',
                    'color': 'black',
                    'border-color': '#667eea'
                }),
                use_container_width=True,
                height=500
            )
            
            # Download option
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Student Data (CSV)",
                data=csv,
                file_name=f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("📝 No students registered yet!")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.page = 'home'

            st.rerun()
