import streamlit as st

def show_prediction_output(prediction):
    st.title('Prediction Output')
    if prediction is not None:
        Value_Estimate = int(round(prediction[0]))
        st.write('Total Quantity (30 Kg Multiples or Bags) :', Value_Estimate)
        st.write('Total Weight :', 30 * Value_Estimate)
        st.write('Estimated Area of Sq Meters it will cover:', int(round(30 * Value_Estimate / 7.5)))
