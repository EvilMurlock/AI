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
    def obstacle_behind_barrier(obstacle):
        barrier_position_guess = 1100 - 350
        if obstacle.rect.x + obstacle.rect.width > barrier_position_guess:
            return True
        else:
            return False
        
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
        
        # My implementation:
        closest_obstacle = MyAgent.GetClosestObstacle(game)
        if(closest_obstacle == None):
            return DinoMove.NO_MOVE
        
        if MyAgent.debug:
            game.add_moving_line(
                Coords(closest_obstacle.rect.x, closest_obstacle.rect.y), Coords(closest_obstacle.rect.x + closest_obstacle.rect.width, closest_obstacle.rect.y + closest_obstacle.rect.height), "purple"
            )
            game.add_moving_line(
                Coords(dino.head.x, dino.head.y), Coords(dino.head.x + dino.head.width, dino.head.y + dino.head.height), "red"
            )
            game.add_moving_line(
                Coords(dino.body.x, dino.body.y), Coords(dino.body.x + dino.body.width, dino.body.y + dino.body.height), "red"
            )
            print("Next OBstacle Behind berrier: "+str(MyAgent.obstacle_behind_barrier(closest_obstacle)))
            #if(not MyAgent.obstacle_behind_barrier(closest_obstacle)):
            game.add_moving_line(
            Coords(1100 - 350,1000), Coords(1100 - 350, -500), "red"
            )
        if dino.Y_DUCK > closest_obstacle.rect.y + closest_obstacle.rect.height:
            
            if(dino.x > game.WIDTH/2 - 300 and dino.jump_vel == 20) or MyAgent.obstacle_behind_barrier(closest_obstacle):
                pass
            #return DinoMove.LEFT
            else:
                pass
                if MyAgent.debug:
                    print("DUCKING RIGHT")
                #return DinoMove.DOWN_RIGHT
            
            return DinoMove.DOWN

        if dino.head.x + dino.head.width > closest_obstacle.rect.x - 50 - game.speed * 5 and not MyAgent.obstacle_behind_barrier(closest_obstacle):
            #print("Distance to obstacle: "+str(dino.head.x + dino.head.width-closest_obstacle.rect.x))



            # RETREAT CHECK (CHICKEN OUT CHECK)
            # END OF CHICKEN CODE

            if MyAgent.debug:
                print("Jumping over obstacle")
            if(dino.body.y + dino.body.height > closest_obstacle.rect.y):
                return DinoMove.UP
            else:
                return DinoMove.RIGHT
        
        if dino.jump_vel > -10 and not MyAgent.obstacle_behind_barrier(closest_obstacle):# and (dino.body.y + dino.body.height > closest_obstacle.rect.y):
            
            if MyAgent.debug:
                print("Double jumping")
                #print("Y Velocity < 0 is = "+ str(dino.jump_vel))

            if dino.head.x + dino.head.width > closest_obstacle.rect.x - 250 - game.speed * 5: # we are close enough to jump over ???MAYBE
                return DinoMove.RIGHT
            
        else:
            if MyAgent.debug:
                print("Retreat check")
            if dino.head.x + dino.head.width >= closest_obstacle.rect.x: # we CANT jump over obstacle, but we are over it
                if MyAgent.debug:
                    print("RETREATING")
                return DinoMove.LEFT
            #if(dino.body.y + dino.body.height - closest_obstacle.rect.y > dino.body.x - (closest_obstacle.rect.x +closest_obstacle.rect.width)):
            #    return DinoMove.RIGHT
            #else:
            #    return DinoMove.LEFT

        """
        if(dino.x > game.WIDTH/2 - 300 and dino.jump_vel == 20) or MyAgent.obstacle_behind_barrier(closest_obstacle):
            pass
            #return DinoMove.LEFT
        else:
            pass
            if MyAgent.debug:
                    print("GOING RIGHT")
        
            return DinoMove.RIGHT
        """
        return DinoMove.NO_MOVE
        # more Y means more Down, more x means more left <===

        