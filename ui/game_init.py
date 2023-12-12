from ui import Component
import streamlit as st
from rule.rule import GameBoard, Player


class InitGameForm(Component):
    def __init__(self, session_key: str, reset_callback) -> None:
        super().__init__(session_key)
        self.reset_callback = reset_callback

    def render(self) -> None:
        st.write("Init Game")
        player_template_options = InitGameForm.player_template_data()
        player_template_selected = st.selectbox(
            "Player Template",
            list(player_template_options.keys()),
        )
        player_template = player_template_options[player_template_selected]
        player_init_data = st.data_editor(
            player_template,
            num_rows="dynamic",
            column_config={"deposit": st.column_config.NumberColumn(min_value=0)},
        )

        if st.button("Init", on_click=lambda: self.on_init(player_init_data)):
            st.info("Init success")

    def on_init(self, player_init_data: list[dict]) -> None:
        game = GameBoard(
            [Player(player["name"], player["deposit"]) for player in player_init_data]
        )
        self.reset_callback(game)

    @staticmethod
    def player_template_data() -> dict:
        def players(num, deposit):
            return [{"name": f"Player {i}", "deposit": deposit} for i in range(num)]

        return {
            "Mahjong": players(4, 100),
            "升级": players(4, 100),
            "Texas hold 'em": players(6, 1000),
        }
