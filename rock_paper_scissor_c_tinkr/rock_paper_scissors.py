"""
Simple Rock Paper Scissors GUI using Tkinter.
"""

import random
import json
import os
import tkinter as tk
from tkinter import ttk

CHOICES = ["rock", "paper", "scissors"]
HIGHSCORE_FILE = "highscores.json"

class RockPaperScissorsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock Paper Scissors")
        self.resizable(False, False)

        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds_played = 0
        self.high_scores = {"best_player": 0, "best_computer": 0}
        self.load_high_scores()

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

        self.ties_label = ttk.Label(score_frame, text="Ties: 0", font=("Segoe UI", 11, "bold"))
        self.ties_label.grid(row=0, column=2, padx=10)
        # Round history
        history_frame = ttk.Frame(self)
        history_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10), padx=10)

        columns = ("round", "player", "computer", "result")
        self.history = ttk.Treeview(history_frame, columns=columns, show="headings", height=6)
        self.history.heading("round", text="Round")
        self.history.heading("player", text="Player")
        self.history.heading("computer", text="Computer")
        self.history.heading("result", text="Result")
        self.history.column("round", width=60, anchor="center")
        self.history.column("player", width=100, anchor="center")
        self.history.column("computer", width=100, anchor="center")
        self.history.column("result", width=120, anchor="center")

        vsb = ttk.Scrollbar(history_frame, orient="vertical", command=self.history.yview)
        self.history.configure(yscrollcommand=vsb.set)
        self.history.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        high_scores_button = ttk.Button(self, text="High Scores", command=self.show_high_scores)
        high_scores_button.grid(row=6, column=0, columnspan=3, pady=(0, 5))

        quit_button = ttk.Button(self, text="Quit", command=self.destroy)
        quit_button.grid(row=7, column=0, columnspan=3, pady=(0, 10))

    def play_round(self, player_choice: str):
        computer_choice = random.choice(CHOICES)
        winner = self.determine_winner(player_choice, computer_choice)

        self.rounds_played += 1

        if winner == "player":
            self.player_score += 1
            result_text = f"You win! {player_choice.capitalize()} beats {computer_choice}."
        elif winner == "computer":
            self.computer_score += 1
            result_text = f"Computer wins! {computer_choice.capitalize()} beats {player_choice}."
        else:
            result_text = f"It's a tie! You both chose {player_choice}."
            self.ties += 1

        self.status_label.config(text=f"Computer chose: {computer_choice}.")
        self.result_label.config(text=result_text)
        self.player_score_label.config(text=f"Player: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        self.ties_label.config(text=f"Ties: {self.ties}")

        # Add to round history
        try:
            self.history.insert("", "end", values=(
                self.rounds_played,
                player_choice.capitalize(),
                computer_choice.capitalize(),
                "Tie" if winner == "tie" else ("Player" if winner == "player" else "Computer"),
            ))
        except Exception:
            pass
        self.check_update_high_scores()

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

    def load_high_scores(self):
        try:
            if os.path.exists(HIGHSCORE_FILE):
                with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # only keep expected keys
                    for k in ("best_player", "best_computer"):
                        if k in data:
                            try:
                                self.high_scores[k] = int(data[k])
                            except Exception:
                                pass
        except Exception:
            pass

    def save_high_scores(self):
        try:
            with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.high_scores, f)
        except Exception:
            pass

    def check_update_high_scores(self):
        updated = False
        if self.player_score > self.high_scores.get("best_player", 0):
            self.high_scores["best_player"] = self.player_score
            updated = True
        if self.computer_score > self.high_scores.get("best_computer", 0):
            self.high_scores["best_computer"] = self.computer_score
            updated = True
        if updated:
            self.save_high_scores()

    def show_high_scores(self):
        top = tk.Toplevel(self)
        top.title("High Scores")
        top.resizable(False, False)
        ttk.Label(top, text="High Scores", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, pady=8, padx=12)
        ttk.Label(top, text=f"Best Player Score: {self.high_scores.get('best_player', 0)}", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", padx=12)
        ttk.Label(top, text=f"Best Computer Score: {self.high_scores.get('best_computer', 0)}", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="w", padx=12)
        ttk.Button(top, text="Close", command=top.destroy).grid(row=3, column=0, pady=10)


if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()

