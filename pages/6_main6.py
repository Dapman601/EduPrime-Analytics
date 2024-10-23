import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
df = pd.read_csv(r'C:\Users\DELL\Documents\02_consults\code2\school_student_data.csv')

# Sidebar filters for demographic data
st.sidebar.header('Filter Data')

# District filter
district_id = st.sidebar.selectbox('Select District ID', options=['All'] + df['SCHOOL_DISTRICT_ID'].unique().tolist())

# School filters (dependent on district selection)
if district_id != 'All':
    # Filter the schools based on the selected district
    filtered_schools = df[df['SCHOOL_DISTRICT_ID'] == district_id]
    school_id = st.sidebar.selectbox('Select School ID', options=['All'] + filtered_schools['SCHOOL_ID'].unique().tolist())
    school_name = st.sidebar.selectbox('Select School Name', options=['All'] + filtered_schools['SCHOOL_NAME'].unique().tolist())
else:
    # If no district is selected, show all schools
    school_id = st.sidebar.selectbox('Select School ID', options=['All'] + df['SCHOOL_ID'].unique().tolist())
    school_name = st.sidebar.selectbox('Select School Name', options=['All'] + df['SCHOOL_NAME'].unique().tolist())

# Grade, Ethnicity, Gender filters
grade = st.sidebar.selectbox('Select Grade', options=['All'] + df['GRADE'].unique().tolist())
ethnicity = st.sidebar.selectbox('Select Ethnicity', options=['All'] + df['ETHNICITY'].unique().tolist())
gender = st.sidebar.selectbox('Select Gender', options=['All'] + df['GENDER'].unique().tolist())

# Apply filters to the dataset
filtered_df = df.copy()
if district_id != 'All':
    filtered_df = filtered_df[filtered_df['SCHOOL_DISTRICT_ID'] == district_id]
if school_id != 'All':
    filtered_df = filtered_df[filtered_df['SCHOOL_ID'] == school_id]
if grade != 'All':
    filtered_df = filtered_df[filtered_df['GRADE'] == grade]
if ethnicity != 'All':
    filtered_df = filtered_df[filtered_df['ETHNICITY'] == ethnicity]
if gender != 'All':
    filtered_df = filtered_df[filtered_df['GENDER'] == gender]

# Create Dashboards
st.title("School Dashboard")

# Enrollment Dashboard
st.header('Enrollment Dashboard')
enrollment_data = filtered_df.groupby('SCHOOL_NAME')['STUDENT_ID'].nunique().reset_index()
enrollment_data.columns = ['School Name', 'Student Count']
st.write(enrollment_data)

# Enrollment Bar Chart
fig_enrollment = px.bar(enrollment_data, x='School Name', y='Student Count', title='Student Enrollment by School')
st.plotly_chart(fig_enrollment)

# Attendance Dashboard
st.header('Attendance Dashboard')
attendance_data = filtered_df[['SCHOOL_NAME', 'ATTENDANCE', 'EXCUSED_ABSENCES']].groupby('SCHOOL_NAME').mean().reset_index()
st.write(attendance_data)

# Attendance Bar Chart
fig_attendance = px.bar(attendance_data, x='SCHOOL_NAME', y='ATTENDANCE', title='Average Attendance by School')
st.plotly_chart(fig_attendance)

# Behavior Dashboard
st.header('Behavior Dashboard')
behavior_data = filtered_df[['SCHOOL_NAME', 'POSITIVE_BEHAVIORS', 'MINOR_CORRECTIVE', 'MAJOR_CORRECTIVE']].groupby('SCHOOL_NAME').mean().reset_index()
st.write(behavior_data)

# Behavior Bar Chart
fig_behavior = px.bar(behavior_data, x='SCHOOL_NAME', y='POSITIVE_BEHAVIORS', title='Positive Behaviors by School')
st.plotly_chart(fig_behavior)

# Discipline Dashboard
st.header('Discipline Dashboard')
discipline_data = filtered_df[['SCHOOL_NAME', 'MINOR_CORRECTIVE', 'MAJOR_CORRECTIVE']].groupby('SCHOOL_NAME').sum().reset_index()
st.write(discipline_data)

# Discipline Bar Chart
fig_discipline = px.bar(discipline_data, x='SCHOOL_NAME', y=['MINOR_CORRECTIVE', 'MAJOR_CORRECTIVE'], title='Discipline Events by School')
st.plotly_chart(fig_discipline)

# Academic Performance Dashboard
st.header('Academic Performance Dashboard')
academic_data = filtered_df[['SCHOOL_NAME', 'FINAL_GRADES']].groupby('SCHOOL_NAME').mean().reset_index()
st.write(academic_data)

# Academic Bar Chart
fig_academics = px.bar(academic_data, x='SCHOOL_NAME', y='FINAL_GRADES', title='Average Final Grades by School')
st.plotly_chart(fig_academics)

# Assessment Performance Dashboard
st.header('Assessment Performance Dashboard')
assessment_data = filtered_df[['SCHOOL_NAME', 'STATE_ELA_PROFICIENCY', 'STATE_MATH_PROFICIENCY']].groupby('SCHOOL_NAME').mean().reset_index()
st.write(assessment_data)

# Assessment Proficiency Bar Chart
fig_assessment = px.bar(assessment_data, x='SCHOOL_NAME', y=['STATE_ELA_PROFICIENCY', 'STATE_MATH_PROFICIENCY'], title='Proficiency in ELA and Math by School')
st.plotly_chart(fig_assessment)
