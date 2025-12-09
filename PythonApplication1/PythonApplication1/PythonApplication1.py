"""Простая игра «Угадай число» с окном Tkinter.

Запустите файл и вводите предел диапазона, чтобы начать игру.
"""

import tkinter as tk
from random import randint
from tkinter import messagebox


class GuessNumberApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Угадай число")
        self.root.resizable(False, False)

        self.secret: int | None = None
        self.limit: int = 0
        self.attempts: int = 0
        self.best: int | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, padx=12, pady=12)
        frame.grid(row=0, column=0)

        tk.Label(frame, text="Верхний предел (≥10):").grid(row=0, column=0, sticky="w")
        self.limit_entry = tk.Entry(frame, width=10)
        self.limit_entry.insert(0, "50")
        self.limit_entry.grid(row=0, column=1, padx=(6, 0))

        self.start_btn = tk.Button(frame, text="Загадать", command=self.start_game)
        self.start_btn.grid(row=0, column=2, padx=(8, 0))

        tk.Label(frame, text="Ваш ответ:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.guess_entry = tk.Entry(frame, width=10, state="disabled")
        self.guess_entry.grid(row=1, column=1, padx=(6, 0), pady=(10, 0))
        self.guess_entry.bind("<Return>", lambda _: self.check_guess())

        self.check_btn = tk.Button(
            frame, text="Проверить", state="disabled", command=self.check_guess
        )
        self.check_btn.grid(row=1, column=2, padx=(8, 0), pady=(10, 0))

        self.status_label = tk.Label(frame, text="Нажмите «Загадать», чтобы начать.")
        self.status_label.grid(row=2, column=0, columnspan=3, sticky="w", pady=(12, 0))

        self.best_label = tk.Label(frame, text="Рекорд: пока нет")
        self.best_label.grid(row=3, column=0, columnspan=3, sticky="w", pady=(4, 0))

    def start_game(self) -> None:
        limit_raw = self.limit_entry.get().strip()

        try:
            if not limit_raw.isdigit():
                messagebox.showwarning("Ошибка", "Введите целое число (минимум 10).")
                return

            limit = int(limit_raw)
            if limit < 10:
                messagebox.showwarning("Ошибка", "Диапазон должен быть не меньше 10.")
                return

            self.limit = limit
            self.secret = randint(1, limit)
            self.attempts = 0
            self.status_label.config(text=f"Загадано число от 1 до {limit}. Угадайте его!")
            self.guess_entry.config(state="normal")
            self.check_btn.config(state="normal")
            self.guess_entry.delete(0, tk.END)
            self.guess_entry.focus_set()
        except (ValueError, OverflowError):
            messagebox.showerror("Ошибка", "Некорректное число. Попробуйте снова.")

    def check_guess(self) -> None:
        if self.secret is None:
            messagebox.showinfo("Игра не начата", "Сначала нажмите «Загадать».")
            return

        try:
            guess_raw = self.guess_entry.get().strip()
            if not guess_raw.isdigit():
                self.status_label.config(text="Введите число.")
                return

            value = int(guess_raw)
            if value < 1 or value > self.limit:
                self.status_label.config(text=f"Введите число от 1 до {self.limit}.")
                return

            self.attempts += 1
            self.guess_entry.delete(0, tk.END)

            if value < self.secret:
                self.status_label.config(text="Моё число больше.")
            elif value > self.secret:
                self.status_label.config(text="Моё число меньше.")
            else:
                self._handle_win()
        except (ValueError, OverflowError):
            self.status_label.config(text="Некорректный ввод. Введите число.")

    def _handle_win(self) -> None:
        assert self.secret is not None
        text = f"Верно! Число {self.secret}. Попыток: {self.attempts}."
        messagebox.showinfo("Победа!", text)

        if self.best is None or self.attempts < self.best:
            self.best = self.attempts

        self.best_label.config(text=f"Рекорд: {self.best} попыток")

        self.status_label.config(text="Нажмите «Загадать», чтобы сыграть снова.")
        self.guess_entry.config(state="disabled")
        self.check_btn.config(state="disabled")
        self.secret = None


def main() -> None:
    root = tk.Tk()
    GuessNumberApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
