import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Load data from Excel file
@st.cache_data  # Cache the data for better performance
def load_data(file_path):
    return pd.read_excel(file_path)

data = load_data("Survey.xlsx")

# Main function to build the web app
def main():
    st.title('Tile Adhesive Solution')
    st.write('Check availability for available materials of different brands and areas')

    # Sidebar
    st.sidebar.title('Features')
    feature_select = st.sidebar.selectbox('Select Feature', ['Shop Name', 'Brand Name', 'Pin Code', 'Prediction Model'])

    if feature_select == 'Shop Name':
        if 'Shop Name' in data.columns:
            shop_name = st.sidebar.selectbox('Select Shop Name', options=data['Shop Name'].unique(), format_func=lambda x: x, index=0)
            filtered_data = data[data['Shop Name'] == shop_name]
            st.write(filtered_data)
        else:
            st.sidebar.write("Shop Name data not found.")

    elif feature_select == 'Brand Name':
        if 'Brand' in data.columns:
            brand_name = st.sidebar.selectbox('Select Brand', options=data['Brand'].unique(), format_func=lambda x: x, index=0)
            filtered_data = data[data['Brand'] == brand_name]
            st.write(filtered_data)
        else:
            st.sidebar.write("Brand data not found.")

    elif feature_select == 'Pin Code':
        if 'Pin Code' in data.columns:
            pin_code = st.sidebar.selectbox('Select Pin Code', options=data['Pin Code'].unique(), format_func=lambda x: x, index=0)
            filtered_data = data[data['Pin Code'] == pin_code]
            st.write(filtered_data)
        else:
            st.sidebar.write("Pin Code data not found.")

    else:
        st.sidebar.write('Prediction Model')
        # Get connected dropdown options
        shop_name = st.selectbox('Select Shop Name', options=data['Shop Name'].unique(), format_func=lambda x: x, index=0)
        brand_name = st.selectbox('Select Brand', options=data[data['Shop Name'] == shop_name]['Brand'].unique(), format_func=lambda x: x, index=0)
        type_options = data[(data['Shop Name'] == shop_name) & (data['Brand'] == brand_name)]['Type'].unique()
        if len(type_options) > 0:
            selected_type = st.selectbox('Select Type', options=type_options, format_func=lambda x: x, index=0)
        else:
            st.write('Type not available in the store.')
            return
        
        pin_code = data[(data['Shop Name'] == shop_name) & (data['Brand'] == brand_name)]['Pin Code'].iloc[0]

        bags_20kg = st.selectbox('Quantity Required (Bags 20Kg)', options=[i for i in range(1, 101)], format_func=lambda x: str(x), index=0)
        bags_10kg = st.selectbox('Quantity Required (Bags 10Kg)', options=[i for i in range(1, 101)], format_func=lambda x: str(x), index=0)
        delivery_time = st.selectbox('Delivery Time (Days)', options=[i for i in range(1, 11)], format_func=lambda x: str(x), index=0)
        calculate_button = st.button('Calculate')

        prediction = None

        if calculate_button:
            # Define X and y for prediction
            X = data[['Pin Code', 'Quantity Available (Bags 20Kg)', 'Quantity Available (Bags 10Kg)', 'Delivery Time (Days)']]
            y = data['Total Quantity (30 Kg Bags)']

            # Train-test split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train XGBoost model
            model = xgb.XGBRegressor()
            model.fit(X_train, y_train)

            # Make prediction
            prediction = model.predict([[pin_code, bags_20kg, bags_10kg, delivery_time]])

            # Display prediction
            if prediction is not None:
                Value_Estimate = int(round(prediction[0]))
                st.write('Total Quantity (30 Kg Multiples or Bags) :',Value_Estimate)
                st.write('Total Weight :',30 * Value_Estimate)
                st.write('Estimated Area of Sq Meters it will cover:', int(round(30 * Value_Estimate/7.5)))

if __name__ == '__main__':
    main()
