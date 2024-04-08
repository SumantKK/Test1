import streamlit as st

def show_landing_page():
    st.image('your_image_path.jpg', use_column_width=True)
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
