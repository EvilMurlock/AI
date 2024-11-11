#!/usr/bin/env python3
from search_templates import Problem, Solution

import heapq
from typing import Optional

class Node(object):
    def __init__(self, state,actions,cost: int):
        self.cost = cost
        self.state = state
        self.actions = actions
    def __repr__(self):
        return f'Node value: {self.cost}'

    def __lt__(self, other):
        return self.cost < other.cost

def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by AStar search."""
    # Your implementation goes here.

    # return Solution([actions leading to goal], goal_state, path_cost)
    explored_node_count = 0
    collection = []
    collection.append(Node(prob.initial_state(),[],0))
    visited_states = {}
    debug = False
    # USE PRIORITY QUEUE so we can insert based on cost, so our colelction is ordered by cost
    while len(collection) > 0:
        if(debug):
            print("-------------------------------- \n")
            for(state, parent_actions, total_cost) in collection:
                #print("State: " +str(state))
                #print("parent_actions: " +str(parent_actions))
                print("\ntotal_cost: " +str(total_cost))
        """(state, parent_actions, total_cost)""" 
        node = heapq.heappop(collection)#collection.pop()

        explored_node_count+=1
        if(explored_node_count%1000 == 0 and debug):
            print("Node count: "+str(explored_node_count))

        if visited_states.__contains__(node.state):
            #print("Repeating")
            continue
        else:
            visited_states[node.state] = None#[]#node.actions
        

        if(prob.is_goal(node.state)):
            final_actions = node.actions#visited_states[node.state]
            return Solution(final_actions, node.state, node.cost)

        for a in prob.actions(node.state):
            new_state = prob.result(node.state, a)
            cost = prob.cost(node.state, a)
            action_list = node.actions.copy()#visited_states[node.state].copy()
            #print(action_list)
            #print(state)
            action_list.append(a)
            new_cost = node.cost + cost
            #index = whereToInsertBasedOnCost(new_cost, collection)
            heapq.heappush(collection, Node(new_state, action_list, new_cost))

"""
def ucs(prob: Problem) -> Optional[Solution]:
    #Return Solution of the problem solved by UCS search.
    # Your implementation goes here.

    collection = []
    collection.append((prob.initial_state(),[],0))
    visited_states = {}
    debug = False
    # USE PRIORITY QUEUE so we can insert based on cost, so our colelction is ordered by cost
    while len(collection) > 0:
        if(debug):
            print("-------------------------------- \n")
            for(state, parent_actions, total_cost) in collection:
                #print("State: " +str(state))
                #print("parent_actions: " +str(parent_actions))
                print("\ntotal_cost: " +str(total_cost))

        (state, parent_actions, total_cost) = collection.pop()

        if visited_states.__contains__(state):
            #print("Repeating")
            continue
        else:
            visited_states[state] = parent_actions

        if(prob.is_goal(state)):
            final_actions = visited_states[state]
            return Solution(final_actions, state, total_cost)

        for a in prob.actions(state):
            new_state = prob.result(state, a)
            cost = prob.cost(state, a)
            action_list = visited_states[state].copy()
            #print(action_list)
            #print(state)
            action_list.append(a)
            index = whereToInsertBasedOnCost(total_cost+cost, collection)
            collection.insert(index,(new_state, action_list, total_cost+cost))

    
    # Return none when no path to goal
    # run test code: python.exe ucs_test.py
    return None #Solution([actions leading to goal], goal_state, path_cost)
"""