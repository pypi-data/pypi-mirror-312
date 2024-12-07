from datetime import datetime

import streamlit as st
from streamlit_timeago import time_ago

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run streamlit_time_ago/example.py`

st.subheader("Time ago component")

# Create an instance of our component with a constant `name` arg, and
# print its output value.
time_ago(datetime.now(), prefix='Submitted:')

st.write('Submitted: just now')
