import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('https://raw.githubusercontent.com/Dapman601/EduPrime-Analytics/refs/heads/main/school_student_data.csv')

# Sidebar filters with cascading behavior
def apply_filters(df):
    filtered_df = df.copy()

    # Sidebar Filters
    with st.sidebar:
        # School District Filter
        school_districts = ['All'] + sorted(df['SCHOOL_DISTRICT_ID'].dropna().unique().tolist())
        selected_district = st.selectbox('Select School District ID', school_districts, index=0)

        if selected_district != 'All':
            filtered_df = filtered_df[filtered_df['SCHOOL_DISTRICT_ID'] == selected_district]

        # School Filter (unique to selected district)
        unique_schools = ['All'] + sorted(filtered_df['SCHOOL_NAME'].dropna().unique().tolist())
        selected_school = st.selectbox('Select School', unique_schools, index=0)

        if selected_school != 'All':
            filtered_df = filtered_df[filtered_df['SCHOOL_NAME'] == selected_school]

        # Student ID Filter (unique to selected school)
        unique_students = ['All'] + sorted(filtered_df['STUDENT_ID'].dropna().unique().tolist())
        selected_student = st.selectbox('Select Student ID', unique_students, index=0)

        if selected_student != 'All':
            filtered_df = filtered_df[filtered_df['STUDENT_ID'] == selected_student]

        # Additional filters
        lea_categories = ['All'] + sorted(filtered_df['LEA_CATEGORY'].dropna().unique().tolist())
        selected_lea_category = st.selectbox('Select LEA Category', lea_categories, index=0)

        if selected_lea_category != 'All':
            filtered_df = filtered_df[filtered_df['LEA_CATEGORY'] == selected_lea_category]

        counties = ['All'] + sorted(filtered_df['COUNTY'].dropna().unique().tolist())
        selected_county = st.selectbox('Select County', counties, index=0)

        if selected_county != 'All':
            filtered_df = filtered_df[filtered_df['COUNTY'] == selected_county]

        cities = ['All'] + sorted(filtered_df['CITY'].dropna().unique().tolist())
        selected_city = st.selectbox('Select City', cities, index=0)

        if selected_city != 'All':
            filtered_df = filtered_df[filtered_df['CITY'] == selected_city]

    return filtered_df

# Apply the filters
filtered_df = apply_filters(df)

# Strategic goals for metrics
strategic_goals = {
    'Attendance': 95,
    'Participation Rate': 80,
    'Time Spent': 1000,  # Example strategic goal for time spent (in minutes)
}

# Function to plot longitudinal data and compare with strategic goals
def plot_longitudinal_data(metric, column_name):
    st.subheader(f"{metric} Over Time")

    if column_name in filtered_df.columns:
        # Group data by 'DATE' and calculate the mean for the selected column
        trend_df = filtered_df.groupby('DATE')[column_name].mean().reset_index()

        if not trend_df.empty:
            # Plot the trend data
            fig = px.line(trend_df, x='DATE', y=column_name, title=f'{metric} Longitudinal Trends')
            st.plotly_chart(fig)

            # Compare with strategic goal
            st.subheader(f"Alignment to Strategic Goals for {metric}")
            goal = strategic_goals.get(metric, None)

            if goal:
                latest_value = trend_df[column_name].iloc[-1]  # Fetch the latest value
                st.write(f"Strategic Goal: {goal}%")
                st.write(f"Latest Value: {latest_value}%")

                # Compare the latest value with the goal and display messages accordingly
                if latest_value >= goal:
                    st.success(f"The {metric} metric is aligned with the strategic goal!")
                else:
                    st.warning(f"The {metric} metric is below the strategic goal. Consider taking action.")
            else:
                st.write("No strategic goal set for this metric.")
        else:
            st.warning(f"No data available for {metric} in the selected filters.")
    else:
        st.error(f"Data for {metric} is not available.")

# Streamlit app structure
st.title("Student Outcomes Dashboard")

# Plot Attendance, Participation Rate, and Time Spent data with filters
plot_longitudinal_data('Attendance', 'ATTENDANCE')
plot_longitudinal_data('Participation Rate', 'PARTICIPATION_RATE')
plot_longitudinal_data('Time Spent', 'TIME_SPENT')
