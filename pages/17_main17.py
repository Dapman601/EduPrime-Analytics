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

# Automatically update the teacher selection based on the selected school, "All" option first
teacher_ids = ["All"] + school_df['TEACHER_ID'].unique().tolist()
selected_teacher = st.sidebar.selectbox("Select Teacher ID:", teacher_ids)

# Filter DataFrame based on the selected teacher
if selected_teacher == "All":
    teacher_df = school_df
else:
    teacher_df = school_df[school_df['TEACHER_ID'] == selected_teacher]

# Teacher Classroom Report section
st.title("Teacher Classroom Reports")

if selected_teacher == "All":
    st.write("Please select a teacher to view the classroom report.")
else:
    st.write(f"### Report for Teacher ID: {selected_teacher}")

    # Calculate classroom statistics
    avg_attendance = teacher_df['ATTENDANCE'].mean()
    avg_final_grades = teacher_df['FINAL_GRADES'].mean()
    special_education_count = teacher_df[teacher_df['SPECIAL_EDUCATION_STATUS'].notnull()].shape[0]

    # Display key metrics for the teacher's classroom
    st.metric("Average Attendance", f"{avg_attendance:.2f}%")
    st.metric("Average Final Grades", f"{avg_final_grades:.2f}")
    st.metric("Number of Students with Special Education Needs", special_education_count)

    # Display detailed student information in the teacher's classroom
    st.write("### Detailed Classroom Report")
    st.dataframe(teacher_df[['STUDENT_ID', 'SCHOOL_NAME', 'ATTENDANCE', 'FINAL_GRADES', 'SPECIAL_EDUCATION_STATUS']])

    # Download option for the classroom report
    csv = teacher_df[['STUDENT_ID', 'SCHOOL_NAME', 'ATTENDANCE', 'FINAL_GRADES', 'SPECIAL_EDUCATION_STATUS']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Classroom Report as CSV",
        data=csv,
        file_name=f'teacher_{selected_teacher}_classroom_report.csv',
        mime='text/csv',
    )

# Additional sections for student performance metrics (At-Risk Students, IEP/504 Students, etc.)
# [Include existing sections from the previous code here]
