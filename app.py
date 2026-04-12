import streamlit as st
from src.recommender import recommend
from modules.input_module import get_student_input

st.title("Talent Map - Career Recommendation")

user = get_student_input()

if st.button("Recommend Career"):

    result = recommend(user)

    st.subheader("Top Career Matches")

    for job, score in result.items():
        st.write(job, ":", round(score, 3))