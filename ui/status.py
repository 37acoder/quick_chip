import streamlit as st
from ui.common import get_game_info, get_user_info, UserInfo, GameInfo
from ui import Component


class StatusPad(Component):
    def __init__(self, session_key: str = ""):
        super().__init__(session_key)
        st.title("Quick Chip ")
        st.subheader("for you borad game")
        st.divider()
        user_info = get_user_info()
        if user_info is None:
            user_info = UserInfo("not login", "not login")
        
        st.write(f"User info")
        st.dataframe(
            {
                "User ID": str([user_info.user_id]),
                "Username": [user_info.username],
            },
            width=200,
            hide_index=True,
        )
        game_info = get_game_info()
        if game_info is None:
            game_info = GameInfo("empty", "empty")

        st.write(f"Game info")
        st.dataframe(
            {
                "Game ID": str([game_info.game_id]),
                "Game Name": [game_info.game_name],
            },
            width=200,
            hide_index=True,
        )
        st.divider()