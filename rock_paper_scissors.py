"""
Simple Rock Paper Scissors GUI using Tkinter.
"""

import random
import tkinter as tk
from tkinter import ttk

CHOICES = ["rock", "paper", "scissors"]

class RockPaperScissorsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors")
        self.resizable(False, False)

        self.player_score = 0
        self.computer_score = 0

        self.create_widgets()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Rock Paper Scissors", font=("Segoe UI", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(10, 5), padx=10)

        self.status_label = ttk.Label(self, text="Choose rock, paper, or scissors to play.", font=("Segoe UI", 11))
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10), padx=10)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 10), padx=10)

        for index, choice in enumerate(CHOICES):
            button = ttk.Button(
                button_frame,
                text=choice.capitalize(),
                command=lambda selection=choice: self.play_round(selection),
                width=12,
            )
            button.grid(row=0, column=index, padx=5)

        self.result_label = ttk.Label(self, text="", font=("Segoe UI", 11))
        self.result_label.grid(row=3, column=0, columnspan=3, pady=(0, 10), padx=10)

        score_frame = ttk.Frame(self, padding=(10, 0, 10, 10))
        score_frame.grid(row=4, column=0, columnspan=3)

        self.player_score_label = ttk.Label(score_frame, text="Player: 0", font=("Segoe UI", 11, "bold"))
        self.player_score_label.grid(row=0, column=0, padx=10)

        self.computer_score_label = ttk.Label(score_frame, text="Computer: 0", font=("Segoe UI", 11, "bold"))
        self.computer_score_label.grid(row=0, column=1, padx=10)

        quit_button = ttk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=5, column=0, columnspan=3, pady=(0, 10))

    def play_round(self, player_choice: str):
        computer_choice = random.choice(CHOICES)
        winner = self.determine_winner(player_choice, computer_choice)

        if winner == "player":
            self.player_score += 1
            result_text = f"You win! {player_choice.capitalize()} beats {computer_choice}."
        elif winner == "computer":
            self.computer_score += 1
            result_text = f"Computer wins! {computer_choice.capitalize()} beats {player_choice}."
        else:
            result_text = f"It's a tie! You both chose {player_choice}."

        self.status_label.config(text=f"Computer chose: {computer_choice}.")
        self.result_label.config(text=result_text)
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")

    @staticmethod
    def determine_winner(player_choice: str, computer_choice: str) -> str:
        if player_choice == computer_choice:
            return "tie"

        winning_combinations = {
            ("rock", "scissors"),
            ("paper", "rock"),
            ("scissors", "paper"),
        }

        return "player" if (player_choice, computer_choice) in winning_combinations else "computer"


if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()

