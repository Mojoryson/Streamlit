# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap
from matplotlib.ticker import FuncFormatter

# File Path
file_path = "data/workout_history_cleaned.csv"

# Load the data
df = pd.read_csv(file_path)
df["time_of_day"] = df["time_of_day"].astype(str).replace("NaT", "Unknown")
df["month"] = df["month"].astype(str)
df["year"] = df["year"].astype(str)
df["class_name"] = df["class_name"].fillna("Unknown")

# Extract everything before 'w/ ' or similar patterns
df['location'] = df['location'].str.extract(r"^(.*?)(?:, LLC\.| w/|$)")[0].str.strip()

# Title and Description
st.title("Workout Report and Visualizations")
st.write(
    "This app displays your workout history and visualizations based on data from Mindbody.com."
)
st.write("### Data Range: January 2017 to December 2024")


# Sidebar Filters
# List of classes to exclude
excluded_classes = ["Unknown", "Boot Camp", "Fighting Mastery™", "Valente Brothers Seminar Adults",
                    "Adult VB Seminar", "Fighting Foundations™"] 

# Filter the class_name column to exclude specific classes
available_classes = df["class_name"].unique()
filtered_classes = [cls for cls in available_classes if cls not in excluded_classes]

# Sidebar Filters
st.sidebar.header("Filter Options")

# Multi-select for year
selected_year = st.sidebar.multiselect(
    "Select Year", sorted(df["year"].unique()), default=df["year"].unique()
)

# Add vertical space
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Multi-select for location
location = st.sidebar.multiselect(
    "Select Location", sorted(df["location"].unique()), default=df["location"].unique()
)

# Add vertical space
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# Multi-select for filtered class names
selected_class = st.sidebar.multiselect(
    "Select Class", filtered_classes, default=filtered_classes
)

# Apply Filters
filtered_df = df[
    (df["year"].isin(selected_year)) & 
    (df["class_name"].isin(selected_class) & 
     (df["location"].isin(location)))
]

with st.container():
    with st.expander("View the data"):
        st.write( """
                The data below is an export from 
                Mindbody.com. It contains the workout history
                & was done using BeautifulSoup. 
                """)
        st.dataframe(df)


if filtered_df.empty:
    st.write("### No data available for the selected filters.")
else:
# Key Metrics
    with st.container():
        st.write("### Key Metrics")
        total_sessions = len(filtered_df)
        total_duration_minutes = filtered_df["duration"].sum()
        avg_duration_minutes = filtered_df["duration"].mean()

        # Convert duration to hours
        total_duration_hours = total_duration_minutes / 60
        avg_duration_hours = avg_duration_minutes / 60

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Sessions", total_sessions)
        col2.metric("Total Duration (hours)", f"{total_duration_hours:,.2f}")
        col3.metric("Avg Duration (hours)", f"{avg_duration_hours:.2f}")
        col4.metric("Total Duration (mins)", f"{total_duration_minutes:,.0f}")

    # Class Frequency Bar Chart
    with st.container():
        st.write("### Class Frequency")
        class_counts = filtered_df["class_name"].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=class_counts.index, y=class_counts.values, palette="viridis", ax=ax)
        ax.set_title("Class Frequency", fontsize=12)
        ax.set_xlabel("Class Name", fontsize=10)
        ax.set_ylabel("Count", fontsize=10)

        # Wrap and rotate x-axis labels
        wrapped_labels = [textwrap.fill(label, 10) for label in class_counts.index]
        rotation_angle = 45 if len(class_counts) > 5 else 0
        ax.set_xticklabels(wrapped_labels, rotation=rotation_angle, ha="right", fontsize=8)

        # Format y-axis for better readability
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"))
        ax.set_ylim(0, class_counts.max() * 1.1)
        st.pyplot(fig)

    # Sessions Over Time Line Chart
    with st.container():
        st.write("### Sessions Over Time")
        filtered_df["date"] = pd.to_datetime(
            filtered_df["year"] + " " + filtered_df["month"], format="%Y %B"
        )
        sessions_over_time = filtered_df.groupby("date").size()
        fig, ax = plt.subplots()
        sessions_over_time.plot(ax=ax, title="Sessions Over Time", marker="o")
        ax.set_ylabel("Number of Sessions")
        st.pyplot(fig)

    # Heatmap for Popular Time of Day
    with st.container():
        st.write("### Popular Time of Day")
        filtered_df["time_of_day"] = filtered_df["time_of_day"].str.extract(r"(\d+:\d+\w+)").fillna("Unknown")
        time_counts = filtered_df["time_of_day"].value_counts().sort_index()

        fig, ax = plt.subplots()
        sns.heatmap(
            [time_counts.values],
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=time_counts.index,
        )
        ax.set_title("Session Popularity by Time of Day", fontsize=12)
        ax.set_xticklabels(time_counts.index, rotation=30, ha="right", fontsize=9)
        st.pyplot(fig)
