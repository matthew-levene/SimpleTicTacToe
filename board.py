import sys
from functools import partial
from tkinter import ttk, Tk, StringVar
from itertools import permutations


horizontal_win_conditions = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)]
]

vertical_win_conditions = [
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)]
]

diagonal_win_conditions = [
    [(0, 0), (1, 1), (2, 2)],
    [(2, 0), (1, 1), (0, 2)]
]


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
        self.zero_zero_guard = False
        self.trap_coords = ()
        self.player_win_tuple_list = []
        self.computer_win_tuple_list = []

        # Init the main looper and show the window
        self._window.mainloop()

    def _check_win_condition(self, win_condition, selected_row, selected_column):
        for win_tuple_list in win_condition:
            for win_tuple in win_tuple_list:
                row, column = win_tuple

                try:
                    if self._board[row][column] == self.player_marker:
                        self.player_win_tuple_list.append((row, column))
                    else:
                        if (row == 0 and column == 0) and not self.zero_zero_guard:
                            row = selected_row
                            column = selected_column
                            self.computer_win_tuple_list.append((row, column))
                        else:
                            self.computer_win_tuple_list.append((row, column))
                except IndexError:
                    continue

        player_perms = permutations(self.player_win_tuple_list, 3)
        for perm in list(player_perms):
            for condition in win_condition:
                if list(perm) == condition:
                    print("Player Won!")
                    sys.exit()

        computer_perms = permutations(list(set(self.computer_win_tuple_list)), 3)
        for perm in list(computer_perms):
            for condition in win_condition:
                if list(perm) == condition:
                    print("Computer Won!")
                    sys.exit()

        self.computer_win_tuple_list = []
        self.player_win_tuple_list = []

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
        self.zero_zero_guard = True if row == 0 and column == 0 else False
        button = ttk.Button(
            frame,
            style=style,
            text=marker,
            padding=35
        )
        button.grid(row=row, column=column)

        self._check_win_condition(horizontal_win_conditions, row, column)
        self._check_win_condition(vertical_win_conditions, row, column)
        self._check_win_condition(diagonal_win_conditions, row, column)

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
