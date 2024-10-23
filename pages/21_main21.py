import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')



# Title of the dashboard
st.title("Student Performance Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# District ID filter
district_options = ['All'] + df['SCHOOL_DISTRICT_ID'].unique().tolist()
selected_district_id = st.sidebar.selectbox("Select District ID", district_options)
if selected_district_id != 'All':
    filtered_district_df = df[df['SCHOOL_DISTRICT_ID'] == selected_district_id]
else:
    filtered_district_df = df

# School ID filter
school_options = ['All'] + filtered_district_df['SCHOOL_ID'].unique().tolist()
selected_school_id = st.sidebar.selectbox("Select School ID", school_options)
if selected_school_id != 'All':
    filtered_school_df = filtered_district_df[filtered_district_df['SCHOOL_ID'] == selected_school_id]
else:
    filtered_school_df = filtered_district_df

# Student ID filter
student_options = ['All'] + filtered_school_df['STUDENT_ID'].unique().tolist()
selected_student_id = st.sidebar.selectbox("Select Student ID", student_options)
if selected_student_id != 'All':
    filtered_student_df = filtered_school_df[filtered_school_df['STUDENT_ID'] == selected_student_id]
else:
    filtered_student_df = filtered_school_df

# Grade filter
grade_options = ['All'] + filtered_student_df['GRADE'].unique().tolist()
selected_grade = st.sidebar.selectbox("Select Grade", grade_options)
if selected_grade != 'All':
    final_filtered_df = filtered_student_df[filtered_student_df['GRADE'] == selected_grade]
else:
    final_filtered_df = filtered_student_df

# Goal 1: Student Performance
st.header("Goal 1: Student Performance")
st.write("The percentage of students meeting proficiency in English Language Arts (ELA) and Mathematics.")

# Leading Indicator 1.1
leading_indicator_1_1 = final_filtered_df[final_filtered_df['STATE_ELA_PROFICIENCY'] >= 75].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of Students Proficient in ELA", leading_indicator_1_1)

# Leading Indicator 1.2
leading_indicator_1_2 = final_filtered_df[final_filtered_df['STATE_MATH_PROFICIENCY'] >= 75].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of Students Proficient in Math", leading_indicator_1_2)

# Goal 2: Student Growth
st.header("Goal 2: Student Growth")
st.write("The percentage of students meeting growth targets in ELA and Math.")

# Leading Indicator 2.1
leading_indicator_2_1 = final_filtered_df[final_filtered_df['STATE_ELA_GROWTH'] >= 75].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of Students Meeting ELA Growth Target", leading_indicator_2_1)

# Leading Indicator 2.2
leading_indicator_2_2 = final_filtered_df[final_filtered_df['STATE_MATH_GROWTH'] >= 75].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of Students Meeting Math Growth Target", leading_indicator_2_2)

# Goal 3: High School Graduation Rates
st.header("Goal 3: High School Graduation Rates")
st.write("The percentage of students graduating on time.")

# Leading Indicator 3.1
leading_indicator_3_1 = final_filtered_df[final_filtered_df['GRADUATION_STATUS'] == 'Graduated'].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of Students Graduating on Time", leading_indicator_3_1)

# Goal 4: High School Assessment Proficiency
st.header("Goal 4: High School Assessment Proficiency")
st.write("The percentage of students who are proficient on all three state high school assessments (Algebra, Literature, Biology) by the end of their 10th grade year.")

# Leading Indicator 4.1
leading_indicator_4_1 = final_filtered_df[
    (final_filtered_df['HIGH_SCHOOL_ALGEBRA_PROFICIENCY'] >= 75) &
    (final_filtered_df['HIGH_SCHOOL_LITERATURE_PROFICIENCY'] >= 75) &
    (final_filtered_df['HIGH_SCHOOL_BIOLOGY_PROFICIENCY'] >= 75)
].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage Proficient on All Three Assessments", leading_indicator_4_1)

# Leading Indicator 4.2
leading_indicator_4_2 = final_filtered_df[final_filtered_df['GRADUATION_STATUS'] == 'Firmly On Track'].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of 9th Graders Firmly On-Track", leading_indicator_4_2)

# Goal 5: Career and Technical Education (CTE)
st.header("Goal 5: CTE Students Passing Competency Assessment")
st.write("The percentage of Career and Technical Education (CTE) students who pass an industry standards-based competency assessment by the end of their 12th grade year will grow from 49.1% in August 2023 to 80.0% in August 2030.")

# Goal 5 Progress
goal_5_df = pd.DataFrame({
    'Year': ['2023', '2030'],
    'Pass Rate': [49.1, 80.0]
})

fig_goal_5 = px.line(goal_5_df, x='Year', y='Pass Rate', title='CTE Pass Rate Goal', markers=True)
st.plotly_chart(fig_goal_5)

# Leading Indicators for Goal 5
st.subheader("Leading Indicators for Goal 5")

# Leading Indicator 5.1: Percentage of eligible students passing the NOCTI
leading_indicator_5_1 = final_filtered_df[final_filtered_df['NOCTI_PASS_RATE'] >= 75].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of Eligible Students Passing NOCTI", leading_indicator_5_1)

# Leading Indicator 5.2: Percentage of CTE students with job placement or postsecondary opportunity
leading_indicator_5_2 = final_filtered_df[final_filtered_df['JOB_PLACEMENT_RATE'] >= 75].shape[0] / final_filtered_df.shape[0] * 100 if final_filtered_df.shape[0] > 0 else 0
st.metric("Percentage of CTE Students with Job Placement/Postsecondary Opportunity", leading_indicator_5_2)
