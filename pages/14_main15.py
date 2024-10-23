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

# Special Education Status section
if st.sidebar.checkbox("IEP, 504, ILAP Students"):
    if 'SPECIAL_EDUCATION_STATUS' in df.columns:
        # Filter for students with special education status
        special_education_df = df[df['SPECIAL_EDUCATION_STATUS'].isin(['IEP', '504', 'ILAP'])]
        
        # Summary statistics
        total_students = special_education_df.shape[0]
        iep_count = special_education_df[special_education_df['SPECIAL_EDUCATION_STATUS'] == 'IEP'].shape[0]
        ilap_count = special_education_df[special_education_df['SPECIAL_EDUCATION_STATUS'] == 'ILAP'].shape[0]
        s504_count = special_education_df[special_education_df['SPECIAL_EDUCATION_STATUS'] == '504'].shape[0]

        # Display metrics
        st.metric("Total IEP, 504, ILAP Students", total_students)
        st.metric("Total IEP Students", iep_count)
        st.metric("Total ILAP Students", ilap_count)
        st.metric("Total 504 Students", s504_count)

        # Display the filtered students
        st.write("### List of Students with IEP, 504, or ILAP")
        st.dataframe(special_education_df[['STUDENT_ID', 'SCHOOL_NAME', 'SPECIAL_EDUCATION_STATUS']])

        # Download option
        csv = special_education_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='iep_504_ilap_students.csv',
            mime='text/csv',
        )
    else:
        st.write("Column 'SPECIAL_EDUCATION_STATUS' does not exist in the dataset.")

# Dashboard for Final Grades
if st.sidebar.checkbox("Student Final Grades"):
    if 'FINAL_GRADES' in df.columns:
        final_grades_df = filtered_df[['STUDENT_ID', 'FINAL_GRADES']].dropna()
        st.write("Student Final Grades:")
        st.bar_chart(final_grades_df.set_index('STUDENT_ID'))
    else:
        st.write("Column 'FINAL_GRADES' does not exist in the dataset.")

# Dashboard for Attendance
if st.sidebar.checkbox("Attendance"):
    if 'ATTENDANCE' in df.columns:
        attendance_df = filtered_df[['STUDENT_ID', 'ATTENDANCE']].dropna()
        st.write("Student Attendance:")
        st.bar_chart(attendance_df.set_index('STUDENT_ID'))
    else:
        st.write("Column 'ATTENDANCE' does not exist in the dataset.")

# Dashboard for State Math Scores
if st.sidebar.checkbox("State Math Scores"):
    if 'STATE_MATH_SCORE' in df.columns:
        math_scores_df = filtered_df[['STUDENT_ID', 'STATE_MATH_SCORE']].dropna()
        st.write("State Math Scores:")
        st.bar_chart(math_scores_df.set_index('STUDENT_ID'))
    else:
        st.write("Column 'STATE_MATH_SCORE' does not exist in the dataset.")

# Dashboard for State ELA Scores
if st.sidebar.checkbox("State ELA Scores"):
    if 'STATE_ELA_SCORE' in df.columns:
        ela_scores_df = filtered_df[['STUDENT_ID', 'STATE_ELA_SCORE']].dropna()
        st.write("State ELA Scores:")
        st.bar_chart(ela_scores_df.set_index('STUDENT_ID'))
    else:
        st.write("Column 'STATE_ELA_SCORE' does not exist in the dataset.")

# Dashboard for Math Scores
if st.sidebar.checkbox("Math Scores"):
    if 'MATH_SCORE' in df.columns:
        math_scores_df = filtered_df[['STUDENT_ID', 'MATH_SCORE']].dropna()
        st.write("Math Scores:")
        st.bar_chart(math_scores_df.set_index('STUDENT_ID'))
    else:
        st.write("Column 'MATH_SCORE' does not exist in the dataset.")

# Add more dashboards as needed based on available columns
