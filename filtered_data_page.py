import streamlit as st
import pandas as pd

def show_filtered_data_page(data):
    st.title('Filtered Data')
    st.write(data)
