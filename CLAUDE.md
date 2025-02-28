# CLAUDE.md - Python Hangman Project

## Commands
- Run the game: `python main.py`
- Run tests: `pytest`
- Run single test: `pytest tests/test_file.py::test_function -v`
- Lint code: `flake8 .`
- Type check: `mypy .`
- Format code: `black .`

## Code Style Guidelines
- **Formatting**: Use Black with 88 character line limit
- **Imports**: Group imports (standard lib, third-party, local) with empty line between groups
- **Typing**: Use type hints for all function parameters and return values
- **Naming**: snake_case for variables/functions, CamelCase for classes, UPPER_CASE for constants
- **Documentation**: Docstrings for modules, classes, functions using """triple quotes"""
- **Error Handling**: Use specific exceptions with contextual error messages
- **Project Structure**: Keep code modular with clear separation of concerns

## Hangman Game Rules
1. **Setup**: Computer selects a secret word and displays blanks (underscores) for each letter
2. **Gameplay**: Player guesses one letter at a time
3. **Correct Guess**: All instances of the letter are revealed in their correct positions
4. **Incorrect Guess**: A body part is added to the gallows in this specific order:
   - 1st wrong guess: Add head
   - 2nd wrong guess: Add body/torso
   - 3rd wrong guess: Add left arm
   - 4th wrong guess: Add right arm
   - 5th wrong guess: Add left leg
   - 6th wrong guess: Add right leg (game over)
5. **Win Condition**: Player reveals all letters in the word before the stick figure is complete
6. **Lose Condition**: Stick figure is fully drawn after exactly 6 incorrect guesses
7. **Input Rules**: 
   - Player may guess a single letter or attempt the full word
   - Full word guesses cost one attempt if incorrect
   - Repeated letter guesses are not penalized (user is prompted to try a different letter)
   - Non-letter inputs are rejected with a friendly message
8. **Display**: Show the word progress, incorrect guesses, and remaining attempts
9. **Interaction Style**:
   - Keep responses friendly but concise
   - No hints or clues about the word should be given
   - If user attempts to discuss unrelated topics, politely redirect to the game

## Game Implementation Constraints
1. **Roles**: Computer always plays as word-picker (host); user always plays as guesser
2. **Difficulty Selection**: Game starts by asking user for difficulty level (1-10)
3. **Word Selection**: Words come from a 500-word list ordered by difficulty
   - Difficulty factors: word length, commonality, repeated characters, frequency of letters
   - Words selected pseudo-randomly from appropriate difficulty percentile
4. **Word Constraints**: All words are 5-10 characters long, English, no proper names
5. **ASCII Display**: Game shows hangman gallows and stick figure using ASCII art
6. **Progression**: Six incorrect guesses complete the hangman figure and end game

## Game Flow Implementation
1. **Initialize Game**:
   - Load word list from `word-list.csv`
   - Display welcome message and ASCII art title
   - Prompt user for difficulty level (1-10)

2. **Word Selection**:
   - Filter words by difficulty range based on user's selection
   - Randomly select a word from the filtered list
   - Initialize game state (guessed letters, remaining attempts, etc.)

3. **Game Loop**:
   - Display current state of the gallows using ASCII art
   - Show current word state (revealed letters and blanks)
   - Display list of incorrect guesses
   - Prompt user for a guess (letter or word)
   - Process input:
     * If input is a single letter:
       - Check if previously guessed; if so, prompt for different letter (no penalty)
       - If valid new letter, check against word
     * If input is a complete word:
       - Check if it matches the secret word
       - If incorrect, count as one wrong guess
     * If input is invalid or off-topic:
       - Provide friendly error message and redirect to game
   - Update game state based on valid guess:
     * If correct letter: reveal all instances in word
     * If correct word: player wins immediately
     * If incorrect: add to wrong guesses, decrease attempts, update gallows with next body part
   - Check win/lose conditions

4. **Game End**:
   - Display final state (completed gallows or completed word)
   - Show win or lose message
   - Reveal the word if player lost
   - Ask if player wants to play again