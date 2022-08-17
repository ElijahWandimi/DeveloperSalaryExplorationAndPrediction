import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, threshold):
    categerical_map = {}
    for c in range(len(categories)):
        if categories.values[c] >= threshold:
            categerical_map[categories.index[c]] = categories.index[c]
        else:
            categerical_map[categories.index[c]] = 'Other'
    return categerical_map

def clean_experience(years):
    if years == 'Less than 1 year':
        return 0.5
    if years == 'More than 50 years':
        return 50
    return float(years)


def clean_education(x):
    if "Master’s degree" in x:
        return "Master's degree"
    if "Bachelor’s degree" in x:
        return "Bachelor's degree"
    if "Professional degree" in x or "Other doctoral" in x:
        return "Post grad"
    return "Less than Bachelor's"


@st.cache
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    cols = ['Country', 'Employment','EdLevel', 'YearsCodePro', 'ConvertedCompYearly']
    df = df[cols]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['Employment'] == 'Employed, full-time']
    df.drop(['Employment'], axis=1, inplace=True)


    df = df[df['Salary'].isin(range(10000, 400000))]

    # applying funcs
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    return df
df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""
    ### Stackoverflow Developer Survey
    """)

    # pie chart for countries
    cnts = df['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(cnts, labels=cnts.index, autopct="%1.1f%%", shadow=True, startangle=45)
    ax1.axis('equal')

    st.write("""#### Number of data from different countries""")

    st.pyplot(fig1)

    st.write("""#### Mean salaries based on countries""")
    cnt_sal = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(cnt_sal)

    st.write("""### Mean salary based on years of experience""")
    cnt_ex = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(cnt_ex)
