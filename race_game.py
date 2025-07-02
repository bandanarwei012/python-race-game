import random
import time
import os

# --- Game Configuration ---
TRACK_LENGTH = 70
NUM_OPPONENTS = 4
OPPONENT_NAMES = ["Shadow", "Vortex", "Blaze", "Titan", "Raptor", "Sting"]
random.shuffle(OPPONENT_NAMES) # Mix them up for each game

# --- Helper Functions ---

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    """Prints the welcome message and rules."""
    clear_screen()
    print("*" * 40)
    print("*" + " " * 38 + "*")
    print("*      WELCOME TO THE TERMINAL RACE!     *")
    print("*" + " " * 38 + "*")
    print("*" * 40)
    print("\nGet ready to race against the best AI drivers.")
    print("Choose your move each turn to outsmart them and reach the finish line first!")
    input("\nPress Enter to start...")

def draw_track(car_name, position, car_char):
    """Draws a single car's track."""
    track = ['-'] * TRACK_LENGTH
    # Ensure the car doesn't go past the finish line visually
    pos_on_track = min(position, TRACK_LENGTH - 1)
    track[pos_on_track] = car_char
    
    track_str = "".join(track)
    print(f"{car_name:<10} |{track_str}| Finish")

def display_race_status(player_name, player_pos, opponents):
    """Displays the current positions of all cars."""
    clear_screen()
    print("=" * (TRACK_LENGTH + 20))
    print(f"RACE STATUS - Turn {turn_counter}")
    print("-" * (TRACK_LENGTH + 20))

    # Player's track
    draw_track(f"{player_name} (You)", player_pos, '>')

    # Opponents' tracks
    for i, opp in enumerate(opponents):
        draw_track(opp['name'], opp['position'], str(i+1))
        
    print("=" * (TRACK_LENGTH + 20))

def get_player_choice():
    """Gets and validates the player's move choice."""
    while True:
        print("\nChoose your move:")
        print("  1. Go Fast      (High speed, high risk)")
        print("  2. Go Steady    (Medium speed, low risk)")
        print("  3. Be Cautious  (Low speed, very low risk)")
        
        choice = input("Enter your choice (1, 2, or 3): ")
        if choice in ['1', '2', '3']:
            return int(choice)
        else:
            print("Invalid input! Please enter 1, 2, or 3.")
            time.sleep(1)

def calculate_move(choice):
    """Calculates the move distance and any setbacks based on choice."""
    if choice == 1: # Go Fast
        move = random.randint(5, 9)
        if random.random() < 0.40: # 40% chance of a mishap
            setback = random.randint(3, 7)
            print(f"\nOh no! You pushed too hard and spun out! You lose {setback} positions.")
            return move - setback
        else:
            print(f"\nYou floored it! Great move!")
            return move
            
    elif choice == 2: # Go Steady
        move = random.randint(3, 6)
        if random.random() < 0.15: # 15% chance of a mishap
            setback = random.randint(1, 3)
            print(f"\nA slight wobble... you lost {setback} positions.")
            return move - setback
        else:
            print(f"\nSmooth and steady.")
            return move

    elif choice == 3: # Be Cautious
        move = random.randint(1, 3)
        # Very low chance of a minor issue
        if random.random() < 0.05:
            print(f"\nYou took it too easy and lost 1 position.")
            return move - 1
        else:
            print(f"\nPlaying it safe.")
            return move

def update_opponent_positions(opponents):
    """Updates the positions of all AI opponents."""
    for opp in opponents:
        # Simple AI: Opponents have different tendencies
        tendency = opp.get('tendency', 0.5) # Default to balanced
        
        if random.random() < tendency:
            # More likely to choose a risky move
            opp_choice = random.choice([1, 1, 2])
        else:
            # More likely to choose a safe move
            opp_choice = random.choice([2, 2, 3])

        move = calculate_move(opp_choice)
        # We don't need to print messages for opponents, so we simplify the call
        if opp_choice == 1:
            opp_move = random.randint(5, 9)
            if random.random() < 0.40: opp_move -= random.randint(3, 7)
        elif opp_choice == 2:
            opp_move = random.randint(3, 6)
            if random.random() < 0.15: opp_move -= random.randint(1, 3)
        else: # choice 3
            opp_move = random.randint(1, 3)
            if random.random() < 0.05: opp_move -= 1
        
        opp['position'] += opp_move
        if opp['position'] < 0:
            opp['position'] = 0

def check_for_winner(player_name, player_pos, opponents):
    """Checks if any car has crossed the finish line."""
    if player_pos >= TRACK_LENGTH:
        return player_name
    
    for opp in opponents:
        if opp['position'] >= TRACK_LENGTH:
            return opp['name']
            
    return None

# --- Main Game Logic ---

print_welcome()

player_name = input("Enter your driver's name: ")
if not player_name:
    player_name = "Player"

# Initialize game state
player_position = 0
opponents = [
    {'name': OPPONENT_NAMES[i], 'position': 0, 'tendency': random.uniform(0.3, 0.7)}
    for i in range(NUM_OPPONENTS)
]
turn_counter = 0
winner = None

# Main game loop
while winner is None:
    turn_counter += 1
    display_race_status(player_name, player_position, opponents)
    
    player_choice = get_player_choice()
    move_distance = calculate_move(player_choice)
    player_position += move_distance
    
    # Ensure player position doesn't go below zero
    if player_position < 0:
        player_position = 0
        
    update_opponent_positions(opponents)
    
    winner = check_for_winner(player_name, player_position, opponents)
    
    # Pause for effect so the player can read the messages
    time.sleep(2.0)

# --- Game Over ---
display_race_status(player_name, player_position, opponents)
print("\n" + "="*30)
print("THE RACE IS OVER!")
print(f"And the winner is... {winner.upper()}!")
print("="*30)
