from ui.board import Board
from ui.game_init import InitGameForm
from ui.common import get_game_info, get_user_info
import streamlit as st
from models.core import Game
from ui.user import UserInfo
from rule.rule import Player, Record, TransferRecord, GameBoard
# with st.sidebar:
#     InitGameForm(
#         "sidebar_init_game_form", lambda game: st.session_state.update({"game": game})
#     ).render()

# if "game" not in st.session_state:
#     st.stop()


# board = Board("board", st.session_state.game)

# board.render_ranking_table()

# st.divider()

# board.render_transfer_form()

# st.divider()
# with st.expander("Records"):
#     board.render_records_table()

with st.sidebar:
    UserInfo("user_info")

    if user := get_user_info():
        InitGameForm("init_game_form").render()

if (game := get_game_info()) is not None:
    game_board = GameBoard(game.game_id)
    board = Board("board", game_board)
    board.render_ranking_table()
    st.divider()
    board.render_transfer_form()
    st.divider()
