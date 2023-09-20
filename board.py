from functools import partial
from tkinter import ttk, Tk, StringVar


class Board:

    def __init__(self):
        self.round_count = 1
        self.player_marker = "x"

        self._window = Tk()
        self._window.title("Tic-Tac-Toe")
        self._window.geometry("500x460+750+200")

        self._draw_choice_input(self._window)
        self._show_opponent_turn(self._window)
        self._draw_board(self._window, 3, 3)

        # Init the main looper and show the window
        self._window.mainloop()

    def _show_opponent_turn(self, frame=None):
        def is_player_turn(round_count):
            return round_count % 2 == 0

        if is_player_turn(self.round_count):
            style = ttk.Style()
            style.configure("RW.TButton", foreground="red", background="white")
        else:
            style = ttk.Style()
            style.configure("BW.TButton", foreground="blue", background="white")

        opponent_turn_label = ttk.Label(
            master=frame if frame is not None else self._window,
            text="{} Turn".format(" Player" if self.round_count % 2 == 0 else "Computer"),
            padding=10,
            style="RW.TButton" if is_player_turn(self.round_count) else "BW.TButton",
            width=20
        )

        opponent_turn_label.grid(row=2, column=0)

    def _no_marker_selected(self):
        return self.player_marker == "x"

    def _get_marker_style(self):
        if self._no_marker_selected():
            self.player_marker = self.player_marker.upper()
        if self.round_count % 2 == 0:
            style = ttk.Style()
            style.configure("RW.TButton", foreground="red", background="white")
            return "X" if self.player_marker == "X" else "O", "RW.TButton"
        else:
            style = ttk.Style()
            style.configure("BW.TButton", foreground="blue", background="white")
            return "O" if not self.player_marker == "O" else "X", "BW.TButton"

    def _update_board(self, frame, row, column):
        marker, style = self._get_marker_style()
        self._board[row].insert(column, marker)
        button = ttk.Button(
            frame,
            style=style,
            text=marker,
            padding=35
        )
        button.grid(row=row, column=column)

        self.round_count += 1

        self._show_opponent_turn()

    def _draw_choice_input(self, window):
        marker_selection = StringVar()
        on_radio_selected = partial(self._store_player_choice, marker_selection)

        choice_label = ttk.Label(window, text="Do you want to play as X or O?", padding=15)
        choice_label.grid()

        choice_frame = ttk.Frame()

        x_text = "X"
        x_choice = ttk.Radiobutton(
            choice_frame,
            text=x_text,
            variable=marker_selection,
            value=x_text,
            padding=10,
            command=on_radio_selected
        )
        x_choice.grid(row=0, column=0)

        o_text = "O"
        o_choice = ttk.Radiobutton(
            choice_frame,
            text=o_text,
            variable=marker_selection,
            value=o_text,
            padding=10,
            command=on_radio_selected
        )
        o_choice.grid(row=0, column=1)

        choice_frame.grid()

    def _store_player_choice(self, marker_selection):
        if self.player_marker != "O" and self.player_marker != "X":
            if self._no_marker_selected():
                self.player_marker = marker_selection.get()
            else:
                self.player_marker = marker_selection.get()

    def _draw_board(self, window, rows, columns):
        self.columns = columns
        self.rows = rows
        self._board: list[list[str]] = [[] for _ in range(rows)]

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
