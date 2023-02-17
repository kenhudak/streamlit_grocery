# streamlit_app.py

# Import Libraries
import streamlit as st
from gsheetsdb import connect
import pandas as pd
import plotly_express as px

# Page Configuration Must be first Streamlit call in Script
st.set_page_config(page_title="Windsor Grocery Prices",
        page_icon=":bread:",
        layout="wide")

# Create a connection object.
conn = connect()

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

# Print results.
#for row in rows:
#   st.write(f"{row.Store} has a :{row.Product}:")

# Put the Google Sheet rows into a Pandas Dataframe
df = pd.DataFrame(rows)

# Confirm that the data was read in properly.
# st.dataframe(df_selection)

# Sidebar section
st.sidebar.header("Select Food Here:")
food = st.sidebar.selectbox(
    "Select the Food:",
    options=df["Product"].unique()
)

df_selection = df.query(
    "Product == @food"
)



# --- Mainpage ---
st.title(":bar_chart: Windsor Basic Food Price Dashboard")
st.markdown("##")

fig = px.line(df_selection, x="Date", y="Price", color="Store", markers=True)
st.plotly_chart(fig)
