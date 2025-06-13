# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Chooose the fruits you want in your Custom Smoothie!
  """
)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_input = st.text_input("Name on Smoothie")
st.write("The name on your smoothie will be:", name_input)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    # st.write("You selected:", ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string += fruit +' '
        st.subheader(fruit + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_input + """')"""

    time_on_insert = st.button('Submit Order')
    
    if time_on_insert:
        session.sql(my_insert_stmt).collect()

        order_stmt = """ Your Smoothie is ordered, """ + name_input + """!"""
        
        st.success(order_stmt, icon="✅")
