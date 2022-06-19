from __future__ import annotations
import random
from math import sqrt


class Game:
    max_number: int
    secret: int
    pr_flip: float
    history: dict[int, str]
    count_guesses: int

    def __init__(self, max_number: int, pr_flip: float):
        self.max_number = max_number
        self.secret = random.randint(0, max_number)
        self.pr_flip = pr_flip
        self.history = {self.secret: "Correct"}
        self.count_guesses = 0

    def submit_guess(self, guess: int) -> str:
        self.count_guesses += 1
        response: str = self.history.get(guess, "")
        # Note: The correct guess already has a response in the history
        if response == "":
            is_higher: bool = self.secret > guess
            flip: bool = random.random() < self.pr_flip
            if is_higher != flip:  # xor
                response = "Higher"
            else:
                response = "Lower"
            self.history[guess] = response
        return response


def probability_method(game: Game):
    # List of intervals where the secret could be
    # List entries: (probability, interval bounds)
    intervals: list[tuple[float, tuple[int, int]]] = [(1.0, (0, game.max_number))]

    response: str = ""
    count = 0
    while response != "Correct" and count <= game.max_number:
        count += 1

        p: float
        low: int
        high: int
        p, (low, high) = max(intervals)

        guess: int = (high + low) // 2

        response = game.submit_guess(guess)

        if response != "Correct":
            p_low: float = game.pr_flip if response == "Higher" else 1 - game.pr_flip
            p_high: float = 1 - p_low
            new_intervals = []
            # Note: These probabilities are not normalized
            for p, (low, high) in intervals:
                if high < guess:
                    new_intervals.append((p * p_low, (low, high)))
                elif guess < low:
                    new_intervals.append((p * p_high, (low, high)))
                else:
                    if low < guess:
                        new_intervals.append((p * p_low, (low, guess - 1)))
                    if guess < high:
                        new_intervals.append((p * p_high, (guess + 1, high)))
            intervals = new_intervals


def run_game():
    print("\t".join(["max", "pr_flip", "mean", "stddev"]))

    for pr_flip in [0, 0.01, 0.1, 1 / 3, .4]:
        for max_number in [10, 100, 1000]:
            tallies: dict[int, int] = dict()
            trials = 10000
            for _ in range(trials):
                game: Game = Game(max_number, pr_flip)
                probability_method(game)
                guesses = game.count_guesses
                tallies[guesses] = tallies.get(guesses, 0) + 1

            e_guesses = sum(k * v / trials for k, v in tallies.items())  # Expectation E[guesses]
            e_guesses_sq = sum(k * k * v / trials for k, v in tallies.items())  # E[guesses^2]
            var_guesses = e_guesses_sq - e_guesses * e_guesses  # Variance
            stddev_guesses = sqrt(var_guesses) # Standard deviation

            print(f"{max_number}\t{pr_flip:.3f}\t{e_guesses:.2f}\t{stddev_guesses:.2f}")


if __name__ == "__main__":
    run_game()
