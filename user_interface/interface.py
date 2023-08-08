from position import Position
import tkinter
from utils import predict
from stockfish import Stockfish
import chess
import time
import torch

board = chess.Board()

sf = Stockfish(
    path='C:/Users/aaa57/pychess-assitance/user_interface/stockfish/stockfish-windows-x86-64-avx2.exe')
best_model = torch.jit.load('user_interface/best_model_cpu_scripted.pt')
GAMETURN = chess.WHITE

position = Position('image')

CAPTUER_INTERVAL = 2000  # ms
capture_after_id = None


def left_pos():
    global position

    position.set_left_position()

    left_button.config(state='disabled')

    left_post_text.config(
        text=f'left_position => {position.left_x}, {position.left_y}')


def right_pos():
    global position
    try:
        position.set_right_position()

        right_button.config(state='disabled')

        right_post_text.config(
            text=f'right_position => {position.right_x}, {position.right_y}')
    except ValueError as e:
        right_post_text.config(
            text=f'{str(e)} please click the reset button')


def reset():
    global position

    position = Position('image')

    position.reset()

    left_button.config(state='active')
    right_button.config(state='active')

    left_post_text.config(text='')
    right_post_text.config(text='')
    capture_text.config(text='')


def capture():
    global position, capture_after_id, sf
    try:
        position.capture()
        capture_after_id = window.after(CAPTUER_INTERVAL, capture)

        capture_text.config(text=f'{position.counter-1} captured')

        fen = predict(
            f'{position.filepath}/{position.counter-1}.png', model=best_model)
        if not GAMETURN:
            fen = fen[::-1]
        board = chess.Board()
        board.set_fen(fen=fen)
        board.turn = GAMETURN
        fen_text.config(text=board.fen())
        try:
            sf_label.config(text='')
            sf.set_fen_position(board.fen())
            move = sf.get_top_moves(1)
            sf_label.config(text=move)
        except:
            pass
    except ValueError as e:
        capture_text.config(
            text=f'{str(e)}')


def cancel_capture():
    global capture_after_id
    window.after_cancel(capture_after_id)

    capture_text.config(text=f'cancel capture')


def white_turn():
    global GAMETURN
    GAMETURN = chess.WHITE

    color_text.config(text=f'{GAMETURN}')


def black_turn():
    global GAMETURN
    GAMETURN = chess.BLACK

    color_text.config(text=f'{GAMETURN}')


window = tkinter.Tk()

window.title("PyChess AssiTance")
window.geometry("800x600")
window.resizable(False, False)

left_post_text = tkinter.Label(
    window, width=100, height=1, fg="red", relief='raised')

left_post_text.pack()

right_post_text = tkinter.Label(
    window, width=100, height=1, fg="red", relief="raised")

right_post_text.pack()

capture_text = tkinter.Label(
    window, width=100, height=1, fg="red", relief='raised')

capture_text.pack()

fen_text = tkinter.Label(
    window, width=100, height=1, fg="black", relief="raised")

fen_text.pack()

color_text = tkinter.Label(
    window, width=100, height=1, fg="black", relief="raised")

color_text.pack()

sf_label = tkinter.Label(window, width=100, height=1,
                         fg="black", relief="raised")

sf_label.pack()

left_button = tkinter.Button(window, overrelief="solid", width=15,
                             command=left_pos, repeatdelay=1000, repeatinterval=100, text='left_position')

right_button = tkinter.Button(window, overrelief="solid", width=15,
                              command=right_pos, repeatdelay=1000, repeatinterval=100, text='right_position')

reset_button = tkinter.Button(window, overrelief="solid", width=15,
                              command=reset, repeatdelay=1000, repeatinterval=100, text='reset position')

capture_button = tkinter.Button(window, overrelief="solid", width=15,
                                command=capture, repeatdelay=1000, repeatinterval=100, text='capture')
capture_cancle_button = tkinter.Button(window, overrelief="solid", width=15,
                                       command=cancel_capture, repeatdelay=1000, repeatinterval=100, text='cancle capture')
left_button.pack(side=tkinter.LEFT, anchor='n')
right_button.pack(side=tkinter.LEFT, anchor='n')
reset_button.pack(side=tkinter.LEFT, anchor='n')
capture_button.pack(side=tkinter.LEFT, anchor='n')
capture_cancle_button.pack(side=tkinter.LEFT, anchor='n')

CheckVar1 = tkinter.IntVar()
CheckVar2 = tkinter.IntVar()

white = tkinter.Checkbutton(
    window, text="White", variable=CheckVar1, command=white_turn, onvalue=1)
black = tkinter.Checkbutton(
    window, text="Black", variable=CheckVar1, command=black_turn, onvalue=2)
white.select()

white.pack()
black.pack()
window.wm_attributes("-topmost", 1)
window.mainloop()
