import configparser


class Config:
    def __init__(self, **kwargs):
        self.file_dir = 'config.ini'
        self.config_file = configparser.ConfigParser()
        self.config_file.read(self.file_dir)

        self.window_width = int(self.config_file['Setup']['Width'])
        self.window_height = int(self.config_file['Setup']['Height'])

        self.fps = float(self.config_file['Gameplay']['Fps'])
        self.snake_speed = int(self.config_file['Gameplay']['InitialSnakeSpeed'])
        self.high_score = int(self.config_file['Gameplay']['HighScore'])

        self.fruit_size = int(self.config_file['Settings']['FruitSize'])
        self.snake_size = int(self.config_file['Settings']['SnakeSize'])

        self.move_up = self.config_file['Controls']['MoveUp'].lower()
        self.move_down = self.config_file['Controls']['MoveDown'].lower()
        self.move_left = self.config_file['Controls']['MoveLeft'].lower()
        self.move_right = self.config_file['Controls']['MoveRight'].lower()
        self.restart_game = self.config_file['Controls']['Restart'].lower()

    def write_config_file(self, section, key, value, new_section=False):
        if new_section:
            self.config_file.add_section(section)

        self.config_file.set(section, key, value)

        with open(self.file_dir) as file:
            self.config_file.write(file)
