"""
Hangman Game - A simple command-line implementation of the classic word guessing game.
"""
import csv
import random
import os
import sys
from typing import List, Set, Tuple, Optional


class HangmanGame:
    """Main class for the Hangman game logic."""

    # ASCII art for the gallows at different stages
    HANGMAN_STAGES = [
        # 0 wrong guesses (initial state)
        """
  +---+
  |   |
      |
      |
      |
      |
=========
        """,
        # 1 wrong guess (head)
        """
  +---+
  |   |
  O   |
      |
      |
      |
=========
        """,
        # 2 wrong guesses (head and body)
        """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
        """,
        # 3 wrong guesses (head, body, left arm)
        """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
        """,
        # 4 wrong guesses (head, body, both arms)
        """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
        """,
        # 5 wrong guesses (head, body, both arms, left leg)
        """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
        """,
        # 6 wrong guesses (complete hangman - game over)
        """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
        """
    ]

    def __init__(self, word_list_path: str = "word-list.csv"):
        """Initialize the game with the word list path."""
        self.word_list_path = word_list_path
        self.word_list: List[Tuple[str, int]] = []
        self.secret_word = ""
        self.guessed_letters: Set[str] = set()
        self.wrong_guesses: Set[str] = set()
        self.wrong_attempts = 0
        self.max_attempts = 6  # Head, body, left arm, right arm, left leg, right leg
        self.game_over = False
        self.won = False

    def load_word_list(self) -> bool:
        """Load the word list from CSV file."""
        try:
            with open(self.word_list_path, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header row
                self.word_list = [(row[0], int(row[1])) for row in reader]
            return True
        except (FileNotFoundError, IOError) as e:
            print(f"Error loading word list: {e}")
            return False

    def select_word(self, difficulty: int) -> bool:
        """Select a word based on the difficulty level (1-10)."""
        if not self.word_list:
            return False

        # Filter words by difficulty
        min_difficulty = max(1, difficulty - 1)
        max_difficulty = min(10, difficulty + 1)
        filtered_words = [
            word for word, diff in self.word_list 
            if min_difficulty <= diff <= max_difficulty
        ]

        if not filtered_words:
            # Fallback to all words if filtering yields nothing
            filtered_words = [word for word, _ in self.word_list]

        self.secret_word = random.choice(filtered_words).lower()
        return True

    def display_word(self) -> str:
        """Return the current state of the word with guessed letters revealed."""
        return " ".join(
            letter if letter.lower() in self.guessed_letters else "_"
            for letter in self.secret_word
        )

    def make_guess(self, guess: str) -> bool:
        """Process a player's guess. Return True if the guess was valid."""
        guess = guess.lower().strip()

        # Check if it's a single letter guess
        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                print(f"You already guessed '{guess}'. Try a different letter.")
                return False
            
            self.guessed_letters.add(guess)
            
            if guess not in self.secret_word:
                self.wrong_guesses.add(guess)
                self.wrong_attempts += 1
                print(f"Sorry, '{guess}' is not in the word.")
            else:
                print(f"Good guess! '{guess}' is in the word.")
            
            return True
            
        # Check if it's a full word guess
        elif len(guess) > 1 and guess.isalpha():
            if guess == self.secret_word:
                # Reveal all letters if correct word guess
                for letter in self.secret_word:
                    self.guessed_letters.add(letter)
                print(f"Congratulations! '{guess}' is the correct word!")
                self.won = True
            else:
                self.wrong_attempts += 1
                print(f"Sorry, '{guess}' is not the correct word.")
            
            return True
            
        else:
            print("Please enter a valid letter or word (letters only).")
            return False

    def check_game_state(self) -> None:
        """Check if the game is won or lost."""
        # Check if player won (all letters guessed)
        if all(letter.lower() in self.guessed_letters for letter in self.secret_word):
            self.game_over = True
            self.won = True
        
        # Check if player lost (too many wrong guesses)
        if self.wrong_attempts >= self.max_attempts:
            self.game_over = True
            self.won = False

    def display_game(self) -> None:
        """Display the current game state."""
        # Clear screen (works on both Windows and Unix-like systems)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Display title
        print("\n===== HANGMAN =====\n")
        
        # Display gallows
        print(self.HANGMAN_STAGES[self.wrong_attempts])
        
        # Display word
        print(f"\nWord: {self.display_word()}")
        
        # Display guessed letters
        print(f"\nIncorrect guesses: {', '.join(sorted(self.wrong_guesses)) if self.wrong_guesses else 'None'}")
        
        # Display attempts remaining
        print(f"Attempts remaining: {self.max_attempts - self.wrong_attempts}")

    def play(self) -> None:
        """Main game loop."""
        # Load word list
        if not self.load_word_list():
            print("Could not load word list. Exiting.")
            return

        # Welcome message and difficulty selection
        print("\n===== WELCOME TO HANGMAN =====\n")
        print("Try to guess the secret word one letter at a time.")
        print("You can also guess the entire word, but if you're wrong, you lose an attempt.")
        print("You have 6 incorrect guesses before the hangman is complete.\n")
        
        # Get difficulty level
        while True:
            try:
                difficulty = int(input("Choose difficulty level (1-10, 1=easiest, 10=hardest): "))
                if 1 <= difficulty <= 10:
                    break
                print("Please enter a number between 1 and 10.")
            except ValueError:
                print("Please enter a valid number.")
            except EOFError:
                print("\nUnable to read input. Using default difficulty level of 5.")
                difficulty = 5
                break
        
        # Select word based on difficulty
        if not self.select_word(difficulty):
            print("Could not select a word. Exiting.")
            return
        
        # Main game loop
        while not self.game_over:
            self.display_game()
            
            try:
                guess = input("\nEnter your guess (letter or word): ")
                
                if not guess:
                    print("Please enter a letter or word.")
                    continue
            except EOFError:
                print("\nUnable to read input. Exiting game.")
                break
                
            # Process guess and check game state
            if self.make_guess(guess):
                self.check_game_state()
        
        # Game over - display final state
        self.display_game()
        
        if self.won:
            print("\nCongratulations! You've guessed the word correctly!")
        else:
            print(f"\nGame over! The word was: {self.secret_word}")
        
        print("\nThanks for playing Hangman!")


def main():
    """Entry point for the application."""
    game = HangmanGame()
    game.play()
    
    # Ask if player wants to play again
    while True:
        try:
            play_again = input("\nWould you like to play again? (y/n): ").lower()
            if play_again in ['y', 'yes']:
                game = HangmanGame()
                game.play()
            elif play_again in ['n', 'no']:
                print("Thanks for playing Hangman! Goodbye!")
                break
            else:
                print("Please enter 'y' or 'n'.")
        except EOFError:
            print("\nUnable to read input. Exiting game.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted. Goodbye!")
        sys.exit(0)
