import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv(r'C:\Users\DELL\Documents\02_consults\code2\school_student_data.csv')

# Sidebar filters
st.sidebar.header("Filter Data")

# Filter for School District
districts = df['SCHOOL_DISTRICT_ID'].unique().tolist()
selected_district = st.sidebar.selectbox("Select School District", ['All'] + districts)

# Filter for School
if selected_district != 'All':
    schools = df[df['SCHOOL_DISTRICT_ID'] == selected_district]['SCHOOL_ID'].unique().tolist()
else:
    schools = df['SCHOOL_ID'].unique().tolist()

selected_school = st.sidebar.selectbox("Select School", ['All'] + schools)

# Filter for Student ID
if selected_school != 'All':
    students = df[df['SCHOOL_ID'] == selected_school]['STUDENT_ID'].unique().tolist()
else:
    students = df['STUDENT_ID'].unique().tolist()

selected_student = st.sidebar.selectbox("Select Student ID", ['All'] + students)

# Filter for Grade
grades = df['GRADE'].unique().tolist()
selected_grade = st.sidebar.selectbox("Select Grade", ['All'] + grades)

# Filter for Date Range
date_range = st.sidebar.date_input("Select Date Range", [])
start_date = min(date_range) if date_range else None
end_date = max(date_range) if date_range else None

# Apply filters to the DataFrame
filtered_df = df.copy()

if selected_district != 'All':
    filtered_df = filtered_df[filtered_df['SCHOOL_DISTRICT_ID'] == selected_district]

if selected_school != 'All':
    filtered_df = filtered_df[filtered_df['SCHOOL_ID'] == selected_school]

if selected_student != 'All':
    filtered_df = filtered_df[filtered_df['STUDENT_ID'] == selected_student]

if selected_grade != 'All':
    filtered_df = filtered_df[filtered_df['GRADE'] == selected_grade]

if start_date and end_date:
    filtered_df['DATE'] = pd.to_datetime(filtered_df['DATE'])
    filtered_df = filtered_df[(filtered_df['DATE'] >= pd.to_datetime(start_date)) & (filtered_df['DATE'] <= pd.to_datetime(end_date))]

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Function to plot longitudinal data with benchmarks
def plot_longitudinal_data_with_benchmark(y_column, y_label, benchmark_value):
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
        return

    trend_df = filtered_df.groupby('DATE')[y_column].mean().reset_index()

    if trend_df.empty:
        st.write("No data available for the selected filters.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(trend_df['DATE'], trend_df[y_column], marker='o', label='Actual')
    
    # Add benchmark line
    plt.axhline(y=benchmark_value, color='r', linestyle='--', label='Benchmark')
    
    plt.title(f'Longitudinal Analysis of {y_label}')
    plt.xlabel('Date')
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

# Set benchmark values (these can be customized or loaded from another source)
attendance_benchmark = 90  # example benchmark for attendance
participation_benchmark = 75  # example benchmark for participation rate

# Plot Attendance and Participation Rate with Benchmarks
if st.sidebar.button("Plot Attendance"):
    plot_longitudinal_data_with_benchmark('ATTENDANCE', 'Attendance', attendance_benchmark)

if st.sidebar.button("Plot Participation Rate"):
    plot_longitudinal_data_with_benchmark('PARTICIPATION_RATE', 'Participation Rate', participation_benchmark)