from ui.board import Board
from ui.game_init import InitGameForm
import streamlit as st


with st.sidebar:
    InitGameForm(
        "sidebar_init_game_form", lambda game: st.session_state.update({"game": game})
    ).render()

if "game" not in st.session_state:
    st.stop()


board = Board("board", st.session_state.game)

board.render_ranking_table()

st.divider()

board.render_transfer_form()

st.divider()
with st.expander("Records"):
    board.render_records_table()
