from ui import Component
import streamlit as st
from biz.user import get_user_by_username, init_user
from ui.common import set_user_info, get_user_info


class UserInitForm(Component):
    def __init__(self, session_key: str = ""):
        super().__init__(session_key)
        self.render_form()

    def render_form(self):
        with st.form("user_init_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Submit"):
                if (
                    user := get_user_by_username(username)
                ) is not None and not user.is_out_date() and password != user.password:
                    st.error("User already exists")
                else:
                    init_user(username, password)
                    st.info(f"User {username} created")
                    set_user_info(username)
                    st.rerun()


class UserInfo(Component):
    def __init__(self, session_key: str = ""):
        super().__init__(session_key)
        self.render()

    def render(self):
        user_info = get_user_info()
        if user_info is None:
            st.write("Please init user")
            UserInitForm(self.session_key + ".user_init_form")
        else:
            print(user_info)
            st.write(f"Hello, {user_info.username}")
            if st.toggle("Switch user"):
                UserInitForm(self.session_key + ".user_init_form")
