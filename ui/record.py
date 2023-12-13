from itertools import groupby
import streamlit as st
from ui.common import get_game_info, get_user_info
from rule.rule import GameBoard
from ui import Component


class Statistics(Component):
    def __init__(self, session_key: str, game_board: GameBoard) -> None:
        super().__init__(session_key)
        self.game_board: GameBoard = game_board
        self.game_records = game_board.game_records
        self.user_id_to_name = lambda user_id: self.game_board.user_id_map[
            user_id
        ].username if user_id != 1 else "God"

    def render_list_record(self):
        st.write("Records")
        records_for_show = [
            {
                "From": self.user_id_to_name(record.from_user_id),
                "To": self.user_id_to_name(record.to_user_id),
                "Amount": record.amount,
                "Time": record.time,
            }
            for record in self.game_records
        ]
        st.dataframe(records_for_show, use_container_width=True)

    def render_line_chart(self):
        """
        from map time -> all_balance
        to map user_name -> list[dict[time: balance]]
        """
        user_name_to_time_balance = {
            "time": [],
            "username": [],
            "balance": [],
        }
        time_window_set = set()
        time_window = None
        for record in self.game_records:
            hour = record.time.hour
            minute = record.time.minute
            time_str = f"{hour}:{minute}"
            for user_id, balance in record.balance_data.items():
                if time_window is None or time_window != time_str:
                    time_window = time_str
                    time_window_set.clear()
                username = self.user_id_to_name(user_id)
                if username in time_window_set:
                    continue
                else:
                    time_window_set.add(username)
                user_name_to_time_balance["time"].append(time_str)
                user_name_to_time_balance["username"].append(username)
                user_name_to_time_balance["balance"].append(balance)

        print(user_name_to_time_balance)
        st.line_chart(
            user_name_to_time_balance, x="time", y="balance", color="username"
        )
