from ui import Component
import streamlit as st
from rule.rule import GameBoard, Player
from ui.common import get_user_info, set_game_info, get_game_info


class InitGameForm(Component):
    def __init__(self, session_key: str) -> None:
        super().__init__(session_key)

    def render(self) -> None:
        game_info = get_game_info()
        with st.expander("Create or join Game", expanded=game_info is None):
            op = st.selectbox("Create/Join", ["Create", "Join"])
            if op == "Create":
                game_name = st.text_input("Game Name")
                game_token = st.text_input("Game Token")
                default_balance = st.number_input("Default Balance", value=100)
                st.button(
                    "Create",
                    on_click=lambda: self.on_create(
                        game_name, game_token, default_balance
                    ),
                )
            elif op == "Join":
                user_id = get_user_info().user_id
                recent_games = Player.get_related_game_by_user_id(user_id)

                recent = st.selectbox(
                    "recent games",
                    options=recent_games or [],
                    format_func=lambda game: game.name,
                )
                game_name = st.text_input("Game Name", value= "" if recent is None else recent.name)
                game_token = st.text_input("Game Token")
                st.button("Join", on_click=lambda: self.on_join(game_name, game_token))

    def on_create(self, game_name: str, game_token: str, default_balance: int) -> None:
        user_info = get_user_info()
        try:
            game = GameBoard.start_new_game(
                user_info.user_id, game_name, game_token, default_balance
            )
        except Exception as e:
            st.error(f"Create failed: {e}, game name: {game_name}, token: {game_token}")
            return
        set_game_info(game._id, game.name)
        st.info("Create success")

    def on_join(self, game_name: str, game_token: str) -> None:
        user_info = get_user_info()
        try:
            game = GameBoard.join_game(user_info.user_id, game_name, game_token)
            set_game_info(game._id, game.name)
            st.info("Join success")
        except Exception as e:
            st.error(f"Join failed: {e}, game name: {game_name}, token: {game_token}")
            return
        st.info("Join success")

    @staticmethod
    def player_template_data() -> dict:
        def players(num, deposit):
            return [{"name": f"Player {i}", "deposit": deposit} for i in range(num)]

        return {
            "Mahjong": players(4, 100),
            "升级": players(4, 100),
            "Texas hold 'em": players(6, 1000),
        }
