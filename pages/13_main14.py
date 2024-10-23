import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')

# Set the page config
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #000000; /* Set background to black */
        color: #FFFFFF; /* Text color */
    }
    .stButton > button {
        background-color: #1DB954; /* Spotify Green */
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 10px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #1ed760; /* Lighter Green on hover */
    }
    .stSelectbox, .stMultiselect {
        background-color: #222222; /* Dark background for select boxes */
        color: #FFFFFF;
        border: 1px solid #1DB954;
    }
    .stSelectbox:hover, .stMultiselect:hover {
        border: 1px solid #1ed760;
    }
    .stMarkdown, .stHeader, .stSubheader {
        color: #FFFFFF; /* White text for headers */
    }
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #001f3f; /* Navy blue background for sidebar */
        color: #FFFFFF; /* Sidebar text color */
    }
    .css-1d391kg * {
        color: #FFFFFF !important; /* Ensure all text in the sidebar is white */
    }
    </style>
    """, unsafe_allow_html=True
)

# Title
st.title("🎓 Student Performance Dashboard")

# Sidebar
st.sidebar.title("🔍 Navigation")
options = [
    "Student Graduation Rate",
    "Graduate Indicators",
    "Seals of Distinction",
    "ML Student Progress Goals",
    "Pre-Accountability Dashboard",
    "Student Final Grades",
    "Superscore Results",
    "IEP, 504, ILAP Students"
]
selection = st.sidebar.selectbox("Select a report", options)

# District selection
districts = df['SCHOOL_DISTRICT_NAME'].unique().tolist()
selected_district = st.sidebar.selectbox("Select District", ['All'] + districts)

# Filter DataFrame based on selected district
if selected_district != 'All':
    df = df[df['SCHOOL_DISTRICT_NAME'] == selected_district]

# School selection based on selected district
schools = df['SCHOOL_NAME'].unique().tolist()
selected_school = st.sidebar.selectbox("Select School", ['All'] + schools)

# Filter DataFrame based on selected school
if selected_school != 'All':
    df = df[df['SCHOOL_NAME'] == selected_school]

# Student selection based on selected school
students = df['STUDENT_ID'].unique().tolist()
selected_student = st.sidebar.selectbox("Select Student", ['All'] + students)

# Filter DataFrame based on selected student
if selected_student != 'All':
    df = df[df['STUDENT_ID'] == selected_student]

# Create a function to display multiple charts in a grid
def display_charts(figures, titles):
    cols = st.columns(len(figures))
    for col, fig, title in zip(cols, figures, titles):
        with col:
            st.subheader(title)
            st.plotly_chart(fig, use_container_width=True)

# Dashboard for Student Graduation Rate
if selection == "Student Graduation Rate":
    graduation_status_counts = df['GRADUATION_STATUS'].value_counts().reset_index()
    graduation_status_counts.columns = ['Status', 'Count']

    # Create pie and bar charts
    pie_fig = px.pie(graduation_status_counts, 
                     names='Status', 
                     values='Count', 
                     title='Graduation Status Distribution', 
                     color='Status', 
                     template='plotly_dark',
                     color_discrete_sequence=px.colors.qualitative.Plotly)

    bar_fig = px.bar(graduation_status_counts, 
                     x='Status', 
                     y='Count', 
                     title='Graduation Status Count', 
                     color='Count', 
                     template='plotly_dark',
                     color_discrete_sequence=px.colors.qualitative.Plotly)

    display_charts([pie_fig, bar_fig], ["Graduation Status Pie Chart", "Graduation Status Bar Chart"])

# Display list of students with IEP, 504, or ILAP
if selection == "IEP, 504, ILAP Students":
    # Filter for students with IEP, 504, or ILAP status
    filtered_df = df[df['SPECIAL_EDUCATION_STATUS'].isin(['IEP', '504', 'ILAP'])]
    
    # Summary statistics
    total_students = filtered_df.shape[0]
    iep_count = filtered_df[filtered_df['SPECIAL_EDUCATION_STATUS'] == 'IEP'].shape[0]
    ilap_count = filtered_df[filtered_df['SPECIAL_EDUCATION_STATUS'] == 'ILAP'].shape[0]
    _504_count = filtered_df[filtered_df['SPECIAL_EDUCATION_STATUS'] == '504'].shape[0]

    st.write("### Summary of Students with IEP, 504, or ILAP")
    st.write(f"**Total Students:** {total_students}")
    st.write(f"**IEP Students:** {iep_count} ({(iep_count / total_students) * 100:.2f}%)")
    st.write(f"**504 Students:** {_504_count} ({(_504_count / total_students) * 100:.2f}%)")
    st.write(f"**ILAP Students:** {ilap_count} ({(ilap_count / total_students) * 100:.2f}%)")
    
    # Display the filtered students
    st.write("### List of Students with IEP, 504, or ILAP")
    st.dataframe(filtered_df[['STUDENT_ID', 'SCHOOL_NAME', 'SPECIAL_EDUCATION_STATUS']])

    # Download option
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name='iep_504_ilap_students.csv',
        mime='text/csv',
    )
