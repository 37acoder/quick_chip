import streamlit as st
from collections import namedtuple


UserInfo = namedtuple("user_info", ["user_id", "username"])


def set_user_info(user_id: int, username: str):
    st.session_state.update({"user_info": UserInfo(user_id, username)})
    clear_game_info()

def get_user_info():
    user_info = st.session_state.get("user_info", None)
    if isinstance(user_info, dict):
        return None
    return user_info


GameInfo = namedtuple("game_info", ["game_id", "game_name"])


def set_game_info(game_id: int, game_name: str):
    st.session_state.update({"game_info": GameInfo(game_id, game_name)})


def clear_game_info():
    st.session_state.update({"game_info": None})


def get_game_info():
    game_info = st.session_state.get("game_info", None)
    if isinstance(game_info, dict):
        return None
    return game_info
