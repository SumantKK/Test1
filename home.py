import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Load data from Excel files
@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

# Define home page function
def home_page():
    st.image('construction.png', use_column_width=True)
    st.title('Tile Adhesive Solution')
    st.write('Welcome to Tile Adhesive Solution!')
    st.write('This web application helps you check the availability of materials from different brands and areas.')
    st.write('We analyze data to provide insights into the availability of tile adhesives in various shops and locations.')
    st.write('Explore the features to find the best solution for your needs.')

    st.write('Description:')
    st.write('- Analyze availability of materials from different brands and areas.')
    st.write('- Predict quantity required based on user inputs.')
    st.write('- Estimate area coverage and total weight of tile adhesives.')

    st.write('Benefits:')
    st.write('- Efficiently find the right tile adhesive for your project.')
    st.write('- Save time by predicting quantity requirements.')
    st.write('- Make informed decisions based on availability and estimated coverage.')

# Main function to build the web app
def main():
    # Load data
    survey_data = load_data("Survey.xlsx")
    builders_data = load_data("Builders Data.xlsx")
    
    # Sidebar
    st.sidebar.title('Features')
    feature_select = st.sidebar.selectbox('Select Feature', ['Home', 'Shop Name', 'Brand Name', 'Region (Address)', 'Prediction Model'])

    if feature_select == 'Home':
        home_page()
    elif feature_select == 'Shop Name':
        if 'Shop Name' in survey_data.columns:
            # Shop Name selection
            shop_name = st.sidebar.selectbox('Select Shop Name', options=survey_data['Shop Name'].unique(), format_func=lambda x: x, index=0)
            filtered_data = survey_data[survey_data['Shop Name'] == shop_name]
            # Display selected columns
            st.write(filtered_data[['Shop Name', 'Brand', 'Type', 'Address', 'Approx Price Range', 'Quantity Available (Bags 20Kg)', 'Quantity Available (Bags 10Kg)']])
        else:
            st.sidebar.write("Shop Name data not found.")
    elif feature_select == 'Brand Name':
        if 'Brand' in survey_data.columns:
            # Brand Name selection
            brand_name = st.sidebar.selectbox('Select Brand', options=survey_data['Brand'].unique(), format_func=lambda x: x, index=0)
            filtered_data = survey_data[survey_data['Brand'] == brand_name]
            # Display selected columns
            st.write(filtered_data[['Brand', 'Type', 'Address', 'Approx Price Range', 'Demand']])
        else:
            st.sidebar.write("Brand data not found.")
    elif feature_select == 'Region (Address)':
        if 'Address' in survey_data.columns:
            # Region (Address) selection
            address = st.sidebar.selectbox('Select Region (Address)', options=survey_data['Address'].unique(), format_func=lambda x: x, index=0)
            filtered_data = survey_data[survey_data['Address'] == address]
            # Display selected columns from the first Excel file
            st.write(filtered_data[['Shop Name', 'Brand', 'Type', 'Address', 'Approx Price Range', 'Quantity Available (Bags 20Kg)', 'Quantity Available (Bags 10Kg)']])
            
            # Filter and display data from the second Excel file (Builders Data.xlsx)
            if 'Address' in builders_data.columns:
                builders_filtered_data = builders_data[builders_data['Address'] == address]
                # Display selected columns from the second Excel file
                st.write("Builders Data:")
                st.write(builders_filtered_data[['Builder Name', 'Building Name', 'Address', 'Configuration', 'Project Type', 'Total Area (Sq Mt)', 'Bags Required (20 Kg)']])
            else:
                st.write("Builders Data not found.")
        else:
            st.sidebar.write("Region (Address) data not found.")
    else:
        st.sidebar.write('Prediction Model')
        
        # Get connected dropdown options
        shop_name = st.selectbox('Select Shop Name', options=survey_data['Shop Name'].unique(), format_func=lambda x: x, index=0)
        shop_name = st.selectbox('Select Address', options=survey_data['Address'].unique(), format_func=lambda x: x, index=0)
        brand_name = st.selectbox('Select Brand', options=survey_data[survey_data['Shop Name'] == shop_name]['Brand'].unique(), format_func=lambda x: x, index=0)
        type_options = survey_data[(survey_data['Shop Name'] == shop_name) & (survey_data['Brand'] == brand_name)]['Type'].unique()
        if len(type_options) > 0:
            selected_type = st.selectbox('Select Type', options=type_options, format_func=lambda x: x, index=0)
        else:
            st.write('Type not available in the store.')
            return
        
        # Use the selected address for predictions and for Builders Data filtering
        address = survey_data[(survey_data['Shop Name'] == shop_name) & (survey_data['Brand'] == brand_name)]['Address'].iloc[0]

        bags_20kg = st.selectbox('Quantity Required (Bags 20Kg)', options=[i for i in range(1, 101)], format_func=lambda x: str(x), index=0)
        bags_10kg = st.selectbox('Quantity Required (Bags 10Kg)', options=[i for i in range(1, 101)], format_func=lambda x: str(x), index=0)
        delivery_time = st.selectbox('Delivery Time (Days)', options=[i for i in range(1, 11)], format_func=lambda x: str(x), index=0)
        calculate_button = st.button('Calculate')

        prediction = None

        if calculate_button:
            # Define X and y for prediction
            X = survey_data[['Quantity Available (Bags 20Kg)', 'Quantity Available (Bags 10Kg)', 'Delivery Time (Days)']]
            y = survey_data['Total Quantity (30 Kg Bags)']

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train XGBoost model
            model = xgb.XGBRegressor()
            model.fit(X_train, y_train)

            # Make prediction
            prediction = model.predict([[bags_20kg, bags_10kg, delivery_time]])

            # Display prediction
            if prediction is not None:
                Value_Estimate = int(round(prediction[0]))
                st.write('Total Quantity (30 Kg Multiples or Bags):', Value_Estimate)
                st.write('Total Weight:', 30 * Value_Estimate)
                st.write('Estimated Area of Sq Meters it will cover:', int(round(30 * Value_Estimate / 7.5)))
        

if __name__ == '__main__':
    main()
