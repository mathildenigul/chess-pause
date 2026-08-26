import streamlit as st
from pipeline import analyze_screenshot
from PIL import Image
import numpy as np
import cv2
import chess
import chess.svg
import streamlit.components.v1 as components
from suggest_move import suggest_move

st.set_page_config(page_title = "Chess Pause", page_icon = "♛")
st.title("Chess Pause")
st.markdown(
'''This app alows you to upload a sceenshot from a chess game you want to continue. Either from a masters' game
you are watching or just a game you want to continue. You can try to cntinue on your own or also see the AI suggestions
for your next move.'''
)


class_names = ["Black_Bishop", "Black_King", "Black_Knight", "Black_Pawn", "Black_Queen", "Black_Rook",
                   "White_Bishop", "White_King", "White_Knight", "White_Pawn", "White_Queen", "White_Rook"]
model_path = "models/piece_classifier.keras"
engine_path = "engine\stockfish-windows-x86-64-avx2.exe"
uploaded_file = st.file_uploader("Upload a chessboard screenshot", type = ["png", "jpg", "jpeg"])
side_to_move = st.radio("Whose turn is it?", ["White", "Black"])
side_code = "w" if side_to_move == "White" else "b"
board_orientation = st.radio("How is the board oriented in your screenshot?", ["White at bottom", "Black at bottom"])

if uploaded_file is not None:
    st.image(uploaded_file, caption = "Your upload", width = 400)
    if st.button("Analyze position"):
        with open("temp_upload.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        fen, move = analyze_screenshot("temp_upload.png", model_path, engine_path, class_names, side_to_move = side_code, board_orientation = board_orientation)
        st.session_state.board = chess.Board(fen)
        st.success(f"Suggested move: {move}")

if "board" in st.session_state:
    svg_string = chess.svg.board(st.session_state.board, size = 400)
    components.html(svg_string, height = 400)
    move_input = st.text_input("Enter your move")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Play move"):
            try:
                st.session_state.board.push_san(move_input)
            except ValueError:
                st.error("Illegal move, please try again.")
    with col2:
        if st.button("Get an AI suggestion"):
            current_fen = st.session_state.board.fen()
            ai_move = suggest_move(current_fen, engine_path)
            st.info(f"AI suggests: {ai_move}")
            
