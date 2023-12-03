import streamlit as st
from ui import Component
from rule.rule import Game


class Board(Component):
    def __init__(self, session_key: str, game: Game) -> None:
        super().__init__(session_key)
        self.game = game

    def render_ranking_table(self) -> None:
        st.write("Ranking")
        player_sorted_by_deposit = sorted(
            self.game.all_player_including_dealder,
            key=lambda player: player.deposit,
            reverse=True,
        )
        self.render_player_deposit_table(player_sorted_by_deposit)

    def render_player_deposit_table(self, players=None) -> None:
        if players is None:
            players = self.game.all_player_including_dealder

        def on_player_deposit_table_change(*args, **kwargs):
            event = st.session_state[
                f"{self.session_key}.player_deposit_table_callback"
            ]
            for num, value in event["edited_rows"].items():
                player = players[int(num)]
                player.deposit = value["Modify"]

        st.data_editor(
            [
                {
                    "Name": player.name,
                    "Balance": player.deposit,
                    "Modify": player.deposit,
                }
                for player in players
            ],
            column_config={
                "Balance": st.column_config.ProgressColumn(
                    "Balance",
                    format="$%f",
                    max_value=max([player.deposit for player in players]),
                    min_value=min([player.deposit for player in players]),
                ),
                "Modify": st.column_config.NumberColumn(),
            },
            use_container_width=True,
            key=f"{self.session_key}.player_deposit_table_callback",
            on_change=on_player_deposit_table_change,
        )

    def render_transfer_form(self) -> None:
        st.write("Transfer")
        from_player_name = st.selectbox(
            "From",
            [player.name for player in self.game.all_player_including_dealder],
        )
        to_player_name = st.selectbox(
            "To",
            [player.name for player in self.game.all_player_including_dealder],
        )
        amount = st.number_input("Amount", min_value=0, value=0)
        from_player = self.game.players_map_by_name[from_player_name]
        to_player = self.game.players_map_by_name[to_player_name]

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
