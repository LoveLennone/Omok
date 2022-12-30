# featureExtractors.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"Feature extractors for Pacman game states"

#from game import Directions, Actions
import util
import gameState

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        features = util.Counter()
        features["bias"] = 1.0 #0.0 #self.scoreEvaluationFunction(state)

        features["black-1"] = 0.0
        features["black-2"] = 0.0
        features["black-3"] = 0.0
        features["black-4"] = 0.0
        features["black-5"] = 0.0

        features["white-1"] = 0.0
        features["white-2"] = 0.0
        features["white-3"] = 0.0
        features["white-4"] = 0.0
        features["white-5"] = 0.0
       
        ori_x, ori_y = action
        black = 0
        white = 0

        map = gameState.Grid(state.dimension, state.dimension)
        for row in range(state.dimension):
            for col in range(state.dimension):
                if state.getColor(row, col) == 'black':
                    map[col][row] = 'x'
                    black += 1
                elif state.getColor(row, col) == 'white':
                    map[col][row] = 'o'
                    white += 1
                else:
                    map[col][row] = 'F'
                  
        map[ori_y][ori_x] = 'x' if black == white else 'o'
        # print(map)
        # print("===================================")

        #ori_x, ori_y = x, y
        n_dx = [0, 0, 1, -1, -1, 1, -1, 1]
        n_dy = [-1, 1, -1, 1, 0, 0, -1, 1]
        window = [0, 0, 0, 0, 0]
        #print(stone, self.matrix[x][y].get_color())

        for y in range(2, state.dimension-2):
            for x in range(2, state.dimension-2):
                if map[y][x] != 'F':
                    #print(y, x)
                    winCnt = 0
                    window[winCnt] = map[y][x]
                    
                    for direct in range(0, len(n_dy), 2):
                        winCnt = 1
                        for next in range(direct, direct + 2):
                            dx, dy = n_dx[next], n_dy[next]
                            cnt = 1
                            while cnt < 3:
                                temp_x, temp_y = x + dx * cnt, y + dy * cnt
                                #print(temp_x, temp_y)
                                window[winCnt] = map[temp_y][temp_x]
                                cnt += 1
                                winCnt += 1

                        num = self.checkWindow(window)
                        if num > 0:
                            key = self.updateFeatures(window[0], num)
                            features[key] += 0.7

        return features

    def checkWindow(self, window):
        cnt = 1
        for i in range(1, 5):
            if window[i] == 'F':
                continue
            elif window[i] == window[0]:
                cnt += 1
            else:
                cnt = 0
                break 
        return cnt

    def updateFeatures(self, color, num):
        if color == 'x':
            key = "black-" + str(num)
        else:
            key = "white-" + str(num)

        #print(key)
        return key

    def scoreEvaluationFunction(self, currentGameState):
        """
        This default evaluation function just returns the score of the state.
        The score is the same one displayed in the Omok GUI.

        This evaluation function is meant for use with adversarial search agents
        """
        tmp = [[0 for x in range(currentGameState.dimension)] for y in range(currentGameState.dimension)] #currentGameState.__str__()
        n_dx = [0, 0, 1, -1, -1, 1, -1, 1]
        n_dy = [-1, 1, -1, 1, 0, 0, -1, 1]

        ans = 0

        for y in range(0, currentGameState.dimension):
            for x in range(0, currentGameState.dimension):
                tmp[y][x] = currentGameState.getColor(y, x)

                if currentGameState.getColor(y, x) == None:
                    sum = 0

                    for next in range(0, len(n_dy)):
                        cnt = 0
                        dx, dy = x + n_dx[next], y + n_dy[next]
                        if currentGameState.getColor(dy, dx) == 'black':
                            cnt = 1.0
                            while True:
                                dx, dy = dx + n_dx[next], dy + n_dy[next]
                                
                                if currentGameState.checkLocation(dx, dy, currentGameState.dimension) == False or currentGameState.getColor(dy, dx) == None:
                                    break
                                elif currentGameState.getColor(dy, dx) == 'black':
                                    cnt *= 2
                                else:
                                    cnt /= 2
                                    break
                        elif currentGameState.getColor(dy, dx) == 'white':
                            cnt = -0.99
                            while True:
                                dx, dy = dx + n_dx[next], dy + n_dy[next]
                                
                                if currentGameState.checkLocation(dx, dy, currentGameState.dimension) == False or currentGameState.getColor(dy, dx) == None:
                                    break
                                elif currentGameState.getColor(dy, dx) == 'white':
                                    cnt *= 2
                                else:
                                    cnt /= 2
                                    break
                        sum += cnt
                    tmp[y][x] = sum
                    ans += sum

        return ans


class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features
