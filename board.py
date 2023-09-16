from tkinter import ttk, Tk
from functools import partial


class Board:

    def __init__(self):
        self._draw_board(3, 3)

    def _update_board(self, row, column):
        pass

    def _draw_board(self, rows, columns):
        self.columns = columns
        self.rows = rows

        window = Tk()
        window.title("Tic-Tac-Toe")
        window.geometry("500x300+750+200")

        frame = ttk.Frame(window, padding=20)
        frame.grid()

        for row in range(rows):
            for column in range(columns):
                on_button_press = partial(self._update_board, row, column)
                button = ttk.Button(
                    frame,
                    text="Row {}, Col {}".format(row, column),
                    padding=35,
                    command=on_button_press
                )
                button.grid(row=row, column=column)

        # Init the main looper and show the window
        window.mainloop()



        
