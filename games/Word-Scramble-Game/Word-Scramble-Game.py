#!/usr/bin/env python3
"""
🔤 Word Scramble Game
=====================
A terminal-based word guessing game where players unscramble shuffled letters.

Features:
  - Random word selection from a categorised built-in word list
  - Difficulty levels (Easy / Medium / Hard)
  - Adaptive word selection based on difficulty
  - Scrambled letter display
  - Hint system (reveals the word's category)
  - 3 lives per game
  - Score tracking across rounds
  - Zero external dependencies (pure Python)
"""

import random
import time
import os
import sys

# ── Word bank ────────────────────────────────────────────────────────────────

WORD_BANK: dict[str, list[str]] = {
    "🐾 Animals": [
        "elephant", "penguin", "dolphin", "cheetah", "giraffe",
        "kangaroo", "crocodile", "flamingo", "panther", "squirrel",
    ],
    "🍎 Fruits": [
        "mango", "papaya", "cherry", "apricot", "banana",
        "guava", "lychee", "peach", "plum", "strawberry",
    ],
    "🌍 Countries": [
        "brazil", "france", "canada", "japan", "kenya",
        "norway", "mexico", "india", "egypt", "sweden",
    ],
    "🔬 Science": [
        "gravity", "nucleus", "photon", "proton", "molecule",
        "quantum", "enzyme", "plasma", "neuron", "voltage",
    ],
    "🎵 Music": [
        "rhythm", "melody", "chorus", "octave", "guitar",
        "violin", "harmony", "trumpet", "bassoon", "symphony",
    ],
    "🏅 Sports": [
        "cricket", "tennis", "hockey", "soccer", "rowing",
        "karate", "boxing", "cycling", "archery", "fencing",
    ],
}

# ── Difficulty settings ─────────────────────────────────────────────────────

DIFFICULTY_LEVELS = {
    "easy": {
        "min_length": 1,
        "max_length": 5,
        "points": 5,
    },
    "medium": {
        "min_length": 6,
        "max_length": 8,
        "points": 10,
    },
    "hard": {
        "min_length": 9,
        "max_length": 100,
        "points": 20,
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def scramble(word: str) -> str:
    """Shuffle letters until the result differs from the original."""
    letters = list(word)

    for _ in range(100):
        random.shuffle(letters)
        scrambled = "".join(letters)

        if scrambled != word:
            return scrambled

    return "".join(letters)


def fancy_scramble(word: str) -> str:
    """Return the scrambled word with spaces between letters."""
    return "  ".join(scramble(word).upper())


def slow_print(text: str, delay: float = 0.03) -> None:
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)

    print()


def draw_lives(lives: int, max_lives: int = 3) -> str:
    return "❤️ " * lives + "🖤 " * (max_lives - lives)


def draw_header(
    score: int,
    round_num: int,
    lives: int,
    difficulty: str,
) -> None:
    print("╔══════════════════════════════════════════════╗")
    print("║          🔤  W O R D  S C R A M B L E  🔤         ║")
    print("╠══════════════════════════════════════════════╣")
    print(
        f"║  Round: {round_num:<5}  "
        f"Score: {score:<6}  "
        f"Lives: {draw_lives(lives):<14}║"
    )
    print(f"║  Difficulty: {difficulty.capitalize():<31}║")
    print("╚══════════════════════════════════════════════╝")
    print()


# ── Difficulty logic ─────────────────────────────────────────────────────────

def choose_difficulty() -> str:
    """Ask player to select difficulty."""
    print("\n  🎯 Select Difficulty:")
    print("      • Easy")
    print("      • Medium")
    print("      • Hard\n")

    while True:
        difficulty = input("  ➤  Enter difficulty: ").strip().lower()

        if difficulty in DIFFICULTY_LEVELS:
            return difficulty

        print("  ❌ Invalid difficulty! Choose easy, medium, or hard.\n")


def pick_word_by_difficulty(difficulty: str) -> tuple[str, str]:
    """Pick word based on difficulty settings."""

    settings = DIFFICULTY_LEVELS[difficulty]

    valid_words = []

    for category, words in WORD_BANK.items():
        filtered_words = [
            word for word in words
            if settings["min_length"] <= len(word) <= settings["max_length"]
        ]

        if filtered_words:
            valid_words.append((category, filtered_words))

    category, words = random.choice(valid_words)
    word = random.choice(words)

    return word, category


# ── Game logic ────────────────────────────────────────────────────────────────

def play_round(
    score: int,
    round_num: int,
    lives: int,
    difficulty: str,
) -> tuple[int, int, bool]:
    """
    Run one round.
    Returns (new_score, new_lives, still_playing).
    """

    word, category = pick_word_by_difficulty(difficulty)

    scrambled = fancy_scramble(word)

    hint_used = False
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        clear()

        draw_header(score, round_num, lives, difficulty)

        print(f"  🔀  Unscramble this word:\n")
        print(f"      ✨  {scrambled}  ✨\n")

        print(
            f"  Letters: {len(word)}   |   "
            f"Attempts left this round: {max_attempts - attempts}"
        )

        if hint_used:
            print(f"  💡 Hint: {category}")

        print()
        print("  Commands: [answer] · 'hint' · 'skip' · 'quit'")
        print()

        try:
            raw = input("  ➤  Your guess: ").strip().lower()

        except (EOFError, KeyboardInterrupt):
            return score, lives, False

        if raw == "quit":
            return score, lives, False

        if raw == "skip":
            print(f"\n  ⏭️  Skipped! The word was: {word.upper()}")
            time.sleep(1.5)

            return score, lives, True

        if raw == "hint":
            if not hint_used:
                hint_used = True
                print(f"\n  💡 Hint unlocked: {category}")

            else:
                print("\n  💡 You already used your hint!")

            time.sleep(1)
            continue

        attempts += 1

        if raw == word:
            base_points = DIFFICULTY_LEVELS[difficulty]["points"]

            bonus = base_points if not hint_used else base_points // 2

            score += bonus

            clear()

            draw_header(score, round_num, lives, difficulty)

            slow_print(
                f"\n  🎉 Correct! +{bonus} points "
                f"{'(hint used: half points)' if hint_used else ''}\n"
            )

            time.sleep(1.5)

            return score, lives, True

        else:
            remaining = max_attempts - attempts

            if remaining > 0:
                print(
                    f"\n  ❌ Nope! Try again. "
                    f"({remaining} attempt{'s' if remaining != 1 else ''} left)"
                )

                time.sleep(1)

            else:
                lives -= 1

                clear()

                draw_header(score, round_num, lives, difficulty)

                slow_print(
                    f"\n  💔 Out of attempts! "
                    f"The word was: {word.upper()}\n"
                )

                time.sleep(2)

                return score, lives, lives > 0

    return score, lives, lives > 0


def game_over_screen(score: int, rounds_played: int) -> None:
    clear()

    print()
    print("  ╔══════════════════════════════════╗")
    print("  ║         💀  GAME  OVER  💀          ║")
    print("  ╚══════════════════════════════════╝")
    print()

    slow_print(
        f"  You survived "
        f"{rounds_played} round{'s' if rounds_played != 1 else ''}."
    )

    slow_print(f"  Final score: {score} points")

    print()

    grade = (
        "🏆 Wordsmith Supreme!" if score >= 80 else
        "🥇 Excellent!" if score >= 60 else
        "🥈 Good effort!" if score >= 40 else
        "🥉 Keep practising!" if score >= 20 else
        "📚 Hit the dictionary!"
    )

    slow_print(f"  {grade}")

    print()


def welcome_screen() -> None:
    clear()

    print()

    slow_print(
        "  ╔══════════════════════════════════════════════╗",
        0.005,
    )

    slow_print(
        "  ║       🔤  W O R D  S C R A M B L E  🔤        ║",
        0.005,
    )

    slow_print(
        "  ╚══════════════════════════════════════════════╝",
        0.005,
    )

    print()

    slow_print(
        "  Unscramble the letters to guess the hidden word!",
        0.02,
    )

    print()

    print("  📋  Rules:")
    print("      • 3 lives per game — lose one each time you run out of attempts")
    print("      • 3 attempts per word before losing a life")
    print("      • Type 'hint' to reveal the word's category")
    print("      • Type 'skip' to skip a word with no penalty")
    print("      • Type 'quit' to end the game at any time")
    print("      • Difficulty affects word complexity and score rewards")

    print()

    input("  Press Enter to start… ")


def main() -> None:
    welcome_screen()

    difficulty = choose_difficulty()

    score = 0
    lives = 3
    round_num = 1

    while lives > 0:
        score, lives, still_playing = play_round(
            score,
            round_num,
            lives,
            difficulty,
        )

        if not still_playing:
            break

        round_num += 1

    game_over_screen(score, round_num)

    try:
        again = input("  Play again? (y/n): ").strip().lower()

    except (EOFError, KeyboardInterrupt):
        again = "n"

    if again == "y":
        main()

    else:
        slow_print("\n  Thanks for playing! 👋\n", 0.02)


if __name__ == "__main__":
    main()
