import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(r'C:\Users\DELL\Documents\02_consults\code2\school_student_data.csv')

# Assessment descriptions
assessment_descriptions = {
    'STATE_ELA_PROFICIENCY': 'Proficiency in English Language Arts (ELA) as measured by state assessments.',
    'STATE_ELA_GROWTH': 'Growth in ELA performance over time, likely based on improvements from previous assessments.',
    'DISTRICT_READING_ASSESSMENT_TARGET': 'Target score or level for reading assessments as set by the district.',
    'DISTRICT_READING_ASSESSMENT_GROWTH': 'Growth in district reading assessment performance.',
    'STATE_MATH_PROFICIENCY': 'Proficiency in mathematics as measured by state assessments.',
    'STATE_MATH_GROWTH': 'Growth in mathematics performance over time, likely based on state assessments.',
    'DISTRICT_MATH_ASSESSMENT_TARGET': 'Target score or level for math assessments as set by the district.',
    'DISTRICT_MATH_ASSESSMENT_GROWTH': 'Growth in district math assessment performance.',
    'CURRICULUM_BASED_MATH_MEASURES': 'Math measures based on the curriculum (possibly internal assessments rather than standardized tests).',
    'HIGH_SCHOOL_LITERATURE_PROFICIENCY': 'Proficiency in high school-level literature.',
    'HIGH_SCHOOL_ALGEBRA_PROFICIENCY': 'Proficiency in high school-level algebra.',
    'HIGH_SCHOOL_BIOLOGY_PROFICIENCY': 'Proficiency in high school-level biology.',
    'PROFICIENCY_ALL_THREE_ASSESSMENTS': 'Indicates whether the student has achieved proficiency in all three key areas (likely literature, algebra, and biology).',
    'CTE_INDUSTRY_STANDARD_PASS_RATE': 'Pass rate for students in Career and Technical Education (CTE) industry-standard assessments.',
    'NOCTI_PASS_RATE': 'Pass rate for NOCTI (National Occupational Competency Testing Institute) exams, which assess career and technical skills.',
    'JOB_PLACEMENT_RATE': 'Rate at which students secure jobs after graduation (may not be an "assessment" in the traditional sense but is linked to CTE success).',
    'POSTSECONDARY_OPPORTUNITIES': 'Availability of postsecondary opportunities, possibly linked to student performance on assessments.',
    'ENGLISH_SCORE': 'Score in English Language Arts or English-related assessments.',
    'MATH_SCORE': 'Score in mathematics assessments.',
    'SCIENCE_SCORE': 'Score in science assessments.',
    'FINAL_GRADES': 'Final grades, likely a cumulative assessment of student performance in multiple subjects.',
    'SCREADY_WRITING_TEST_DURATION': 'Duration spent on the SC READY writing test, which could relate to performance on this specific assessment.',
    'STATE_ELA_SCORE': 'Specific score from the state-administered ELA assessments.',
    'STATE_MATH_SCORE': 'Specific score from the state-administered math assessments.'
}

# Sidebar filters
st.sidebar.title("Longitudinal data report for all Assessment")

# Filter by school district
districts = df['SCHOOL_DISTRICT_ID'].unique()
selected_district = st.sidebar.selectbox('Select School District', ['All'] + list(districts))

if selected_district != 'All':
    df = df[df['SCHOOL_DISTRICT_ID'] == selected_district]

# Filter by school
schools = df['SCHOOL_ID'].unique()
selected_school = st.sidebar.selectbox('Select School', ['All'] + list(schools))

if selected_school != 'All':
    df = df[df['SCHOOL_ID'] == selected_school]

# Filter by student
students = df['STUDENT_ID'].unique()
selected_student = st.sidebar.selectbox('Select Student', ['All'] + list(students))

if selected_student != 'All':
    df = df[df['STUDENT_ID'] == selected_student]

# Select assessment type
selected_assessment = st.sidebar.selectbox('Select Assessment Type', list(assessment_descriptions.keys()))

# Display assessment description
st.sidebar.write("**Assessment Description:**")
st.sidebar.write(assessment_descriptions[selected_assessment])

# Ensure DATE is in datetime format
df['DATE'] = pd.to_datetime(df['DATE'])

# Filter data for the selected assessment
if not df.empty and selected_assessment in df.columns:
    # Group by DATE and calculate mean for the selected assessment
    trend_df = df.groupby('DATE')[selected_assessment].mean().reset_index()

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(trend_df['DATE'], trend_df[selected_assessment], marker='o', label=selected_assessment)
    plt.title(f'Longitudinal Data Report for {assessment_descriptions[selected_assessment]}')
    plt.xlabel('Date')
    plt.ylabel(selected_assessment)
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()
    st.pyplot(plt)

else:
    st.warning("No data available for the selected filters or assessment type.")
