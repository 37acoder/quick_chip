from ui.board import Board
from ui.game_init import InitGameForm
from ui.common import get_game_info, get_user_info
import streamlit as st
from ui.record import Statistics
from ui.user import UserInfo
from ui.status import StatusPad
from rule.rule import GameBoard

with st.sidebar:
    StatusPad("status_pad")
    UserInfo("user_info")

    if user := get_user_info():
        InitGameForm("init_game_form").render()

if (game := get_game_info()) is not None:
    game_board = GameBoard(game.game_id)
    board = Board("board", game_board)
    main_tab, record_tab, transfer_tab = st.tabs(("Main", "Records", "Transfer"))
    record = Statistics("record", game_board)
    with main_tab:
        board.render_ranking_table()
        st.divider()
        record.render_line_chart()
    with record_tab:
        record.render_list_record()
    with transfer_tab:
        board.render_transfer_form()
        st.divider()
