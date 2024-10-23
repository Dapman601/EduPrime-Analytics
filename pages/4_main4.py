import pandas as pd
import streamlit as st
import plotly.express as px

# Load the data from the specified path
@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')  # Your dataset path
    return df

df = load_data()

st.title('Student Grouping Based on Assessment and Demographic Data')



# Replace known non-numeric values with NaN before conversion
df['FINAL_GRADES'] = df['FINAL_GRADES'].replace({'On Track': None, 'Not On Track': None})

# Ensure columns are numeric (convert non-numeric to NaN)
def ensure_numeric(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert non-numeric to NaN
    return df.dropna(subset=columns)  # Drop rows where any of the numeric columns are NaN

# Define numeric columns
numeric_columns = ['FINAL_GRADES', 'MATH_SCORE', 'STATE_MATH_PROFICIENCY', 'STATE_ELA_SCORE']

# Ensure only numeric values are used, excluding 'On Track' or similar entries
df = ensure_numeric(df, numeric_columns)



# Filter by demographic data
with st.sidebar:
    st.header("Demographic Filters")

    # District ID filter
    district_id_filter = st.selectbox("Select School District ID", options=["All"] + df['SCHOOL_DISTRICT_ID'].unique().tolist())
    
    # Update school ID options based on selected district
    if district_id_filter != "All":
        district_schools = df[df['SCHOOL_DISTRICT_ID'] == district_id_filter]['SCHOOL_ID'].unique()
    else:
        district_schools = df['SCHOOL_ID'].unique()
    
    school_id_filter = st.selectbox("Select School ID", options=["All"] + district_schools.tolist())
    
    # Grade, Gender, and Ethnicity filters
    grade_filter = st.selectbox("Select Grade", options=["All"] + df['GRADE'].unique().tolist())
    gender_filter = st.selectbox("Select Gender", options=["All"] + df['GENDER'].unique().tolist())
    ethnicity_filter = st.selectbox("Select Ethnicity", options=["All"] + df['ETHNICITY'].unique().tolist())

# Apply filters to the data
if district_id_filter != "All":
    df = df[df['SCHOOL_DISTRICT_ID'] == district_id_filter]
if school_id_filter != "All":
    df = df[df['SCHOOL_ID'] == school_id_filter]
if grade_filter != "All":
    df = df[df['GRADE'] == grade_filter]
if gender_filter != "All":
    df = df[df['GENDER'] == gender_filter]
if ethnicity_filter != "All":
    df = df[df['ETHNICITY'] == ethnicity_filter]

# Grouping by Performance - using FINAL_GRADES for student tiering
def classify_tier(final_grade):
    if pd.isna(final_grade):
        return "No Data"
    elif final_grade < 40:
        return "Tier 4 (Severe Remediation)"
    elif final_grade < 50:
        return "Tier 3 (Moderate Remediation)"
    elif final_grade < 60:
        return "Tier 2 (Needs Improvement)"
    else:
        return "On Track"

# Apply the classification based on FINAL_GRADES
df['Tier'] = df['FINAL_GRADES'].apply(classify_tier)

st.header('Students Grouped by Tiers')

# Show grouped students
grouped_df = df.groupby('Tier').size().reset_index(name='Number of Students')

# Plot the distribution of students across tiers
fig = px.bar(grouped_df, x='Tier', y='Number of Students', title='Students Distribution by Tiers')
st.plotly_chart(fig)

# Allow users to see detailed data for each group
selected_tier = st.selectbox("Select Tier to View Student Details", options=df['Tier'].unique())
tier_students = df[df['Tier'] == selected_tier]

st.write(f"### Students in {selected_tier}")
st.dataframe(tier_students[['STUDENT_ID', 'SCHOOL_NAME', 'GRADE', 'GENDER', 'ETHNICITY', 'FINAL_GRADES']])

# Optionally, add another analysis for ELA scores
if st.checkbox("Show ELA Tier Grouping"):
    df['ELA_Tier'] = df['STATE_ELA_SCORE'].apply(classify_tier)
    st.write(df[['STUDENT_ID', 'GRADE', 'GENDER', 'STATE_ELA_SCORE', 'ELA_Tier']])
