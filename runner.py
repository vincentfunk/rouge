from game import Game
from tkinter import Tk, Label

game = Game(25, 75)

root = Tk()
board = Label(root, text=game.board(), font="TkFixedFont", background='black', foreground='white')
board.grid(column=0, row=0)
board.focus_set()


def key_pressed(event):
    game.round(event.char)
    board.configure(text=game.board())


board.bind("<Key>", key_pressed)
root.mainloop()
