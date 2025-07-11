import time

from game import Game
from tkinter import Tk, Label
from entities.player import DeadError

game = Game(25, 75)

root = Tk()
board = Label(root, text=game.board(), font="TkFixedFont", background='black', foreground='white')
board.grid(column=0, row=0)
board.focus_set()


def key_pressed(event):
    try:
        game.round(event.char)
        board.configure(text=game.board())
    except DeadError as e:
        root.quit()
        print(e.message)


board.bind("<Key>", key_pressed)
root.mainloop()

