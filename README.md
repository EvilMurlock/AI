# AI I
This repository contains practical tasks for the [Artificial Intelligence 1](http://ktiml.mff.cuni.cz/~bartak/ui/) course, that is based on book by Russel and Norvig [Artificial Intellignece: A Modern Approach, 4th Edition](https://www.pearson.com/us/higher-education/program/Russell-Artificial-Intelligence-A-Modern-Approach-4th-Edition/PGM1263338.html). Tasks are designed to review AI algorithms and use them to play games.

---

## Requirements
All assignments will be written in python. Task were created for python 3.9 however there should not be any problems with backward compatibility. You can solve all assignments while working exclusively with python standard library, however for game visualizations you will need to install modul [pygame](https://www.pygame.org/wiki/GettingStarted).
For installation you can use [pip](https://pypi.org/project/pip/):

    python3 -m pip install -U pygame --user


## Assignments
In total there will be 5 programming assignments whose solutions will be submitted via [ReCodEx](https://recodex.mff.cuni.cz/). In each of them you will write an AI agent that plays suitable games for corresponding lecture topic. Moreover there will by partial assignments, in which you will need to implement algorithms, that will allow you to implement suitable agent functions, however your agent implementation can use any approach you like.

| Game | Suggested Approach |
| ---- | ------ |
| [Dino](dino/README.md) | rule-based agent |
| Pac-Man | uniform-cost search | [//]: # (TODO: [sub-section](./child.md#sub-section) )
| Sokoban | A* with custom heuristics |
| Cell Wars | minimax or Monte Carlo tree search |
| Minesweeper | backtracking search for CSPs |






