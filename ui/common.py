import streamlit as st
from collections import namedtuple


user_info = namedtuple("user_info", ["username"])


def set_user_info(username: str):
    st.session_state.update({"user_info": user_info(username)})


def get_user_info():
    user_info = st.session_state.get("user_info", None)
    if isinstance(user_info, dict):
        return None
    return user_info