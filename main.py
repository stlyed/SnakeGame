import random

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import *
from kivy.uix.widget import Widget
from kivy.core.window import Window

from config import Config


class SnakeFruit(Widget, Config):
    def __init__(self, **kwargs):
        super(SnakeFruit, self).__init__(**kwargs)

        # set some default values
        self.size = (self.fruit_size, self.fruit_size)
        self.new_pos()

    def is_collision(self, snake):
        if self.collide_widget(snake):
            return True

    # send the fruit to a random position within the screen
    def new_pos(self, exclude_cords=None):
        def random_x_cord():
            return self.width * round(random.randint(0, self.window_width - self.width) / self.width)

        def random_y_cord():
            return self.width * round(random.randint(0, self.window_height - self.width) / self.width)

        # get a new random position for the fruit
        cords = (random_x_cord(), random_y_cord())

        # exclude_cords: where the snake is located
        # if the new position of the fruit is where the snake is located, get a new position
        if exclude_cords:
            for i in range(len(exclude_cords)):
                if exclude_cords[i].x == cords[0] and exclude_cords[i].x == cords[1]:
                    self.new_pos(exclude_cords)

        self.pos = cords


class SnakeSegment(Widget, Config):
    def __init__(self, **kwargs):
        super(SnakeSegment, self).__init__(**kwargs)

        # set default values
        self.speed = self.snake_speed
        self.size = (self.snake_size, self.snake_size)
        self.new_pos()

    # send the fruit to a random position within the screen
    def new_pos(self):
        possible_x = self.width * round(random.randint(0, self.window_width - self.width) / self.width)
        possible_y = self.width * round(random.randint(0, self.window_height - self.width) / self.width)
        self.pos = (possible_x, possible_y)

    def move(self, x, y):
        self.x += x
        self.y += y


# overall logic for the game
class SnakeGame(Widget, Config):
    score = NumericProperty(0)
    message = StringProperty()

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        # for keyboard events
        Window.bind(on_key_down=self.keyboard_event)
        # set the window to the correct size
        Window.size = (self.window_width, self.window_height)
        # run the update function with an interval based on fps value
        Clock.schedule_interval(self.update, 1 / self.fps)

        # set some default values for the snake
        self.original_speed = self.snake_speed
        self.direction = [0, 0]
        self.snake_segments = []
        self.is_running = True if (self.direction[0] == self.direction[0]) else False

        # add a segment to the snake
        # self.add_snake_segment()

    def add_snake_segment(self):
        new_segment = SnakeSegment()
        self.add_widget(new_segment)
        self.snake_segments.append(new_segment)

    def restart(self):
        # reset the score
        self.score = 0
        # reset the position of snake and fruit
        self.fruit.new_pos(self.snake_segments)
        self.snake.new_pos()
        # delete the old snake
        for i in range(len(self.snake_segments)):
            self.remove_widget(self.snake_segments[i])
        self.snake_segments = []
        # set the speed of the snake back to original speed
        self.snake_speed = self.original_speed
        # make sure the snake is standing still
        self.direction = [0, 0]
        self.is_running = True

    # miscellaneous functions that are very important
    def update(self, *args):
        if self.is_running:
            # remove any messages from the screen
            self.message = ''

            # check for collision between snake and fruit
            if self.fruit.x == self.snake.x and self.fruit.y == self.snake.y:
                self.score += 1
                self.fruit.new_pos(self.snake_segments)
                self.add_snake_segment()

            # check for collision between snake and the right side of the screen
            if self.snake.x + self.direction[0] >= self.width:
                self.direction[0] = 0
                self.is_running = False
            # check for collision between snake and the left side of the screen
            if self.snake.x - self.direction[0] <= self.snake.width and self.direction[0] < 0:
                self.direction[1] = 0
                self.is_running = False
            # check for collision between snake and the top of the screen
            if self.snake.y + self.direction[1] >= self.height:
                self.direction[1] = 0
                self.is_running = False
            # check for collision between snake and the bottom of the screen
            if self.snake.y - self.direction[1] <= self.snake.height and self.direction[1] < 0:
                self.direction[1] = 0
                self.is_running = False

            # check for collision between snake and a snake segment
            for i in range(len(self.snake_segments) - 1):
                if self.snake_segments[i].x == self.snake.x and self.snake_segments[i].y == self.snake.y:
                    self.is_running = False

            if self.snake_segments:
                # make all segments follow each other starting from the back
                for i in range(len(self.snake_segments) - 1, 0, -1):
                    self.snake_segments[i].pos = (self.snake_segments[i - 1].x, self.snake_segments[i - 1].y)
                # the second segment will have the same coordinates as the head
                self.snake_segments[0].pos = (self.snake.x, self.snake.y)

            # constantly move the snake
            self.snake.move(self.direction[0], self.direction[1])

        else:
            self.message = '               Game Over \n' \
                           f'Press the \"{self.restart_game.upper()}\" key to restart!'
            self.message_label.center_x += 0

    # keyboard events
    def keyboard_event(self, *args):
        key_code = list(args)[3]
        # listen for controls from user while the game is running
        if self.is_running:
            # if the user press the key to move towards a direction,
            # and they are not currently moving in the opposite direction
            if key_code == self.move_up and self.direction[1] == 0:
                self.direction = [0, self.snake_speed]
            elif key_code == self.move_down and self.direction[1] == 0:
                self.direction = [0, (self.snake_speed * -1)]
            elif key_code == self.move_right and self.direction[0] == 0:
                self.direction = [self.snake_speed, 0]
            elif key_code == self.move_left and self.direction[0] == 0:
                self.direction = [(self.snake_speed * -1), 0]

        if not self.is_running:
            if key_code == self.restart_game:
                self.restart()


class SnakeApp(App):
    def build(self):
        snakeGame = SnakeGame()
        return snakeGame


if __name__ == '__main__':
    SnakeApp().run()


# TODO: save high score
# TODO: Make game over label above snake and fruit
# TODO: Make snake go faster as time goes by
# FIXME: death if you change direction too fast
