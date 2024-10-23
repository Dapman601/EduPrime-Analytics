import pandas as pd
import streamlit as st

# Load the dataset
df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')


# Sidebar filters
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

# Automatically update the grade selection based on the selected school, "All" option first
grades = ["All"] + school_df['GRADE'].unique().tolist()
selected_grade = st.sidebar.selectbox("Select Grade:", grades)

# Filter DataFrame based on the selected grade
if selected_grade == "All":
    grade_df = school_df
else:
    grade_df = school_df[school_df['GRADE'] == selected_grade]

# Section: Testing History of Students
st.title("Testing History of Students")

# Get current year and last year from the dataset
years = df['DATE'].apply(lambda x: str(x).split('-')[0]).unique()
if len(years) > 1:
    current_year = max(years)
    last_year = str(int(current_year) - 1)
else:
    current_year = max(years)
    last_year = None

st.write(f"### Current Test Year: {current_year}")
if last_year:
    st.write(f"### Last Test Year: {last_year}")

# Filter data for current year and last year
current_year_df = grade_df[grade_df['DATE'].str.startswith(current_year)]
last_year_df = grade_df[grade_df['DATE'].str.startswith(last_year)] if last_year else pd.DataFrame()

# Display test results for the current year
st.write("### Current Year Test Results")

if not current_year_df.empty:
    st.dataframe(current_year_df[['STUDENT_ID', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']])
else:
    st.write("No data available for the current year.")

# Enrollment in special programs for current year
st.write("### Special Programs Enrollment (Current Year)")
if 'SPECIAL_EDUCATION_STATUS' in current_year_df.columns:
    special_programs_current = current_year_df[current_year_df['SPECIAL_EDUCATION_STATUS'].notnull()]
    st.dataframe(special_programs_current[['STUDENT_ID', 'SPECIAL_EDUCATION_STATUS']])
else:
    st.write("No data available for special program enrollment.")

# Display test results for last year
if last_year:
    st.write("### Last Year Test Results")
    if not last_year_df.empty:
        st.dataframe(last_year_df[['STUDENT_ID', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']])
    else:
        st.write("No data available for the last year.")

# Enrollment in special programs for last year
if last_year and 'SPECIAL_EDUCATION_STATUS' in last_year_df.columns:
    st.write("### Special Programs Enrollment (Last Year)")
    special_programs_last = last_year_df[last_year_df['SPECIAL_EDUCATION_STATUS'].notnull()]
    st.dataframe(special_programs_last[['STUDENT_ID', 'SPECIAL_EDUCATION_STATUS']])
else:
    st.write("No data available for special program enrollment for the last year.")

# Comparison of current year and last year's test scores
if not current_year_df.empty and not last_year_df.empty:
    st.write("### Comparison of Test Results (Current vs Last Year)")
    
    comparison_df = pd.merge(current_year_df[['STUDENT_ID', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']],
                             last_year_df[['STUDENT_ID', 'STATE_ELA_SCORE', 'STATE_MATH_SCORE', 'SCIENCE_SCORE']],
                             on='STUDENT_ID',
                             suffixes=('_current', '_last'))
    
    st.dataframe(comparison_df)
else:
    st.write("No comparison data available.")

# Download option for testing history
st.write("### Download Testing History")
csv = current_year_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Current Year Test Results as CSV",
    data=csv,
    file_name=f'test_results_{current_year}.csv',
    mime='text/csv',
)
