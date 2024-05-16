import math
import random

class PlayerProfile:
    def __init__(self, rating, rd=20, volatility=0.1):
        self.rating = rating
        self.rd = rd
        self.volatility = volatility
        self.history = []  # Store history of rating, rd, and volatility

    def update_profile(self, new_rating, new_rd, new_volatility):
        self.rating = new_rating
        self.rd = new_rd
        self.volatility = new_volatility
        self.history.append((new_rating, new_rd, new_volatility))

    def get_latest_profile(self):
        if self.history:
            return self.history[-1]
        else:
            return (self.rating, self.rd, self.volatility)

class Player:
    def __init__(self, profile):
        self.profile = profile

    def update_profile(self, new_rating, new_rd, new_volatility):
        self.profile.update_profile(new_rating, new_rd, new_volatility)

    def get_latest_profile(self):
        return self.profile.get_latest_profile()

class Glicko2System:
    def __init__(self, tau=0.6, default_rd=20, default_vol=0.1, k_factor=40, inactivity_penalty=10):
        self.tau = tau                   # System constant (the "concentration" of ratings)
        self.default_rd = default_rd     # Default rating deviation
        self.default_vol = default_vol   # Default volatility
        self.k_factor = k_factor         # Customizable K-factor
        self.inactivity_penalty = inactivity_penalty  # Penalty for inactivity

    def _g(self, rd):
        return 1 / math.sqrt(1 + 3 * (rd ** 2) / (math.pi ** 2))

    def calculate_expected_outcome(self, rating_i, rating_j, rd_j):
         rating_difference = rating_j - rating_i
         return 1 / (1 + 10 ** (-self._g(rd_j) * rating_difference / 200))

    def update_player_ratings(self, player1, player2, match_result, match_importance):
        '''expected_outcome = self.calculate_expected_outcome(player1.profile.rating, player2.profile.rating, player2.profile.rd)
        g_rd_j = self._g(player2.profile.rd)
        E = expected_outcome
        v = self._v(g_rd_j, E)
        d2 = self._d2(player1.profile.rating, player1.profile.rd, player2.profile.rd, g_rd_j, E)
        S = 1 if match_result == 1 else 0
        delta = self.calculate_delta(v, d2, player1.profile.rating, S, E, g_rd_j)
        
        # Update player profiles
        new_rating_player1 = player1.profile.rating + delta
        new_rd_player1 = math.sqrt(1 / (1 / (player1.profile.rd ** 2) + 1 / v))
        player1.update_profile(new_rating_player1, new_rd_player1, player1.profile.volatility)
        
        new_rating_player2 = player2.profile.rating - delta
        new_rd_player2 = math.sqrt(1 / (1 / (player2.profile.rd ** 2) + 1 / v))
        player2.update_profile(new_rating_player2, new_rd_player2, player2.profile.volatility)'''
        
        # Calculate expected outcome
        expected_outcome = self.calculate_expected_outcome(player1.profile.rating, player2.profile.rating, player2.profile.rd)
        
        # Calculate v and d2
        # v is volatility , d2 is variance of the player rating 
        g_rd_j = self._g(player2.profile.rd)
        E = expected_outcome
        v = self._v(g_rd_j, E)
        d2 = self._d2(player1.profile.rating, player1.profile.rd, player2.profile.rd, g_rd_j, E)

        # Update ratings for player1 and player2 based on match result
        # Simulate match outcome (1: player1 wins, 0: player2 wins)
        if match_result == 1:
            S = 1
        else:
            S = 0
        
        delta = self.calculate_delta(v, d2, player1.profile.rating, S, E, g_rd_j)
        
        new_rating_player1 = player1.profile.rating + delta
        new_rd_player1 = math.sqrt(1 / (1 / (player1.profile.rd ** 2) + 1 / v))
        player1.update_profile(new_rating_player1, new_rd_player1, player1.profile.volatility)
        
        new_rating_player2 = player2.profile.rating - delta
        
        new_rd_player2 = math.sqrt(1 / (1 / (player2.profile.rd ** 2) + 1 / v))
        player2.update_profile(new_rating_player2, new_rd_player2, player2.profile.volatility)
        
        
        
        print(player1.profile.rating)
        print(player2.profile.rating)
        

    def _v(self, g_rd_j, E):
        return 1 / (g_rd_j ** 2 * E * (1 - E))

    def _d2(self, rating_i, rd_i, rd_j, g_rd_j, E):
        v = self._v(g_rd_j, E)
        return 1 / (1 / (rd_i ** 2) + 1 / v)

    def calculate_delta(self, v, d2, rating_i, S, E, g_rd_j):
        return v * g_rd_j * (S - E)

    def print_expected_outcome(self, player1, player2):
        expected_outcome = self.calculate_expected_outcome(player1.profile.rating, player2.profile.rating, player2.profile.rd)
        print(f"Expected outcome for Player 1 against Player 2: {expected_outcome:.2f}")


    def _g(self, rd):
        return 1 / math.sqrt(1 + 3 * (rd ** 2) / (math.pi ** 2))

    def calculate_expected_outcome(self, rating_i, rating_j, rd_j):
        rating_difference = abs(rating_j - rating_i)
        return 1 / (1 + 10 ** (-self._g(rd_j) * rating_difference / 200))
     

    def _E(self, player, opponent):
        return self.calculate_expected_outcome(player.rating, opponent.rating, opponent.rd)


    ''' def _f(self, x, player, opponents, results):
        v = 0
        for i, opponent in enumerate(opponents):
            E = self._E(player, opponent)
            v += (self._g(opponent.rd) * (results[i] - E))
        return (v / self._d2(player, opponents))'''

class PlayerManager:
    def __init__(self):
        self.players = {}  # Dictionary to store players and their profiles

    def add_player(self, player_id, rating, rd=20, volatility=0.1):
        if player_id not in self.players:
            profile = PlayerProfile(rating, rd, volatility)
            self.players[player_id] = Player(profile)
            
            return  self.players[player_id]

    def setup_match(self, player1_id, player2_id, match_result):
        if player1_id in self.players and player2_id in self.players:
            player1 = self.players[player1_id]
            player2 = self.players[player2_id]
            glicko2.update_player_ratings(player1, player2, match_result)
            glicko2.print_expected_outcome(player1, player2)
        else:
            print("One or both players do not exist.")

# Example usage:
if __name__ == "__main__":
    
    player_manager = PlayerManager()

    # Add players
    player1 = player_manager.add_player("player1", rating=2048)
    player2 = player_manager.add_player("player2", rating=2450)

    glicko2 = Glicko2System()
    
    match_result = random.choice([1, 0])  # 1: player1 wins, 0: player2 wins

    player_manager.setup_match("player1", "player2", match_result)
    
    player1_profile_new = player1.get_latest_profile()
    player2_profile_new = player2.get_latest_profile()
    
    print(player1_profile_new)
    
    player3 = player_manager.add_player("player3", rating=1000)
    player_manager.setup_match("player1", "player3", match_result)
    
    player1_profile_new = player1.get_latest_profile()
    player3_profile_new = player3.get_latest_profile()
    
    print(player1_profile_new)
    print(player3_profile_new)

    
    '''num_matches = 5

    for i in range(num_matches):
        match_result = random.choice([1, 0])  # 1: player1 wins, 0: player2 wins
        print('match result is ', match_result)
        player_manager.setup_match("player1", "player2", match_result)
        '''
    
      
