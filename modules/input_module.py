import streamlit as st

def get_student_input():

    st.header("Student Profile")

    interests = st.multiselect(
        "Select your interests",
        [
            "Mathematics",
            "Programming",
            "Technology",
            "Design",
            "Biology",
            "Communication",
            "Physics",
            "Business"
        ]
    )

    return interests