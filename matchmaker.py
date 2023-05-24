tank = [4000, 2000]
dps = [3000, 2900, 3200, 3100]
support = [3300, 2700, 3900, 3500]

def mm_first_draft(tank, dps, support):
    team_1 = []
    team_2 = []
    smallest_difference = 1000000

    # tank is most important but we have no way to balance it. dps is second most important so try to balance tank through dps
    # try to find the optimal dps to give each tank to try to balance the gap

    # get all unique tank + dps combinations
    dps_teams = [[[dps[0], dps[1]], [dps[2], dps[3]]], [[dps[0], dps[2]], [dps[1], dps[3]]], [[dps[0], dps[3]], [dps[1], dps[2]]]]
    teams_with_tank = [[ [tank[0]] + dps_teams[0][0], [tank[1]] + dps_teams[0][1] ],
                       [ [tank[1]] + dps_teams[0][0], [tank[0]] + dps_teams[0][1] ],
                       [ [tank[0]] + dps_teams[1][0], [tank[1]] + dps_teams[1][1] ],
                       [ [tank[1]] + dps_teams[1][0], [tank[0]] + dps_teams[1][1] ],
                       [ [tank[0]] + dps_teams[2][0], [tank[1]] + dps_teams[2][1] ],
                       [ [tank[1]] + dps_teams[2][0], [tank[0]] + dps_teams[2][1] ]]
    
    # find which combination of tank + dps results in the lowest difference
    for teams in teams_with_tank:
        team_1_average = sum(teams[0])/3
        team_2_average = sum(teams[1])/3
        difference = abs(team_1_average - team_2_average)
        if difference < smallest_difference:
            smallest_difference = difference
            team_1 = teams[0]
            team_2 = teams[1]


    # we don't care about supports
    # just optimally balance them and add the higher avg support to the lower avg team
    support = sorted(support)
    if sum(team_1)/3 < sum(team_2)/3:
        team_1 += [support[0], support[3]]
        team_2 += [support[1], support[2]]
    else:
        team_2 += [support[0], support[3]]
        team_1 += [support[1], support[2]]
    

    team_1_average = sum(team_1)/5
    team_2_average = sum(team_2)/5
    return team_1, team_1_average, team_2, team_2_average


print(mm_first_draft(tank, dps, support))