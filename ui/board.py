import streamlit as st
from ui import Component
from rule.rule import GameBoard
from ui.common import get_user_info, get_game_info

class Board(Component):
    def __init__(self, session_key: str, game: GameBoard) -> None:
        super().__init__(session_key)
        self.game = game

    def render_ranking_table(self) -> None:
        st.write(f"Game {self.game.game_model.name} Ranking Table, {self.game.owner.username} is owner")
        if self.game.owner._id == get_user_info().user_id:
            st.write("You are owner")
            if st.toggle("show token"):
                st.write(self.game.game_model.token)
        
        player_infos = [
            {
                "Name": name,
                "Balance": info.balance,
            }
            for name, info in self.game.player_info_map_by_name.items()
        ]

        player_sorted_by_deposit = sorted(
            player_infos,
            key=lambda player: player["Balance"],
            reverse=True,
        )
        self.render_player_deposit_table(player_sorted_by_deposit)

    def render_player_deposit_table(self, player_infos) -> None:
        st.data_editor(
            player_infos,
            column_config={
                "Balance": st.column_config.ProgressColumn(
                    "Balance",
                    format="$%f",
                    max_value=100 if len(player_infos) == 0 else max([infos["Balance"] for infos in player_infos]),
                    min_value=0,
                ),
            },
            use_container_width=True,
            key=f"{self.session_key}.player_deposit_table_callback",
        )

    def render_transfer_form(self) -> None:
        st.write("Transfer")
        
        user_id = get_user_info().user_id
        self_index = next((i for i, player in enumerate(self.game.players) if player.user_model._id == user_id), 0)
        is_owner = self.game.game_model.owner_id == user_id
        from_player= st.selectbox(
            "From",
            self.game.players,
            format_func=lambda player: player.name,
            index=self_index,
            disabled=not is_owner,
        )
        to_player= st.selectbox(
            "To",
            self.game.players,
            format_func=lambda player: player.name,
        )
        amount = st.number_input("Amount", min_value=0, value=0)

        def on_transfer():
            self.game.transfer(from_player, to_player, amount)

        if st.button("Transfer", on_click=on_transfer):
            st.info(f"Transfer success {from_player.name} -> {to_player.name} {amount}")

    def render_records_table(self) -> None:
        st.write("Records")
        st.dataframe(
            [
                {"Time": record.time, "Content": record.content()}
                for record in self.game.records
            ],
            use_container_width=True,
        )
