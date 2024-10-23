import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    # Placeholder for actual data loading logic
    df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
district_filter = st.sidebar.selectbox("Select District", options=["All"] + df['SCHOOL_DISTRICT_NAME'].unique().tolist())
school_filter = st.sidebar.selectbox("Select School", options=["All"] + df['SCHOOL_NAME'].unique().tolist())
grade_filter = st.sidebar.selectbox("Select Grade", options=["All"] + df['GRADE'].unique().tolist())

# Apply filters to the data
filtered_df = df.copy()
if district_filter != "All":
    filtered_df = filtered_df[filtered_df['SCHOOL_DISTRICT_NAME'] == district_filter]
if school_filter != "All":
    filtered_df = filtered_df[filtered_df['SCHOOL_NAME'] == school_filter]
if grade_filter != "All":
    filtered_df = filtered_df[filtered_df['GRADE'] == grade_filter]

# Dashboard Title
st.title("Student Data Dashboard")

# Task 1: Review Student Assessment and Demographics
st.subheader("Student Assessment and Demographics Dashboard")
if not filtered_df.empty:
    st.dataframe(filtered_df[['STUDENT_ID', 'SCHOOL_NAME', 'GENDER', 'ETHNICITY', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']])
else:
    st.write("No data available for the selected filters.")

# Task 2: ML Progress Monitoring
st.subheader("Multilingual Learners (ML) Progress Monitoring")
ml_students_df = filtered_df[filtered_df['ML_PROGRAM_YEAR'].notnull()]
if not ml_students_df.empty:
    st.write("### ML Students Progress")
    st.dataframe(ml_students_df[['STUDENT_ID', 'SCHOOL_NAME', 'ML_PROGRAM_YEAR', 'ML_ACCESS_SCORE', 'ENGLISH_SCORE']])
else:
    st.write("No ML students found for the selected filters.")

# Task 3: Track Progress on Student Learning Objectives
st.subheader("Student Learning Objectives (SLO) Progress")
if 'GOAL_DIRECTED_BEHAVIOR' in filtered_df.columns and 'FINAL_GRADES' in filtered_df.columns:
    st.dataframe(filtered_df[['STUDENT_ID', 'SCHOOL_NAME', 'FINAL_GRADES', 'GOAL_DIRECTED_BEHAVIOR']])
else:
    st.write("No data available for Student Learning Objectives.")

# Task 4: Track Gifted and Talented Students
st.subheader("Gifted and Talented Students Tracking")
gifted_students_df = filtered_df[(filtered_df['STATE_ELA_SCORE'] > 85) & (filtered_df['STATE_MATH_SCORE'] > 85)]
if not gifted_students_df.empty:
    st.write("### Gifted and Talented Students")
    st.dataframe(gifted_students_df[['STUDENT_ID', 'SCHOOL_NAME', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']])
else:
    st.write("No Gifted and Talented students found for the selected filters.")

# Task 5: Transfer Assessment Data Between Schools
st.subheader("Transfer Student Assessment Data")
transfer_students_df = filtered_df[filtered_df['SCHOOL_ID'] != school_filter]
if not transfer_students_df.empty:
    st.write("### Students Transferred from Other Schools")
    st.dataframe(transfer_students_df[['STUDENT_ID', 'SCHOOL_NAME', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']])
else:
    st.write("No transfer students found.")

# Task 6: Create Custom Student Groups
st.subheader("Create Custom Student Groups")
selected_students = st.multiselect("Select Student IDs to Group:", filtered_df['STUDENT_ID'].unique())
if selected_students:
    grouped_students_df = filtered_df[filtered_df['STUDENT_ID'].isin(selected_students)]
    st.dataframe(grouped_students_df[['STUDENT_ID', 'SCHOOL_NAME', 'GENDER', 'ETHNICITY', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']])
else:
    st.write("No students selected.")

# Task: Special Programs - IEP, 504, ILAP Students
st.subheader("Special Programs: IEP, 504, ILAP Students")
if 'SPECIAL_EDUCATION_STATUS' in filtered_df.columns:
    iep_students_df = filtered_df[filtered_df['SPECIAL_EDUCATION_STATUS'].isin(['IEP', '504', 'ILAP'])]
    if not iep_students_df.empty:
        st.write("### List of Students with IEP, 504, or ILAP")
        st.dataframe(iep_students_df[['STUDENT_ID', 'SCHOOL_NAME', 'SPECIAL_EDUCATION_STATUS']])
        
        csv = iep_students_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name='iep_504_ilap_students.csv',
            mime='text/csv',
        )

        total_students = iep_students_df.shape[0]
        iep_count = iep_students_df[iep_students_df['SPECIAL_EDUCATION_STATUS'] == 'IEP'].shape[0]
        ilap_count = iep_students_df[iep_students_df['SPECIAL_EDUCATION_STATUS'] == 'ILAP'].shape[0]
        s504_count = iep_students_df[iep_students_df['SPECIAL_EDUCATION_STATUS'] == '504'].shape[0]

        st.metric("Total IEP, 504, ILAP Students", total_students)
        st.metric("Total IEP Students", iep_count)
        st.metric("Total ILAP Students", ilap_count)
        st.metric("Total 504 Students", s504_count)
    else:
        st.write("No IEP, 504, or ILAP students found.")
else:
    st.write("SPECIAL_EDUCATION_STATUS column not available.")

# Task: Teacher Classroom Reports
st.subheader("Teacher Classroom Reports")
if 'TEACHER_ID' in filtered_df.columns:
    st.write("### Classroom Reports by Teacher")
    teacher_df = filtered_df.groupby('TEACHER_ID').agg({
        'STUDENT_ID': 'count',
        'FINAL_GRADES': 'mean',
        'ATTENDANCE': 'mean'
    }).reset_index()
    st.dataframe(teacher_df)
else:
    st.write("Teacher data not available.")
