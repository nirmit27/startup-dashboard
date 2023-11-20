""" Introduction to Streamlit """

import time as t
import numpy as np
import pandas as pd
import streamlit as st

# Text ...
st.title('Text Utilities')
st.header('I am learning Streamlit.')

# st.subheader('... and I am loving it!')
# st.write('This is normal text.')

st.markdown("""
### My favourite movies 
- Raajneeti
- Jab Tak Hai Jaan
""")

st.code("""
def foo(n):
    return n**2
x = foo(2)
""")

st.subheader('This is how you write equations using LaTeX ...')
st.latex('x^2 + y^2 = 16')

st.divider()

# DataFrame ...
st.subheader('DataFrame creation ...')
df = pd.DataFrame({
    'name': ["Nirmit", "Akash", "Anurag"],
    'cgpa': [8.8, 8.7, 8.6],
    'package': [10, 20, 30]
})
df['index'] = pd.Series(np.linspace(1, 3, 3))
df.set_index('index', inplace=True)
st.dataframe(df)

# Metrics ...
st.metric('Revenue', 'Rs 3L', '-3%')

# JSON ...
st.json({
    'name': ["Nirmit", "Akash", "Anurag"],
    'cgpa': [8.8, 8.7, 8.6],
    'package': [10, 20, 30]
})
st.divider()

# Media ...
st.subheader('Say hello to Gojo!')
st.image(image='resources/gojo.jpg')

# Layout ...
st.sidebar.title('Sidebar')

st.subheader()

col1, col2 = st.columns(2)

with col1:
    st.image(image='resources/gojo.jpg')
with col2:
    st.image(image='resources/gojo.jpg')

# Messages ...
st.warning('Tread lightly!')

# Progress bar ...
bar = st.progress(0)
for i in range(1, 101):
    t.sleep(0.5)
    bar.progress(i)
st.divider()

# User input ...
# name = st.text_input('Enter name')
# age = st.number_input('Enter age')
# date = st.date_input('Enter registration date')

# File Uploading ...

# st.markdown("""
#     <h2 style="text-align: center; margin-bottom: 30px">
#     File Upload
#     </h2>
#     """, unsafe_allow_html=True)
#
#     file = st.file_uploader('Upload the dataset')
#
#     if file is not None:
#         df = pd.read_csv(file)
#         st.dataframe(df.describe())

# Login page layout ...

# st.title('Login Page')
#     st.markdown("""
#     <h2 style="text-align: center; margin-bottom: 30px">
#     Login Page
#     </h2>
#     """, unsafe_allow_html=True)
#
#     email = st.text_input('Enter email')
#     pwd = st.text_input('Enter password', type='password')
#     gender = st.selectbox('Select gender', ["Male", "Female", "Others"])
#
#     btn = st.button('Login')
#
#     if btn:
#         if email == 'example_27@gmail.com' and pwd == 'pwd12345':
#             # st.success('Login successful!')
#             st.balloons()
#         else:
#             st.error('Login failed!')
