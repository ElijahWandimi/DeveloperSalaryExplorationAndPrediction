from itertools import count
import streamlit as st
import pickle
import numpy as np

def load_model():
    with open("saved_steps.pkl", "rb") as file:
        data = pickle.load(file)
    return data

data = load_model()

rf_model = data['model']
le_education = data['le_ed']
le_country = data['le_country']

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""Enter the required information below""")

    education_levels = ("Master's degree", "Bachelor's degree", "Less than Bachelor's", 'Post grad')
    countries = ('United States of America', 'Germany', 'United Kingdom of Great Britain and Northern Ireland',
                'India', 'Canada', 'France', 'Brazil', 'Spain', 'Netherlands', 'Australia', 'Italy', 'Poland', 'Sweden', 'Russian Federation',
                'Switzerland', 'Other')

    # selections for country,  education level and years of experience
    country = st.selectbox("Country", countries)
    education = st.selectbox("Education", education_levels)
    experience = st.slider("Years of experience", 0, 50, 2)

    btnOk = st.button("Predict salary")
    if btnOk:
        x = np.array([[country, education, experience]])
        x[:, 0] = le_country.fit_transform(x[:, 0])
        x[:, 1] = le_education.fit_transform(x[:, 1])
        x = x.astype(float)

        # predict
        salary = rf_model.predict(x)
        st.subheader(f"Your estimated salary is ${salary[0]:.2f} per year")
