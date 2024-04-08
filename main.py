import streamlit as st
from landing_page import show_landing_page
from filtered_data_page import show_filtered_data_page
from prediction_output_page import show_prediction_output
from sklearn.model_selection import train_test_split
import xgboost as xgb
import pandas as pd

# Load data from Excel file
@st.cache_data  # Cache the data for better performance
def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data("Survey.xlsx")

# Set page configuration for landing page
st.set_page_config(page_title="Tile Adhesive Solution", page_icon=":adhesive_bandage:", layout="wide", initial_sidebar_state="expanded")

def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox('Go to', ['Landing Page', 'Filtered Data', 'Prediction Output'])

    if page == 'Landing Page':
        show_landing_page()
    elif page == 'Filtered Data':
        show_filtered_data_page(data)
    elif page == 'Prediction Output':
        show_prediction_output(None)  # Replace None with actual prediction when available

if __name__ == '__main__':
    main()
