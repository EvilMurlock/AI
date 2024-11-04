#!/usr/bin/env python3
from search_templates import Problem, Solution
from typing import Optional


def whereToInsertBasedOnCost(cost, collection):
    index = 0
    for (x,y , nodeCost) in collection:

        if(cost > nodeCost):
            return index
        index+=1
    return index

def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by UCS search."""
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
