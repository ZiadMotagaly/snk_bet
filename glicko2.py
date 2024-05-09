# Load necessary modules
import math
import random

# Define Player and Glicko2System classes
class Player:
    def __init__(self, rating, rd=20, vol=0.1, last_played=0):
        self.rating = rating    # Player's rating
        self.rd = rd            # Player's rating deviation
        self.vol = vol          # Player's volatility (how much the rating changes)
        self.last_played = last_played  # Timestamp of last activity
        self.history = []  # Store history of rating, rd, and volatility

        

class Glicko2System:
    def __init__(self, tau=0.6, default_rd=20, default_vol=0.1, k_factor=40, inactivity_penalty=10):
        self.tau = tau                   # System constant (the "concentration" of ratings)
        self.default_rd = default_rd     # Default rating deviation
        self.default_vol = default_vol   # Default volatility
        self.k_factor = k_factor         # Customizable K-factor
        self.inactivity_penalty = inactivity_penalty  # Penalty for inactivity

    # g function scales the rating deviation to a scale dependent on RD 
    def _g(self, rd):
        return 1 / math.sqrt(1 + 3 * (rd ** 2) / (math.pi ** 2))

    def calculate_expected_outcome(self, rating_i, rating_j, rd_j):
         rating_difference = rating_j - rating_i
         return 1 / (1 + 10 ** (-self._g(rd_j) * rating_difference / 200))
        #return 1 / (1 + 10 ** (-self._g(rd_j) * (rating_i - rating_j) / 200))
    
    def update_player_ratings(self, player1, player2, match_result):
        # Calculate expected outcome
        expected_outcome = self.calculate_expected_outcome(player1.rating, player2.rating, player2.rd)
        
        # Calculate v and d2
        # v is volatility , d2 is variance of the player rating 
        g_rd_j = self._g(player2.rd)
        E = expected_outcome
        v = self._v(g_rd_j, E)
        d2 = self._d2(player1.rating, player1.rd, player2.rd, g_rd_j, E)

        # Update ratings for player1 and player2 based on match result
        # Simulate match outcome (1: player1 wins, 0: player2 wins)
        if match_result == 1:
            S = 1
        else:
            S = 0
        
        delta = self.calculate_delta(v, d2, player1.rating, S, E, g_rd_j)
        player1.rating += delta
        player1.rd = math.sqrt(1 / (1 / (player1.rd ** 2) + 1 / v))
        
        
        # Apply inactivity penalty to player1
        #self.apply_inactivity_penalty(player1)

        # Update player2
        player2.rating -= delta
        player2.rd = math.sqrt(1 / (1 / (player2.rd ** 2) + 1 / v))
        player2.last_played = 0  # Reset last played timestamp
        
        print(player1.rating)
        print(player2.rating)
     
        
    def _v(self, g_rd_j, E):
        return 1 / (g_rd_j ** 2 * E * (1 - E))

    def _d2(self, rating_i, rd_i, rd_j, g_rd_j, E):
        v = self._v(g_rd_j, E)
        return 1 / (1 / (rd_i ** 2) + 1 / v)

    def calculate_delta(self, v, d2, rating_i, S, E, g_rd_j):
        return v * g_rd_j * (S - E)

    def apply_inactivity_penalty(self, player):
        # Apply penalty for inactivity
        if player.last_played > 0:  # Check if player has been inactive
            penalty = self.inactivity_penalty
            player.rating -= penalty
            player.rd = min(math.sqrt(player.rd ** 2 + penalty ** 2), self.default_rd)

    def print_expected_outcome(self, player1, player2):
        # Calculate expected outcome
        expected_outcome = self.calculate_expected_outcome(player1.rating, player2.rating, player2.rd)
        print(f"Expected outcome for Player 1 against Player 2: {expected_outcome:.2f}")

# Example usage:
if __name__ == "__main__":
    # Create players
    player1 = Player(rating=2048)
    player2 = Player(rating=2450)

    # Create Glicko-2 system
    glicko2 = Glicko2System()

    # Simulate a match result (1: player1 wins, 0: player2 wins)
    num_matches = 5


    '''#  player ratings based on match result
    glicko2.update_player_ratings(player1, player2, match_result)

    # Print expected outcome
    glicko2.print_expected_outcome(player1, player2)'''
    
    
    for i in range(num_matches):
        
        match_result = random.choice([1, 0])  # 1: player1 wins, 0: player2 wins
        print(match_result)

        glicko2.update_player_ratings(player1, player2, match_result)
        
        glicko2.print_expected_outcome(player1, player2)

        
# The expected outcome is slightly exponential. So winning expectation of 
# Comparing player 1 with elo 750 and elo 1750 , is less than 1750 and 2750. In the first run or iteration 

