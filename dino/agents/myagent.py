#!/usr/bin/env python3
from game.dino import *
from game.agent import Agent
from game import *

class MyAgent(Agent):
    """Reflex agent static class for Dino game."""
    
    # use class variables only for debugging
    debug_txt = None

    def __init__(self) -> None:
        # AGENT WON'T BE INITIALIZED, SO THIS IS FINE
        raise RuntimeError

    @staticmethod
    def GetClosestObstacle(game: Game) -> Obstacle:
        if len(game.obstacles) == 0:
            return None
        closest_ob = None
        curr_distance = 99999
        for o in game.obstacles:
            left_distance = o.rect.x + o.rect.width - game.dino.x
            if(left_distance > 0):
                if left_distance < curr_distance:
                    closest_ob = o
                    curr_distance = left_distance
        # find closest future obstacle
        return closest_ob
    
    @staticmethod
    def get_move(game: Game) -> DinoMove:
        """
        Note: Remember you are creating simple-reflex agent, that should not
        store or access any information except provided.
        """
        # # for visual debugging intellisense you can use
        # from game.debug_game import DebugGame
        # game: DebugGame = game
        # if not hasattr(MyAgent, "debug_txt"):
        #     _ = game.add_text(Coords(10, 10), "red", "Hello World.")
        #     MyAgent.debug_txt = game.add_text(Coords(10, 30), "red", "0")
        # else:
        #     MyAgent.debug_txt.text = str(game.score)
        # game.add_dino_rect(Coords(-10, -10), 150, 150, "yellow")
        # l = game.add_dino_line(Coords(0, 0), Coords(100, 0), "black")
        # l.dxdy.update(50, 30)
        # l.dxdy.x += 50
        # game.add_moving_line(Coords(1000, 100), Coords(1000, 500), "purple")

        # YOUR CODE GOES HERE


        # DUMMY COPPY HERE --------------
        
        if MyAgent.debug:
            from game.debug_game import DebugGame

            game: DebugGame = game
            if MyAgent.debug_txt is None:
                _ = game.add_text(Coords(10, 10), "red", "Hello World.")
                MyAgent.debug_txt = game.add_text(
                    Coords(10, 30), "red", "0"
                )
            else:
                MyAgent.debug_txt.text = str(game.score)
            game.add_dino_rect(Coords(-10, -10), 150, 150, "yellow")
            l = game.add_dino_line(
                Coords(0, 0), Coords(600 // game.speed, 0), "black"
            )
            l.vector.x -= Dino.HEAD_X + game.dino.head.width
            l.dxdy.update(Dino.HEAD_X + game.dino.head.width, 0)
            l.dxdy.y += 50
            if game.score % 20 == 0:
                game.add_moving_line(
                    Coords(1000, 100), Coords(1000, 500), "purple"
                )

        dino = game.dino
        # Dy implementation:
        closest_obstacle = MyAgent.GetClosestObstacle(game)
        if(closest_obstacle == None):
            return DinoMove.NO_MOVE
        
        game.add_moving_line(
            Coords(closest_obstacle.rect.x, closest_obstacle.rect.y), Coords(closest_obstacle.rect.x + closest_obstacle.rect.width, closest_obstacle.rect.y + closest_obstacle.rect.height), "purple"
        )

        if dino.body.y > closest_obstacle.rect.y + closest_obstacle.rect.height:
            return DinoMove.DOWN
        if dino.x + dino.body.width < closest_obstacle.rect.x + 300:
            return DinoMove.UP_RIGHT
        return DinoMove.NO_MOVE
        # more Y means more Down
        # JUMPING CODE
        # DUCKING CODE
        # RETREAT LEFT CODE

        """
        # Dummy implementation:
        x = game.dino.x
        dino_lowest = game.dino.body.y + game.dino.body.height
        for o in game.obstacles:
            if o.rect.x > x and o.rect.x < x + 120 + 5 * (
                game.speed - 5
            ):
                if MyAgent.verbose:
                    print("jumping right")
                return DinoMove.UP
            if dino_lowest < o.rect.y and o.rect.coords.x < x + 150:
                if MyAgent.verbose:
                    print("running right")
                return DinoMove.RIGHT
            if o.rect.x < x and o.rect.x + 105 > x:
                if MyAgent.verbose:
                    print("running right")
                return DinoMove.RIGHT
        """
        