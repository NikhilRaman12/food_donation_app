# Food Donation Insights Dashboard

This project provides an interactive dashboard built with Streamlit to analyze food donation data stored in a SQLite database. The dashboard allows users to explore various aspects of the food donation process, including donation trends, claims, and potential wastage.

## Project Structure

```
.
├── app.py                  # Streamlit application code
├── requirements.txt        # List of required Python libraries
├── providers_data.csv      # Data for food providers
├── receivers_data.csv      # Data for food receivers
├── food_listings_data.csv  # Data for food listings (donations)
├── claims_data.csv         # Data for donation claims
└── README.md               # Project README file
```

## Setup Instructions

1.  **Prerequisites:**
    *   Ensure you have Python installed (version 3.6 or higher recommended).
    *   Ensure you have `pip` installed.

2.  **Clone the repository (or download files):**
    Download the project files (`app.py`, `requirements.txt`, and the `.csv` data files) to your local machine.

3.  **Install dependencies:**
    Navigate to the project directory in your terminal and install the required libraries using pip:

    ```bash
pip install -r requirements.txt
```

4.  **Obtain Data:**
    The necessary data is provided in the `.csv` files (`providers_data.csv`, `receivers_data.csv`, `food_listings_data.csv`, `claims_data.csv`). These files will be used by the `app.py` script to create the SQLite database (`food_donation.db`) automatically when the application is run for the first time.

## Running the Streamlit App

1.  **Navigate to the project directory:**
    Open your terminal or command prompt and change your current directory to the folder where you saved the project files.

2.  **Run the Streamlit application:**
    Execute the following command:

    ```bash
streamlit run app.py
```

3.  **Access the dashboard:**
    Your web browser should open automatically to display the Streamlit dashboard (usually at `http://localhost:8501`). If it doesn't, open your browser and go to that address.

## Features

The dashboard provides insights into:

*   Total number of food donations and claims
*   Distribution of donations by food type and meal type
*   Top providers and receivers by donation/claim count
*   Analysis of unclaimed and expired food (wastage)
*   City-wise donation and claim analysis
*   Monthly trends in donations and claims

## Contact

For any questions or issues, please contact https://www.linkedin.com/in/nikhil-raman-k-448589201/

