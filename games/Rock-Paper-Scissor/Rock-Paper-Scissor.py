class Rock_Paper_Scissor:
    def __init__(self):
        self.user_score = 0
        self.computer_score = 0
        self.rounds_played = 0 
        self.play_game()

    def users_play(self):
        import random
        choices = ["rock", "paper", "scissor"]
        
        user_choice = ""
        while user_choice not in choices:
            user_choice = input("Enter your choice (rock, paper, or scissor): ").lower()
            if user_choice not in choices:
                print("Invalid choice. Please choose rock, paper, or scissor.")

        computer_choice = random.choice(choices)
        print(f"Computer chose: {computer_choice}")

        if user_choice == computer_choice:
            print("It's a Tie!")
            return "tie"
        elif (user_choice == "rock" and computer_choice == "scissor") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissor" and computer_choice == "paper"):
            print("You Win this round!")
            return "user"
        else:
            print("Computer Wins this round!")
            return "computer"


    def statistics(self):
        print("\n--- Game Statistics ---")
        print(f"Rounds Played: {self.rounds_played}")
        print(f"Your Score: {self.user_score}")
        print(f"Computer Score: {self.computer_score}")


    def save_game(self):
        name = input("Enter your name to save the results (optional): ")
        if not name:
            name = "Anonymous"
        result_string = f"Player: {name}, Final Score: {self.user_score} - {self.computer_score} (User-Computer), Rounds: {self.rounds_played}\n"
        try:
            with open("game_results.txt", "a") as f:
                f.write(result_string)
            print("Game results saved successfully.")
        except IOError:
            print("Error: Could not save game results to file.")


    def play_game(self): 
        print("Welcome to Rock, Paper, Scissors!")
        while True:
            self.rounds_played += 1
            print(f"\n--- Round {self.rounds_played} ---")
            
            round_winner = self.users_play() # Call the users_play method for one round

            if round_winner == "user":
                self.user_score += 1
            elif round_winner == "computer":
                self.computer_score += 1

            self.statistics()
            play_again_input = input("do you want to play again ? (yes/no): ").lower()
            if play_again_input != "yes":
                print("\nThanks for playing! Final results:")
                self.statistics()
                self.save_game()
                break
        
game = Rock_Paper_Scissor()
print(game)