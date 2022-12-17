import copy
import math
import random


# find the most suitable depth according to the total number of tokens and throw number left
def best_depth(state):
    token_num = len(state["upper"]) + len(state["lower"])
    throw_num = state["upThrow"] + state["lowThrow"]
    if throw_num == 18:
        if 0 <= token_num <= 3:
            return 5
        if 4 <= token_num <= 6:
            return 4
        if 7 <= token_num <= 9:
            return 3
        if 8 <= token_num:
            return 2
    
    return 2

def end_game(state):
    if win_game(state, "upper") or win_game(state, "lower"):
        return True 
    return False

def ab_minimax(state, color, depth, alpha, beta, maxPlayer, playerColor):
    # base case
    if depth == 0 or end_game(state):
        # state = remove_beaten(state)
        # eva = evaluate(state, playerColor)
        # print(eva[0],eva[1])
        return evaluate(state, playerColor)
    
    # player case
    if maxPlayer:
        state = remove_beaten(state)
        maxEval = [-9999, state]
        actions = find_actions(state, color)
        # print(actions)
        for action in actions: 
            # print(123)
            child_state = apply_action(copy.deepcopy(state), color, action)
            # print(child_state["action"])
            if color == "upper":
                new_color = "lower"
            else:
                new_color = "upper"
            evaluation = ab_minimax(child_state, new_color, depth - 1, alpha, beta, False, playerColor)
            if evaluation[0] >= maxEval[0]:
                maxEval[0] = evaluation[0]
                maxEval[1] = evaluation[1]
            alpha = max(alpha, evaluation[0])
            if beta <= alpha:
                break
        return maxEval
    # opponent case
    else:
        minEval = [9999,state]
        actions = find_actions(state, color)
        for action in actions:
            # print(456)
            child_state = apply_action(copy.deepcopy(state), color, action)
            # print(child_state["action"])
            if color == "upper":
                new_color = "lower"
            else:
                new_color = "upper"
            evaluation = ab_minimax(child_state, new_color, depth - 1, alpha, beta, True, playerColor)
            if evaluation[0] <= minEval[0]:
                minEval[0] = evaluation[0]
                minEval[1] = evaluation[1]
            beta = min(beta, evaluation[0])
            if beta <= alpha:
                break
        return minEval


# apply action to state base on color
def apply_action(state, color, action):
    if len(state["action"]) == 0:
        state["action"].append(action)
    if action[0] == "THROW":
        state[color].append((action[1], action[2]))
        if color == "upper":
            state["upThrow"] += 1
        else:
            state["lowThrow"] += 1
    elif action[0] == "SLIDE" or action[0] == "SWING":
        for token in state[color]:
            if token[1] == action[1]:
                token[1] == action[2]
                break
    return state


# this function returns a list consists of all possible actions
def find_actions(state, color):
    # list all available throw positions
    avail_throws = []
    avail_slides = []
    avail_swings = []
    # add available positions for throw action to avail_throws
    for i in range(-4, 5):
        if color == "upper" and i + state["upThrow"] >= 4 and state["upThrow"] < 9:
            for j in range(-4, 5):
                if i + j <= 4 and i + j >= -4:
                    avail_throws.append(("THROW", "r", (i, j)))
                    avail_throws.append(("THROW", "p", (i, j)))
                    avail_throws.append(("THROW", "s", (i, j)))
                    
        elif color == "lower" and state["lowThrow"] - i >= 4 and state["lowThrow"] < 9:
            for j in range(-4, 5):
                if i + j <= 4 and i + j >= -4:
                    avail_throws.append(("THROW", "r", (i, j)))
                    avail_throws.append(("THROW", "p", (i, j)))
                    avail_throws.append(("THROW", "s", (i, j)))

    # add available slide actions to avail_slides
    for token in state[color]:
        hexes = adjacent_hexes(token[1][0], token[1][1])
        for hex in hexes:
            avail_slides.append(("SLIDE", token[1], hex))
    
    # add available swing actions to avail_swings
    for token1 in state[color]:
        for token2 in state[color]:
            if is_adjacent(token1[1], token2[1]):
                remove_lst = []
                hexes1 = adjacent_hexes(token1[1][0], token1[1][1])
                hexes2 = adjacent_hexes(token2[1][0], token2[1][1])
                # add the positions that can be "slide" to to remove_lst
                for hex in hexes2:
                    if hex in hexes1:
                        remove_lst.append(hex)
                # remove hexes in hexes2 that exist in remove_lst
                for hex in remove_lst:
                    hexes2.remove(hex)
                # remove the current position 
                hexes2.remove((token1[1][0], token1[1][1]))
                for hex in hexes2:
                    avail_swings.append(("SWING", token1[1], hex))

    avail_throws = list(set(avail_throws))
    avail_slides = list(set(avail_slides))
    avail_swings = list(set(avail_swings))

    return avail_throws + avail_slides + avail_swings


# returns all positions adjacent to (r, q)
def adjacent_hexes(r, q):
    upper_bound = 4 
    lower_bound = -4
    hexes = [(r + 1, q), (r - 1, q), (r, q + 1), (r, q - 1), (r + 1, q - 1), (r - 1, q + 1)]
    appli_hexes = []

    for item in hexes:
        if not (item[0] > upper_bound or item[0] < lower_bound or item[1] > upper_bound or item[1] < lower_bound or item[0] + item[1] > upper_bound or item[0] + item[1] < lower_bound):
            appli_hexes.append(item)
    return appli_hexes

# this function checks if p1 and p2 are adjacent
def is_adjacent(p1, p2):
    if p1[0] == p2[0]:
        if p1[1] + 1 == p2[1] or p1[1] - 1 == p2[1]:
            return True
    elif p1[1] == p2[1]:
        if p1[0] + 1 == p2[0] or p1[0] - 1 == p2[0]:
            return True
    elif p1[0] + 1 == p2[0] and p1[1] - 1 == p2[1]:
        return True
    elif p1[0] - 1 == p2[0] and p1[1] + 1 == p2[1]:
        return True
    
    return False


def evaluate(state, player):
    colors = ["upper", "lower"]
    opponent = colors.remove(player)
    opponent = colors[0]

    # Feature 1 and Feature 2: player's and opponent's throw left
    if player == "upper":
        p_throw = 9 - state["upThrow"]
        o_throw = 9 - state["lowThrow"]
    else:
        p_throw = 9 - state["lowThrow"]
        o_throw = 9 - state["upThrow"]
    
    # Feature 3 and Feature 4: player's and opponent's token number on board
    p_token_num = len(state[player])
    o_token_num = len(state[opponent])

    # Feature 5: number of kills of opponent's token by player
    count = 0 
    found = False
    for i in range(len(state[player])):
        for j in range(len(state[opponent])):
            if not found and state[player][i][1] == state[opponent][j][1] and battle(state[player][i][0], state[opponent][j][0]):
                found = True
                for k in range(len(state[opponent])):
                   if state[opponent][k] == state[opponent][j]:
                       count += 1
    p_kill_num = count
    
    # Feature 6: number of kills of player's token by opponent
    count = 0 
    found = False
    for i in range(len(state[opponent])):
        for j in range(len(state[player])):
            if not found and state[opponent][i][1] == state[player][j][1] and battle(state[opponent][i][0], state[player][j][0]):
                found = True
                for k in range(len(state[player])):
                   if state[player][k] == state[player][j]:
                       count += 1
    o_kill_num = count

    # Feature 7: player wins
    p_wins = 0
    if win_game(state, player):
        p_wins = 1
    
    # Feature 8: opponent wins
    o_wins = 0
    if win_game(state, opponent):
        o_wins = 1

    # Feature 9: player can still win
    p_rps = []
    o_rps = []
    for token in state[player]:
        if token[0] not in p_rps:
            p_rps.append(token[0])
    for token in state[opponent]:
        if token[0] not in o_rps:
            o_rps.append(token[0])
    lst = []
    for i in o_rps:
        for j in p_rps:
            if battle(j, i):
                lst.append(i)
                break
    if len(lst) == len(o_rps):
        p_winnable = 1
    else:
        p_winnable = 0

    # Feature 10: opponent can still win
    p_rps = []
    o_rps = []
    for token in state[player]:
        if token[0] not in p_rps:
            p_rps.append(token[0])
    for token in state[opponent]:
        if token[0] not in o_rps:
            o_rps.append(token[0])
    lst = []
    for i in p_rps:
        for j in o_rps:
            if battle(j, i):
                lst.append(i)
                break
    if len(lst) == len(p_rps):
        o_winnable = 1
    else:
        o_winnable = 0

    # Feature 11: Kill number of player by itself
    found = False
    p_kill_self_num = 0
    for i in range(len(state[player])):
        if not found:
            for j in range(len(state[player])):
                if state[player][i][1] == state[player][j][1] and battle(state[player][i][0], state[player][j][0]):
                    for token in state[player]:
                        if token == state[player][j]:
                            p_kill_self_num += 1
                    found = True
                    break 
    
    # Feature 12: Kill number of opponent by itself
    found = False
    o_kill_self_num = 0
    for i in range(len(state[opponent])):
        if not found:
            for j in range(len(state[opponent])):
                if state[opponent][i][1] == state[opponent][j][1] and battle(state[opponent][i][0], state[opponent][j][0]):
                    for token in state[opponent]:
                        if token == state[opponent][j]:
                            o_kill_self_num += 1
                    found = True
                    break 
    
    # Feature 13: player's closest distance to its beatable token
    p_distance = 0
    for token in state[player]:
        distance = closest_target_distance(token, state[opponent])
        if distance == 999:
            # p_distance -= 9
            continue
        else:
            p_distance += (9 - distance)

    # Feature 14: opponent's closest distance to its beatable token
    o_distance = 0
    for token in state[opponent]:
        distance = closest_target_distance(token, state[player])
        if distance == 999:
            # o_distance -= 9
            continue
        else:
            o_distance += (4 - distance)

    weight = [30, 5, 10, 999, 5, 10, 5]

    evaluate = (weight[0]*(p_throw - o_throw) + weight[1]*(p_token_num - o_token_num) +  
        weight[2]*(p_kill_num - o_kill_num) + weight[3]*(p_wins - o_wins) +  
        weight[4]*(p_winnable - o_winnable) - weight[5]*(p_kill_self_num - o_kill_self_num) + 
        weight[6]*(p_distance ))
    
    return (evaluate, state)

# returns true if player wins the game
def win_game(state, player):
    colors = ["upper", "lower"]
    opponent = colors.remove(player)
    opponent = colors[0]

    if player == "upper":
        o_throw = "lowThrow"
    else:
        o_throw = "upThrow"

    if not state[o_throw] == 9:
        return False
    elif len(state[opponent]) == 0:
        return True
    # if opponent only contains one type of token
    elif one_kind(state[opponent]) and len(state[opponent]) == 1:
        for i in range(len(state[player])):
            if battle(state[player][i][0], state[opponent][0][0]):
                return True
    return False

# returns true if tokens contains only one kind of token
def one_kind(tokens):
    if len(tokens) == 1:
        return True
    else:
        contains = tokens[0][0]
        for i in range(1, len(tokens)):
            if tokens[i][0] != contains:
                return False
    return True


def closest_target_distance(my_token, enemy_tokens):
    target_hx = 999

    for i in range(len(enemy_tokens)):
        if battle(my_token[0],enemy_tokens[i][0]):
            curr_hx = math.sqrt(math.pow(my_token[1][0] - enemy_tokens[i][1][0], 2) +
                                math.pow(my_token[1][1] - enemy_tokens[i][1][1], 2))
            if curr_hx < target_hx:
                if battle(my_token[0],enemy_tokens[i][0]):
                    target_hx = curr_hx

        return target_hx
'''
*********************** below functions are for update *****************************
'''

# make moves base on the actions 
def do_actions(state, color, opponent_action, player_action):
    colors = ["upper", "lower"]
    opponent = colors.remove(color)
    opponent = colors[0]

    # update player side 
    if player_action[0] == "THROW":
            state[color].append((player_action[1], player_action[2]))
            # update number of throws left
            if opponent == "upper":
                state["lowThrow"] += 1
            else:
                state["upThrow"] += 1
    elif player_action[0] == "SLIDE" or player_action[0] == "SWING":
        for token in state[color]:
            if token[1] == player_action[1]:
                state[color].remove(token)
                state[color].append((token[0], player_action[2]))
                break
    # update opponent side
    if opponent_action[0] == "THROW":
            state[opponent].append((opponent_action[1], opponent_action[2]))
            if opponent == "lower":
                state["lowThrow"] += 1
            else:
                state["upThrow"] += 1
    elif opponent_action[0] == "SLIDE" or opponent_action[0] == "SWING":
        for token in state[opponent]:
            if token[1] == opponent_action[1]:
                state[opponent].remove(token)
                state[opponent].append((token[0], opponent_action[2]))
                break
    return state

# remove all beaten tokens 
def remove_beaten(state):
    temp_lst = [] 
    # store all tokens into temp_lst
    for upper in state["upper"]:
        new = (upper[0].upper(), upper[1]) 
        temp_lst.append(new)
    for lower in state["lower"]:
        temp_lst.append(copy.deepcopy(lower))

    new_lst = []
    comparison_lst = []
    coordinate_lst =  [] 
    # store all coordinats to coordinate_lst with no duplicates 
    for i in temp_lst:
        if i[1] not in coordinate_lst:
            coordinate_lst.append(i[1])

    # according to each unique coordinate, append all tokens on that point to comparison_lst then battle
    for coor in coordinate_lst:
        for token in temp_lst:
            if token[1] == coor:
                comparison_lst.append(token)

        # remaing is the remaining tokens on the same position after battle
        remaining = battle_in_the_hex(comparison_lst) #[(('p',1,2))]
        # append all tokens in remaining to new_lst
        for i in remaining:
            new_lst.append(i)
        # reset comparison_lst
        comparison_lst = []
    
    # empty the tokens on both sides then assign all tokens remain in new_lst back to the state
    state["upper"] = []
    state["lower"] = []
    for i in new_lst:
        if i[0] == "R" or i[0] == "P" or i[0] == "S":
            new = (i[0].lower(),i[1])
            state["upper"].append(new)
        else:
            state["lower"].append(i)
    
    return state

def battle_in_the_hex(lst):
    # Firstly check if the hex contains at least one rock, one paper and one scissor
    rock = 0
    paper = 0
    scissor = 0
    new_lst = []
    for i in lst:
        if i[0] == 'R' or i[0] == 'r':
            rock += 1
        if i[0] == 'P' or i[0] == 'p':
            paper += 1
        if i[0] == 'S' or i[0] == 's':
            scissor += 1
    if rock > 0 and scissor >0 and paper >0:
        return new_lst
    # only scissors and papers
    elif scissor>0 and paper>0 and rock == 0:
        for i in lst:
            if i[0] == 'S' or i[0] == 's':
                new_lst.append(i)
    # only papers and rocks
    elif rock>0 and paper>0 and scissor == 0:
        for i in lst:
            if i[0] == 'P' or i[0] == 'p':
                new_lst.append(i)
    # only rocks and scissors
    elif scissor>0 and rock>0 and paper == 0:
        for i in lst:
            if i[0] == 'R' or i[0] == 'r':
                new_lst.append(i)
    else:
        for i in lst:
            new_lst.append(i)
    return new_lst

# return true only if p1 beats p2
def battle(p1, p2):
    if p1 == 'p' and p2 == 'r':
        return True
    if p1 == 'r' and p2 == 's':
        return True
    if p1 == 's' and p2 == 'p':
        return True
    if p1 == 'P' and p2 == 'r':
        return True
    if p1 == 'R' and p2 == 's':
        return True
    if p1 == 'S' and p2 == 'p':
        return True
    if p1 == 'P' and p2 == 'R':
        return True
    if p1 == 'R' and p2 == 'S':
        return True
    if p1 == 'S' and p2 == 'P':
        return True
    if p1 == 'p' and p2 == 'R':
        return True
    if p1 == 'r' and p2 == 'S':
        return True
    if p1 == 's' and p2 == 'P':
        return True

    return False

def in_danger(state,color):
    if color == "upper":
        opponent = 'lower'
    else:
        opponent = 'upper'
    for token in state[color]:
        for enemy in state[opponent]:
            if battle(enemy[0],token[0]) and is_adjacent(token[1],enemy[1]):
                direction = run_away(token[1],enemy[1])
                return ('SLIDE', token[1],direction)
    return False

def run_away(loc1,loc2):
    hexes = adjacent_hexes(loc1[0],loc1[1])
    lst = []
    for hex in hexes:
        if (math.sqrt(math.pow(hex[0] - loc2[0], 2) +
                                math.pow(hex[1] - loc2[1], 2))) >= math.sqrt(2):
            lst.append(hex)
    if lst != []:
        return random.choice(lst)
    else:
        hexes.remove(loc2)
        for hex in hexes:
            lst.append(hex)
        return random.choice(lst)
    

def direct_eat(state,color):
    if color == "upper":
        opponent = 'lower'
    else:
        opponent = 'upper'
    for token in state[color]:
        for enemy in state[opponent]:
            if battle(token[0],enemy[0]) and is_adjacent(token[1],enemy[1]):
                return ('SLIDE', token[1],enemy[1])
    return False

def direct_throw(state,color):
    if color == "upper":
        opponent = 'lower'
    else:
        opponent = 'upper'
    actions = find_actions(state, color)
    for action in actions:
        if action[0] == "TRHOW":
            for token in state[opponent]:
                if battle(action[1], token[0]) and action[2] == token[1]:
                    return action
    return False

def chase(state,color):
    if color == "upper":
        opponent = 'lower'
    else:
        opponent = 'upper'
    actions = find_actions(state,color)
    for token in state[color]:
        target_hexes = two_hexes_away(token[1][0], token[1][1])
        lst = []
        for i in state[opponent]:
            if i[1] in target_hexes:
                lst.append(i)
        for hex in lst:
            if battle(token[0],hex[0]):
                if ('SWING',token[1],hex[1]) in actions:
                    return ('SWING',token[1],hex[1])
                else:
                    # check whether chasing this token is likely to be killed
                    surrounding = adjacent_hexes(hex[1][0], hex[1][1])
                    for i in range(len(surrounding)):
                        if (defeat(token[0]), (surrounding[i][0],surrounding[i][1])) in state[opponent]:
                            i -= 1
                            break
                    if i == len(surrounding)-1:
                        return move_towards(token[1],hex[1])
    return False
                    

def two_hexes_away(r,q):
    upper_bound = 4 
    lower_bound = -4
    hexes = [(r + 2, q-2), (r +2 , q-1), (r+2, q ), (r + 1, q + 1), (r , q +2 ), (r - 1, q + 2),
                (r - 2, q + 2), (r - 2, q + 1), (r - 2, q), (r - 1, q - 1), (r , q - 2),(r + 1, q - 2)]
    appli_hexes = []

    for item in hexes:
        if not (item[0] > upper_bound or item[0] < lower_bound or item[1] > upper_bound or item[1] < lower_bound or item[0] + item[1] > upper_bound or item[0] + item[1] < lower_bound):
            appli_hexes.append(item)
    return appli_hexes

def move_towards(loc1,loc2):
    if (loc2[0] - 2 == loc1[0] and loc2[1] == loc1[1]) or (loc2[0] - 2 == loc1[0] and loc2[1] +1 == loc1[1]):
        return ("SLIDE",loc1,(loc1[0]+1, loc1[1]))
    elif (loc2[0] - 2 == loc1[0] and loc2[1] + 2== loc1[1]) or (loc2[0] - 1 == loc1[0] and loc2[1] +2== loc1[1]):
        return ("SLIDE",loc1,(loc1[0]+1, loc1[1]-1))
    elif (loc2[0] == loc1[0] and loc2[1] + 2== loc1[1]) or (loc2[0] + 1 == loc1[0] and loc2[1] +1== loc1[1]):
        return ("SLIDE",loc1,(loc1[0], loc1[1]-1))
    elif (loc2[0] + 2== loc1[0] and loc2[1] == loc1[1]) or (loc2[0] + 2 == loc1[0] and loc2[1] -1== loc1[1]):
        return ("SLIDE",loc1,(loc1[0]-1, loc1[1]))
    elif (loc2[0] + 2== loc1[0] and loc2[1] - 2== loc1[1]) or (loc2[0] + 1 == loc1[0] and loc2[1] -2== loc1[1]):
        return ("SLIDE",loc1,(loc1[0]-1, loc1[1]+1))
    elif (loc2[0] == loc1[0] and loc2[1]-2 == loc1[1]) or (loc2[0] - 1 == loc1[0] and loc2[1] -1== loc1[1]):
        return ("SLIDE",loc1,(loc1[0], loc1[1]+1))

def defeat(a):
    if a == 'p':
        return 's'
    elif a == 'r':
        return 'p'
    else:
        return 'r'
