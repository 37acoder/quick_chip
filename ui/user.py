from ui import Component
import streamlit as st
from ui.common import set_user_info, get_user_info, clear_game_info
from models.core import User


class UserInitForm(Component):
    def __init__(self, session_key: str = ""):
        super().__init__(session_key)
        self.render_form()

    def render_form(self):
        with st.form("user_init_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Submit"):
                if (user := User.get_user_by_username(username)) is not None:
                    if user.is_out_date():
                        user.update_password(password)
                        st.info(f"User {username} login")
                        set_user_info(user._id, username)
                        st.rerun()
                    elif password == user.password:
                        set_user_info(user._id, username)
                        st.info("Login success")
                        st.rerun()
                    else:
                        st.error("User already exists and wrong password")
                else:
                    user = User.init_user(username, password)
                    st.info(f"User {username} created")
                    set_user_info(user._id, username)
                    st.rerun()
 

class UserInfo(Component):
    def __init__(self, session_key: str = ""):
        super().__init__(session_key)
        self.render()

    def render(self):
        user_info = get_user_info()
        with st.expander("User Login/Create", expanded=user_info is None):
            UserInitForm(self.session_key + ".user_init_form")
