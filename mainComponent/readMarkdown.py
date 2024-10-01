import streamlit as st


def ShowStMarkDown( markDownPath: str):
    with open(markDownPath) as md:
        content = md.read()
    st.markdown(content)