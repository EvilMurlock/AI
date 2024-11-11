#!/usr/bin/env python3
from game.controllers import PacManControllerBase
from game.pacman import Game, DM, Direction
from typing import List
import sys
from os.path import dirname

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(__file__))))
from search_templates import *
from ucs import ucs



class PacProblem(Problem):

    ghost_presence_cost_scaling = 1000
    undersirable_ghost_distance = 30
    undersirable_ghost_cost_multi = 1
    penalty_power = 4
    undersirable_ghost_flat_cost = 0

    ghost_eat_distance = 100
    fruit_eat_distance = 60
    ghost_distance_to_eat_pill = 8
    def __init__(self, game: Game) -> None:
        self.game: Game = game
        


    #def initial_state(self) -> int:
    #    return self.game.pac_loc
    def initial_state(self) -> [int]:
        return tuple([self.game.pac_loc]+self.game.ghost_locs + [0])
    
    #def actions(self, state: int) -> List[int]:
    #    return [0,1,2,3]
    def actions(self, state: [int]) -> List[int]:
        return [0,1,2,3]
    #def result(self, state: int, action: int) -> int:
    #    return self.game.get_neighbor(state, action)

    def result(self, state: [int], action: int) -> [int]:
        nextState = [0]*6
        nextState[0] = self.game.get_neighbor(state[0], action)
        for i in range(0,4):
            closer = True
            if(self.game.edible_times[i] > 0):
                closer = False
            #dist_func = self.game.get_distance_function(DM.PATH)
            direction = self.game.get_next_ghost_dir(i, state[0], closer, DM.PATH)
            #nextState[i+1] = state[i+1] 
            if(direction == -1):
                nextState[i+1] = state[i+1] 
            else:
                nextState[i+1] = self.game.get_ghost_neighbors(i)[direction] # predict ghost movement # right now disabled, because pacman and ghosts might jupm over each other
            #nextState[i+1] = self.game.get_ghost_neighbors(i)[self.game.ghost_dirs[i]]
        nextState[5] = state[5]
        return tuple(nextState)
    
    """
    def is_goal(self, state: int) -> bool:
        #pill_on_node = self.game.get_pill_node(state)
        pill_index = self.game.get_pill_index(state)
        if(pill_index == -1):
            return False
        if(self.game.check_pill(pill_index)):
            return True
        return False
    """
    def are_edible_ghosts_close(self, state):
        for i in range(0,4):
            if(self.game.is_in_lair(i)):
                continue
            if(self.game.edible_times[i]>0
               and self.game.get_path_distance(state[0], state[i+1]) < self.ghost_eat_distance):
                return True
            
        return False
    
    def fruit_is_close(self, state):
        fruit_position = self.game.fruit_loc
        if(fruit_position != -1 and self.game.get_path_distance(state[0], fruit_position) < self.fruit_eat_distance):
            return True
        return False
    def colliding_with_big_pill(self, state):
        index = self.game.get_power_pill_index(state[0])
        if(index==-1):
            return False
        
        if(self.game.check_power_pill(index)):
            return True
        return False

    def any_ghost_power_pill_close(self, state):
        for i in range(0,4):
            if(self.game.get_path_distance(state[0], state[1+i]) < self.ghost_distance_to_eat_pill):
                return True
        return False

    def is_goal(self, state: [int]) -> bool:
        #pill_on_node = self.game.get_pill_node(state)
        
        if(not self.are_edible_ghosts_close(state) and #disables dot eating when edible ghost is close
            not self.fruit_is_close(state)):

            pill_index = self.game.get_pill_index(state[0])
            power_pill_index = self.game.get_power_pill_index(state[0])

            if (pill_index != -1 and
            self.game.check_pill(pill_index)):
                #print("PILL GOAL")
                return True
            if (power_pill_index != -1 and
                self.game.check_power_pill(pill_index) and
                (self.game.get_pills_count() < 10 or
                self.any_ghost_power_pill_close(state))):
                #print("PILL GOAL")
                return True
            


        for i in range(0,4):
            if(self.game.edible_times[i] > 0):
                if(state[0] == state[1+i]):
                    #print("GHOST GOAL")
                    return True

        #if(self.game.edible_times[0] > 0):
        #    if(self.check_ghost_colision(state)):
        #        return True
            
        fruit_position = self.game.fruit_loc
        if(fruit_position != -1 and state[0] == fruit_position and
           not self.are_edible_ghosts_close(state)):
            #print("FRUIT GOAL")
            return True
        
        

        return False
    """
    def cost(self, state: int, action: int) -> float:
        #vraci nejlepsi cestu, ne nejkratsi
        cost = 1 # time
        for index in range(0,4):
            if(self.game.eating_time > 0):
                pass
            else:
                ghost = self.game.get_ghost_loc(index)
                cost += 200/(self.game.get_manhattan_distance(state, ghost)+1)*self.ghost_presence_cost_scaling
            
        return cost
    """
    def check_ghost_colision(self, state):
        if(self.game.get_manhattan_distance(state[0], state[1]) < 3 or
           self.game.get_manhattan_distance(state[0], state[2]) < 3 or
           self.game.get_manhattan_distance(state[0], state[3]) < 3 or
           self.game.get_manhattan_distance(state[0], state[4]) < 3):
            return True
        """
        if(state[0] == state[1] or 
            state[0] == state[2] or
            state[0] == state[3] or
            state[0] == state[4]):
            return True
        """
        return False
    def cost(self, state: [int], action: int) -> float:
        #vraci nejlepsi cestu, ne nejkratsi
        cost = 1 # time
        shouldIEatPill = False
        for i in range(0,4):
            if(self.game.edible_times[i] > 0): # do not add penalty from ghost proximity if ghost edible
                pass
            else:
                #cost += 200/(self.game.get_manhattan_distance(state[0], ghost)+1)*self.ghost_presence_cost_scaling
                if(self.ghost_close(state,i)):
                    distance = self.distance_from_ghost(state,i)
                    penalty = self.undersirable_ghost_distance/(distance+2) * self.undersirable_ghost_cost_multi
                    cost += penalty**self.penalty_power
                    cost += self.undersirable_ghost_flat_cost
                    if(distance < self.ghost_distance_to_eat_pill):
                        shouldIEatPill = True
                    if(self.game.get_manhattan_distance(state[0], state[i+1]) < 3):
                        cost += 10000
        if(not shouldIEatPill and self.colliding_with_big_pill(state)):
            cost += 50 # dont eat the pill if ghost are not close
        return cost
    




    def ghost_close(self, state, ghost_index):
        distance = self.game.get_path_distance(state[0],state[1+ghost_index])
        if(distance < 0):
            return False
        if(distance < self.undersirable_ghost_distance):
            return True

        return False
    def distance_from_ghost(self, state, ghost_index):
        return self.game.get_path_distance(state[0],state[1+ghost_index])

class Agent_Using_UCS(PacManControllerBase):
    def tick(self, game: Game) -> None:
        prob = PacProblem(game)
        sol = ucs(prob)
        if sol is None or not sol.actions:
            pass
            if self.verbose:
                pass
                print("No path found.", file=sys.stderr)
        else:
            self.pacman.set(sol.actions[0])

        
        if(self.verbose):
            #cost = 1 # time
            min_cost = 999
            for index in range(3,4):
                ghost = self.game.get_ghost_loc(index)
                cost = 200/(game.get_manhattan_distance(game.pac_loc, ghost)+1)
                if(min_cost > cost):
                    min_cost = cost
                print(game.get_next_ghost_dir(index, game.pac_loc, True, DM.PATH))
                #print(ghost)
                #print(game.get_manhattan_distance(game.pac_loc, ghost))
                #print(game.edible_times[index])
            #print("Min cost: "+str(cost))
        
        #for i in range (0,4):
        #    print("Ghost " + str(i) + "  -> "+ str(game.get_path_distance(game.pac_loc, game.ghost_locs[i])))
        #if(self.game.edible_times[0] > 0):
        #    print("we are in eating time: "+str(self.game.edible_times[0]))