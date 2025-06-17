import tkinter as tk
from tkinter import ttk

# Example Game Class
class DummyGame(tk.Frame):
    def __init__(self, master, return_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        label = tk.Label(self, text="Dummy Game Started", font=("Arial", 16))
        label.grid(row=0, column=0, pady=20)

        back_button = tk.Button(self, text="← Back to menu", command=return_callback)
        back_button.grid(row=1, column=0, pady=10)


class GameSelector(tk.Frame):
    def __init__(self, master, start_game_callback):
        super().__init__(master)
        self.grid(row=0, column=0, sticky="nsew")

        label = tk.Label(self, text="Choose a Game", font=("Arial", 20))
        label.grid(row=0, column=0, pady=20)

        chess_btn = tk.Button(self, text="Play Chess", command=lambda: start_game_callback("chess"))
        chess_btn.grid(row=1, column=0, pady=5)

        dummy_btn = tk.Button(self, text="Play Dummy Game", command=lambda: start_game_callback("dummy"))
        dummy_btn.grid(row=2, column=0, pady=5)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mirror Chess")

        # Ensure the window resizes nicely
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.current_screen = None
        self.show_game_selector()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

    def show_game_selector(self):
        self.clear_screen()
        self.current_screen = GameSelector(self, self.start_game)

    def start_game(self, game_name):
        self.clear_screen()
        if game_name == "chess":
            # Later you could do: self.current_screen = ChessGame(self, self.show_game_selector)
            self.current_screen = DummyGame(self, self.show_game_selector)
        elif game_name == "dummy":
            self.current_screen = DummyGame(self, self.show_game_selector)


if __name__ == "__main__":
    app = App()
    app.mainloop()