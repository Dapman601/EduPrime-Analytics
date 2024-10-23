import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv(r'C:\Users\DELL\Documents\02_consults\code2\school_student_data.csv')

# Filter necessary columns from the dataset for ELA Proficiency
# Ensure that the dataset has a column for the year and a column for ELA proficiency percentage
if 'STATE_ELA_PROFICIENCY' in df.columns and 'GRADE' in df.columns:
    ela_df = df[df['GRADE'].between(3, 8)]  # Filter grades 3-8
    ela_df = ela_df.groupby('DATE')['STATE_ELA_PROFICIENCY'].mean().reset_index()
else:
    st.error("The dataset does not contain the required 'STATE_ELA_PROFICIENCY' and 'GRADE' columns.")
    st.stop()

# Initial goal values
start_year = 2023
end_year = 2030
start_percentage = 34.0
end_percentage = 65.0

# Sidebar for input of yearly ELA proficiency data
st.sidebar.title("Enter Yearly ELA Proficiency Results")

# Collecting actual ELA proficiency for the given years
yearly_data = {}
for year in range(start_year, end_year + 1):
    if year in ela_df['DATE'].values:
        actual_value = ela_df[ela_df['DATE'] == year]['STATE_ELA_PROFICIENCY'].values[0]
        yearly_data[year] = st.sidebar.number_input(f"ELA Proficiency for {year}", value=float(actual_value), min_value=0.0, max_value=100.0, step=0.1)
    else:
        yearly_data[year] = st.sidebar.number_input(f"ELA Proficiency for {year}", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

# Goal details
st.title("ELA Proficiency Growth Tracker (Grades 3-8)")
st.write(f"**Goal**: Increase the percentage of proficient students in grades 3-8 from **{start_percentage}%** in August {start_year} to **{end_percentage}%** by August {end_year}.")

# Create a dataframe to track both actual and target proficiency levels
data = {
    "Year": list(range(start_year, end_year + 1)),
    "Target ELA Proficiency (%)": [start_percentage + (end_percentage - start_percentage) * (year - start_year) / (end_year - start_year) for year in range(start_year, end_year + 1)],
    "Actual ELA Proficiency (%)": [yearly_data[year] for year in range(start_year, end_year + 1)]
}
progress_df = pd.DataFrame(data)

# Plotting the target and actual proficiency levels using Plotly
fig = go.Figure()

# Add target line
fig.add_trace(go.Scatter(
    x=progress_df['Year'], y=progress_df['Target ELA Proficiency (%)'],
    mode='lines+markers',
    name='Target ELA Proficiency',
    line=dict(color='green', dash='dash'),
    marker=dict(color='green')
))

# Add actual line
fig.add_trace(go.Scatter(
    x=progress_df['Year'], y=progress_df['Actual ELA Proficiency (%)'],
    mode='lines+markers',
    name='Actual ELA Proficiency',
    line=dict(color='blue'),
    marker=dict(color='blue')
))

# Customize the layout
fig.update_layout(
    title="ELA Proficiency Progress (Grades 3-8)",
    xaxis_title="Year",
    yaxis_title="Proficiency (%)",
    yaxis_range=[0, 100],
    showlegend=True,
    legend_title_text='Proficiency Levels',
)

# Display the figure
st.plotly_chart(fig)

# Display current year proficiency vs target
current_year = st.selectbox("Select the current year to compare progress:", options=list(range(start_year, end_year + 1)))
current_proficiency = yearly_data[current_year]
target_proficiency = progress_df[progress_df['Year'] == current_year]['Target ELA Proficiency (%)'].values[0]

st.metric(label=f"Current Year ({current_year}) ELA Proficiency", value=f"{current_proficiency}%")
st.metric(label=f"Target ELA Proficiency for {current_year}", value=f"{target_proficiency}%")

# Display how far the current year is from the target
if current_proficiency < target_proficiency:
    st.write(f"The current proficiency is **{target_proficiency - current_proficiency}%** below the target for {current_year}.")
elif current_proficiency > target_proficiency:
    st.write(f"The current proficiency is **{current_proficiency - target_proficiency}%** above the target for {current_year}.")
else:
    st.write(f"The current proficiency meets the target for {current_year}.")

# Display a download button for the progress data
csv = progress_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Progress Data as CSV",
    data=csv,
    file_name='ela_proficiency_progress.csv',
    mime='text/csv',
)
