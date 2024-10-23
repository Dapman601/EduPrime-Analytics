import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')

# Ensure DATE column is in datetime format
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')



# Sidebar for filtering options
st.sidebar.header("Filter Data")

# Filter by District ID
district_id = st.sidebar.selectbox('Select School District ID', options=['All'] + df['SCHOOL_DISTRICT_ID'].unique().tolist())
if district_id != 'All':
    filtered_df = df[df['SCHOOL_DISTRICT_ID'] == district_id]
else:
    filtered_df = df.copy()

# Automatically detect schools in the selected district
schools_in_district = filtered_df['SCHOOL_NAME'].unique()
school_name = st.sidebar.selectbox('Select School', options=['All'] + schools_in_district.tolist())
if school_name != 'All':
    filtered_df = filtered_df[filtered_df['SCHOOL_NAME'] == school_name]

# Filter by demographic options
grade = st.sidebar.multiselect('Select Grade', options=['All'] + filtered_df['GRADE'].unique().tolist())
if 'All' in grade:
    grade = []
filtered_df = filtered_df[filtered_df['GRADE'].isin(grade)] if grade else filtered_df

ethnicity = st.sidebar.multiselect('Select Ethnicity', options=['All'] + filtered_df['ETHNICITY'].unique().tolist())
if 'All' in ethnicity:
    ethnicity = []
filtered_df = filtered_df[filtered_df['ETHNICITY'].isin(ethnicity)] if ethnicity else filtered_df

# Check if filtered_df is empty after filtering
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    # KPI options
    kpi_option = st.sidebar.selectbox(
        "Select Metric to View",
        options=['Attendance', 'State ELA Proficiency', 'State Math Proficiency', 'Behavior', 'Discipline']
    )

    # Define strategic goals (for demonstration purposes, these are made up)
    strategic_goals = {
        "Attendance": 90,  # Goal for attendance rate to be 90% or higher
        "State ELA Proficiency": 85,  # Goal for ELA proficiency to be at 85% or higher
        "State Math Proficiency": 85,  # Goal for Math proficiency to be at 85% or higher
        "Behavior": 10,  # Behavior incidents should stay below 10%
        "Discipline": 5   # Discipline incidents should stay below 5%
    }

    # Display longitudinal trends and comparisons with strategic plans
    def plot_longitudinal_data(metric):
        st.subheader(f"{metric} Over Time")
        
        # Prepare the DataFrame for the selected metric
        if metric == 'Attendance':
            trend_df = filtered_df.groupby('DATE')['ATTENDANCE'].mean().reset_index()
        elif metric == 'State ELA Proficiency':
            trend_df = filtered_df.groupby('DATE')['STATE_ELA_PROFICIENCY'].mean().reset_index()
        elif metric == 'State Math Proficiency':
            trend_df = filtered_df.groupby('DATE')['STATE_MATH_PROFICIENCY'].mean().reset_index()
        elif metric == 'Behavior':
            trend_df = filtered_df.groupby('DATE')['POSITIVE_BEHAVIORS'].mean().reset_index()
        elif metric == 'Discipline':
            trend_df = filtered_df.groupby('DATE')['MAJOR_CORRECTIVE'].mean().reset_index()

        # Check for empty DataFrame
        if trend_df.empty:
            st.warning("No data available for the selected metric.")
            return

        # Plotting
        fig = px.line(trend_df, x='DATE', y=trend_df.columns[1], title=f'{metric} Longitudinal Trends')
        st.plotly_chart(fig)

        # Compare with strategic goal
        st.subheader(f"Alignment to Strategic Goals for {metric}")
        goal = strategic_goals.get(metric, None)
        if goal is not None:
            latest_value = trend_df[trend_df.columns[1]].iloc[-1]  # Access the first y-axis column
            st.write(f"Strategic Goal: {goal}%")
            st.write(f"Latest Value: {latest_value}%")
            
            if latest_value >= goal:
                st.success(f"The {metric} metric is aligned with the strategic goal!")
            else:
                st.warning(f"The {metric} metric is below the strategic goal. Consider taking action.")
        else:
            st.write("No strategic goal set for this metric.")

    # Render the dashboard based on selected KPI
    plot_longitudinal_data(kpi_option)

# Footer
st.sidebar.write("Note: Longitudinal data reports generated based on filtered selections.")
