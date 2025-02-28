# Hangman Game

A simple command-line implementation of the classic Hangman word guessing game.

## Running the Game

```bash
python app.py
```

## How to Play

1. Choose a difficulty level from 1-10
2. Guess one letter at a time or try the entire word
3. You have 6 incorrect guesses before the game ends

Requires Python 3.6+

## Technical Comments

- This entire repository was written by Claude Code (for under $2 in less than 30 minutes [less than 10 minutes of actual "work" by Claude]) - I did not touch a single file or line of code.

```
Total cost: $1.30
Total duration (API): 6m 52.8s
Total duration (wall): 36m 32.7s
```

Claude's achievements:
* Created a word-list given vague constraints and estimated the difficulty of guessing that word. (Needs more validation but looks OK on first glance.)
* Created a decent CLI with a serviceable ASCII-art "UI".
* Implemented the rules of the game, and acted as a good "host" that isn't vulnerable to at least the most obvious tricks.
* Understood my design intentions even when I was vague or made explicit mistakes; made really good guesses when working with incomplete information or ambiguity.
* Code quality: fully typed; object-oriented solution; good separation of concerns; decent error-handling; identification of edge cases even without prompting; documentation of functions; used standard libraries only; mostly OS-independent; no obvious security vulnerabilities; no obvious performance bottlenecks; no obvious memory leaks.
* Handled source control reasonably well (I didn't give it time to make many incremental commits).
* Under 300 lines, including comments and the ASCII-art.
