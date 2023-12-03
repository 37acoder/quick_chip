import streamlit as st


class Component:
    def __init__(self, session_key: str = "") -> None:
        self.session_key = session_key or self.__class__.__name__
        if session_key not in st.session_state:
            st.session_state[self.session_key] = {}
        self.session = st.session_state[self.session_key]
