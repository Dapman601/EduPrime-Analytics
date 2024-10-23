import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv(r'C:\Users\DELL\Documents\02_consults\code2\school_student_data.csv')

# Sidebar filters
st.sidebar.header("Filters")

# School District Filter
school_districts = df['SCHOOL_DISTRICT_NAME'].unique().tolist()
school_districts.insert(0, 'All')  # Add 'All' option
selected_district = st.sidebar.selectbox('Select School District', school_districts)

# School Filter
if selected_district == 'All':
    schools = df['SCHOOL_NAME'].unique().tolist()
else:
    schools = df[df['SCHOOL_DISTRICT_NAME'] == selected_district]['SCHOOL_NAME'].unique().tolist()
schools.insert(0, 'All')  # Add 'All' option
selected_school = st.sidebar.selectbox('Select School', schools)

# Student ID Filter
if selected_school == 'All':
    student_ids = df['STUDENT_ID'].unique().tolist()
else:
    student_ids = df[df['SCHOOL_NAME'] == selected_school]['STUDENT_ID'].unique().tolist()
student_ids.insert(0, 'All')  # Add 'All' option
selected_student_id = st.sidebar.selectbox('Select Student ID', student_ids)

# Assessment Type Filter
assessment_types = ['STATE_ELA_PROFICIENCY', 'STATE_MATH_PROFICIENCY', 'SCREADY_WRITING_TEST_DURATION']  # Add other relevant assessment types
selected_assessment = st.sidebar.selectbox('Select Assessment Type', assessment_types)

# Filter DataFrame based on selections
filtered_df = df.copy()

if selected_district != 'All':
    filtered_df = filtered_df[filtered_df['SCHOOL_DISTRICT_NAME'] == selected_district]

if selected_school != 'All':
    filtered_df = filtered_df[filtered_df['SCHOOL_NAME'] == selected_school]

if selected_student_id != 'All':
    filtered_df = filtered_df[filtered_df['STUDENT_ID'] == selected_student_id]

# Display filtered data
st.subheader("Filtered Data")
st.write(filtered_df)

# Example Visualization: EOCEP Math Performance by Special Education Status
if not filtered_df.empty:
    # Group data for visualization
    group_data = filtered_df.groupby('SPECIAL_EDUCATION_STATUS')[selected_assessment].mean().reset_index()

    # Create bar chart
    fig = px.bar(group_data, x='SPECIAL_EDUCATION_STATUS', y=selected_assessment,
                 title=f'{selected_assessment} by Special Education Status',
                 labels={'SPECIAL_EDUCATION_STATUS': 'Special Education Status', 
                         selected_assessment: selected_assessment})

    st.plotly_chart(fig)

# Additional visualizations can be added here similarly
