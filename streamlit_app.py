# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests 
# Write directly to the app
st.title(f":cup_with_straw: customize your profileSmoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie.
  """
)

# option = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
# )

#st.write("You selected:", option)


# option = st.selectbox(
#     "What is your Favourite Fruit ?",
#   ('Banana','strawnerries','Peaches')
# )

#st.write("You Favourite Fruit is :", option)

name_on_order=st.text_input('Name on Smoothie:')
st.write('Name on the smoothie will be:',name_on_order
)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe,use_container_width=True)
st.stop()


ingredients_list = st.multiselect('choose upto 5 ingredients:', my_dataframe,max_selections=5)

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen+'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    # Corrected SQL statement (fixing the quote typos)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) 
                        values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    st.write(my_insert_stmt)


time_to_insert=st.button('submit_order')
if time_to_insert :
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
 

