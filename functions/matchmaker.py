from itertools import combinations, product
import random

def matchmaker(tank, dps, support):
    acceptable_teams = []
    smallest_difference = 1000000
    best_teams = ()

    # Generate all combinations of 2 DPS and 2 support players
    dps_combinations = list(combinations(dps, 2))
    support_combinations = list(combinations(support, 2))

    # For each tank, pair it with each possible combination of DPS and support players
    all_teams = list(product(tank, dps_combinations, support_combinations))


    half_index = len(all_teams) // 2
    first_half = all_teams[:half_index]
    second_half = (all_teams[half_index:])[::-1]

    for team1, team2 in zip(first_half, second_half):
        team1_average = (team1[0]["tank"] + team1[1][0]["dps"] + team1[1][1]["dps"] + team1[2][0]["support"] + team1[2][1]["support"])/5
        team2_average = (team1[0]["tank"] + team2[1][0]["dps"] + team2[1][1]["dps"] + team2[2][0]["support"] + team2[2][1]["support"])/5
        difference = abs(team1_average - team2_average)
        if difference <= 0:
            acceptable_teams.append((team1, team1_average, team2, team2_average, difference))
        if difference < smallest_difference:
            smallest_difference = difference
            best_teams = (team1, team1_average, team2, team2_average, difference)
    
    if len(acceptable_teams) < 2:
        return best_teams
    
    return random.choice(acceptable_teams)