# Bike Sharing Data Analysis Project

**Author**: Fadli Shidqi Firdaus  
**Email**: fadlishidqifirdaus@gmail.com  
**ID Dicoding**: fadli26

## Project Overview

This project focuses on analyzing a bike-sharing dataset to gain insights into user behavior, including when bikes are most rented, the impact of weather, and differences between casual and registered users. The analysis was performed using Python, Pandas, and Streamlit for visualization.

## Questions to be Answered

1. On which day are users most likely to rent bikes, and on which day is the demand the lowest?
2. At what time of day does the largest spike in bike rentals occur?
3. Which season tends to be the most popular for bike rentals based on usage volume?
4. Is there a relationship between bike rentals and temperature or weather conditions?
5. Are there more casual users or registered users renting bikes?

## Project Structure

- **`app.py`**: This is the main Python script containing the analysis and visualizations, designed to be run via Streamlit.
- **`day.csv`**: The dataset containing daily bike rental information.
- **`hour.csv`**: The dataset containing hourly bike rental information.
- **`requirements.txt`**: Contains the necessary libraries and their versions for this project.

## Datasets

Both `hour.csv` and `day.csv` have the following fields (except for the `hr` column which is only in `hour.csv`):

- `instant`: Record index.
- `dteday`: Date.
- `season`: Season (1: spring, 2: summer, 3: fall, 4: winter).
- `yr`: Year (0: 2011, 1: 2012).
- `mnth`: Month (1 to 12).
- `hr`: Hour (0 to 23) – only in `hour.csv`.
- `holiday`: Whether the day is a holiday or not.
- `weekday`: Day of the week.
- `workingday`: 1 if the day is neither a weekend nor a holiday, otherwise 0.
- `weathersit`: Weather situation (1: Clear, 2: Mist, 3: Light Snow, 4: Heavy Rain).
- `temp`: Normalized temperature in Celsius.
- `atemp`: Normalized feeling temperature in Celsius.
- `hum`: Normalized humidity.
- `windspeed`: Normalized wind speed.
- `casual`: Count of casual users.
- `registered`: Count of registered users.
- `cnt`: Count of total rental bikes (casual + registered).

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/bike-sharing-analysis.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd bike-sharing-analysis
    ```

3. **Create a virtual environment**:
    ```bash
    virtualenv venv
    ```

4. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

## Data Cleaning Process

The following steps were taken to clean and preprocess the data:
- Unnecessary columns were dropped (`workingday`, `instant`, `atemp`, `holiday`).
- Columns were renamed for better clarity (e.g., `cnt` to `count_total`, `dteday` to `date_day`).
- Categorical columns were converted to more understandable names (e.g., season and weather situation).
- Date columns were converted to proper datetime format.
- Temperature, humidity, and wind speed were restored to their original scales.

## Analysis and Results

### 1. **Most and Least Frequent Days for Rentals**  
   - Days with the highest and lowest bike rentals were identified.

### 2. **Peak Rental Hours**  
   - The time of day with the highest rental activity was found.

### 3. **Popular Season for Rentals**  
   - The season with the most bike rentals was analyzed.

### 4. **Temperature and Weather Correlation**  
   - The relationship between weather, temperature, and bike rentals was explored.

### 5. **Comparison Between Casual and Registered Users**  
   - The total rentals were compared between casual and registered users.

## Visualizations

Several visualizations were created using Seaborn and Matplotlib, including:
- **Bar plots** to visualize total rentals by day and season.
- **Line plots** to show bike rental trends by hour.
- **Bar plots** to compare rentals by weather condition.
- **Bar plots** to compare rentals between casual and registered users.

## Deployment

This app is deployed on Streamlit Cloud. You can view the live version [here](https://yourappname.streamlit.app).

## Dependencies

- Python 3.x
- pandas
- seaborn
- matplotlib
- numpy
- streamlit

## Future Work

Possible future improvements for this analysis:
- Including more datasets to expand the scope of analysis.
- Integrating machine learning models to predict bike rental demand.

## Acknowledgments

Thanks to the creators of the dataset for providing the data, and to the open-source community for the libraries used in this project.

---

Feel free to clone and modify this project as you see fit. Contributions are always welcome!
