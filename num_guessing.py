import customtkinter as ctk
from tkinter import messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.levels = {"Easy": 50, "Medium": 100, "Hard": 500}
        self.current_level = "Medium"
        self.max_number = self.levels[self.current_level]

        self.secret = random.randint(1, self.max_number)
        self.attempts = 0
        self.history = []
        self.score = 0

        self.main_frame = ctk.CTkFrame(root, corner_radius=15)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.main_frame, text="🎯 Number Guessing Game 🎯",
                                        font=("Comic Sans MS", 18, "bold"))
        self.title_label.pack(pady=10)

        self.diff_var = ctk.StringVar(value=self.current_level)
        self.diff_menu = ctk.CTkOptionMenu(self.main_frame, values=list(self.levels.keys()),
                                           variable=self.diff_var, command=self.change_level,
                                           width=150)
        self.diff_menu.pack(pady=5)

        self.theme_var = ctk.StringVar(value="Light")
        self.theme_switch = ctk.CTkSwitch(self.main_frame, text="Dark Mode",
                                          command=self.toggle_theme,
                                          variable=self.theme_var,
                                          onvalue="Dark", offvalue="Light")
        self.theme_switch.pack(pady=5)

        self.label = ctk.CTkLabel(self.main_frame, 
                                  text=f"Guess a number between 1 and {self.max_number}:",
                                  font=("Arial", 13))
        self.label.pack(pady=5)

        self.entry = ctk.CTkEntry(self.main_frame, font=("Arial", 13), justify="center", width=100)
        self.entry.pack(pady=10)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=10)

        self.submit_btn = ctk.CTkButton(self.button_frame, text="Submit",
                                        command=self.check_guess,
                                        fg_color="#4CAF50", hover_color="#45a049",
                                        font=("Arial", 12, "bold"), width=100, corner_radius=15)
        self.submit_btn.grid(row=0, column=0, padx=5)

        self.restart_btn = ctk.CTkButton(self.button_frame, text="Restart",
                                         command=self.restart_game,
                                         fg_color="#f44336", hover_color="#da190b",
                                         font=("Arial", 12, "bold"), width=100, corner_radius=15)
        self.restart_btn.grid(row=0, column=1, padx=5)

        self.hint_btn = ctk.CTkButton(self.button_frame, text="💡 Hint",
                                      command=self.show_hint,
                                      fg_color="#2196F3", hover_color="#0b79d0",
                                      font=("Arial", 11, "bold"), width=100, corner_radius=15)
        self.hint_btn.grid(row=0, column=2, padx=5)

        self.result_label = ctk.CTkLabel(self.main_frame, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)

        self.attempts_label = ctk.CTkLabel(self.main_frame, text="Attempts: 0", font=("Arial", 11))
        self.attempts_label.pack()

        self.score_label = ctk.CTkLabel(self.main_frame, text="Score: 0", font=("Arial", 11, "bold"))
        self.score_label.pack(pady=5)

    def toggle_theme(self):
        if self.theme_var.get() == "Dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def change_level(self, choice):
        self.current_level = choice
        self.max_number = self.levels[choice]
        self.restart_game()
        self.label.configure(text=f"Guess a number between 1 and {self.max_number}:")

    def show_hint(self):
        if not self.secret:
            return
        hints = []
        hints.append("The number is divisible by 2." if self.secret % 2 == 0 else "The number is odd.")
        mid = self.max_number // 2
        hints.append(f"The number is greater than {mid}." if self.secret > mid else f"The number is less than or equal to {mid}.")
        low, high = max(1, self.secret - 10), min(self.max_number, self.secret + 10)
        hints.append(f"The number is between {low} and {high}.")
        messagebox.showinfo("💡 Hint", random.choice(hints))

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.attempts += 1
            self.history.append(guess)
            self.attempts_label.configure(text=f"Attempts: {self.attempts}")

            diff = abs(self.secret - guess)
            if guess < self.secret:
                msg = "🔥 Very Hot!" if diff <= 5 else "⬇️ Too Low!"
                self.result_label.configure(text=f"{msg} Try again.", text_color="blue")
            elif guess > self.secret:
                msg = "🔥 Very Hot!" if diff <= 5 else "⬆️ Too High!"
                self.result_label.configure(text=f"{msg} Try again.", text_color="orange")
            else:
                self.score += 1
                self.score_label.configure(text=f"Score: {self.score}")
                self.result_label.configure(text=f"🎉 Correct! You guessed in {self.attempts} attempts.", text_color="green")
                messagebox.showinfo("Winner", f"🏆 You guessed it in {self.attempts} attempts!\nGuesses: {self.history}\n\n✅ Total Score: {self.score}")
        except ValueError:
            messagebox.showerror("Invalid Input", "❌ Please enter a valid number.")

    def restart_game(self):
        self.secret = random.randint(1, self.max_number)
        self.attempts = 0
        self.history.clear()
        self.result_label.configure(text="", text_color="white")
        self.entry.delete(0, "end")
        self.attempts_label.configure(text="Attempts: 0")

if __name__ == "__main__":
    root = ctk.CTk()
    game = NumberGuessingGame(root)
    root.mainloop()
