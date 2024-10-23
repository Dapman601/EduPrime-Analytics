import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')



# Sidebar for selecting filters
st.sidebar.header("Filter Options")

# Unique values for district selection, "All" option first
district_ids = ["All"] + df['SCHOOL_DISTRICT_ID'].unique().tolist()
selected_district = st.sidebar.selectbox("Select School District:", district_ids)

# Filter DataFrame based on the selected district
if selected_district == "All":
    district_df = df
else:
    district_df = df[df['SCHOOL_DISTRICT_ID'] == selected_district]

# Automatically update the school selection based on the selected district, "All" option first
school_ids = ["All"] + district_df['SCHOOL_ID'].unique().tolist()
selected_school = st.sidebar.selectbox("Select School ID:", school_ids)

# Filter DataFrame based on the selected school
if selected_school == "All":
    school_df = district_df
else:
    school_df = district_df[district_df['SCHOOL_ID'] == selected_school]

# Automatically update the student selection based on the selected school, "All" option first
student_ids = ["All"] + school_df['STUDENT_ID'].unique().tolist()
selected_student = st.sidebar.selectbox("Select Student ID:", student_ids)

# Filter DataFrame based on the selected student
if selected_student == "All":
    filtered_df = school_df
else:
    filtered_df = school_df[school_df['STUDENT_ID'] == selected_student]

# Display metrics dashboard based on the selection
st.title("Student Dashboard")

# At-Risk Students section
st.sidebar.header("Identify At-Risk Students")

# Define at-risk criteria
risk_criteria = st.sidebar.multiselect(
    "Select At-Risk Categories:",
    ["Low Attendance", "Low Final Grades", "Low Math Scores", "Low ELA Scores"],
)

# Initialize an empty DataFrame to hold at-risk students
at_risk_students = filtered_df.copy()

# Define thresholds for at-risk criteria
attendance_threshold = 75  # example threshold for attendance
final_grades_threshold = 65  # example threshold for final grades
math_scores_threshold = 60  # example threshold for math scores
ela_scores_threshold = 60  # example threshold for ELA scores

# Apply filters based on selected criteria
if "Low Attendance" in risk_criteria:
    at_risk_students = at_risk_students[at_risk_students['ATTENDANCE'] < attendance_threshold]

if "Low Final Grades" in risk_criteria:
    at_risk_students = at_risk_students[at_risk_students['FINAL_GRADES'] < final_grades_threshold]

if "Low Math Scores" in risk_criteria:
    at_risk_students = at_risk_students[at_risk_students['STATE_MATH_SCORE'] < math_scores_threshold]

if "Low ELA Scores" in risk_criteria:
    at_risk_students = at_risk_students[at_risk_students['STATE_ELA_SCORE'] < ela_scores_threshold]

# Display at-risk students
if not at_risk_students.empty:
    st.write("### At-Risk Students")
    st.dataframe(at_risk_students[['STUDENT_ID', 'SCHOOL_NAME', 'ATTENDANCE', 'FINAL_GRADES', 'STATE_MATH_SCORE', 'STATE_ELA_SCORE']])
    
    # Download option for at-risk students
    csv = at_risk_students.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download At-Risk Students as CSV",
        data=csv,
        file_name='at_risk_students.csv',
        mime='text/csv',
    )
else:
    st.write("No at-risk students identified based on the selected criteria.")

# Additional sections for student performance metrics (Final Grades, Attendance, etc.)
# [Include existing sections from the previous code here]
