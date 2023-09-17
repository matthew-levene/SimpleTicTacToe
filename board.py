from tkinter import ttk, Tk
from functools import partial


class Board:

    def __init__(self):
        self.round_count = 1
        self._draw_board(3, 3)

    def _get_marker_style(self):
        if self.round_count % 2:
            style = ttk.Style()
            style.configure("RW.TButton", foreground="red", background="white")
            return "X", "RW.TButton"
        else:
            style = ttk.Style()
            style.configure("BW.TButton", foreground="blue", background="white")
            return "0", "BW.TButton"

    def _update_board(self, frame, row, column):
        marker, style = self._get_marker_style()
        self._board[row].insert(column, "X")
        button = ttk.Button(
            frame,
            style=style,
            text=marker,
            padding=35
        )
        button.grid(row=row, column=column)

        self.round_count += 1

    def _draw_board(self, rows, columns):
        self.columns = columns
        self.rows = rows
        self._board: list[list[str]] = [[] for _ in range(rows)]

        window = Tk()
        window.title("Tic-Tac-Toe")
        window.geometry("500x320+750+200")

        frame = ttk.Frame(window, padding=20)
        frame.grid()

        for row in range(rows):
            for column in range(columns):
                style = ttk.Style()
                style.configure("W.TButton", background="white")

                on_button_press = partial(self._update_board, frame, row, column)
                button = ttk.Button(
                    frame,
                    style="W.TButton",
                    padding=35,
                    command=on_button_press
                )
                button.grid(row=row, column=column)

        # Init the main looper and show the window
        window.mainloop()
