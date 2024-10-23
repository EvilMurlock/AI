#!/usr/bin/env python3
from search_templates import Problem, Solution
from typing import Optional


def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by UCS search."""
    # Your implementation goes here.

    collection = []
    collection.append((prob.initial_state(),[]))
    visited_states = {}

    # USE PRIORITY QUEUE so we can insert based on cost, so our colelction is ordered by cost
    while len(collection) > 0:
        (state, parent_actions) = collection.pop()
        if visited_states.__contains__(state):
            continue
        else:
            visited_states[state] = parent_actions

        if(prob.is_goal(state)):
            final_actions = visited_states[state]
            final_cost = 0
            for a in final_actions:
                final_cost += prob.cost(a)
            return Solution(final_actions, state, final_cost)

        for a in prob.actions(state):
            new_state = prob.result(state, a)
            cost = prob.cost(state, a)
            action_list = visited_states[state]
            action_list.append(a)
            collection.append((new_state, action_list.append(a)))

    
    # Return none when no path to goal
    # run test code: python.exe ucs_test.py
    return None #Solution([actions leading to goal], goal_state, path_cost)
