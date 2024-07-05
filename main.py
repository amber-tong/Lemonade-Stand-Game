import random

num_players = 3
num_days = 100
num_spots = 12

players = [{'name': f'Player {i+1}', 'location': None, 'profit': 0, 'strategy': None} for i in range(num_players)]
results = [0, 0, 0]
previous_locations = []
previous_highest_utility = []
player1_consecutive_high_utility = 0
player2_consecutive_high_utility = 0
player3_consecutive_high_utility = 0
count = 0

def main():
    set_player_strategies(["equilibrium", "equilibrium", "equilibrium"])
    play_game()

def set_player_strategies(strategies):
    for i, player in enumerate(players):
        if strategies[i] == "equilibrium":
            player['strategy'] = "equilibrium"
        elif strategies[i] == "random":
            player['strategy'] = "random"
        elif strategies[i] == "popular spot":
            player['strategy'] = "popular spot"
        elif strategies[i] == "previous success":
            player['strategy'] = "previous success"
        elif strategies[i] == "collaborate1":
            player['strategy'] = "collaborate1"
        elif strategies[i] == "collaborate2":
            player['strategy'] = "collaborate2"
        else:
            raise ValueError(f"Invalid strategy: {strategies[i]}")

def play_game():
    global player1_consecutive_high_utility, player2_consecutive_high_utility, player3_consecutive_high_utility, count

    # Iterate through 100 days (num_days)
    for day in range(num_days):
        count += 1 # Keeps track of what day it is
      
        # Set up the lemonade stands
        set_up()
      
        # Sell lemonade for the day
        sell_lemonade()

        # Start changing strategies
        if count == 10:
            set_player_strategies(["random", "equilibrium", "equilibrium"]) # Player 1 changes
        if count == 11: 
            set_player_strategies(["random", "random", "popular spot"]) # Player 2 and 3 changes
        if count == 21:
            set_player_strategies(["random", "previous success", "popular spot"]) # Player 2 changes
      
        # Change strategy if one player has the highest utility for 5 days in a row
        # The other 2 players collaborate to get a higher utility
        if player1_consecutive_high_utility == 5 and count > 21:
            set_player_strategies(["random", "collaborate1", "collaborate2"])
            player1_consecutive_high_utility = 0
        if player2_consecutive_high_utility == 5 and count > 21:
            set_player_strategies(["collaborate1", "previous success", "collaborate2"]) 
            player2_consecutive_high_utility = 0
        if player3_consecutive_high_utility == 5 and count > 21:
            set_player_strategies(["collaborate1", "collaborate2", "popular spot"]) 
            player3_consecutive_high_utility = 0
 
        # Reset profit and location at the end of the day
        for player in players:
            player['profit'] = 0
            player['location'] = 0

    # Print results at the end of the game
    print("Player 1 total sum of profit is:", results[0])
    print("Player 2 total sum of profit is:", results[1])
    print("Player 3 total sum of profit is:", results[2])

def set_up():
    global count
    
    # Choose a location for each player
    for player in players:
    
        # Random strategy for player 1 on the eleventh day where they pick any location apart from 12 because they are diverting from players 2 and 3 to gain more profit
        if player['strategy'] == "random" and count == 10:
            player['location'] = random.randint(1, 11)

        # Random strategy - randomly pick a location everyday
        if player['strategy'] == "random":
            player['location'] = random.randint(1, num_spots)

        # Stick to a popular spot strategy - mixed strategy
        elif player['strategy'] == "popular spot":
            # Finds the location that appears most frequently in the previous_locations list 
            popular_spot = max(set(previous_locations), key=previous_locations.count)
            player['location'] = popular_spot

        # Stick to the highest utililty spot strategy
        elif player['strategy'] == 'previous success':
            # Finds the location that appears most frequently in the previous_highest_utility list 
            previous_success = max(set(previous_highest_utility), key=previous_highest_utility.count)
            player['location'] = previous_success

        # Collaboration strategy - first collaborator randomly picks a location
        elif player['strategy'] == 'collaborate1':
            player['location'] = random.randint(1, num_spots)
            collaboration = player['location']
        # Collaboration strategy - second collaborator picks a location 6 steps away from the first collaborator
        elif player['strategy'] == 'collaborate2':
            player['location'] = (collaboration + 6)%12

        # Equilibrium strategy
        elif player['strategy'] == 'equilibrium':
            player['location'] = 12

        else:
            raise ValueError(f"Invalid strategy: {player['strategy']}")

    # previous_locations list containing all players previous locations
    previous = [player['location'] for player in players]
    for i in range(3):
        previous_locations.append(previous[i])

def sell_lemonade():
    global player1_consecutive_high_utility, player2_consecutive_high_utility, player3_consecutive_high_utility
  
    # Calculate the utility for each player
    utility_profit = [utility(players[0]['location'], players[1]['location'], players[2]['location']), utility(players[1]['location'], players[0]['location'], players[2]['location']), utility(players[2]['location'], players[1]['location'], players[0]['location']) ]
  
    i=0
    # Update profit
    for player in players:
        player['profit'] += utility_profit[i]
        results[i] += utility_profit[i]
        i+=1

    # previous_highest_utility list containing the location with the highest utility at the end of everyday after the eleventh day
    if count > 11:  
        highest_utility_index = utility_profit.index(max(utility_profit))
        previous_highest_utility.append(players[highest_utility_index]['location'])

    # Calculate which player has the highest utility
    highest_utility_player = max(players, key=lambda p: p['profit'])

    # Make count of how many consecutive days the player has had the highest utility
    if highest_utility_player['name'] == players[0]['name']:
        player1_consecutive_high_utility += 1
        player2_consecutive_high_utility = 0 # Reset to 0 - not consecutive
        player3_consecutive_high_utility = 0
    elif highest_utility_player['name'] == players[1]['name']:
        player1_consecutive_high_utility = 0
        player2_consecutive_high_utility += 1
        player3_consecutive_high_utility = 0
    else:
        player1_consecutive_high_utility = 0
        player2_consecutive_high_utility = 0
        player3_consecutive_high_utility += 1

def utility(player1, player2, player3):
    u = 0

    # Calculate the anti clockwise distance and clockwise distance from the player
    if (player1 < player3):
        if(player3 > player2 and player1 < player2):
            u = (player1 + 12) - player3
            u += player2 - player1
        else:
            u = player3 - player1
            u += ((player1 + 12) - player2) % 12
    else:
        if (player2 < player1 and player2 > player3):
            u = (player3 + 12) - player1
            u += player1 - player2
        else:
            u = player1 - player3
            u += ((player2 + 12) - player1) % 12

    # If the other 2 players are on the same spot, player1 gets the highest utility
    if (player2 == player3):
        u = 12
    # If player1 is on the same spot as one of the other players
    if (player1 == player2 or player1 == player3):
        u = 6
    # If all players are on the same spot
    if (player1 == player2 == player3):
        u = 8
      
    return u

main()