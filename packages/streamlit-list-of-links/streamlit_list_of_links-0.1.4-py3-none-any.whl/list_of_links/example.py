import streamlit as st
from list_of_links import list_of_links

st.subheader("Component with constant args")

people = ["Alice", "Bob", "Charlie", "David", "Eve"]
people_tuples = [(name, str(idx)) for idx, name in enumerate(people)]
link_target = list_of_links("World", people_tuples)
st.markdown("You chose link target %s!" % link_target)

st.markdown("---")
st.subheader("Component with variable args")

name_input = st.text_input("Enter a title", value="Streamlit")
link_target_2 = list_of_links(name_input, people_tuples, key="foo")
st.markdown("You chose link target %s!" % link_target_2)