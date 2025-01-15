# Workout Report and Visualizations

This Streamlit app displays your workout history and visualizations based on data from Mindbody.com.


## Features

- Display workout history
- Visualize workout data
- Filter workouts by class name and date range

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to view the app.

## Data Preparation

The extracted data is cleaned and preprocessed to ensure it is in a suitable format for analysis. This includes:
- Converting the `time_of_day` column to string and handling missing values.
- Converting the `month` and `year` columns to string.
- Handling missing values in the `class_name` column.
- Extracting the location from the `location` column.

## Feature Building

The following features are built to enhance the analysis:
- **Number of Classes per Year**: A bar chart showing the number of classes each year.
- **Class Distribution by Time of Day**: A visualization showing the distribution of classes throughout the day.
- **Class Attendance Trends**: Analysis of attendance trends over time.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

&copy; CodeRod Solutions LLC