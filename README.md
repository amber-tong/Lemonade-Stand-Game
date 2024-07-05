# Lemonade-Stand-Game
This project focuses on agent-based modelling, non-cooperative and cooperative games, and sequential decision-making under uncertainty.

### Game Description
On Lemonade Island, three players set up lemonade stands on a circular beach with twelve spots (like the numbers on a clock). The price of lemonade is fixed, and customers go to the nearest stand. Each night, the players move their stands simultaneously without any cost. The game is repeated for 100 days.

### Utility Calculation
- **Different Spots:** Each player's utility is the sum of the distances to the nearest stands on either side.
- **Same Spot:** Each player receives £8.
- **Two Collocated Stands:** Collocated players receive £6 each, and the lone player receives £12.
- **Total Utility:** Always £24 per round.

### Example
If Alice sets up at 3 o'clock, Bob at 10 o'clock, and Candy at 6 o'clock:
- **Clockwise Arrangement:** Alice (3), Candy (6), Bob (10)
- **Distances:** Alice to Candy = 3 spots, Candy to Bob = 4 spots, Bob to Alice = 5 spots
- **Utilities:** Alice = £8, Bob = £9, Candy = £7

## How My Agent Works

The game progresses through the following steps:

1. **Initialisation**: Players start with strategies set to "equilibrium" by default.
2. **Daily Operations**: Each day, players decide where to set up their stands based on their chosen strategy:
   - **Random**: Chooses a random spot.
   - **Popular Spot**: Sets up at the spot most frequently chosen by all players in previous rounds.
   - **Previous Success**: Returns to spots that yielded the highest utility in previous rounds.
   - **Collaboration**: Players strategically collaborate to maximize profits.
   - **Equilibrium**: Default strategy, setting up at spot 12.
3. **Utility Calculation**: Each player's utility is calculated based on their stand's proximity to other stands. Utilities are updated daily.
4. **Strategy Changes**: Strategies may change based on predefined conditions (e.g., after a certain number of days or consecutive high utilities).
5. **End of Game**: After 100 days, total profits for each player are displayed.

## Getting Started

To run the simulation:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/lemonade-stand-game.git
   cd lemonade-stand-game

2. Run the simulation:
   ```bash
   python main.py
