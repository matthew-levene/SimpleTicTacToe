import tkinter as tk


class Board:

    def __init__(self):
        self._draw_board(3, 3)

    def _draw_board(self, columns, rows):
        self.columns = columns
        self.rows = rows

        window = tk.Tk()
        window.title("Tic-Tac-Toe")
        window.geometry("500x500+750+200")

        # Init the main looper and show the window
        window.mainloop()



        
