import random


from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import *
from kivy.properties import *
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.uix.button import MDRectangleFlatButton

from config import Config


class MainMenu(Screen):
    pass


class SettingMenu(Screen):
    pass


class SnakeGame(Screen):
    class Grid(Widget, Config):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.size = [self.widget_size, self.widget_size]
            self.pos = [0, 0]

    class Fruit(Widget, Config):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.size = [self.widget_size, self.widget_size]
            self.new_pos()

        def new_pos(self):
            # random number that is divisible by the width of the fruit, to make sure the fruit is always on a grid
            def random_num(start, end):
                return self.width * round(random.randint(start, end - self.width) / self.width)

            # get a new random position for the fruit
            self.pos = [random_num(0, self.game_width), random_num(0, self.game_height)]

    class Segment(Widget, Config):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            # set default values
            self.speed = self.widget_size
            self.size = [self.widget_size, self.widget_size]
            self.new_pos()

        # change the x and y coordinates of the snake
        def new_pos(self, cords: list = None):
            # random number that is divisible by the width of the snake, to make sure the snake is always on a grid
            def random_num(start, end):
                return self.width * round(random.randint(start, end - self.width) / self.width)

            if cords:
                # if some coordinates where specified, use them
                self.pos = cords
            else:
                # get a new random position for the snake
                self.pos = [random_num(0, self.game_width), random_num(0, self.game_height)]

        # move the snake relatively to its current position
        def move(self, cords):
            self.pos = [self.x + cords[0], self.y + cords[1]]

    class Game(Widget, Config):
        score = NumericProperty(0)
        high_score = NumericProperty(0)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # add a fruit, a snake and the background grid
            self.fruit = SnakeGame.Fruit()
            self.add_widget(self.fruit)
            self.snake = SnakeGame.Segment()
            self.add_widget(self.snake)
            self.create_background_grid()

            # set some variables to use
            self.is_running = None  # 1: game is running, 0: game is pause, -1: game over
            self.snake_segments = None
            self.direction = None
            self.original_speed = self.speed

            # set some widgets that will need to be used
            self.game_over_widget = SnakeGame.GameOver()
            self.try_again_btn = MDRectangleFlatButton(
                text='Try Again',
                theme_text_color='Custom',
                text_color=[1, 1, 1, 1],
                line_color=[1, 1, 1, 1],
                center_x=self.game_width / 3,
                y=self.game_height / 5,
            )
            self.try_again_btn.bind(on_press=self.restart)

            # set the window to the correct size
            Window.size = [self.window_width, self.window_height]
            # run the update function with an interval based on speed of the snake
            self.clock = Clock.schedule_interval(self.update, 1 / self.speed)

            # load and start the game
            self.start()

        def start(self):
            self.fruit.new_pos()
            self.snake.new_pos()

            # set some default values for the snake
            self.direction = [0, 0]
            self.snake_segments = []
            self.speed = self.original_speed
            self.is_running = True

        def restart(self, *args):
            # so pycharm could not show me a warning
            if args:
                pass

            # reset the score
            self.score = 0
            # delete the old snake
            if self.snake_segments:
                for i in range(len(self.snake_segments)):
                    self.remove_widget(self.snake_segments[i])
                self.snake_segments = []

            # remove all widgets from playing area
            self.remove_widget(self.game_over_widget)
            self.remove_widget(self.try_again_btn)

            # start the game
            self.start()

        def game_over(self):
            self.direction = [0, 0]
            self.is_running = -1

            self.add_widget(self.game_over_widget)
            self.add_widget(self.try_again_btn)

        def update(self, *args):
            assert args

            # start listening for keyboard events on this frame
            Window.bind(on_key_down=self.keyboard_event)

            if self.is_running == 1:
                # check for collision between snake and fruit
                if self.fruit.x == self.snake.x and self.fruit.y == self.snake.y:
                    def new_fruit_pos():
                        self.fruit.new_pos()
                        # check if fruit spawn under the snake
                        for i in range(len(self.snake_segments)):
                            if self.fruit.pos == self.snake_segments[i] or self.fruit.pos == self.snake_segments[i - 1]:
                                new_fruit_pos()

                    self.score += 1
                    # update high score if it is bigger than the regular score and write it the file
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.write_config_file('Achievements', 'high_score', str(self.high_score))

                    new_fruit_pos()  # give the snake a new position
                    self.add_snake_segment()
                    self.change_speed()

                # check for collision between snake and the right side of the screen
                if self.snake.x + self.direction[0] >= self.game_width:
                    self.game_over()
                # check for collision between snake and the left side of the screen
                if self.snake.x - self.direction[0] <= self.snake.width and self.direction[0] < 0:
                    self.game_over()
                # check for collision between snake and the top of the screen
                if self.snake.y + self.direction[1] >= self.game_height - self.snake.height:
                    self.game_over()
                # check for collision between snake and the bottom of the screen
                if self.snake.y - self.direction[1] <= self.snake.height and self.direction[1] < 0:
                    self.game_over()

                # check for collision between snake and a snake segment
                for i in range(len(self.snake_segments) - 1):
                    if self.snake_segments[i].x == self.snake.x and self.snake_segments[i].y == self.snake.y:
                        self.game_over()

                if self.snake_segments:
                    # make all segments follow each other starting from the back
                    for i in range(len(self.snake_segments) - 1, 0, -1):
                        self.snake_segments[i].pos = self.snake_segments[i - 1].pos
                    # the second segment will have the same coordinates as the head
                    self.snake_segments[0].new_pos([self.snake.x, self.snake.y])

                # constantly move the snake
                self.snake.move(self.direction)

        def add_snake_segment(self):
            new_segment = SnakeGame.Segment()
            self.add_widget(new_segment)
            self.snake_segments.append(new_segment)

        def change_speed(self, speed: int = None):
            if speed:
                self.speed = self.difficulty
            else:
                self.speed += self.difficulty

            # cancel the saved event
            self.clock.cancel()
            # create a new event
            self.clock = Clock.schedule_interval(self.update, 1 / self.speed)

        def create_background_grid(self):
            for i in range(int(self.game_width // self.widget_size)):
                for j in range(int(self.game_height // self.widget_size)):
                    background_grid = SnakeGame.Grid()
                    background_grid.pos = [i * self.widget_size, j * self.widget_size]
                    self.add_widget(background_grid)

        def keyboard_event(self, *args):
            key_code = list(args)[3]
            # listen for controls from user while the game.py is running
            """
            # if the user press the key to move towards a direction,
             and they are not currently moving in the opposite direction
                # stop listening for new keyboard events
                # give instructions in the new direction chosen
            """
            # game is running
            if self.is_running == 1:
                if key_code == self.move_up and self.direction[1] == 0:
                    Window.unbind(on_key_down=self.keyboard_event)
                    self.direction = [0, self.widget_size]
                elif key_code == self.move_down and self.direction[1] == 0:
                    Window.unbind(on_key_down=self.keyboard_event)
                    self.direction = [0, (self.widget_size * -1)]
                elif key_code == self.move_right and self.direction[0] == 0:
                    Window.unbind(on_key_down=self.keyboard_event)
                    self.direction = [self.widget_size, 0]
                elif key_code == self.move_left and self.direction[0] == 0:
                    Window.unbind(on_key_down=self.keyboard_event)
                    self.direction = [(self.widget_size * -1), 0]
            # game is paused
            elif self.is_running == 0:
                if key_code == self.restart_game:
                    self.restart()

            # game is over, you lost
            elif self.is_running == -1:
                if key_code == self.restart_game:
                    self.restart()

    class GameOver(Widget, Config):
        title = StringProperty()
        subtitle = StringProperty()

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.size = [self.game_width, self.game_height]
            self.title = 'Game Over!'
            self.subtitle = f'Press {self.restart_game} to play Again'


class WindowManager(ScreenManager):
    pass


class SnakeApp(MDApp):
    def build(self):
        return Builder.load_file('main.kv')


if __name__ == '__main__':
    SnakeApp().run()
