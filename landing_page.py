import streamlit as st

def show_landing_page():
    # Set page configuration
    st.set_page_config(page_title="Tile Adhesive Solution", page_icon=":adhesive_bandage:", layout="wide", initial_sidebar_state="expanded")

    # Custom CSS to change background color
    st.markdown(
        """
        <style>
        .reportview-container {
            background: linear-gradient(to right top, #00416A, #E4E5E6);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.image('construction.py', use_column_width=True)
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
